"""
https://github.github.com/gfm/#entity-and-numeric-character-references
"""
import os

import pytest

from pymarkdown.bad_tokenization_error import BadTokenizationError
from pymarkdown.tokenized_markdown import TokenizedMarkdown

from .utils import (
    act_and_assert
)


@pytest.mark.gfm
def test_character_references_321():
    """
    Test case 321:  Entity references consist of & + any of the valid HTML5 entity names + ;. The document https://html.spec.whatwg.org/multipage/entities.json is used as an authoritative source for the valid entity references and their corresponding code points.
    """

    # Arrange
    source_markdown = """&nbsp; &amp; &copy; &AElig; &Dcaron;
&frac34; &HilbertSpace; &DifferentialD;
&ClockwiseContourIntegral; &ngE;"""
    expected_tokens = [
        "[para(1,1):\n\n]",
        "[text(1,1):\a&nbsp;\a\u00A0\a \a&amp;\a\a&\a&amp;\a\a \a&copy;\a©\a \a&AElig;\aÆ\a \a&Dcaron;\aĎ\a\n\a&frac34;\a¾\a \a&HilbertSpace;\aℋ\a \a&DifferentialD;\aⅆ\a\n\a&ClockwiseContourIntegral;\a∲\a \a&ngE;\a≧̸\a::\n\n]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>\u00A0 &amp; © Æ Ď
¾ ℋ ⅆ
∲ ≧̸</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_character_references_321a():
    """
    Test case 321a:  must be case sensitive
    """

    # Arrange
    source_markdown = """&ouml; &OUML;"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):\a&ouml;\aö\a \a&\a&amp;\aOUML;:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>ö &amp;OUML;</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_character_references_322():
    """
    Test case 322:  Decimal numeric character references consist of &# + a string of 1–7 arabic digits + ;. A numeric character reference is parsed as the corresponding Unicode character. Invalid Unicode code points will be replaced by the REPLACEMENT CHARACTER (U+FFFD). For security reasons, the code point U+0000 will also be replaced by U+FFFD.
    """

    # Arrange
    source_markdown = """&#35; &#1234; &#992; &#0;"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):\a&#35;\a#\a \a&#1234;\aӒ\a \a&#992;\aϠ\a \a&#0;\a�\a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p># Ӓ Ϡ �</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_character_references_323():
    """
    Test case 323:  Hexadecimal numeric character references consist of &# + either X or x + a string of 1-6 hexadecimal digits + ;. They too are parsed as the corresponding Unicode character (this time specified with a hexadecimal numeral instead of decimal).
    """

    # Arrange
    source_markdown = """&#X22; &#XD06; &#xcab;"""
    expected_tokens = [
        "[para(1,1):]",
        '[text(1,1):\a&#X22;\a\a"\a&quot;\a\a \a&#XD06;\aആ\a \a&#xcab;\aಫ\a:]',
        "[end-para:::True]",
    ]
    expected_gfm = """<p>&quot; ആ ಫ</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_character_references_323a():
    """
    Test case 323a:  code point 0
    """

    # Arrange
    source_markdown = """&#X0; &#x000000;"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):\a&#X0;\a�\a \a&#x000000;\a�\a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>� �</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_character_references_324():
    """
    Test case 324:  Here are some nonentities:
    """

    # Arrange
    source_markdown = """&nbsp &x; &#; &#x;
&#87654321;
&#abcdef0;
&ThisIsNotDefined; &hi?;"""
    expected_tokens = [
        "[para(1,1):\n\n\n]",
        "[text(1,1):\a&\a&amp;\anbsp \a&\a&amp;\ax; \a&\a&amp;\a#; \a&\a&amp;\a#x;\n\a&\a&amp;\a#87654321;\n\a&\a&amp;\a#abcdef0;\n\a&\a&amp;\aThisIsNotDefined; \a&\a&amp;\ahi?;::\n\n\n]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>&amp;nbsp &amp;x; &amp;#; &amp;#x;
&amp;#87654321;
&amp;#abcdef0;
&amp;ThisIsNotDefined; &amp;hi?;</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_character_references_324a():
    """
    Test case 324a:  Extension of 324
    """

    # Arrange
    source_markdown = """&"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):\a&\a&amp;\a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>&amp;</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_character_references_325():
    """
    Test case 325:  Although HTML5 does accept some entity references without a trailing semicolon (such as &copy), these are not recognized here, because it makes the grammar too ambiguous:
    """

    # Arrange
    source_markdown = """&copy"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):\a&\a&amp;\acopy:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>&amp;copy</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_character_references_326():
    """
    Test case 326:  Strings that are not on the list of HTML5 named entities are not recognized as entity references either:
    """

    # Arrange
    source_markdown = """&MadeUpEntity;"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):\a&\a&amp;\aMadeUpEntity;:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>&amp;MadeUpEntity;</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_character_references_327():
    """
    Test case 327:  (part 1) Entity and numeric character references are recognized in any context besides code spans or code blocks, including URLs, link titles, and fenced code block info strings:
    """

    # Arrange
    source_markdown = '<a href="&ouml;&ouml;.html">'
    expected_tokens = [
        "[html-block(1,1)]",
        '[text(1,1):<a href="&ouml;&ouml;.html">:]',
        "[end-html-block:::True]",
    ]
    expected_gfm = """<a href="&ouml;&ouml;.html">"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_character_references_328():
    """
    Test case 328:  (part 2) Entity and numeric character references are recognized in any context besides code spans or code blocks, including URLs, link titles, and fenced code block info strings:
    """

    # Arrange
    source_markdown = '[foo](/f&ouml;&ouml; "f&ouml;&ouml;")'
    expected_tokens = [
        "[para(1,1):]",
        '[link(1,1):inline:/f%C3%B6%C3%B6:föö:/f&ouml;&ouml;:f&ouml;&ouml;::foo:False:":: :]',
        "[text(1,2):foo:]",
        "[end-link:::False]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="/f%C3%B6%C3%B6" title="föö">foo</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_character_references_328a():
    """
    Test case 328a:  variation
    """

    # Arrange
    source_markdown = '[f&ouml;&ouml;](/f&ouml;&ouml; "f&ouml;&ouml;")'
    expected_tokens = [
        "[para(1,1):]",
        '[link(1,1):inline:/f%C3%B6%C3%B6:föö:/f&ouml;&ouml;:f&ouml;&ouml;::f&ouml;&ouml;:False:":: :]',
        "[text(1,2):f\a&ouml;\aö\a\a&ouml;\aö\a:]",
        "[end-link:::False]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="/f%C3%B6%C3%B6" title="föö">föö</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_character_references_329():
    """
    Test case 329:  (part 3) Entity and numeric character references are recognized in any context besides code spans or code blocks, including URLs, link titles, and fenced code block info strings:
    """

    # Arrange
    source_markdown = """[foo]

[foo]: /f&ouml;&ouml; "f&ouml;&ouml;\""""
    expected_tokens = [
        "[para(1,1):]",
        "[link(1,1):shortcut:/f%C3%B6%C3%B6:föö::::foo:::::]",
        "[text(1,2):foo:]",
        "[end-link:::False]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        '[link-ref-def(3,1):True::foo:: :/f%C3%B6%C3%B6:/f&ouml;&ouml;: :föö:"f&ouml;&ouml;":]',
    ]
    expected_gfm = """<p><a href="/f%C3%B6%C3%B6" title="föö">foo</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_character_references_330():
    """
    Test case 330:  (part 4) Entity and numeric character references are recognized in any context besides code spans or code blocks, including URLs, link titles, and fenced code block info strings:
    """

    # Arrange
    source_markdown = """``` f&ouml;&ouml;
foo
```
"""
    expected_tokens = [
        "[fcode-block(1,1):`:3:föö:f&ouml;&ouml;:::: ]",
        "[text(2,1):foo:]",
        "[end-fcode-block::3:False]",
        "[BLANK(4,1):]",
    ]
    expected_gfm = """<pre><code class="language-föö">foo
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_character_references_331():
    """
    Test case 331:  (part 1) Entity and numeric character references are treated as literal text in code spans and code blocks:
    """

    # Arrange
    source_markdown = """`f&ouml;&ouml;`"""
    expected_tokens = [
        "[para(1,1):]",
        "[icode-span(1,1):f\a&\a&amp;\aouml;\a&\a&amp;\aouml;:`::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><code>f&amp;ouml;&amp;ouml;</code></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_character_references_332():
    """
    Test case 332:  (part 2) Entity and numeric character references are treated as literal text in code spans and code blocks:
    """

    # Arrange
    source_markdown = """    f&ouml;f&ouml;"""
    expected_tokens = [
        "[icode-block(1,5):    :]",
        "[text(1,5):f\a&\a&amp;\aouml;f\a&\a&amp;\aouml;:]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<pre><code>f&amp;ouml;f&amp;ouml;
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_character_references_333():
    """
    Test case 333:  (part 1) Entity and numeric character references cannot be used in place of symbols indicating structure in CommonMark documents.
    """

    # Arrange
    source_markdown = """&#42;foo&#42;
*foo*"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):\a&#42;\a*\afoo\a&#42;\a*\a\n::\n]",
        "[emphasis(2,1):1:*]",
        "[text(2,2):foo:]",
        "[end-emphasis(2,5)::1:*:False]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>*foo*
<em>foo</em></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_character_references_334():
    """
    Test case 334:  (part 2) Entity and numeric character references cannot be used in place of symbols indicating structure in CommonMark documents.
    """

    # Arrange
    source_markdown = """&#42; foo

* foo"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):\a&#42;\a*\a foo:]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[ulist(3,1):*::2:]",
        "[para(3,3):]",
        "[text(3,3):foo:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<p>* foo</p>
<ul>
<li>foo</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_character_references_335():
    """
    Test case 335:  (part 3) Entity and numeric character references cannot be used in place of symbols indicating structure in CommonMark documents.
    """

    # Arrange
    source_markdown = """foo&#10;&#10;bar"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):foo\a&#10;\a\n\a\a&#10;\a\n\abar:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>foo

bar</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_character_references_336():
    """
    Test case 336:  (part 4) Entity and numeric character references cannot be used in place of symbols indicating structure in CommonMark documents.
    """

    # Arrange
    source_markdown = """&#9;foo"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):\a&#9;\a\t\afoo:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>\tfoo</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_character_references_336a():
    """
    Test case 336a:  variations
    """

    # Arrange
    source_markdown = """# F&ouml;o"""
    expected_tokens = [
        "[atx(1,1):1:0:]",
        "[text(1,3):F\a&ouml;\aö\ao: ]",
        "[end-atx:::False]",
    ]
    expected_gfm = """<h1>Föo</h1>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_character_references_336b():
    """
    Test case 336b:  variations
    """

    # Arrange
    source_markdown = """F&ouml;o
---"""
    expected_tokens = [
        "[setext(2,1):-:3::(1,1)]",
        "[text(1,1):F\a&ouml;\aö\ao:]",
        "[end-setext:::False]",
    ]
    expected_gfm = """<h2>Föo</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_character_references_336c():
    """
    Test case 336c:  variations
    """

    # Arrange
    source_markdown = """    F&ouml;o"""
    expected_tokens = [
        "[icode-block(1,5):    :]",
        "[text(1,5):F\a&\a&amp;\aouml;o:]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<pre><code>F&amp;ouml;o
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_character_references_336d():
    """
    Test case 336d:  variations
    """

    # Arrange
    source_markdown = """```text
F&ouml;o
```"""
    expected_tokens = [
        "[fcode-block(1,1):`:3:text:::::]",
        "[text(2,1):F\a&\a&amp;\aouml;o:]",
        "[end-fcode-block::3:False]",
    ]
    expected_gfm = """<pre><code class="language-text">F&amp;ouml;o
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_character_references_336e():
    """
    Test case 336e:  variations
    """

    # Arrange
    source_markdown = """<script>
F&ouml;o
</script>"""
    expected_tokens = [
        "[html-block(1,1)]",
        "[text(1,1):<script>\nF&ouml;o\n</script>:]",
        "[end-html-block:::False]",
    ]
    expected_gfm = """<script>
F&ouml;o
</script>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_character_references_337():
    """
    Test case 337:  (part 5) Entity and numeric character references cannot be used in place of symbols indicating structure in CommonMark documents.
    """

    # Arrange
    source_markdown = """[a](url &quot;tit&quot;)"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):[:]",
        "[text(1,2):a:]",
        "[text(1,3):]:]",
        '[text(1,4):(url \a&quot;\a\a"\a&quot;\a\atit\a&quot;\a\a"\a&quot;\a\a):]',
        "[end-para:::True]",
    ]
    expected_gfm = """<p>[a](url &quot;tit&quot;)</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_character_references_extra_01():
    """
    Test case extra 1:  various
    """

    # Arrange
    source_markdown = """&quot;this is cool!&quot;)"""
    expected_tokens = [
        "[para(1,1):]",
        '[text(1,1):\a&quot;\a\a"\a&quot;\a\athis is cool!\a&quot;\a\a"\a&quot;\a\a):]',
        "[end-para:::True]",
    ]
    expected_gfm = """<p>&quot;this is cool!&quot;)</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_character_references_extra_02():
    """
    Test case extra 2:  various
    """

    # Arrange
    source_markdown = """&#34;this is cool!&#34;)"""
    expected_tokens = [
        "[para(1,1):]",
        '[text(1,1):\a&#34;\a\a"\a&quot;\a\athis is cool!\a&#34;\a\a"\a&quot;\a\a):]',
        "[end-para:::True]",
    ]
    expected_gfm = """<p>&quot;this is cool!&quot;)</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_character_references_extra_03():
    """
    Test case extra 3:  various
    """

    # Arrange
    source_markdown = """&#x22;this is cool!&#x22;)"""
    expected_tokens = [
        "[para(1,1):]",
        '[text(1,1):\a&#x22;\a\a"\a&quot;\a\athis is cool!\a&#x22;\a\a"\a&quot;\a\a):]',
        "[end-para:::True]",
    ]
    expected_gfm = """<p>&quot;this is cool!&quot;)</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


def test_missing_entities_json_file():
    """
    Test the entities.json not being present in the specified directory.
    """

    alternate_resource_path = "bob"

    try:
        TokenizedMarkdown(resource_path=alternate_resource_path)

        assert False, "Should have exited prior to this."
    except BadTokenizationError as this_exception:
        assert str(this_exception).startswith(
            "Named character entity map file '"
            + alternate_resource_path
            + "\\entities.json' was not loaded ([Errno 2] No such file or directory: '"
        )


def test_bad_entities_json_file():
    """
    Test the entities.json not being a valid json file in the specified directory.
    """

    alternate_resource_path = os.path.join(os.path.split(__file__)[0], "resources")
    full_alternate_resource_path = os.path.abspath(alternate_resource_path)

    try:
        TokenizedMarkdown(resource_path=alternate_resource_path)

        assert False, "Should have exited prior to this."
    except BadTokenizationError as this_exception:
        assert (
            str(this_exception)
            == "Named character entity map file '"
            + full_alternate_resource_path
            + "\\entities.json' is not a valid JSON file (Expecting value: line 1 column 1 (char 0))."
        )
