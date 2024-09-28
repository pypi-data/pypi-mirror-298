"""
Bitmap Module

This provides the `Bitmap` and `CompressedBitmap` classes, which
provide support for reading the images stored in CChat 2.1 and 2.5
files.
"""

from contextlib import contextmanager
from enum import Enum
from io import BytesIO
import itertools
import logging
import math
import os
from pathlib import Path
import re
import struct
from typing import (
    Any,
    BinaryIO,
    Iterator,
    Optional,
    Tuple,
    Union,
)
import zlib

from PIL.Image import Image, frombytes
from PIL.Image import open as image_open


_LOG = logging.getLogger(__name__)


class PaletteType(Enum):
    # Standard Bitmap, no Palette
    NONE = 0
    # Standard Bitmap, with Palette
    EMBEDDED = 1
    # Compressed Bitmap, with compressed palette
    EXPLICIT = 2
    # Compressed Bitmap, with empty compressed palette
    EMPTY = 3
    # Compressed Bitmap; *without* compressed palette
    IMPLICIT = 4

    def __str__(self) -> str:
        return self.name.title()


class Bitmap:
    """
    Class for de/serializing standard .bmp files.

    Comic Chat 2.1 avatars store images as regular embedded BMP
    files. 2.5 files use a kind of modified BMP file that is handled
    separately in the `CompressedBitmap` subclass.

    BMP files have the following structure:
    0x00 - Bitmap file header  (14 bytes)
    0x0E - DIB Header          (40 bytes)
    0x36 - Palette, if present
         - Pixel data [immediately after Palette or DIB]

    For more info, see https://en.wikipedia.org/wiki/BMP_file_format#File_structure
    """

    _HEADER_SIZE = 14  # (includes magic through offset)

    def __init__(
        self,
        initial: Optional[Union[bytes, str, Path, "Bitmap", BinaryIO]] = None,
        autorepair: bool = False,
    ):
        # Binary data, in order;
        #
        # underscored fields have getters/setters instead that help
        # enforce consistency.

        self.header: bytes  # Covers the following:
        self.magic = b"BM"
        self._filesize = 0
        self.reserved_a = 0
        self.reserved_b = 0
        self._offset = 0

        self.dib = DIBHeader()
        self._palette = b""
        self._data = b""

        # Cache/Options

        self._img: Optional[Image] = None
        self._autorepair = autorepair
        self._invalidate = True

        file: BinaryIO
        if isinstance(initial, bytes):
            file = BytesIO(initial)
            self.read(file)
        elif isinstance(initial, (str, Path)):
            with open(initial, "rb") as file:
                self.read(file)
        elif isinstance(initial, Bitmap):
            file = BytesIO(bytes(initial))
            self.read(file)
        elif initial is not None:
            self.read(initial)

    def __repr__(self) -> str:
        tokens = [
            type(self).__name__,
            f"dim={self.dib.width}x{self.dib.height}",
            f"bpp={self.dib.bits_per_pixel}",
            f"comp=0x{self.dib.compression_method:02x}",
            f"pal={self.palette_type()!s}",
        ]
        return "<" + " ".join(tokens) + ">"

    #####################################
    # Getters/Setters for binary fields #
    #####################################

    @property
    def header(self) -> bytes:
        return struct.pack(
            "<2sIHHI",
            self.magic,
            self.filesize,
            self.reserved_a,
            self.reserved_b,
            self.offset,
        )

    @header.setter
    def header(self, value: bytes) -> None:
        (
            self.magic,
            self._filesize,
            self.reserved_a,
            self.reserved_b,
            self._offset,
        ) = struct.unpack("<2sIHHI", value)

    @property
    def filesize(self) -> int:
        if not self._filesize:
            self._filesize = self.offset + len(self.data)
        return self._filesize

    @property
    def offset(self) -> int:
        if not self._offset:
            self._offset = self._HEADER_SIZE + self.dib.size + len(self.palette)
        return self._offset

    @property
    def palette(self) -> bytes:
        return self._palette

    @palette.setter
    def palette(self, value: bytes) -> None:
        if self._invalidate:
            self._offset = 0
            self._filesize = 0
            self._img = None
        self._palette = value

    @property
    def data(self) -> bytes:
        return self._data

    @data.setter
    def data(self, value: bytes) -> None:
        if self._invalidate:
            self._filesize = 0
            self._img = None
        self._data = value

    ####################################################
    # Convenience functions / derived property getters #
    ####################################################

    @property
    def dimensions(self) -> Tuple[int, int]:
        return (self.dib.width, self.dib.height)

    @property
    def row_size(self) -> int:
        return self.dib.row_size()

    def palette_type(self) -> PaletteType:
        if self.palette:
            return PaletteType.EMBEDDED
        return PaletteType.NONE

    def __bytes__(self) -> bytes:
        """
        Return a BMP in its original disk format. (Windows or MSCC compressed)
        """
        return self.bitmap()

    def bitmap(self) -> bytes:
        """
        Return a standard Windows BMP as bytes.
        """
        return self.header + bytes(self.dib) + self.palette + self.data

    def characterize(self, extra_fields: Tuple[Any, ...] = ()) -> Tuple[Any, ...]:
        """
        Debugging convenience method; please don't rely on this as API.

        Return some fields that help characterize what type
        of image this is. Only used for debugging purposes in
        strictness_check() methods in various other classes.

        Returns a Tuple with the following fields:
          - int: color depth (bits per pixel)
          - bool: if image size is present in the DIB header
          - bool: if # colors is non-zero in the DIB header
          - int: the *bmp* (not cchat!) compression method used, if any
          - str: The method that the palette was stored
          - Any extra fields passed in by the caller.
        """
        info = (
            self.dib.bits_per_pixel,
            bool(self.dib.image_size),
            bool(self.dib.n_colors),
            self.dib.compression_method,
            str(self.palette_type()),
        ) + tuple(extra_fields)
        return info

    ##########################
    # Stuff that does stuff! #
    ##########################

    def read(self, file: BinaryIO) -> None:
        self._img = None
        with self._disable_invalidation():
            self._read_header(file)
            self.dib.read(file)
            self._read_palette(file)

            nbytes = self.filesize - self.offset
            data = file.read(nbytes)

            if len(data) != nbytes:
                raise EOFError(f"Expected {nbytes} of bitmap data, but got only {len(data)}")

            self.data = data

    def get_img(self, hack_2bpp_to_1bpp: bool = False) -> Image:
        """
        Get a PIL Image object from this Bitmap.

        :param hack_2bpp_to_1bpp: Due to a bug in some Avatar upgrade
           software, some monochrome images were inadvertantly stored
           as 2bpp. It's impossible to tell from looking at the bitmap
           data alone if this should be corrected, so the caller needs
           to pass this flag in when the correction is desired.
        """
        if self._img:
            return self._img

        # CChat 2.1 files use RLE_4 compression sometimes, which PIL doesn't support. :(
        if self.dib.compression_method == 0x02:
            self._img = self._rle4_decompress().get_img()
            return self._img

        # PIL doesn't support 2-bits-per-pixel. ;_;
        if self.dib.bits_per_pixel == 2:
            self._img = self._2bpp_image(hack_2bpp_to_1bpp)
            return self._img

        # Everything else should be pretty normal.
        self._img = image_open(BytesIO(self.bitmap()))
        return self._img

    ####################
    # Internal helpers #
    ####################

    def _read_header(self, file: BinaryIO) -> None:
        data = file.read(2)
        if data != b"BM":
            raise ValueError(f"Expected Bitmap file header 'BM', got '{data.hex()}'")
        file.seek(-2, os.SEEK_CUR)
        self.header = file.read(self._HEADER_SIZE)

    def _read_palette(self, file: BinaryIO) -> None:
        if self.dib.bits_per_pixel <= 8:
            colors = self.dib.n_colors
            if not colors:
                colors = 2**self.dib.bits_per_pixel
            self.palette = file.read(4 * colors)
        else:
            assert self.dib.n_colors == 0, "Expected dib.n_colors to be 0 when bpp > 8"

    def _2bpp_image(self, hack_2bpp_to_1bpp: bool) -> Image:
        """
        Get a PIL image for 2bpp bitmaps.
        """
        assert self.dib.bits_per_pixel == 2
        if self.dib.compression_method:
            raise NotImplementedError(
                f"DIB compression method {self.dib.compression_method}"
                " not currently supported for 2bpp images."
            )
        newdata = bytearray()
        if hack_2bpp_to_1bpp:
            # This image is 2 bits per pixel, but it was meant to be 1bpp.
            # As a hack, force it back to 1bpp!
            for idx in self._2bpp_indices():
                idx_a = (idx >> 1) * 3
                idx_b = (idx & 0x01) * 3
                newdata.extend(self.palette[4 * idx_a : 4 * idx_a + 4])
                newdata.extend(self.palette[4 * idx_b : 4 * idx_b + 4])
            dimensions = (self.dimensions[0] * 2, self.dimensions[1])
        else:
            # Normal 2bpp image. Well, as normal as those get, anyway. O:-)
            for idx in self._2bpp_indices():
                newdata.extend(self.palette[4 * idx : 4 * idx + 4])
            dimensions = self.dimensions

        img = frombytes(
            "RGBA",
            dimensions,
            bytes(newdata),
            "raw",
            "RGBA",
            0,
            -1,
        )
        if hack_2bpp_to_1bpp:
            img = img.crop((0, 0, *self.dimensions))
        return img

    def _2bpp_indices(self) -> Iterator[int]:
        """
        This method is a generator that yields a sequence of palette indices.

        PIL doesn't natively support 2bpp images. Fair enough, they're
        weird. I think even Windows 95/98 don't support such a
        format. In CChat avatars, they're only used for v2.5 avatars
        to encode multiple 1bpp images together into one
        pseudo-image. In a rare case, there's a single avatar I know
        of (Y-Guy.AVB) that appears to use a 2bpp image for its icon
        as the result of an automatic v2.5 conversion tool bug.
        """
        for y in range(self.dib.height):
            offset = self.row_size * y
            for x in range(self.dib.width):
                shift = 6 - ((x % 4) * 2)  # 6, 4, 2, 0, ...
                pal_idx = (self.data[offset + int(x / 4)] >> shift) & 0x03
                yield pal_idx

    def _rle4_indices(self) -> bytearray:
        """
        This method returns a sequence of palette indices.

        PIL does not appear to natively support RLE4 compressed
        bitmaps. So, this method will yield a sequence of indices with
        no padding.

        This is unfortunately very messy.

        https://learn.microsoft.com/en-us/openspecs/windows_protocols/ms-wmf/73b57f24-6d78-4eeb-9c06-8f892d88f1ab
        """
        pixels = bytearray()
        row = bytearray()
        data = BytesIO(self.data)

        def _end_of_line() -> None:
            # I *think* the EOL marker can "imply" pixels. It
            # certainly can for "DELTA" and "EOB" markers.
            n = self.dib.width - len(row)
            if n < 0:
                # I think sometimes data can get saved in the margin,
                # even though it's not "part of the image". In those
                # cases, we need to actually ignore some pixels. Rude.
                for _ in range(abs(n)):
                    row.pop()
                n = 0
            row.extend(b"\x00" * n)
            pixels.extend(row)
            row.clear()

        while True:
            x, y = data.read(2)
            if x == 0:
                if y == 0:
                    # Encoded mode - End of Line
                    _end_of_line()
                elif y == 1:
                    # Encoded mode - End of Bitmap
                    num_rows = int(len(pixels) / self.dib.width)
                    rows_rem = self.dib.height - num_rows
                    for _ in range(rows_rem):
                        _end_of_line()
                    break
                elif y == 2:
                    # Encoded mode - Delta
                    dx, dy = data.read(2)
                    _LOG.debug(f"Delta - {dx},{dy}")
                    x_offset = len(row) + dx
                    for _ in range(dy):
                        _end_of_line()
                    row.extend(b"\x00" * x_offset)
                else:
                    # Absolute mode - y indicates number of indices to follow.
                    # run length is "aligned on a word boundary".
                    rounded = math.ceil(y / 4) * 2
                    abs_data = data.read(rounded)
                    _LOG.debug(f"Absolute mode: {y} pixels")
                    for i in range(y):
                        bval = abs_data[int(i / 2)]
                        row.append((bval >> (0 if (i % 2) else 4)) & 0x0F)
            else:
                # Encoded mode - alternating colors
                _LOG.debug(f"Encoded mode: {x} pixels")
                for i in range(x):
                    row.append((y >> (0 if (i % 2) else 4)) & 0x0F)

        assert len(pixels) == self.dib.width * self.dib.height
        return pixels

    def _rle4_decompress(self) -> "Bitmap":
        """
        Return a whole new bitmap object that removes RLE4 compression.

        This method is *heinously* inefficient, it is notably the
        slowest image deserialization pathway possible in this
        library. I just ran out of neurons to care about improving it,
        and I was happier to have something that was provably correct.

        Apologies for the functionally correct software.
        """
        assert self.dib.compression_method == 0x02, "compression method is not RLE4"
        assert self.dib.bits_per_pixel == 4, "compression method was RLE4 but bpp wasn't 4?"

        def _pad(data: bytes) -> Iterator[int]:
            for x in range(self.dib.height):
                for y in range(self.dib.width):
                    yield data[x * self.dib.width + y]
                for y in range((self.row_size * 2) - self.dib.width):
                    yield 0

        def _pack(it: Iterator[int]) -> Iterator[int]:
            while True:
                try:
                    value = (next(it) << 4) | next(it)
                    yield value
                except StopIteration:
                    break

        tmp_data = bytes(_pack(_pad(self._rle4_indices())))
        assert len(tmp_data) == self.dib.expected_size()

        tmp = Bitmap(self)  # Make a copy!
        tmp.dib.image_size = 0  # This is legal to zero when ...
        tmp.dib.compression_method = 0  # ... compression method is 0.
        tmp.data = tmp_data  # Replace with the uncompressed data O:-)
        return tmp

    @contextmanager
    def _disable_invalidation(self) -> Iterator[None]:
        """
        Turn off cached field invalidation temporarily.

        During initial object construction from existing bitmap data,
        we'll read in filesize and offset. When palette and bitmap
        data are read in, this would otherwise delete the stored
        values. This bypasses that.
        """
        self._invalidate = False
        try:
            yield
        finally:
            self._invalidate = True

        # Paranoia: what if the input data was *bad*?

        given = self._filesize
        self._filesize = 0
        computed = self.filesize

        if given != computed:
            raise ValueError(
                f"Given bitmap filesize {given} does not match computed size {computed}"
            )

        given = self._offset
        self._offset = 0
        computed = self.offset

        if given != computed:
            raise ValueError(f"Given bitmap offset {given} does not match computed size {computed}")


class DIBHeader:
    """
    DIBHeader is a fairly straightforward data class representing the DIB header.

    https://en.wikipedia.org/wiki/BMP_file_format#DIB_header_(bitmap_information_header)

    This class represents only the 40 byte BITMAPINFOHEADER variant.

    Both CChat 2.1 and 2.5 files utilize this structure. See `Bitmap`
    or `CompressedBitmap` for more details.
    """

    _expected_size = 40

    def __init__(self) -> None:
        self.size = self._expected_size
        self.width = 0
        self.height = 0
        self.n_color_planes = 0
        self.bits_per_pixel = 0
        self.compression_method = 0
        self.image_size = 0
        self.x_res = 0
        self.y_res = 0
        self.n_colors = 0
        self.imp_colors = 0

    def read(self, file: BinaryIO) -> None:
        self.size = struct.unpack("<I", file.read(4))[0]
        if self.size != self._expected_size:
            raise ValueError(
                f"Expected {self._expected_size} byte bitmap DIB header, but got size={self.size}"
            )

        data = struct.unpack("<iiHHIIiiII", file.read(36))
        self.width = data[0]
        self.height = data[1]
        self.n_color_planes = data[2]
        self.bits_per_pixel = data[3]
        self.compression_method = data[4]
        self.image_size = data[5]
        self.x_res = data[6]
        self.y_res = data[7]
        self.n_colors = data[8]
        self.imp_colors = data[9]

        # image_size is an optional field when compression is zero,
        # because it can be computed. If it's provided, though, double-check it:
        if self.compression_method == 0 and self.image_size:
            if self.expected_size() != self.image_size:
                _LOG.warning(
                    f"Non-zero DIB field image_size ({self.image_size})"
                    f" does not match expected size ({self.expected_size()}"
                )

    def row_size(self) -> int:
        """Returns the row size of this image in bytes"""
        return math.ceil((self.bits_per_pixel * self.width) / 32) * 4

    def expected_size(self) -> int:
        """Returns the anticipated size of this image in bytes"""
        return self.row_size() * self.height

    def __bytes__(self) -> bytes:
        return struct.pack(
            "<IiiHHIIiiII",
            self.size,
            self.width,
            self.height,
            self.n_color_planes,
            self.bits_per_pixel,
            self.compression_method,
            self.image_size,
            self.x_res,
            self.y_res,
            self.n_colors,
            self.imp_colors,
        )

    def print(self) -> None:
        print(f"  Width: {self.width}")
        print(f"  Height: {self.height}")
        print(f"  Color Planes: {self.n_color_planes}")
        print(f"  Color Depth: {self.bits_per_pixel}")
        print(f"  Compression Method: {self.compression_method}")
        print(f"  Image size: {self.image_size}")
        print(f"  X-Res: {self.x_res}")
        print(f"  Y-Res: {self.y_res}")
        print(f"  # Colors: {self.n_colors}")
        print(f"  # Imp. Colors: {self.imp_colors}")


class CompressedBitmap(Bitmap):
    """
    This class represents the Compressed Bitmaps used in CChat 2.5 files.

    These bitmaps differ from traditional bitmaps by omitting the file
    header completely, loading the palette data *before* the DIB
    header, and using ZLIB to compress the pixel data.

    The structure is:

    - Palette data, if present.
      The palette structure can be present, but empty.
      If the palette data is absent, it means we have an implied palette.
    - DIB header (40 bytes)
    - Uncompressed size (4 bytes)
    - Compressed size (4 bytes)
    - ZLIB compressed pixel data (variable)

    .. note:: Currently, it's not an intentionally supported operation
       to modify the compressed_size, uncompressed_size, cpalette or
       zdata fields directly. Do so at your own risk.

       Setting the .palette or .data fields will update these fields
       accordingly.
    """

    def __init__(
        self,
        initial: Optional[Union[bytes, str, Path, "Bitmap", BinaryIO]] = None,
        autorepair: bool = False,
    ):
        self.compressed_size = 0
        self.uncompressed_size = 0
        self.cpalette: Optional[bytes] = None
        self.zdata: bytes = b""

        # Super call last because it invokes read()
        super().__init__(initial, autorepair)

    #####################################
    # Getters/Setters for binary fields #
    #####################################

    @property
    def palette(self) -> bytes:
        return self._palette

    @palette.setter
    def palette(self, value: bytes) -> None:
        cpalette = bytearray()
        buf = BytesIO(value)
        for _ in range(len(value) // 4):
            cpalette.extend(bytes(reversed(buf.read(3))))
            buf.read(1)
        if self._invalidate:
            self._offset = 0
            self._filesize = 0
            self._img = None
        self.cpalette = bytes(cpalette)
        self._palette = value

    @property
    def data(self) -> bytes:
        if self._data:
            return self._data

        try:
            self._data = zlib.decompress(self.zdata, bufsize=self.uncompressed_size)
        except zlib.error as exc:
            if not self._autorepair:
                raise
            _LOG.info(f"zlib data is corrupted. attempting repair. error: {str(exc)}")
            if not self._repair():
                _LOG.info("zlib data recovery failed.")
                raise
            _LOG.warning("zlib data is corrupted, but was successfully recovered.")

        if len(self._data) != self.uncompressed_size:
            raise ValueError(
                f"Expected {self.uncompressed_size} bytes after decompressing, "
                f"got {len(self._data)} bytes"
            )

        return self._data

    @data.setter
    def data(self, value: bytes) -> None:
        if len(value) != self.dib.expected_size():
            raise ValueError(
                f"Size of new data {len(value)} "
                f"does not match expected size from DIB header {self.dib.expected_size()}"
            )

        if self._invalidate:
            self._filesize = 0
            self._img = None

        zdata = zlib.compress(value)
        self._data = value
        self.zdata = zdata
        self.uncompressed_size = len(value)
        self.compressed_size = len(zdata)

    ####################################################
    # Convenience functions / derived property getters #
    ####################################################

    def __bytes__(self) -> bytes:
        """
        Return the MSCC compressed bitmap bytes for this object.

        Unlike the base class, we want a packing that's in the
        compressed form here.  use bitmap() to get bytes for a normal
        bitmap file instead.

        Though, keep in mind: this direct conversion may not make
        sense for implicit palette bitmaps, which need to be split
        apart and reconstructed into several constituent monochrome
        images instead.
        """
        buff = bytearray()
        if self.cpalette is not None:
            magic = b"\x01\x01"
            num_colors = int(len(self.cpalette) / 3)
            color_length = len(self.cpalette) + 2
            buff += struct.pack("<2sHH", magic, color_length, num_colors)
            buff += self.cpalette

        buff += bytes(self.dib)
        buff += struct.pack("<II", self.uncompressed_size, self.compressed_size)
        buff += self.zdata

        return bytes(buff)

    def palette_type(self) -> PaletteType:
        # Compressed palette is present and non-empty. This occurs for
        # 4bpp and 8bpp base images.
        # imgflag is always 0x02.
        if self.cpalette:
            return PaletteType.EXPLICIT

        # A custom palette header was present, but it didn't contain
        # anything. This appears to occur for 24bps full-color base
        # images that do not use a palette.
        # imgflag is always 0x02.
        if self.cpalette is not None:
            return PaletteType.EMPTY

        # No custom palette was present at all. These images generally
        # contain one or more alpha transparency compositing masks,
        # but can contain monochrome base image data when possible,
        # too. (Primarily for MS-authored comic avatar files.)
        #
        # imgflag == 0x04 (monochrome base img + halo + mask)
        # imgflag == 0x05 (compositing mask for full-color head images)
        # imgflag == 0x03 (halo mask for pre-composited full-color images)
        #
        # See generate_implied_palette() for even more detail.
        return PaletteType.IMPLICIT

    ##########################
    # Stuff that does stuff! #
    ##########################

    def generate_implied_palette(self, flag: int = 0) -> None:
        if self.palette_type() != PaletteType.IMPLICIT:
            return

        assert self.palette == b"", "Unexpected palette data for implicit palette image"

        if self.dib.bits_per_pixel == 1:
            assert flag in (
                0x03,
                0x04,
            ), f"implicit 1bpp flag was 0x{flag:02x}, expected 0x03/0x04"

            if flag == 0x04:
                # 1bpp and flag==0x04 only happens for icons - and I
                # think this is actually just an accident; I think the
                # conversion tool to upgrade avatars to the 2.5 format
                # accidentally compresses monochrome icons in a
                # strange way that was only meant for mask images.

                # I believe flag==0x04 was meant to be for 2bpp
                # images; and in fact when these icons are displayed
                # in cchat they appear at half-width because they are
                # being interpreted as 2bpp images.

                # For our purposes, though, we can just set a special
                # palette for these types of images and the icons will
                # extract correctly based on their original intent
                # (How they appear in v2.1 files), and at the right
                # size.

                # This impacts four avatars I've found: John Bruton,
                # Jean-Luc Dehaene, Costas Simitis and Blues Elmwood.
                self._palette = b"\x00\x00\x00\xFF\xFF\xFF\xFF\xFF"
            elif flag == 0x03:
                # This is used for offset3/halo mask images.
                # It's used in thousands of avatars.
                # The colors match those used in v2.1 mask images.
                self._palette = b"\xFF\xFF\xFF\xFF\x00\x00\x00\xFF"

        elif self.dib.bits_per_pixel == 2:
            assert flag in (
                0x04,
                0x05,
            ), f"implicit 2bpp flag was 0x{flag:02x}, expected 0x04/0x05"
            if flag == 0x05:
                # This is a 2-color mask stored in offset2 for
                # full-color dynamic format avatars.

                # I've found only 11 avatars that use this mode: BUCK,
                # GESSELM, Kalana, McGraw, Ray, Re-Man, Tom, Trisha,
                # Trudy, VERONICA, and zar-zoon.

                # Almost always, they use only the first and last
                # palette entries and behave like normal binary
                # masks. On rare occasion, just a few pixels in one or
                # two poses use the other palette entries; this rarity
                # occurs in BUCK, GESSELM and VERONICA avatars.

                # Behavior for the "rare" palette entries was verified
                # by hand in CChat 2.5 by modifying avatars and
                # observing the behavior.

                self._palette = (
                    b"\xFF\xFF\xFF\xFF"  # White (Transparent)
                    b"\xFF\xFF\xFF\xFF"  # (rarely used - same as above)
                    b"\x00\x00\x00\xFF"  # (rarely used - same as below)
                    b"\x00\x00\x00\xFF"  # Black (Opaque)
                )
            elif flag == 0x04:
                # This is a 4-color image that encodes a monochrome
                # base image, the halo, and the mask. (The halo may be
                # omitted in some circumstances.) The colors I choose
                # below are fully arbitrary, but I am abusing the RGB
                # channels to encode three separate two-color images
                # that we'll extract later with Image.getchannel().

                # Red channel encodes the black and white base image,
                # which interprets the halo and background as fully
                # white.

                # Green channel encodes the transparency mask, which
                # interprets the background and halo region as fully
                # white and the base image pixels as black. This mask
                # will be inverted before PIL uses it as a mask, but
                # it maintains consistency with how masks are stored
                # in 2.1 images.

                # Blue channel encodes the halo mask, which functions
                # similarly to the tight transparency mask, but
                # toggles the halo pixels to black, leaving only the
                # background region white. Like the tight transparency
                # mask, these colors are inverted from PIL's
                # expectation of a transparency mask, but it's
                # consistent with explicit palette data from CChat
                # 2.1.
                self._palette = (
                    b"\xFF\xFF\xFF\xFF"  # Background region
                    b"\xFF\xFF\x00\xFF"  # Halo region
                    b"\xFF\x00\x00\xFF"  # White opaque pixels (base image)
                    b"\x00\x00\x00\xFF"  # Black opaque pixels (base image)
                )

        else:
            raise NotImplementedError(
                f"Cannot generate implicit palette for bpp={self.dib.bits_per_pixel}"
            )

    def read(self, file: BinaryIO) -> None:
        # Compressed bitmaps have no 14 byte header; as a result,
        # filesize and offset are computed only on-demand instead.

        # Weird proprietary palette is *before* the DIB header:
        self._read_custom_palette(file)

        # DIB header is simply the normal kind:
        self.dib.read(file)

        # The palette which would otherwise occur here has already been read.

        (self.uncompressed_size, self.compressed_size) = struct.unpack("<II", file.read(8))

        if self.uncompressed_size != self.dib.expected_size():
            raise ValueError(
                f"Uncompressed size written before ZLIB data ({self.uncompressed_size})"
                f" does not match expected size ({self.dib.expected_size()}), "
                "this bitmap header may be corrupt."
            )
        if self.compressed_size > self.uncompressed_size + 11:
            raise ValueError(
                f"Compressed size written before ZLIB data ({self.compressed_size}) "
                f"is more than 11 bytes larger than the uncompressed/expected size"
                f" ({self.uncompressed_size}), this bitmap header may be corrupt."
            )

        self.zdata = file.read(self.compressed_size)

        if len(self.zdata) != self.compressed_size:
            raise EOFError(
                f"Could not read {self.compressed_size} bytes of compressed data."
                f" (Read only {len(self.zdata)} bytes.)"
            )

    ####################
    # Internal helpers #
    ####################

    def _recover_data_newline_method(self, nbytes: int = 1) -> bool:
        # This method looks at 0x0a bytes and attempts to see if they
        # should have been 0x0a 0x0d sequences. It relies on a human
        # operator having already re-padded the data with null byte(s)
        # to bring it up to "correct size".
        _LOG.debug(f"Attempting to recover data newline repair method (nbytes={nbytes}) ...")
        offset = 0
        indices = []
        while True:
            index = self.zdata.find(b"\x0a", offset)
            if index == -1:
                break
            indices.append(index)
            offset = index + 1

        if not indices:
            _LOG.debug("newline repair method isn't applicable.")
            return False
        _LOG.debug(f"Found {len(indices)} 0x0a bytes")

        attempts = 0
        for configuration in itertools.combinations(indices, nbytes):
            attempts += 1
            zdata = bytearray(self.zdata[:-nbytes])
            for offset in sorted(configuration, reverse=True):
                # Sort backwards so we can insert back-to-front without doing weird math.
                zdata.insert(offset, 0x0D)
            try:
                self._data = zlib.decompress(zdata, bufsize=self.uncompressed_size)
                _LOG.debug(f"\nSuccess!!! - attempt #{attempts}, inserted 0x0D @ {configuration}")
                self.zdata = bytes(zdata)
                return True
            except zlib.error:
                # No good.
                pass

        _LOG.debug(f"\nCouldn't repair using newline repair method (nbytes={nbytes}).")
        return False

    def _repair_tripod(self) -> bool:
        """
        Detect and fix corruption caused by the Tripod webserver.

        The tripod webserver attempted to find and modify apparent
        HTML tags in the response body.

        Generally, this means binary data that happened to look like
        the start of an HTML tag may have been uppercased or
        lowercased, depending.

        In practice, this means data like <b, <f, and <h are
        suspicious in tripod files where the zlib data fails to
        decompress; recovery is sometimes possible by simple
        guess-and-check modifying the capitalization of any such
        bytes.

        Personally, I've not observed any occurrences of anything
        longer than "<BO" or "</B"; three bytes seems about as much as
        you're likely to run into by chance; but who knows! you could
        get very unlucky!
        """
        _LOG.debug("Attempting to repair data using tripod uncorruption method ...")
        tagnames = ("body", "frameset", "html", "head")

        def _make_pattern(tag: str) -> bytes:
            ret = "(?:".join(tag)
            ret += ")?" * (len(tag) - 1)
            return ret.encode()

        patterns = [_make_pattern(tag) for tag in tagnames]
        pattern = b"</?(" + b"|".join(patterns) + b")"

        indices = []
        for match in re.finditer(pattern, self.zdata, re.IGNORECASE):
            _LOG.debug(f"found suspicious data: {match.group(0)!r} @ 0x{match.start(0):02x}")
            for i in range(match.start(1), match.end(1)):
                indices.append(i)

        if not indices:
            _LOG.debug("Tripod data recovery method isn't applicable.")
            return False
        _LOG.debug(f"Found {len(indices)} suspicious bytes")
        _LOG.debug(f"There are {2**len(indices)-1} possible alterations to try")

        zdata = bytearray(self.zdata)

        for configuration in itertools.product((True, False), repeat=len(indices)):
            for offset, modify in zip(indices, configuration):
                if modify:
                    zdata[offset] = ord(chr(zdata[offset]).upper())
                else:
                    zdata[offset] = ord(chr(zdata[offset]).lower())
            try:
                self._data = zlib.decompress(zdata, bufsize=self.uncompressed_size)
                _LOG.debug(f"Success!!! - configuration: {configuration}")
                self.zdata = bytes(zdata)
                return True
            except zlib.error as exc:
                _LOG.debug(f"No good - {str(exc)}")

        _LOG.debug("Couldn't recover the data (tripod method)")
        return False

    def _repair(self) -> bool:
        if self._repair_tripod():
            return True

        # These other methods require knowing how short or overlong
        # the data buffer is, which may not be possible with
        # corruption and may require outside help from the Binary
        # class, so they're stubbed out for now because they aren't
        # fully automatic.

        # if self._recover_data_newline_method(nbytes=1):
        #     return True
        # if self._recover_data_newline_method(nbytes=2):
        #     return True
        return False

    def _read_custom_palette(self, file: BinaryIO) -> None:
        # If there is no palette here, we expect to read '28 00' as
        # the first two bytes of the DIB header. This should be fairly
        # resilient.
        curpos = file.tell()
        magic = file.read(2)
        if magic != b"\x01\x01":
            file.seek(curpos, os.SEEK_SET)
            return

        color_length = struct.unpack("<H", file.read(2))[0]
        if color_length < 2:
            raise ValueError(f"Expected palette size to be two or more bytes, got {color_length}")
        num_colors = struct.unpack("<H", file.read(2))[0]
        if color_length != num_colors * 3 + 2:
            raise ValueError(
                f"Expected palette size to be {num_colors * 3 + 2}, got {color_length}"
            )

        self.cpalette = file.read(num_colors * 3)
        if len(self.cpalette) != (num_colors * 3):
            raise EOFError(
                f"Expected {num_colors * 3} bytes of palette data, read only {len(self.cpalette)}"
            )

        # The packed format here appears to be BGR, Windows BMP files
        # expect RGB0. Reverse the order and pad every three bytes
        # with an empty fourth.
        buf = BytesIO(self.cpalette)
        palette = bytearray()
        for _ in range(num_colors):
            palette.extend(bytes(reversed(buf.read(3))))
            palette.append(0)
        self._palette = bytes(palette)
