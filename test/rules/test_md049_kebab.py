"""
Module to provide tests related to the MD049 rule.
"""
from pymarkdown.plugins.rule_md_049 import compare_anchor


def test_german_umlaut():
    """
    Test to verify that CamelCase is converted into kebab-case
    """
    # Arrange
    text = "Äpfelknödel sind lecker"
    # Act
    result = compare_anchor("äpfelknödel-sind-lecker", text)
    # Assert
    assert result


def test_normal_english_headline():
    """
    Test to verify that CamelCase is converted into kebab-case
    """
    # Arrange
    text = "Some Headline with different stuff!"
    # Act
    result = compare_anchor("some-headline-with-different-stuff", text)
    # Assert
    assert result


def test_html_tags_in_heading():
    """
    Test to verify that CamelCase is converted into kebab-case
    """
    # Arrange
    text = "2- Adding a New Admin by <kbd> Change Role </kbd> Button in People Page"
    # Act
    result = compare_anchor(
        "2-adding-a-new-admin-by-change-role-button-in-people-page", text
    )
    # Assert
    assert result


def test_html_tags_in_heading2():
    """
    Test to verify that CamelCase is converted into kebab-case
    """
    # Arrange
    text = "2- Adding a New Admin by <kbd> Change Role </kbd> Button in People Page"
    # Act
    result = compare_anchor(
        "2-adding-a-new-admin-by-kbd-change-role-button-in-people-page", text
    )
    # Assert
    assert not result


def test_tiggs_in_heading():
    """
    Test to verify that CamelCase is converted into kebab-case
    """
    # Arrange
    text = "Adding a New Admin by `Button in People Page`"
    # Act
    result = compare_anchor("adding-a-new-admin-by-button-in-people-page", text)
    # Assert
    assert result


def test_slash_in_heading():
    """
    Test to verify that CamelCase is converted into kebab-case
    """
    # Arrange
    text = "TB-Workflow JOBP_ZS000TB01_CIS-Auto [System/Client/Plant]"
    # Act
    result = compare_anchor(
        "tb-workflow-jobp_zs000tb01_cis-auto-systemclientplant", text
    )
    # Assert
    assert result


def test_some_mixed_string():
    """
    Test to verify that CamelCase is converted into kebab-case
    """
    # Arrange
    text = "some-mixed_string With spaces_underscores-and-hyphens"
    # Act
    result = compare_anchor(
        "some-mixed-string-with-spaces-underscores-and-hyphens", text
    )
    # Assert
    assert result
