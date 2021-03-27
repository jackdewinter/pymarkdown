"""
https://github.github.com/gfm/#paragraph
"""
import pytest

from .utils import act_and_assert

# pylint: disable=too-many-lines


@pytest.mark.gfm
def test_paragraph_extra_43a():
    """
    Test case extra 43a:  Paragraph with code span with newline inside
    """

    # Arrange
    source_markdown = """a`code&#xa;span`a"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        "[icode-span(1,2):code\a&\a&amp;\a#xa;span:`::]",
        "[text(1,17):a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<code>code&amp;#xa;span</code>a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_43b():
    """
    Test case extra 43b:  Paragraph with code span with newline inside
    """

    # Arrange
    source_markdown = """a`code &#xa; span`a"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        "[icode-span(1,2):code \a&\a&amp;\a#xa; span:`::]",
        "[text(1,19):a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<code>code &amp;#xa; span</code>a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_44a():
    """
    Test case extra 44a:  Paragraph with raw HTML with newline inside
    """

    # Arrange
    source_markdown = """a<raw&#xa;html='cool'>a"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a\a<\a&lt;\araw\a&#xa;\a\n\ahtml='cool'\a>\a&gt;\aa:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a&lt;raw\nhtml='cool'&gt;a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_44b():
    """
    Test case extra 44b:  Paragraph with raw HTML with newline inside
    """

    # Arrange
    source_markdown = """a<raw &#xa; html='cool'>a"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a\a<\a&lt;\araw \a&#xa;\a\n\a html='cool'\a>\a&gt;\aa:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a&lt;raw \n html='cool'&gt;a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_44c():
    """
    Test case extra 44c:  Paragraph with raw HTML with newline inside
    """

    # Arrange
    source_markdown = """a<raw html='cool &#xa; man'>a"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        "[raw-html(1,2):raw html='cool &#xa; man']",
        "[text(1,29):a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<raw html='cool &#xa; man'>a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_45a():
    """
    Test case extra 45a:  Paragraph with URI autolink with newline inside, renders invalid
    """

    # Arrange
    source_markdown = """a<http://www.&#xa;google.com>a"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        "[uri-autolink(1,2):http://www.&#xa;google.com]",
        "[text(1,30):a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<a href="http://www.&amp;#xa;google.com">http://www.&amp;#xa;google.com</a>a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_46a():
    """
    Test case extra 46a:  Paragraph with email autolink with newline inside, renders invalid
    """

    # Arrange
    source_markdown = """a<foo@bar&#xa;.com>a"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a\a<\a&lt;\afoo@bar\a&#xa;\a\n\a.com\a>\a&gt;\aa:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a&lt;foo@bar\n.com&gt;a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_46c():
    """
    Test case extra 46c:  Paragraph with email autolink with newline inside, renders invalid
    """

    # Arrange
    source_markdown = """a*foo&#xa;bar*a"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        "[emphasis(1,2):1:*]",
        "[text(1,3):foo\a&#xa;\a\n\abar:]",
        "[end-emphasis(1,14)::]",
        "[text(1,15):a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<em>foo\nbar</em>a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_47():
    """
    Test case extra 47:  Paragraph with inline link with newline in label
    """

    # Arrange
    source_markdown = """a[Fo
o](/uri "testing")a"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):a:]",
        '[link(1,2):inline:/uri:testing::::Fo\no:False:":: :]',
        "[text(1,3):Fo\no::\n]",
        "[end-link::]",
        "[text(2,19):a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<a href="/uri" title="testing">Fo\no</a>a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_47a():
    """
    Test case extra 47:  Paragraph with inline link with newline in label
    """

    # Arrange
    source_markdown = """a[Fo
o](/uri "testing")"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):a:]",
        '[link(1,2):inline:/uri:testing::::Fo\no:False:":: :]',
        "[text(1,3):Fo\no::\n]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<a href="/uri" title="testing">Fo\no</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_48x():
    """
    Test case extra 48:  Paragraph with inline link with newline in pre-URI space
    """

    # Arrange
    source_markdown = """a[Foo](
/uri "testing")a"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):a:]",
        '[link(1,2):inline:/uri:testing::::Foo:False:":\n: :]',
        "[text(1,3):Foo:]",
        "[end-link::]",
        "[text(2,16):a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<a href="/uri" title="testing">Foo</a>a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_48a():
    """
    Test case extra 48a:  48 with whitespace before newline
    """

    # Arrange
    source_markdown = """a[Foo](\a\a
/uri "testing")a""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):a:]",
        '[link(1,2):inline:/uri:testing::::Foo:False:":  \n: :]',
        "[text(1,3):Foo:]",
        "[end-link::]",
        "[text(2,16):a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<a href="/uri" title="testing">Foo</a>a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_48b():
    """
    Test case extra 48b:  48 with whitespace after newline
    """

    # Arrange
    source_markdown = """a[Foo](
   /uri "testing")a"""
    expected_tokens = [
        "[para(1,1):\n   ]",
        "[text(1,1):a:]",
        '[link(1,2):inline:/uri:testing::::Foo:False:":\n: :]',
        "[text(1,3):Foo:]",
        "[end-link::]",
        "[text(2,19):a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<a href="/uri" title="testing">Foo</a>a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_48ba():
    """
    Test case extra 48ba:  48 with whitespace after newline
    """

    # Arrange
    source_markdown = """a[Foo](
   /uri "testing")"""
    expected_tokens = [
        "[para(1,1):\n   ]",
        "[text(1,1):a:]",
        '[link(1,2):inline:/uri:testing::::Foo:False:":\n: :]',
        "[text(1,3):Foo:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<a href="/uri" title="testing">Foo</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_48c():
    """
    Test case extra 48c:  48 with whitespace before and after newline
    """

    # Arrange
    source_markdown = """a[Foo](\a\a
   /uri "testing")a""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[para(1,1):\n   ]",
        "[text(1,1):a:]",
        '[link(1,2):inline:/uri:testing::::Foo:False:":  \n: :]',
        "[text(1,3):Foo:]",
        "[end-link::]",
        "[text(2,19):a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<a href="/uri" title="testing">Foo</a>a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_48ca():
    """
    Test case extra 48ca:  48 with whitespace before and after newline
    """

    # Arrange
    source_markdown = """a[Foo](\a\a
   /uri "testing")""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[para(1,1):\n   ]",
        "[text(1,1):a:]",
        '[link(1,2):inline:/uri:testing::::Foo:False:":  \n: :]',
        "[text(1,3):Foo:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<a href="/uri" title="testing">Foo</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_48d():
    """
    Test case extra 48d:  Paragraph with inline link with newline in pre-URI space
    """

    # Arrange
    source_markdown = """a[Foo](
/uri "testing")"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):a:]",
        '[link(1,2):inline:/uri:testing::::Foo:False:":\n: :]',
        "[text(1,3):Foo:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<a href="/uri" title="testing">Foo</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_49():
    """
    Test case extra 49:  Paragraph with inline link with newline in URI, invalidating it
    """

    # Arrange
    source_markdown = """a[Foo](/ur
i "testing")a"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):a:]",
        "[text(1,2):[:]",
        "[text(1,3):Foo:]",
        "[text(1,6):]:]",
        '[text(1,7):(/ur\ni \a"\a&quot;\atesting\a"\a&quot;\a)a::\n]',
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a[Foo](/ur\ni &quot;testing&quot;)a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_49a():
    """
    Test case extra 49a:  Paragraph with inline link with newline in URI, invalidating it
    """

    # Arrange
    source_markdown = """a[Foo](/ur
i "testing")"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):a:]",
        "[text(1,2):[:]",
        "[text(1,3):Foo:]",
        "[text(1,6):]:]",
        '[text(1,7):(/ur\ni \a"\a&quot;\atesting\a"\a&quot;\a)::\n]',
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a[Foo](/ur\ni &quot;testing&quot;)</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_50x():
    """
    Test case extra 50:  Paragraph with inline link with newline in post-URI space
    """

    # Arrange
    source_markdown = """a[Foo](/uri\a
"testing")a""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):a:]",
        '[link(1,2):inline:/uri:testing::::Foo:False:":: \n:]',
        "[text(1,3):Foo:]",
        "[end-link::]",
        "[text(2,11):a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<a href="/uri" title="testing">Foo</a>a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_50a():
    """
    Test case extra 50:  50 with whitespace before newline
    """

    # Arrange
    source_markdown = """a[Foo](/uri\a\a
"testing")a""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):a:]",
        '[link(1,2):inline:/uri:testing::::Foo:False:"::  \n:]',
        "[text(1,3):Foo:]",
        "[end-link::]",
        "[text(2,11):a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<a href="/uri" title="testing">Foo</a>a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_50b():
    """
    Test case extra 50:  50 with whitespace after newline
    """

    # Arrange
    source_markdown = """a[Foo](/uri
   "testing")a"""
    expected_tokens = [
        "[para(1,1):\n   ]",
        "[text(1,1):a:]",
        '[link(1,2):inline:/uri:testing::::Foo:False:"::\n:]',
        "[text(1,3):Foo:]",
        "[end-link::]",
        "[text(2,14):a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<a href="/uri" title="testing">Foo</a>a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_50ba():
    """
    Test case extra 50a:  50 with whitespace after newline
    """

    # Arrange
    source_markdown = """a[Foo](/uri
   "testing")"""
    expected_tokens = [
        "[para(1,1):\n   ]",
        "[text(1,1):a:]",
        '[link(1,2):inline:/uri:testing::::Foo:False:"::\n:]',
        "[text(1,3):Foo:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<a href="/uri" title="testing">Foo</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_50c():
    """
    Test case extra 50c:  50 with whitespace before and after newline
    """

    # Arrange
    source_markdown = """a[Foo](/uri\a\a
   "testing")a""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[para(1,1):\n   ]",
        "[text(1,1):a:]",
        '[link(1,2):inline:/uri:testing::::Foo:False:"::  \n:]',
        "[text(1,3):Foo:]",
        "[end-link::]",
        "[text(2,14):a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<a href="/uri" title="testing">Foo</a>a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_50ca():
    """
    Test case extra 50ca:  50 with whitespace before and after newline
    """

    # Arrange
    source_markdown = """a[Foo](/uri\a\a
   "testing")""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[para(1,1):\n   ]",
        "[text(1,1):a:]",
        '[link(1,2):inline:/uri:testing::::Foo:False:"::  \n:]',
        "[text(1,3):Foo:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<a href="/uri" title="testing">Foo</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_50d():
    """
    Test case extra 50d:  Paragraph with inline link with newline in post-URI space
    """

    # Arrange
    source_markdown = """a[Foo](/uri\a
"testing")""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):a:]",
        '[link(1,2):inline:/uri:testing::::Foo:False:":: \n:]',
        "[text(1,3):Foo:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<a href="/uri" title="testing">Foo</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_51():
    """
    Test case extra 51:  Paragraph with inline link with newline in title
    """

    # Arrange
    source_markdown = """a[Foo](/uri "test
ing")a"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):a:]",
        '[link(1,2):inline:/uri:test\ning::::Foo:False:":: :]',
        "[text(1,3):Foo:]",
        "[end-link::]",
        "[text(2,6):a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<a href="/uri" title="test\ning">Foo</a>a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_51a():
    """
    Test case extra 51a:  Paragraph with inline link with newline in title
    """

    # Arrange
    source_markdown = """a[Foo](</uri> "test
ing")a"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):a:]",
        '[link(1,2):inline:/uri:test\ning::::Foo:True:":: :]',
        "[text(1,3):Foo:]",
        "[end-link::]",
        "[text(2,6):a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<a href="/uri" title="test\ning">Foo</a>a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_51aa():
    """
    Test case extra 51aa:  Paragraph with inline link with newline in title
    """

    # Arrange
    source_markdown = """a[Foo](</uri> "test
ing")"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):a:]",
        '[link(1,2):inline:/uri:test\ning::::Foo:True:":: :]',
        "[text(1,3):Foo:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<a href="/uri" title="test\ning">Foo</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_51b():
    """
    Test case extra 51b:  Paragraph with inline link with newline in title
    """

    # Arrange
    source_markdown = """a[Foo](</uri> "te\\\\st
ing")a"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):a:]",
        '[link(1,2):inline:/uri:te\\st\ning::te\\\\st\ning::Foo:True:":: :]',
        "[text(1,3):Foo:]",
        "[end-link::]",
        "[text(2,6):a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<a href="/uri" title="te\\st\ning">Foo</a>a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_51ba():
    """
    Test case extra 51ba:  Paragraph with inline link with newline in title
    """

    # Arrange
    source_markdown = """a[Foo](</uri> "te\\\\st
ing")"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):a:]",
        '[link(1,2):inline:/uri:te\\st\ning::te\\\\st\ning::Foo:True:":: :]',
        "[text(1,3):Foo:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<a href="/uri" title="te\\st\ning">Foo</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_51c():
    """
    Test case extra 51c:  Paragraph with inline link with newline in title
    """

    # Arrange
    source_markdown = """a[Foo](/uri "test
ing")"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):a:]",
        '[link(1,2):inline:/uri:test\ning::::Foo:False:":: :]',
        "[text(1,3):Foo:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<a href="/uri" title="test\ning">Foo</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_52x():
    """
    Test case extra 52:  Paragraph with inline link with newline after title
    """

    # Arrange
    source_markdown = """a[Foo](/uri "testing"
)a"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):a:]",
        '[link(1,2):inline:/uri:testing::::Foo:False:":: :\n]',
        "[text(1,3):Foo:]",
        "[end-link::]",
        "[text(2,2):a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<a href="/uri" title="testing">Foo</a>a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_52a():
    """
    Test case extra 52:  52 with whitespace before newline
    """

    # Arrange
    source_markdown = """a[Foo](/uri "testing"\a\a
)a""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):a:]",
        '[link(1,2):inline:/uri:testing::::Foo:False:":: :  \n]',
        "[text(1,3):Foo:]",
        "[end-link::]",
        "[text(2,2):a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<a href="/uri" title="testing">Foo</a>a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_52aa():
    """
    Test case extra 52:  52 with whitespace before newline
    """

    # Arrange
    source_markdown = """a[Foo](/uri "testing"\a\a
)""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):a:]",
        '[link(1,2):inline:/uri:testing::::Foo:False:":: :  \n]',
        "[text(1,3):Foo:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<a href="/uri" title="testing">Foo</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_52b():
    """
    Test case extra 52b:  52 with whitespace after newline
    """

    # Arrange
    source_markdown = """a[Foo](/uri "testing"
  )a"""
    expected_tokens = [
        "[para(1,1):\n  ]",
        "[text(1,1):a:]",
        '[link(1,2):inline:/uri:testing::::Foo:False:":: :\n]',
        "[text(1,3):Foo:]",
        "[end-link::]",
        "[text(2,4):a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<a href="/uri" title="testing">Foo</a>a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_52ba():
    """
    Test case extra 52ba:  52 with whitespace after newline
    """

    # Arrange
    source_markdown = """a[Foo](/uri "testing"
  )"""
    expected_tokens = [
        "[para(1,1):\n  ]",
        "[text(1,1):a:]",
        '[link(1,2):inline:/uri:testing::::Foo:False:":: :\n]',
        "[text(1,3):Foo:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<a href="/uri" title="testing">Foo</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_52c():
    """
    Test case extra 52c:  52 with whitespace before and after newline
    """

    # Arrange
    source_markdown = """a[Foo](/uri "testing"\a\a
  )a""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[para(1,1):\n  ]",
        "[text(1,1):a:]",
        '[link(1,2):inline:/uri:testing::::Foo:False:":: :  \n]',
        "[text(1,3):Foo:]",
        "[end-link::]",
        "[text(2,4):a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<a href="/uri" title="testing">Foo</a>a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_52ca():
    """
    Test case extra 52ca:  52 with whitespace before and after newline
    """

    # Arrange
    source_markdown = """a[Foo](/uri "testing"\a\a
  )""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[para(1,1):\n  ]",
        "[text(1,1):a:]",
        '[link(1,2):inline:/uri:testing::::Foo:False:":: :  \n]',
        "[text(1,3):Foo:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<a href="/uri" title="testing">Foo</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_52d():
    """
    Test case extra 52d:  Paragraph with inline link with newline after title
    """

    # Arrange
    source_markdown = """a[Foo](/uri "testing"
)"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):a:]",
        '[link(1,2):inline:/uri:testing::::Foo:False:":: :\n]',
        "[text(1,3):Foo:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<a href="/uri" title="testing">Foo</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_53():
    """
    Test case extra 53:  Paragraph with full link with newline in label
    """

    # Arrange
    source_markdown = """[bar]: /url 'title'
    
a[foo
bar][bar]a"""
    expected_tokens = [
        "[link-ref-def(1,1):True::bar:: :/url:: :title:'title':]",
        "[BLANK(2,1):    ]",
        "[para(3,1):\n]",
        "[text(3,1):a:]",
        "[link(3,2):full:/url:title:::bar:foo\nbar:::::]",
        "[text(3,3):foo\nbar::\n]",
        "[end-link::]",
        "[text(4,10):a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<a href="/url" title="title">foo\nbar</a>a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_53a():
    """
    Test case extra 53a:  Paragraph with full link with newline in label
    """

    # Arrange
    source_markdown = """[bar]: /url 'title'
    
a![foo
bar][bar]a"""
    expected_tokens = [
        "[link-ref-def(1,1):True::bar:: :/url:: :title:'title':]",
        "[BLANK(2,1):    ]",
        "[para(3,1):\n]",
        "[text(3,1):a:]",
        "[image(3,2):full:/url:title:foo\nbar:::bar:foo\nbar:::::]",
        "[text(4,10):a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<img src="/url" alt="foo\nbar" title="title" />a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_53aa():
    """
    Test case extra 53aa:  Paragraph with full link with newline in label
    """

    # Arrange
    source_markdown = """[bar]: /url 'title'

a![foo
bar][bar]"""
    expected_tokens = [
        "[link-ref-def(1,1):True::bar:: :/url:: :title:'title':]",
        "[BLANK(2,1):]",
        "[para(3,1):\n]",
        "[text(3,1):a:]",
        "[image(3,2):full:/url:title:foo\nbar:::bar:foo\nbar:::::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<img src="/url" alt="foo\nbar" title="title" /></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_53b():
    """
    Test case extra 53b:  Paragraph with full link with newline in label
    """

    # Arrange
    source_markdown = """[bar]: /url 'title'
    
a[foo&#xa;bar][bar]a"""
    expected_tokens = [
        "[link-ref-def(1,1):True::bar:: :/url:: :title:'title':]",
        "[BLANK(2,1):    ]",
        "[para(3,1):]",
        "[text(3,1):a:]",
        "[link(3,2):full:/url:title:::bar:foo&#xa;bar:::::]",
        "[text(3,3):foo\a&#xa;\a\n\abar:]",
        "[end-link::]",
        "[text(3,20):a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<a href="/url" title="title">foo\nbar</a>a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_53c():
    """
    Test case extra 53c:  Paragraph with full link with newline in label
    """

    # Arrange
    source_markdown = """[bar]: /url 'title'
    
a![foo&#xa;bar][bar]a"""
    expected_tokens = [
        "[link-ref-def(1,1):True::bar:: :/url:: :title:'title':]",
        "[BLANK(2,1):    ]",
        "[para(3,1):]",
        "[text(3,1):a:]",
        "[image(3,2):full:/url:title:foo\nbar:::bar:foo&#xa;bar:::::]",
        "[text(3,21):a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<img src="/url" alt="foo\nbar" title="title" />a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_53d():
    """
    Test case extra 53d:  Paragraph with full link with newline in label
    """

    # Arrange
    source_markdown = """[bar]: /url 'title'
    
a[foo
bar][bar]"""
    expected_tokens = [
        "[link-ref-def(1,1):True::bar:: :/url:: :title:'title':]",
        "[BLANK(2,1):    ]",
        "[para(3,1):\n]",
        "[text(3,1):a:]",
        "[link(3,2):full:/url:title:::bar:foo\nbar:::::]",
        "[text(3,3):foo\nbar::\n]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<a href="/url" title="title">foo\nbar</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_54():
    """
    Test case extra 54:  Paragraph with full link with newline in reference
    """

    # Arrange
    source_markdown = """[ba\nr]: /url 'title'
    
a[foo][ba
r]a"""
    expected_tokens = [
        "[link-ref-def(1,1):True::ba r:ba\nr: :/url:: :title:'title':]",
        "[BLANK(3,1):    ]",
        "[para(4,1):\n]",
        "[text(4,1):a:]",
        "[link(4,2):full:/url:title:::ba\nr:foo:::::]",
        "[text(4,3):foo:]",
        "[end-link::]",
        "[text(5,3):a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<a href="/url" title="title">foo</a>a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_54a():
    """
    Test case extra 54a:  Paragraph with full link with newline in reference
    """

    # Arrange
    source_markdown = """[ba\nr]: /url 'title'

a![foo][ba
r]a"""
    expected_tokens = [
        "[link-ref-def(1,1):True::ba r:ba\nr: :/url:: :title:'title':]",
        "[BLANK(3,1):]",
        "[para(4,1):\n]",
        "[text(4,1):a:]",
        "[image(4,2):full:/url:title:foo:::ba\nr:foo:::::]",
        "[text(5,3):a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<img src="/url" alt="foo" title="title" />a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_54aa():
    """
    Test case extra 54aa:  Paragraph with full link with newline in reference
    """

    # Arrange
    source_markdown = """[ba\nr]: /url 'title'

a![foo][ba
r]"""
    expected_tokens = [
        "[link-ref-def(1,1):True::ba r:ba\nr: :/url:: :title:'title':]",
        "[BLANK(3,1):]",
        "[para(4,1):\n]",
        "[text(4,1):a:]",
        "[image(4,2):full:/url:title:foo:::ba\nr:foo:::::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<img src="/url" alt="foo" title="title" /></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_54b():
    """
    Test case extra 54b:  Paragraph with full link with newline in reference
    """

    # Arrange
    source_markdown = """[ba&#xa;r]: /url 'title'

a[foo][ba&#xa;r]a"""
    expected_tokens = [
        "[link-ref-def(1,1):True::ba&#xa;r:: :/url:: :title:'title':]",
        "[BLANK(2,1):]",
        "[para(3,1):]",
        "[text(3,1):a:]",
        "[link(3,2):full:/url:title:::ba&#xa;r:foo:::::]",
        "[text(3,3):foo:]",
        "[end-link::]",
        "[text(3,17):a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<a href="/url" title="title">foo</a>a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_54c():
    """
    Test case extra 54c:  Paragraph with full link with newline in reference
    """

    # Arrange
    source_markdown = """[ba&#xa;r]: /url 'title'

a![foo][ba&#xa;r]a"""
    expected_tokens = [
        "[link-ref-def(1,1):True::ba&#xa;r:: :/url:: :title:'title':]",
        "[BLANK(2,1):]",
        "[para(3,1):]",
        "[text(3,1):a:]",
        "[image(3,2):full:/url:title:foo:::ba&#xa;r:foo:::::]",
        "[text(3,18):a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<img src="/url" alt="foo" title="title" />a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_54d():
    """
    Test case extra 54d:  Paragraph with full link with newline in reference
    """

    # Arrange
    source_markdown = """[ba\nr]: /url 'title'

a[foo][ba
r]"""
    expected_tokens = [
        "[link-ref-def(1,1):True::ba r:ba\nr: :/url:: :title:'title':]",
        "[BLANK(3,1):]",
        "[para(4,1):\n]",
        "[text(4,1):a:]",
        "[link(4,2):full:/url:title:::ba\nr:foo:::::]",
        "[text(4,3):foo:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<a href="/url" title="title">foo</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_55():
    """
    Test case extra 55:  Paragraph with shortcut link with newline in label
    """

    # Arrange
    source_markdown = """[ba\nr]: /url 'title'
    
a[ba
r]a"""
    expected_tokens = [
        "[link-ref-def(1,1):True::ba r:ba\nr: :/url:: :title:'title':]",
        "[BLANK(3,1):    ]",
        "[para(4,1):\n]",
        "[text(4,1):a:]",
        "[link(4,2):shortcut:/url:title::::ba\nr:::::]",
        "[text(4,3):ba\nr::\n]",
        "[end-link::]",
        "[text(5,3):a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<a href="/url" title="title">ba\nr</a>a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_55a():
    """
    Test case extra 55a:  Paragraph with shortcut link with newline in label
    """

    # Arrange
    source_markdown = """[ba\nr]: /url 'title'
    
a![ba
r]a"""
    expected_tokens = [
        "[link-ref-def(1,1):True::ba r:ba\nr: :/url:: :title:'title':]",
        "[BLANK(3,1):    ]",
        "[para(4,1):\n]",
        "[text(4,1):a:]",
        "[image(4,2):shortcut:/url:title:ba\nr::::ba\nr:::::]",
        "[text(5,3):a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<img src="/url" alt="ba\nr" title="title" />a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_55aa():
    """
    Test case extra 55aa:  Paragraph with shortcut link with newline in label
    """

    # Arrange
    source_markdown = """[ba\nr]: /url 'title'
    
a![ba
r]"""
    expected_tokens = [
        "[link-ref-def(1,1):True::ba r:ba\nr: :/url:: :title:'title':]",
        "[BLANK(3,1):    ]",
        "[para(4,1):\n]",
        "[text(4,1):a:]",
        "[image(4,2):shortcut:/url:title:ba\nr::::ba\nr:::::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<img src="/url" alt="ba\nr" title="title" /></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_55b():
    """
    Test case extra 55b:  Paragraph with shortcut link with newline in label
    """

    # Arrange
    source_markdown = """[ba&#xa;r]: /url 'title'
    
a[ba&#xa;r]a"""
    expected_tokens = [
        "[link-ref-def(1,1):True::ba&#xa;r:: :/url:: :title:'title':]",
        "[BLANK(2,1):    ]",
        "[para(3,1):]",
        "[text(3,1):a:]",
        "[link(3,2):shortcut:/url:title::::ba&#xa;r:::::]",
        "[text(3,3):ba\a&#xa;\a\n\ar:]",
        "[end-link::]",
        "[text(3,12):a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<a href="/url" title="title">ba\nr</a>a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_55c():
    """
    Test case extra 55c:  Paragraph with shortcut link with newline in label
    """

    # Arrange
    source_markdown = """[ba&#xa;r]: /url 'title'
    
a![ba&#xa;r]a"""
    expected_tokens = [
        "[link-ref-def(1,1):True::ba&#xa;r:: :/url:: :title:'title':]",
        "[BLANK(2,1):    ]",
        "[para(3,1):]",
        "[text(3,1):a:]",
        "[image(3,2):shortcut:/url:title:ba\nr::::ba&#xa;r:::::]",
        "[text(3,13):a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<img src="/url" alt="ba\nr" title="title" />a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_55d():
    """
    Test case extra 55d:  Paragraph with shortcut link with newline in label
    """

    # Arrange
    source_markdown = """[ba\nr]: /url 'title'
    
a[ba
r]"""
    expected_tokens = [
        "[link-ref-def(1,1):True::ba r:ba\nr: :/url:: :title:'title':]",
        "[BLANK(3,1):    ]",
        "[para(4,1):\n]",
        "[text(4,1):a:]",
        "[link(4,2):shortcut:/url:title::::ba\nr:::::]",
        "[text(4,3):ba\nr::\n]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<a href="/url" title="title">ba\nr</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_56():
    """
    Test case extra 56:  Paragraph with collapsed link with newline in label
    """

    # Arrange
    source_markdown = """[ba\nr]: /url 'title'
    
a[ba
r][]a"""
    expected_tokens = [
        "[link-ref-def(1,1):True::ba r:ba\nr: :/url:: :title:'title':]",
        "[BLANK(3,1):    ]",
        "[para(4,1):\n]",
        "[text(4,1):a:]",
        "[link(4,2):collapsed:/url:title::::ba\nr:::::]",
        "[text(4,3):ba\nr::\n]",
        "[end-link::]",
        "[text(5,5):a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<a href="/url" title="title">ba\nr</a>a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_56a():
    """
    Test case extra 56a:  Paragraph with collapsed link with newline in label
    """

    # Arrange
    source_markdown = """[ba\nr]: /url 'title'
    
a![ba
r][]a"""
    expected_tokens = [
        "[link-ref-def(1,1):True::ba r:ba\nr: :/url:: :title:'title':]",
        "[BLANK(3,1):    ]",
        "[para(4,1):\n]",
        "[text(4,1):a:]",
        "[image(4,2):collapsed:/url:title:ba\nr::::ba\nr:::::]",
        "[text(5,5):a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<img src="/url" alt="ba\nr" title="title" />a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_56aa():
    """
    Test case extra 56aa:  Paragraph with collapsed link with newline in label
    """

    # Arrange
    source_markdown = """[ba\nr]: /url 'title'
    
a![ba
r][]"""
    expected_tokens = [
        "[link-ref-def(1,1):True::ba r:ba\nr: :/url:: :title:'title':]",
        "[BLANK(3,1):    ]",
        "[para(4,1):\n]",
        "[text(4,1):a:]",
        "[image(4,2):collapsed:/url:title:ba\nr::::ba\nr:::::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<img src="/url" alt="ba\nr" title="title" /></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_56b():
    """
    Test case extra 56a:  Paragraph with collapsed link with newline in label
    """

    # Arrange
    source_markdown = """[ba&#xa;r]: /url 'title'
    
a[ba&#xa;r][]a"""
    expected_tokens = [
        "[link-ref-def(1,1):True::ba&#xa;r:: :/url:: :title:'title':]",
        "[BLANK(2,1):    ]",
        "[para(3,1):]",
        "[text(3,1):a:]",
        "[link(3,2):collapsed:/url:title::::ba&#xa;r:::::]",
        "[text(3,3):ba\a&#xa;\a\n\ar:]",
        "[end-link::]",
        "[text(3,14):a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<a href="/url" title="title">ba\nr</a>a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_56c():
    """
    Test case extra 56c:  Paragraph with collapsed link with newline in label
    """

    # Arrange
    source_markdown = """[ba&#xa;r]: /url 'title'
    
a![ba&#xa;r][]a"""
    expected_tokens = [
        "[link-ref-def(1,1):True::ba&#xa;r:: :/url:: :title:'title':]",
        "[BLANK(2,1):    ]",
        "[para(3,1):]",
        "[text(3,1):a:]",
        "[image(3,2):collapsed:/url:title:ba\nr::::ba&#xa;r:::::]",
        "[text(3,15):a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<img src="/url" alt="ba\nr" title="title" />a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_56d():
    """
    Test case extra 56d:  Paragraph with collapsed link with newline in label
    """

    # Arrange
    source_markdown = """[ba\nr]: /url 'title'

a[ba
r][]a"""
    expected_tokens = [
        "[link-ref-def(1,1):True::ba r:ba\nr: :/url:: :title:'title':]",
        "[BLANK(3,1):]",
        "[para(4,1):\n]",
        "[text(4,1):a:]",
        "[link(4,2):collapsed:/url:title::::ba\nr:::::]",
        "[text(4,3):ba\nr::\n]",
        "[end-link::]",
        "[text(5,5):a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<a href="/url" title="title">ba\nr</a>a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_57():
    """
    Test case extra 57:  Paragraph with collapsed link with newline in label
    """

    # Arrange
    source_markdown = """[\nbar]: /url 'title'
    
a[
bar][]a"""
    expected_tokens = [
        "[link-ref-def(1,1):True::bar:\nbar: :/url:: :title:'title':]",
        "[BLANK(3,1):    ]",
        "[para(4,1):\n]",
        "[text(4,1):a:]",
        "[link(4,2):collapsed:/url:title::::\nbar:::::]",
        "[text(4,3):\nbar::\n]",
        "[end-link::]",
        "[text(5,7):a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<a href="/url" title="title">\nbar</a>a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_57a():
    """
    Test case extra 57a:  Paragraph with collapsed link with newline in label
    """

    # Arrange
    source_markdown = """[\nbar]: /url 'title'

a![
bar][]a"""
    expected_tokens = [
        "[link-ref-def(1,1):True::bar:\nbar: :/url:: :title:'title':]",
        "[BLANK(3,1):]",
        "[para(4,1):\n]",
        "[text(4,1):a:]",
        "[image(4,2):collapsed:/url:title:\nbar::::\nbar:::::]",
        "[text(5,7):a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<img src="/url" alt="\nbar" title="title" />a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_57aa():
    """
    Test case extra 57aa:  Paragraph with collapsed link with newline in label
    """

    # Arrange
    source_markdown = """[\nbar]: /url 'title'

a![
bar][]"""
    expected_tokens = [
        "[link-ref-def(1,1):True::bar:\nbar: :/url:: :title:'title':]",
        "[BLANK(3,1):]",
        "[para(4,1):\n]",
        "[text(4,1):a:]",
        "[image(4,2):collapsed:/url:title:\nbar::::\nbar:::::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<img src="/url" alt="\nbar" title="title" /></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_57b():
    """
    Test case extra 57b:  Paragraph with collapsed link with newline in label
    """

    # Arrange
    source_markdown = """[\nbar]: /url 'title'
    
a[
bar][]"""
    expected_tokens = [
        "[link-ref-def(1,1):True::bar:\nbar: :/url:: :title:'title':]",
        "[BLANK(3,1):    ]",
        "[para(4,1):\n]",
        "[text(4,1):a:]",
        "[link(4,2):collapsed:/url:title::::\nbar:::::]",
        "[text(4,3):\nbar::\n]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<a href="/url" title="title">\nbar</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_58():
    """
    Test case extra 58:  Paragraph with full link with newline in reference
    """

    # Arrange
    source_markdown = """[\nbar]: /url 'title'
    
a[foo][
bar]a"""
    expected_tokens = [
        "[link-ref-def(1,1):True::bar:\nbar: :/url:: :title:'title':]",
        "[BLANK(3,1):    ]",
        "[para(4,1):\n]",
        "[text(4,1):a:]",
        "[link(4,2):full:/url:title:::\nbar:foo:::::]",
        "[text(4,3):foo:]",
        "[end-link::]",
        "[text(5,5):a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<a href="/url" title="title">foo</a>a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_58a():
    """
    Test case extra 58a:  Paragraph with full link with newline in reference
    """

    # Arrange
    source_markdown = """[\nbar]: /url 'title'
    
a![foo][
bar]a"""
    expected_tokens = [
        "[link-ref-def(1,1):True::bar:\nbar: :/url:: :title:'title':]",
        "[BLANK(3,1):    ]",
        "[para(4,1):\n]",
        "[text(4,1):a:]",
        "[image(4,2):full:/url:title:foo:::\nbar:foo:::::]",
        "[text(5,5):a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<img src="/url" alt="foo" title="title" />a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_58aa():
    """
    Test case extra 58aa:  Paragraph with full link with newline in reference
    """

    # Arrange
    source_markdown = """[\nbar]: /url 'title'
    
a![foo][
bar]"""
    expected_tokens = [
        "[link-ref-def(1,1):True::bar:\nbar: :/url:: :title:'title':]",
        "[BLANK(3,1):    ]",
        "[para(4,1):\n]",
        "[text(4,1):a:]",
        "[image(4,2):full:/url:title:foo:::\nbar:foo:::::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<img src="/url" alt="foo" title="title" /></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_58b():
    """
    Test case extra 58b:  Paragraph with full link with newline in reference
    """

    # Arrange
    source_markdown = """[\nbar]: /url 'title'
    
a[foo][
bar]"""
    expected_tokens = [
        "[link-ref-def(1,1):True::bar:\nbar: :/url:: :title:'title':]",
        "[BLANK(3,1):    ]",
        "[para(4,1):\n]",
        "[text(4,1):a:]",
        "[link(4,2):full:/url:title:::\nbar:foo:::::]",
        "[text(4,3):foo:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<a href="/url" title="title">foo</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_59():
    """
    Test case extra 59:  Paragraph with inline image with newline between image chars, invalidating it.
    """

    # Arrange
    source_markdown = """a!
[Foo](/uri "testing")a"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):a!\n::\n]",
        '[link(2,1):inline:/uri:testing::::Foo:False:":: :]',
        "[text(2,2):Foo:]",
        "[end-link::]",
        "[text(2,22):a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a!\n<a href="/uri" title="testing">Foo</a>a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_59a():
    """
    Test case extra 59a:  Paragraph with inline image with newline between image chars, invalidating it.
    """

    # Arrange
    source_markdown = """a!
[Foo](/uri "testing")"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):a!\n::\n]",
        '[link(2,1):inline:/uri:testing::::Foo:False:":: :]',
        "[text(2,2):Foo:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a!\n<a href="/uri" title="testing">Foo</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_60():
    """
    Test case extra 60:  Paragraph with inline link with newline in label but not title.
    """

    # Arrange
    source_markdown = """a[Fo
o](/uri)a"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):a:]",
        "[link(1,2):inline:/uri:::::Fo\no:False::::]",
        "[text(1,3):Fo\no::\n]",
        "[end-link::]",
        "[text(2,9):a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<a href="/uri">Fo\no</a>a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_60a():
    """
    Test case extra 60a:  Paragraph with inline link with newline in label but not title.
    """

    # Arrange
    source_markdown = """a![Fo
o](/uri)a"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):a:]",
        "[image(1,2):inline:/uri::Fo\no::::Fo\no:False::::]",
        "[text(2,9):a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<img src="/uri" alt="Fo\no" />a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_60aa():
    """
    Test case extra 60aa:  Paragraph with inline link with newline in label but not title.
    """

    # Arrange
    source_markdown = """a![Fo
o](/uri)"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):a:]",
        "[image(1,2):inline:/uri::Fo\no::::Fo\no:False::::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<img src="/uri" alt="Fo\no" /></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_60b():
    """
    Test case extra 60b:  Paragraph with inline link with newline in label but not title.
    """

    # Arrange
    source_markdown = """a[Fo
o](/uri)"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):a:]",
        "[link(1,2):inline:/uri:::::Fo\no:False::::]",
        "[text(1,3):Fo\no::\n]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<a href="/uri">Fo\no</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_61():
    """
    Test case extra 61:  Paragraph with inline image with newline in label
    """

    # Arrange
    source_markdown = """a![fo
o](/url "title")a"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):a:]",
        '[image(1,2):inline:/url:title:fo\no::::fo\no:False:":: :]',
        "[text(2,17):a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<img src="/url" alt="fo\no" title="title" />a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_61a():
    """
    Test case extra 61a:  Paragraph with inline image with newline in label
    """

    # Arrange
    source_markdown = """a[fo&#xa;o](/url "title")a"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        '[link(1,2):inline:/url:title::::fo&#xa;o:False:":: :]',
        "[text(1,3):fo\a&#xa;\a\n\ao:]",
        "[end-link::]",
        "[text(1,26):a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<a href="/url" title="title">fo\no</a>a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_61b():
    """
    Test case extra 61b:  Paragraph with inline image with newline in label
    """

    # Arrange
    source_markdown = """a![fo&#xa;o](/url "title")a"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        '[image(1,2):inline:/url:title:fo\no::::fo&#xa;o:False:":: :]',
        "[text(1,27):a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<img src="/url" alt="fo\no" title="title" />a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_61c():
    """
    Test case extra 61c:  Paragraph with inline image with newline in label
    """

    # Arrange
    source_markdown = """a[fo&#Xa;o](/url "title")a"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        '[link(1,2):inline:/url:title::::fo&#Xa;o:False:":: :]',
        "[text(1,3):fo\a&#Xa;\a\n\ao:]",
        "[end-link::]",
        "[text(1,26):a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<a href="/url" title="title">fo\no</a>a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_61ca():
    """
    Test case extra 61c:  Paragraph with inline image with newline in label
    """

    # Arrange
    source_markdown = """a![fo&#Xa;o](/url "title")a"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        '[image(1,2):inline:/url:title:fo\no::::fo&#Xa;o:False:":: :]',
        "[text(1,27):a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<img src="/url" alt="fo\no" title="title" />a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_61d():
    """
    Test case extra 61d:  Paragraph with inline image with newline in label
    """

    # Arrange
    source_markdown = """a[fo&#x00000a;o](/url "title")a"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        '[link(1,2):inline:/url:title::::fo&#x00000a;o:False:":: :]',
        "[text(1,3):fo\a&#x00000a;\a\n\ao:]",
        "[end-link::]",
        "[text(1,31):a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<a href="/url" title="title">fo\no</a>a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_61da():
    """
    Test case extra 61d:  Paragraph with inline image with newline in label
    """

    # Arrange
    source_markdown = """a![fo&#x00000a;o](/url "title")a"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        '[image(1,2):inline:/url:title:fo\no::::fo&#x00000a;o:False:":: :]',
        "[text(1,32):a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<img src="/url" alt="fo\no" title="title" />a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_61e():
    """
    Test case extra 61e:  Paragraph with inline image with newline in label
    """

    # Arrange
    source_markdown = """a[fo&#10;o](/url "title")a"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        '[link(1,2):inline:/url:title::::fo&#10;o:False:":: :]',
        "[text(1,3):fo\a&#10;\a\n\ao:]",
        "[end-link::]",
        "[text(1,26):a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<a href="/url" title="title">fo\no</a>a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_61ea():
    """
    Test case extra 61e:  Paragraph with inline image with newline in label
    """

    # Arrange
    source_markdown = """a![fo&#10;o](/url "title")a"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        '[image(1,2):inline:/url:title:fo\no::::fo&#10;o:False:":: :]',
        "[text(1,27):a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<img src="/url" alt="fo\no" title="title" />a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_61f():
    """
    Test case extra 61f:  Paragraph with inline image with newline in label
    """

    # Arrange
    source_markdown = """a[fo&#0000010;o](/url "title")a"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        '[link(1,2):inline:/url:title::::fo&#0000010;o:False:":: :]',
        "[text(1,3):fo\a&#0000010;\a\n\ao:]",
        "[end-link::]",
        "[text(1,31):a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<a href="/url" title="title">fo\no</a>a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_61fa():
    """
    Test case extra 61f:  Paragraph with inline image with newline in label
    """

    # Arrange
    source_markdown = """a![fo&#0000010;o](/url "title")a"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        '[image(1,2):inline:/url:title:fo\no::::fo&#0000010;o:False:":: :]',
        "[text(1,32):a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<img src="/url" alt="fo\no" title="title" />a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_61g():
    """
    Test case extra 61g:  Paragraph with inline image with newline in label
    """

    # Arrange
    source_markdown = """a[fo&NewLine;o](/url "title")a"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        '[link(1,2):inline:/url:title::::fo&NewLine;o:False:":: :]',
        "[text(1,3):fo\a&NewLine;\a\n\ao:]",
        "[end-link::]",
        "[text(1,30):a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<a href="/url" title="title">fo\no</a>a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_61ga():
    """
    Test case extra 61g:  Paragraph with inline image with newline in label
    """

    # Arrange
    source_markdown = """a![fo&NewLine;o](/url "title")a"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        '[image(1,2):inline:/url:title:fo\no::::fo&NewLine;o:False:":: :]',
        "[text(1,31):a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<img src="/url" alt="fo\no" title="title" />a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_61h():
    """
    Test case extra 61c:  Paragraph with inline image with newline in label
    """

    # Arrange
    source_markdown = """a[fo&#xA;o](/url "title")a"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        '[link(1,2):inline:/url:title::::fo&#xA;o:False:":: :]',
        "[text(1,3):fo\a&#xA;\a\n\ao:]",
        "[end-link::]",
        "[text(1,26):a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<a href="/url" title="title">fo\no</a>a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_61ha():
    """
    Test case extra 61c:  Paragraph with inline image with newline in label
    """

    # Arrange
    source_markdown = """a![fo&#xA;o](/url "title")a"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        '[image(1,2):inline:/url:title:fo\no::::fo&#xA;o:False:":: :]',
        "[text(1,27):a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<img src="/url" alt="fo\no" title="title" />a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_61j():
    """
    Test case extra 61j:  Paragraph with inline image with newline in label
    """

    # Arrange
    source_markdown = """a![fo
o](/url "title")"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):a:]",
        '[image(1,2):inline:/url:title:fo\no::::fo\no:False:":: :]',
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<img src="/url" alt="fo\no" title="title" /></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_62():
    """
    Test case extra 62:  Paragraph with inline image with newline before URI
    """

    # Arrange
    source_markdown = """a![Foo](
/uri "testing")a"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):a:]",
        '[image(1,2):inline:/uri:testing:Foo::::Foo:False:":\n: :]',
        "[text(2,16):a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<img src="/uri" alt="Foo" title="testing" />a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_62a():
    """
    Test case extra 62a:  62 with whitespace before newline
    """

    # Arrange
    source_markdown = """a![Foo](\a\a
/uri "testing")a""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):a:]",
        '[image(1,2):inline:/uri:testing:Foo::::Foo:False:":  \n: :]',
        "[text(2,16):a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<img src="/uri" alt="Foo" title="testing" />a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_62b():
    """
    Test case extra 62b:  62 with whitespace after newline
    """

    # Arrange
    source_markdown = """a![Foo](
   /uri "testing")a"""
    expected_tokens = [
        "[para(1,1):\n   ]",
        "[text(1,1):a:]",
        '[image(1,2):inline:/uri:testing:Foo::::Foo:False:":\n: :]',
        "[text(2,19):a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<img src="/uri" alt="Foo" title="testing" />a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_62ba():
    """
    Test case extra 62ba:  62 with whitespace after newline
    """

    # Arrange
    source_markdown = """a![Foo](
   /uri "testing")"""
    expected_tokens = [
        "[para(1,1):\n   ]",
        "[text(1,1):a:]",
        '[image(1,2):inline:/uri:testing:Foo::::Foo:False:":\n: :]',
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<img src="/uri" alt="Foo" title="testing" /></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_62c():
    """
    Test case extra 62c:  62 with whitespace before and after newline
    """

    # Arrange
    source_markdown = """a![Foo](\a\a
   /uri "testing")a""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[para(1,1):\n   ]",
        "[text(1,1):a:]",
        '[image(1,2):inline:/uri:testing:Foo::::Foo:False:":  \n: :]',
        "[text(2,19):a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<img src="/uri" alt="Foo" title="testing" />a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_62ca():
    """
    Test case extra 62ca:  62 with whitespace before and after newline
    """

    # Arrange
    source_markdown = """a![Foo](\a\a
   /uri "testing")""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[para(1,1):\n   ]",
        "[text(1,1):a:]",
        '[image(1,2):inline:/uri:testing:Foo::::Foo:False:":  \n: :]',
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<img src="/uri" alt="Foo" title="testing" /></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_62d():
    """
    Test case extra 62d:  Paragraph with inline image with newline before URI
    """

    # Arrange
    source_markdown = """a[Foo](&#xa;/uri "testing")a"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        '[link(1,2):inline:%0A/uri:testing:&#xa;/uri:::Foo:False:":: :]',
        "[text(1,3):Foo:]",
        "[end-link::]",
        "[text(1,28):a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<a href="%0A/uri" title="testing">Foo</a>a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_62e():
    """
    Test case extra 62e:  Paragraph with inline image with newline before URI
    """

    # Arrange
    source_markdown = """a![Foo](&#xa;/uri "testing")a"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        '[image(1,2):inline:%0A/uri:testing:Foo:&#xa;/uri:::Foo:False:":: :]',
        "[text(1,29):a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<img src="%0A/uri" alt="Foo" title="testing" />a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_62f():
    """
    Test case extra 62f:  Paragraph with inline image with newline before URI
    """

    # Arrange
    source_markdown = """a![Foo](
/uri "testing")"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):a:]",
        '[image(1,2):inline:/uri:testing:Foo::::Foo:False:":\n: :]',
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<img src="/uri" alt="Foo" title="testing" /></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_63():
    """
    Test case extra 63:  Paragraph with inline image with newline in the URI, invalidating it
    """

    # Arrange
    source_markdown = """a![Foo](/ur
i "testing")a"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):a:]",
        "[text(1,2):![:]",
        "[text(1,4):Foo:]",
        "[text(1,7):]:]",
        '[text(1,8):(/ur\ni \a"\a&quot;\atesting\a"\a&quot;\a)a::\n]',
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a![Foo](/ur\ni &quot;testing&quot;)a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_63a():
    """
    Test case extra 63a:  Paragraph with inline image with newline in the URI, invalidating it
    """

    # Arrange
    source_markdown = """a[Foo](/ur&#xa;i "testing")a"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        '[link(1,2):inline:/ur%0Ai:testing:/ur&#xa;i:::Foo:False:":: :]',
        "[text(1,3):Foo:]",
        "[end-link::]",
        "[text(1,28):a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<a href="/ur%0Ai" title="testing">Foo</a>a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_63b():
    """
    Test case extra 63b:  Paragraph with inline image with newline in the URI, invalidating it
    """

    # Arrange
    source_markdown = """a![Foo](/ur&#xa;i "testing")a"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        '[image(1,2):inline:/ur%0Ai:testing:Foo:/ur&#xa;i:::Foo:False:":: :]',
        "[text(1,29):a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<img src="/ur%0Ai" alt="Foo" title="testing" />a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_63c():
    """
    Test case extra 63a:  Paragraph with inline image with newline in the URI, invalidating it
    """

    # Arrange
    source_markdown = """a[Foo](</ur&#xa;i> "testing")a"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        '[link(1,2):inline:/ur%0Ai:testing:/ur&#xa;i:::Foo:True:":: :]',
        "[text(1,3):Foo:]",
        "[end-link::]",
        "[text(1,30):a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<a href="/ur%0Ai" title="testing">Foo</a>a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_63d():
    """
    Test case extra 63b:  Paragraph with inline image with newline in the URI, invalidating it
    """

    # Arrange
    source_markdown = """a![Foo](</ur&#xa;i> "testing")a"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        '[image(1,2):inline:/ur%0Ai:testing:Foo:/ur&#xa;i:::Foo:True:":: :]',
        "[text(1,31):a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<img src="/ur%0Ai" alt="Foo" title="testing" />a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_63e():
    """
    Test case extra 63e:  Paragraph with inline image with newline in the URI, invalidating it
    """

    # Arrange
    source_markdown = """a![Foo](/ur
i "testing")"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):a:]",
        "[text(1,2):![:]",
        "[text(1,4):Foo:]",
        "[text(1,7):]:]",
        '[text(1,8):(/ur\ni \a"\a&quot;\atesting\a"\a&quot;\a)::\n]',
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a![Foo](/ur\ni &quot;testing&quot;)</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_64x():
    """
    Test case extra 64:  Paragraph with inline image with newline after the URI
    """

    # Arrange
    source_markdown = """a![Foo](/uri
"testing")a"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):a:]",
        '[image(1,2):inline:/uri:testing:Foo::::Foo:False:"::\n:]',
        "[text(2,11):a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<img src="/uri" alt="Foo" title="testing" />a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_64xa():
    """
    Test case extra 64a:  Paragraph with inline image with newline after the URI
    """

    # Arrange
    source_markdown = """a![Foo](/uri
"testing")"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):a:]",
        '[image(1,2):inline:/uri:testing:Foo::::Foo:False:"::\n:]',
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<img src="/uri" alt="Foo" title="testing" /></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_64a():
    """
    Test case extra 64a:  64 with whitespace before newline
    """

    # Arrange
    source_markdown = """a![Foo](/uri\a\a
"testing")a""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):a:]",
        '[image(1,2):inline:/uri:testing:Foo::::Foo:False:"::  \n:]',
        "[text(2,11):a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<img src="/uri" alt="Foo" title="testing" />a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_64b():
    """
    Test case extra 64b:  64 with whitespace after newline
    """

    # Arrange
    source_markdown = """a![Foo](/uri
 "testing")a"""
    expected_tokens = [
        "[para(1,1):\n ]",
        "[text(1,1):a:]",
        '[image(1,2):inline:/uri:testing:Foo::::Foo:False:"::\n:]',
        "[text(2,12):a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<img src="/uri" alt="Foo" title="testing" />a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_64ba():
    """
    Test case extra 64ba:  64 with whitespace after newline
    """

    # Arrange
    source_markdown = """a![Foo](/uri
 "testing")"""
    expected_tokens = [
        "[para(1,1):\n ]",
        "[text(1,1):a:]",
        '[image(1,2):inline:/uri:testing:Foo::::Foo:False:"::\n:]',
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<img src="/uri" alt="Foo" title="testing" /></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_64c():
    """
    Test case extra 64c:  64 with whitespace before and after newline
    """

    # Arrange
    source_markdown = """a![Foo](/uri\a\a
 "testing")a""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[para(1,1):\n ]",
        "[text(1,1):a:]",
        '[image(1,2):inline:/uri:testing:Foo::::Foo:False:"::  \n:]',
        "[text(2,12):a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<img src="/uri" alt="Foo" title="testing" />a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_64ca():
    """
    Test case extra 64ca:  64 with whitespace before and after newline
    """

    # Arrange
    source_markdown = """a![Foo](/uri\a\a
 "testing")""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[para(1,1):\n ]",
        "[text(1,1):a:]",
        '[image(1,2):inline:/uri:testing:Foo::::Foo:False:"::  \n:]',
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<img src="/uri" alt="Foo" title="testing" /></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_64d():
    """
    Test case extra 64d:  Paragraph with inline image with newline after the URI
    """

    # Arrange
    source_markdown = """a[Foo](/uri&#xa;"testing")a"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        '[link(1,2):inline:/uri%0A%22testing%22::/uri&#xa;"testing":::Foo:False::::]',
        "[text(1,3):Foo:]",
        "[end-link::]",
        "[text(1,27):a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<a href="/uri%0A%22testing%22">Foo</a>a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_64e():
    """
    Test case extra 64e:  Paragraph with inline image with newline after the URI
    """

    # Arrange
    source_markdown = """a![Foo](/uri&#xa;"testing")a"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        '[image(1,2):inline:/uri%0A%22testing%22::Foo:/uri&#xa;"testing":::Foo:False::::]',
        "[text(1,28):a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<img src="/uri%0A%22testing%22" alt="Foo" />a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_65x():
    """
    Test case extra 65x:  Paragraph with inline image with newline after the URI and no text
    """

    # Arrange
    source_markdown = """a![Foo](/uri
)a"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):a:]",
        "[image(1,2):inline:/uri::Foo::::Foo:False:::\n:]",
        "[text(2,2):a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<img src="/uri" alt="Foo" />a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_65xa():
    """
    Test case extra 65xa:  Paragraph with inline image with newline after the URI and no text
    """

    # Arrange
    source_markdown = """a![Foo](/uri
)"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):a:]",
        "[image(1,2):inline:/uri::Foo::::Foo:False:::\n:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<img src="/uri" alt="Foo" /></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_65a():
    """
    Test case extra 65a:  Paragraph with inline image with newline after the URI and no text
    """

    # Arrange
    source_markdown = """a[Foo](/uri
)a"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):a:]",
        "[link(1,2):inline:/uri:::::Foo:False:::\n:]",
        "[text(1,3):Foo:]",
        "[end-link::]",
        "[text(2,2):a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<a href="/uri">Foo</a>a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_65b():
    """
    Test case extra 65b:  Paragraph with inline image with newline after the URI and no text
    """

    # Arrange
    source_markdown = """a[Foo](/uri
)"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):a:]",
        "[link(1,2):inline:/uri:::::Foo:False:::\n:]",
        "[text(1,3):Foo:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<a href="/uri">Foo</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_66x():
    """
    Test case extra 66:  Paragraph with inline image with newline in the title
    """

    # Arrange
    source_markdown = """a![Foo](/uri "test
ing")a"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):a:]",
        '[image(1,2):inline:/uri:test\ning:Foo::::Foo:False:":: :]',
        "[text(2,6):a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<img src="/uri" alt="Foo" title="test\ning" />a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_66xa():
    """
    Test case extra 66xa:  Paragraph with inline image with newline in the title
    """

    # Arrange
    source_markdown = """a![Foo](/uri "test
ing")"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):a:]",
        '[image(1,2):inline:/uri:test\ning:Foo::::Foo:False:":: :]',
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<img src="/uri" alt="Foo" title="test\ning" /></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_66a():
    """
    Test case extra 66a:  Paragraph with inline image with newline in the title
    """

    # Arrange
    source_markdown = """a[Foo](/uri "test&#xa;ing")a"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        '[link(1,2):inline:/uri:test\ning::test&#xa;ing::Foo:False:":: :]',
        "[text(1,3):Foo:]",
        "[end-link::]",
        "[text(1,28):a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<a href="/uri" title="test\ning">Foo</a>a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_66b():
    """
    Test case extra 66b:  Paragraph with inline image with newline in the title
    """

    # Arrange
    source_markdown = """a![Foo](/uri "test&#xa;ing")a"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        '[image(1,2):inline:/uri:test\ning:Foo::test&#xa;ing::Foo:False:":: :]',
        "[text(1,29):a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<img src="/uri" alt="Foo" title="test\ning" />a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_66c():
    """
    Test case extra 66c:  Paragraph with inline image with newline in the title
    """

    # Arrange
    source_markdown = """a![Foo](</uri> "test
ing")a"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):a:]",
        '[image(1,2):inline:/uri:test\ning:Foo::::Foo:True:":: :]',
        "[text(2,6):a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<img src="/uri" alt="Foo" title="test\ning" />a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_66ca():
    """
    Test case extra 66ca:  Paragraph with inline image with newline in the title
    """

    # Arrange
    source_markdown = """a![Foo](</uri> "test
ing")"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):a:]",
        '[image(1,2):inline:/uri:test\ning:Foo::::Foo:True:":: :]',
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<img src="/uri" alt="Foo" title="test\ning" /></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_66d():
    """
    Test case extra 66d:  Paragraph with inline image with newline in the title
    """

    # Arrange
    source_markdown = """a[Foo](</uri> "te\\\\st
ing")a"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):a:]",
        '[link(1,2):inline:/uri:te\\st\ning::te\\\\st\ning::Foo:True:":: :]',
        "[text(1,3):Foo:]",
        "[end-link::]",
        "[text(2,6):a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<a href="/uri" title="te\\st\ning">Foo</a>a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_66da():
    """
    Test case extra 66da:  Paragraph with inline image with newline in the title
    """

    # Arrange
    source_markdown = """a[Foo](</uri> "te\\\\st
ing")"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):a:]",
        '[link(1,2):inline:/uri:te\\st\ning::te\\\\st\ning::Foo:True:":: :]',
        "[text(1,3):Foo:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<a href="/uri" title="te\\st\ning">Foo</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_67x():
    """
    Test case extra 67:  Paragraph with inline image with newline after the title
    """

    # Arrange
    source_markdown = """a![Foo](/uri "testing"
)a"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):a:]",
        '[image(1,2):inline:/uri:testing:Foo::::Foo:False:":: :\n]',
        "[text(2,2):a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<img src="/uri" alt="Foo" title="testing" />a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_67xa():
    """
    Test case extra 67:  Paragraph with inline image with newline after the title
    """

    # Arrange
    source_markdown = """a![Foo](/uri "testing"
)"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):a:]",
        '[image(1,2):inline:/uri:testing:Foo::::Foo:False:":: :\n]',
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<img src="/uri" alt="Foo" title="testing" /></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_67a():
    """
    Test case extra 67a:  67 with whitespace before newline
    """

    # Arrange
    source_markdown = """a![Foo](/uri "testing"\a\a
)a""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):a:]",
        '[image(1,2):inline:/uri:testing:Foo::::Foo:False:":: :  \n]',
        "[text(2,2):a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<img src="/uri" alt="Foo" title="testing" />a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_67aa():
    """
    Test case extra 67aa:  67 with whitespace before newline
    """

    # Arrange
    source_markdown = """a![Foo](/uri "testing"\a\a
)""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):a:]",
        '[image(1,2):inline:/uri:testing:Foo::::Foo:False:":: :  \n]',
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<img src="/uri" alt="Foo" title="testing" /></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_67b():
    """
    Test case extra 67b:  67 with whitespace after newline
    """

    # Arrange
    source_markdown = """a![Foo](/uri "testing"
   )a"""
    expected_tokens = [
        "[para(1,1):\n   ]",
        "[text(1,1):a:]",
        '[image(1,2):inline:/uri:testing:Foo::::Foo:False:":: :\n]',
        "[text(2,5):a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<img src="/uri" alt="Foo" title="testing" />a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_67ba():
    """
    Test case extra 67ba:  67 with whitespace after newline
    """

    # Arrange
    source_markdown = """a![Foo](/uri "testing"
   )"""
    expected_tokens = [
        "[para(1,1):\n   ]",
        "[text(1,1):a:]",
        '[image(1,2):inline:/uri:testing:Foo::::Foo:False:":: :\n]',
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<img src="/uri" alt="Foo" title="testing" /></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_67c():
    """
    Test case extra 67c:  67 with whitespace before and after newline
    """

    # Arrange
    source_markdown = """a![Foo](/uri "testing"\a\a
   )a""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[para(1,1):\n   ]",
        "[text(1,1):a:]",
        '[image(1,2):inline:/uri:testing:Foo::::Foo:False:":: :  \n]',
        "[text(2,5):a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<img src="/uri" alt="Foo" title="testing" />a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_67ca():
    """
    Test case extra 67ca:  67 with whitespace before and after newline
    """

    # Arrange
    source_markdown = """a![Foo](/uri "testing"\a\a
   )""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[para(1,1):\n   ]",
        "[text(1,1):a:]",
        '[image(1,2):inline:/uri:testing:Foo::::Foo:False:":: :  \n]',
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<img src="/uri" alt="Foo" title="testing" /></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_67d():
    """
    Test case extra 67d:  67 with whitespace before and after newline
    """

    # Arrange
    source_markdown = """a[Foo](/uri "testing"&#xa;)a"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        "[text(1,2):[:]",
        "[text(1,3):Foo:]",
        "[text(1,6):]:]",
        '[text(1,7):(/uri \a"\a&quot;\atesting\a"\a&quot;\a\a&#xa;\a\n\a)a:]',
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a[Foo](/uri &quot;testing&quot;\n)a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_67e():
    """
    Test case extra 67e:  67 with whitespace before and after newline
    """

    # Arrange
    source_markdown = """a![Foo](/uri "testing"&#xa;)a"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        "[text(1,2):![:]",
        "[text(1,4):Foo:]",
        "[text(1,7):]:]",
        '[text(1,8):(/uri \a"\a&quot;\atesting\a"\a&quot;\a\a&#xa;\a\n\a)a:]',
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a![Foo](/uri &quot;testing&quot;\n)a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_68x():
    """
    Test case extra 68:  Paragraph with link containing label with replacement
    """

    # Arrange
    source_markdown = """a[Fo&beta;o](/uri "testing")a"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        '[link(1,2):inline:/uri:testing::::Fo&beta;o:False:":: :]',
        "[text(1,3):Fo\a&beta;\aβ\ao:]",
        "[end-link::]",
        "[text(1,29):a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<a href="/uri" title="testing">Foβo</a>a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_68a():
    """
    Test case extra 68a:  68 without special characters
    """

    # Arrange
    source_markdown = """a[Foo](/uri "testing")a"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        '[link(1,2):inline:/uri:testing::::Foo:False:":: :]',
        "[text(1,3):Foo:]",
        "[end-link::]",
        "[text(1,23):a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<a href="/uri" title="testing">Foo</a>a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_68b():
    """
    Test case extra 68b:  68 with newline before special characters
    """

    # Arrange
    source_markdown = """a[Fo
&beta;o](/uri "testing")a"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):a:]",
        '[link(1,2):inline:/uri:testing::::Fo\n&beta;o:False:":: :]',
        "[text(1,3):Fo\n\a&beta;\aβ\ao::\n]",
        "[end-link::]",
        "[text(2,25):a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<a href="/uri" title="testing">Fo\nβo</a>a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_69():
    """
    Test case extra 69:  Paragraph with link containing label with backslash
    """

    # Arrange
    source_markdown = """a[Fo\\]o](/uri "testing")a"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        '[link(1,2):inline:/uri:testing::::Fo\\]o:False:":: :]',
        "[text(1,3):Fo\\\b]o:]",
        "[end-link::]",
        "[text(1,25):a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<a href="/uri" title="testing">Fo]o</a>a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_69a():
    """
    Test case extra 69a:  69 with newline before special characters
    """

    # Arrange
    source_markdown = """a[Fo
\\]o](/uri "testing")a"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):a:]",
        '[link(1,2):inline:/uri:testing::::Fo\n\\]o:False:":: :]',
        "[text(1,3):Fo\n\\\b]o::\n]",
        "[end-link::]",
        "[text(2,21):a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<a href="/uri" title="testing">Fo\n]o</a>a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_70():
    """
    Test case extra 70:  Paragraph with link containing uri with space
    """

    # Arrange
    source_markdown = """a[Foo](</my uri> "testing")a"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        '[link(1,2):inline:/my%20uri:testing:/my uri:::Foo:True:":: :]',
        "[text(1,3):Foo:]",
        "[end-link::]",
        "[text(1,28):a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<a href="/my%20uri" title="testing">Foo</a>a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_70a():
    """
    Test case extra 70a:  70 with newline before special characters, rendering it invalid
    """

    # Arrange
    source_markdown = """a[Foo](</my
 uri> "testing")a"""
    expected_tokens = [
        "[para(1,1):\n ]",
        "[text(1,1):a:]",
        "[text(1,2):[:]",
        "[text(1,3):Foo:]",
        "[text(1,6):]:]",
        '[text(1,7):(\a<\a&lt;\a/my\nuri\a>\a&gt;\a \a"\a&quot;\atesting\a"\a&quot;\a)a::\n]',
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a[Foo](&lt;/my\nuri&gt; &quot;testing&quot;)a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_71x():
    """
    Test case extra 71:  Paragraph with link containing title with replacement
    """

    # Arrange
    source_markdown = """a[Foo](/uri "test&beta;ing")a"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        '[link(1,2):inline:/uri:testβing::test&beta;ing::Foo:False:":: :]',
        "[text(1,3):Foo:]",
        "[end-link::]",
        "[text(1,29):a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<a href="/uri" title="testβing">Foo</a>a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_71a():
    """
    Test case extra 71a:  71 with newline before special characters
    """

    # Arrange
    source_markdown = """a[Foo](/uri "test
&beta;ing")a"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):a:]",
        '[link(1,2):inline:/uri:test\nβing::test\n&beta;ing::Foo:False:":: :]',
        "[text(1,3):Foo:]",
        "[end-link::]",
        "[text(2,12):a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<a href="/uri" title="test\nβing">Foo</a>a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_72():
    """
    Test case extra 72:  Paragraph with link containing title with backslash
    """

    # Arrange
    source_markdown = """a[Foo](/uri "test\\#ing")a"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        '[link(1,2):inline:/uri:test#ing::test\\#ing::Foo:False:":: :]',
        "[text(1,3):Foo:]",
        "[end-link::]",
        "[text(1,25):a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<a href="/uri" title="test#ing">Foo</a>a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_72a():
    """
    Test case extra 72a:  72 with newline before special characters
    """

    # Arrange
    source_markdown = """a[Foo](/uri "test
\\#ing")a"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):a:]",
        '[link(1,2):inline:/uri:test\n#ing::test\n\\#ing::Foo:False:":: :]',
        "[text(1,3):Foo:]",
        "[end-link::]",
        "[text(2,8):a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<a href="/uri" title="test\n#ing">Foo</a>a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_73():
    """
    Test case extra 73:  Paragraph with image containing label with replacement
    """

    # Arrange
    source_markdown = """a![Fo&beta;o](/uri "testing")a"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        '[image(1,2):inline:/uri:testing:Foβo::::Fo&beta;o:False:":: :]',
        "[text(1,30):a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<img src="/uri" alt="Foβo" title="testing" />a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_73a():
    """
    Test case extra 73a:  73 without special characters
    """

    # Arrange
    source_markdown = """a![Foo](/uri "testing")a"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        '[image(1,2):inline:/uri:testing:Foo::::Foo:False:":: :]',
        "[text(1,24):a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<img src="/uri" alt="Foo" title="testing" />a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_73b():
    """
    Test case extra 73b:  73 with newline before special characters
    """

    # Arrange
    source_markdown = """a![Fo
&beta;o](/uri "testing")a"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):a:]",
        '[image(1,2):inline:/uri:testing:Fo\nβo::::Fo\n&beta;o:False:":: :]',
        "[text(2,25):a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<img src="/uri" alt="Fo\nβo" title="testing" />a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_74():
    """
    Test case extra 74:  Paragraph with image containing label with backslash
    """

    # Arrange
    source_markdown = """a![Fo\\]o](/uri "testing")a"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        '[image(1,2):inline:/uri:testing:Fo]o::::Fo\\]o:False:":: :]',
        "[text(1,26):a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<img src="/uri" alt="Fo]o" title="testing" />a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_74a():
    """
    Test case extra 74a:  74 with newline before special characters
    """

    # Arrange
    source_markdown = """a![Fo
\\]o](/uri "testing")a"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):a:]",
        '[image(1,2):inline:/uri:testing:Fo\n]o::::Fo\n\\]o:False:":: :]',
        "[text(2,21):a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<img src="/uri" alt="Fo\n]o" title="testing" />a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_75():
    """
    Test case extra 75:  Paragraph with image containing uri with space
    """

    # Arrange
    source_markdown = """a![Foo](</my uri> "testing")a"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        '[image(1,2):inline:/my%20uri:testing:Foo:/my uri:::Foo:True:":: :]',
        "[text(1,29):a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<img src="/my%20uri" alt="Foo" title="testing" />a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_75a():
    """
    Test case extra 75a:  75 with newline before special characters, invalidating it
    """

    # Arrange
    source_markdown = """a![Foo](</my
 uri> "testing")a"""
    expected_tokens = [
        "[para(1,1):\n ]",
        "[text(1,1):a:]",
        "[text(1,2):![:]",
        "[text(1,4):Foo:]",
        "[text(1,7):]:]",
        '[text(1,8):(\a<\a&lt;\a/my\nuri\a>\a&gt;\a \a"\a&quot;\atesting\a"\a&quot;\a)a::\n]',
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a![Foo](&lt;/my\nuri&gt; &quot;testing&quot;)a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_76():
    """
    Test case extra 76:  Paragraph with image containing title with replacement
    """

    # Arrange
    source_markdown = """a![Foo](/uri "test&beta;ing")a"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        '[image(1,2):inline:/uri:testβing:Foo::test&beta;ing::Foo:False:":: :]',
        "[text(1,30):a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<img src="/uri" alt="Foo" title="testβing" />a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_76a():
    """
    Test case extra 76a:  76 with newline before special characters
    """

    # Arrange
    source_markdown = """a![Foo](/uri "test
&beta;ing")a"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):a:]",
        '[image(1,2):inline:/uri:test\nβing:Foo::test\n&beta;ing::Foo:False:":: :]',
        "[text(2,12):a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<img src="/uri" alt="Foo" title="test\nβing" />a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_77():
    """
    Test case extra 77:  Paragraph with image containing title with backslash
    """

    # Arrange
    source_markdown = """a![Foo](/uri "test\\#ing")a"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        '[image(1,2):inline:/uri:test#ing:Foo::test\\#ing::Foo:False:":: :]',
        "[text(1,26):a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<img src="/uri" alt="Foo" title="test#ing" />a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_77a():
    """
    Test case extra 77a:  77 with newline before special characters
    """

    # Arrange
    source_markdown = """a![Foo](/uri "test\n\\#ing")a"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):a:]",
        '[image(1,2):inline:/uri:test\n#ing:Foo::test\n\\#ing::Foo:False:":: :]',
        "[text(2,8):a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<img src="/uri" alt="Foo" title="test\n#ing" />a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_78():
    """
    Test case extra 78:  Paragraph with full link with backslash in label
    """

    # Arrange
    source_markdown = """a[foo\\#bar][bar]a

[bar]: /url 'title'"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        "[link(1,2):full:/url:title:::bar:foo\\#bar:::::]",
        "[text(1,3):foo\\\b#bar:]",
        "[end-link::]",
        "[text(1,17):a:]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[link-ref-def(3,1):True::bar:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<p>a<a href="/url" title="title">foo#bar</a>a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_78a():
    """
    Test case extra 78a:  78 with newline before special chars
    """

    # Arrange
    source_markdown = """a[foo
\\#bar][bar]a

[bar]: /url 'title'"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):a:]",
        "[link(1,2):full:/url:title:::bar:foo\n\\#bar:::::]",
        "[text(1,3):foo\n\\\b#bar::\n]",
        "[end-link::]",
        "[text(2,12):a:]",
        "[end-para:::True]",
        "[BLANK(3,1):]",
        "[link-ref-def(4,1):True::bar:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<p>a<a href="/url" title="title">foo\n#bar</a>a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_79():
    """
    Test case extra 79:  Paragraph with full link with replacement in label
    """

    # Arrange
    source_markdown = """a[foo&beta;bar][bar]a

[bar]: /url 'title'"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        "[link(1,2):full:/url:title:::bar:foo&beta;bar:::::]",
        "[text(1,3):foo\a&beta;\aβ\abar:]",
        "[end-link::]",
        "[text(1,21):a:]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[link-ref-def(3,1):True::bar:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<p>a<a href="/url" title="title">fooβbar</a>a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_79a():
    """
    Test case extra 79a:  79 with newline before special characters
    """

    # Arrange
    source_markdown = """a[foo
&beta;bar][bar]a

[bar]: /url 'title'"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):a:]",
        "[link(1,2):full:/url:title:::bar:foo\n&beta;bar:::::]",
        "[text(1,3):foo\n\a&beta;\aβ\abar::\n]",
        "[end-link::]",
        "[text(2,16):a:]",
        "[end-para:::True]",
        "[BLANK(3,1):]",
        "[link-ref-def(4,1):True::bar:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<p>a<a href="/url" title="title">foo\nβbar</a>a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_80():
    """
    Test case extra 80:  Paragraph with full link with replacement in reference
    """

    # Arrange
    source_markdown = """a[foo][ba&beta;r]a

[ba&beta;r]: /url 'title'"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        "[link(1,2):full:/url:title:::ba&beta;r:foo:::::]",
        "[text(1,3):foo:]",
        "[end-link::]",
        "[text(1,18):a:]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[link-ref-def(3,1):True::ba&beta;r:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<p>a<a href="/url" title="title">foo</a>a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_80a():
    """
    Test case extra 80a:  80 with newline before special characters
    """

    # Arrange
    source_markdown = """a[foo][ba
&beta;r]a

[ba
&beta;r]: /url 'title'"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):a:]",
        "[link(1,2):full:/url:title:::ba\n&beta;r:foo:::::]",
        "[text(1,3):foo:]",
        "[end-link::]",
        "[text(2,9):a:]",
        "[end-para:::True]",
        "[BLANK(3,1):]",
        "[link-ref-def(4,1):True::ba &beta;r:ba\n&beta;r: :/url:: :title:'title':]",
    ]
    expected_gfm = """<p>a<a href="/url" title="title">foo</a>a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_81():
    """
    Test case extra 81:  Paragraph with full link with backspace in reference
    """

    # Arrange
    source_markdown = """a[foo][ba\\]r]a

[ba\\]r]: /url 'title'"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        "[link(1,2):full:/url:title:::ba\\]r:foo:::::]",
        "[text(1,3):foo:]",
        "[end-link::]",
        "[text(1,14):a:]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[link-ref-def(3,1):True::ba\\]r:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<p>a<a href="/url" title="title">foo</a>a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_81a():
    """
    Test case extra 81a:  81 with newline before special characters
    """

    # Arrange
    source_markdown = """a[foo][ba
\\]r]a

[ba
\\]r]: /url 'title'"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):a:]",
        "[link(1,2):full:/url:title:::ba\n\\]r:foo:::::]",
        "[text(1,3):foo:]",
        "[end-link::]",
        "[text(2,5):a:]",
        "[end-para:::True]",
        "[BLANK(3,1):]",
        "[link-ref-def(4,1):True::ba \\]r:ba\n\\]r: :/url:: :title:'title':]",
    ]
    expected_gfm = """<p>a<a href="/url" title="title">foo</a>a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_82():
    """
    Test case extra 82:  Paragraph with shortcut link with replacement in label
    """

    # Arrange
    source_markdown = """a[ba&beta;r]a

[ba&beta;r]: /url 'title'"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        "[link(1,2):shortcut:/url:title::::ba&beta;r:::::]",
        "[text(1,3):ba\a&beta;\aβ\ar:]",
        "[end-link::]",
        "[text(1,13):a:]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[link-ref-def(3,1):True::ba&beta;r:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<p>a<a href="/url" title="title">baβr</a>a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_82a():
    """
    Test case extra 82a:  82 with newline before special characters
    """

    # Arrange
    source_markdown = """a[ba
&beta;r]a

[ba
&beta;r]: /url 'title'"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):a:]",
        "[link(1,2):shortcut:/url:title::::ba\n&beta;r:::::]",
        "[text(1,3):ba\n\a&beta;\aβ\ar::\n]",
        "[end-link::]",
        "[text(2,9):a:]",
        "[end-para:::True]",
        "[BLANK(3,1):]",
        "[link-ref-def(4,1):True::ba &beta;r:ba\n&beta;r: :/url:: :title:'title':]",
    ]
    expected_gfm = """<p>a<a href="/url" title="title">ba\nβr</a>a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_83():
    """
    Test case extra 83:  Paragraph with shortcut link with backslash in label
    """

    # Arrange
    source_markdown = """a[ba\\]r]a

[ba\\]r]: /url 'title'"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        "[link(1,2):shortcut:/url:title::::ba\\]r:::::]",
        "[text(1,3):ba\\\b]r:]",
        "[end-link::]",
        "[text(1,9):a:]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[link-ref-def(3,1):True::ba\\]r:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<p>a<a href="/url" title="title">ba]r</a>a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_83a():
    """
    Test case extra 83a:  83 with newline before special characters
    """

    # Arrange
    source_markdown = """a[ba
\\]r]a

[ba
\\]r]: /url 'title'"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):a:]",
        "[link(1,2):shortcut:/url:title::::ba\n\\]r:::::]",
        "[text(1,3):ba\n\\\b]r::\n]",
        "[end-link::]",
        "[text(2,5):a:]",
        "[end-para:::True]",
        "[BLANK(3,1):]",
        "[link-ref-def(4,1):True::ba \\]r:ba\n\\]r: :/url:: :title:'title':]",
    ]
    expected_gfm = """<p>a<a href="/url" title="title">ba\n]r</a>a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_84x():
    """
    Test case extra 84:  Paragraph with collapsed link with replacement in label
    """

    # Arrange
    source_markdown = """a[ba&beta;r][]a

[ba&beta;r]: /url 'title'"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        "[link(1,2):collapsed:/url:title::::ba&beta;r:::::]",
        "[text(1,3):ba\a&beta;\aβ\ar:]",
        "[end-link::]",
        "[text(1,15):a:]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[link-ref-def(3,1):True::ba&beta;r:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<p>a<a href="/url" title="title">baβr</a>a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_84a():
    """
    Test case extra 84a:  84 with newline before special characters
    """

    # Arrange
    source_markdown = """a[ba
&beta;r][]a

[ba
&beta;r]: /url 'title'"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):a:]",
        "[link(1,2):collapsed:/url:title::::ba\n&beta;r:::::]",
        "[text(1,3):ba\n\a&beta;\aβ\ar::\n]",
        "[end-link::]",
        "[text(2,11):a:]",
        "[end-para:::True]",
        "[BLANK(3,1):]",
        "[link-ref-def(4,1):True::ba &beta;r:ba\n&beta;r: :/url:: :title:'title':]",
    ]
    expected_gfm = """<p>a<a href="/url" title="title">ba\nβr</a>a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_85():
    """
    Test case extra 85:  Paragraph with collapsed link with backslash in label
    """

    # Arrange
    source_markdown = """a[ba\\]r][]a

[ba\\]r]: /url 'title'"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        "[link(1,2):collapsed:/url:title::::ba\\]r:::::]",
        "[text(1,3):ba\\\b]r:]",
        "[end-link::]",
        "[text(1,11):a:]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[link-ref-def(3,1):True::ba\\]r:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<p>a<a href="/url" title="title">ba]r</a>a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_85a():
    """
    Test case extra 85a:  85 with newline before special characters
    """

    # Arrange
    source_markdown = """a[ba
\\]r][]a

[ba
\\]r]: /url 'title'"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):a:]",
        "[link(1,2):collapsed:/url:title::::ba\n\\]r:::::]",
        "[text(1,3):ba\n\\\b]r::\n]",
        "[end-link::]",
        "[text(2,7):a:]",
        "[end-para:::True]",
        "[BLANK(3,1):]",
        "[link-ref-def(4,1):True::ba \\]r:ba\n\\]r: :/url:: :title:'title':]",
    ]
    expected_gfm = """<p>a<a href="/url" title="title">ba\n]r</a>a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_90x():
    """
    Test case extra 90:  Paragraph with full image with backslash in label
    """

    # Arrange
    source_markdown = """a![foo\\#bar][bar]a

[bar]: /url 'title'"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        "[image(1,2):full:/url:title:foo#bar:::bar:foo\\#bar:::::]",
        "[text(1,18):a:]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[link-ref-def(3,1):True::bar:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<p>a<img src="/url" alt="foo#bar" title="title" />a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_90a():
    """
    Test case extra 90a:  90 with newline before special chars
    """

    # Arrange
    source_markdown = """a![foo
\\#bar][bar]a

[bar]: /url 'title'"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):a:]",
        "[image(1,2):full:/url:title:foo\n#bar:::bar:foo\n\\#bar:::::]",
        "[text(2,12):a:]",
        "[end-para:::True]",
        "[BLANK(3,1):]",
        "[link-ref-def(4,1):True::bar:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<p>a<img src="/url" alt="foo\n#bar" title="title" />a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_91x():
    """
    Test case extra 91:  Paragraph with full image with replacement in label
    """

    # Arrange
    source_markdown = """a![foo&beta;bar][bar]a

[bar]: /url 'title'"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        "[image(1,2):full:/url:title:fooβbar:::bar:foo&beta;bar:::::]",
        "[text(1,22):a:]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[link-ref-def(3,1):True::bar:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<p>a<img src="/url" alt="fooβbar" title="title" />a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_91a():
    """
    Test case extra 91a:  91 with newline before special characters
    """

    # Arrange
    source_markdown = """a![foo
&beta;bar][bar]a

[bar]: /url 'title'"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):a:]",
        "[image(1,2):full:/url:title:foo\nβbar:::bar:foo\n&beta;bar:::::]",
        "[text(2,16):a:]",
        "[end-para:::True]",
        "[BLANK(3,1):]",
        "[link-ref-def(4,1):True::bar:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<p>a<img src="/url" alt="foo\nβbar" title="title" />a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_92x():
    """
    Test case extra 92:  Paragraph with full image with replacement in reference
    """

    # Arrange
    source_markdown = """a![foo][ba&beta;r]a

[ba&beta;r]: /url 'title'"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        "[image(1,2):full:/url:title:foo:::ba&beta;r:foo:::::]",
        "[text(1,19):a:]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[link-ref-def(3,1):True::ba&beta;r:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<p>a<img src="/url" alt="foo" title="title" />a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_92a():
    """
    Test case extra 92a:  92 with newline before special characters
    """

    # Arrange
    source_markdown = """a![foo][ba
&beta;r]a

[ba
&beta;r]: /url 'title'"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):a:]",
        "[image(1,2):full:/url:title:foo:::ba\n&beta;r:foo:::::]",
        "[text(2,9):a:]",
        "[end-para:::True]",
        "[BLANK(3,1):]",
        "[link-ref-def(4,1):True::ba &beta;r:ba\n&beta;r: :/url:: :title:'title':]",
    ]
    expected_gfm = """<p>a<img src="/url" alt="foo" title="title" />a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_93x():
    """
    Test case extra 93:  Paragraph with full image with backspace in reference
    """

    # Arrange
    source_markdown = """a![foo][ba\\]r]a

[ba\\]r]: /url 'title'"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        "[image(1,2):full:/url:title:foo:::ba\\]r:foo:::::]",
        "[text(1,15):a:]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[link-ref-def(3,1):True::ba\\]r:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<p>a<img src="/url" alt="foo" title="title" />a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_93a():
    """
    Test case extra 93a:  93 with newline before special characters
    """

    # Arrange
    source_markdown = """a![foo][ba
\\]r]a

[ba
\\]r]: /url 'title'"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):a:]",
        "[image(1,2):full:/url:title:foo:::ba\n\\]r:foo:::::]",
        "[text(2,5):a:]",
        "[end-para:::True]",
        "[BLANK(3,1):]",
        "[link-ref-def(4,1):True::ba \\]r:ba\n\\]r: :/url:: :title:'title':]",
    ]
    expected_gfm = """<p>a<img src="/url" alt="foo" title="title" />a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_94x():
    """
    Test case extra 94:  Paragraph with shortcut image with replacement in label
    """

    # Arrange
    source_markdown = """a![ba&beta;r]a

[ba&beta;r]: /url 'title'"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        "[image(1,2):shortcut:/url:title:baβr::::ba&beta;r:::::]",
        "[text(1,14):a:]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[link-ref-def(3,1):True::ba&beta;r:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<p>a<img src="/url" alt="baβr" title="title" />a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_94a():
    """
    Test case extra 94a:  94 with newline before special characters
    """

    # Arrange
    source_markdown = """a![ba
&beta;r]a

[ba
&beta;r]: /url 'title'"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):a:]",
        "[image(1,2):shortcut:/url:title:ba\nβr::::ba\n&beta;r:::::]",
        "[text(2,9):a:]",
        "[end-para:::True]",
        "[BLANK(3,1):]",
        "[link-ref-def(4,1):True::ba &beta;r:ba\n&beta;r: :/url:: :title:'title':]",
    ]
    expected_gfm = """<p>a<img src="/url" alt="ba\nβr" title="title" />a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_95x():
    """
    Test case extra 95:  Paragraph with shortcut image with backslash in label
    """

    # Arrange
    source_markdown = """a![ba\\]r]a

[ba\\]r]: /url 'title'"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        "[image(1,2):shortcut:/url:title:ba]r::::ba\\]r:::::]",
        "[text(1,10):a:]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[link-ref-def(3,1):True::ba\\]r:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<p>a<img src="/url" alt="ba]r" title="title" />a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_95a():
    """
    Test case extra 95a:  95 with newline before special characters
    """

    # Arrange
    source_markdown = """a![ba
\\]r]a

[ba
\\]r]: /url 'title'"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):a:]",
        "[image(1,2):shortcut:/url:title:ba\n]r::::ba\n\\]r:::::]",
        "[text(2,5):a:]",
        "[end-para:::True]",
        "[BLANK(3,1):]",
        "[link-ref-def(4,1):True::ba \\]r:ba\n\\]r: :/url:: :title:'title':]",
    ]
    expected_gfm = """<p>a<img src="/url" alt="ba\n]r" title="title" />a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_96x():
    """
    Test case extra 96:  Paragraph with collapsed image with replacement in label
    """

    # Arrange
    source_markdown = """a![ba&beta;r][]a

[ba&beta;r]: /url 'title'"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        "[image(1,2):collapsed:/url:title:baβr::::ba&beta;r:::::]",
        "[text(1,16):a:]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[link-ref-def(3,1):True::ba&beta;r:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<p>a<img src="/url" alt="baβr" title="title" />a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_96a():
    """
    Test case extra 96a:  96 with newline before special characters
    """

    # Arrange
    source_markdown = """a![ba
&beta;r][]a

[ba
&beta;r]: /url 'title'"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):a:]",
        "[image(1,2):collapsed:/url:title:ba\nβr::::ba\n&beta;r:::::]",
        "[text(2,11):a:]",
        "[end-para:::True]",
        "[BLANK(3,1):]",
        "[link-ref-def(4,1):True::ba &beta;r:ba\n&beta;r: :/url:: :title:'title':]",
    ]
    expected_gfm = """<p>a<img src="/url" alt="ba\nβr" title="title" />a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_97x():
    """
    Test case extra 97:  Paragraph with collapsed image with backslash in label
    """

    # Arrange
    source_markdown = """a![ba\\]r][]a

[ba\\]r]: /url 'title'"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        "[image(1,2):collapsed:/url:title:ba]r::::ba\\]r:::::]",
        "[text(1,12):a:]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[link-ref-def(3,1):True::ba\\]r:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<p>a<img src="/url" alt="ba]r" title="title" />a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_97a():
    """
    Test case extra 97a:  97 with newline before special characters
    """

    # Arrange
    source_markdown = """a![ba
\\]r][]a

[ba
\\]r]: /url 'title'"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):a:]",
        "[image(1,2):collapsed:/url:title:ba\n]r::::ba\n\\]r:::::]",
        "[text(2,7):a:]",
        "[end-para:::True]",
        "[BLANK(3,1):]",
        "[link-ref-def(4,1):True::ba \\]r:ba\n\\]r: :/url:: :title:'title':]",
    ]
    expected_gfm = """<p>a<img src="/url" alt="ba\n]r" title="title" />a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_d5():
    """
    Test case extra d5:  Paragraph with link split at the whitespaces
    """

    # Arrange
    source_markdown = """abc
[link](
 /uri
  "title"
   )
  def"""
    expected_tokens = [
        "[para(1,1):\n\n \n  \n   \n  ]",
        "[text(1,1):abc\n::\n]",
        '[link(2,1):inline:/uri:title::::link:False:":\n:\n:\n]',
        "[text(2,2):link:]",
        "[end-link::]",
        "[text(5,5):\ndef::\n]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>abc\n<a href="/uri" title="title">link</a>\ndef</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_d6():
    """
    Test case extra d6:  Paragraph with image split at the whitespaces
    """

    # Arrange
    source_markdown = """abc
![link](
 /uri
  "title"
   )
  def"""
    expected_tokens = [
        "[para(1,1):\n\n \n  \n   \n  ]",
        "[text(1,1):abc\n::\n]",
        '[image(2,1):inline:/uri:title:link::::link:False:":\n:\n:\n]',
        "[text(5,5):\ndef::\n]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>abc\n<img src="/uri" alt="link" title="title" />\ndef</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_e3():
    """
    Test case extra e3:  Inline link inside of inline link
    """

    # Arrange
    source_markdown = """a[foo [bar](/uri)](/uri)a"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        "[text(1,2):[:]",
        "[text(1,3):foo :]",
        "[link(1,7):inline:/uri:::::bar:False::::]",
        "[text(1,8):bar:]",
        "[end-link::]",
        "[text(1,18):]:]",
        "[text(1,19):(/uri)a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a[foo <a href="/uri">bar</a>](/uri)a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_e3a():
    """
    Test case extra e3a:  Inline image inside of inline link
    """

    # Arrange
    source_markdown = """a[foo ![bar](/uri)](/uri)a"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        "[link(1,2):inline:/uri:::::foo ![bar](/uri):False::::]",
        "[text(1,3):foo :]",
        "[image(1,7):inline:/uri::bar::::bar:False::::]",
        "[end-link::]",
        "[text(1,26):a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<a href="/uri">foo <img src="/uri" alt="bar" /></a>a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_e3b():
    """
    Test case extra e3b:  Inline image inside of inline link
    """

    # Arrange
    source_markdown = """a![foo ![bar](/uri)](/uri)a"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        "[image(1,2):inline:/uri::foo bar::::foo ![bar](/uri):False::::]",
        "[text(1,27):a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<img src="/uri" alt="foo bar" />a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_e3c():
    """
    Test case extra e3c:  Inline image inside of inline link
    """

    # Arrange
    source_markdown = """a![foo [bar](/uri)](/uri)a"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        "[image(1,2):inline:/uri::foo bar::::foo [bar](/uri):False::::]",
        "[text(1,26):a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<img src="/uri" alt="foo bar" />a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_e4():
    """
    Test case extra e4:  Full link w/ label matching inside of inline link
    """

    # Arrange
    source_markdown = """a[foo [bar][barx]](/uri)a
    
[bar]: /url 'title'"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        "[link(1,2):inline:/uri:::::foo [bar][barx]:False::::]",
        "[text(1,3):foo :]",
        "[text(1,7):[:]",
        "[text(1,8):bar:]",
        "[text(1,11):]:]",
        "[text(1,12):[:]",
        "[text(1,13):barx:]",
        "[text(1,17):]:]",
        "[end-link::]",
        "[text(1,25):a:]",
        "[end-para:::True]",
        "[BLANK(2,1):    ]",
        "[link-ref-def(3,1):True::bar:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<p>a<a href="/uri">foo [bar][barx]</a>a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_e4a():
    """
    Test case extra e4a:  Full link w/ label matching inside of inline link
    """

    # Arrange
    source_markdown = """a[foo ![bar][barx]](/uri)a
    
[bar]: /url 'title'"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        "[link(1,2):inline:/uri:::::foo ![bar][barx]:False::::]",
        "[text(1,3):foo :]",
        "[text(1,7):![:]",
        "[text(1,9):bar:]",
        "[text(1,12):]:]",
        "[text(1,13):[:]",
        "[text(1,14):barx:]",
        "[text(1,18):]:]",
        "[end-link::]",
        "[text(1,26):a:]",
        "[end-para:::True]",
        "[BLANK(2,1):    ]",
        "[link-ref-def(3,1):True::bar:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<p>a<a href="/uri">foo ![bar][barx]</a>a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_e4b():
    """
    Test case extra e4b:  Full link w/ label matching inside of inline link
    """

    # Arrange
    source_markdown = """a![foo ![bar][barx]](/uri)a
    
[bar]: /url 'title'"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        "[image(1,2):inline:/uri::foo ![bar][barx]::::foo ![bar][barx]:False::::]",
        "[text(1,27):a:]",
        "[end-para:::True]",
        "[BLANK(2,1):    ]",
        "[link-ref-def(3,1):True::bar:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<p>a<img src="/uri" alt="foo ![bar][barx]" />a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_e4c():
    """
    Test case extra e4c:  Full link w/ label matching inside of inline link
    """

    # Arrange
    source_markdown = """a![foo [bar][barx]](/uri)a
    
[bar]: /url 'title'"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        "[image(1,2):inline:/uri::foo [bar][barx]::::foo [bar][barx]:False::::]",
        "[text(1,26):a:]",
        "[end-para:::True]",
        "[BLANK(2,1):    ]",
        "[link-ref-def(3,1):True::bar:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<p>a<img src="/uri" alt="foo [bar][barx]" />a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_e5():
    """
    Test case extra e5:  Full link w/ reference matching inside of inline link
    """

    # Arrange
    source_markdown = """a[foo [barx][bar]](/uri)a
    
[bar]: /url 'title'"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        "[text(1,2):[:]",
        "[text(1,3):foo :]",
        "[link(1,7):full:/url:title:::bar:barx:::::]",
        "[text(1,8):barx:]",
        "[end-link::]",
        "[text(1,18):]:]",
        "[text(1,19):(/uri)a:]",
        "[end-para:::True]",
        "[BLANK(2,1):    ]",
        "[link-ref-def(3,1):True::bar:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<p>a[foo <a href="/url" title="title">barx</a>](/uri)a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_e5a():
    """
    Test case extra e5a:  Full link w/ reference matching inside of inline link
    """

    # Arrange
    source_markdown = """a[foo ![barx][bar]](/uri)a
    
[bar]: /url 'title'"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        "[link(1,2):inline:/uri:::::foo ![barx][bar]:False::::]",
        "[text(1,3):foo :]",
        "[image(1,7):full:/url:title:barx:::bar:barx:::::]",
        "[end-link::]",
        "[text(1,26):a:]",
        "[end-para:::True]",
        "[BLANK(2,1):    ]",
        "[link-ref-def(3,1):True::bar:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<p>a<a href="/uri">foo <img src="/url" alt="barx" title="title" /></a>a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_e5b():
    """
    Test case extra e5b:  Full link w/ reference matching inside of inline link
    """

    # Arrange
    source_markdown = """a![foo ![barx][bar]](/uri)a
    
[bar]: /url 'title'"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        "[image(1,2):inline:/uri::foo barx::::foo ![barx][bar]:False::::]",
        "[text(1,27):a:]",
        "[end-para:::True]",
        "[BLANK(2,1):    ]",
        "[link-ref-def(3,1):True::bar:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<p>a<img src="/uri" alt="foo barx" />a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_e5c():
    """
    Test case extra e5c:  Full link w/ reference matching inside of inline link
    """

    # Arrange
    source_markdown = """a![foo [barx][bar]](/uri)a
    
[bar]: /url 'title'"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        "[image(1,2):inline:/uri::foo barx::::foo [barx][bar]:False::::]",
        "[text(1,26):a:]",
        "[end-para:::True]",
        "[BLANK(2,1):    ]",
        "[link-ref-def(3,1):True::bar:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<p>a<img src="/uri" alt="foo barx" />a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_e6():
    """
    Test case extra e6:  Collapsed link inside of inline link
    """

    # Arrange
    source_markdown = """a[foo [bar][]](/uri)a
    
[bar]: /url 'title'"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        "[text(1,2):[:]",
        "[text(1,3):foo :]",
        "[link(1,7):collapsed:/url:title::::bar:::::]",
        "[text(1,8):bar:]",
        "[end-link::]",
        "[text(1,14):]:]",
        "[text(1,15):(/uri)a:]",
        "[end-para:::True]",
        "[BLANK(2,1):    ]",
        "[link-ref-def(3,1):True::bar:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<p>a[foo <a href="/url" title="title">bar</a>](/uri)a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_e6a():
    """
    Test case extra e6a:  Collapsed link inside of inline link
    """

    # Arrange
    source_markdown = """a[foo ![bar][]](/uri)a
    
[bar]: /url 'title'"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        "[link(1,2):inline:/uri:::::foo ![bar][]:False::::]",
        "[text(1,3):foo :]",
        "[image(1,7):collapsed:/url:title:bar::::bar:::::]",
        "[end-link::]",
        "[text(1,22):a:]",
        "[end-para:::True]",
        "[BLANK(2,1):    ]",
        "[link-ref-def(3,1):True::bar:: :/url:: :title:'title':]",
    ]
    expected_gfm = (
        """<p>a<a href="/uri">foo <img src="/url" alt="bar" title="title" /></a>a</p>"""
    )

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_e6b():
    """
    Test case extra e6b:  Collapsed link inside of inline link
    """

    # Arrange
    source_markdown = """a![foo ![bar][]](/uri)a
    
[bar]: /url 'title'"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        "[image(1,2):inline:/uri::foo bar::::foo ![bar][]:False::::]",
        "[text(1,23):a:]",
        "[end-para:::True]",
        "[BLANK(2,1):    ]",
        "[link-ref-def(3,1):True::bar:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<p>a<img src="/uri" alt="foo bar" />a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_e6c():
    """
    Test case extra e6c:  Collapsed link inside of inline link
    """

    # Arrange
    source_markdown = """a![foo [bar][]](/uri)a
    
[bar]: /url 'title'"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        "[image(1,2):inline:/uri::foo bar::::foo [bar][]:False::::]",
        "[text(1,22):a:]",
        "[end-para:::True]",
        "[BLANK(2,1):    ]",
        "[link-ref-def(3,1):True::bar:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<p>a<img src="/uri" alt="foo bar" />a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_e7():
    """
    Test case extra e7:  Collapsed link inside of inline link
    """

    # Arrange
    source_markdown = """a[foo [barx][]](/uri)a
    
[bar]: /url 'title'"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        "[link(1,2):inline:/uri:::::foo [barx][]:False::::]",
        "[text(1,3):foo :]",
        "[text(1,7):[:]",
        "[text(1,8):barx:]",
        "[text(1,12):]:]",
        "[text(1,13):[:]",
        "[text(1,14):]:]",
        "[end-link::]",
        "[text(1,22):a:]",
        "[end-para:::True]",
        "[BLANK(2,1):    ]",
        "[link-ref-def(3,1):True::bar:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<p>a<a href="/uri">foo [barx][]</a>a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_e7a():
    """
    Test case extra e7a:  Collapsed link inside of inline link
    """

    # Arrange
    source_markdown = """a[foo ![barx][]](/uri)a
    
[bar]: /url 'title'"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        "[link(1,2):inline:/uri:::::foo ![barx][]:False::::]",
        "[text(1,3):foo :]",
        "[text(1,7):![:]",
        "[text(1,9):barx:]",
        "[text(1,13):]:]",
        "[text(1,14):[:]",
        "[text(1,15):]:]",
        "[end-link::]",
        "[text(1,23):a:]",
        "[end-para:::True]",
        "[BLANK(2,1):    ]",
        "[link-ref-def(3,1):True::bar:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<p>a<a href="/uri">foo ![barx][]</a>a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_e7b():
    """
    Test case extra e7b:  Collapsed link inside of inline link
    """

    # Arrange
    source_markdown = """a![foo ![barx][]](/uri)a
    
[bar]: /url 'title'"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        "[image(1,2):inline:/uri::foo ![barx][]::::foo ![barx][]:False::::]",
        "[text(1,24):a:]",
        "[end-para:::True]",
        "[BLANK(2,1):    ]",
        "[link-ref-def(3,1):True::bar:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<p>a<img src="/uri" alt="foo ![barx][]" />a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_e7c():
    """
    Test case extra e7c:  Collapsed link inside of inline link
    """

    # Arrange
    source_markdown = """a![foo [barx][]](/uri)a
    
[bar]: /url 'title'"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        "[image(1,2):inline:/uri::foo [barx][]::::foo [barx][]:False::::]",
        "[text(1,23):a:]",
        "[end-para:::True]",
        "[BLANK(2,1):    ]",
        "[link-ref-def(3,1):True::bar:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<p>a<img src="/uri" alt="foo [barx][]" />a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_e8():
    """
    Test case extra e8:  Shortcut link inside of inline link
    """

    # Arrange
    source_markdown = """a[foo [bar]](/uri)a
    
[bar]: /url 'title'"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        "[text(1,2):[:]",
        "[text(1,3):foo :]",
        "[link(1,7):shortcut:/url:title::::bar:::::]",
        "[text(1,8):bar:]",
        "[end-link::]",
        "[text(1,12):]:]",
        "[text(1,13):(/uri)a:]",
        "[end-para:::True]",
        "[BLANK(2,1):    ]",
        "[link-ref-def(3,1):True::bar:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<p>a[foo <a href="/url" title="title">bar</a>](/uri)a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_e8a():
    """
    Test case extra e8a:  Shortcut link inside of inline link
    """

    # Arrange
    source_markdown = """a[foo ![bar]](/uri)a
    
[bar]: /url 'title'"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        "[link(1,2):inline:/uri:::::foo ![bar]:False::::]",
        "[text(1,3):foo :]",
        "[image(1,7):shortcut:/url:title:bar::::bar:::::]",
        "[end-link::]",
        "[text(1,20):a:]",
        "[end-para:::True]",
        "[BLANK(2,1):    ]",
        "[link-ref-def(3,1):True::bar:: :/url:: :title:'title':]",
    ]
    expected_gfm = (
        """<p>a<a href="/uri">foo <img src="/url" alt="bar" title="title" /></a>a</p>"""
    )

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_e8b():
    """
    Test case extra e8b:  Shortcut link inside of inline link
    """

    # Arrange
    source_markdown = """a![foo ![bar]](/uri)a
    
[bar]: /url 'title'"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        "[image(1,2):inline:/uri::foo bar::::foo ![bar]:False::::]",
        "[text(1,21):a:]",
        "[end-para:::True]",
        "[BLANK(2,1):    ]",
        "[link-ref-def(3,1):True::bar:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<p>a<img src="/uri" alt="foo bar" />a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_e8c():
    """
    Test case extra e8c:  Shortcut link inside of inline link
    """

    # Arrange
    source_markdown = """a![foo [bar]](/uri)a
    
[bar]: /url 'title'"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        "[image(1,2):inline:/uri::foo bar::::foo [bar]:False::::]",
        "[text(1,20):a:]",
        "[end-para:::True]",
        "[BLANK(2,1):    ]",
        "[link-ref-def(3,1):True::bar:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<p>a<img src="/uri" alt="foo bar" />a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_e9():
    """
    Test case extra e9:  Shortcut link inside of inline link
    """

    # Arrange
    source_markdown = """a[foo [barx]](/uri)a
    
[bar]: /url 'title'"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        "[link(1,2):inline:/uri:::::foo [barx]:False::::]",
        "[text(1,3):foo :]",
        "[text(1,7):[:]",
        "[text(1,8):barx:]",
        "[text(1,12):]:]",
        "[end-link::]",
        "[text(1,20):a:]",
        "[end-para:::True]",
        "[BLANK(2,1):    ]",
        "[link-ref-def(3,1):True::bar:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<p>a<a href="/uri">foo [barx]</a>a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_e9a():
    """
    Test case extra e9a:  Shortcut link inside of inline link
    """

    # Arrange
    source_markdown = """a[foo ![barx]](/uri)a
    
[bar]: /url 'title'"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        "[link(1,2):inline:/uri:::::foo ![barx]:False::::]",
        "[text(1,3):foo :]",
        "[text(1,7):![:]",
        "[text(1,9):barx:]",
        "[text(1,13):]:]",
        "[end-link::]",
        "[text(1,21):a:]",
        "[end-para:::True]",
        "[BLANK(2,1):    ]",
        "[link-ref-def(3,1):True::bar:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<p>a<a href="/uri">foo ![barx]</a>a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_e9b():
    """
    Test case extra e9b:  Shortcut link inside of inline link
    """

    # Arrange
    source_markdown = """a![foo ![barx]](/uri)a
    
[bar]: /url 'title'"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        "[image(1,2):inline:/uri::foo ![barx]::::foo ![barx]:False::::]",
        "[text(1,22):a:]",
        "[end-para:::True]",
        "[BLANK(2,1):    ]",
        "[link-ref-def(3,1):True::bar:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<p>a<img src="/uri" alt="foo ![barx]" />a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_e9c():
    """
    Test case extra e9c:  Shortcut link inside of inline link
    """

    # Arrange
    source_markdown = """a![foo [barx]](/uri)a
    
[bar]: /url 'title'"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        "[image(1,2):inline:/uri::foo [barx]::::foo [barx]:False::::]",
        "[text(1,21):a:]",
        "[end-para:::True]",
        "[BLANK(2,1):    ]",
        "[link-ref-def(3,1):True::bar:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<p>a<img src="/uri" alt="foo [barx]" />a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_f0():
    """
    Test case extra f0:  Inline link inside of full link
    """

    # Arrange
    source_markdown = """a[foo [bar2](/url2)][bar]a
    
[bar]: /url 'title'"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        "[text(1,2):[:]",
        "[text(1,3):foo :]",
        "[link(1,7):inline:/url2:::::bar2:False::::]",
        "[text(1,8):bar2:]",
        "[end-link::]",
        "[text(1,20):]:]",
        "[link(1,21):shortcut:/url:title::::bar:::::]",
        "[text(1,22):bar:]",
        "[end-link::]",
        "[text(1,26):a:]",
        "[end-para:::True]",
        "[BLANK(2,1):    ]",
        "[link-ref-def(3,1):True::bar:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<p>a[foo <a href="/url2">bar2</a>]<a href="/url" title="title">bar</a>a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_f0a():
    """
    Test case extra f0a:  Inline link inside of full link
    """

    # Arrange
    source_markdown = """a[foo ![bar2](/url2)][bar]a
    
[bar]: /url 'title'"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        "[link(1,2):full:/url:title:::bar:foo ![bar2](/url2):::::]",
        "[text(1,3):foo :]",
        "[image(1,7):inline:/url2::bar2::::bar2:False::::]",
        "[end-link::]",
        "[text(1,27):a:]",
        "[end-para:::True]",
        "[BLANK(2,1):    ]",
        "[link-ref-def(3,1):True::bar:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<p>a<a href="/url" title="title">foo <img src="/url2" alt="bar2" /></a>a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_f0b():
    """
    Test case extra f0b:  Inline link inside of full link
    """

    # Arrange
    source_markdown = """a![foo ![bar2](/url2)][bar]a
    
[bar]: /url 'title'"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        "[image(1,2):full:/url:title:foo bar2:::bar:foo ![bar2](/url2):::::]",
        "[text(1,28):a:]",
        "[end-para:::True]",
        "[BLANK(2,1):    ]",
        "[link-ref-def(3,1):True::bar:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<p>a<img src="/url" alt="foo bar2" title="title" />a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_f0c():
    """
    Test case extra f0c:  Inline link inside of full link
    """

    # Arrange
    source_markdown = """a![foo [bar2](/url2)][bar]a
    
[bar]: /url 'title'"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        "[image(1,2):full:/url:title:foo bar2:::bar:foo [bar2](/url2):::::]",
        "[text(1,27):a:]",
        "[end-para:::True]",
        "[BLANK(2,1):    ]",
        "[link-ref-def(3,1):True::bar:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<p>a<img src="/url" alt="foo bar2" title="title" />a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_f1():
    """
    Test case extra f1:  Full link inside of full link
    """

    # Arrange
    source_markdown = """a[foo [bar2][bar]][bar]a
    
[bar]: /url 'title'"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        "[text(1,2):[:]",
        "[text(1,3):foo :]",
        "[link(1,7):full:/url:title:::bar:bar2:::::]",
        "[text(1,8):bar2:]",
        "[end-link::]",
        "[text(1,18):]:]",
        "[link(1,19):shortcut:/url:title::::bar:::::]",
        "[text(1,20):bar:]",
        "[end-link::]",
        "[text(1,24):a:]",
        "[end-para:::True]",
        "[BLANK(2,1):    ]",
        "[link-ref-def(3,1):True::bar:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<p>a[foo <a href="/url" title="title">bar2</a>]<a href="/url" title="title">bar</a>a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_f1a():
    """
    Test case extra f1a:  Full link inside of full link
    """

    # Arrange
    source_markdown = """a[foo ![bar2][bar]][bar]a
    
[bar]: /url 'title'"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        "[link(1,2):full:/url:title:::bar:foo ![bar2][bar]:::::]",
        "[text(1,3):foo :]",
        "[image(1,7):full:/url:title:bar2:::bar:bar2:::::]",
        "[end-link::]",
        "[text(1,25):a:]",
        "[end-para:::True]",
        "[BLANK(2,1):    ]",
        "[link-ref-def(3,1):True::bar:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<p>a<a href="/url" title="title">foo <img src="/url" alt="bar2" title="title" /></a>a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_f1b():
    """
    Test case extra f1b:  Full link inside of full link
    """

    # Arrange
    source_markdown = """a![foo ![bar2][bar]][bar]a
    
[bar]: /url 'title'"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        "[image(1,2):full:/url:title:foo bar2:::bar:foo ![bar2][bar]:::::]",
        "[text(1,26):a:]",
        "[end-para:::True]",
        "[BLANK(2,1):    ]",
        "[link-ref-def(3,1):True::bar:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<p>a<img src="/url" alt="foo bar2" title="title" />a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_f1c():
    """
    Test case extra f1c:  Full link inside of full link
    """

    # Arrange
    source_markdown = """a![foo [bar2][bar]][bar]a
    
[bar]: /url 'title'"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        "[image(1,2):full:/url:title:foo bar2:::bar:foo [bar2][bar]:::::]",
        "[text(1,25):a:]",
        "[end-para:::True]",
        "[BLANK(2,1):    ]",
        "[link-ref-def(3,1):True::bar:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<p>a<img src="/url" alt="foo bar2" title="title" />a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_f2():
    """
    Test case extra f2:  Full link inside of full link
    """

    # Arrange
    source_markdown = """a[foo [bar][bar2]][bar]a
    
[bar]: /url 'title'"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        "[link(1,2):full:/url:title:::bar:foo [bar][bar2]:::::]",
        "[text(1,3):foo :]",
        "[text(1,7):[:]",
        "[text(1,8):bar:]",
        "[text(1,11):]:]",
        "[text(1,12):[:]",
        "[text(1,13):bar2:]",
        "[text(1,17):]:]",
        "[end-link::]",
        "[text(1,24):a:]",
        "[end-para:::True]",
        "[BLANK(2,1):    ]",
        "[link-ref-def(3,1):True::bar:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<p>a<a href="/url" title="title">foo [bar][bar2]</a>a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_f2a():
    """
    Test case extra f2a:  Full link inside of full link
    """

    # Arrange
    source_markdown = """a[foo ![bar][bar2]][bar]a
    
[bar]: /url 'title'"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        "[link(1,2):full:/url:title:::bar:foo ![bar][bar2]:::::]",
        "[text(1,3):foo :]",
        "[text(1,7):![:]",
        "[text(1,9):bar:]",
        "[text(1,12):]:]",
        "[text(1,13):[:]",
        "[text(1,14):bar2:]",
        "[text(1,18):]:]",
        "[end-link::]",
        "[text(1,25):a:]",
        "[end-para:::True]",
        "[BLANK(2,1):    ]",
        "[link-ref-def(3,1):True::bar:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<p>a<a href="/url" title="title">foo ![bar][bar2]</a>a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_f2b():
    """
    Test case extra f2b:  Full link inside of full link
    """

    # Arrange
    source_markdown = """a![foo ![bar][bar2]][bar]a
    
[bar]: /url 'title'"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        "[image(1,2):full:/url:title:foo ![bar][bar2]:::bar:foo ![bar][bar2]:::::]",
        "[text(1,26):a:]",
        "[end-para:::True]",
        "[BLANK(2,1):    ]",
        "[link-ref-def(3,1):True::bar:: :/url:: :title:'title':]",
    ]
    expected_gfm = (
        """<p>a<img src="/url" alt="foo ![bar][bar2]" title="title" />a</p>"""
    )

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_f2c():
    """
    Test case extra f2c:  Full link inside of full link
    """

    # Arrange
    source_markdown = """a![foo [bar][bar2]][bar]a
    
[bar]: /url 'title'"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        "[image(1,2):full:/url:title:foo [bar][bar2]:::bar:foo [bar][bar2]:::::]",
        "[text(1,25):a:]",
        "[end-para:::True]",
        "[BLANK(2,1):    ]",
        "[link-ref-def(3,1):True::bar:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<p>a<img src="/url" alt="foo [bar][bar2]" title="title" />a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_f3():
    """
    Test case extra f3:  Collapsed link inside of full link
    """

    # Arrange
    source_markdown = """a[foo [bar2][]][bar]a
    
[bar]: /url 'title'"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        "[link(1,2):full:/url:title:::bar:foo [bar2][]:::::]",
        "[text(1,3):foo :]",
        "[text(1,7):[:]",
        "[text(1,8):bar2:]",
        "[text(1,12):]:]",
        "[text(1,13):[:]",
        "[text(1,14):]:]",
        "[end-link::]",
        "[text(1,21):a:]",
        "[end-para:::True]",
        "[BLANK(2,1):    ]",
        "[link-ref-def(3,1):True::bar:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<p>a<a href="/url" title="title">foo [bar2][]</a>a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_f3a():
    """
    Test case extra f3a:  Collapsed link inside of full link
    """

    # Arrange
    source_markdown = """a[foo ![bar2][]][bar]a
    
[bar]: /url 'title'"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        "[link(1,2):full:/url:title:::bar:foo ![bar2][]:::::]",
        "[text(1,3):foo :]",
        "[text(1,7):![:]",
        "[text(1,9):bar2:]",
        "[text(1,13):]:]",
        "[text(1,14):[:]",
        "[text(1,15):]:]",
        "[end-link::]",
        "[text(1,22):a:]",
        "[end-para:::True]",
        "[BLANK(2,1):    ]",
        "[link-ref-def(3,1):True::bar:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<p>a<a href="/url" title="title">foo ![bar2][]</a>a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_f3b():
    """
    Test case extra f3b:  Collapsed link inside of full link
    """

    # Arrange
    source_markdown = """a![foo ![bar2][]][bar]a
    
[bar]: /url 'title'"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        "[image(1,2):full:/url:title:foo ![bar2][]:::bar:foo ![bar2][]:::::]",
        "[text(1,23):a:]",
        "[end-para:::True]",
        "[BLANK(2,1):    ]",
        "[link-ref-def(3,1):True::bar:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<p>a<img src="/url" alt="foo ![bar2][]" title="title" />a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_f3c():
    """
    Test case extra f3c:  Collapsed link inside of full link
    """

    # Arrange
    source_markdown = """a![foo [bar2][]][bar]a
    
[bar]: /url 'title'"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        "[image(1,2):full:/url:title:foo [bar2][]:::bar:foo [bar2][]:::::]",
        "[text(1,22):a:]",
        "[end-para:::True]",
        "[BLANK(2,1):    ]",
        "[link-ref-def(3,1):True::bar:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<p>a<img src="/url" alt="foo [bar2][]" title="title" />a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_f4():
    """
    Test case extra f4:  Collapsed link inside of full link
    """

    # Arrange
    source_markdown = """a[foo [bar][]][bar]a
    
[bar]: /url 'title'"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        "[text(1,2):[:]",
        "[text(1,3):foo :]",
        "[link(1,7):collapsed:/url:title::::bar:::::]",
        "[text(1,8):bar:]",
        "[end-link::]",
        "[text(1,14):]:]",
        "[link(1,15):shortcut:/url:title::::bar:::::]",
        "[text(1,16):bar:]",
        "[end-link::]",
        "[text(1,20):a:]",
        "[end-para:::True]",
        "[BLANK(2,1):    ]",
        "[link-ref-def(3,1):True::bar:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<p>a[foo <a href="/url" title="title">bar</a>]<a href="/url" title="title">bar</a>a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_f4a():
    """
    Test case extra f4a:  Collapsed link inside of full link
    """

    # Arrange
    source_markdown = """a[foo ![bar][]][bar]a
    
[bar]: /url 'title'"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        "[link(1,2):full:/url:title:::bar:foo ![bar][]:::::]",
        "[text(1,3):foo :]",
        "[image(1,7):collapsed:/url:title:bar::::bar:::::]",
        "[end-link::]",
        "[text(1,21):a:]",
        "[end-para:::True]",
        "[BLANK(2,1):    ]",
        "[link-ref-def(3,1):True::bar:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<p>a<a href="/url" title="title">foo <img src="/url" alt="bar" title="title" /></a>a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_f4b():
    """
    Test case extra f4b:  Collapsed link inside of full link
    """

    # Arrange
    source_markdown = """a![foo ![bar][]][bar]a
    
[bar]: /url 'title'"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        "[image(1,2):full:/url:title:foo bar:::bar:foo ![bar][]:::::]",
        "[text(1,22):a:]",
        "[end-para:::True]",
        "[BLANK(2,1):    ]",
        "[link-ref-def(3,1):True::bar:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<p>a<img src="/url" alt="foo bar" title="title" />a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_f4c():
    """
    Test case extra f4c:  Collapsed link inside of full link
    """

    # Arrange
    source_markdown = """a![foo [bar][]][bar]a
    
[bar]: /url 'title'"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        "[image(1,2):full:/url:title:foo bar:::bar:foo [bar][]:::::]",
        "[text(1,21):a:]",
        "[end-para:::True]",
        "[BLANK(2,1):    ]",
        "[link-ref-def(3,1):True::bar:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<p>a<img src="/url" alt="foo bar" title="title" />a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_f5():
    """
    Test case extra f5:  Shortcut link inside of full link
    """

    # Arrange
    source_markdown = """a[foo [bar2]][bar]a
    
[bar]: /url 'title'"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        "[link(1,2):full:/url:title:::bar:foo [bar2]:::::]",
        "[text(1,3):foo :]",
        "[text(1,7):[:]",
        "[text(1,8):bar2:]",
        "[text(1,12):]:]",
        "[end-link::]",
        "[text(1,19):a:]",
        "[end-para:::True]",
        "[BLANK(2,1):    ]",
        "[link-ref-def(3,1):True::bar:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<p>a<a href="/url" title="title">foo [bar2]</a>a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_f5a():
    """
    Test case extra f5a:  Shortcut link inside of full link
    """

    # Arrange
    source_markdown = """a[foo ![bar2]][bar]a
    
[bar]: /url 'title'"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        "[link(1,2):full:/url:title:::bar:foo ![bar2]:::::]",
        "[text(1,3):foo :]",
        "[text(1,7):![:]",
        "[text(1,9):bar2:]",
        "[text(1,13):]:]",
        "[end-link::]",
        "[text(1,20):a:]",
        "[end-para:::True]",
        "[BLANK(2,1):    ]",
        "[link-ref-def(3,1):True::bar:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<p>a<a href="/url" title="title">foo ![bar2]</a>a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_f5b():
    """
    Test case extra f5b:  Shortcut link inside of full link
    """

    # Arrange
    source_markdown = """a![foo ![bar2]][bar]a
    
[bar]: /url 'title'"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        "[image(1,2):full:/url:title:foo ![bar2]:::bar:foo ![bar2]:::::]",
        "[text(1,21):a:]",
        "[end-para:::True]",
        "[BLANK(2,1):    ]",
        "[link-ref-def(3,1):True::bar:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<p>a<img src="/url" alt="foo ![bar2]" title="title" />a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_f5c():
    """
    Test case extra f5c:  Shortcut link inside of full link
    """

    # Arrange
    source_markdown = """a![foo [bar2]][bar]a
    
[bar]: /url 'title'"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        "[image(1,2):full:/url:title:foo [bar2]:::bar:foo [bar2]:::::]",
        "[text(1,20):a:]",
        "[end-para:::True]",
        "[BLANK(2,1):    ]",
        "[link-ref-def(3,1):True::bar:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<p>a<img src="/url" alt="foo [bar2]" title="title" />a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_f6():
    """
    Test case extra f6:  Shortcut link inside of full link
    """

    # Arrange
    source_markdown = """a[foo [bar]][bar]a
    
[bar]: /url 'title'"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        "[text(1,2):[:]",
        "[text(1,3):foo :]",
        "[link(1,7):shortcut:/url:title::::bar:::::]",
        "[text(1,8):bar:]",
        "[end-link::]",
        "[text(1,12):]:]",
        "[link(1,13):shortcut:/url:title::::bar:::::]",
        "[text(1,14):bar:]",
        "[end-link::]",
        "[text(1,18):a:]",
        "[end-para:::True]",
        "[BLANK(2,1):    ]",
        "[link-ref-def(3,1):True::bar:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<p>a[foo <a href="/url" title="title">bar</a>]<a href="/url" title="title">bar</a>a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_f6a():
    """
    Test case extra f6a:  Shortcut link inside of full link
    """

    # Arrange
    source_markdown = """a[foo ![bar]][bar]a
    
[bar]: /url 'title'"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        "[link(1,2):full:/url:title:::bar:foo ![bar]:::::]",
        "[text(1,3):foo :]",
        "[image(1,7):shortcut:/url:title:bar::::bar:::::]",
        "[end-link::]",
        "[text(1,19):a:]",
        "[end-para:::True]",
        "[BLANK(2,1):    ]",
        "[link-ref-def(3,1):True::bar:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<p>a<a href="/url" title="title">foo <img src="/url" alt="bar" title="title" /></a>a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_f6b():
    """
    Test case extra f6b:  Shortcut link inside of full link
    """

    # Arrange
    source_markdown = """a![foo ![bar]][bar]a
    
[bar]: /url 'title'"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        "[image(1,2):full:/url:title:foo bar:::bar:foo ![bar]:::::]",
        "[text(1,20):a:]",
        "[end-para:::True]",
        "[BLANK(2,1):    ]",
        "[link-ref-def(3,1):True::bar:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<p>a<img src="/url" alt="foo bar" title="title" />a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_f6c():
    """
    Test case extra f6c:  Shortcut link inside of full link
    """

    # Arrange
    source_markdown = """a![foo [bar]][bar]a
    
[bar]: /url 'title'"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        "[image(1,2):full:/url:title:foo bar:::bar:foo [bar]:::::]",
        "[text(1,19):a:]",
        "[end-para:::True]",
        "[BLANK(2,1):    ]",
        "[link-ref-def(3,1):True::bar:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<p>a<img src="/url" alt="foo bar" title="title" />a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_f7():
    """
    Test case extra f7:  Inline link inside of collapsed link
    """

    # Arrange
    source_markdown = """a[foo [bar2](/url2)][]a
    
[bar]: /url 'title'"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        "[text(1,2):[:]",
        "[text(1,3):foo :]",
        "[link(1,7):inline:/url2:::::bar2:False::::]",
        "[text(1,8):bar2:]",
        "[end-link::]",
        "[text(1,20):]:]",
        "[text(1,21):[:]",
        "[text(1,22):]:]",
        "[text(1,23):a:]",
        "[end-para:::True]",
        "[BLANK(2,1):    ]",
        "[link-ref-def(3,1):True::bar:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<p>a[foo <a href="/url2">bar2</a>][]a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_f7a():
    """
    Test case extra f7a:  Inline link inside of collapsed link
    """

    # Arrange
    source_markdown = """a[foo ![bar2](/url2)][]a
    
[bar]: /url 'title'"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        "[text(1,2):[:]",
        "[text(1,3):foo :]",
        "[image(1,7):inline:/url2::bar2::::bar2:False::::]",
        "[text(1,21):]:]",
        "[text(1,22):[:]",
        "[text(1,23):]:]",
        "[text(1,24):a:]",
        "[end-para:::True]",
        "[BLANK(2,1):    ]",
        "[link-ref-def(3,1):True::bar:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<p>a[foo <img src="/url2" alt="bar2" />][]a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_f7b():
    """
    Test case extra f7b:  Inline link inside of collapsed link
    """

    # Arrange
    source_markdown = """a![foo ![bar2](/url2)][]a
    
[bar]: /url 'title'"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        "[text(1,2):![:]",
        "[text(1,4):foo :]",
        "[image(1,8):inline:/url2::bar2::::bar2:False::::]",
        "[text(1,22):]:]",
        "[text(1,23):[:]",
        "[text(1,24):]:]",
        "[text(1,25):a:]",
        "[end-para:::True]",
        "[BLANK(2,1):    ]",
        "[link-ref-def(3,1):True::bar:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<p>a![foo <img src="/url2" alt="bar2" />][]a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_f7c():
    """
    Test case extra f7c:  Inline link inside of collapsed link
    """

    # Arrange
    source_markdown = """a![foo [bar2](/url2)][]a
    
[bar]: /url 'title'"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        "[text(1,2):![:]",
        "[text(1,4):foo :]",
        "[link(1,8):inline:/url2:::::bar2:False::::]",
        "[text(1,9):bar2:]",
        "[end-link::]",
        "[text(1,21):]:]",
        "[text(1,22):[:]",
        "[text(1,23):]:]",
        "[text(1,24):a:]",
        "[end-para:::True]",
        "[BLANK(2,1):    ]",
        "[link-ref-def(3,1):True::bar:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<p>a![foo <a href="/url2">bar2</a>][]a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_f8():
    """
    Test case extra f8:  Inline link inside of collapsed link
    """

    # Arrange
    source_markdown = """a[foo [bar](/url2)][]a
    
[bar]: /url 'title'"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        "[text(1,2):[:]",
        "[text(1,3):foo :]",
        "[link(1,7):inline:/url2:::::bar:False::::]",
        "[text(1,8):bar:]",
        "[end-link::]",
        "[text(1,19):]:]",
        "[text(1,20):[:]",
        "[text(1,21):]:]",
        "[text(1,22):a:]",
        "[end-para:::True]",
        "[BLANK(2,1):    ]",
        "[link-ref-def(3,1):True::bar:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<p>a[foo <a href="/url2">bar</a>][]a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_f8a():
    """
    Test case extra f8a:  Inline link inside of collapsed link
    """

    # Arrange
    source_markdown = """a[foo ![bar](/url2)][]a
    
[bar]: /url 'title'"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        "[text(1,2):[:]",
        "[text(1,3):foo :]",
        "[image(1,7):inline:/url2::bar::::bar:False::::]",
        "[text(1,20):]:]",
        "[text(1,21):[:]",
        "[text(1,22):]:]",
        "[text(1,23):a:]",
        "[end-para:::True]",
        "[BLANK(2,1):    ]",
        "[link-ref-def(3,1):True::bar:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<p>a[foo <img src="/url2" alt="bar" />][]a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_f8b():
    """
    Test case extra f8b:  Inline link inside of collapsed link
    """

    # Arrange
    source_markdown = """a![foo ![bar](/url2)][]a
    
[bar]: /url 'title'"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        "[text(1,2):![:]",
        "[text(1,4):foo :]",
        "[image(1,8):inline:/url2::bar::::bar:False::::]",
        "[text(1,21):]:]",
        "[text(1,22):[:]",
        "[text(1,23):]:]",
        "[text(1,24):a:]",
        "[end-para:::True]",
        "[BLANK(2,1):    ]",
        "[link-ref-def(3,1):True::bar:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<p>a![foo <img src="/url2" alt="bar" />][]a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_f8c():
    """
    Test case extra f8c:  Inline link inside of collapsed link
    """

    # Arrange
    source_markdown = """a![foo [bar](/url2)][]a
    
[bar]: /url 'title'"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        "[text(1,2):![:]",
        "[text(1,4):foo :]",
        "[link(1,8):inline:/url2:::::bar:False::::]",
        "[text(1,9):bar:]",
        "[end-link::]",
        "[text(1,20):]:]",
        "[text(1,21):[:]",
        "[text(1,22):]:]",
        "[text(1,23):a:]",
        "[end-para:::True]",
        "[BLANK(2,1):    ]",
        "[link-ref-def(3,1):True::bar:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<p>a![foo <a href="/url2">bar</a>][]a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_f9():
    """
    Test case extra f9:  Full link inside of collapsed link
    """

    # Arrange
    source_markdown = """a[foo [bar2][bar]][]a
    
[bar]: /url 'title'"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        "[text(1,2):[:]",
        "[text(1,3):foo :]",
        "[link(1,7):full:/url:title:::bar:bar2:::::]",
        "[text(1,8):bar2:]",
        "[end-link::]",
        "[text(1,18):]:]",
        "[text(1,19):[:]",
        "[text(1,20):]:]",
        "[text(1,21):a:]",
        "[end-para:::True]",
        "[BLANK(2,1):    ]",
        "[link-ref-def(3,1):True::bar:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<p>a[foo <a href="/url" title="title">bar2</a>][]a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_f9a():
    """
    Test case extra f9a:  Full link inside of collapsed link
    """

    # Arrange
    source_markdown = """a[foo ![bar2][bar]][]a
    
[bar]: /url 'title'"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        "[text(1,2):[:]",
        "[text(1,3):foo :]",
        "[image(1,7):full:/url:title:bar2:::bar:bar2:::::]",
        "[text(1,19):]:]",
        "[text(1,20):[:]",
        "[text(1,21):]:]",
        "[text(1,22):a:]",
        "[end-para:::True]",
        "[BLANK(2,1):    ]",
        "[link-ref-def(3,1):True::bar:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<p>a[foo <img src="/url" alt="bar2" title="title" />][]a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_f9b():
    """
    Test case extra f9b:  Full link inside of collapsed link
    """

    # Arrange
    source_markdown = """a![foo ![bar2][bar]][]a
    
[bar]: /url 'title'"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        "[text(1,2):![:]",
        "[text(1,4):foo :]",
        "[image(1,8):full:/url:title:bar2:::bar:bar2:::::]",
        "[text(1,20):]:]",
        "[text(1,21):[:]",
        "[text(1,22):]:]",
        "[text(1,23):a:]",
        "[end-para:::True]",
        "[BLANK(2,1):    ]",
        "[link-ref-def(3,1):True::bar:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<p>a![foo <img src="/url" alt="bar2" title="title" />][]a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_f9c():
    """
    Test case extra f9c:  Full link inside of collapsed link
    """

    # Arrange
    source_markdown = """a![foo [bar2][bar]][]a
    
[bar]: /url 'title'"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        "[text(1,2):![:]",
        "[text(1,4):foo :]",
        "[link(1,8):full:/url:title:::bar:bar2:::::]",
        "[text(1,9):bar2:]",
        "[end-link::]",
        "[text(1,19):]:]",
        "[text(1,20):[:]",
        "[text(1,21):]:]",
        "[text(1,22):a:]",
        "[end-para:::True]",
        "[BLANK(2,1):    ]",
        "[link-ref-def(3,1):True::bar:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<p>a![foo <a href="/url" title="title">bar2</a>][]a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_g0():
    """
    Test case extra g0:  Full link inside of collapsed link
    """

    # Arrange
    source_markdown = """a[foo [bar2][bar3]][]a
    
[bar]: /url 'title'"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        "[text(1,2):[:]",
        "[text(1,3):foo :]",
        "[text(1,7):[:]",
        "[text(1,8):bar2:]",
        "[text(1,12):]:]",
        "[text(1,13):[:]",
        "[text(1,14):bar3:]",
        "[text(1,18):]:]",
        "[text(1,19):]:]",
        "[text(1,20):[:]",
        "[text(1,21):]:]",
        "[text(1,22):a:]",
        "[end-para:::True]",
        "[BLANK(2,1):    ]",
        "[link-ref-def(3,1):True::bar:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<p>a[foo [bar2][bar3]][]a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_g0a():
    """
    Test case extra g0a:  Full link inside of collapsed link
    """

    # Arrange
    source_markdown = """a[foo ![bar2][bar3]][]a
    
[bar]: /url 'title'"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        "[text(1,2):[:]",
        "[text(1,3):foo :]",
        "[text(1,7):![:]",
        "[text(1,9):bar2:]",
        "[text(1,13):]:]",
        "[text(1,14):[:]",
        "[text(1,15):bar3:]",
        "[text(1,19):]:]",
        "[text(1,20):]:]",
        "[text(1,21):[:]",
        "[text(1,22):]:]",
        "[text(1,23):a:]",
        "[end-para:::True]",
        "[BLANK(2,1):    ]",
        "[link-ref-def(3,1):True::bar:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<p>a[foo ![bar2][bar3]][]a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_g0b():
    """
    Test case extra g0b:  Full link inside of collapsed link
    """

    # Arrange
    source_markdown = """a![foo ![bar2][bar3]][]a
    
[bar]: /url 'title'"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        "[text(1,2):![:]",
        "[text(1,4):foo :]",
        "[text(1,8):![:]",
        "[text(1,10):bar2:]",
        "[text(1,14):]:]",
        "[text(1,15):[:]",
        "[text(1,16):bar3:]",
        "[text(1,20):]:]",
        "[text(1,21):]:]",
        "[text(1,22):[:]",
        "[text(1,23):]:]",
        "[text(1,24):a:]",
        "[end-para:::True]",
        "[BLANK(2,1):    ]",
        "[link-ref-def(3,1):True::bar:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<p>a![foo ![bar2][bar3]][]a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_g0c():
    """
    Test case extra g0c:  Full link inside of collapsed link
    """

    # Arrange
    source_markdown = """a![foo [bar2][bar3]][]a
    
[bar]: /url 'title'"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        "[text(1,2):![:]",
        "[text(1,4):foo :]",
        "[text(1,8):[:]",
        "[text(1,9):bar2:]",
        "[text(1,13):]:]",
        "[text(1,14):[:]",
        "[text(1,15):bar3:]",
        "[text(1,19):]:]",
        "[text(1,20):]:]",
        "[text(1,21):[:]",
        "[text(1,22):]:]",
        "[text(1,23):a:]",
        "[end-para:::True]",
        "[BLANK(2,1):    ]",
        "[link-ref-def(3,1):True::bar:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<p>a![foo [bar2][bar3]][]a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_g1():
    """
    Test case extra g1:  Collapsed link inside of collapsed link
    """

    # Arrange
    source_markdown = """a[foo [bar2][]][]a
    
[bar]: /url 'title'"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        "[text(1,2):[:]",
        "[text(1,3):foo :]",
        "[text(1,7):[:]",
        "[text(1,8):bar2:]",
        "[text(1,12):]:]",
        "[text(1,13):[:]",
        "[text(1,14):]:]",
        "[text(1,15):]:]",
        "[text(1,16):[:]",
        "[text(1,17):]:]",
        "[text(1,18):a:]",
        "[end-para:::True]",
        "[BLANK(2,1):    ]",
        "[link-ref-def(3,1):True::bar:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<p>a[foo [bar2][]][]a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_g1a():
    """
    Test case extra g1a:  Collapsed link inside of collapsed link
    """

    # Arrange
    source_markdown = """a[foo ![bar2][]][]a
    
[bar]: /url 'title'"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        "[text(1,2):[:]",
        "[text(1,3):foo :]",
        "[text(1,7):![:]",
        "[text(1,9):bar2:]",
        "[text(1,13):]:]",
        "[text(1,14):[:]",
        "[text(1,15):]:]",
        "[text(1,16):]:]",
        "[text(1,17):[:]",
        "[text(1,18):]:]",
        "[text(1,19):a:]",
        "[end-para:::True]",
        "[BLANK(2,1):    ]",
        "[link-ref-def(3,1):True::bar:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<p>a[foo ![bar2][]][]a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_g1b():
    """
    Test case extra g1b:  Collapsed link inside of collapsed link
    """

    # Arrange
    source_markdown = """a![foo ![bar2][]][]a
    
[bar]: /url 'title'"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        "[text(1,2):![:]",
        "[text(1,4):foo :]",
        "[text(1,8):![:]",
        "[text(1,10):bar2:]",
        "[text(1,14):]:]",
        "[text(1,15):[:]",
        "[text(1,16):]:]",
        "[text(1,17):]:]",
        "[text(1,18):[:]",
        "[text(1,19):]:]",
        "[text(1,20):a:]",
        "[end-para:::True]",
        "[BLANK(2,1):    ]",
        "[link-ref-def(3,1):True::bar:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<p>a![foo ![bar2][]][]a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_g1c():
    """
    Test case extra g1c:  Collapsed link inside of collapsed link
    """

    # Arrange
    source_markdown = """a![foo [bar2][]][]a
    
[bar]: /url 'title'"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        "[text(1,2):![:]",
        "[text(1,4):foo :]",
        "[text(1,8):[:]",
        "[text(1,9):bar2:]",
        "[text(1,13):]:]",
        "[text(1,14):[:]",
        "[text(1,15):]:]",
        "[text(1,16):]:]",
        "[text(1,17):[:]",
        "[text(1,18):]:]",
        "[text(1,19):a:]",
        "[end-para:::True]",
        "[BLANK(2,1):    ]",
        "[link-ref-def(3,1):True::bar:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<p>a![foo [bar2][]][]a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_g2():
    """
    Test case extra g2:  Collapsed link inside of collapsed link
    """

    # Arrange
    source_markdown = """a[foo [bar][]][]a
    
[bar]: /url 'title'"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        "[text(1,2):[:]",
        "[text(1,3):foo :]",
        "[link(1,7):collapsed:/url:title::::bar:::::]",
        "[text(1,8):bar:]",
        "[end-link::]",
        "[text(1,14):]:]",
        "[text(1,15):[:]",
        "[text(1,16):]:]",
        "[text(1,17):a:]",
        "[end-para:::True]",
        "[BLANK(2,1):    ]",
        "[link-ref-def(3,1):True::bar:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<p>a[foo <a href="/url" title="title">bar</a>][]a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_g2a():
    """
    Test case extra g2a:  Collapsed link inside of collapsed link
    """

    # Arrange
    source_markdown = """a[foo ![bar][]][]a
    
[bar]: /url 'title'"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        "[text(1,2):[:]",
        "[text(1,3):foo :]",
        "[image(1,7):collapsed:/url:title:bar::::bar:::::]",
        "[text(1,15):]:]",
        "[text(1,16):[:]",
        "[text(1,17):]:]",
        "[text(1,18):a:]",
        "[end-para:::True]",
        "[BLANK(2,1):    ]",
        "[link-ref-def(3,1):True::bar:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<p>a[foo <img src="/url" alt="bar" title="title" />][]a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_g2b():
    """
    Test case extra g2b:  Collapsed link inside of collapsed link
    """

    # Arrange
    source_markdown = """a![foo ![bar][]][]a
    
[bar]: /url 'title'"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        "[text(1,2):![:]",
        "[text(1,4):foo :]",
        "[image(1,8):collapsed:/url:title:bar::::bar:::::]",
        "[text(1,16):]:]",
        "[text(1,17):[:]",
        "[text(1,18):]:]",
        "[text(1,19):a:]",
        "[end-para:::True]",
        "[BLANK(2,1):    ]",
        "[link-ref-def(3,1):True::bar:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<p>a![foo <img src="/url" alt="bar" title="title" />][]a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_g2c():
    """
    Test case extra g2c:  Collapsed link inside of collapsed link
    """

    # Arrange
    source_markdown = """a![foo [bar][]][]a
    
[bar]: /url 'title'"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        "[text(1,2):![:]",
        "[text(1,4):foo :]",
        "[link(1,8):collapsed:/url:title::::bar:::::]",
        "[text(1,9):bar:]",
        "[end-link::]",
        "[text(1,15):]:]",
        "[text(1,16):[:]",
        "[text(1,17):]:]",
        "[text(1,18):a:]",
        "[end-para:::True]",
        "[BLANK(2,1):    ]",
        "[link-ref-def(3,1):True::bar:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<p>a![foo <a href="/url" title="title">bar</a>][]a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_g3():
    """
    Test case extra g3:  Shortcut link inside of collapsed link
    """

    # Arrange
    source_markdown = """a[foo [bar2]][]a
    
[bar]: /url 'title'"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        "[text(1,2):[:]",
        "[text(1,3):foo :]",
        "[text(1,7):[:]",
        "[text(1,8):bar2:]",
        "[text(1,12):]:]",
        "[text(1,13):]:]",
        "[text(1,14):[:]",
        "[text(1,15):]:]",
        "[text(1,16):a:]",
        "[end-para:::True]",
        "[BLANK(2,1):    ]",
        "[link-ref-def(3,1):True::bar:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<p>a[foo [bar2]][]a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_g3a():
    """
    Test case extra g3a:  Shortcut link inside of collapsed link
    """

    # Arrange
    source_markdown = """a[foo ![bar2]][]a
    
[bar]: /url 'title'"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        "[text(1,2):[:]",
        "[text(1,3):foo :]",
        "[text(1,7):![:]",
        "[text(1,9):bar2:]",
        "[text(1,13):]:]",
        "[text(1,14):]:]",
        "[text(1,15):[:]",
        "[text(1,16):]:]",
        "[text(1,17):a:]",
        "[end-para:::True]",
        "[BLANK(2,1):    ]",
        "[link-ref-def(3,1):True::bar:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<p>a[foo ![bar2]][]a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_g3b():
    """
    Test case extra g3b:  Shortcut link inside of collapsed link
    """

    # Arrange
    source_markdown = """a![foo ![bar2]][]a
    
[bar]: /url 'title'"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        "[text(1,2):![:]",
        "[text(1,4):foo :]",
        "[text(1,8):![:]",
        "[text(1,10):bar2:]",
        "[text(1,14):]:]",
        "[text(1,15):]:]",
        "[text(1,16):[:]",
        "[text(1,17):]:]",
        "[text(1,18):a:]",
        "[end-para:::True]",
        "[BLANK(2,1):    ]",
        "[link-ref-def(3,1):True::bar:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<p>a![foo ![bar2]][]a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_g3c():
    """
    Test case extra g3c:  Shortcut link inside of collapsed link
    """

    # Arrange
    source_markdown = """a![foo [bar2]][]a
    
[bar]: /url 'title'"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        "[text(1,2):![:]",
        "[text(1,4):foo :]",
        "[text(1,8):[:]",
        "[text(1,9):bar2:]",
        "[text(1,13):]:]",
        "[text(1,14):]:]",
        "[text(1,15):[:]",
        "[text(1,16):]:]",
        "[text(1,17):a:]",
        "[end-para:::True]",
        "[BLANK(2,1):    ]",
        "[link-ref-def(3,1):True::bar:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<p>a![foo [bar2]][]a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_g4():
    """
    Test case extra g4:  Shortcut link inside of collapsed link
    """

    # Arrange
    source_markdown = """a[foo [bar]][]a
    
[bar]: /url 'title'"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        "[text(1,2):[:]",
        "[text(1,3):foo :]",
        "[link(1,7):shortcut:/url:title::::bar:::::]",
        "[text(1,8):bar:]",
        "[end-link::]",
        "[text(1,12):]:]",
        "[text(1,13):[:]",
        "[text(1,14):]:]",
        "[text(1,15):a:]",
        "[end-para:::True]",
        "[BLANK(2,1):    ]",
        "[link-ref-def(3,1):True::bar:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<p>a[foo <a href="/url" title="title">bar</a>][]a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_g4a():
    """
    Test case extra g4a:  Shortcut link inside of collapsed link
    """

    # Arrange
    source_markdown = """a[foo ![bar]][]a
    
[bar]: /url 'title'"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        "[text(1,2):[:]",
        "[text(1,3):foo :]",
        "[image(1,7):shortcut:/url:title:bar::::bar:::::]",
        "[text(1,13):]:]",
        "[text(1,14):[:]",
        "[text(1,15):]:]",
        "[text(1,16):a:]",
        "[end-para:::True]",
        "[BLANK(2,1):    ]",
        "[link-ref-def(3,1):True::bar:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<p>a[foo <img src="/url" alt="bar" title="title" />][]a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_g4b():
    """
    Test case extra g4b:  Shortcut link inside of collapsed link
    """

    # Arrange
    source_markdown = """a![foo ![bar]][]a
    
[bar]: /url 'title'"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        "[text(1,2):![:]",
        "[text(1,4):foo :]",
        "[image(1,8):shortcut:/url:title:bar::::bar:::::]",
        "[text(1,14):]:]",
        "[text(1,15):[:]",
        "[text(1,16):]:]",
        "[text(1,17):a:]",
        "[end-para:::True]",
        "[BLANK(2,1):    ]",
        "[link-ref-def(3,1):True::bar:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<p>a![foo <img src="/url" alt="bar" title="title" />][]a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_g4c():
    """
    Test case extra g4c:  Shortcut link inside of collapsed link
    """

    # Arrange
    source_markdown = """a![foo [bar]][]a
    
[bar]: /url 'title'"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        "[text(1,2):![:]",
        "[text(1,4):foo :]",
        "[link(1,8):shortcut:/url:title::::bar:::::]",
        "[text(1,9):bar:]",
        "[end-link::]",
        "[text(1,13):]:]",
        "[text(1,14):[:]",
        "[text(1,15):]:]",
        "[text(1,16):a:]",
        "[end-para:::True]",
        "[BLANK(2,1):    ]",
        "[link-ref-def(3,1):True::bar:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<p>a![foo <a href="/url" title="title">bar</a>][]a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_g5():
    """
    Test case extra g5:  Inline link inside of shortcut link
    """

    # Arrange
    source_markdown = """a[foo [bar2](/url2)]a
    
[bar]: /url 'title'"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        "[text(1,2):[:]",
        "[text(1,3):foo :]",
        "[link(1,7):inline:/url2:::::bar2:False::::]",
        "[text(1,8):bar2:]",
        "[end-link::]",
        "[text(1,20):]:]",
        "[text(1,21):a:]",
        "[end-para:::True]",
        "[BLANK(2,1):    ]",
        "[link-ref-def(3,1):True::bar:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<p>a[foo <a href="/url2">bar2</a>]a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_g5a():
    """
    Test case extra g5a:  Inline link inside of shortcut link
    """

    # Arrange
    source_markdown = """a[foo ![bar2](/url2)]a
    
[bar]: /url 'title'"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        "[text(1,2):[:]",
        "[text(1,3):foo :]",
        "[image(1,7):inline:/url2::bar2::::bar2:False::::]",
        "[text(1,21):]:]",
        "[text(1,22):a:]",
        "[end-para:::True]",
        "[BLANK(2,1):    ]",
        "[link-ref-def(3,1):True::bar:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<p>a[foo <img src="/url2" alt="bar2" />]a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_g5b():
    """
    Test case extra g5b:  Inline link inside of shortcut link
    """

    # Arrange
    source_markdown = """a![foo ![bar2](/url2)]a
    
[bar]: /url 'title'"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        "[text(1,2):![:]",
        "[text(1,4):foo :]",
        "[image(1,8):inline:/url2::bar2::::bar2:False::::]",
        "[text(1,22):]:]",
        "[text(1,23):a:]",
        "[end-para:::True]",
        "[BLANK(2,1):    ]",
        "[link-ref-def(3,1):True::bar:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<p>a![foo <img src="/url2" alt="bar2" />]a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_g5c():
    """
    Test case extra g5c:  Inline link inside of shortcut link
    """

    # Arrange
    source_markdown = """a![foo [bar2](/url2)]a
    
[bar]: /url 'title'"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        "[text(1,2):![:]",
        "[text(1,4):foo :]",
        "[link(1,8):inline:/url2:::::bar2:False::::]",
        "[text(1,9):bar2:]",
        "[end-link::]",
        "[text(1,21):]:]",
        "[text(1,22):a:]",
        "[end-para:::True]",
        "[BLANK(2,1):    ]",
        "[link-ref-def(3,1):True::bar:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<p>a![foo <a href="/url2">bar2</a>]a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_g6():
    """
    Test case extra g6:  Inline link inside of shortcut link
    """

    # Arrange
    source_markdown = """a[foo [bar](/url2)]a
    
[bar]: /url 'title'"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        "[text(1,2):[:]",
        "[text(1,3):foo :]",
        "[link(1,7):inline:/url2:::::bar:False::::]",
        "[text(1,8):bar:]",
        "[end-link::]",
        "[text(1,19):]:]",
        "[text(1,20):a:]",
        "[end-para:::True]",
        "[BLANK(2,1):    ]",
        "[link-ref-def(3,1):True::bar:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<p>a[foo <a href="/url2">bar</a>]a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_g6a():
    """
    Test case extra g6a:  Inline link inside of shortcut link
    """

    # Arrange
    source_markdown = """a[foo ![bar](/url2)]a
    
[bar]: /url 'title'"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        "[text(1,2):[:]",
        "[text(1,3):foo :]",
        "[image(1,7):inline:/url2::bar::::bar:False::::]",
        "[text(1,20):]:]",
        "[text(1,21):a:]",
        "[end-para:::True]",
        "[BLANK(2,1):    ]",
        "[link-ref-def(3,1):True::bar:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<p>a[foo <img src="/url2" alt="bar" />]a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_g6b():
    """
    Test case extra g6b:  Inline link inside of shortcut link
    """

    # Arrange
    source_markdown = """a![foo ![bar](/url2)]a
    
[bar]: /url 'title'"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        "[text(1,2):![:]",
        "[text(1,4):foo :]",
        "[image(1,8):inline:/url2::bar::::bar:False::::]",
        "[text(1,21):]:]",
        "[text(1,22):a:]",
        "[end-para:::True]",
        "[BLANK(2,1):    ]",
        "[link-ref-def(3,1):True::bar:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<p>a![foo <img src="/url2" alt="bar" />]a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_g6c():
    """
    Test case extra g6c:  Inline link inside of shortcut link
    """

    # Arrange
    source_markdown = """a![foo [bar](/url2)]a
    
[bar]: /url 'title'"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        "[text(1,2):![:]",
        "[text(1,4):foo :]",
        "[link(1,8):inline:/url2:::::bar:False::::]",
        "[text(1,9):bar:]",
        "[end-link::]",
        "[text(1,20):]:]",
        "[text(1,21):a:]",
        "[end-para:::True]",
        "[BLANK(2,1):    ]",
        "[link-ref-def(3,1):True::bar:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<p>a![foo <a href="/url2">bar</a>]a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_g7():
    """
    Test case extra f7:  Full link inside of shortcut link
    """

    # Arrange
    source_markdown = """a[foo [bar2][bar]]a
    
[bar]: /url 'title'"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        "[text(1,2):[:]",
        "[text(1,3):foo :]",
        "[link(1,7):full:/url:title:::bar:bar2:::::]",
        "[text(1,8):bar2:]",
        "[end-link::]",
        "[text(1,18):]:]",
        "[text(1,19):a:]",
        "[end-para:::True]",
        "[BLANK(2,1):    ]",
        "[link-ref-def(3,1):True::bar:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<p>a[foo <a href="/url" title="title">bar2</a>]a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_g7a():
    """
    Test case extra g7a:  Full link inside of shortcut link
    """

    # Arrange
    source_markdown = """a[foo ![bar2][bar]]a
    
[bar]: /url 'title'"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        "[text(1,2):[:]",
        "[text(1,3):foo :]",
        "[image(1,7):full:/url:title:bar2:::bar:bar2:::::]",
        "[text(1,19):]:]",
        "[text(1,20):a:]",
        "[end-para:::True]",
        "[BLANK(2,1):    ]",
        "[link-ref-def(3,1):True::bar:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<p>a[foo <img src="/url" alt="bar2" title="title" />]a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_g7b():
    """
    Test case extra g7b:  Full link inside of shortcut link
    """

    # Arrange
    source_markdown = """a![foo ![bar2][bar]]a
    
[bar]: /url 'title'"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        "[text(1,2):![:]",
        "[text(1,4):foo :]",
        "[image(1,8):full:/url:title:bar2:::bar:bar2:::::]",
        "[text(1,20):]:]",
        "[text(1,21):a:]",
        "[end-para:::True]",
        "[BLANK(2,1):    ]",
        "[link-ref-def(3,1):True::bar:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<p>a![foo <img src="/url" alt="bar2" title="title" />]a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_g7c():
    """
    Test case extra g7c:  Full link inside of shortcut link
    """

    # Arrange
    source_markdown = """a![foo [bar2][bar]]a
    
[bar]: /url 'title'"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        "[text(1,2):![:]",
        "[text(1,4):foo :]",
        "[link(1,8):full:/url:title:::bar:bar2:::::]",
        "[text(1,9):bar2:]",
        "[end-link::]",
        "[text(1,19):]:]",
        "[text(1,20):a:]",
        "[end-para:::True]",
        "[BLANK(2,1):    ]",
        "[link-ref-def(3,1):True::bar:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<p>a![foo <a href="/url" title="title">bar2</a>]a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_g8():
    """
    Test case extra g8:  Full link inside of shortcut link
    """

    # Arrange
    source_markdown = """a[foo [bar][bar]]a
    
[bar]: /url 'title'"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        "[text(1,2):[:]",
        "[text(1,3):foo :]",
        "[link(1,7):full:/url:title:::bar:bar:::::]",
        "[text(1,8):bar:]",
        "[end-link::]",
        "[text(1,17):]:]",
        "[text(1,18):a:]",
        "[end-para:::True]",
        "[BLANK(2,1):    ]",
        "[link-ref-def(3,1):True::bar:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<p>a[foo <a href="/url" title="title">bar</a>]a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_g8a():
    """
    Test case extra g8a:  Full link inside of shortcut link
    """

    # Arrange
    source_markdown = """a[foo ![bar][bar]]a
    
[bar]: /url 'title'"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        "[text(1,2):[:]",
        "[text(1,3):foo :]",
        "[image(1,7):full:/url:title:bar:::bar:bar:::::]",
        "[text(1,18):]:]",
        "[text(1,19):a:]",
        "[end-para:::True]",
        "[BLANK(2,1):    ]",
        "[link-ref-def(3,1):True::bar:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<p>a[foo <img src="/url" alt="bar" title="title" />]a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_g8b():
    """
    Test case extra g8b:  Full link inside of shortcut link
    """

    # Arrange
    source_markdown = """a![foo ![bar][bar]]a
    
[bar]: /url 'title'"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        "[text(1,2):![:]",
        "[text(1,4):foo :]",
        "[image(1,8):full:/url:title:bar:::bar:bar:::::]",
        "[text(1,19):]:]",
        "[text(1,20):a:]",
        "[end-para:::True]",
        "[BLANK(2,1):    ]",
        "[link-ref-def(3,1):True::bar:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<p>a![foo <img src="/url" alt="bar" title="title" />]a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_g8c():
    """
    Test case extra g8c:  Full link inside of shortcut link
    """

    # Arrange
    source_markdown = """a![foo [bar][bar]]a
    
[bar]: /url 'title'"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        "[text(1,2):![:]",
        "[text(1,4):foo :]",
        "[link(1,8):full:/url:title:::bar:bar:::::]",
        "[text(1,9):bar:]",
        "[end-link::]",
        "[text(1,18):]:]",
        "[text(1,19):a:]",
        "[end-para:::True]",
        "[BLANK(2,1):    ]",
        "[link-ref-def(3,1):True::bar:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<p>a![foo <a href="/url" title="title">bar</a>]a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_g9():
    """
    Test case extra g9:  Collapsed link inside of shortcut link
    """

    # Arrange
    source_markdown = """a[foo [bar2][]]a
    
[bar]: /url 'title'"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        "[text(1,2):[:]",
        "[text(1,3):foo :]",
        "[text(1,7):[:]",
        "[text(1,8):bar2:]",
        "[text(1,12):]:]",
        "[text(1,13):[:]",
        "[text(1,14):]:]",
        "[text(1,15):]:]",
        "[text(1,16):a:]",
        "[end-para:::True]",
        "[BLANK(2,1):    ]",
        "[link-ref-def(3,1):True::bar:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<p>a[foo [bar2][]]a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_g9a():
    """
    Test case extra g9a:  Collapsed link inside of shortcut link
    """

    # Arrange
    source_markdown = """a[foo ![bar2][]]a
    
[bar]: /url 'title'"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        "[text(1,2):[:]",
        "[text(1,3):foo :]",
        "[text(1,7):![:]",
        "[text(1,9):bar2:]",
        "[text(1,13):]:]",
        "[text(1,14):[:]",
        "[text(1,15):]:]",
        "[text(1,16):]:]",
        "[text(1,17):a:]",
        "[end-para:::True]",
        "[BLANK(2,1):    ]",
        "[link-ref-def(3,1):True::bar:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<p>a[foo ![bar2][]]a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_g9b():
    """
    Test case extra g9b:  Collapsed link inside of shortcut link
    """

    # Arrange
    source_markdown = """a![foo ![bar2][]]a
    
[bar]: /url 'title'"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        "[text(1,2):![:]",
        "[text(1,4):foo :]",
        "[text(1,8):![:]",
        "[text(1,10):bar2:]",
        "[text(1,14):]:]",
        "[text(1,15):[:]",
        "[text(1,16):]:]",
        "[text(1,17):]:]",
        "[text(1,18):a:]",
        "[end-para:::True]",
        "[BLANK(2,1):    ]",
        "[link-ref-def(3,1):True::bar:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<p>a![foo ![bar2][]]a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_g9c():
    """
    Test case extra g9c:  Collapsed link inside of shortcut link
    """

    # Arrange
    source_markdown = """a![foo [bar2][]]a
    
[bar]: /url 'title'"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        "[text(1,2):![:]",
        "[text(1,4):foo :]",
        "[text(1,8):[:]",
        "[text(1,9):bar2:]",
        "[text(1,13):]:]",
        "[text(1,14):[:]",
        "[text(1,15):]:]",
        "[text(1,16):]:]",
        "[text(1,17):a:]",
        "[end-para:::True]",
        "[BLANK(2,1):    ]",
        "[link-ref-def(3,1):True::bar:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<p>a![foo [bar2][]]a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_h0():
    """
    Test case extra h0:  Collapsed link inside of shortcut link
    """

    # Arrange
    source_markdown = """a[foo [bar][]]a
    
[bar]: /url 'title'"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        "[text(1,2):[:]",
        "[text(1,3):foo :]",
        "[link(1,7):collapsed:/url:title::::bar:::::]",
        "[text(1,8):bar:]",
        "[end-link::]",
        "[text(1,14):]:]",
        "[text(1,15):a:]",
        "[end-para:::True]",
        "[BLANK(2,1):    ]",
        "[link-ref-def(3,1):True::bar:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<p>a[foo <a href="/url" title="title">bar</a>]a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_h0a():
    """
    Test case extra h0a:  Collapsed link inside of shortcut link
    """

    # Arrange
    source_markdown = """a[foo ![bar][]]a
    
[bar]: /url 'title'"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        "[text(1,2):[:]",
        "[text(1,3):foo :]",
        "[image(1,7):collapsed:/url:title:bar::::bar:::::]",
        "[text(1,15):]:]",
        "[text(1,16):a:]",
        "[end-para:::True]",
        "[BLANK(2,1):    ]",
        "[link-ref-def(3,1):True::bar:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<p>a[foo <img src="/url" alt="bar" title="title" />]a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_h0b():
    """
    Test case extra h0b:  Collapsed link inside of shortcut link
    """

    # Arrange
    source_markdown = """a![foo ![bar][]]a
    
[bar]: /url 'title'"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        "[text(1,2):![:]",
        "[text(1,4):foo :]",
        "[image(1,8):collapsed:/url:title:bar::::bar:::::]",
        "[text(1,16):]:]",
        "[text(1,17):a:]",
        "[end-para:::True]",
        "[BLANK(2,1):    ]",
        "[link-ref-def(3,1):True::bar:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<p>a![foo <img src="/url" alt="bar" title="title" />]a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_h0c():
    """
    Test case extra h0c:  Collapsed link inside of shortcut link
    """

    # Arrange
    source_markdown = """a![foo [bar][]]a
    
[bar]: /url 'title'"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        "[text(1,2):![:]",
        "[text(1,4):foo :]",
        "[link(1,8):collapsed:/url:title::::bar:::::]",
        "[text(1,9):bar:]",
        "[end-link::]",
        "[text(1,15):]:]",
        "[text(1,16):a:]",
        "[end-para:::True]",
        "[BLANK(2,1):    ]",
        "[link-ref-def(3,1):True::bar:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<p>a![foo <a href="/url" title="title">bar</a>]a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_h1():
    """
    Test case extra h1:  Shortcut link inside of shortcut link
    """

    # Arrange
    source_markdown = """a[foo [bar2]]a
    
[bar]: /url 'title'"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        "[text(1,2):[:]",
        "[text(1,3):foo :]",
        "[text(1,7):[:]",
        "[text(1,8):bar2:]",
        "[text(1,12):]:]",
        "[text(1,13):]:]",
        "[text(1,14):a:]",
        "[end-para:::True]",
        "[BLANK(2,1):    ]",
        "[link-ref-def(3,1):True::bar:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<p>a[foo [bar2]]a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_h1a():
    """
    Test case extra h1a:  Shortcut link inside of shortcut link
    """

    # Arrange
    source_markdown = """a[foo ![bar2]]a
    
[bar]: /url 'title'"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        "[text(1,2):[:]",
        "[text(1,3):foo :]",
        "[text(1,7):![:]",
        "[text(1,9):bar2:]",
        "[text(1,13):]:]",
        "[text(1,14):]:]",
        "[text(1,15):a:]",
        "[end-para:::True]",
        "[BLANK(2,1):    ]",
        "[link-ref-def(3,1):True::bar:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<p>a[foo ![bar2]]a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_h1b():
    """
    Test case extra h1b:  Shortcut link inside of shortcut link
    """

    # Arrange
    source_markdown = """a![foo ![bar2]]a
    
[bar]: /url 'title'"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        "[text(1,2):![:]",
        "[text(1,4):foo :]",
        "[text(1,8):![:]",
        "[text(1,10):bar2:]",
        "[text(1,14):]:]",
        "[text(1,15):]:]",
        "[text(1,16):a:]",
        "[end-para:::True]",
        "[BLANK(2,1):    ]",
        "[link-ref-def(3,1):True::bar:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<p>a![foo ![bar2]]a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_h1c():
    """
    Test case extra h1c:  Shortcut link inside of shortcut link
    """

    # Arrange
    source_markdown = """a![foo [bar2]]a
    
[bar]: /url 'title'"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        "[text(1,2):![:]",
        "[text(1,4):foo :]",
        "[text(1,8):[:]",
        "[text(1,9):bar2:]",
        "[text(1,13):]:]",
        "[text(1,14):]:]",
        "[text(1,15):a:]",
        "[end-para:::True]",
        "[BLANK(2,1):    ]",
        "[link-ref-def(3,1):True::bar:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<p>a![foo [bar2]]a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_h2():
    """
    Test case extra h2:  Shortcut link inside of shortcut link
    """

    # Arrange
    source_markdown = """a[foo [bar]]a
    
[bar]: /url 'title'"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        "[text(1,2):[:]",
        "[text(1,3):foo :]",
        "[link(1,7):shortcut:/url:title::::bar:::::]",
        "[text(1,8):bar:]",
        "[end-link::]",
        "[text(1,12):]:]",
        "[text(1,13):a:]",
        "[end-para:::True]",
        "[BLANK(2,1):    ]",
        "[link-ref-def(3,1):True::bar:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<p>a[foo <a href="/url" title="title">bar</a>]a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_h2a():
    """
    Test case extra h2a:  Shortcut link inside of shortcut link
    """

    # Arrange
    source_markdown = """a[foo ![bar]]a
    
[bar]: /url 'title'"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        "[text(1,2):[:]",
        "[text(1,3):foo :]",
        "[image(1,7):shortcut:/url:title:bar::::bar:::::]",
        "[text(1,13):]:]",
        "[text(1,14):a:]",
        "[end-para:::True]",
        "[BLANK(2,1):    ]",
        "[link-ref-def(3,1):True::bar:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<p>a[foo <img src="/url" alt="bar" title="title" />]a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_h2b():
    """
    Test case extra h2b:  Shortcut link inside of shortcut link
    """

    # Arrange
    source_markdown = """a![foo ![bar]]a
    
[bar]: /url 'title'"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        "[text(1,2):![:]",
        "[text(1,4):foo :]",
        "[image(1,8):shortcut:/url:title:bar::::bar:::::]",
        "[text(1,14):]:]",
        "[text(1,15):a:]",
        "[end-para:::True]",
        "[BLANK(2,1):    ]",
        "[link-ref-def(3,1):True::bar:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<p>a![foo <img src="/url" alt="bar" title="title" />]a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_h2c():
    """
    Test case extra h2c:  Shortcut link inside of shortcut link
    """

    # Arrange
    source_markdown = """a![foo [bar]]a
    
[bar]: /url 'title'"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        "[text(1,2):![:]",
        "[text(1,4):foo :]",
        "[link(1,8):shortcut:/url:title::::bar:::::]",
        "[text(1,9):bar:]",
        "[end-link::]",
        "[text(1,13):]:]",
        "[text(1,14):a:]",
        "[end-para:::True]",
        "[BLANK(2,1):    ]",
        "[link-ref-def(3,1):True::bar:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<p>a![foo <a href="/url" title="title">bar</a>]a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_h9():
    """
    Test case extra h9:  Inline link containing lin breaks
    """

    # Arrange
    source_markdown = """abc\n[link](\n/uri\n"title"\n)\ndef"""
    expected_tokens = [
        "[para(1,1):\n\n\n\n\n]",
        "[text(1,1):abc\n::\n]",
        '[link(2,1):inline:/uri:title::::link:False:":\n:\n:\n]',
        "[text(2,2):link:]",
        "[end-link::]",
        "[text(5,2):\ndef::\n]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>abc\n<a href="/uri" title="title">link</a>\ndef</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_h9a():
    """
    Test case extra h9:  Inline image containing lin breaks
    """

    # Arrange
    source_markdown = """abc\n![link](\n/uri\n"title"\n)\ndef"""
    expected_tokens = [
        "[para(1,1):\n\n\n\n\n]",
        "[text(1,1):abc\n::\n]",
        '[image(2,1):inline:/uri:title:link::::link:False:":\n:\n:\n]',
        "[text(5,2):\ndef::\n]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>abc\n<img src="/uri" alt="link" title="title" />\ndef</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_h9aa():
    """
    Test case extra h9:  Inline image containing lin breaks
    """

    # Arrange
    source_markdown = """abc\n![link](\n/uri\n"title"\n)"""
    expected_tokens = [
        "[para(1,1):\n\n\n\n]",
        "[text(1,1):abc\n::\n]",
        '[image(2,1):inline:/uri:title:link::::link:False:":\n:\n:\n]',
        "[end-para:::True]",
    ]
    expected_gfm = """<p>abc\n<img src="/uri" alt="link" title="title" /></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_h9b():
    """
    Test case extra h9b:  Inline link containing lin breaks
    """

    # Arrange
    source_markdown = """abc\n[link](\n/uri\n"title"\n)"""
    expected_tokens = [
        "[para(1,1):\n\n\n\n]",
        "[text(1,1):abc\n::\n]",
        '[link(2,1):inline:/uri:title::::link:False:":\n:\n:\n]',
        "[text(2,2):link:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>abc\n<a href="/uri" title="title">link</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_j0():
    """
    Test case extra j0:  Inline link containing line breaks
    """

    # Arrange
    source_markdown = """abc\n[link](  \n  /uri  \n   "title"   \n )\ndef"""
    expected_tokens = [
        "[para(1,1):\n\n  \n   \n \n]",
        "[text(1,1):abc\n::\n]",
        '[link(2,1):inline:/uri:title::::link:False:":  \n:  \n:   \n]',
        "[text(2,2):link:]",
        "[end-link::]",
        "[text(5,3):\ndef::\n]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>abc\n<a href="/uri" title="title">link</a>\ndef</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_j0a():
    """
    Test case extra j0a:  Inline image containing line breaks
    """

    # Arrange
    source_markdown = """abc\n![link](  \n  /uri  \n   "title"   \n )\ndef"""
    expected_tokens = [
        "[para(1,1):\n\n  \n   \n \n]",
        "[text(1,1):abc\n::\n]",
        '[image(2,1):inline:/uri:title:link::::link:False:":  \n:  \n:   \n]',
        "[text(5,3):\ndef::\n]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>abc\n<img src="/uri" alt="link" title="title" />\ndef</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_j0b():
    """
    Test case extra j0:  Inline link containing line breaks
    """

    # Arrange
    source_markdown = """abc\n[link](  \n  /uri  \n   "title"   \n ) \ndef"""
    expected_tokens = [
        "[para(1,1):\n\n  \n   \n \n]",
        "[text(1,1):abc\n::\n]",
        '[link(2,1):inline:/uri:title::::link:False:":  \n:  \n:   \n]',
        "[text(2,2):link:]",
        "[end-link::]",
        "[text(5,3):\ndef:: \n]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>abc\n<a href="/uri" title="title">link</a>\ndef</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_j0c():
    """
    Test case extra j0a:  Inline image containing line breaks
    """

    # Arrange
    source_markdown = """abc\n![link](  \n  /uri  \n   "title"   \n ) \ndef"""
    expected_tokens = [
        "[para(1,1):\n\n  \n   \n \n]",
        "[text(1,1):abc\n::\n]",
        '[image(2,1):inline:/uri:title:link::::link:False:":  \n:  \n:   \n]',
        "[text(5,3):\ndef:: \n]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>abc\n<img src="/uri" alt="link" title="title" />\ndef</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_j0d():
    """
    Test case extra j0d:  Inline link containing line breaks
    """

    # Arrange
    source_markdown = """abc\n[link](  \n  /uri  \n   "title"   \n )"""
    expected_tokens = [
        "[para(1,1):\n\n  \n   \n ]",
        "[text(1,1):abc\n::\n]",
        '[link(2,1):inline:/uri:title::::link:False:":  \n:  \n:   \n]',
        "[text(2,2):link:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>abc\n<a href="/uri" title="title">link</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_j0e():
    """
    Test case extra j0e:  Inline link containing line breaks inside
    """

    # Arrange
    source_markdown = """abc
[link](\a\a\a\a
  /uri\a\a
   "title"\a\a\a
 )
 def""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[para(1,1):\n\n  \n   \n \n ]",
        "[text(1,1):abc\n::\n]",
        '[link(2,1):inline:/uri:title::::link:False:":    \n:  \n:   \n]',
        "[text(2,2):link:]",
        "[end-link::]",
        "[text(5,3):\ndef::\n]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>abc\n<a href="/uri" title="title">link</a>\ndef</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_j0ea():
    """
    Test case extra j0ea:  Inline link containing line breaks inside of block quote
    """

    # Arrange
    source_markdown = """> abc
> [link](\a\a\a\a
>   /uri\a\a
>    "title"\a\a\a
>  )
> def""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> \n> \n> ]",
        "[para(1,3):\n\n  \n   \n \n]",
        "[text(1,3):abc\n::\n]",
        '[link(2,1):inline:/uri:title::::link:False:":    \n:  \n:   \n]',
        "[text(2,2):link:]",
        "[end-link::]",
        "[text(5,3):\ndef::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc
<a href="/uri" title="title">link</a>
def</p>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_extra_j0eb():
    """
    Test case extra j0e:  Inline link containing line breaks inside of list
    """

    # Arrange
    source_markdown = """- abc
  [link](\a\a\a\a
    /uri\a\a
     "title"\a\a\a
   )
   def""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[ulist(1,1):-::2::  \n  \n  \n  \n  ]",
        "[para(1,3):\n\n  \n   \n \n ]",
        "[text(1,3):abc\n::\n]",
        '[link(2,1):inline:/uri:title::::link:False:":    \n:  \n:   \n]',
        "[text(2,2):link:]",
        "[end-link::]",
        "[text(5,3):\ndef::\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>abc
<a href="/uri" title="title">link</a>
def</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)
