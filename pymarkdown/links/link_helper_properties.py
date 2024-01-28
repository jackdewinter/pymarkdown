"""
Module to help contain the elements of a link.
"""

# pylint: disable=too-many-instance-attributes
from dataclasses import dataclass
from typing import Optional


@dataclass
class LinkHelperProperties:
    """
    Class to help contain the elements of a link.
    """

    ex_label: Optional[str]
    label_type: Optional[str]
    before_link_whitespace: Optional[str]
    inline_link: Optional[str]
    pre_inline_link: Optional[str]
    before_title_whitespace: Optional[str]
    bounding_character: Optional[str]
    inline_title: Optional[str]
    pre_inline_title: Optional[str]
    after_title_whitespace: Optional[str]
    did_use_angle_start: Optional[bool]

    def __init__(self) -> None:
        self.ex_label = None
        self.label_type = None
        self.did_use_angle_start = False
        self.before_link_whitespace = None
        self.inline_link = None
        self.pre_inline_link = None
        self.before_title_whitespace = None
        self.bounding_character = None
        self.inline_title = None
        self.pre_inline_title = None
        self.after_title_whitespace = None


# pylint: enable=too-many-instance-attributes
