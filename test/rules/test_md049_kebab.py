"""
Module to provide tests related to the MD049 rule.
"""
from pymarkdown.plugins.rule_md_049 import anchor2regex


def test_german_umlaut():
    """
    Test to verify that CamelCase is converted into kebab-case
    """
    # Arrange
    text = "Äpfelknödel sind lecker"
    # Act
    result = anchor2regex("äpfelknödel-sind-lecker").match(text)
    # Assert
    assert result


def test_normal_english_headline():
    """
    Test to verify that CamelCase is converted into kebab-case
    """
    # Arrange
    text = "Some Headline with different stuff!"
    # Act
    result = anchor2regex("some-headline-with-different-stuff").match(text)
    # Assert
    assert result

def test_html_tags_in_heading():
    """
    Test to verify that CamelCase is converted into kebab-case
    """
    # Arrange
    text = "2- Adding a New Admin by <kbd> Change Role </kbd> Button in People Page"
    # Act
    result = anchor2regex(
        "2-adding-a-new-admin-by-change-role-button-in-people-page"
    ).match(text)
    # Assert
    assert result


def test_some_mixed_string():
    """
    Test to verify that CamelCase is converted into kebab-case
    """
    # Arrange
    text = "some-mixed_string With spaces_underscores-and-hyphens"
    # Act
    result = anchor2regex(
        "some-mixed-string-with-spaces-underscores-and-hyphens"
    ).match(text)
    # Assert
    assert result
