"""
https://github.github.com/gfm/#emphasis-and-strong-emphasis
"""

from test.utils import act_and_assert

import pytest


@pytest.mark.gfm
def test_emphasis_476():
    """
    Test case 476:  (part 1) Rule 14
    """

    # Arrange
    source_markdown = """***foo***"""
    expected_tokens = [
        "[para(1,1):]",
        "[emphasis(1,1):1:*]",
        "[emphasis(1,2):2:*]",
        "[text(1,4):foo:]",
        "[end-emphasis(1,7)::]",
        "[end-emphasis(1,9)::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><em><strong>foo</strong></em></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_emphasis_477():
    """
    Test case 477:  (part 2) Rule 14
    """

    # Arrange
    source_markdown = """_____foo_____"""
    expected_tokens = [
        "[para(1,1):]",
        "[emphasis(1,1):1:_]",
        "[emphasis(1,2):2:_]",
        "[emphasis(1,4):2:_]",
        "[text(1,6):foo:]",
        "[end-emphasis(1,9)::]",
        "[end-emphasis(1,11)::]",
        "[end-emphasis(1,13)::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><em><strong><strong>foo</strong></strong></em></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_emphasis_478():
    """
    Test case 478:  (part 1) Rule 15
    """

    # Arrange
    source_markdown = """*foo _bar* baz_"""
    expected_tokens = [
        "[para(1,1):]",
        "[emphasis(1,1):1:*]",
        "[text(1,2):foo :]",
        "[text(1,6):_:]",
        "[text(1,7):bar:]",
        "[end-emphasis(1,10)::]",
        "[text(1,11): baz:]",
        "[text(1,15):_:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><em>foo _bar</em> baz_</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_emphasis_479():
    """
    Test case 479:  (part 2) Rule 15
    """

    # Arrange
    source_markdown = """*foo __bar *baz bim__ bam*"""
    expected_tokens = [
        "[para(1,1):]",
        "[emphasis(1,1):1:*]",
        "[text(1,2):foo :]",
        "[emphasis(1,6):2:_]",
        "[text(1,8):bar :]",
        "[text(1,12):*:]",
        "[text(1,13):baz bim:]",
        "[end-emphasis(1,20)::]",
        "[text(1,22): bam:]",
        "[end-emphasis(1,26)::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><em>foo <strong>bar *baz bim</strong> bam</em></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_emphasis_480():
    """
    Test case 480:  (part 1) Rule 16
    """

    # Arrange
    source_markdown = """**foo **bar baz**"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):**:]",
        "[text(1,3):foo :]",
        "[emphasis(1,7):2:*]",
        "[text(1,9):bar baz:]",
        "[end-emphasis(1,16)::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>**foo <strong>bar baz</strong></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_emphasis_481():
    """
    Test case 481:  (part 2) Rule 16
    """

    # Arrange
    source_markdown = """*foo *bar baz*"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):*:]",
        "[text(1,2):foo :]",
        "[emphasis(1,6):1:*]",
        "[text(1,7):bar baz:]",
        "[end-emphasis(1,14)::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>*foo <em>bar baz</em></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_emphasis_482():
    """
    Test case 482:  (part 1) Rule 17
    """

    # Arrange
    source_markdown = """*[bar*](/url)"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):*:]",
        "[link(1,2):inline:/url:::::bar*:False::::]",
        "[text(1,3):bar:]",
        "[text(1,6):*:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>*<a href="/url">bar*</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_emphasis_483():
    """
    Test case 483:  (part 2) Rule 17
    """

    # Arrange
    source_markdown = """_foo [bar_](/url)"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):_:]",
        "[text(1,2):foo :]",
        "[link(1,6):inline:/url:::::bar_:False::::]",
        "[text(1,7):bar:]",
        "[text(1,10):_:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>_foo <a href="/url">bar_</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_emphasis_484():
    """
    Test case 484:  (part 3) Rule 17
    """

    # Arrange
    source_markdown = """*<img src="foo" title="*"/>"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):*:]",
        '[raw-html(1,2):img src="foo" title="*"/]',
        "[end-para:::True]",
    ]
    expected_gfm = """<p>*<img src="foo" title="*"/></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_emphasis_485():
    """
    Test case 485:  (part 4) Rule 17
    """

    # Arrange
    source_markdown = """**<a href="**">"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):**:]",
        '[raw-html(1,3):a href="**"]',
        "[end-para:::True]",
    ]
    expected_gfm = """<p>**<a href="**"></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_emphasis_486():
    """
    Test case 486:  (part 5) Rule 17
    """

    # Arrange
    source_markdown = """__<a href="__">"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):__:]",
        '[raw-html(1,3):a href="__"]',
        "[end-para:::True]",
    ]
    expected_gfm = """<p>__<a href="__"></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_emphasis_487():
    """
    Test case 487:  (part 6) Rule 17
    """

    # Arrange
    source_markdown = """*a `*`*"""
    expected_tokens = [
        "[para(1,1):]",
        "[emphasis(1,1):1:*]",
        "[text(1,2):a :]",
        "[icode-span(1,4):*:`::]",
        "[end-emphasis(1,7)::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><em>a <code>*</code></em></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_emphasis_488():
    """
    Test case 488:  (part 7) Rule 17
    """

    # Arrange
    source_markdown = """_a `_`_"""
    expected_tokens = [
        "[para(1,1):]",
        "[emphasis(1,1):1:_]",
        "[text(1,2):a :]",
        "[icode-span(1,4):_:`::]",
        "[end-emphasis(1,7)::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><em>a <code>_</code></em></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_emphasis_489():
    """
    Test case 489:  (part 8) Rule 17
    """

    # Arrange
    source_markdown = """**a<http://foo.bar/?q=**>"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):**:]",
        "[text(1,3):a:]",
        "[uri-autolink(1,4):http://foo.bar/?q=**]",
        "[end-para:::True]",
    ]
    expected_gfm = (
        """<p>**a<a href="http://foo.bar/?q=**">http://foo.bar/?q=**</a></p>"""
    )

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_emphasis_490():
    """
    Test case 490:  (part 9) Rule 17
    """

    # Arrange
    source_markdown = """__a<http://foo.bar/?q=__>"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):__:]",
        "[text(1,3):a:]",
        "[uri-autolink(1,4):http://foo.bar/?q=__]",
        "[end-para:::True]",
    ]
    expected_gfm = (
        """<p>__a<a href="http://foo.bar/?q=__">http://foo.bar/?q=__</a></p>"""
    )

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)
