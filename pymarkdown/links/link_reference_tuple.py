"""
Module to hold the tuple of information for creating a Link Reference Definition.
"""
from dataclasses import dataclass
from typing import Optional

from pymarkdown.links.link_reference_info import LinkReferenceInfo
from pymarkdown.links.link_reference_titles import LinkReferenceTitles


@dataclass(frozen=True)
class LinkReferenceDefinitionTuple:
    """
    Class to hold the tuple of information for creating a Link Reference Definition.
    """

    normalized_destination: Optional[str]
    link_titles: LinkReferenceTitles
    link_info: LinkReferenceInfo
