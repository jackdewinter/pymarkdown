"""
https://github.github.com/gfm/#images
"""
import pytest

from pymarkdown.tokenized_markdown import TokenizedMarkdown
from pymarkdown.transform_to_gfm import TransformToGfm

from .utils import assert_if_lists_different, assert_if_strings_different


@pytest.mark.gfm
def test_image_link_580():
    """
    Test case 580:  (part 1) Syntax for images is like the syntax for links, with one difference
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """![foo](/url "title")"""
    expected_tokens = ["[para(1,1):]", "[image:/url:title:foo]", "[end-para]"]
    expected_gfm = """<p><img src="/url" alt="foo" title="title" /></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_image_link_581():
    """
    Test case 581:  (part 2) Syntax for images is like the syntax for links, with one difference
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """![foo *bar*]

[foo *bar*]: train.jpg "train & tracks"
"""
    expected_tokens = [
        "[para(1,1):]",
        "[image:train.jpg:train &amp; tracks:foo bar]",
        "[end-para]",
        "[BLANK:]",
        '[link-ref-def(3,1):True::foo *bar*:: :train.jpg:: :train &amp; tracks:"train & tracks":]',
        "[BLANK:]",
    ]
    expected_gfm = (
        """<p><img src="train.jpg" alt="foo bar" title="train &amp; tracks" /></p>"""
    )

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_image_link_582():
    """
    Test case 582:  (part 3) Syntax for images is like the syntax for links, with one difference
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """![foo ![bar](/url)](/url2)"""
    expected_tokens = ["[para(1,1):]", "[image:/url2::foo bar]", "[end-para]"]
    expected_gfm = """<p><img src="/url2" alt="foo bar" /></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_image_link_583():
    """
    Test case 583:  (part 4) Syntax for images is like the syntax for links, with one difference
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """![foo [bar](/url)](/url2)"""
    expected_tokens = ["[para(1,1):]", "[image:/url2::foo bar]", "[end-para]"]
    expected_gfm = """<p><img src="/url2" alt="foo bar" /></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_image_link_584():
    """
    Test case 584:  (part 1) Only the plain string content is rendered, without formatting.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """![foo *bar*][]

[foo *bar*]: train.jpg "train & tracks"
"""
    expected_tokens = [
        "[para(1,1):]",
        "[image:train.jpg:train &amp; tracks:foo bar]",
        "[end-para]",
        "[BLANK:]",
        '[link-ref-def(3,1):True::foo *bar*:: :train.jpg:: :train &amp; tracks:"train & tracks":]',
        "[BLANK:]",
    ]
    expected_gfm = (
        """<p><img src="train.jpg" alt="foo bar" title="train &amp; tracks" /></p>"""
    )

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_image_link_585():
    """
    Test case 585:  (part 2) Only the plain string content is rendered, without formatting.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """![foo *bar*][foobar]

[FOOBAR]: train.jpg "train & tracks"
"""
    expected_tokens = [
        "[para(1,1):]",
        "[image:train.jpg:train &amp; tracks:foo bar]",
        "[end-para]",
        "[BLANK:]",
        '[link-ref-def(3,1):True::foobar:FOOBAR: :train.jpg:: :train &amp; tracks:"train & tracks":]',
        "[BLANK:]",
    ]
    expected_gfm = (
        """<p><img src="train.jpg" alt="foo bar" title="train &amp; tracks" /></p>"""
    )

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_image_link_586():
    """
    Test case 586:  (part 3) Only the plain string content is rendered, without formatting.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """![foo](train.jpg)"""
    expected_tokens = ["[para(1,1):]", "[image:train.jpg::foo]", "[end-para]"]
    expected_gfm = """<p><img src="train.jpg" alt="foo" /></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_image_link_587():
    """
    Test case 587:  (part 4) Only the plain string content is rendered, without formatting.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """My ![foo bar](/path/to/train.jpg  "title"   )"""
    expected_tokens = [
        "[para(1,1):]",
        "[text:My :]",
        "[image:/path/to/train.jpg:title:foo bar]",
        "[end-para]",
    ]
    expected_gfm = (
        """<p>My <img src="/path/to/train.jpg" alt="foo bar" title="title" /></p>"""
    )

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_image_link_588():
    """
    Test case 588:  (part 5) Only the plain string content is rendered, without formatting.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """![foo](<url>)"""
    expected_tokens = ["[para(1,1):]", "[image:url::foo]", "[end-para]"]
    expected_gfm = """<p><img src="url" alt="foo" /></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_image_link_589():
    """
    Test case 589:  (part 6) Only the plain string content is rendered, without formatting.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """![](/url)"""
    expected_tokens = ["[para(1,1):]", "[image:/url::]", "[end-para]"]
    expected_gfm = """<p><img src="/url" alt="" /></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_image_link_590():
    """
    Test case 590:  (part 1) Reference-style:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """![foo][bar]

[bar]: /url"""
    expected_tokens = [
        "[para(1,1):]",
        "[image:/url::foo]",
        "[end-para]",
        "[BLANK:]",
        "[link-ref-def(3,1):True::bar:: :/url:::::]",
    ]
    expected_gfm = """<p><img src="/url" alt="foo" /></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_image_link_591():
    """
    Test case 591:  (part 2) Reference-style:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """![foo][bar]

[BAR]: /url"""
    expected_tokens = [
        "[para(1,1):]",
        "[image:/url::foo]",
        "[end-para]",
        "[BLANK:]",
        "[link-ref-def(3,1):True::bar:BAR: :/url:::::]",
    ]
    expected_gfm = """<p><img src="/url" alt="foo" /></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_image_link_592():
    """
    Test case 592:  (part 1) Collapsed:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """![foo][]

[foo]: /url "title"
"""
    expected_tokens = [
        "[para(1,1):]",
        "[image:/url:title:foo]",
        "[end-para]",
        "[BLANK:]",
        '[link-ref-def(3,1):True::foo:: :/url:: :title:"title":]',
        "[BLANK:]",
    ]
    expected_gfm = """<p><img src="/url" alt="foo" title="title" /></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_image_link_593():
    """
    Test case 593:  (part 2) Collapsed:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """![*foo* bar][]

[*foo* bar]: /url "title"
"""
    expected_tokens = [
        "[para(1,1):]",
        "[image:/url:title:foo bar]",
        "[end-para]",
        "[BLANK:]",
        '[link-ref-def(3,1):True::*foo* bar:: :/url:: :title:"title":]',
        "[BLANK:]",
    ]
    expected_gfm = """<p><img src="/url" alt="foo bar" title="title" /></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_image_link_594():
    """
    Test case 594:  The labels are case-insensitive:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """![Foo][]

[foo]: /url "title"
"""
    expected_tokens = [
        "[para(1,1):]",
        "[image:/url:title:Foo]",
        "[end-para]",
        "[BLANK:]",
        '[link-ref-def(3,1):True::foo:: :/url:: :title:"title":]',
        "[BLANK:]",
    ]
    expected_gfm = """<p><img src="/url" alt="Foo" title="title" /></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_image_link_595():
    """
    Test case 595:  As with reference links, whitespace is not allowed between the two sets of brackets:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """![foo]\a
[]

[foo]: /url "title"
""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[para(1,1):\n]",
        "[image:/url:title:foo]",
        "[text:\n:: \n]",
        "[text:[:]",
        "[text:]:]",
        "[end-para]",
        "[BLANK:]",
        '[link-ref-def(4,1):True::foo:: :/url:: :title:"title":]',
        "[BLANK:]",
    ]
    expected_gfm = """<p><img src="/url" alt="foo" title="title" />
[]</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_image_link_596():
    """
    Test case 596:  (part 1) Shortcut
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """![foo]

[foo]: /url "title"
"""
    expected_tokens = [
        "[para(1,1):]",
        "[image:/url:title:foo]",
        "[end-para]",
        "[BLANK:]",
        '[link-ref-def(3,1):True::foo:: :/url:: :title:"title":]',
        "[BLANK:]",
    ]
    expected_gfm = """<p><img src="/url" alt="foo" title="title" /></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_image_link_597():
    """
    Test case 597:  (part 2) Shortcut
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """![*foo* bar]

[*foo* bar]: /url "title"
"""
    expected_tokens = [
        "[para(1,1):]",
        "[image:/url:title:foo bar]",
        "[end-para]",
        "[BLANK:]",
        '[link-ref-def(3,1):True::*foo* bar:: :/url:: :title:"title":]',
        "[BLANK:]",
    ]
    expected_gfm = """<p><img src="/url" alt="foo bar" title="title" /></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_image_link_598():
    """
    Test case 598:  The link labels are case-insensitive:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """![[foo]]

[[foo]]: /url "title"
"""
    expected_tokens = [
        "[para(1,1):]",
        "[text:![:]",
        "[text:[:]",
        "[text:foo:]",
        "[text:]:]",
        "[text:]:]",
        "[end-para]",
        "[BLANK:]",
        "[para(3,1):]",
        "[text:[:]",
        "[text:[:]",
        "[text:foo:]",
        "[text:]:]",
        "[text:]:]",
        "[text:: /url &quot;title&quot;:]",
        "[end-para]",
        "[BLANK:]",
    ]
    expected_gfm = """<p>![[foo]]</p>
<p>[[foo]]: /url &quot;title&quot;</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_image_link_599():
    """
    Test case 599:  If you just want a literal ! followed by bracketed text, you can backslash-escape the opening [:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """![Foo]

[foo]: /url "title"
"""
    expected_tokens = [
        "[para(1,1):]",
        "[image:/url:title:Foo]",
        "[end-para]",
        "[BLANK:]",
        '[link-ref-def(3,1):True::foo:: :/url:: :title:"title":]',
        "[BLANK:]",
    ]
    expected_gfm = """<p><img src="/url" alt="Foo" title="title" /></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_image_link_600():
    """
    Test case 600:  If you just want a literal ! followed by bracketed text, you can backslash-escape the opening [:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """!\\[foo]

[foo]: /url "title"
"""
    expected_tokens = [
        "[para(1,1):]",
        "[text:![foo:]",
        "[text:]:]",
        "[end-para]",
        "[BLANK:]",
        '[link-ref-def(3,1):True::foo:: :/url:: :title:"title":]',
        "[BLANK:]",
    ]
    expected_gfm = """<p>![foo]</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_image_link_601():
    """
    Test case 601:  If you want a link after a literal !, backslash-escape the !:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """\\![foo]

[foo]: /url "title"
"""
    expected_tokens = [
        "[para(1,1):]",
        "[text:!:]",
        "[link:/url:title]",
        "[text:foo:]",
        "[end-link::]",
        "[end-para]",
        "[BLANK:]",
        '[link-ref-def(3,1):True::foo:: :/url:: :title:"title":]',
        "[BLANK:]",
    ]
    expected_gfm = """<p>!<a href="/url" title="title">foo</a></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
