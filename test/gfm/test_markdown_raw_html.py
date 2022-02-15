"""
https://github.github.com/gfm/#raw-html
"""

from test.utils import act_and_assert

import pytest


@pytest.mark.gfm
def test_raw_html_632():
    """
    Test case 632:  Here are some simple open tags:
    """

    # Arrange
    source_markdown = """<a><bab><c2c>"""
    expected_tokens = [
        "[para(1,1):]",
        "[raw-html(1,1):a]",
        "[raw-html(1,4):bab]",
        "[raw-html(1,9):c2c]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a><bab><c2c></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_raw_html_632a():
    """
    Test case 632a:  variation of 632 with text between tags
    """

    # Arrange
    source_markdown = """each <a> tag <bab> is <c2c> different"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):each :]",
        "[raw-html(1,6):a]",
        "[text(1,9): tag :]",
        "[raw-html(1,14):bab]",
        "[text(1,19): is :]",
        "[raw-html(1,23):c2c]",
        "[text(1,28): different:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>each <a> tag <bab> is <c2c> different</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_raw_html_633():
    """
    Test case 633:  Empty elements:
    """

    # Arrange
    source_markdown = """<a/><b2/>"""
    expected_tokens = [
        "[para(1,1):]",
        "[raw-html(1,1):a/]",
        "[raw-html(1,5):b2/]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a/><b2/></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_raw_html_634():
    """
    Test case 634:  Whitespace is allowed:
    """

    # Arrange
    source_markdown = """<a  /><b2
data="foo" >"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[raw-html(1,1):a  /]",
        '[raw-html(1,7):b2\ndata="foo" ]',
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a  /><b2
data="foo" ></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_raw_html_634a():
    """
    Test case 634a:  variation of 634 in list
    """

    # Arrange
    source_markdown = """- <a  /><b2
data="foo" ><c>"""
    expected_tokens = [
        "[ulist(1,1):-::2::]",
        "[para(1,3):\n]",
        "[raw-html(1,3):a  /]",
        '[raw-html(1,9):b2\ndata="foo" ]',
        "[raw-html(2,13):c]",
        "[end-para:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li><a  /><b2
data="foo" ><c></li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_raw_html_634bx():
    """
    Test case 634b:  variation of 634 in block quote
    """

    # Arrange
    source_markdown = """> <a  /><b2
data="foo" ><c>"""
    expected_tokens = [
        "[block-quote(1,1)::> \n]",
        "[para(1,3):\n]",
        "[raw-html(1,3):a  /]",
        '[raw-html(1,9):b2\ndata="foo" ]',
        "[raw-html(2,13):c]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p><a  /><b2
data="foo" ><c></p>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_raw_html_634ba():
    """
    Test case 634ba:  variation of 634 in block quote
    """

    # Arrange
    source_markdown = """> <a  /><b2
> data="foo" ><c>"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> ]",
        "[para(1,3):\n]",
        "[raw-html(1,3):a  /]",
        '[raw-html(1,9):b2\ndata="foo" ]',
        "[raw-html(2,15):c]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p><a  /><b2
data="foo" ><c></p>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_raw_html_634bb():
    """
    Test case 634bb:  variation of 634 in block quote
    """

    # Arrange
    source_markdown = """> <a  /><b2
>   data="foo" ><c>"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> ]",
        "[para(1,3):\n  ]",
        "[raw-html(1,3):a  /]",
        '[raw-html(1,9):b2\n\a  \a\x03\adata="foo" ]',
        "[raw-html(2,17):c]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p><a  /><b2
data="foo" ><c></p>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_raw_html_634c():
    """
    Test case 634c:  variation of 634 in setext
    """

    # Arrange
    source_markdown = """<a  /><b2
data="foo" ><c>
---"""
    expected_tokens = [
        "[setext(3,1):-:3::(1,1)]",
        "[raw-html(1,1):a  /]",
        '[raw-html(1,7):b2\ndata="foo" ]',
        "[raw-html(2,13):c]",
        "[end-setext::]",
    ]
    expected_gfm = """<h2><a  /><b2
data="foo" ><c></h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_raw_html_634d():
    """
    Test case 634c:  variation of 634 in atx
    """

    # Arrange
    source_markdown = """# <a  /><b2
data="foo" ><c>"""
    expected_tokens = [
        "[atx(1,1):1:0:]",
        "[text(1,3)::\a \a\x03\a]",
        "[raw-html(1,3):a  /]",
        "[text(1,9):\a<\a&lt;\ab2:]",
        "[end-atx::]",
        "[para(2,1):]",
        '[text(2,1):data=\a"\a&quot;\afoo\a"\a&quot;\a \a>\a&gt;\a:]',
        "[raw-html(2,13):c]",
        "[end-para:::True]",
    ]
    expected_gfm = """<h1><a  />&lt;b2</h1>
<p>data=&quot;foo&quot; &gt;<c></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_raw_html_635():
    """
    Test case 635:  With attributes:
    """

    # Arrange
    source_markdown = """<a foo="bar" bam = 'baz <em>"</em>'
_boolean zoop:33=zoop:33 />"""
    expected_tokens = [
        "[para(1,1):\n]",
        """[raw-html(1,1):a foo="bar" bam = 'baz <em>"</em>'
_boolean zoop:33=zoop:33 /]""",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a foo="bar" bam = 'baz <em>"</em>'
_boolean zoop:33=zoop:33 /></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_raw_html_636():
    """
    Test case 636:  Custom tag names can be used:
    """

    # Arrange
    source_markdown = """Foo <responsive-image src="foo.jpg" />"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):Foo :]",
        '[raw-html(1,5):responsive-image src="foo.jpg" /]',
        "[end-para:::True]",
    ]
    expected_gfm = """<p>Foo <responsive-image src="foo.jpg" /></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_raw_html_637():
    """
    Test case 637:  Illegal tag names, not parsed as HTML:
    """

    # Arrange
    source_markdown = """<33> <__>"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):\a<\a&lt;\a33\a>\a&gt;\a \a<\a&lt;\a:]",
        "[text(1,7):__:]",
        "[text(1,9):\a>\a&gt;\a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>&lt;33&gt; &lt;__&gt;</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_raw_html_638():
    """
    Test case 638:  Illegal attribute names:
    """

    # Arrange
    source_markdown = """<a h*#ref="hi">"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):\a<\a&lt;\aa h:]",
        "[text(1,5):*:]",
        '[text(1,6):#ref=\a"\a&quot;\ahi\a"\a&quot;\a\a>\a&gt;\a:]',
        "[end-para:::True]",
    ]
    expected_gfm = """<p>&lt;a h*#ref=&quot;hi&quot;&gt;</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_raw_html_639():
    """
    Test case 639:  Illegal attribute values:
    """

    # Arrange
    source_markdown = """<a href="hi'> <a href=hi'>"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):\a<\a&lt;\aa href=\a\"\a&quot;\ahi'\a>\a&gt;\a \a<\a&lt;\aa href=hi'\a>\a&gt;\a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>&lt;a href=&quot;hi'&gt; &lt;a href=hi'&gt;</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_raw_html_639a():
    """
    Test case 639a:  Illegal attribute values:
    """

    # Arrange
    source_markdown = """<a href='hi"> <a href=hi">"""
    expected_tokens = [
        "[para(1,1):]",
        '[text(1,1):\a<\a&lt;\aa href=\'hi\a"\a&quot;\a\a>\a&gt;\a \a<\a&lt;\aa href=hi\a"\a&quot;\a\a>\a&gt;\a:]',
        "[end-para:::True]",
    ]
    expected_gfm = """<p>&lt;a href='hi&quot;&gt; &lt;a href=hi&quot;&gt;</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_raw_html_640():
    """
    Test case 640:  Illegal whitespace:
    """

    # Arrange
    source_markdown = """< a><
foo><bar/ >
<foo bar=baz
bim!bop />"""
    expected_tokens = [
        "[para(1,1):\n\n\n]",
        "[text(1,1):\a<\a&lt;\a a\a>\a&gt;\a\a<\a&lt;\a\nfoo\a>\a&gt;\a\a<\a&lt;\abar/ \a>\a&gt;\a\n\a<\a&lt;\afoo bar=baz\nbim!bop /\a>\a&gt;\a::\n\n\n]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>&lt; a&gt;&lt;
foo&gt;&lt;bar/ &gt;
&lt;foo bar=baz
bim!bop /&gt;</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_raw_html_641():
    """
    Test case 641:  Missing whitespace:
    """

    # Arrange
    source_markdown = """<a href='bar'title=title>"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):\a<\a&lt;\aa href='bar'title=title\a>\a&gt;\a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>&lt;a href='bar'title=title&gt;</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_raw_html_642():
    """
    Test case 642:  Closing tags:
    """

    # Arrange
    source_markdown = """</a></foo >"""
    expected_tokens = [
        "[para(1,1):]",
        "[raw-html(1,1):/a]",
        "[raw-html(1,5):/foo ]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p></a></foo ></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_raw_html_642a():
    """
    Test case 642a:  variation on 642 with a closing tag character without a valid closing tag name
    """

    # Arrange
    source_markdown = """</>"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):\a<\a&lt;\a/\a>\a&gt;\a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>&lt;/&gt;</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_raw_html_643():
    """
    Test case 643:  Illegal attributes in closing tag:
    """

    # Arrange
    source_markdown = """</a href="foo">"""
    expected_tokens = [
        "[para(1,1):]",
        '[text(1,1):\a<\a&lt;\a/a href=\a"\a&quot;\afoo\a"\a&quot;\a\a>\a&gt;\a:]',
        "[end-para:::True]",
    ]
    expected_gfm = """<p>&lt;/a href=&quot;foo&quot;&gt;</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_raw_html_644():
    """
    Test case 644:  (part 1) Comments:
    """

    # Arrange
    source_markdown = """foo <!-- this is a
comment - with hyphen -->"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):foo :]",
        "[raw-html(1,5):!-- this is a\ncomment - with hyphen --]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>foo <!-- this is a
comment - with hyphen --></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_raw_html_644a():
    """
    Test case 644a:  variation of 644 with extra indent
    """

    # Arrange
    source_markdown = """foo <!-- this is a
 comment - with hyphen -->"""
    expected_tokens = [
        "[para(1,1):\n ]",
        "[text(1,1):foo :]",
        "[raw-html(1,5):!-- this is a\n\a \a\x03\acomment - with hyphen --]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>foo <!-- this is a
comment - with hyphen --></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_raw_html_644aa():
    """
    Test case 644a:  variation of 644 with extra indent and trailing text
    """

    # Arrange
    source_markdown = """foo <!-- this is a
 comment - with hyphen -->bar"""
    expected_tokens = [
        "[para(1,1):\n ]",
        "[text(1,1):foo :]",
        "[raw-html(1,5):!-- this is a\n\a \a\x03\acomment - with hyphen --]",
        "[text(2,27):bar:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>foo <!-- this is a
comment - with hyphen -->bar</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_raw_html_644b():
    """
    Test case 644b:  variation of 644 with extra indent and trailing text
    """

    # Arrange
    source_markdown = """foo <!-- this is a
 comment - with hyphen -->  foo
bar"""
    expected_tokens = [
        "[para(1,1):\n \n]",
        "[text(1,1):foo :]",
        "[raw-html(1,5):!-- this is a\n\a \a\x03\acomment - with hyphen --]",
        "[text(2,27):  foo\nbar::\n]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>foo <!-- this is a
comment - with hyphen -->  foo
bar</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_raw_html_644c():
    """
    Test case 644c:  variation of 644 with comment text
    """

    # Arrange
    source_markdown = """foo <!--
this is a
comment - with hyphen
-->bar"""
    expected_tokens = [
        "[para(1,1):\n\n\n]",
        "[text(1,1):foo :]",
        "[raw-html(1,5):!--\nthis is a\ncomment - with hyphen\n--]",
        "[text(4,4):bar:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>foo <!--
this is a
comment - with hyphen
-->bar</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_raw_html_645():
    """
    Test case 645:  (part 2) Comments:
    """

    # Arrange
    source_markdown = """foo <!-- not a comment -- two hyphens -->"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):foo \a<\a&lt;\a!-- not a comment -- two hyphens --\a>\a&gt;\a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>foo &lt;!-- not a comment -- two hyphens --&gt;</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_raw_html_646():
    """
    Test case 646:  Not comments:
    """

    # Arrange
    source_markdown = """foo <!--> foo -->

foo <!-- foo--->"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):foo \a<\a&lt;\a!--\a>\a&gt;\a foo --\a>\a&gt;\a:]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[para(3,1):]",
        "[text(3,1):foo \a<\a&lt;\a!-- foo---\a>\a&gt;\a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>foo &lt;!--&gt; foo --&gt;</p>
<p>foo &lt;!-- foo---&gt;</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_raw_html_646a():
    """
    Test case 646a:  Not comments:
    """

    # Arrange
    source_markdown = """foo <![CDATA[>&<>"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):foo \a<\a&lt;\a:]",
        "[text(1,6):![:]",
        "[text(1,8):CDATA:]",
        "[text(1,13):[:]",
        "[text(1,14):\a>\a&gt;\a\a&\a&amp;\a\a<\a&lt;\a\a>\a&gt;\a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>foo &lt;![CDATA[&gt;&amp;&lt;&gt;</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_raw_html_647():
    """
    Test case 647:  Processing instructions:
    """

    # Arrange
    source_markdown = """foo <?php echo $a; ?>"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):foo :]",
        "[raw-html(1,5):?php echo $a; ?]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>foo <?php echo $a; ?></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_raw_html_648():
    """
    Test case 648:  Declarations:
    """

    # Arrange
    source_markdown = """foo <!ELEMENT br EMPTY>"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):foo :]",
        "[raw-html(1,5):!ELEMENT br EMPTY]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>foo <!ELEMENT br EMPTY></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_raw_html_648a():
    """
    Test case 648a:  variation of 644 with shorter
    """

    # Arrange
    source_markdown = """foo <!ELEMENT>"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):foo \a<\a&lt;\a!ELEMENT\a>\a&gt;\a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>foo &lt;!ELEMENT&gt;</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_raw_html_649():
    """
    Test case 649:  CDATA sections:
    """

    # Arrange
    source_markdown = """foo <![CDATA[>&<]]>"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):foo :]",
        "[raw-html(1,5):![CDATA[>&<]]]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>foo <![CDATA[>&<]]></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_raw_html_650():
    """
    Test case 650:  Entity and numeric character references are preserved in HTML attributes:
    """

    # Arrange
    source_markdown = """foo <a href="&ouml;">"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):foo :]",
        '[raw-html(1,5):a href="&ouml;"]',
        "[end-para:::True]",
    ]
    expected_gfm = """<p>foo <a href="&ouml;"></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_raw_html_651():
    """
    Test case 651:  (part 1) Backslash escapes do not work in HTML attributes:
    """

    # Arrange
    source_markdown = """foo <a href="\\*">"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):foo :]",
        '[raw-html(1,5):a href="\\*"]',
        "[end-para:::True]",
    ]
    expected_gfm = """<p>foo <a href="\\*"></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_raw_html_652():
    """
    Test case 652:  (part 2) Backslash escapes do not work in HTML attributes:
    """

    # Arrange
    source_markdown = """<a href="\\"">"""
    expected_tokens = [
        "[para(1,1):]",
        '[text(1,1):\a<\a&lt;\aa href=\a"\a&quot;\a\\\b\a"\a&quot;\a\a"\a&quot;\a\a>\a&gt;\a:]',
        "[end-para:::True]",
    ]
    expected_gfm = """<p>&lt;a href=&quot;&quot;&quot;&gt;</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)
