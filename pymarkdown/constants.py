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

    __unicode_whitespace = ConstantWrapper(
        "\x20\x09\x0a\x0c\x0d\u00a0\u1680\u2000\u2001\u2002\u2003\u2004\u2005\u2006\u2007"
        + "\u2008\u2009\u200A\u202F\u205F\u3000"
    )

    __punctuation_characters = ConstantWrapper(
        # standard ascii punctuation
        "\u0020\u0021\u0022\u0023\u0024\u0025\u0026\u0027\u0028"
        + "\u0029\u002a\u002b\u002c\u002d\u002e\u002f"
        + "\u003a\u003b\u003c\u003d\u003e\u003f\u0040"
        + "\u005b\u005c\u005d\u005e\u005f\u0060"
        + "\u007b\u007c\u007d\u007e"
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
