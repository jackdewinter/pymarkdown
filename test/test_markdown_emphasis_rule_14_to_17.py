"""
https://github.github.com/gfm/#emphasis-and-strong-emphasis
"""
import pytest

from pymarkdown.tokenized_markdown import TokenizedMarkdown
from pymarkdown.transform_to_gfm import TransformToGfm

from .utils import (
    assert_if_lists_different,
    assert_if_strings_different,
    assert_token_consistency,
)


@pytest.mark.gfm
def test_emphasis_476():
    """
    Test case 476:  (part 1) Rule 14
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """***foo***"""
    expected_tokens = [
        "[para(1,1):]",
        "[emphasis:1:*]",
        "[emphasis:2:*]",
        "[text:foo:]",
        "[end-emphasis::2:*:False]",
        "[end-emphasis::1:*:False]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><em><strong>foo</strong></em></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_emphasis_477():
    """
    Test case 477:  (part 2) Rule 14
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """_____foo_____"""
    expected_tokens = [
        "[para(1,1):]",
        "[emphasis:1:_]",
        "[emphasis:2:_]",
        "[emphasis:2:_]",
        "[text:foo:]",
        "[end-emphasis::2:_:False]",
        "[end-emphasis::2:_:False]",
        "[end-emphasis::1:_:False]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><em><strong><strong>foo</strong></strong></em></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_emphasis_478():
    """
    Test case 478:  (part 1) Rule 15
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """*foo _bar* baz_"""
    expected_tokens = [
        "[para(1,1):]",
        "[emphasis:1:*]",
        "[text:foo :]",
        "[text:_:]",
        "[text:bar:]",
        "[end-emphasis::1:*:False]",
        "[text: baz:]",
        "[text:_:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><em>foo _bar</em> baz_</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_emphasis_479():
    """
    Test case 479:  (part 2) Rule 15
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """*foo __bar *baz bim__ bam*"""
    expected_tokens = [
        "[para(1,1):]",
        "[emphasis:1:*]",
        "[text:foo :]",
        "[emphasis:2:_]",
        "[text:bar :]",
        "[text:*:]",
        "[text:baz bim:]",
        "[end-emphasis::2:_:False]",
        "[text: bam:]",
        "[end-emphasis::1:*:False]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><em>foo <strong>bar *baz bim</strong> bam</em></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_emphasis_480():
    """
    Test case 480:  (part 1) Rule 16
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """**foo **bar baz**"""
    expected_tokens = [
        "[para(1,1):]",
        "[text:**:]",
        "[text:foo :]",
        "[emphasis:2:*]",
        "[text:bar baz:]",
        "[end-emphasis::2:*:False]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>**foo <strong>bar baz</strong></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_emphasis_481():
    """
    Test case 481:  (part 2) Rule 16
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """*foo *bar baz*"""
    expected_tokens = [
        "[para(1,1):]",
        "[text:*:]",
        "[text:foo :]",
        "[emphasis:1:*]",
        "[text:bar baz:]",
        "[end-emphasis::1:*:False]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>*foo <em>bar baz</em></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_emphasis_482():
    """
    Test case 482:  (part 1) Rule 17
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """*[bar*](/url)"""
    expected_tokens = [
        "[para(1,1):]",
        "[text:*:]",
        "[link:inline:/url:::::bar*:False::::]",
        "[text:bar:]",
        "[text:*:]",
        "[end-link:::False]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>*<a href="/url">bar*</a></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_emphasis_483():
    """
    Test case 483:  (part 2) Rule 17
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """_foo [bar_](/url)"""
    expected_tokens = [
        "[para(1,1):]",
        "[text:_:]",
        "[text:foo :]",
        "[link:inline:/url:::::bar_:False::::]",
        "[text:bar:]",
        "[text:_:]",
        "[end-link:::False]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>_foo <a href="/url">bar_</a></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_emphasis_484():
    """
    Test case 484:  (part 3) Rule 17
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """*<img src="foo" title="*"/>"""
    expected_tokens = [
        "[para(1,1):]",
        "[text:*:]",
        '[raw-html:img src="foo" title="*"/]',
        "[end-para:::True]",
    ]
    expected_gfm = """<p>*<img src="foo" title="*"/></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_emphasis_485():
    """
    Test case 485:  (part 4) Rule 17
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """**<a href="**">"""
    expected_tokens = [
        "[para(1,1):]",
        "[text:**:]",
        '[raw-html:a href="**"]',
        "[end-para:::True]",
    ]
    expected_gfm = """<p>**<a href="**"></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_emphasis_486():
    """
    Test case 486:  (part 5) Rule 17
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """__<a href="__">"""
    expected_tokens = [
        "[para(1,1):]",
        "[text:__:]",
        '[raw-html:a href="__"]',
        "[end-para:::True]",
    ]
    expected_gfm = """<p>__<a href="__"></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_emphasis_487():
    """
    Test case 487:  (part 6) Rule 17
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """*a `*`*"""
    expected_tokens = [
        "[para(1,1):]",
        "[emphasis:1:*]",
        "[text:a :]",
        "[icode-span:*:`::]",
        "[end-emphasis::1:*:False]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><em>a <code>*</code></em></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_emphasis_488():
    """
    Test case 488:  (part 7) Rule 17
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """_a `_`_"""
    expected_tokens = [
        "[para(1,1):]",
        "[emphasis:1:_]",
        "[text:a :]",
        "[icode-span:_:`::]",
        "[end-emphasis::1:_:False]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><em>a <code>_</code></em></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_emphasis_489():
    """
    Test case 489:  (part 8) Rule 17
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """**a<http://foo.bar/?q=**>"""
    expected_tokens = [
        "[para(1,1):]",
        "[text:**:]",
        "[text:a:]",
        "[uri-autolink:http://foo.bar/?q=**]",
        "[end-para:::True]",
    ]
    expected_gfm = (
        """<p>**a<a href="http://foo.bar/?q=**">http://foo.bar/?q=**</a></p>"""
    )

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_emphasis_490():
    """
    Test case 490:  (part 9) Rule 17
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """__a<http://foo.bar/?q=__>"""
    expected_tokens = [
        "[para(1,1):]",
        "[text:__:]",
        "[text:a:]",
        "[uri-autolink:http://foo.bar/?q=__]",
        "[end-para:::True]",
    ]
    expected_gfm = (
        """<p>__a<a href="http://foo.bar/?q=__">http://foo.bar/?q=__</a></p>"""
    )

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)
