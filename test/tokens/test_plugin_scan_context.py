from typing import Dict, List

from pymarkdown.general.main_presentation import MainPresentation
from pymarkdown.plugin_manager.fix_token_record import FixTokenRecord
from pymarkdown.plugin_manager.plugin_manager import PluginManager
from pymarkdown.plugin_manager.plugin_scan_context import PluginScanContext
from pymarkdown.tokens.markdown_token import MarkdownToken, MarkdownTokenClass


class __NotSupportedToken(MarkdownToken):
    """
    Token that is not supported and for testing purposes only.
    """

    def __init__(self) -> None:
        MarkdownToken.__init__(
            self,
            "unsupported",
            MarkdownTokenClass.SPECIAL,
        )


def test_plugin_scan_context_register_token_fix_no_map() -> None:
    """
    Test to make sure to try and change this token while reporting that we are in fix mode, but not in token fix mode.
    """

    # Arrange
    scan_context = PluginScanContext(
        PluginManager(MainPresentation()),
        "scan_file",
        [],
        fix_mode=True,
        file_output=None,
        fix_token_map=None,
        replace_tokens_list=None,
    )

    # Act
    scan_context.register_fix_token_request(
        __NotSupportedToken(), "ID001", "completed_file", "some-name", "some-value"
    )

    # Assert


def test_plugin_scan_context_register_token_first_one() -> None:
    """
    Test to register the first record against a token for fixing.
    """

    # Arrange
    token_map: Dict[MarkdownToken, List[FixTokenRecord]] = {}
    scan_context = PluginScanContext(
        PluginManager(MainPresentation()),
        "scan_file",
        [],
        fix_mode=True,
        file_output=None,
        fix_token_map=token_map,
        replace_tokens_list=None,
    )
    token_to_report = __NotSupportedToken()

    # Act
    scan_context.register_fix_token_request(
        token_to_report, "ID001", "completed_file", "some-name", "some-value"
    )

    # Assert
    assert token_to_report in token_map
    found_record_list = token_map[token_to_report]
    assert found_record_list
    assert len(found_record_list) == 1
    assert found_record_list[0].plugin_id == "ID001"


def test_plugin_scan_context_register_token_second_one() -> None:
    """
    Test to register the second record against a token for fixing.
    """

    # Arrange
    token_map: Dict[MarkdownToken, List[FixTokenRecord]] = {}
    scan_context = PluginScanContext(
        PluginManager(MainPresentation()),
        "scan_file",
        [],
        fix_mode=True,
        file_output=None,
        fix_token_map=token_map,
        replace_tokens_list=None,
    )
    token_to_report = __NotSupportedToken()
    scan_context.register_fix_token_request(
        token_to_report, "ID001", "completed_file", "some-name", "some-value"
    )

    # Act
    scan_context.register_fix_token_request(
        token_to_report,
        "ID002",
        "completed_file",
        "some-other-name",
        "some-other-value",
    )

    # Assert
    assert token_to_report in token_map
    found_record_list = token_map[token_to_report]
    assert found_record_list
    assert len(found_record_list) == 2
    assert found_record_list[0].plugin_id == "ID001"
    assert found_record_list[1].plugin_id == "ID002"
