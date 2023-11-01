"""
Constants
"""


from typing import Any, Callable, Union, cast


class ClassProperty(property):
    """
    Decorator class to allow for a classmethod to expose a "class property".
    """

    def __get__(self, __obj: Any, owner: Union[type, None] = ...) -> Any:  # type: ignore
        _ = __obj
        fget_x = cast(Callable[..., Any], self.fget)
        return classmethod(fget_x).__get__(None, owner)()


class ConstantWrapper:
    """
    Simple class to provide for container that only allows
    read-only access to the value.
    """

    def __init__(self, value_to_wrap: Any) -> None:
        self.__wrapped_value = value_to_wrap

    def value(self) -> Any:
        """
        Raw value that is wrapped.
        """
        return self.__wrapped_value

    def contains(self, value: Any) -> bool:
        """
        Whether the specified value is contained within the wrapped value.
        """
        return value in self.__wrapped_value


class Constants:
    """
    Constants to use throughout the parser.
    """

    __ascii_whitespace = "\x20\x09\x0a\x0b\x0c\x0d"

    __non_space_ascii_whitespace = __ascii_whitespace[1:]

    __ascii_control_characters = (
        "\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f"
        + "\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f"
        + "\x20\x7f"
    )

    # https://www.compart.com/en/unicode/category/Zs
    __unicode_whitespace = ConstantWrapper(
        "\x20\x09\x0a\x0c\x0d\u00a0\u1680\u2000\u2001\u2002\u2003\u2004\u2005\u2006\u2007"
        + "\u2008\u2009\u200A\u202F\u205F\u3000"
    )

    __punctuation_characters = ConstantWrapper(
        # standard ascii punctuation - https://github.github.com/gfm/#ascii-punctuation-character
        "\u0021\u0022\u0023\u0024\u0025\u0026\u0027\u0028\u0029\u002a\u002b\u002c\u002d\u002e\u002f"
        + "\u003a\u003b\u003c\u003d\u003e\u003f\u0040"
        + "\u005b\u005c\u005d\u005e\u005f\u0060"
        + "\u007b\u007c\u007d\u007e"
        # Pc - Connector Punctuation - https://www.compart.com/en/unicode/category/Pc
        + "\u005f"
        + "\u203f\u2040\u2054"
        + "\ufe33\ufe34\ufe4d\ufe4e\ufe4f"
        + "\uff3f"
        # Pd - Dash Punctuation - https://www.compart.com/en/unicode/category/Pd
        + "\u002d\u058a\u05be"
        + "\u1400\u1806"
        + "\u2010\u2011\u2012\u2013\u2014\u2015"
        + "\u2e17\u2e1a\u2e3a\u2e3b\u2e40"
        + "\u301c\u3030\u30a0"
        + "\ufe31\ufe32\ufe58\ufe63"
        + "\uff0d"
        + "\U00010ead"
        # Pe - Close Punctuation - https://www.compart.com/en/unicode/category/Pe
        + "\u0029\u005d\u007d"
        + "\u0f3b\u0f3d"
        + "\u169c"
        + "\u2046\u207e\u208e"
        + "\u2309\u230b\u232a"
        + "\u2769\u276b\u276d\u276f\u2771\u2773\u2775\u27c6\u27e7\u27e9\u27eb\u27ed\u27ef"
        + "\u2984\u2986\u2988\u298a\u298c\u298e\u2990\u2992\u2994\u2996\u2998\u29d9\u29db\u29fd"
        + "\u2e23\u2e25\u2e27\u2e29"
        + "\u3009\u300b\u300d\u300f\u3011\u3015\u3017\u3019\u301b\u301e\u301f"
        + "\ufd3e"
        + "\ufe18\ufe36\ufe38\ufe3a\ufe3c\ufe3e\ufe40\ufe42\ufe44\ufe48\ufe5a\ufe5c\ufe5e"
        + "\uff09\uff3d\uff5d\uff60\uff63"
        # Pf - Final Punctuation - https://www.compart.com/en/unicode/category/Pf
        + "\u00bb"
        + "\u2019\u201d\u203a"
        + "\u2e03\u2e05\u2e0a\u2e0d\u2e1d\u2e21"
        # Pi - Initial Punctuation - https://www.compart.com/en/unicode/category/Pi
        + "\u00ab"
        + "\u2018\u201b\u201c\u201f\u2039"
        + "\u2e02\u2e04\u2e09\u2e0c\u2e1c\u2e20"
        # Po - Other Punctuation - https://www.compart.com/en/unicode/category/Po
        + "\u0021\u0022\u0023\u0025\u0026\u0027\u002a\u002c\u002e\u002f\u003a\u003b\u003f\u0040\u005c"
        + "\u00a1\u00a7\u00b6\u00b7\u00bf"
        + "\u037e\u0387"
        + "\u055a\u055b\u055c\u055d\u055e\u055f\u0589\u05c0\u05c3\u05c6\u05f3\u05f4"
        + "\u0609\u060a\u060c\u060d\u061b\u061e\u061f\u066a\u066b\u066c\u066d\u06d4"
        + "\u0700\u0701\u0702\u0703\u0704\u0705\u0706\u0707\u0708\u0709\u070a\u070b\u070c\u070d\u07f7\u07f8\u07f9"
        + "\u0830\u0831\u0832\u0833\u0834\u0835\u0836\u0837\u0838\u0839\u083a\u083b\u083c\u083d\u083e\u085e"
        + "\u0964\u0965\u0970\u09fd"
        + "\u0a76\u0af0"
        + "\u0c77\u0c84"
        + "\u0df4"
        + "\u0e4f\u0e5a\u0e5b"
        + "\u0f04\u0f05\u0f06\u0f07\u0f08\u0f09\u0f0a\u0f0b\u0f0c\u0f0d\u0f0e\u0f0f\u0f10\u0f11\u0f12\u0f14\u0f85\u0fd0\u0fd1\u0fd2\u0fd3\u0fd4\u0fd9\u0fda"
        + "\u104a\u104b\u104c\u104d\u104e\u104f\u10fb"
        + "\u1360\u1361\u1362\u1363\u1364\u1365\u1366\u1367\u1368"
        + "\u166e\u16eb\u16ec\u16ed"
        + "\u1735\u1736\u17d4\u17d5\u17d6\u17d8\u17d9\u17da"
        + "\u1800\u1801\u1802\u1803\u1804\u1805\u1807\u1808\u1809\u180a"
        + "\u1944\u1945"
        + "\u1a1e\u1a1f\u1aa0\u1aa1\u1aa2\u1aa3\u1aa4\u1aa5\u1aa6\u1aa8\u1aa9\u1aaa\u1aab\u1aac\u1aad"
        + "\u1b5a\u1b5b\u1b5c\u1b5d\u1b5e\u1b5f\u1b60\u1bfc\u1bfd\u1bfe\u1bff"
        + "\u1c3b\u1c3c\u1c3d\u1c3e\u1c3f\u1c7e\u1c7f\u1cc0\u1cc1\u1cc2\u1cc3\u1cc4\u1cc5\u1cc6\u1cc7\u1cd3"
        + "\u2016\u2017\u2020\u2021\u2022\u2023\u2024\u2025\u2026\u2027\u2030\u2031\u2032\u2033\u2034\u2035\u2036\u2037\u2038\u203b\u203c\u203d\u203e\u2041\u2042\u2043\u2047\u2048\u2049\u204a\u204b\u204c\u204d\u204e\u204f\u2050\u2051\u2053\u2055\u2056\u2057\u2058\u2059\u205a\u205b\u205c\u205d\u205e"
        + "\u2cf9\u2cfa\u2cfb\u2cfc\u2cfe\u2cff"
        + "\u2d70"
        + "\u2e00\u2e01\u2e06\u2e07\u2e08\u2e0b\u2e0e\u2e0f\u2e10\u2e11\u2e12\u2e13\u2e14\u2e15\u2e16\u2e18\u2e19\u2e1b\u2e1e\u2e1f\u2e2a\u2e2b\u2e2c\u2e2d\u2e2e\u2e30\u2e31\u2e32\u2e33\u2e34\u2e35\u2e36\u2e37\u2e38\u2e39\u2e3c\u2e3d\u2e3e\u2e3f\u2e41\u2e43\u2e44\u2e45\u2e46\u2e47\u2e48\u2e49\u2e4a\u2e4b\u2e4c\u2e4d\u2e4e\u2e4f\u2e52"
        + "\u3001\u3002\u3003\u303d\u30fb"
        + "\ua4fe\ua4ff"
        + "\ua60d\ua60e\ua60f\ua673\ua67e\ua6f2\ua6f3\ua6f4\ua6f5\ua6f6\ua6f7"
        + "\ua874\ua875\ua876\ua877\ua8ce\ua8cf\ua8f8\ua8f9\ua8fa\ua8fc"
        + "\ua92e\ua92f\ua95f\ua9c1\ua9c2\ua9c3\ua9c4\ua9c5\ua9c6\ua9c7\ua9c8\ua9c9\ua9ca\ua9cb\ua9cc\ua9cd\ua9de\ua9df"
        + "\uaa5c\uaa5d\uaa5e\uaa5f\uaade\uaadf\uaaf0\uaaf1"
        + "\uabeb"
        + "\ufe10\ufe11\ufe12\ufe13\ufe14\ufe15\ufe16\ufe19\ufe30\ufe45\ufe46\ufe49\ufe4a\ufe4b\ufe4c\ufe50\ufe51\ufe52\ufe54\ufe55\ufe56\ufe57\ufe5f\ufe60\ufe61\ufe68\ufe6a\ufe6b"
        + "\uff01\uff02\uff03\uff05\uff06\uff07\uff0a\uff0c\uff0e\uff0f\uff1a\uff1b\uff1f\uff20\uff3c\uff61\uff64\uff65"
        # 10100...
        + "\U00010100\U00010101\U00010102\U0001039f\U000103d0\U0001056f\U00010857\U0001091f\U0001093f\U00010a50\U00010a51\U00010a52\U00010a53"
        + "\U00010a54\U00010a55\U00010a56\U00010a57\U00010a58\U00010a7f\U00010af0\U00010af1\U00010af2\U00010af3\U00010af4\U00010af5"
        + "\U00010af6\U00010b39\U00010b3a\U00010b3b\U00010b3c\U00010b3d\U00010b3e\U00010b3f\U00010b99\U00010b9a\U00010b9b\U00010b9c"
        + "\U00010f55\U00010f56\U00010f57\U00010f58\U00010f59\U00011047\U00011048\U00011049\U0001104a\U0001104b\U0001104c\U0001104d"
        + "\U000110bb\U000110bc\U000110be\U000110bf\U000110c0\U000100c1\U00011140\U00011141\U00011142\U00011143\U00011174\U00011175"
        + "\U000111c5\U000111c6\U000111c7\U000111c8\U000111cd\U000111db\U000111dd\U000111de\U000111df\U00011238\U00011239\U0001123a"
        + "\U0001123b\U0001123c\U0001123d\U000112a9\U0001144b\U0001144c\U0001144d\U0001144e\U0001144f\U0001145a\U0001145b\U0001145d"
        + "\U000114c6\U000115c1\U000115c2\U000115c3\U000115c4\U000115c5\U000115c6\U000115c7\U000115c8\U000115c9\U000115ca\U000115cb"
        + "\U000115cc\U000115cd\U000115ce\U000115cf\U000115d0\U000115d1\U000115d2\U000115d3\U000115d4\U000115d5\U000115d6\U000115d7"
        + "\U00011641\U00011642\U00011643\U00011660\U00011661\U00011662\U00011663\U00011664\U00011665\U00011666\U00011667\U00011668"
        + "\U00011669\U0001166a\U0001166b\U0001166c\U0001173c\U0001173d\U0001173e\U0001183b\U00011944\U00011945\U00011946\U000119e2"
        + "\U00011a3f\U00011a40\U00011a41\U00011a42\U00011a43\U00011a44\U00011a45\U00011a46\U00011a9a\U00011a9b\U00011a9c\U00011a9e"
        + "\U00011a9f\U00011aa0\U00011aa1\U00011aa2\U00011c41\U00011c42\U00011c43\U00011c44\U00011c45\U00011c70\U00011c71\U00011ef7"
        + "\U00011ef8\U00011fff\U00012470\U00012471\U00012472\U00012473\U00012474\U00016a6e\U00016a6f\U00016af5\U00016b37\U00016b38"
        + "\U00016b39\U00016b3a\U00016b3b\U00016b44\U00016e97\U00016e98\U00016e99\U00016e9a\U00016fe2\U0001bc9f\U0001da87\U0001da88"
        + "\U0001da89\U0001da8a\U0001da8b\U0001e95e\U0001e95f"
        # Ps - Open Punctuation - https://www.compart.com/en/unicode/category/Ps
        + "\u0028\u005b\u007b"
        + "\u0f3a\u0f3c"
        + "\u169b"
        + "\u201a\u201e\u2045\u207d\u208d"
        + "\u2308\u230a\u2329"
        + "\u2768\u276a\u276c\u276e\u2770\u2772\u2774\u27c5\u27e6\u27e8\u27ea\u27ec\u27ee"
        + "\u2983\u2985\u2987\u2989\u298b\u298d\u298f\u2991\u2993\u2995\u2997\u29d8\u29da\u29fc"
        + "\u2e22\u2e24\u2e26\u2e28\u2e42"
        + "\u3008\u300a\u300c\u300e\u3010\u3014\u3016\u3018\u301a\u301d"
        + "\ufd3f"
        + "\ufe17\ufe35\ufe37\ufe39\ufe3b\ufe3d\ufe3f\ufe41\ufe43\ufe47\ufe59\ufe5b\ufe5d"
        + "\uff08\uff3b\uff5b\uff3f\uff62"
    )

    link_type__inline = "inline"
    link_type__full = "full"
    link_type__shortcut = "shortcut"
    link_type__collapsed = "collapsed"

    # http://www.fileformat.info/info/unicode/category/index.htm
    # http://www.fileformat.info/info/unicode/category/P*/list.htm

    @ClassProperty
    def punctuation_characters(self) -> ConstantWrapper:
        """
        Standard punctuation characters.
        """
        return self.__punctuation_characters

    @ClassProperty
    def unicode_whitespace(self) -> ConstantWrapper:
        """
        Unicode whitespace characters.
        """
        return self.__unicode_whitespace

    @ClassProperty
    def ascii_control_characters(self) -> str:
        """
        Standard ASCII control characters, below 0x00-0x1f and 0x7f.
        """
        return self.__ascii_control_characters

    @ClassProperty
    def non_space_ascii_whitespace(self) -> str:
        """
        Standard ASCII whitespace characters minus the space character.
        """
        return self.__non_space_ascii_whitespace

    @ClassProperty
    def ascii_whitespace(self) -> str:
        """
        Standard ASCII whitespace characters.
        """
        return self.__ascii_whitespace
