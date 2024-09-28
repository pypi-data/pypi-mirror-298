"""
This module lays out the "expected" image types.

This image metadata represents the image metadata of every avatar and
background file I have come across, split by context of where it
occurs. This is done so that I have an easy table to reference when I
want to know in what circumstances certain flags appear, or when
certain images are present or not and what forms they take, etc.

A certain type of image format being absent here doesn't mean it isn't
supported, but it may mean the tool will do something unpredictable
with it, because I haven't encountered it myself to test.

It's just kind of helpful to see this info all in one place.

Table entries are:

- bits per pixel
- Does the DIB header provide a byte size for the raw RGB data?
- Does the DIB header state the number of colors in the palette?
  (No defaults to 2^bpp)
- DIB header compression flag (0 is no compression.)
- How is the palette stored?
- Comic Chat v2.5 attributes field, if present.
"""

IMG_TABLE = {
    "icon": (
        # bpp, size?, ncol?, comp, PaletteType, flag
        (1, True, True, 0, "Embedded", None),
        (1, True, True, 0, "Implicit", 0x04),
        # ^ J Bruton, C Simitis, JL Dehaene, etc. MS Bug!
        (2, False, True, 0, "Implicit", 0x04),
        # Y-Guy, this is a bug! See `icon()`
        (4, True, True, 2, "Embedded", None),
        (4, False, True, 0, "Embedded", None),
        (4, True, True, 0, "Explicit", 0x02),
        (4, True, False, 0, "Explicit", 0x02),
        (4, True, False, 0, "Embedded", None),
        (4, True, False, 2, "Embedded", None),
        (8, False, True, 0, "Embedded", None),
        (8, True, True, 1, "Embedded", None),  # Oh! Neat. TOM. of course.
        (8, False, False, 0, "Embedded", None),
        (8, False, True, 0, "Explicit", 0x02),
        (8, True, True, 0, "Explicit", 0x02),
        (8, False, False, 0, "Explicit", 0x02),
        (24, False, False, 0, "None", None),
        (24, True, False, 0, "Empty", 0x02),
        (24, True, False, 0, "None", None),
        (24, False, False, 0, "Empty", 0x02),
    ),
    "bg": (
        # bpp, size?, ncol?, comp, PaletteType, flag
        (1, True, False, 0, "Explicit", 0x02),
        (4, True, True, 0, "Explicit", 0x02),
        (4, True, False, 0, "Explicit", 0x02),
        (4, False, True, 0, "Explicit", 0x02),
        (8, False, False, 0, "Explicit", 0x02),
        (8, False, True, 0, "Explicit", 0x02),
        (8, True, False, 0, "Explicit", 0x02),
        (8, True, True, 0, "Explicit", 0x02),
        (24, False, False, 0, "Empty", 0x02),
        (24, True, False, 0, "Empty", 0x02),
    ),
    "v55": [
        # First image: pose/head/face base image
        (
            # bpp, size?, ncol?, comp, PaletteType
            (1, False, True, 0, "Embedded"),
            (1, False, False, 0, "Embedded"),
            (1, True, True, 0, "Embedded"),
            (1, True, False, 0, "Embedded"),
            (4, False, True, 0, "Embedded"),
            (4, True, True, 2, "Embedded"),  # RLE4 compression
            (8, False, True, 0, "Embedded"),
            (8, True, True, 0, "Embedded"),
            (8, True, False, 0, "Embedded"),
            (24, False, False, 0, "None"),
            (24, True, False, 0, "None"),
        ),
        # Second image: compositing mask
        (
            # bpp, size?, ncol?, comp, PaletteType
            (1, True, False, 0, "Embedded"),
            (1, False, False, 0, "Embedded"),
            (1, False, True, 0, "Embedded"),
            (4, True, True, 2, "Embedded"),
        ),
        # Third image: halo mask
        (
            # bpp, size?, ncol?, comp, PaletteType
            (1, True, False, 0, "Embedded"),  # kwensa
            (1, True, False, 0, "Embedded"),  # Jean-Luc, John Bruton
            (1, True, True, 0, "Embedded"),  # Jean-Luc, John Bruton
            (1, False, True, 0, "Embedded"),  # 75 files
            (1, False, False, 0, "Embedded"),  # shizuka
            (4, True, True, 2, "Embedded"),  # tom
            (8, False, True, 0, "Embedded"),  # missvampire
            (24, True, False, 0, "None"),  # 7 files
            (24, False, False, 0, "None"),  # 69 files
        ),
    ],
    "v66": [
        # First image: ...
        (
            # bpp, size?, ncol?, comp, PaletteType, flag
            (2, False, True, 0, "Implicit", 0x04),
            (4, True, True, 0, "Explicit", 0x02),
            (4, False, True, 0, "Explicit", 0x02),
            (8, False, True, 0, "Explicit", 0x02),
            (8, True, True, 0, "Explicit", 0x02),
            (8, True, False, 0, "Explicit", 0x02),
            (24, False, False, 0, "Empty", 0x02),
            (24, True, False, 0, "Empty", 0x02),
        ),
        # Second image: ...
        (
            # bpp, size?, ncol?, comp, PaletteType, flag
            (2, False, True, 0, "Implicit", 0x05),
        ),
        # Third image: ...
        (
            # bpp, size?, ncol?, comp, PaletteType, flag
            (1, False, True, 0, "Implicit", 0x03),
        ),
    ],
}
