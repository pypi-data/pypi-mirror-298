from typing import (
    TYPE_CHECKING,
    List,
    Optional,
    Tuple,
)

from PIL import Image

from .bitmap import Bitmap
from .util import exc_summary


if TYPE_CHECKING:
    from .binary import Binary


class ImageMetadata:
    """
    Represents an image header entry as seen in a Comic Chat AVB/BGB file.

    :param parent: The parent Binary object, needed for actually
        retrieving the image data.
    :param kind: One of POSE, FACE, BODY, ICON or BKGD. Used for
        display in the image table summary, as well as conditional
        fixes for improperly stored images.

    :param offset: Virtual offset to image data.
    :param unk: Unknown header flag; always 0x01 in v2.5 files.
    :param flag: Image compression type for v2.5 files.
    """

    def __init__(
        self,
        parent: "Binary",
        kind: str,
        context: Optional[str] = None,
        *,
        offset: Optional[int] = None,
        unk: Optional[int] = None,
        flag: Optional[int] = None,
    ) -> None:
        self._parent = parent
        self._kind = kind
        self._bmp: Optional[Bitmap] = None
        self._img: Optional[Image.Image] = None
        self.context = context
        self.offset = offset
        self.unk = unk  # None (2.1) / 0x01 (2.5)
        self.flag = flag  # None (2.1) / 0x02 - 0x05 (2.5)

    def __bool__(self) -> bool:
        return bool(self.offset)

    @property
    def bmp(self) -> Optional[Bitmap]:
        if self._bmp:
            return self._bmp

        if not self.offset:
            return None

        self._bmp = self._parent.get_bmp(self.offset, self.flag or 0)
        return self._bmp

    @property
    def img(self) -> Optional[Image.Image]:
        if self._img:
            return self._img

        if self.bmp is None:
            return None

        # If this is an icon and the flag is 0x04, it's been
        # mistakenly processed as a 2bpp mask. We need to pretend
        # it's a 1bpp image instead and force it back to a
        # regular, monochromatic 1bpp icon.
        use_hack = self.flag == 0x04 and self._kind == "ICON"
        self._img = self.bmp.get_img(hack_2bpp_to_1bpp=use_hack)
        return self._img

    @staticmethod
    def img_table_hdr() -> List[str]:
        return [
            "  PARENT                 TYPE @vOFFSET @ACTUAL    WxH   BPP #COL Palette ",
            "  -----------------------------------------------------------------------",
        ]

    def img_table_row(self, evaluate: bool = False) -> Tuple[str, Optional[Exception]]:
        """
        Return a table row entry for this image metadata object.

        Because some image metadata entries may lead to corrupt or
        un-parseable entries, this method returns a tuple containing
        the row entry itself (filling as many fields as it can), and
        an Exception object, if any, with full details as to why the
        bmp could not be retrieved.

        NOTE: This method forces evaluation of the .bmp, but does not
        attempt to deserialize the image itself; for Comic Chat v2.5
        avatars, this means that there may be lingering issues with
        the image if e.g. the bitmap metadata is retrieved
        successfully, but there are issues with the zlib data that
        follows.
        """
        if not self.offset:
            return ("", None)

        real_offset = self._parent.get_offset(self.offset)
        ret = f"  {self.context:22s} {self._kind:4s} {self.offset:08X} {real_offset:08X}"

        try:
            bmp = self.bmp
            assert bmp is not None
        except Exception as exc:  # pylint: disable=broad-exception-caught

            # The caller is responsible for the exception data: we
            # want to provide a cohesive image data table, so we can't
            # stop for small errors. BaseExceptions are allowed to
            # halt the program, though.

            # NB: _parse_images will collect these exceptions and
            # log/raise them appropriately via multi_exception_shim,
            # so we don't need to log them here.

            exc.add_note(
                f"For {self.context} {self._kind} image; "
                f"vOffset=0x{self.offset:08X} offset=0x{real_offset:08X}"
            )

            ret += f"                           ❌ {exc_summary(exc)}"
            return (ret, exc)

        ret += (
            f" {bmp.dib.width:03d}x{bmp.dib.height:03d}"
            f" {bmp.dib.bits_per_pixel:2d}  {bmp.dib.n_colors:3d}  {bmp.palette_type():8s}"
        )

        if evaluate:
            try:
                _ = self.img
            except Exception as exc:  # pylint: disable=broad-exception-caught

                # Same exception-handling safety commentary as above.
                exc.add_note(
                    f"For {self.context} {self._kind} image; "
                    f"vOffset=0x{self.offset:08X} offset=0x{real_offset:08X}"
                )
                ret += f" ❌ {exc_summary(exc)}"
                return (ret, exc)

        return (ret, None)
