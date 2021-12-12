"""
https://github.github.com/gfm/#code-spans
"""

import pytest

from .utils import act_and_assert


@pytest.mark.gfm
def test_code_spans_338():
    """
    Test case 338:  This is a simple code span:
    """

    # Arrange
    source_markdown = """`foo`"""
    expected_tokens = [
        "[para(1,1):]",
        "[icode-span(1,1):foo:`::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><code>foo</code></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_code_spans_339():
    """
    Test case 339:  Here two backticks are used, because the code contains a backtick.
                    This example also illustrates stripping of a single leading
                    and trailing space:
    """

    # Arrange
    source_markdown = """`` foo ` bar ``"""
    expected_tokens = [
        "[para(1,1):]",
        "[icode-span(1,1):foo ` bar:``: : ]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><code>foo ` bar</code></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_code_spans_340():
    """
    Test case 340:  This example shows the motivation for stripping leading and trailing spaces:
    """

    # Arrange
    source_markdown = """` `` `"""
    expected_tokens = [
        "[para(1,1):]",
        "[icode-span(1,1):``:`: : ]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><code>``</code></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_code_spans_341():
    """
    Test case 341:  Note that only one space is stripped:
    """

    # Arrange
    source_markdown = """`  ``  `"""
    expected_tokens = [
        "[para(1,1):]",
        "[icode-span(1,1): `` :`: : ]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><code> `` </code></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_code_spans_342():
    """
    Test case 342:  The stripping only happens if the space is on both sides of the string:
    """

    # Arrange
    source_markdown = """` a`"""
    expected_tokens = [
        "[para(1,1):]",
        "[icode-span(1,1): a:`::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><code> a</code></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_code_spans_343():
    """
    Test case 343:  Only spaces, and not unicode whitespace in general, are stripped in this way:
    """

    # Arrange
    source_markdown = """`\u00A0b\u00A0`"""
    expected_tokens = [
        "[para(1,1):]",
        "[icode-span(1,1):\u00A0b\u00A0:`::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><code>\u00A0b\u00A0</code></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_code_spans_344():
    """
    Test case 344:  No stripping occurs if the code span contains only spaces:
    """

    # Arrange
    source_markdown = """` `
`  `"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[icode-span(1,1): :`::]",
        "[text(1,4):\n::\n]",
        "[icode-span(2,1):  :`::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><code> </code>
<code>  </code></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_code_spans_344a():
    """
    Test case 344a:  variation of 344 with a whitespace string that is longer than 2.
    """

    # Arrange
    source_markdown = """`   `"""
    expected_tokens = [
        "[para(1,1):]",
        "[icode-span(1,1):   :`::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><code>   </code></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_code_spans_345():
    """
    Test case 345:  (part 1) Line endings are treated like spaces:
    """

    # Arrange
    source_markdown = """``
foo
bar\a\a
baz
``""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[para(1,1):\n\n\n\n]",
        "[icode-span(1,1):foo\a\n\a \abar  \a\n\a \abaz:``:\a\n\a \a:\a\n\a \a]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><code>foo bar   baz</code></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_code_spans_345a():
    """
    Test case 345a:  variation of 345 with extra indentation
    """

    # Arrange
    source_markdown = """``
 foo
  bar\a\a
baz
``""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[para(1,1):\n \n  \n\n]",
        "[icode-span(1,1):foo\a\n\a \abar  \a\n\a \abaz:``:\a\n\a \a:\a\n\a \a]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><code>foo bar   baz</code></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_code_spans_345b():
    """
    Test case 345b:  variation of 345 over a single newline
    """

    # Arrange
    source_markdown = """``this is
a code span``"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[icode-span(1,1):this is\a\n\a \aa code span:``::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><code>this is a code span</code></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_code_spans_346():
    """
    Test case 346:  (part 2) Line endings are treated like spaces:
    """

    # Arrange
    source_markdown = """``
foo 
``"""
    expected_tokens = [
        "[para(1,1):\n\n]",
        "[icode-span(1,1):foo :``:\a\n\a \a:\a\n\a \a]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><code>foo </code></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_code_spans_346ax():
    """
    Test case 346a:  variation of 346 within a list with no indentation
    """

    # Arrange
    source_markdown = """- ``
foo\a
``""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[ulist(1,1):-::2::\n]",
        "[para(1,3):\n\n]",
        "[icode-span(1,3):foo :``:\a\n\a \a:\a\n\a \a]",
        "[end-para:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li><code>foo </code></li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_code_spans_346aa():
    """
    Test case 346aa:  variation of 346a within a list with indentation
    """

    # Arrange
    source_markdown = """- ``
  foo\a
  ``""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[ulist(1,1):-::2::  \n  ]",
        "[para(1,3):\n\n]",
        "[icode-span(1,3):foo :``:\a\n\a \a:\a\n\a \a]",
        "[end-para:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li><code>foo </code></li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_code_spans_346bx():
    """
    Test case 346b:  variation of 346 within a block quote with no indentation
    """

    # Arrange
    source_markdown = """> ``
foo 
``"""
    expected_tokens = [
        "[block-quote(1,1)::> \n\n]",
        "[para(1,3):\n\n]",
        "[icode-span(1,3):foo :``:\a\n\a \a:\a\n\a \a]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p><code>foo </code></p>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_code_spans_346ba():
    """
    Test case 346ba:  variation of 346b within a block quote with
        block quotes indentation
    """

    # Arrange
    source_markdown = """> ``
> foo\a
> ``""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> ]",
        "[para(1,3):\n\n]",
        "[icode-span(1,3):foo :``:\a\n\a \a:\a\n\a \a]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p><code>foo </code></p>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_code_spans_346bb():
    """
    Test case 346ba:  variation of 346b within a block quote with
        block quotes indentation
    """

    # Arrange
    source_markdown = """start
> ``
> foo\a
> ``""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):start:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> \n> \n> ]",
        "[para(2,3):\n\n]",
        "[icode-span(2,3):foo :``:\a\n\a \a:\a\n\a \a]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<p>start</p>
<blockquote>
<p><code>foo </code></p>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_code_spans_346c():
    """
    Test case 346c:  variation of 346 within a link label
    """

    # Arrange
    source_markdown = """a[a``
foo\a
``a](/uri)a""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[para(1,1):\n\n]",
        "[text(1,1):a:]",
        "[link(1,2):inline:/uri:::::a``\nfoo \n``a:False::::]",
        "[text(1,3):a:]",
        "[icode-span(1,4):foo :``:\a\n\a \a:\a\n\a \a]",
        "[text(3,3):a:]",
        "[end-link::]",
        "[text(3,11):a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<a href="/uri">a<code>foo </code>a</a>a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_code_spans_346ca():
    """
    Test case 346c:  variation of 346c with extra space
    """

    # Arrange
    source_markdown = """a[a``
 foo\a
 ``a](/uri)a""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[para(1,1):\n \n ]",
        "[text(1,1):a:]",
        "[link(1,2):inline:/uri:::::a``\nfoo \n``a:False::::]",
        "[text(1,3):a:]",
        "[icode-span(1,4):foo :``:\a\n\a \a:\a\n\a \a]",
        "[text(3,3):a:]",
        "[end-link::]",
        "[text(3,11):a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<a href="/uri">a<code>foo </code>a</a>a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_code_spans_346d():
    """
    Test case 346:  variation of 346 within a setext heading
    """

    # Arrange
    source_markdown = """a``
foo 
``a
---"""
    expected_tokens = [
        "[setext(4,1):-:3::(1,1)]",
        "[text(1,1):a:]",
        "[icode-span(1,2):foo :``:\a\n\a \a:\a\n\a \a]",
        "[text(3,3):a:]",
        "[end-setext::]",
    ]
    expected_gfm = """<h2>a<code>foo </code>a</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_code_spans_347():
    """
    Test case 347:  Interior spaces are not collapsed:
    """

    # Arrange
    source_markdown = """`foo   bar\a
baz`""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[para(1,1):\n]",
        "[icode-span(1,1):foo   bar \a\n\a \abaz:`::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><code>foo   bar  baz</code></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_code_spans_348():
    """
    Test case 348:  Note that backslash escapes do not work in code spans. All backslashes are treated literally:
    """

    # Arrange
    source_markdown = """`foo\\`bar`"""
    expected_tokens = [
        "[para(1,1):]",
        "[icode-span(1,1):foo\\:`::]",
        "[text(1,7):bar`:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><code>foo\\</code>bar`</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_code_spans_349():
    """
    Test case 349:  (part 1) Backslash escapes are never needed, because one can
                    always choose a string of n backtick characters as delimiters,
                    where the code does not contain any strings of exactly n
                    backtick characters.
    """

    # Arrange
    source_markdown = """``foo`bar``"""
    expected_tokens = [
        "[para(1,1):]",
        "[icode-span(1,1):foo`bar:``::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><code>foo`bar</code></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_code_spans_350():
    """
    Test case 350:  (part 2) Backslash escapes are never needed, because one can
                    always choose a string of n backtick characters as delimiters,
                    where the code does not contain any strings of exactly n backtick
                    characters.
    """

    # Arrange
    source_markdown = """` foo `` bar `"""
    expected_tokens = [
        "[para(1,1):]",
        "[icode-span(1,1):foo `` bar:`: : ]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><code>foo `` bar</code></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_code_spans_351():
    """
    Test case 351:  Code span backticks have higher precedence than any other inline
                    constructs except HTML tags and autolinks.
    """

    # Arrange
    source_markdown = """*foo`*`"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):*:]",
        "[text(1,2):foo:]",
        "[icode-span(1,5):*:`::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>*foo<code>*</code></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_code_spans_352():
    """
    Test case 352:  And this is not parsed as a link:
    """

    # Arrange
    source_markdown = """[not a `link](/foo`)"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):[:]",
        "[text(1,2):not a :]",
        "[icode-span(1,8):link](/foo:`::]",
        "[text(1,20):):]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>[not a <code>link](/foo</code>)</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_code_spans_353():
    """
    Test case 353:  Code spans, HTML tags, and autolinks have the same precedence. Thus, this is code:
    """

    # Arrange
    source_markdown = """`<a href="`">`"""
    expected_tokens = [
        "[para(1,1):]",
        '[icode-span(1,1):\a<\a&lt;\aa href=\a"\a&quot;\a:`::]',
        '[text(1,12):\a"\a&quot;\a\a>\a&gt;\a`:]',
        "[end-para:::True]",
    ]
    expected_gfm = """<p><code>&lt;a href=&quot;</code>&quot;&gt;`</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_code_spans_354():
    """
    Test case 354:  But this is an HTML tag:
    """

    # Arrange
    source_markdown = """<a href="`">`"""
    expected_tokens = [
        "[para(1,1):]",
        '[raw-html(1,1):a href="`"]',
        "[text(1,13):`:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="`">`</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_code_spans_355():
    """
    Test case 355:  And this is code:
    """

    # Arrange
    source_markdown = """`<http://foo.bar.`baz>`"""
    expected_tokens = [
        "[para(1,1):]",
        "[icode-span(1,1):\a<\a&lt;\ahttp://foo.bar.:`::]",
        "[text(1,19):baz\a>\a&gt;\a`:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><code>&lt;http://foo.bar.</code>baz&gt;`</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_code_spans_356():
    """
    Test case 356:  But this is an autolink:
    """

    # Arrange
    source_markdown = """<http://foo.bar.`baz>`"""
    expected_tokens = [
        "[para(1,1):]",
        "[uri-autolink(1,1):http://foo.bar.`baz]",
        "[text(1,22):`:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="http://foo.bar.%60baz">http://foo.bar.`baz</a>`</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_code_spans_357():
    """
    Test case 357:  (part 1) When a backtick string is not closed by a matching
                    backtick string, we just have literal backticks:
    """

    # Arrange
    source_markdown = """```foo``"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):```foo``:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>```foo``</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_code_spans_358():
    """
    Test case 358:  (part 2) When a backtick string is not closed by a matching
                    backtick string, we just have literal backticks:
    """

    # Arrange
    source_markdown = """`foo"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):`foo:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>`foo</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_code_spans_359():
    """
    Test case 359:  The following case also illustrates the need for opening and
                    closing backtick strings to be equal in length:
    """

    # Arrange
    source_markdown = """`foo``bar``"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):`foo:]",
        "[icode-span(1,5):bar:``::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>`foo<code>bar</code></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_code_spans_extra_01():
    """
    Test case extra 01: test case with text before, during, and after
        the code span, which goes over two lines
    """

    # Arrange
    source_markdown = """aa``` a
a ```aa
foo"""
    expected_tokens = [
        "[para(1,1):\n\n]",
        "[text(1,1):aa:]",
        "[icode-span(1,3):a\a\n\a \aa:```: : ]",
        "[text(2,6):aa\nfoo::\n]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>aa<code>a a</code>aa
foo</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_code_spans_extra_02():
    """
    Test case 02:  Paragraph with single code span start and no space outside and inside
    """

    # Arrange
    source_markdown = """aa`aa`aa"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):aa:]",
        "[icode-span(1,3):aa:`::]",
        "[text(1,7):aa:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>aa<code>aa</code>aa</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_code_spans_extra_03():
    """
    Test case 03:  Paragraph with double code span start and one space outside and inside
    """

    # Arrange
    source_markdown = """aa `` aa `` aa"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):aa :]",
        "[icode-span(1,4):aa:``: : ]",
        "[text(1,12): aa:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>aa <code>aa</code> aa</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_code_spans_extra_04():
    """
    Test case 04:  Paragraph with triple code span start and three spaces outside and inside
    """

    # Arrange
    source_markdown = """aa  ```  aa  ```  aa"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):aa  :]",
        "[icode-span(1,5): aa :```: : ]",
        "[text(1,17):  aa:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>aa  <code> aa </code>  aa</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)
