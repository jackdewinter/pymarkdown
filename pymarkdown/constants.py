"""
Constants
"""


# pylint: disable=too-few-public-methods
class Constants:
    """
    Constants to use throughout the parser.
    """

    whitespace = "\x20\x09\x0a\x0b\x0c\x0d"

    non_space_whitespace = whitespace[1:]

    ascii_control_characters = (
        "\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f"
        + "\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f"
        + "\x20\x7f"
    )

    unicode_whitespace = "\x20\x09\x0a\x0c\x0d\u00a0\u1680\u2000\u2001\u2002\u2003\u2004\u2005\u2006\u2007\u2008\u2009\u200A\u202F\u205F\u3000"

    punctuation_characters = (
        # standard ascii punctuation
        "\u0020\u0021\u0022\u0023\u0024\u0025\u0026\u0027\u0028"
        + "\u0029\u002a\u002b\u002c\u002d\u002e\u002f"
        + "\u003a\u003b\u003c\u003d\u003e\u003f\u0040"
        + "\u005b\u005c\u005d\u005e\u005f\u0060"
        + "\u007b\u007c\u007d\u007e"
    )
    # http://www.fileformat.info/info/unicode/category/index.htm
    # http://www.fileformat.info/info/unicode/category/P*/list.htm

    inline_emphasis = "*_"


# pylint: enable=too-few-public-methods
