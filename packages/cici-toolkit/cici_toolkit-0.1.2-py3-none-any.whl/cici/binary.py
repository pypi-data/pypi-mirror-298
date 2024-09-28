"""
Binary - Microsoft Comic Chat Binary files support

This module provides access to the `Binary` class, which provides
support for reading and writing Microsoft Comic Chat binary files,
including AVB (Avatar) and BGB (Binary) files.
"""

import enum
import hashlib
from io import BytesIO
import logging
import os
from pathlib import Path
import struct
from typing import (
    BinaryIO,
    Dict,
    List,
    Optional,
    Tuple,
    Union,
)

from PIL import Image
import chardet

from .bitmap import Bitmap, CompressedBitmap
from .emotion import EmotionHeaderBase
from .imgmeta import ImageMetadata
from .table import IMG_TABLE
from .util import exc_summary, multi_exception_shim


_LOG = logging.getLogger(__name__)


class FileVersion(enum.Enum):
    CCHAT_21 = 1
    CCHAT_25 = 2

    def version(self) -> float:
        if self == FileVersion.CCHAT_21:
            ret = 2.1
        else:
            assert self == FileVersion.CCHAT_25
            ret = 2.5
        return ret


class FileType(enum.Enum):
    # Combined, static poses. This is the format produced by the
    # widely available CCEdit v55 and v66 tools.
    AVATAR_STATIC = 1

    # Dynamic poses. This is the format used by most
    # Microsoft-published avatars, but a few enterprising hackers
    # managed to create their own; notably Shunji Haruki.
    AVATAR_DYNAMIC = 2

    # Background files: Only available in CCHAT_25 files.
    BACKGROUND = 3

    def describe(self) -> str:
        if self == FileType.AVATAR_STATIC:
            ret = "Avatar, Static poses"
        elif self == FileType.AVATAR_DYNAMIC:
            ret = "Avatar, Dynamic poses"
        else:
            assert self == FileType.BACKGROUND
            ret = "Background"
        return ret


class Field(enum.Enum):
    NAME = 1
    COMPOSITION = 2
    ICON_OFFSET = 3
    FACES_V1 = 4
    BODIES_V1 = 5
    END_OF_HEADER = 6
    END_OF_FILE = 7
    EIGHT = 8  # What's this do? I dunno :3
    COMBINED_V1 = 9
    FACES_V2 = 0x0A
    BODIES_V2 = 0x0B
    COMBINED_V2 = 0x0C
    ICON_INFO = 0x100
    BG_INFO = 0x102
    COPYRIGHT = 0x103
    DOWNLOAD = 0x104
    DOWNLOAD2 = 0x105
    PROTECTION = 0x106
    REBASE = 0x107


def decodify(raw: bytes) -> str:
    """
    decodify tries to decode string data.

    AVB/BGB files do not store what encoding they use, so it's a trial
    and error process. The large majority of files accessible to me,
    an English speaker, are likely ASCII or Windows-1252/ISO-8859-1.

    In some cases, this is ambiguous and some files may actually be
    encoded with other encodings; we'll try our best to guess a
    reasonable default.
    """
    # Try as UTF-8 first. This will probably only work when it's
    # literal ASCII.
    try:
        return raw.decode()
    except UnicodeDecodeError:
        pass

    # It is probably Windows-1252/ISO-8859-1 if the only non-ASCII
    # characters are © and/or ®. These characters could be inserted
    # into the text field of the CCEdit editor with dedicated
    # clickable buttons, so their presence is likely.
    raw2 = raw.replace(b"\xAE", b"").replace(b"\xA9", b"")
    if raw2.isascii():
        return raw.decode("Windows-1252")

    # chardet never seems to guess Japanese, even when it is. For
    # now, "just try it". Comic Chat was very popular in Japan.
    try:
        return raw.decode("shift_jis")
    except UnicodeDecodeError:
        # Well, it wasn't Japanese.
        pass

    # Get a guess from chardet as a last resort.
    # Sometimes it throws its hands up and says "I dunno",
    # in which case, just default to Windows-1252 again.
    guess = chardet.detect(raw).get("encoding", "Windows-1252")
    if guess is None:
        guess = "Windows-1252"
    try:
        return raw.decode(guess)
    except UnicodeDecodeError:
        # ah geez. maybe it guessed something that isn't Windows-1252
        # and its own guess failed.
        pass

    return raw.decode("Windows-1252")


def encodify(value: str) -> bytes:
    """
    encodify is the opposite of `decodify` and outputs encoded bytes.

    Like decodify, this will try to guess the most appropriate
    encoding for a string.
    """
    # The nice thing about *encoding* is that it's a lot easier to
    # determine the encoding. If an encoding isn't legal, we try a
    # different one!

    # Try as ASCII first.
    try:
        return value.encode("ASCII") + b"\x00"
    except UnicodeEncodeError:
        pass

    # Then Shift_JIS (Japanese):
    try:
        return value.encode("Shift_JIS") + b"\x00"
    except UnicodeEncodeError:
        pass

    # Finally, Windows-1252.
    return value.encode("Windows-1252") + b"\x00"


class Binary:
    """
    This represents CChat AVB and BGB files.

    :param file: Can be None, bytes, a file-like object,
                 or a str/Path pointing to a file.

    :param parse_images: Set to False if you don't want to attempt
        parsing of images at all. This can be useful for parsing
        metadata out of damaged files. Images can be buffered post-hoc
        by calling `read_images()`, but the file will still need to be
        open. This is not supported when passing a str/path as @file.
    """

    def __init__(
        self,
        file: Union[bytes, str, Path, BinaryIO],
        parse_images: bool = True,
        autorepair: bool = False,
    ) -> None:
        # Settings
        self._autorepair = autorepair

        # Main Header
        self.version: Tuple[int, int]
        self.ftype: FileType
        self.fvers: FileVersion

        # Simple metadata
        self.name: Optional[str] = None
        self.copyright: Optional[str] = None
        self.author: Optional[str] = None
        self.download_orig: Optional[str] = None
        self.download_new: Optional[str] = None
        self.protected = False
        self._unk8: Optional[int] = None  # always 0x01 for avatars; absent otherwise
        self.composition: Optional[int] = None  # 0x05: body/pose-first, 0x02: head-first, 0x00: ??
        self.added_bytes = 0

        # Images and Emotion data:
        self._icon = ImageMetadata(self, "ICON", "Icon")
        self._bg = ImageMetadata(self, "BKGD", "Background")
        self.emotions: List[EmotionHeaderBase] = []

        # Fields for strictness checking, debugging, and summary output:
        self._regions: List[Tuple[int, int]] = []
        self._fields_seen: List[int] = []
        self._end_of_header = 0
        self._end_of_bitmaps = 0
        self._img_table: Optional[List[str]] = None
        self._canvas_size: Optional[Tuple[int, int]] = None
        self._eof_checked = False

        # Alright, let's get this show on the road.

        # NB: It'd be nice to allow empty Binary() files and to fill them out as we go,
        # but the class isn't *quite* set up for that just yet, we need some refactoring.
        # For now, (sorry), require something to be passed in.
        self._file: BinaryIO
        if isinstance(file, bytes):
            self._file = BytesIO(file)
            self.read(parse_images)
        elif isinstance(file, (str, Path)):
            if not parse_images:
                raise ValueError(
                    "parse_images=False not supported when file is passed as str/Path."
                )
            with open(file, "rb") as infile:
                self._file = infile
                self.read(parse_images)
        else:
            self._file = file
            self.read(parse_images)

    def _warn(self, msg: str) -> None:
        _LOG.warning(msg)

    def _read_string(self, length_prefix: bool = False, what: str = "") -> str:
        """
        Read string data from the open AVB/BGB file at current offset.

        Strings associated with names don't store a length prefix, but
        every other string does. This method maintains bug-level
        compatibility with how CChat reads strings, which ignores the
        length prefix stored in the file.

        This method calls `decodify` and returns a decoded string
        without a trailing null byte.
        """
        n = 0
        if length_prefix:
            n = struct.unpack("<h", self._file.read(2))[0]

        # Quirk: even if we have a length prefix, cchat reads until
        #        null regardless of the length. SCARY!
        #        This can lead to both under- and overreads.
        data = bytearray()
        while True:
            data += self._file.read(1)
            if data[-1] == 0:
                break

        if length_prefix and n != len(data):
            self._warn(f"String read for {what} got {len(data)} bytes, was expecting {n}!")

        return decodify(data[:-1])

    def _read_length_prefixed_data(self) -> bytes:
        """
        Read a length-prefixed data segment at the current offset.

        This cannot be used for length-prefixed strings due to a bug
        in MSCC, see `_read_string`.
        """
        n = struct.unpack("<h", self._file.read(2))[0]
        return self._file.read(n)

    def _read_copyright_author(self) -> None:
        """
        Read the copyright and author from file at the current offset.
        """
        copyauth = self._read_string(length_prefix=True, what="Copyright/Author")
        if "\\n" in copyauth:
            self.copyright, self.author = copyauth.split("\\n", maxsplit=1)
        else:
            self.copyright = copyauth

    def _seek(self, offset: int, whence: int) -> int:
        curpos = self._file.tell()
        pos = self._file.seek(offset, whence)
        if pos > self._size:
            self._file.seek(curpos, os.SEEK_SET)
            raise EOFError(f"Offset 0x{pos:02X} is beyond EOF (0x{self._size:02X})")
        return pos

    def read(self, parse_images: bool = True) -> None:
        """
        Parse the open AVB/BGB file from the current offset.

        If parse_images is False, images will not be parsed or
        buffered at all.  Call `read_images` later if you wish to do
        it separately, but keep in mind that the file will still need
        to be open!

        This option is most useful when dealing with damaged files
        that need to be repaired, or for getting metadata out of
        damaged files.

        Also note: when parse_images is False, warnings related to EOF
        markers and extra trailing data will not be triggered unless
        `read_images` is later called.
        """
        curpos = self._file.tell()
        self._size = self._file.seek(0, os.SEEK_END)
        self._file.seek(curpos, os.SEEK_SET)

        magic = self._file.read(2)
        _LOG.info("signature/magic: 0x%s", magic.hex())

        if magic == b"\x81\x00":
            self.version = (2, 1)
        elif magic == b"\x81\x81":
            self.version = (2, 5)
        else:
            raise ValueError(
                "Unrecognized file magic; expected 0x8181 (v2.5) or 0x8100 (v2.1); got "
                f"0x{magic.hex()}"
            )

        self.ftype = FileType(struct.unpack("<h", self._file.read(2))[0])
        _LOG.info("type: %s (0x%04x)", self.ftype, self.ftype.value)
        self.fvers = FileVersion(struct.unpack("<h", self._file.read(2))[0])
        _LOG.info("version: %s (0x%04x)", self.fvers, self.fvers.value)

        fingerprint = (magic, self.ftype, self.fvers)
        if fingerprint not in (
            (b"\x81\x81", FileType.AVATAR_STATIC, FileVersion.CCHAT_25),
            (b"\x81\x81", FileType.AVATAR_DYNAMIC, FileVersion.CCHAT_25),
            (b"\x81\x81", FileType.BACKGROUND, FileVersion.CCHAT_25),
            (b"\x81\x00", FileType.AVATAR_STATIC, FileVersion.CCHAT_21),
            (b"\x81\x00", FileType.AVATAR_DYNAMIC, FileVersion.CCHAT_21),
        ):
            raise ValueError(f"Unexpected file signature: {fingerprint}")

        fields_seen = []
        while True:
            field_type = struct.unpack("<h", self._file.read(2))[0]
            fields_seen.append(field_type)
            try:
                field = Field(field_type)
            except:
                _LOG.error(
                    "0x%x is not a valid metadata field type (@offset 0x%x)",
                    field_type,
                    self._file.tell(),
                )
                raise

            if field == Field.NAME:
                self.name = self._read_string()
                _LOG.info("0x0001 / name: %s", self.name)

            elif field == Field.COMPOSITION:
                self.composition = struct.unpack("<h", self._file.read(2))[0]
                _LOG.info("0x0002 / composition flag: 0x%02x", self.composition)

            elif field == Field.ICON_OFFSET:
                # This is used for v2.1 files only. ICON_INFO is used otherwise.
                offset = struct.unpack("<I", self._file.read(4))[0]
                self._icon.offset = offset
                _LOG.info("0x0003 / icon offset: 0x%08x", self._icon.offset)
                if not self._icon.offset:
                    self._warn("Icon offset was zero. That's probably not right.")

            elif field == Field.EIGHT:
                self._unk8 = struct.unpack("<h", self._file.read(2))[0]
                _LOG.info("0x0008 / unknown avatar field: 0x%02x", self._unk8)

            # All 0x1nn field types are length-prefixed.
            elif field == Field.ICON_INFO:
                data = self._read_length_prefixed_data()
                if len(data) != 6:
                    _LOG.debug("Bad header data: %s", repr(data))
                    raise ValueError("Icon header size was not exactly 6 bytes")

                (self._icon.offset, self._icon.unk, self._icon.flag) = struct.unpack("<IBB", data)

                _LOG.info("0x0100 / icon header:")
                _LOG.info("  offset:     0x%08x", self._icon.offset)
                _LOG.info("  unknown:    0x%02x", self._icon.unk)
                _LOG.info("  image type: 0x%02x", self._icon.flag)
                if not self._icon.offset:
                    self._warn("Icon offset was zero. That's probably not right.")

            elif field == Field.BG_INFO:
                data = self._read_length_prefixed_data()
                if len(data) != 6:
                    _LOG.debug("Bad header data: %s", repr(data))
                    raise ValueError("Background header size was not exactly 6 bytes")

                (self._bg.offset, self._bg.unk, self._bg.flag) = struct.unpack("<IBB", data)

                _LOG.info("0x0102 / background header:")
                _LOG.info("  offset:     0x%08x", self._bg.offset)
                _LOG.info("  unknown:    0x%02x", self._bg.unk)
                _LOG.info("  image type: 0x%02x", self._bg.flag)
                if not self._bg.offset:
                    self._warn("Background offset was zero. That's probably not right.")

            elif field == Field.COPYRIGHT:
                self._read_copyright_author()
                _LOG.info("0x0103 / authorship information:")
                _LOG.info("  copyright: %s", self.copyright)
                _LOG.info("  author: %s", self.author)

            elif field == Field.DOWNLOAD:
                self.download_orig = self._read_string(length_prefix=True, what="Download URL")
                _LOG.info("0x0104 / download URL: %s", self.download_orig)

            elif field == Field.DOWNLOAD2:
                self.download_new = self._read_string(length_prefix=True, what="Download URL2")
                _LOG.info("0x0105 / download override: %s", self.download_new)

            elif field == Field.PROTECTION:
                data = self._read_length_prefixed_data()
                if len(data) != 1:
                    _LOG.debug("Bad protection header data: %s", repr(data))
                    raise ValueError("Protection header size was not exactly one byte")

                self.protected = struct.unpack("<?", data)[0]
                _LOG.info("0x0106 / protected: %s", self.protected)

            elif field == Field.REBASE:
                data = self._read_length_prefixed_data()
                if len(data) != 4:
                    _LOG.debug("Bad rebase header data: %s", repr(data))
                    raise ValueError("Rebase header was not exactly 4 bytes")

                offset = struct.unpack("<i", data)[0]
                _LOG.info("0x0107 / rebase: %d byte(s)", offset)
                self.added_bytes += offset

            elif field in (
                Field.FACES_V1,
                Field.BODIES_V1,
                Field.COMBINED_V1,
                Field.FACES_V2,
                Field.BODIES_V2,
                Field.COMBINED_V2,
            ):
                count = struct.unpack("<h", self._file.read(2))[0]
                _LOG.info(
                    "0x%04x / %s: %d entries",
                    field_type,
                    EmotionHeaderBase.describe_field(field_type),
                    count,
                )
                klass = EmotionHeaderBase.get_klass(field_type)
                combined = field in (Field.COMBINED_V1, Field.COMBINED_V2)

                hdr = klass.table_header(combined)
                _LOG.info("  %s", hdr)
                _LOG.info("  %s", "-" * len(hdr))

                for i in range(count):
                    eheader = klass(self, field_type, i)
                    eheader.read(self._file)
                    self.emotions.append(eheader)
                    _LOG.info("  %s", eheader.get_summary_row())

            elif field == Field.END_OF_HEADER:
                _LOG.info("0x0006 / End of header; start of image data")
                break

            else:
                raise ValueError(f"Unknown field type {field_type:X}")

        _LOG.info("header fingerprint: %s", self.header_fingerprint())

        self._end_of_header = self._file.tell()
        _LOG.info(f"end of header: 0x{self._end_of_header:X}")
        self._regions.append((0, self._end_of_header))
        self._fields_seen = fields_seen
        if parse_images:
            self.read_images()

    def read_images(self, evaluate: bool = False) -> None:
        self._parse_images(evaluate)
        # We don't know where the image table ends unless we can parse it,
        # so this check winds up here as the only place it *can* go.
        if not self._eof_checked:
            self._check_end_of_file()

    def print_summary(self, advanced: bool = False) -> None:
        output = {}

        if hasattr(self._file, "name"):
            output["file"] = self._file.name
            output["size"] = str(os.path.getsize(self._file.name))
        elif hasattr(self._file, "getvalue"):
            output["file"] = "<IO Buffer>"
            output["size"] = str(len(self._file.getvalue()))
        else:
            output["file"] = "<No File>"
            output["size"] = "<Unknown>"

        if advanced:
            output["type"] = repr(self.ftype)
            output["version"] = repr(self.fvers)
        else:
            output["type"] = self.ftype.describe()
            output["version"] = str(self.fvers.version())

        # Hack to get a little separator O:-)
        output[" "] = " "

        output["name"] = self.name or "--"
        output["copyright"] = self.copyright or "--"
        output["author"] = self.author or "--"

        output["download (new)"] = self.download_new or "--"
        output["download (old)"] = self.download_orig or "--"
        output["protected"] = "yes" if self.protected else "no"

        # O:-)
        output["  "] = " "

        output["emotions"] = f"{len(self.emotions)}"
        output["unique images"] = str(
            len(set(emotion.unstable_hash() for emotion in self.emotions))
        )
        output["emotion types"] = str(len(set(e.emotion for e in self.emotions))) + "/12"  # lol
        output["fingerprint"] = self.header_fingerprint()

        width = max(len(k) for k in output) + 1
        for k, v in output.items():
            if k.strip():
                k = k + ":"
            print(f"{k:{width}} {v}")

    def print_emotion_table(self) -> None:
        combined = not any(e.face_data() or e.body_data() for e in self.emotions)
        last_record_type = None
        for emotion in self.emotions:
            if emotion.field_type != last_record_type:
                last_record_type = emotion.field_type
                print("")
                hdr = emotion.table_header(combined)
                print(hdr)
                print("-" * len(hdr))
            print(emotion.get_summary_row())

    def header_fingerprint(self) -> str:
        ret: List[object] = [
            self.ftype.value,
            self.fvers.value,
            self.composition,
            self._icon.unk,
            self._icon.flag,
            self._bg.unk,
            self._bg.flag,
        ]
        for emotion in self.emotions:
            ret.append(emotion.fingerprint())
        data = str(tuple(ret)).encode()
        return hashlib.md5(data).hexdigest()

    def _parse_images(self, evaluate: bool = False) -> None:
        """
        Parse all of the image metadata present in this file.

        This method is called towards the end of read(). This method
        will parse all of the image metadata, but does not actually
        process or reconstruct any of those images yet. Data will be
        *buffered* but not decompressed.

        This method may report failures if the offsets listed in the
        headers are incorrect, the file is short, the bitmap headers
        in the file are corrupt, etc. When evaluate is False, this
        method may surprisingly sometimes *not fail* for CChat 2.5
        files with zlib stream corruption, or other image data
        interpretation problems which may only surface when fully
        evaluating images.

        On Python3.11+, ExceptionGroup will be raised to report *all*
        image parsing problems instead of stopping at only the first
        problem.
        """
        exceptions = []
        img_table = []

        def _handle_row(entry: Tuple[str, Optional[Exception]]) -> None:
            row, exc = entry
            if row:
                _LOG.info(row)
                img_table.append(row)
            if exc:
                assert row
                exceptions.append(exc)

        # ---

        _LOG.info("")
        _LOG.info("Image data:")
        for line in ImageMetadata.img_table_hdr():
            _LOG.info(line)
            img_table.append(line)

        _handle_row(self._icon.img_table_row(evaluate))
        _handle_row(self._bg.img_table_row(evaluate))

        for emotion in self.emotions:
            problems = False
            for entry in emotion.get_img_table_rows(evaluate):
                _handle_row(entry)
                problems = problems or bool(entry[1])
            if evaluate and not problems:
                try:
                    # Final sanity check!
                    _ = emotion.render()
                except Exception as exc:  # pylint: disable=broad-exception-caught
                    _handle_row(
                        (f"    ❌ Problem compositing {emotion.kind()}: {exc_summary(exc)}", exc)
                    )

        self._img_table = img_table
        multi_exception_shim(exceptions, _LOG, "There were multiple problems parsing images")

    def print_image_table(self) -> None:
        if self._img_table is None:
            raise RuntimeError("read_images() must be called before printing the image table.")
        for line in self._img_table:
            print(line)

    def _check_end_of_file(self) -> None:
        """
        This method checks that there is no extra data at the end of the file.

        It's called at the end of `read_images()`. It will only ever
        produce warnings, it doesn't raise any exceptions.
        """
        start = self._end_of_bitmaps
        self._file.seek(start, os.SEEK_SET)

        data = self._file.read(2)
        if data != b"\x07\x00":
            self._warn(f"0x07 EOF record not found immediately after image data (at 0x{start:X}).")
            self._file.seek(start, os.SEEK_SET)

        junk_start = self._file.tell()
        data = self._file.read()
        if data == b"":
            # EOF! We love EOF.
            pass
        elif data.replace(b"\x00", b""):
            self._warn(f"Found junk data at end of file (from 0x{junk_start:X}).")
        else:
            self._warn(f"Found empty bytes at end of file (from 0x{junk_start:X}).")

        end = self._file.tell()
        self._regions.append((start, end))
        self._eof_checked = True

    def get_offset(self, offset: int) -> int:
        """
        Get an absolute offset from a relative one.

        Offsets advertised in AVB/BGB files can be rebased if 0x107
        headers are present. This method translates the recorded
        offset into the real, absolute offset.
        """
        return offset + self.added_bytes

    def get_bmp(self, offset: int, flags: int = 0) -> Bitmap:
        """
        Get a Bitmap object located at a given offset.

        This method takes a raw offset as advertised directly in the
        Emotion/Pose data tables and it may not match the real offset
        in the binary file if any rebase headers are present in the
        file header.

        The object returned may be a Bitmap or a CompressedBitmap.

        Raw data will be buffered but not deserialized into a usable
        format; this method may error out if the data stream is
        truncated or if the bitmap headers are corrupted in some way.
        """
        ofs = self.get_offset(offset)
        self._seek(ofs, os.SEEK_SET)

        bmp: Bitmap
        if flags:
            bmp = CompressedBitmap(self._file, autorepair=self._autorepair)
            bmp.generate_implied_palette(flags)
        else:
            bmp = Bitmap(self._file, autorepair=self._autorepair)

        end = self._file.tell()
        if (ofs, end) not in self._regions:
            self._regions.append((ofs, end))
        self._end_of_bitmaps = max(self._end_of_bitmaps, end)

        return bmp

    @property
    def background(self) -> Optional[Image.Image]:
        # A setter API would be nice to add (...)
        return self._bg.img

    @property
    def icon(self) -> Optional[Image.Image]:
        # A setter API would be nice to add (...)
        return self._icon.img

    def strictness_check(self) -> None:
        # A lot of these checks are redundant as the library has grown
        # and become more robust; I simply haven't audited them all to
        # see which are now superfluous. In the worst case, they serve
        # as a convenient localized reference for the assumptions this
        # library makes.
        #
        # Ideally, these would all be warnings; but at time of writing
        # I have only 7 files in my possession that trigger any
        # assertions (without running into a hard error earlier in the
        # parse), and it's still useful to keep these assertions as
        # strict failures for purposes of understanding which
        # circumstances *never* happen and which are indicative of
        # more minor problems. (IOW: as warnings, they get lost in the
        # noise of more minor problems. For remaining assertion
        # failures witnessed on files in circulations, they should
        # either be converted to hard errors if they are not usable in
        # comic chat, or downgraded to warnings if they DO work, but
        # potentially with issues.)

        # ###############################################
        # *** Validate metadata fields present/absent ***
        # ###############################################

        # These fields must be present:
        mandatory = {
            FileType.AVATAR_DYNAMIC: {
                FileVersion.CCHAT_21: {0x04, 0x05},
                FileVersion.CCHAT_25: {
                    0x0A,
                    0x0B,
                    0x01,
                    0x02,
                    0x100,
                },  # 0x08: downgraded to warning; observed on files in circulation
            },
            FileType.AVATAR_STATIC: {
                FileVersion.CCHAT_21: {0x09},
                FileVersion.CCHAT_25: {0x0C, 0x01, 0x02, 0x100},  # 0x08: warn-only
            },
            FileType.BACKGROUND: {FileVersion.CCHAT_25: {0x102}},
        }

        # These fields must be absent:
        forbidden = set()
        if self.ftype == FileType.AVATAR_DYNAMIC:
            forbidden |= {0x09, 0x0C}
        if self.ftype == FileType.AVATAR_STATIC:
            forbidden |= {0x04, 0x05, 0x0A, 0x0B}
        if self.ftype == FileType.BACKGROUND:
            forbidden |= {
                0x01,
                0x02,
                0x03,
                0x04,
                0x05,
                0x08,
                0x09,
                0x0A,
                0x0B,
                0x0C,
                0x100,
            }
        if self.fvers == FileVersion.CCHAT_21:
            forbidden |= {0x0A, 0x0B, 0x0C}
            forbidden |= {0x100, 0x103, 0x104, 0x105, 0x106, 0x107}
        if self.fvers == FileVersion.CCHAT_25:
            forbidden |= {0x04, 0x05, 0x09}
            forbidden |= {0x03}

        for field in forbidden:
            assert field not in self._fields_seen, (
                f"field 0x{field:02X} unexpectedly present in file type "
                f"{self.ftype.name}/{self.fvers.name}"
            )
        for field in mandatory[self.ftype][self.fvers]:
            assert field in self._fields_seen, (
                f"field 0x{field:02X} unexpectedly missing in file type "
                f"{self.ftype.name}/{self.fvers.name}"
            )

        if self.fvers == FileVersion.CCHAT_25 and self.ftype != FileType.BACKGROUND:
            if 0x08 not in self._fields_seen:
                self._warn(
                    "Field 0x08 missing from binary; This is likely caused by hex-editing damage."
                )

        # ##############################
        # *** Validate Misc Fields *** #
        # ##############################

        if self.fvers == FileVersion.CCHAT_25 and self.ftype != FileType.BACKGROUND:
            assert self._icon.unk == 0x01, f"Icon field #3 was not 0x01 (0x{self._icon.unk:02X})"
            assert self._icon.flag in (0x02, 0x04), self._icon.flag

        if self.ftype == FileType.AVATAR_DYNAMIC:
            # Only SUSAN.AVB (2.1 or 2.5) uses 0x02 here.
            # Absolutely everything else uses 0x05.
            assert self.composition in (
                0x02,
                0x05,
            ), f"Expecting composition type 0x05 or 0x02, found 0x{self.composition:02X}"
        elif self.ftype == FileType.AVATAR_STATIC and self.fvers == FileVersion.CCHAT_21:
            # glenda.avb and tux.avb have a 0x00 here. Don't know why.
            assert self.composition in (
                0x00,
                0x05,
            ), f"Expecting composition type 0x05 or 0x00, found 0x{self.composition:02X}"
        elif self.ftype != FileType.BACKGROUND:
            assert (
                self.composition == 0x05
            ), f"Expecting composition type 0x05, found 0x{self.composition:02X}"

        if self.ftype == FileType.BACKGROUND:
            assert self._bg.unk == 0x01
            assert self._bg.flag == 0x02
        else:
            assert self._icon.offset
            assert (
                self._unk8 == 0x01 or 0x08 not in self._fields_seen
            ), f"Expecting 0x01 in field 0x08, got 0x{self._unk8:X}"

        # ####################################
        # *** Validate Images & Emotions *** #
        # ####################################

        for emotion in self.emotions:
            try:
                emotion.strictness_check()
            except:
                _LOG.error("strictness check failed for %s", emotion.describe())
                raise

        if bmp := self._icon.bmp:
            info = bmp.characterize((self._icon.flag,))
            assert info in IMG_TABLE["icon"], f"unexpected image info for icon: {info}"

        if bmp := self._bg.bmp:
            info = bmp.characterize((self._bg.flag,))
            assert info in IMG_TABLE["bg"], f"unexpected image info for bgb: {info}"

        # ##############################
        # *** Validate File Layout *** #
        # ##############################

        if self.ftype == FileType.BACKGROUND:
            assert self._bg.offset is not None
            expected_offset = self.get_offset(self._bg.offset)
        else:
            assert self._icon.offset is not None
            expected_offset = self.get_offset(self._icon.offset)
        assert self._end_of_header == expected_offset, (
            f"End of header (0x{self._end_of_header:02x})"
            f" is not located at icon/bg offset (0x{expected_offset:02x})"
        )

        self._regions = sorted(self._regions)
        end = 0
        for region in self._regions:
            if region[0] == end:
                end = region[1]
        if end != self._file.tell():
            for region in self._regions:
                _LOG.debug("%x %x", region[0], region[1])
            self._warn(f"Detected unused bytes starting at 0x{end:X}")

    def guess_canvas_size(self) -> Tuple[int, int]:
        if self._canvas_size is not None:
            return self._canvas_size
        max_height = 0
        max_width = 0
        for emotion in self.emotions:
            # Every last emotion header; pose/body/face should have a base image.
            # buut, sometimes files are corrupt and we can't read it.
            try:
                bmp = emotion.bitmap(0)
                if not bmp:
                    continue
            except Exception as exc:  # pylint: disable=broad-exception-caught
                _LOG.warning(f"Error reading image while guessing canvas size: {exc_summary(exc)}")
                _LOG.debug("Error reading image while guessing canvas size", exc_info=exc)
                continue

            max_width = max(max_width, bmp.dib.width)
            max_height = max(max_height, bmp.dib.height)
        self._canvas_size = (max_width, max_height)
        return self._canvas_size

    @classmethod
    def _write_field(cls, file: BinaryIO, field: Field, value: bytes = b"") -> None:
        file.write(struct.pack("<h", field.value))
        if field.value >= 0x100:
            # All fields in this range are length-prefixed.
            file.write(struct.pack("<h", len(value)))
        file.write(value)

    def _write_image_fields(self, file: BinaryIO) -> None:
        """
        Write out the image fields to a file.

        This includes BG, Icon, emotions, and the end-of-header record.
        """
        if self._bg.offset:
            # Background Info (V2)
            self._write_field(
                file,
                Field.BG_INFO,
                struct.pack("<IBB", self._bg.offset, self._bg.unk, self._bg.flag),
            )

        if self._icon.offset:
            if self.fvers == FileVersion.CCHAT_21:
                # Icon Offset (V1)
                self._write_field(file, Field.ICON_OFFSET, struct.pack("<I", self._icon.offset))
            else:
                # Icon Info (V2)
                self._write_field(
                    file,
                    Field.ICON_INFO,
                    struct.pack("<IBB", self._icon.offset, self._icon.unk, self._icon.flag),
                )

        # Emotion headers
        for field_type in (
            Field.FACES_V1,
            Field.BODIES_V1,
            Field.COMBINED_V1,
            Field.FACES_V2,
            Field.BODIES_V2,
            Field.COMBINED_V2,
        ):
            emotions = [e for e in self.emotions if e.field_type == field_type.value]
            if not emotions:
                continue

            self._write_field(file, field_type, struct.pack("<h", len(emotions)))
            for emotion in emotions:
                file.write(bytes(emotion))

        # END_OF_HEADER
        self._write_field(file, Field.END_OF_HEADER)

    def write(self, file: BinaryIO) -> None:
        """
        Write this binary back out to file.

        Offsets are recomputed and re-written to file; offsets of
        emotion headers **will be altered in-memory** to reflect the
        new file layout. Rebase headers are removed.

        Any data that was repaired in-memory is written back out to
        file in place of the original corrupted data, in effect
        repairing the file.

        Any unused data regions between image files, or any unused
        trailing data will also be omitted.
        """

        # Gotta make sure the image table is fully cooked before we
        # attempt to write. Evaluation is not necessary; we'll just
        # write garbage data back out if we got garbage in.
        if self._img_table is None:
            self.read_images()

        if self.version == (2, 1):
            magic = b"\x81\x00"
        else:
            magic = b"\x81\x81"
        header = struct.pack("<2shh", magic, self.ftype.value, self.fvers.value)
        file.write(header)

        # Field.REBASE would get written here if we were going to do it.
        # No need, we're re-generating the file from scratch with freshly
        # computed correct offsets.
        self.added_bytes = 0

        if self.ftype in (FileType.AVATAR_STATIC, FileType.AVATAR_DYNAMIC):
            # Name is not included for FileType.BACKGROUND
            name = self.name or "NoName"
            data = encodify(name)
            self._write_field(file, Field.NAME, data)
            self._write_field(file, Field.EIGHT, struct.pack("<h", self._unk8 or 0x01))
            self._write_field(file, Field.COMPOSITION, struct.pack("<h", self.composition))

        if self.fvers == FileVersion.CCHAT_25:
            if self.copyright or self.author:
                copyright_ = self.copyright or "Not specified"
                author = self.author or "Not specified"
                copyauth = f"{copyright_}\\n{author}"
                data = encodify(copyauth)
                self._write_field(file, Field.COPYRIGHT, data)
            if self.download_orig:
                data = encodify(self.download_orig)
                self._write_field(file, Field.DOWNLOAD, data)
            if self.protected:
                self._write_field(file, Field.PROTECTION, struct.pack("<B", self.protected))
            if self.download_new:
                data = encodify(self.download_new)
                self._write_field(file, Field.DOWNLOAD2, data)

        # Write out a mock-version of the rest of the header data with
        # (possibly) wrong offsets so we can compute where the data
        # region will start.

        dummy_buffer = BytesIO()
        self._write_image_fields(dummy_buffer)
        start_of_data = file.tell() + dummy_buffer.tell()
        del dummy_buffer

        # Now, plan where all the images will go...
        image_table: Dict[Tuple[int, str], int] = {}
        image_buffer = bytearray()

        def _write_image(bmp: Optional[Bitmap]) -> Optional[int]:
            if not bmp:
                return None

            # Deduplicate identical images O:-)
            data = bytes(bmp)
            ident = (len(data), hashlib.md5(data).hexdigest())

            if ident in image_table:
                return image_table[ident]

            offset = start_of_data + len(image_buffer)
            image_table[ident] = offset
            image_buffer.extend(data)
            return offset

        # Write out images to buffer and update header offsets
        if bmp := self._bg.bmp:
            self._bg.offset = _write_image(bmp)

        if bmp := self._icon.bmp:
            self._icon.offset = _write_image(bmp)

        for emotion in self.emotions:
            for i in range(3):
                emotion.update_offset(i, _write_image(emotion.bitmap(i)) or 0)

        # Now that the offsets have been updated, actually write out the rest of the header.
        self._write_image_fields(file)
        assert file.tell() == start_of_data, "Miscalculated the header size - this is a bug :("

        # IMAGE DATA --
        file.write(image_buffer)

        # END_OF_FILE
        self._write_field(file, Field.END_OF_FILE)
