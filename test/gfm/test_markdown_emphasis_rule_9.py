"""
https://github.github.com/gfm/#emphasis-and-strong-emphasis
"""

from test.utils import act_and_assert

import pytest


@pytest.mark.gfm
def test_emphasis_413() -> None:
    """
    Test case 413:  (part 1) Any nonempty sequence of inline elements can be the contents of an emphasized span.
    """

    # Arrange
    source_markdown = """*foo [bar](/url)*"""
    expected_tokens = [
        "[para(1,1):]",
        "[emphasis(1,1):1:*]",
        "[text(1,2):foo :]",
        "[link(1,6):inline:/url:::::bar:False::::]",
        "[text(1,7):bar:]",
        "[end-link::]",
        "[end-emphasis(1,17)::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><em>foo <a href="/url">bar</a></em></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_emphasis_414() -> None:
    """
    Test case 414:  (part 2) Any nonempty sequence of inline elements can be the contents of an emphasized span.
    """

    # Arrange
    source_markdown = """*foo
bar*"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[emphasis(1,1):1:*]",
        "[text(1,2):foo\nbar::\n]",
        "[end-emphasis(2,4)::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><em>foo
bar</em></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_emphasis_415() -> None:
    """
    Test case 415:  (part 1) In particular, emphasis and strong emphasis can be nested inside emphasis:
    """

    # Arrange
    source_markdown = """_foo __bar__ baz_"""
    expected_tokens = [
        "[para(1,1):]",
        "[emphasis(1,1):1:_]",
        "[text(1,2):foo :]",
        "[emphasis(1,6):2:_]",
        "[text(1,8):bar:]",
        "[end-emphasis(1,11)::]",
        "[text(1,13): baz:]",
        "[end-emphasis(1,17)::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><em>foo <strong>bar</strong> baz</em></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_emphasis_416() -> None:
    """
    Test case 416:  (part 2) In particular, emphasis and strong emphasis can be nested inside emphasis:
    """

    # Arrange
    source_markdown = """_foo _bar_ baz_"""
    expected_tokens = [
        "[para(1,1):]",
        "[emphasis(1,1):1:_]",
        "[text(1,2):foo :]",
        "[emphasis(1,6):1:_]",
        "[text(1,7):bar:]",
        "[end-emphasis(1,10)::]",
        "[text(1,11): baz:]",
        "[end-emphasis(1,15)::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><em>foo <em>bar</em> baz</em></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_emphasis_417() -> None:
    """
    Test case 417:  (part 3) In particular, emphasis and strong emphasis can be nested inside emphasis:
    """

    # Arrange
    source_markdown = """__foo_ bar_"""
    expected_tokens = [
        "[para(1,1):]",
        "[emphasis(1,1):1:_]",
        "[emphasis(1,2):1:_]",
        "[text(1,3):foo:]",
        "[end-emphasis(1,6)::]",
        "[text(1,7): bar:]",
        "[end-emphasis(1,11)::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><em><em>foo</em> bar</em></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_emphasis_418() -> None:
    """
    Test case 418:  (part 4) In particular, emphasis and strong emphasis can be nested inside emphasis:
    """

    # Arrange
    source_markdown = """*foo *bar**"""
    expected_tokens = [
        "[para(1,1):]",
        "[emphasis(1,1):1:*]",
        "[text(1,2):foo :]",
        "[emphasis(1,6):1:*]",
        "[text(1,7):bar:]",
        "[end-emphasis(1,10)::]",
        "[end-emphasis(1,11)::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><em>foo <em>bar</em></em></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_emphasis_419() -> None:
    """
    Test case 419:  (part 5) In particular, emphasis and strong emphasis can be nested inside emphasis:
    """

    # Arrange
    source_markdown = """*foo **bar** baz*"""
    expected_tokens = [
        "[para(1,1):]",
        "[emphasis(1,1):1:*]",
        "[text(1,2):foo :]",
        "[emphasis(1,6):2:*]",
        "[text(1,8):bar:]",
        "[end-emphasis(1,11)::]",
        "[text(1,13): baz:]",
        "[end-emphasis(1,17)::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><em>foo <strong>bar</strong> baz</em></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_emphasis_420() -> None:
    """
    Test case 420:  (part 6) In particular, emphasis and strong emphasis can be nested inside emphasis:
    """

    # Arrange
    source_markdown = """*foo**bar**baz*"""
    expected_tokens = [
        "[para(1,1):]",
        "[emphasis(1,1):1:*]",
        "[text(1,2):foo:]",
        "[emphasis(1,5):2:*]",
        "[text(1,7):bar:]",
        "[end-emphasis(1,10)::]",
        "[text(1,12):baz:]",
        "[end-emphasis(1,15)::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><em>foo<strong>bar</strong>baz</em></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_emphasis_421() -> None:
    """
    Test case 421:  For the same reason, we don’t get two consecutive emphasis sections in this example:
    """

    # Arrange
    source_markdown = """*foo**bar*"""
    expected_tokens = [
        "[para(1,1):]",
        "[emphasis(1,1):1:*]",
        "[text(1,2):foo**bar:]",
        "[end-emphasis(1,10)::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><em>foo**bar</em></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_emphasis_422() -> None:
    """
    Test case 422:  (part 1) The same condition ensures that the following cases are all strong emphasis nested inside emphasis, even when the interior spaces are omitted:
    """

    # Arrange
    source_markdown = """***foo** bar*"""
    expected_tokens = [
        "[para(1,1):]",
        "[emphasis(1,1):1:*]",
        "[emphasis(1,2):2:*]",
        "[text(1,4):foo:]",
        "[end-emphasis(1,7)::]",
        "[text(1,9): bar:]",
        "[end-emphasis(1,13)::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><em><strong>foo</strong> bar</em></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_emphasis_423() -> None:
    """
    Test case 423:  (part 2) The same condition ensures that the following cases are all strong emphasis nested inside emphasis, even when the interior spaces are omitted:
    """

    # Arrange
    source_markdown = """*foo **bar***"""
    expected_tokens = [
        "[para(1,1):]",
        "[emphasis(1,1):1:*]",
        "[text(1,2):foo :]",
        "[emphasis(1,6):2:*]",
        "[text(1,8):bar:]",
        "[end-emphasis(1,11)::]",
        "[end-emphasis(1,13)::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><em>foo <strong>bar</strong></em></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_emphasis_424() -> None:
    """
    Test case 424:  (part 3) The same condition ensures that the following cases are all strong emphasis nested inside emphasis, even when the interior spaces are omitted:
    """

    # Arrange
    source_markdown = """*foo**bar***"""
    expected_tokens = [
        "[para(1,1):]",
        "[emphasis(1,1):1:*]",
        "[text(1,2):foo:]",
        "[emphasis(1,5):2:*]",
        "[text(1,7):bar:]",
        "[end-emphasis(1,10)::]",
        "[end-emphasis(1,12)::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><em>foo<strong>bar</strong></em></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_emphasis_425() -> None:
    """
    Test case 425:  (part 1) When the lengths of the interior closing and opening delimiter runs are both multiples of 3, though, they can match to create emphasis:
    """

    # Arrange
    source_markdown = """foo***bar***baz"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):foo:]",
        "[emphasis(1,4):1:*]",
        "[emphasis(1,5):2:*]",
        "[text(1,7):bar:]",
        "[end-emphasis(1,10)::]",
        "[end-emphasis(1,12)::]",
        "[text(1,13):baz:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>foo<em><strong>bar</strong></em>baz</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_emphasis_426() -> None:
    """
    Test case 426:  (part 2) When the lengths of the interior closing and opening delimiter runs are both multiples of 3, though, they can match to create emphasis:
    """

    # Arrange
    source_markdown = """foo******bar*********baz"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):foo:]",
        "[emphasis(1,4):2:*]",
        "[emphasis(1,6):2:*]",
        "[emphasis(1,8):2:*]",
        "[text(1,10):bar:]",
        "[end-emphasis(1,13)::]",
        "[end-emphasis(1,15)::]",
        "[end-emphasis(1,17)::]",
        "[text(1,19):***baz:]",
        "[end-para:::True]",
    ]
    expected_gfm = (
        """<p>foo<strong><strong><strong>bar</strong></strong></strong>***baz</p>"""
    )

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_emphasis_427() -> None:
    """
    Test case 427:  (part 1) When the lengths of the interior closing and opening delimiter runs are both multiples of 3, though, they can match to create emphasis:
    """

    # Arrange
    source_markdown = """*foo **bar *baz* bim** bop*"""
    expected_tokens = [
        "[para(1,1):]",
        "[emphasis(1,1):1:*]",
        "[text(1,2):foo :]",
        "[emphasis(1,6):2:*]",
        "[text(1,8):bar :]",
        "[emphasis(1,12):1:*]",
        "[text(1,13):baz:]",
        "[end-emphasis(1,16)::]",
        "[text(1,17): bim:]",
        "[end-emphasis(1,21)::]",
        "[text(1,23): bop:]",
        "[end-emphasis(1,27)::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><em>foo <strong>bar <em>baz</em> bim</strong> bop</em></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_emphasis_428() -> None:
    """
    Test case 428:  (part 2) When the lengths of the interior closing and opening delimiter runs are both multiples of 3, though, they can match to create emphasis:
    """

    # Arrange
    source_markdown = """*foo [*bar*](/url)*"""
    expected_tokens = [
        "[para(1,1):]",
        "[emphasis(1,1):1:*]",
        "[text(1,2):foo :]",
        "[link(1,6):inline:/url:::::*bar*:False::::]",
        "[emphasis(1,7):1:*]",
        "[text(1,8):bar:]",
        "[end-emphasis(1,11)::]",
        "[end-link::]",
        "[end-emphasis(1,19)::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><em>foo <a href="/url"><em>bar</em></a></em></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_emphasis_429() -> None:
    """
    Test case 429:  (part 1) There can be no empty emphasis or strong emphasis:
    """

    # Arrange
    source_markdown = """** is not an empty emphasis"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):** is not an empty emphasis:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>** is not an empty emphasis</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_emphasis_430() -> None:
    """
    Test case 430:  (part 2) There can be no empty emphasis or strong emphasis:
    """

    # Arrange
    source_markdown = """**** is not an empty strong emphasis"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):**** is not an empty strong emphasis:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>**** is not an empty strong emphasis</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)
