"""
The Emotion chip that Data was looking for this whole time

Unfortunately it was written in Python, so it tended to go a little
haywire.

This module implements the `OldEmotionHeader` class for v2.1 files,
and `EmotionHeader` for v2.5 files. Both classes inherit from the
abstract `EmotionHeaderBase` class which provides common functionality
for both.

Each one of these objects describes one entry in the
pose/gesture/emotion table; meaning it describes either one singular
pose, or for Microsoft-published avatar files, either one face or one
body.
"""

import enum
import logging
import struct
from typing import (
    TYPE_CHECKING,
    Any,
    BinaryIO,
    List,
    Optional,
    Set,
    Tuple,
    Type,
    Union,
    cast,
)

from PIL import ImageChops
from PIL.Image import Image

from .bitmap import PaletteType
from .imgmeta import ImageMetadata
from .table import IMG_TABLE


if TYPE_CHECKING:
    from .binary import Binary
    from .bitmap import Bitmap


_LOG = logging.getLogger(__name__)


class Emotion(enum.IntEnum):
    HAPPY = 1
    COY = 2
    BORED = 3
    SCARED = 4
    SAD = 5
    ANGRY = 6
    SHOUT = 7
    LAUGH = 8
    NEUTRAL = 9
    WAVE = 10
    POINT_TO_OTHER = 11
    POINT_TO_SELF = 12
    # The below emotions aren't accessible via ccedit nor cchat
    DOUBLEPOINT = 13  # mscc 2.5's LANCE
    SHRUG = 14  # mscc 2.5's DAN, SUSAN; and many user-edited files
    _3QRWALK = 15  # mscc 2.5's LANCE
    SIDEWALK = 16  # Not observed in the wild at all
    _3QFWALK = 17  # mscc 2.5's LANCE

    def __str__(self) -> str:
        return self.name.lstrip("_")


class EmotionHeaderBase:
    # pylint: disable=too-many-public-methods

    # okay like. theoretically yes this object is kind of doing too many things but
    # I am bad at OO design and I don't feel like refactoring everything right now, and like.
    # stop judging me, pylint!!!

    def __init__(self, parent: "Binary", field_type: int, n: int) -> None:
        # Metadata
        self._parent = parent
        self.field_type = field_type
        self.n = n

        # Cache: Although imgmeta caches raw images, *these* images
        # are potentially lightly transformed from the raw images in
        # the case of v2.5 avatars where mask + halo data is
        # multiplexed into a single image; also in the rarer case that
        # the mask/halo data is not correctly sized or contains
        # non-monochrome data; see _maskify().
        self._img1: Optional[Image] = None
        self._img2: Optional[Image] = None
        self._img3: Optional[Image] = None

        #####################
        # Actual field data #
        #####################

        # contains offsets, an unknown byte, and an image decoding flag.
        # The unknown byte/flag are only defined for v2.5 files.
        self._imgmeta = [
            ImageMetadata(parent, self.kind()),
            ImageMetadata(parent, "MASK"),
            ImageMetadata(parent, "HALO"),
        ]

        self.emotion: Union[int, Emotion] = 0
        self.intensity = 0
        self.coordinates_1 = (0, 0)  # Can be face center or junction point, depending.

        # Only for 0x04/0x0A (Faces)
        self.coordinates_2 = (0, 0)  # (Junction offset, when defined.)
        self.coordinates_3 = (0, 0)  # (Face center, when defined.)

    @staticmethod
    def describe_field(field_type: int) -> str:
        if field_type not in (0x04, 0x05, 0x09, 0x0A, 0x0B, 0x0C):
            raise ValueError("Unrecognized field type")

        noun = ver = ""
        if field_type in (0x04, 0x0A):
            noun = "Faces"
        if field_type in (0x05, 0x0B):
            noun = "Bodies"
        if field_type in (0x09, 0x0C):
            noun = "Poses"
        if field_type in (0x04, 0x05, 0x09):
            ver = "v2.1"
        if field_type in (0x0A, 0x0B, 0x0C):
            ver = "v2.5"

        assert noun and ver
        return f"{noun} ({ver})"

    @staticmethod
    def get_klass(field_type: int) -> Type["EmotionHeaderBase"]:
        if field_type in (0x04, 0x05, 0x09):
            return OldEmotionHeader
        assert field_type in (0x0A, 0x0B, 0x0C)
        return EmotionHeader

    def _warn(self, msg: str) -> None:
        prefix = f"Emotion {self.field_type:02X}/#{self.n:02d} ({str(self.emotion)}): "
        msg = prefix + msg
        _LOG.warning(msg)

    @property
    def face_coordinates(self) -> Optional[Tuple[int, int]]:
        """
        Return the facial center coordinates, if they exist.

        Faces and poses have facial coordinates, but bodies do
        not. These coordinates are stored in different locations in
        the serialized struct depending on what type of entry this is.

        Faces use the third set of coordinates, poses use the first
        set.
        """
        if self.face_data():
            return self.coordinates_3
        if self.body_data():
            return None
        return self.coordinates_1

    @property
    def junction_point(self) -> Optional[Tuple[int, int]]:
        """
        Return the face/body junction point coordinates.

        Faces and Bodies have junction coordinates, poses do not.
        """
        if self.face_data() or self.body_data():
            return self.coordinates_1
        return None

    @property
    def junction_offset(self) -> Optional[Tuple[int, int]]:
        """
        Return the face junction point offset.

        Only faces have this offset.
        """
        if self.face_data():
            return self.coordinates_2
        return None

    def face_data(self) -> bool:
        """
        True if this data represents a FACE.
        """
        return self.field_type in (0x04, 0x0A)

    def body_data(self) -> bool:
        """
        True if this data represents a BODY.
        """
        return self.field_type in (0x05, 0x0B)

    def kind(self) -> str:
        """
        What kind of data is this?

        :return: "FACE", "BODY", or "POSE".
        """
        if self.face_data():
            return "FACE"
        if self.body_data():
            return "BODY"
        return "POSE"

    def intensity_wire(self) -> int:
        """
        This function computes the intensity of the emotion for
        the MSCC control message wire protocol.

        Each message sent from Comic Chat sends an intensity for the
        emotion, ranging from 0-10 inclusive. Notably, specialty poses
        like Wave, Neutral, Point_to_self, and Point_to_other always
        use 0, but this value can also be used by very "mild"
        expressions/gestures.

        (NOTE: Non-specialty emotions such as Happy/Sad etc cannot use
        a literal intensity of 0x00, that will crash Comic Chat!)

        It is *closely related to*, but *different* from the intensity
        slider visible in CCEdit, which follows a maddening, subtly
        different algorithm.

        This function *is* defined in CChat for all values from 0x00
        to 0xFF, even though only certain values appear in avatars
        made with official editors.

        The table below shows each wire intensity alongside the range
        of actual emotional intensity values that produce that value,
        and the total number of values that map to that single wire
        intensity.

        0:  [0x00 - 0x19]  26
        1:  [0x1A - 0x32]  25
        2:  [0x33 - 0x4C]  26
        3:  [0x4D - 0x65]  25
        4:  [0x66 - 0x7F]  26
        5:  [0x80 - 0x98]  25
        6:  [0x99 - 0xB2]  26
        7:  [0xB3 - 0xCB]  25
        8:  [0xCC - 0xE5]  26
        9:  [0xE6 - 0xFE]  25
        ::  [    0xFF   ]   1

        It's worth noting that the intensity 0xFF produces the wire
        value ":", which is "0" + 10. This function returns an integer
        and not a char, however.
        """
        return int((self.intensity * 10) / 255)

    def intensity_v55(self) -> int:
        """
        Return the CCEdit v55 slider intensity for this emotion.

        Returns a number from 0 to 10, with 0 meaning "low" emotion
        and 10 meaning "high" emotion. This is backwards from the v66
        convention.

        v55 used "1" for low intensity and "10" for maximum
        intensity. However, the literal byte values it chose for the
        emotion intensity had the unfortunate property that they were
        not unique for the wire protocol and had several collisions:

        idx   EI      wire
        -----------------
         0: 0x00  =>  0         (specialty poses)
         1: 0x19  =>  0         (emotion wheel: near the center, low)
         2: 0x33  =>  2
         3: 0x4C  =>  2
         4: 0x66  =>  4
         5: 0x7F  =>  4
         6: 0x99  =>  6
         7: 0xB2  =>  6
         8: 0xCC  =>  8
         9: 0xE5  =>  8
        10: 0xFF  =>  :         (emotion wheel: near the edge, high)

        The mapping function for index to intensity here is:
        f(x) = int(255/10 * x)

        This function performs the inverse and returns the intensity
        index (0-10) for a given emotion intensity.

        For "unusual" intensity values (created by a hex editor or v66
        of CCedit), the numerical indexes returned by this function
        are only hypothetical, since there is no legitimate way to
        produce those values in v55.

        The inverse intensity mapping for this function is:

        [0x00 - 0x18]: 0
        [0x19 - 0x32]: 1
        [0x33 - 0x4B]: 2
        [0x4C - 0x65]: 3
        [0x66 - 0x7E]: 4
        [0x7F - 0x98]: 5
        [0x99 - 0xB1]: 6
        [0xB2 - 0xCB]: 7
        [0xCC - 0xE4]: 8
        [0xE5 - 0xFE]: 9
        [   0xFF    ]: 10

        """
        return int((self.intensity + 0.5) / 25.5)

    def intensity_v66(self) -> int:
        """
        Return the CCEdit v66 slider intensity for this emotion.

        Returns a number from 0 to 10, with 10 meaning "high" emotion
        and 0 meaning "low" emotion. This is backwards from the v55
        convention.

        v66 used "10" for low intensity and "1" for maximum
        intensity. It is inverted from the v55 convention; but avoids
        collisions when mapping to the wire intensity.

        idx   EI      wire
        -----------------
         0: 0x00  =>  0         (specialty poses)
        10: 0x01  =>  0         (emotion wheel: near the center, low)
         9: 0x1B  =>  1
         8: 0x34  =>  2
         7: 0x4E  =>  3
         6: 0x67  =>  4
         5: 0x81  =>  5
         4: 0x9A  =>  6
         3: 0xB4  =>  7
         2: 0xCD  =>  8
         1: 0xE7  =>  9         (emotion wheel: near the edge, high)

        This mapping from index to intensity is:
        f(x) = (256 - int(255/10 * x)) % 256

        Notably, v66 cannot produce the intensity value 0xFF nor the
        wire intensity 10. The slider value of "0" for specialty
        poses is special-cased to the intensity value 0x00.

        Like the v55 function, intensity values outside of the
        well-defined values are hypothetical, since there was no way
        to produce those values with the official v66 editor.

        The inverse intensity mapping for this function is:

        [   0x00    ]: 0
        [0x01 - 0x1A]: 10
        [0x1B - 0x33]: 9
        [0x34 - 0x4D]: 8
        [0x4E - 0x66]: 7
        [0x67 - 0x80]: 6
        [0x81 - 0x99]: 5
        [0x9A - 0xB3]: 4
        [0xB4 - 0xCC]: 3
        [0xCD - 0xE6]: 2
        [0xE7 - 0xFF]: 1

        """
        if self.intensity == 0x00:
            return 0
        return 10 - int((self.intensity - 1) / 25.5)

    def describe(self) -> str:
        # Specialty poses do not use/advertise an intensity subscript
        if self.emotion >= Emotion.NEUTRAL:
            subscript = ""
        else:
            # Use the wire intensity because it is consistent across
            # v55 and v66 made avatars; and it actually represents how
            # the gestures are communicated over the IRC protocol.
            subscript = f"[{self.intensity_wire()}]"

        return f"#{self.n:02d} {str(self.emotion)}{subscript}"

    def unstable_hash(self) -> int:
        return hash(self._imgmeta[0].offset)

    def read(self, file: BinaryIO) -> None:
        data = struct.unpack("<IIIh", file.read(14))
        for i in range(3):
            self._imgmeta[i].offset = data[i]

        # NB: It's not safe to use _warn until self.emotion is set.
        try:
            self.emotion = Emotion(data[3])
        except ValueError:
            self.emotion = data[3]
            self._warn(f"Found unknown emotion #{self.emotion}")
        if self.emotion >= 13:
            self._warn(f"Emotion ({str(self.emotion)}) is inaccessible in CChat")

        if not any(self._imgmeta[i].offset for i in range(3)):
            self._warn("Emotion has zero attached images. That's probably not right.")

        # Note: x/y appear to be stored as 2 byte integers, but the
        # HOB is *almost always zero*. Need to investigate to see if
        # there's a CCedit limitation or a CChat one.
        self.intensity, x, y = struct.unpack("<Bhh", file.read(5))
        self.coordinates_1 = (x, y)

        if self.face_data():
            # HOB on these is sometimes used; it's definitely signed.
            self.coordinates_2 = cast(Tuple[int, int], struct.unpack("<hh", file.read(4)))
            # HOB are (almost always) always zero again.
            self.coordinates_3 = cast(Tuple[int, int], struct.unpack("<hh", file.read(4)))

        # NB: It's not safe to use describe() until intensity is set.
        for imgmeta in self._imgmeta:
            imgmeta.context = self.describe()

    def size(self) -> int:
        # NB: This represents an abstract size,
        # v2.1 and v2.5 records are both bigger in practice.
        return 19 + (8 if self.face_data() else 0)

    def __bytes__(self) -> bytes:
        data = struct.pack(
            "<IIIhBhh",
            self._imgmeta[0].offset,
            self._imgmeta[1].offset,
            self._imgmeta[2].offset,
            int(self.emotion),
            self.intensity,
            self.coordinates_1[0],
            self.coordinates_1[1],
        )
        if self.face_data():
            data += struct.pack(
                "<hhhh",
                self.coordinates_2[0],
                self.coordinates_2[1],
                self.coordinates_3[0],
                self.coordinates_3[1],
            )
        return data

    def bitmap(self, index: int) -> Optional["Bitmap"]:
        """
        Retrieve a raw bitmap associated with this emotion/pose.

        :param index: Valid values are 0-2, inclusive.
        :return: A Bitmap object, if the image at that index exists.
        """
        return self._imgmeta[index].bmp

    def update_offset(self, index: int, offset: int) -> None:
        """
        Update the file offset for a specified bitmap.

        This is used by the Binary writer when it re-arranges the
        image table to write back out to file. You shouldn't need to
        use this function under normal circumstances.

        :param index: Which bitmap's offset to update, [0-2]
        :param offset: Virtual (unrebased) offset to bitmap; uint32_t.
        """
        self._imgmeta[index].offset = offset

    def raw_image(self, index: int) -> Optional[Image]:
        """
        Retrieve a raw image associated with this emotion/pose.

        :param index: Valid values are 0-2, inclusive.
        :return: a PIL Image object, if the image at that index exists.
        """
        return self._imgmeta[index].img

    def base_img(self) -> Image:
        """
        Retrieve the base image for this emotion/pose.

        :return: a PIL Image object.
        """
        if self._img1:
            return self._img1
        self._img1 = self.raw_image(0)
        assert self._img1
        return self._img1

    def _maskify(self, img: Image, kind: str) -> Image:
        # Turns mask data into a mask we can use with PIL.
        base = self.bitmap(0)
        assert base is not None

        if len(img.getcolors()) > 2:
            self._warn(f"{kind} uses more than 2 colors")

        base_img_lum = base.get_img().convert("L")
        mask_img_lum = img.convert("L")

        if mask_img_lum.size < base.dimensions:
            self._warn(f"{kind} is smaller than the base image and will be upscaled")
            mask_img_lum = mask_img_lum.resize(base.dimensions)

        # Normally, any white pixels in the mask correspond to white
        # pixels in the base image. These pixels become fully
        # transparent when composited onto a background. If there are
        # white pixels in the mask that happen to overlay non-white
        # pixels (this is extremely rare in avatars in circulation!)
        # this may induce partial transparency. To emulate this,
        # multiply the mask against the base image. In most cases,
        # this will have no effect at all; in rare cases, this will
        # "grow" the mask to include any sections of the base image
        # that have non-white pixels.
        img = ImageChops.multiply(base_img_lum, mask_img_lum)
        if list(img.getdata()) != list(mask_img_lum.getdata()):
            self._warn(f"{kind} selects non-white pixels and has been modified")

        img = ImageChops.invert(img)
        return img

    def halo_img(self) -> Image:
        # "Halo" mask - this is a looser fitting mask that adds the "halo" border.
        if self._img3:
            return self._img3
        img = self.raw_image(2)
        if img is None:
            raise RuntimeError("No halo image defined")
        self._img3 = self._maskify(img, "halo")
        return self._img3

    def mask_img(self) -> Image:
        # "Tight" mask - this is used for compositing faces onto bodies.
        # (Or in rare cases, bodies onto faces!)
        if self._img2:
            return self._img2
        img = self.raw_image(1)
        if img is None:
            raise RuntimeError("No mask image defined")
        self._img2 = self._maskify(img, "mask")
        return self._img2

    def render(self, transparency: str = "halo") -> Image:
        """
        Used for getting different composite images.

        "halo" - use the halo mask to composite this image.
        "mask-preferred" - use the tight mask to composite this image, but fall back to the halo.
        "mask-none" - use the tight mask if possible, fall back to no transparency.
        "none" - do not use any transparency mask.
        """
        if transparency not in ("halo", "mask-preferred", "mask-none", "none"):
            raise ValueError(f"unrecognized transparency argument {transparency}")

        img = self.base_img()
        img = img.convert("RGBA")
        alpha = None

        if transparency in ("mask-preferred", "mask-none"):
            try:
                alpha = self.mask_img()
            except RuntimeError:
                pass

        if transparency in ("mask-preferred", "halo"):
            if alpha is None:
                alpha = self.halo_img()

        if alpha:
            img.putalpha(alpha)
        return img

    def fingerprint(self) -> Tuple[Any, ...]:
        """
        Return fingerprint data for this emotion.

        This data includes data characteristic of this emotion entry,
        used ultimately for computing the "header fingerprint" of the
        entire file. It cannot detect changes in the pose data itself,
        but as a result is tolerant of offset differences. This is
        ultimately a heuristic for determining when two different
        avatars have different metadata, but the "same poses".

        Modifying this function will change the header fingerprint
        algorithm and output, so do not change it without very good
        reason.
        """
        return (
            int(self.emotion),
            self.intensity,
            bool(self._imgmeta[0]),
            bool(self._imgmeta[1]),
            bool(self._imgmeta[2]),
            self.coordinates_1,
            self.coordinates_2,
            self.coordinates_3,
            self._imgmeta[0].flag or 0,
            self._imgmeta[1].flag or 0,
            self._imgmeta[2].flag or 0,
        )

    @classmethod
    def table_header(cls, combined: bool = True) -> str:
        ret = "## kind offset_1 offset_2 offset_3 Emotion        EI xy_coord_1"
        if not combined:
            ret += " xy_coord_2 xy_coord_3"
        return ret

    def _summary_fields(self) -> List[str]:
        # Used for table output.
        return [
            f"{self.n:02d}",
            self.kind(),
            f"{self._imgmeta[0].offset:08X}",
            f"{self._imgmeta[1].offset:08X}",
            f"{self._imgmeta[2].offset:08X}",
            f"{str(self.emotion):14}",
            f"{self.intensity:02X}",
        ]

    def _summary_fields_suffix(self) -> List[str]:
        # Used for table output.
        ret = [
            f"({self.coordinates_1[0]:3d}, {self.coordinates_1[1]:3d})",
        ]
        if self.face_data():
            ret.append(f"({self.coordinates_2[0]:3d}, {self.coordinates_2[1]:3d})")
            ret.append(f"({self.coordinates_3[0]:3d}, {self.coordinates_3[1]:3d})")
        elif self.body_data():
            ret.append("    --    ")
            ret.append("    --    ")
        return ret

    def get_summary_row(self) -> str:
        fields = self._summary_fields() + self._summary_fields_suffix()
        return " ".join(fields)

    def get_img_table_rows(self, evaluate: bool = False) -> List[Tuple[str, Optional[Exception]]]:
        return [imgmeta.img_table_row(evaluate) for imgmeta in self._imgmeta if imgmeta]

    def strictness_check(self) -> None:
        # The order in which the emotions are stored appears to follow
        # a priority order:
        #
        # Neutral > Laugh > Bored > Angry > Happy > Scared > Shout >
        # Sad > Coy > Point to Self > Point to Other > Wave
        #
        # Maybe I'll check this (someday)

        # Although any intensity is generally valid, only a select few
        # values were produced by official editors and have generally
        # reliable behavior. Warn for unusual intensity values.
        assert self.intensity in (
            0x00,
            0x01,
            0x1B,
            0x34,
            0x4E,
            0x67,
            0x81,
            0x9A,
            0xB4,
            0xCD,
            0xE7,
            0x19,
            0x33,
            0x4C,
            0x66,
            0x7F,
            0x99,
            0xB2,
            0xCC,
            0xE5,
            0xFF,
        ), f"Unusual emotional intensity (EI) value 0x{self.intensity:02X}"

        # Check the face center coordinates. The official editor was
        # buggy and could produce bizarre values in some
        # circumstances, and hex-edited avatars often feature bizarre
        # coordinates.

        # In my own testing, the face locations I calculated as being
        # at 0x0F would glitch out and select a bigger coordinate.  I
        # couldn't select any coordinate lower than this.

        # When transparent margins are present, however, you can
        # select a location overlapping with or purely in the margin
        # to get lower values. So low it can underflow back up to
        # 0xFF!

        # Try to guess a canvas size for this character.
        # This can't be known with certainty; this is only the largest we can prove.
        # In the case that some calculation below fails to make sense with this palette size,
        # we may fall back to guessing the default 154x224, but it's not possible to know
        # for sure what the real canvas size actually was.
        w, h = self._parent.guess_canvas_size()
        bmp = self.bitmap(0)
        assert bmp is not None

        # NB: Bodies don't have face coordinates O:-)
        if self.face_coordinates is not None and self.face_coordinates[0] >= w:
            if (w - bmp.dib.width) > (256 - self.face_coordinates[0] + 16):
                # The value is too big, but it might be explained as
                # underflow and we are centered in the left margin -
                # the value underflowed due to the crop.
                self._warn(f"face-x appears to have underflown ({w}x{h} canvas)")
            elif (154 - bmp.dib.width) > (256 - self.face_coordinates[0] + 16):
                # Might still be underflow if we assume the default 154x224 canvas.
                self._warn("face-x appears to have underflown (assuming 154x224 canvas)")
            elif self.face_coordinates[0] < 0x90:
                # 0x89, 137, is the highest value you can get using
                # the standard template size of 154 x 224. In this
                # case, we assume the point is deep into the margin on the right.
                self._warn("face-x appears to be in the right margin.")
            else:
                self._warn(
                    f"face-x {self.face_coordinates[0]} exceeds canvas width ({w})"
                    " and standard canvas width (154) and cannot be explained by underflow"
                )

        if self.face_coordinates is not None and self.face_coordinates[1] >= h:
            if (h - bmp.dib.height) > (256 - self.face_coordinates[1] + 16):
                # Value is too big, but it might be underflow again.
                # We might be very high up in the top margin that got
                # cropped off.
                self._warn(f"face-y appears to have underflown ({w}x{h} canvas)")
            elif (224 - bmp.dib.height) > (256 - self.face_coordinates[1] + 16):
                self._warn("face-y appears to have underflown (assuming 154x224 canvas)")
            elif self.face_coordinates[1] < 0xD0:
                # 0xCF, 207, is the highest value you can get using
                # the standard template size of 154 x 224. In this
                # case, we assume the point is deep into the margin on
                # the bottom.
                self._warn("face-y appears to be in the bottom margin.")
            else:
                self._warn(
                    f"face-y {self.face_coordinates[1]}"
                    f" exceeds canvas height ({h})"
                    " and standard canvas height (224) and cannot be explained by underflow"
                )

        # These coordinates never seem to use the HOB.
        # assert 0 <= self.coordinates_1[0] <= 255
        # Re-Man uses the HOB for a single pose! It's just uncommon. Seems to work well.
        assert 0 <= self.coordinates_1[1] <= 255
        if self.face_data():
            assert 0 <= self.coordinates_3[0] <= 255
            assert 0 <= self.coordinates_3[1] <= 255


class OldEmotionHeader(EmotionHeaderBase):
    # This represents Poses, Faces and Bodies for v2.1 files.

    def __init__(self, parent: "Binary", field_type: int, n: int) -> None:
        super().__init__(parent, field_type, n)
        self.reserved_16: bytes = b"\x00" * 16

    def read(self, file: BinaryIO) -> None:
        super().read(file)
        self.reserved_16 = file.read(16)

    def __bytes__(self) -> bytes:
        return super().__bytes__() + self.reserved_16

    def size(self) -> int:
        return super().size() + 16

    def strictness_check(self) -> None:
        super().strictness_check()
        assert self.reserved_16 == b"\x00" * 16

        assert self._imgmeta[0]
        bmp = self.bitmap(0)
        assert bmp is not None

        # This is just a nice way to see the spread of possible image
        # types I've seen. There's no inherent reason why ones not
        # present here wouldn't work, but it's nice to have a
        # reference for what's out there.

        info = bmp.characterize()
        assert info in IMG_TABLE["v55"][0], f"unexpected image type for image: {info}"

        # Random factoid: 1bpp images that store their palette as
        # (black, white) are mode='1' to PIL, whereas (white, black)
        # become 1bpp 'P' type.  Silly, yet true!

        if self._parent.composition == 0x05:
            # For files that render face-on-body (most dynamic avatars),
            # we require the presence of a tight mask which is for
            # v2.1 files always stored in the offset_2 slot.
            if self.face_data():
                assert self._imgmeta[1], "offset_2 must be set for facial data"
            if self.body_data():
                # Well, it's more that it's extraneous and I've never seen it happen.
                # I don't think it actually hurts anything.
                assert not self._imgmeta[1], "offset_2 shouldn't be set for body data"
            if not (self.face_data() or self.body_data()):
                # Similarly, I doubt this is harmful - I've just never seen it.
                assert not self._imgmeta[1], "offset_2 shouldn't be set for pose data"
        elif self._parent.composition == 0x02:
            # These are files that render body-on-face (SUSAN only).
            if self.face_data() and self._imgmeta[1]:
                self._warn("Face Mask not expected to be set when composition == 0x02")
            if self.body_data():
                assert self._imgmeta[
                    1
                ], "offset_2 must be set for body data for composition == 0x02"

        if bmp := self.bitmap(1):
            info = bmp.characterize()
            assert info in IMG_TABLE["v55"][1], f"unexpected image type for mask: {info}"
            img = bmp.get_img()
            img = img.convert("RGB")
            colors = img.getcolors()
            assert len(colors) <= 2, f"ofs2/mask uses more than 2 colors ({len(colors)}) (v2.1)"
            colorset = set(pair[1] for pair in colors)
            assert colorset <= {
                (255, 255, 255),
                (0, 0, 0),
            }, f"ofs2/mask colorset {colorset}"

        # offset_3, the halo image, must be defined!
        assert self._imgmeta[2], "missing halo mask"
        bmp = self.bitmap(2)
        assert bmp is not None
        info = bmp.characterize()
        assert info in IMG_TABLE["v55"][2], f"unexpected image type for halo: {info}"

        # Forego checking the halo colors here -- if it's more than 2 colors,
        # we'll emit a warning during normal parsing instead.
        # In practice, 99.9% of files use a halo image that's black and white.
        # Only a single file I observed didn't, and that file had only a single
        # pixel that was (255, 255, 254) that violates this assumption.


class EmotionHeader(EmotionHeaderBase):
    # This represents Poses, Faces and Bodies for v2.5 files.

    def read(self, file: BinaryIO) -> None:
        super().read(file)

        data = struct.unpack("<BBB", file.read(3))
        for i in range(3):
            self._imgmeta[i].unk = data[i]

        data = struct.unpack("<BBB", file.read(3))
        for i in range(3):
            self._imgmeta[i].flag = data[i]

    def __bytes__(self) -> bytes:
        return super().__bytes__() + struct.pack(
            "<BBBBBB",
            self._imgmeta[0].unk,
            self._imgmeta[1].unk,
            self._imgmeta[2].unk,
            self._imgmeta[0].flag,
            self._imgmeta[1].flag,
            self._imgmeta[2].flag,
        )

    def size(self) -> int:
        return super().size() + 6

    def _split_2bpp_image(self) -> None:
        """
        This method "splits" a 2bpp image that uses arbitrary
        colors (as explained in Bitmap.py) into three separate black
        and white component images.
        """
        img = self.raw_image(0)
        assert img is not None
        self._img1 = img.getchannel("R")
        self._img2 = self._maskify(img.getchannel("G"), "mask")
        self._img3 = self._maskify(img.getchannel("B"), "halo")

    def base_img(self) -> Image:
        if self._img1:
            return self._img1
        if self._imgmeta[0].flag == 0x04:
            self._split_2bpp_image()
            assert self._img1 is not None
            return self._img1
        return super().base_img()

    def mask_img(self) -> Image:
        if self._img2:
            return self._img2
        if self._imgmeta[0].flag == 0x04:
            self._split_2bpp_image()
            assert self._img2 is not None
            return self._img2
        return super().mask_img()

    def halo_img(self) -> Image:
        if self._img3:
            return self._img3
        if self._imgmeta[0].flag == 0x04:
            # Halo is encoded in image1
            self._split_2bpp_image()
            assert self._img3 is not None
            return self._img3
        if self._imgmeta[1].flag == 0x05:
            # There's *no* halo, so use the tight mask from img2.
            self._img3 = self.mask_img()
            return self._img3
        return super().halo_img()

    @classmethod
    def table_header(cls, combined: bool = True) -> str:
        ret = "## kind offset_1 offset_2 offset_3 Emotion        EI F1 F2 F3 xy_coord_1"
        if not combined:
            ret += " xy_coord_2 xy_coord_3"
        return ret

    def _summary_fields(self) -> List[str]:
        return super()._summary_fields() + [
            f"{self._imgmeta[0].flag:02X}",
            f"{self._imgmeta[1].flag:02X}",
            f"{self._imgmeta[2].flag:02X}",
        ]

    def strictness_check(self) -> None:
        super().strictness_check()

        assert self._imgmeta[0].unk == 0x01
        assert self._imgmeta[1].unk == 0x01
        assert self._imgmeta[2].unk == 0x01
        # Redundant with checks below, but nice to see in one place:
        assert self._imgmeta[0].flag in (0x02, 0x04)
        assert self._imgmeta[1].flag in (0x03, 0x05)
        assert self._imgmeta[2].flag == 0x03

        # All poses and bodies have a halo.
        # All faces have a halo and a mask.
        # But, where are they hiding? O:-)
        if self._imgmeta[0].flag == 0x04:
            # offset_1 has the implied 2bpp format.
            # It can be used for faces, bodies, or poses. (!)
            # In any event, it contains all the transparencies we need.
            assert not self._imgmeta[1]
            assert not self._imgmeta[2]
        elif self._imgmeta[0].flag == 0x02:
            # offset_1 has a normal kind of image, so we need to get
            # our transparencies from somewhere.  One or the other
            # should be defined, but not both.
            assert self._imgmeta[1] or self._imgmeta[2]
            assert not (self._imgmeta[1] and self._imgmeta[2])

        assert self._imgmeta[0]
        bmp = self.bitmap(0)
        assert bmp
        info = bmp.characterize((self._imgmeta[0].flag,))
        assert info in IMG_TABLE["v66"][0], f"unexpected image type for image: {info}"

        if bmp.palette_type() == PaletteType.IMPLICIT:
            # All this block really tests is that we got a 2bpp flag=0x04 image
            # that actually encodes one or more monochrome images and masks in one
            # image field.
            assert self._imgmeta[0].flag == 0x04
            img = bmp.get_img()
            colors = img.getcolors()
            assert (
                len(colors) <= 4
            ), f"ofs1 implied palette img doesn't have <=4 colors {len(colors)}"
            # PIL's typing extension package seems to lie about the type of getcolors();
            colorset = cast(Set[Tuple[int, int, int, int]], set(pair[1] for pair in colors))
            assert colorset <= {
                (255, 255, 255, 255),
                (255, 255, 0, 255),
                (255, 0, 0, 255),
                (0, 0, 0, 255),
            }, f"ofs1 colorset {colorset}"

            if self.kind() == "POSE":
                assert len(colors) <= 3, "pose colors"
                # This encodes the base image + halo.
                #
                # The way this gets encoded is by combining the halo
                # into the white foreground data; effectively
                # "eliminating" the dedicated "halo" channel. Therefore,
                # we have red (white foreground), black (black
                # foreground), and white (transparency) pixels only.
                assert colorset <= {
                    (255, 0, 0, 255),
                    (255, 255, 255, 255),
                    (0, 0, 0, 255),
                }, f"pose1 colorset {colorset}"
            else:
                if (self.kind() == "BODY" and self._parent.composition == 0x05) or (
                    self.kind() == "FACE" and self._parent.composition == 0x02
                ):
                    # This *also* encodes a base image + halo.

                    # The tight mask is almost never
                    # present. *sometimes*, though, a superfluous halo
                    # is included anyway -- SUSAN.AVB does this for
                    # her final two facial emotions.

                    # Like the POSE section above, the halo data is
                    # usually combined with the foreground data; in
                    # the case it isn't and we have standalone HALO
                    # pixels, we know we have superfluous tight mask
                    # data.
                    if (255, 255, 0, 255) in colorset:
                        self._warn("2bpp multi-channel image includes superfluous tight mask data.")

        if bmp := self.bitmap(1):
            info = bmp.characterize((self._imgmeta[1].flag,))
            assert info in IMG_TABLE["v66"][1], f"unexpected image type for ofs2/mask: {info}"
            img = bmp.get_img()
            colors = img.getcolors()
            assert len(colors) == 2, "ofs2/mask doesn't have exactly 2 colors"
            # As above, PIL's type extension is not correct about the type of getcolors()
            colorset = cast(Set[Tuple[int, int, int, int]], set(pair[1] for pair in colors))
            assert colorset <= {
                (0, 0, 0, 255),
                (255, 255, 255, 255),
            }, f"ofs2 colorset {colorset} emotion {self.n}"
            # offset_2 is very scant! This would be the "tight mask" for heads only;
            # but that mask is packed into offset_1 2bpp when possible instead, I think.
        else:
            # For some reason ...?
            assert self._imgmeta[1].flag == 0x03, "absent ofs2 should use 03 flag"

        if bmp := self.bitmap(2):
            info = bmp.characterize((self._imgmeta[2].flag,))
            assert info in IMG_TABLE["v66"][2], f"unexpected image type for ofs3/halo: {info}"

            img = bmp.get_img()
            colors = img.getcolors()
            assert len(colors) <= 2, "ofs3/halo uses more than 2 colors (v2.5)"
        else:
            assert self._imgmeta[2].flag == 0x03
