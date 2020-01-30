"""
Module to provide helper methods for tests.
"""


def assert_if_lists_different(expected_tokens, actual_tokens):
    """
    Compart two lists and make sure they are equal, asserting if not.
    """

    print("expected_tokens:" + str(expected_tokens))
    print("actual_html:" + str(actual_tokens))
    assert len(expected_tokens) == len(actual_tokens), "List lengths are not the same."

    # pylint: disable=consider-using-enumerate
    for element_index in range(0, len(expected_tokens)):
        assert str(expected_tokens[element_index]) == str(
            actual_tokens[element_index]
        ), ("List items " + str(element_index) + " are not equal.")
    # pylint: enable=consider-using-enumerate
