"""
https://github.github.com/gfm/#paragraph
"""

from test.utils import act_and_assert

import pytest


# pylint: disable=too-many-lines
@pytest.mark.gfm
def test_paragraph_series_j_l_bh_s_t():
    """
    Test case:  Inline link containing backslash hard line break in label, followed by text
    was:        test_paragraph_extra_h8
    """

    # Arrange
    source_markdown = """a[foo\\\ncom](/uri "title")a"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):a:]",
        '[link(1,2):inline:/uri:title::::foo\\\ncom:False:":: :]',
        "[text(1,3):foo:]",
        "[hard-break(1,6):\\:\n]",
        "[text(2,1):com:]",
        "[end-link::]",
        "[text(2,19):a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<a href="/uri" title="title">foo<br />
com</a>a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_j_i_bh_s_t():
    """
    Test case:  Inline image containing backslash hard line break in label, followed by text
    was:        test_paragraph_extra_h8a
    """

    # Arrange
    source_markdown = """a![foo\\\ncom](/uri "title")a"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):a:]",
        '[image(1,2):inline:/uri:title:foo\ncom::::foo\\\ncom:False:":: :]',
        "[text(2,19):a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<img src="/uri" alt="foo
com" title="title" />a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_j_l_sh_s_t():
    """
    Test case:  Inline image containing space hard line break in label, followed by text
    was:        test_paragraph_extra_h8b
    """

    # Arrange
    source_markdown = """a[foo  \ncom](/uri "title")a"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):a:]",
        '[link(1,2):inline:/uri:title::::foo  \ncom:False:":: :]',
        "[text(1,3):foo:]",
        "[hard-break(1,6):  :\n]",
        "[text(2,1):com:]",
        "[end-link::]",
        "[text(2,19):a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<a href="/uri" title="title">foo<br />
com</a>a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_j_i_sh_s_t():
    """
    Test case:  Inline image containing space hard line break in label, followed by text
    was:        test_paragraph_extra_h8c
    """

    # Arrange
    source_markdown = """a![foo  \ncom](/uri "title")a"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):a:]",
        '[image(1,2):inline:/uri:title:foo\ncom::::foo  \ncom:False:":: :]',
        "[text(2,19):a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<img src="/uri" alt="foo
com" title="title" />a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_j_l_rh_s_t():
    """
    Test case:  Inline link containing split raw html in label
    was:        test_paragraph_extra_c7, changed split text at end to text
    """

    # Arrange
    source_markdown = """a[li<de\nfg>nk](/url)a"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):a:]",
        "[link(1,2):inline:/url:::::li<de\nfg>nk:False::::]",
        "[text(1,3):li:]",
        "[raw-html(1,5):de\nfg]",
        "[text(2,4):nk:]",
        "[end-link::]",
        "[text(2,13):a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<a href="/url">li<de
fg>nk</a>a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_j_i_rh_s_t():
    """
    Test case:  Inline image containing split raw html in label
    was:        test_paragraph_extra_c8, changed split text at end to text
    """

    # Arrange
    source_markdown = """a![li<de\nfg>nk](/url)a"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):a:]",
        "[image(1,2):inline:/url::li<de\nfg>nk::::li<de\nfg>nk:False::::]",
        "[text(2,13):a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<img src="/url" alt="li<de
fg>nk" />a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_j_l_em_s_t():
    """
    Test case:  Inline link containing split emphasis in label
    was:        test_paragraph_extra_e1
    """

    # Arrange
    source_markdown = """a[a*li\nnk*a](/uri "title")a"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):a:]",
        '[link(1,2):inline:/uri:title::::a*li\nnk*a:False:":: :]',
        "[text(1,3):a:]",
        "[emphasis(1,4):1:*]",
        "[text(1,5):li\nnk::\n]",
        "[end-emphasis(2,3)::]",
        "[text(2,4):a:]",
        "[end-link::]",
        "[text(2,20):a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<a href="/uri" title="title">a<em>li\nnk</em>a</a>a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_j_i_em_s_t():
    """
    Test case:  Inline image containing split emphasis in label
    was:        test_paragraph_extra_e2
    """

    # Arrange
    source_markdown = """a![a*li\nnk*a](/uri "title")a"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):a:]",
        '[image(1,2):inline:/uri:title:ali\nnka::::a*li\nnk*a:False:":: :]',
        "[text(2,20):a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<img src="/uri" alt="ali\nnka" title="title" />a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_j_l_em_t():
    """
    Test case:  Inline image containing emphasis in label
    was:        test_paragraph_extra_d9
    """

    # Arrange
    source_markdown = """a[*link*](/uri "title")a"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        '[link(1,2):inline:/uri:title::::*link*:False:":: :]',
        "[emphasis(1,3):1:*]",
        "[text(1,4):link:]",
        "[end-emphasis(1,8)::]",
        "[end-link::]",
        "[text(1,24):a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<a href="/uri" title="title"><em>link</em></a>a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_j_i_em_t():
    """
    Test case:  Inline link containing emphasis in label
    was:        test_paragraph_extra_e0
    """

    # Arrange
    source_markdown = """a![*link*](/uri "title")a"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        '[image(1,2):inline:/uri:title:link::::*link*:False:":: :]',
        "[text(1,25):a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<img src="/uri" alt="link" title="title" />a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_j_l_ua_t():
    """
    Test case:  Inline link containing URI autolink in label
    was:        test_paragraph_extra_h6
    """

    # Arrange
    source_markdown = """a[a<http://google.com>a](/uri "title")a"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        '[link(1,2):inline:/uri:title::::a<http://google.com>a:False:":: :]',
        "[text(1,3):a:]",
        "[uri-autolink(1,4):http://google.com]",
        "[text(1,23):a:]",
        "[end-link::]",
        "[text(1,39):a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<a href="/uri" title="title">a<a href="http://google.com">http://google.com</a>a</a>a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_j_i_ua_t():
    """
    Test case:  Inline image containing URI autolink in label
    was:        test_paragraph_extra_h6a
    """

    # Arrange
    source_markdown = """a![a<http://google.com>a](/uri "title")a"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        '[image(1,2):inline:/uri:title:ahttp://google.coma::::a<http://google.com>a:False:":: :]',
        "[text(1,40):a:]",
        "[end-para:::True]",
    ]
    expected_gfm = (
        """<p>a<img src="/uri" alt="ahttp://google.coma" title="title" />a</p>"""
    )

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_j_l_ea_t():
    """
    Test case:  Inline link containing email autolink in label
    was:        test_paragraph_extra_h7
    """

    # Arrange
    source_markdown = """a[a<foo@r.com>a](/uri "title")a"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        '[link(1,2):inline:/uri:title::::a<foo@r.com>a:False:":: :]',
        "[text(1,3):a:]",
        "[email-autolink(1,4):foo@r.com]",
        "[text(1,15):a:]",
        "[end-link::]",
        "[text(1,31):a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<a href="/uri" title="title">a<a href="mailto:foo@r.com">foo@r.com</a>a</a>a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_j_i_ea_t():
    """
    Test case:  Inline image containing email autolink in label
    was:        test_paragraph_extra_h7a
    """

    # Arrange
    source_markdown = """a![a<foo@r.com>a](/uri "title")a"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        '[image(1,2):inline:/uri:title:afoo@r.coma::::a<foo@r.com>a:False:":: :]',
        "[text(1,32):a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<img src="/uri" alt="afoo@r.coma" title="title" />a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_j_l_cs_t():
    """
    Test case:  Inline link containing code span in label
    was:        test_paragraph_extra_h4
    """

    # Arrange
    source_markdown = """a[a`li nk`a](/uri "title")a"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        '[link(1,2):inline:/uri:title::::a`li nk`a:False:":: :]',
        "[text(1,3):a:]",
        "[icode-span(1,4):li nk:`::]",
        "[text(1,11):a:]",
        "[end-link::]",
        "[text(1,27):a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<a href="/uri" title="title">a<code>li nk</code>a</a>a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_j_i_cs_t():
    """
    Test case:  Inline image containing code span in label
    was:        test_paragraph_extra_h4a
    """

    # Arrange
    source_markdown = """a![a`li nk`a](/uri "title")a"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        '[image(1,2):inline:/uri:title:ali nka::::a`li nk`a:False:":: :]',
        "[text(1,28):a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<img src="/uri" alt="ali nka" title="title" />a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_j_l_rh_t():
    """
    Test case:  Inline link containing code span in label
    was:        test_paragraph_extra_h5
    """

    # Arrange
    source_markdown = """a[a<li nk>a](/uri "title")a"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        '[link(1,2):inline:/uri:title::::a<li nk>a:False:":: :]',
        "[text(1,3):a:]",
        "[raw-html(1,4):li nk]",
        "[text(1,11):a:]",
        "[end-link::]",
        "[text(1,27):a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<a href="/uri" title="title">a<li nk>a</a>a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_j_i_rh_t():
    """
    Test case:  Inline image containing code span in label
    was:        test_paragraph_extra_h5a
    """

    # Arrange
    source_markdown = """a![a<li nk>a](/uri "title")a"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        '[image(1,2):inline:/uri:title:a<li nk>a::::a<li nk>a:False:":: :]',
        "[text(1,28):a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<img src="/uri" alt="a<li nk>a" title="title" />a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_j_l_cs_s_t():
    """
    Test case:  Inline link containing split code span in label
    """

    # Arrange
    source_markdown = """a[a`li\nnk`a](/uri "title")a"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):a:]",
        '[link(1,2):inline:/uri:title::::a`li\nnk`a:False:":: :]',
        "[text(1,3):a:]",
        "[icode-span(1,4):li\a\n\a \ank:`::]",
        "[text(2,4):a:]",
        "[end-link::]",
        "[text(2,20):a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<a href="/uri" title="title">a<code>li nk</code>a</a>a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_j_i_cs_s_t():
    """
    Test case:  Inline image containing split code span in label
    """

    # Arrange
    source_markdown = """a![a`li\nnk`a](/uri "title")a"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):a:]",
        '[image(1,2):inline:/uri:title:ali nka::::a`li\nnk`a:False:":: :]',
        "[text(2,20):a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<img src="/uri" alt="ali nka" title="title" />a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_j_l_nt_t_s_t():
    """
    Test case:  Inline link with no title containing split text in label
    was:        test_paragraph_extra_a2
    """

    # Arrange
    source_markdown = """a![fo
o](</my url>)a"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):a:]",
        "[image(1,2):inline:/my%20url::fo\no:/my url:::fo\no:True::::]",
        "[text(2,14):a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<img src="/my%20url" alt="fo
o" />a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_j_i_nt_t_s_t():
    """
    Test case:  Inline image with no title containing split text in label
    was:        test_paragraph_extra_a2a
    """

    # Arrange
    source_markdown = """a[fo
o](</my url>)a"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):a:]",
        "[link(1,2):inline:/my%20url::/my url:::fo\no:True::::]",
        "[text(1,3):fo\no::\n]",
        "[end-link::]",
        "[text(2,14):a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<a href="/my%20url">fo
o</a>a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_j_l_t_s_t():
    """
    Test case:  Inline link containing split text in label
    """

    # Arrange
    source_markdown = """a![fo
o](</my url> "title")a"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):a:]",
        '[image(1,2):inline:/my%20url:title:fo\no:/my url:::fo\no:True:":: :]',
        "[text(2,22):a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<img src="/my%20url" alt="fo
o" title="title" />a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_j_i_t_s_t():
    """
    Test case:  Inline image containing split text in label
    """

    # Arrange
    source_markdown = """a[fo
o](</my url> "title")a"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):a:]",
        '[link(1,2):inline:/my%20url:title:/my url:::fo\no:True:":: :]',
        "[text(1,3):fo\no::\n]",
        "[end-link::]",
        "[text(2,22):a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<a href="/my%20url" title="title">fo
o</a>a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_j_i_nt_t_t():
    """
    Test case:  Inline image with no title containing text in label
    """

    # Arrange
    source_markdown = """a![foo](</my url>)a"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        "[image(1,2):inline:/my%20url::foo:/my url:::foo:True::::]",
        "[text(1,19):a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<img src="/my%20url" alt="foo" />a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_j_l_nt_t_t():
    """
    Test case:  Inline link with no title containing text in label
    """

    # Arrange
    source_markdown = """a[foo](</my url>)a"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        "[link(1,2):inline:/my%20url::/my url:::foo:True::::]",
        "[text(1,3):foo:]",
        "[end-link::]",
        "[text(1,18):a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<a href="/my%20url">foo</a>a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_j_l_t_t():
    """
    Test case:  Inline link containing text in label
    """

    # Arrange
    source_markdown = """a![foo](</my url> "title")a"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        '[image(1,2):inline:/my%20url:title:foo:/my url:::foo:True:":: :]',
        "[text(1,27):a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<img src="/my%20url" alt="foo" title="title" />a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_j_i_t_t():
    """
    Test case:  Inline image containing text in label
    """

    # Arrange
    source_markdown = """a[foo](</my url> "title")a"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        '[link(1,2):inline:/my%20url:title:/my url:::foo:True:":: :]',
        "[text(1,3):foo:]",
        "[end-link::]",
        "[text(1,26):a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<a href="/my%20url" title="title">foo</a>a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_j_l_t_t_s():
    """
    Test case:  Inline link containing text in label and split text after
    """

    # Arrange
    source_markdown = """a[foo](/url "title")a\nb"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):a:]",
        '[link(1,2):inline:/url:title::::foo:False:":: :]',
        "[text(1,3):foo:]",
        "[end-link::]",
        "[text(1,21):a\nb::\n]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<a href="/url" title="title">foo</a>a
b</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_j_i_t_t_s():
    """
    Test case:  Inline image containing text in label and split text after
    """

    # Arrange
    source_markdown = """a![foo](/url "title")a\nb"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):a:]",
        '[image(1,2):inline:/url:title:foo::::foo:False:":: :]',
        "[text(1,22):a\nb::\n]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<img src="/url" alt="foo" title="title" />a
b</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_j_l_t_cs_s():
    """
    Test case:  Inline link with no title containing split text in label
    was:        test_paragraph_extra_c9, added title, removed split raw html in label
    """

    # Arrange
    source_markdown = """a[link](/url "title")`a\nb`"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):a:]",
        '[link(1,2):inline:/url:title::::link:False:":: :]',
        "[text(1,3):link:]",
        "[end-link::]",
        "[icode-span(1,22):a\a\n\a \ab:`::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<a href="/url" title="title">link</a><code>a b</code></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_j_i_t_cs_s():
    """
    Test case:  Inline link with no title containing split text in label
    was:        test_paragraph_extra_d0, added title, removed split raw html in label
    """

    # Arrange
    source_markdown = """a![link](/url "title")`a\nb`"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):a:]",
        '[image(1,2):inline:/url:title:link::::link:False:":: :]',
        "[icode-span(1,23):a\a\n\a \ab:`::]",
        "[end-para:::True]",
    ]
    expected_gfm = (
        """<p>a<img src="/url" alt="link" title="title" /><code>a b</code></p>"""
    )

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_j_l_t_cs():
    """
    Test case:  Inline link with text in label followed by code span
    """

    # Arrange
    source_markdown = """a[link](/url "title")`ab`"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        '[link(1,2):inline:/url:title::::link:False:":: :]',
        "[text(1,3):link:]",
        "[end-link::]",
        "[icode-span(1,22):ab:`::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<a href="/url" title="title">link</a><code>ab</code></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_j_i_t_cs():
    """
    Test case:  Inline image with text in label followed by code span
    """

    # Arrange
    source_markdown = """a![link](/url "title")`ab`"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        '[image(1,2):inline:/url:title:link::::link:False:":: :]',
        "[icode-span(1,23):ab:`::]",
        "[end-para:::True]",
    ]
    expected_gfm = (
        """<p>a<img src="/url" alt="link" title="title" /><code>ab</code></p>"""
    )

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_j_l_t_rh_s():
    """
    Test case:  Inline link containing text in label with split raw html after
    was:        test_paragraph_extra_d1, added title, removed split raw html in label
    """

    # Arrange
    source_markdown = """a[link](/url "title")<a\nb>"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):a:]",
        '[link(1,2):inline:/url:title::::link:False:":: :]',
        "[text(1,3):link:]",
        "[end-link::]",
        "[raw-html(1,22):a\nb]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<a href="/url" title="title">link</a><a
b></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_j_i_t_rh_s():
    """
    Test case:  Inline image containing text in label with split raw html after
    was:        test_paragraph_extra_d2, added title, removed split raw html in label
    """

    # Arrange
    source_markdown = """a![link](/url "title")<a\nb>"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):a:]",
        '[image(1,2):inline:/url:title:link::::link:False:":: :]',
        "[raw-html(1,23):a\nb]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<img src="/url" alt="link" title="title" /><a
b></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_j_l_t_rh():
    """
    Test case:  Inline link containing text in label with raw html after
    was:        test_paragraph_extra_d1, added title, removed split raw html in label
    """

    # Arrange
    source_markdown = """a[link](/url "title")<a b>"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        '[link(1,2):inline:/url:title::::link:False:":: :]',
        "[text(1,3):link:]",
        "[end-link::]",
        "[raw-html(1,22):a b]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<a href="/url" title="title">link</a><a b></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_j_i_t_rh():
    """
    Test case:  Inline image containing text in label with split raw html after
    was:        test_paragraph_extra_d2, added title, removed split raw html in label
    """

    # Arrange
    source_markdown = """a![link](/url "title")<a b>"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        '[image(1,2):inline:/url:title:link::::link:False:":: :]',
        "[raw-html(1,23):a b]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<img src="/url" alt="link" title="title" /><a b></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_j_l_t_em_s():
    """
    Test case:  Inline link containing text in label with split emphasis after
    was:        test_paragraph_extra_d3, added title, removed split raw html in label
    """

    # Arrange
    source_markdown = """a[link](/url)*a\nb*"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):a:]",
        "[link(1,2):inline:/url:::::link:False::::]",
        "[text(1,3):link:]",
        "[end-link::]",
        "[emphasis(1,14):1:*]",
        "[text(1,15):a\nb::\n]",
        "[end-emphasis(2,2)::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<a href="/url">link</a><em>a
b</em></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_j_i_t_em_s():
    """
    Test case:  Inline image containing text in label with split emphasis after
    was:        test_paragraph_extra_d4, added title, removed split raw html in label
    """

    # Arrange
    source_markdown = """a![link](/url)*a\nb*"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):a:]",
        "[image(1,2):inline:/url::link::::link:False::::]",
        "[emphasis(1,15):1:*]",
        "[text(1,16):a\nb::\n]",
        "[end-emphasis(2,2)::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<img src="/url" alt="link" /><em>a
b</em></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_j_l_t_em():
    """
    Test case:  Inline link containing text in label with emphasis after
    """

    # Arrange
    source_markdown = """a[link](/url)*a b*"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        "[link(1,2):inline:/url:::::link:False::::]",
        "[text(1,3):link:]",
        "[end-link::]",
        "[emphasis(1,14):1:*]",
        "[text(1,15):a b:]",
        "[end-emphasis(1,18)::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<a href="/url">link</a><em>a b</em></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_j_i_t_em():
    """
    Test case:  Inline image containing text in label with emphasis after
    was:        test_paragraph_extra_d4, added title, removed split raw html in label
    """

    # Arrange
    source_markdown = """a![link](/url)*a b*"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        "[image(1,2):inline:/url::link::::link:False::::]",
        "[emphasis(1,15):1:*]",
        "[text(1,16):a b:]",
        "[end-emphasis(1,19)::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<img src="/url" alt="link" /><em>a b</em></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_j_em_l_t_t():
    """
    Test case:  Inline link containing text in label surrounded by emphasis
    was:        test_paragraph_extra_d7
    """

    # Arrange
    source_markdown = """a*[link](/uri "title")*a"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        "[text(1,2):*:]",
        '[link(1,3):inline:/uri:title::::link:False:":: :]',
        "[text(1,4):link:]",
        "[end-link::]",
        "[text(1,23):*:]",
        "[text(1,24):a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a*<a href="/uri" title="title">link</a>*a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_j_em_i_t_t():
    """
    Test case:  Inline link containing text in label surrounded by emphasis
    was:        test_paragraph_extra_d8
    """

    # Arrange
    source_markdown = """a*![link](/uri "title")*a"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        "[text(1,2):*:]",
        '[image(1,3):inline:/uri:title:link::::link:False:":: :]',
        "[text(1,24):*:]",
        "[text(1,25):a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a*<img src="/uri" alt="link" title="title" />*a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_j_l_t_ua():
    """
    Test case:  Inline link containing text in label followed by url autolink
    """

    # Arrange
    source_markdown = """a[link](/url "title")<http://google.com>a"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        '[link(1,2):inline:/url:title::::link:False:":: :]',
        "[text(1,3):link:]",
        "[end-link::]",
        "[uri-autolink(1,22):http://google.com]",
        "[text(1,41):a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<a href="/url" title="title">link</a><a href="http://google.com">http://google.com</a>a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_j_i_t_ua():
    """
    Test case:  Inline image containing text in label followed by url autolink
    """

    # Arrange
    source_markdown = """a![link](/url "title")<http://google.com>a"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        '[image(1,2):inline:/url:title:link::::link:False:":: :]',
        "[uri-autolink(1,23):http://google.com]",
        "[text(1,42):a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<img src="/url" alt="link" title="title" /><a href="http://google.com">http://google.com</a>a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_j_l_t_ea():
    """
    Test case:  Inline link containing text in label followed by email autolink
    """

    # Arrange
    source_markdown = """a[link](/url "title")<foo@r.com>a"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        '[link(1,2):inline:/url:title::::link:False:":: :]',
        "[text(1,3):link:]",
        "[end-link::]",
        "[email-autolink(1,22):foo@r.com]",
        "[text(1,33):a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<a href="/url" title="title">link</a><a href="mailto:foo@r.com">foo@r.com</a>a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_j_i_t_ea():
    """
    Test case:  Inline image containing text in label followed by email autolink
    """

    # Arrange
    source_markdown = """a![link](/url "title")<foo@r.com>a"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        '[image(1,2):inline:/url:title:link::::link:False:":: :]',
        "[email-autolink(1,23):foo@r.com]",
        "[text(1,34):a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<img src="/url" alt="link" title="title" /><a href="mailto:foo@r.com">foo@r.com</a>a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_j_l_t_bh():
    """
    Test case:  Inline link containing text in label followed by backslash hard break
    """

    # Arrange
    source_markdown = """a[link](/url "title")\\\na"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):a:]",
        '[link(1,2):inline:/url:title::::link:False:":: :]',
        "[text(1,3):link:]",
        "[end-link::]",
        "[hard-break(1,22):\\:\n]",
        "[text(2,1):a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<a href="/url" title="title">link</a><br />
a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_j_i_t_bh():
    """
    Test case:  Inline image containing text in label followed by backslash hard break
    """

    # Arrange
    source_markdown = """a![link](/url "title")\\\na"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):a:]",
        '[image(1,2):inline:/url:title:link::::link:False:":: :]',
        "[hard-break(1,23):\\:\n]",
        "[text(2,1):a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<img src="/url" alt="link" title="title" /><br />
a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_j_l_t_sh():
    """
    Test case:  Inline link containing text in label followed by spaces hard break
    """

    # Arrange
    source_markdown = """a[link](/url "title")   \na"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):a:]",
        '[link(1,2):inline:/url:title::::link:False:":: :]',
        "[text(1,3):link:]",
        "[end-link::]",
        "[hard-break(1,22):   :\n]",
        "[text(2,1):a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<a href="/url" title="title">link</a><br />
a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_j_i_t_sh():
    """
    Test case:  Inline image containing text in label followed by spaces hard break
    """

    # Arrange
    source_markdown = """a![link](/url "title")   \na"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):a:]",
        '[image(1,2):inline:/url:title:link::::link:False:":: :]',
        "[hard-break(1,23):   :\n]",
        "[text(2,1):a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<img src="/url" alt="link" title="title" /><br />
a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)
