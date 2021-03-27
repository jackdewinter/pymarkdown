"""
https://github.github.com/gfm/#images
"""
import pytest

from .utils import act_and_assert


@pytest.mark.gfm
def test_image_link_580x():
    """
    Test case 580:  (part 1) Syntax for images is like the syntax for links, with one difference
    """

    # Arrange
    source_markdown = """![foo](/url "title")"""
    expected_tokens = [
        "[para(1,1):]",
        '[image(1,1):inline:/url:title:foo::::foo:False:":: :]',
        "[end-para:::True]",
    ]
    expected_gfm = """<p><img src="/url" alt="foo" title="title" /></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_image_link_580a():
    """
    Test case 580a:  variation
    """

    # Arrange
    source_markdown = """![foo](/url 'title')"""
    expected_tokens = [
        "[para(1,1):]",
        "[image(1,1):inline:/url:title:foo::::foo:False:':: :]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><img src="/url" alt="foo" title="title" /></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_image_link_580b():
    """
    Test case 580a:  variation
    """

    # Arrange
    source_markdown = """![foo](/url (title))"""
    expected_tokens = [
        "[para(1,1):]",
        "[image(1,1):inline:/url:title:foo::::foo:False:(:: :]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><img src="/url" alt="foo" title="title" /></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_image_link_580c():
    """
    Test case 580c:  variation
    """

    # Arrange
    source_markdown = """![foo](</my url> (title))"""
    expected_tokens = [
        "[para(1,1):]",
        "[image(1,1):inline:/my%20url:title:foo:/my url:::foo:True:(:: :]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><img src="/my%20url" alt="foo" title="title" /></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_image_link_580d():
    """
    Test case 580d:  variation
    """

    # Arrange
    source_markdown = """![foo](</my url> (title & treaty))"""
    expected_tokens = [
        "[para(1,1):]",
        "[image(1,1):inline:/my%20url:title &amp; treaty:foo:/my url:title & treaty::foo:True:(:: :]",
        "[end-para:::True]",
    ]
    expected_gfm = (
        """<p><img src="/my%20url" alt="foo" title="title &amp; treaty" /></p>"""
    )

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_image_link_580e():
    """
    Test case 580:  (part 1) Syntax for images is like the syntax for links, with one difference
    """

    # Arrange
    source_markdown = """![foo](/url "title") abc"""
    expected_tokens = [
        "[para(1,1):]",
        '[image(1,1):inline:/url:title:foo::::foo:False:":: :]',
        "[text(1,21): abc:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><img src="/url" alt="foo" title="title" /> abc</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_image_link_581():
    """
    Test case 581:  (part 2) Syntax for images is like the syntax for links, with one difference
    """

    # Arrange
    source_markdown = """![foo *bar*]

[foo *bar*]: train.jpg "train & tracks"
"""
    expected_tokens = [
        "[para(1,1):]",
        "[image(1,1):shortcut:train.jpg:train &amp; tracks:foo bar::::foo *bar*:::::]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        '[link-ref-def(3,1):True::foo *bar*:: :train.jpg:: :train &amp; tracks:"train & tracks":]',
        "[BLANK(4,1):]",
    ]
    expected_gfm = (
        """<p><img src="train.jpg" alt="foo bar" title="train &amp; tracks" /></p>"""
    )

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_image_link_582():
    """
    Test case 582:  (part 3) Syntax for images is like the syntax for links, with one difference
    """

    # Arrange
    source_markdown = """![foo ![bar](/url)](/url2)"""
    expected_tokens = [
        "[para(1,1):]",
        "[image(1,1):inline:/url2::foo bar::::foo ![bar](/url):False::::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><img src="/url2" alt="foo bar" /></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_image_link_583():
    """
    Test case 583:  (part 4) Syntax for images is like the syntax for links, with one difference
    """

    # Arrange
    source_markdown = """![foo [bar](/url)](/url2)"""
    expected_tokens = [
        "[para(1,1):]",
        "[image(1,1):inline:/url2::foo bar::::foo [bar](/url):False::::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><img src="/url2" alt="foo bar" /></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_image_link_584():
    """
    Test case 584:  (part 1) Only the plain string content is rendered, without formatting.
    """

    # Arrange
    source_markdown = """![foo *bar*][]

[foo *bar*]: train.jpg "train & tracks"
"""
    expected_tokens = [
        "[para(1,1):]",
        "[image(1,1):collapsed:train.jpg:train &amp; tracks:foo bar::::foo *bar*:::::]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        '[link-ref-def(3,1):True::foo *bar*:: :train.jpg:: :train &amp; tracks:"train & tracks":]',
        "[BLANK(4,1):]",
    ]
    expected_gfm = (
        """<p><img src="train.jpg" alt="foo bar" title="train &amp; tracks" /></p>"""
    )

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_image_link_585():
    """
    Test case 585:  (part 2) Only the plain string content is rendered, without formatting.
    """

    # Arrange
    source_markdown = """![foo *bar*][foobar]

[FOOBAR]: train.jpg "train & tracks"
"""
    expected_tokens = [
        "[para(1,1):]",
        "[image(1,1):full:train.jpg:train &amp; tracks:foo bar:::foobar:foo *bar*:::::]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        '[link-ref-def(3,1):True::foobar:FOOBAR: :train.jpg:: :train &amp; tracks:"train & tracks":]',
        "[BLANK(4,1):]",
    ]
    expected_gfm = (
        """<p><img src="train.jpg" alt="foo bar" title="train &amp; tracks" /></p>"""
    )

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_image_link_586():
    """
    Test case 586:  (part 3) Only the plain string content is rendered, without formatting.
    """

    # Arrange
    source_markdown = """![foo](train.jpg)"""
    expected_tokens = [
        "[para(1,1):]",
        "[image(1,1):inline:train.jpg::foo::::foo:False::::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><img src="train.jpg" alt="foo" /></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_image_link_587():
    """
    Test case 587:  (part 4) Only the plain string content is rendered, without formatting.
    """

    # Arrange
    source_markdown = """My ![foo bar](/path/to/train.jpg  "title"   )"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):My :]",
        '[image(1,4):inline:/path/to/train.jpg:title:foo bar::::foo bar:False:"::  :   ]',
        "[end-para:::True]",
    ]
    expected_gfm = (
        """<p>My <img src="/path/to/train.jpg" alt="foo bar" title="title" /></p>"""
    )

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_image_link_588():
    """
    Test case 588:  (part 5) Only the plain string content is rendered, without formatting.
    """

    # Arrange
    source_markdown = """![foo](<url>)"""
    expected_tokens = [
        "[para(1,1):]",
        "[image(1,1):inline:url::foo::::foo:True::::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><img src="url" alt="foo" /></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_image_link_589():
    """
    Test case 589:  (part 6) Only the plain string content is rendered, without formatting.
    """

    # Arrange
    source_markdown = """![](/url)"""
    expected_tokens = [
        "[para(1,1):]",
        "[image(1,1):inline:/url:::::::False::::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><img src="/url" alt="" /></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_image_link_590():
    """
    Test case 590:  (part 1) Reference-style:
    """

    # Arrange
    source_markdown = """![foo][bar]

[bar]: /url"""
    expected_tokens = [
        "[para(1,1):]",
        "[image(1,1):full:/url::foo:::bar:foo:::::]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[link-ref-def(3,1):True::bar:: :/url:::::]",
    ]
    expected_gfm = """<p><img src="/url" alt="foo" /></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_image_link_591():
    """
    Test case 591:  (part 2) Reference-style:
    """

    # Arrange
    source_markdown = """![foo][bar]

[BAR]: /url"""
    expected_tokens = [
        "[para(1,1):]",
        "[image(1,1):full:/url::foo:::bar:foo:::::]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[link-ref-def(3,1):True::bar:BAR: :/url:::::]",
    ]
    expected_gfm = """<p><img src="/url" alt="foo" /></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_image_link_592():
    """
    Test case 592:  (part 1) Collapsed:
    """

    # Arrange
    source_markdown = """![foo][]

[foo]: /url "title"
"""
    expected_tokens = [
        "[para(1,1):]",
        "[image(1,1):collapsed:/url:title:foo::::foo:::::]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        '[link-ref-def(3,1):True::foo:: :/url:: :title:"title":]',
        "[BLANK(4,1):]",
    ]
    expected_gfm = """<p><img src="/url" alt="foo" title="title" /></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_image_link_592a():
    """
    Test case 592:  (part 1) Collapsed:
    """

    # Arrange
    source_markdown = """![foo][]\a

[foo]: /url "title"
""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[para(1,1):: ]",
        "[image(1,1):collapsed:/url:title:foo::::foo:::::]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        '[link-ref-def(3,1):True::foo:: :/url:: :title:"title":]',
        "[BLANK(4,1):]",
    ]
    expected_gfm = """<p><img src="/url" alt="foo" title="title" /></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_image_link_592b():
    """
    Test case 592:  (part 1) Collapsed:
    """

    # Arrange
    source_markdown = """![foo][]\atext

[foo]: /url "title"
""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[para(1,1):]",
        "[image(1,1):collapsed:/url:title:foo::::foo:::::]",
        "[text(1,9): text:]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        '[link-ref-def(3,1):True::foo:: :/url:: :title:"title":]',
        "[BLANK(4,1):]",
    ]
    expected_gfm = """<p><img src="/url" alt="foo" title="title" /> text</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_image_link_593():
    """
    Test case 593:  (part 2) Collapsed:
    """

    # Arrange
    source_markdown = """![*foo* bar][]

[*foo* bar]: /url "title"
"""
    expected_tokens = [
        "[para(1,1):]",
        "[image(1,1):collapsed:/url:title:foo bar::::*foo* bar:::::]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        '[link-ref-def(3,1):True::*foo* bar:: :/url:: :title:"title":]',
        "[BLANK(4,1):]",
    ]
    expected_gfm = """<p><img src="/url" alt="foo bar" title="title" /></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_image_link_594():
    """
    Test case 594:  The labels are case-insensitive:
    """

    # Arrange
    source_markdown = """![Foo][]

[foo]: /url "title"
"""
    expected_tokens = [
        "[para(1,1):]",
        "[image(1,1):collapsed:/url:title:Foo::::Foo:::::]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        '[link-ref-def(3,1):True::foo:: :/url:: :title:"title":]',
        "[BLANK(4,1):]",
    ]
    expected_gfm = """<p><img src="/url" alt="Foo" title="title" /></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_image_link_595():
    """
    Test case 595:  As with reference links, whitespace is not allowed between the two sets of brackets:
    """

    # Arrange
    source_markdown = """![foo]\a
[]

[foo]: /url "title"
""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[para(1,1):\n]",
        "[image(1,1):shortcut:/url:title:foo::::foo:::::]",
        "[text(1,7):\n:: \n]",
        "[text(2,1):[:]",
        "[text(2,2):]:]",
        "[end-para:::True]",
        "[BLANK(3,1):]",
        '[link-ref-def(4,1):True::foo:: :/url:: :title:"title":]',
        "[BLANK(5,1):]",
    ]
    expected_gfm = """<p><img src="/url" alt="foo" title="title" />
[]</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_image_link_596():
    """
    Test case 596:  (part 1) Shortcut
    """

    # Arrange
    source_markdown = """![foo]

[foo]: /url "title"
"""
    expected_tokens = [
        "[para(1,1):]",
        "[image(1,1):shortcut:/url:title:foo::::foo:::::]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        '[link-ref-def(3,1):True::foo:: :/url:: :title:"title":]',
        "[BLANK(4,1):]",
    ]
    expected_gfm = """<p><img src="/url" alt="foo" title="title" /></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_image_link_597():
    """
    Test case 597:  (part 2) Shortcut
    """

    # Arrange
    source_markdown = """![*foo* bar]

[*foo* bar]: /url "title"
"""
    expected_tokens = [
        "[para(1,1):]",
        "[image(1,1):shortcut:/url:title:foo bar::::*foo* bar:::::]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        '[link-ref-def(3,1):True::*foo* bar:: :/url:: :title:"title":]',
        "[BLANK(4,1):]",
    ]
    expected_gfm = """<p><img src="/url" alt="foo bar" title="title" /></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_image_link_598():
    """
    Test case 598:  The link labels are case-insensitive:
    """

    # Arrange
    source_markdown = """![[foo]]

[[foo]]: /url "title"
"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):![:]",
        "[text(1,3):[:]",
        "[text(1,4):foo:]",
        "[text(1,7):]:]",
        "[text(1,8):]:]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[para(3,1):]",
        "[text(3,1):[:]",
        "[text(3,2):[:]",
        "[text(3,3):foo:]",
        "[text(3,6):]:]",
        "[text(3,7):]:]",
        '[text(3,8):: /url \a"\a&quot;\atitle\a"\a&quot;\a:]',
        "[end-para:::True]",
        "[BLANK(4,1):]",
    ]
    expected_gfm = """<p>![[foo]]</p>
<p>[[foo]]: /url &quot;title&quot;</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_image_link_599():
    """
    Test case 599:  If you just want a literal ! followed by bracketed text, you can backslash-escape the opening [:
    """

    # Arrange
    source_markdown = """![Foo]

[foo]: /url "title"
"""
    expected_tokens = [
        "[para(1,1):]",
        "[image(1,1):shortcut:/url:title:Foo::::Foo:::::]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        '[link-ref-def(3,1):True::foo:: :/url:: :title:"title":]',
        "[BLANK(4,1):]",
    ]
    expected_gfm = """<p><img src="/url" alt="Foo" title="title" /></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_image_link_600():
    """
    Test case 600:  If you just want a literal ! followed by bracketed text, you can backslash-escape the opening [:
    """

    # Arrange
    source_markdown = """!\\[foo]

[foo]: /url "title"
"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):!\\\b[foo:]",
        "[text(1,7):]:]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        '[link-ref-def(3,1):True::foo:: :/url:: :title:"title":]',
        "[BLANK(4,1):]",
    ]
    expected_gfm = """<p>![foo]</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_image_link_601():
    """
    Test case 601:  If you want a link after a literal !, backslash-escape the !:
    """

    # Arrange
    source_markdown = """\\![foo]

[foo]: /url "title"
"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):\\\b!:]",
        "[link(1,3):shortcut:/url:title::::foo:::::]",
        "[text(1,4):foo:]",
        "[end-link::]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        '[link-ref-def(3,1):True::foo:: :/url:: :title:"title":]',
        "[BLANK(4,1):]",
    ]
    expected_gfm = """<p>!<a href="/url" title="title">foo</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)
