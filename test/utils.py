"""
Module to provide helper methods for tests.
"""


def assert_if_lists_different(expected_tokens, actual_tokens):
    """
    Compart two lists and make sure they are equal, asserting if not.
    """

    print("expected_tokens:" + str(expected_tokens))
    print("actual_html:" + str(actual_tokens))
    assert expected_tokens == actual_tokens
