"""
Module to provide tests related to the MD049 rule.
"""
from pymarkdown.plugins.rule_md_049 import compare_anchor


def test_german_umlaut():
    """
    Test to verify that CamelCase is converted into kebab-case
    """
    # Arrange
    text = "Äp\u2764fel  \xA1 knödel \xA0 sind \xA0 lecker \u2764"
    # Act
    result = compare_anchor("äpfel---knödel---sind---lecker-", text)
    # Assert
    assert result


def test_numbers():
    """
    Test to verify that CamelCase is converted into kebab-case
    """
    # Arrange
    text = "1.1 test 2"
    # Act
    result = compare_anchor("11-test-2", text)
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


def test_inlinecode_in_heading():
    """
    Test to verify that CamelCase is converted into kebab-case
    """
    # Arrange
    text = "TB-IMG-Activity `/DTBOM/00_CHSETB `: Assign a table to Change  Set"
    # Act
    result = compare_anchor(
        "tb-img-activity-dtbom00_chsetb--assign-a-table-to-change--set", text
    )
    # Assert
    assert result


def test_inlinecode_extrem_in_heading():
    """
    Test to verify that CamelCase is converted into kebab-case
    """
    # Arrange
    text = "TB-Workflow `<Name>[Parameters]`"
    # Act
    result = compare_anchor("tb-workflow-nameparameters", text)
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
        "some-mixed_string-with-spaces_underscores-and-hyphens", text
    )
    # Assert
    assert result
