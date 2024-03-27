"""
Base class for images and links.
"""

# pylint: disable=too-many-instance-attributes
from typing import Optional, Tuple, Union

from typing_extensions import override

from pymarkdown.links.link_helper_properties import LinkHelperProperties
from pymarkdown.tokens.inline_markdown_token import InlineMarkdownToken
from pymarkdown.tokens.markdown_token import MarkdownToken


class ReferenceMarkdownToken(InlineMarkdownToken):
    """
    Base class for images and links.
    """

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        lhp: LinkHelperProperties,
        token_name: str,
        extra_data: Optional[str],
        text_from_blocks: str,
        line_number: int = 0,
        column_number: int = 0,
        requires_end_token: bool = False,
        can_force_close: bool = True,
    ):
        self.simple_extra_data = extra_data
        if lhp:
            (
                self.__label_type,
                self.__link_uri,
                self.__link_title,
                self.__pre_link_uri,
                self.__pre_link_title,
                self.__ex_label,
                self.__text_from_blocks,
                self.__did_use_angle_start,
                self.__inline_title_bounding_character,
                self.__before_link_whitespace,
                self.__before_title_whitespace,
                self.__after_title_whitespace,
            ) = (
                lhp.label_type,
                lhp.inline_link,
                lhp.inline_title,
                lhp.pre_inline_link,
                lhp.pre_inline_title,
                lhp.ex_label,
                text_from_blocks,
                lhp.did_use_angle_start,
                lhp.bounding_character,
                lhp.before_link_whitespace,
                lhp.before_title_whitespace,
                lhp.after_title_whitespace,
            )
        else:
            (
                self.__label_type,
                self.__link_uri,
                self.__link_title,
                self.__pre_link_uri,
                self.__pre_link_title,
                self.__ex_label,
                self.__text_from_blocks,
                self.__did_use_angle_start,
                self.__inline_title_bounding_character,
                self.__before_link_whitespace,
                self.__before_title_whitespace,
                self.__after_title_whitespace,
            ) = (
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                False,
                "",
                "",
                "",
                "",
            )

        assert self.__link_uri is not None, "This field should be defined."
        assert self.__label_type is not None, "This field should be defined."
        assert self.__pre_link_uri is not None, "This field should be defined."

        part_1, part_2 = self.__compose_extra_data_field(token_name)

        InlineMarkdownToken.__init__(
            self,
            token_name,
            f"{part_1}{part_2}",
            line_number=line_number,
            column_number=column_number,
            requires_end_token=requires_end_token,
            can_force_close=can_force_close,
        )

    # pylint: enable=too-many-arguments

    def __build_extra_data(
        self, extra_data: Optional[str], label_type: str
    ) -> Tuple[str, str]:
        assert self.__link_title is not None, "This field should be defined."
        assert self.__link_uri is not None, "This field should be defined."
        assert extra_data is not None, "This field should be defined."
        part_1 = MarkdownToken.extra_data_separator.join(
            [label_type, self.__link_uri, self.__link_title, extra_data]
        )
        assert (
            self.__inline_title_bounding_character is not None
        ), "This field should be defined."
        assert (
            self.__before_link_whitespace is not None
        ), "This field should be defined."
        assert (
            self.__before_title_whitespace is not None
        ), "This field should be defined."
        assert (
            self.__after_title_whitespace is not None
        ), "This field should be defined."
        assert self.__pre_link_title is not None, "This field should be defined."
        assert self.__ex_label is not None, "This field should be defined."
        assert self.__pre_link_uri is not None, "This field should be defined."
        part_2 = MarkdownToken.extra_data_separator.join(
            [
                self.__pre_link_uri,
                self.__pre_link_title,
                self.__ex_label,
                self.__text_from_blocks,
                str(self.__did_use_angle_start),
                self.__inline_title_bounding_character,
                self.__before_link_whitespace,
                self.__before_title_whitespace,
                self.__after_title_whitespace,
            ]
        )
        return part_1, part_2

    @property
    def label_type(self) -> str:
        """
        Returns the type of label that was used.
        """
        assert self.__label_type is not None, "Label type must be defined."
        return self.__label_type

    @property
    def link_uri(self) -> str:
        """
        Returns the URI for the link itself.
        """
        assert self.__link_uri is not None, "Link uri must be defined."
        return self.__link_uri

    @property
    def active_link_uri(self) -> str:
        """
        Returns the active URI for the link, preferring the __pre_link_uri over the __link_uri.
        """
        active_link = self.__pre_link_uri or self.__link_uri
        assert active_link is not None, "Active link must be defined."
        return active_link

    @property
    def link_title(self) -> Optional[str]:
        """
        Returns the text associated with the link's title.
        """
        return self.__link_title

    @property
    def active_link_title(self) -> Optional[str]:
        """
        Returns the active text associated with the link's title, preferring the __pre_link_title over the __link_title.
        """
        return self.__pre_link_title or self.__link_title

    @property
    def ex_label(self) -> Optional[str]:
        """
        Returns the text extracted from the blocks of the link, after processing.
        """
        return self.__ex_label

    @property
    def text_from_blocks(self) -> str:
        """
        Returns the text extracted from the blocks of the link, before processing.
        """
        return self.__text_from_blocks

    @property
    def did_use_angle_start(self) -> Optional[bool]:
        """
        Returns a value indicating whether an angle start was used around the URI.
        """
        return self.__did_use_angle_start

    @property
    def inline_title_bounding_character(self) -> Optional[str]:
        """
        Returns the bounding character used for the title.
        """
        return self.__inline_title_bounding_character

    @property
    def before_link_whitespace(self) -> Optional[str]:
        """
        Returns the whitespace extracted before the link.
        """
        return self.__before_link_whitespace

    @property
    def before_title_whitespace(self) -> Optional[str]:
        """
        Returns the whitespace extracted before the title.
        """
        return self.__before_title_whitespace

    @property
    def after_title_whitespace(self) -> Optional[str]:
        """
        Returns the whitespace extracted after the title.
        """
        return self.__after_title_whitespace

    def __compose_extra_data_field(self, token_name: str) -> Tuple[str, str]:
        """
        Compose the object's self.extra_data field from the local object's variables.
        """
        extra_data = (
            f"{self.simple_extra_data}{MarkdownToken.extra_data_separator}"
            if token_name == MarkdownToken._token_inline_image
            else self.simple_extra_data
        )

        # Purposefully split this way to accommodate the extra data
        assert self.__label_type is not None, "Label type must be defined."
        part_1, part_2 = self.__build_extra_data(extra_data, self.__label_type)
        self._set_extra_data(f"{part_1}{part_2}")
        return part_1, part_2

    @override
    def _modify_token(self, field_name: str, field_value: Union[str, int]) -> bool:
        if field_name == "text_from_blocks" and isinstance(field_value, str):
            self.__text_from_blocks = field_value
            self.__compose_extra_data_field(self.token_name)

            return True
        return False


# pylint: enable=too-many-instance-attributes
