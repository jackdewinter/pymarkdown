"""
https://github.github.com/gfm/#images
"""
import pytest

from pymarkdown.tokenized_markdown import TokenizedMarkdown

from .utils import assert_if_lists_different


@pytest.mark.skip
def test_image_link_580():
    """
    Test case 580:  (part 1) Syntax for images is like the syntax for links, with one difference
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """![foo](/url "title")"""
    expected_tokens = [
        "[ulist:-::2:]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


@pytest.mark.skip
def test_image_link_581():
    """
    Test case 581:  (part 2) Syntax for images is like the syntax for links, with one difference
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """![foo *bar*]

[foo *bar*]: train.jpg "train & tracks"
"""
    expected_tokens = [
        "[ulist:-::2:]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


@pytest.mark.skip
def test_image_link_582():
    """
    Test case 582:  (part 3) Syntax for images is like the syntax for links, with one difference
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """![foo ![bar](/url)](/url2)"""
    expected_tokens = [
        "[ulist:-::2:]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


@pytest.mark.skip
def test_image_link_583():
    """
    Test case 583:  (part 4) Syntax for images is like the syntax for links, with one difference
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """![foo [bar](/url)](/url2)"""
    expected_tokens = [
        "[ulist:-::2:]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


@pytest.mark.skip
def test_image_link_584():
    """
    Test case 584:  (part 1) Only the plain string content is rendered, without formatting.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """![foo *bar*][]

[foo *bar*]: train.jpg "train & tracks"
"""
    expected_tokens = [
        "[ulist:-::2:]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


@pytest.mark.skip
def test_image_link_585():
    """
    Test case 585:  (part 2) Only the plain string content is rendered, without formatting.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """![foo *bar*][foobar]

[FOOBAR]: train.jpg "train & tracks"
"""
    expected_tokens = [
        "[ulist:-::2:]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


@pytest.mark.skip
def test_image_link_586():
    """
    Test case 586:  (part 3) Only the plain string content is rendered, without formatting.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """![foo](train.jpg)"""
    expected_tokens = [
        "[ulist:-::2:]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


@pytest.mark.skip
def test_image_link_587():
    """
    Test case 587:  (part 4) Only the plain string content is rendered, without formatting.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """My ![foo bar](/path/to/train.jpg  "title"   )"""
    expected_tokens = [
        "[ulist:-::2:]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


@pytest.mark.skip
def test_image_link_588():
    """
    Test case 588:  (part 5) Only the plain string content is rendered, without formatting.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """![foo](<url>)"""
    expected_tokens = [
        "[ulist:-::2:]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


@pytest.mark.skip
def test_image_link_589():
    """
    Test case 589:  (part 6) Only the plain string content is rendered, without formatting.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """![](/url)"""
    expected_tokens = [
        "[ulist:-::2:]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


@pytest.mark.skip
def test_image_link_590():
    """
    Test case 590:  (part 1) Reference-style:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """![foo][bar]

[bar]: /url"""
    expected_tokens = [
        "[ulist:-::2:]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


@pytest.mark.skip
def test_image_link_591():
    """
    Test case 591:  (part 2) Reference-style:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """![foo][bar]

[BAR]: /url"""
    expected_tokens = [
        "[ulist:-::2:]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


@pytest.mark.skip
def test_image_link_592():
    """
    Test case 592:  (part 1) Collapsed:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """![foo][]

[foo]: /url "title"
"""
    expected_tokens = [
        "[ulist:-::2:]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


@pytest.mark.skip
def test_image_link_593():
    """
    Test case 593:  (part 2) Collapsed:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """![*foo* bar][]

[*foo* bar]: /url "title"
"""
    expected_tokens = [
        "[ulist:-::2:]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


@pytest.mark.skip
def test_image_link_594():
    """
    Test case 594:  The labels are case-insensitive:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """![Foo][]

[foo]: /url "title"
"""
    expected_tokens = [
        "[ulist:-::2:]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


@pytest.mark.skip
def test_image_link_595():
    """
    Test case 595:  As with reference links, whitespace is not allowed between the two sets of brackets:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """![foo]\a
[]

[foo]: /url "title"
""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[ulist:-::2:]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


@pytest.mark.skip
def test_image_link_596():
    """
    Test case 596:  (part 1) Shortcut
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """![foo]

[foo]: /url "title"
"""
    expected_tokens = [
        "[ulist:-::2:]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


@pytest.mark.skip
def test_image_link_597():
    """
    Test case 597:  (part 2) Shortcut
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """![*foo* bar]

[*foo* bar]: /url "title"
"""
    expected_tokens = [
        "[ulist:-::2:]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


@pytest.mark.skip
def test_image_link_598():
    """
    Test case 598:  The link labels are case-insensitive:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """![[foo]]

[[foo]]: /url "title"
"""
    expected_tokens = [
        "[ulist:-::2:]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


@pytest.mark.skip
def test_image_link_599():
    """
    Test case 599:  If you just want a literal ! followed by bracketed text, you can backslash-escape the opening [:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """![Foo]

[foo]: /url "title"
"""
    expected_tokens = [
        "[ulist:-::2:]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


@pytest.mark.skip
def test_image_link_600():
    """
    Test case 600:  If you just want a literal ! followed by bracketed text, you can backslash-escape the opening [:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """!\\[foo]

[foo]: /url "title"
"""
    expected_tokens = [
        "[ulist:-::2:]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


@pytest.mark.skip
def test_image_link_601():
    """
    Test case 601:  If you want a link after a literal !, backslash-escape the !:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """\\![foo]

[foo]: /url "title"
"""
    expected_tokens = [
        "[ulist:-::2:]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
