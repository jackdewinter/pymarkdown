"""
Testing various aspects of whitespaces around links.
"""

from test.utils import act_and_assert

import pytest


@pytest.mark.gfm
def test_whitespaces_inline_link_with_spaces_before_label():
    """
    Test case:  inline link label with spaces before
    """

    # Arrange
    source_markdown = """[ fred](/url)"""
    expected_tokens = [
        "[para(1,1):]",
        "[link(1,1):inline:/url::::: fred:False::::]",
        "[text(1,2): fred:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="/url"> fred</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_inline_link_with_tabs_outside():
    """
    Test case:  inline link label with tabs before
    """

    # Arrange
    source_markdown = """this\tis [fred](/url) a\tlink"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):this\tis :]",
        "[link(1,12):inline:/url:::::fred:False::::]",
        "[text(1,13):fred:]",
        "[end-link::]",
        "[text(1,24): a\tlink:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>this\tis <a href="/url">fred</a> a\tlink</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_inline_link_with_tabs_large_outside():
    """
    Test case:  inline link label with tabs before
    """

    # Arrange
    source_markdown = """an\tlink
this\tis [fred](/url) a\tlink
large\text"""
    expected_tokens = [
        "[para(1,1):\n\n]",
        "[text(1,1):an\tlink\nthis\tis ::\n]",
        "[link(2,12):inline:/url:::::fred:False::::]",
        "[text(2,13):fred:]",
        "[end-link::]",
        "[text(2,24): a\tlink\nlarge\text::\n]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>an\tlink
this\tis <a href="/url">fred</a> a\tlink
large\text</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_inline_link_with_tabs_large_outside_no_spaces():
    """
    Test case:  inline link label with tabs before
    """

    # Arrange
    source_markdown = """an\tlink
this\tis[fred](/url)a\tlink
large\text"""
    expected_tokens = [
        "[para(1,1):\n\n]",
        "[text(1,1):an\tlink\nthis\tis::\n]",
        "[link(2,11):inline:/url:::::fred:False::::]",
        "[text(2,12):fred:]",
        "[end-link::]",
        "[text(2,23):a\tlink\nlarge\text::\n]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>an\tlink
this\tis<a href="/url">fred</a>a\tlink
large\text</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_inline_link_with_tabs_large_outside_with_duplicate_outside():
    """
    Test case:  inline link label with tabs before
    """

    # Arrange
    source_markdown = """an\tlink an\tlink
this\tis this\tis [fred](/url) a\tlink a\tlink
large\text large\text"""
    expected_tokens = [
        "[para(1,1):\n\n]",
        "[text(1,1):an\tlink an\tlink\nthis\tis this\tis ::\n]",
        "[link(2,20):inline:/url:::::fred:False::::]",
        "[text(2,21):fred:]",
        "[end-link::]",
        "[text(2,32): a\tlink a\tlink\nlarge\text large\text::\n]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>an\tlink an\tlink
this\tis this\tis <a href="/url">fred</a> a\tlink a\tlink
large\text large\text</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_inline_link_with_tabs_large_outside_with_duplicate_outside_first_two():
    """
    Test case:  inline link label with tabs before
    """

    # Arrange
    source_markdown = """an\tlink an\tlink
this\tis this\tis [fred](/url) a\tlink a\tlink"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):an\tlink an\tlink\nthis\tis this\tis ::\n]",
        "[link(2,20):inline:/url:::::fred:False::::]",
        "[text(2,21):fred:]",
        "[end-link::]",
        "[text(2,32): a\tlink a\tlink:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>an\tlink an\tlink
this\tis this\tis <a href="/url">fred</a> a\tlink a\tlink</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_inline_link_with_tabs_large_outside_with_duplicate_outside_and_links():
    """
    Test case:  inline link label with tabs before
    """

    # Arrange
    source_markdown = """an\tlink an\tlink
this\tis this\tis [fred](/url) a\tlink a\tlink [barney](/url) another\tlink another\tlink
large\text large\text"""
    expected_tokens = [
        "[para(1,1):\n\n]",
        "[text(1,1):an\tlink an\tlink\nthis\tis this\tis ::\n]",
        "[link(2,20):inline:/url:::::fred:False::::]",
        "[text(2,21):fred:]",
        "[end-link::]",
        "[text(2,32): a\tlink a\tlink :]",
        "[link(2,50):inline:/url:::::barney:False::::]",
        "[text(2,51):barney:]",
        "[end-link::]",
        "[text(2,64): another\tlink another\tlink\nlarge\text large\text::\n]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>an\tlink an\tlink
this\tis this\tis <a href="/url">fred</a> a\tlink a\tlink <a href="/url">barney</a> another\tlink another\tlink
large\text large\text</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_inline_link_with_tabs_large_outside_with_duplicate_outside_and_links_no_space():
    """
    Test case:  inline link label with tabs before
    """

    # Arrange
    source_markdown = """an\tlink an\tlink
this\tis this\tis[fred](/url)a\tlink a\tlink[barney](/url)another\tlink another\tlink
large\text large\text"""
    expected_tokens = [
        "[para(1,1):\n\n]",
        "[text(1,1):an\tlink an\tlink\nthis\tis this\tis::\n]",
        "[link(2,19):inline:/url:::::fred:False::::]",
        "[text(2,20):fred:]",
        "[end-link::]",
        "[text(2,31):a\tlink a\tlink:]",
        "[link(2,45):inline:/url:::::barney:False::::]",
        "[text(2,46):barney:]",
        "[end-link::]",
        "[text(2,59):another\tlink another\tlink\nlarge\text large\text::\n]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>an\tlink an\tlink
this\tis this\tis<a href="/url">fred</a>a\tlink a\tlink<a href="/url">barney</a>another\tlink another\tlink
large\text large\text</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_inline_link_with_tabs_large_outside_with_duplicate_outside_and_links_no_word_just_space():
    """
    Test case:  inline link label with tabs before
    """

    # Arrange
    source_markdown = """an\tlink an\tlink
this\tis this\tis[fred](/url) [barney](/url)another\tlink another\tlink
large\text large\text"""
    expected_tokens = [
        "[para(1,1):\n\n]",
        "[text(1,1):an\tlink an\tlink\nthis\tis this\tis::\n]",
        "[link(2,19):inline:/url:::::fred:False::::]",
        "[text(2,20):fred:]",
        "[end-link::]",
        "[text(2,31): :]",
        "[link(2,32):inline:/url:::::barney:False::::]",
        "[text(2,33):barney:]",
        "[end-link::]",
        "[text(2,46):another\tlink another\tlink\nlarge\text large\text::\n]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>an\tlink an\tlink
this\tis this\tis<a href="/url">fred</a> <a href="/url">barney</a>another\tlink another\tlink
large\text large\text</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_inline_link_with_tabs_large_outside_with_duplicate_outside_and_links_no_word_just_tab():
    """
    Test case:  inline link label with tabs before
    """

    # Arrange
    source_markdown = """an\tlink an\tlink
this\tis this\tis[fred](/url)\t[barney](/url)another\tlink another\tlink
large\text large\text"""
    expected_tokens = [
        "[para(1,1):\n\n]",
        "[text(1,1):an\tlink an\tlink\nthis\tis this\tis::\n]",
        "[link(2,19):inline:/url:::::fred:False::::]",
        "[text(2,20):fred:]",
        "[end-link::]",
        "[text(2,31):\t:]",
        "[link(2,33):inline:/url:::::barney:False::::]",
        "[text(2,34):barney:]",
        "[end-link::]",
        "[text(2,47):another\tlink another\tlink\nlarge\text large\text::\n]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>an\tlink an\tlink
this\tis this\tis<a href="/url">fred</a>\t<a href="/url">barney</a>another\tlink another\tlink
large\text large\text</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_inline_link_with_tabs_large_outside_with_duplicate_outside_and_links_more_links():
    """
    Test case:  inline link label with tabs before
    """

    # Arrange
    source_markdown = """an\tlink [wilma](/url) an\tlink
this\tis this\tis[fred](/url)a\tlink a\tlink[barney](/url)another\tlink another\tlink
large\text[betty](/url)large\text"""
    expected_tokens = [
        "[para(1,1):\n\n]",
        "[text(1,1):an\tlink :]",
        "[link(1,10):inline:/url:::::wilma:False::::]",
        "[text(1,11):wilma:]",
        "[end-link::]",
        "[text(1,23): an\tlink\nthis\tis this\tis::\n]",
        "[link(2,19):inline:/url:::::fred:False::::]",
        "[text(2,20):fred:]",
        "[end-link::]",
        "[text(2,31):a\tlink a\tlink:]",
        "[link(2,45):inline:/url:::::barney:False::::]",
        "[text(2,46):barney:]",
        "[end-link::]",
        "[text(2,59):another\tlink another\tlink\nlarge\text::\n]",
        "[link(3,12):inline:/url:::::betty:False::::]",
        "[text(3,13):betty:]",
        "[end-link::]",
        "[text(3,25):large\text:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>an\tlink <a href="/url">wilma</a> an\tlink
this\tis this\tis<a href="/url">fred</a>a\tlink a\tlink<a href="/url">barney</a>another\tlink another\tlink
large\text<a href="/url">betty</a>large\text</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_inline_link_with_tabs_large_outside_with_more_links_and_middle_surrounding_spaces():
    """
    Test case:  inline link label with tabs before
    """

    # Arrange
    source_markdown = """an\tlink [wilma](/url) an\tlink
this\tis this\tis[fred](/url) a\tlink a\tlink [barney](/url)another\tlink another\tlink
large\text[betty](/url)large\text"""
    expected_tokens = [
        "[para(1,1):\n\n]",
        "[text(1,1):an\tlink :]",
        "[link(1,10):inline:/url:::::wilma:False::::]",
        "[text(1,11):wilma:]",
        "[end-link::]",
        "[text(1,23): an\tlink\nthis\tis this\tis::\n]",
        "[link(2,19):inline:/url:::::fred:False::::]",
        "[text(2,20):fred:]",
        "[end-link::]",
        "[text(2,31): a\tlink a\tlink :]",
        "[link(2,50):inline:/url:::::barney:False::::]",
        "[text(2,51):barney:]",
        "[end-link::]",
        "[text(2,64):another\tlink another\tlink\nlarge\text::\n]",
        "[link(3,12):inline:/url:::::betty:False::::]",
        "[text(3,13):betty:]",
        "[end-link::]",
        "[text(3,25):large\text:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>an\tlink <a href="/url">wilma</a> an\tlink
this\tis this\tis<a href="/url">fred</a> a\tlink a\tlink <a href="/url">barney</a>another\tlink another\tlink
large\text<a href="/url">betty</a>large\text</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_inline_link_with_tabs_large_outside_with_more_links_and_middle_surrounding_tabs():
    """
    Test case:  inline link label with tabs before
    """

    # Arrange
    source_markdown = """an\tlink\t[wilma](/url)\tan\tlink
this\tis this\tis\t[fred](/url)\ta\tlink a\tlink\t[barney](/url)\tanother\tlink another\tlink
large\text\t[betty](/url)\tlarge\text"""
    expected_tokens = [
        "[para(1,1):\n\n]",
        "[text(1,1):an\tlink\t:]",
        "[link(1,13):inline:/url:::::wilma:False::::]",
        "[text(1,14):wilma:]",
        "[end-link::]",
        "[text(1,26):\tan\tlink\nthis\tis this\tis\t::\n]",
        "[link(2,21):inline:/url:::::fred:False::::]",
        "[text(2,22):fred:]",
        "[end-link::]",
        "[text(2,33):\ta\tlink a\tlink\t:]",
        "[link(2,57):inline:/url:::::barney:False::::]",
        "[text(2,58):barney:]",
        "[end-link::]",
        "[text(2,71):\tanother\tlink another\tlink\nlarge\text\t::\n]",
        "[link(3,13):inline:/url:::::betty:False::::]",
        "[text(3,14):betty:]",
        "[end-link::]",
        "[text(3,26):\tlarge\text:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>an\tlink\t<a href="/url">wilma</a>\tan\tlink
this\tis this\tis\t<a href="/url">fred</a>\ta\tlink a\tlink\t<a href="/url">barney</a>\tanother\tlink another\tlink
large\text\t<a href="/url">betty</a>\tlarge\text</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_inline_link_with_tabs_large_outside_with_more_links_and_ending_with_spaces():
    """
    Test case:  inline link label with tabs before
    """

    # Arrange
    source_markdown = """an\tlink\t[wilma](/url)\tan\tlink
this\tis this\tis\t[fred](/url)\ta\tlink a\tlink\t[barney](/url)\tanother\tlink another\tlink
large\text\t[betty](/url)  """
    expected_tokens = [
        "[para(1,1):\n\n:  ]",
        "[text(1,1):an\tlink\t:]",
        "[link(1,13):inline:/url:::::wilma:False::::]",
        "[text(1,14):wilma:]",
        "[end-link::]",
        "[text(1,26):\tan\tlink\nthis\tis this\tis\t::\n]",
        "[link(2,21):inline:/url:::::fred:False::::]",
        "[text(2,22):fred:]",
        "[end-link::]",
        "[text(2,33):\ta\tlink a\tlink\t:]",
        "[link(2,57):inline:/url:::::barney:False::::]",
        "[text(2,58):barney:]",
        "[end-link::]",
        "[text(2,71):\tanother\tlink another\tlink\nlarge\text\t::\n]",
        "[link(3,13):inline:/url:::::betty:False::::]",
        "[text(3,14):betty:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>an\tlink\t<a href="/url">wilma</a>\tan\tlink
this\tis this\tis\t<a href="/url">fred</a>\ta\tlink a\tlink\t<a href="/url">barney</a>\tanother\tlink another\tlink
large\text\t<a href="/url">betty</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_inline_link_with_tabs_large_outside_with_more_links_and_ending_with_tabs():
    """
    Test case:  inline link label with tabs before
    """

    # Arrange
    source_markdown = """an\tlink\t[wilma](/url)\tan\tlink
this\tis this\tis\t[fred](/url)\ta\tlink a\tlink\t[barney](/url)\tanother\tlink another\tlink
large\text\t[betty](/url)\t\t"""
    expected_tokens = [
        "[para(1,1):\n\n:\t\t]",
        "[text(1,1):an\tlink\t:]",
        "[link(1,13):inline:/url:::::wilma:False::::]",
        "[text(1,14):wilma:]",
        "[end-link::]",
        "[text(1,26):\tan\tlink\nthis\tis this\tis\t::\n]",
        "[link(2,21):inline:/url:::::fred:False::::]",
        "[text(2,22):fred:]",
        "[end-link::]",
        "[text(2,33):\ta\tlink a\tlink\t:]",
        "[link(2,57):inline:/url:::::barney:False::::]",
        "[text(2,58):barney:]",
        "[end-link::]",
        "[text(2,71):\tanother\tlink another\tlink\nlarge\text\t::\n]",
        "[link(3,13):inline:/url:::::betty:False::::]",
        "[text(3,14):betty:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>an\tlink\t<a href="/url">wilma</a>\tan\tlink
this\tis this\tis\t<a href="/url">fred</a>\ta\tlink a\tlink\t<a href="/url">barney</a>\tanother\tlink another\tlink
large\text\t<a href="/url">betty</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_inline_link_with_tabs_before_label():
    """
    Test case:  inline link label with tabs before
    """

    # Arrange
    source_markdown = """[\tfred](/url)"""
    expected_tokens = [
        "[para(1,1):]",
        "[link(1,1):inline:/url:::::\tfred:False::::]",
        "[text(1,2):\tfred:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="/url">\tfred</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_inline_link_with_form_feeds_before_label():
    """
    Test case:  inline link label with form feeds before
    """

    # Arrange
    source_markdown = """[\u000cfred](/url)"""
    expected_tokens = [
        "[para(1,1):]",
        "[link(1,1):inline:/url:::::\u000cfred:False::::]",
        "[text(1,2):\u000cfred:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="/url">\u000cfred</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_shortcut_link_with_spaces_before_label():
    """
    Test case:  shortcut link label with spaces before
    """

    # Arrange
    source_markdown = """[  fred]

[ fred]: /url
"""
    expected_tokens = [
        "[para(1,1):]",
        "[link(1,1):shortcut:/url:::::  fred:False::::]",
        "[text(1,2):  fred:]",
        "[end-link::]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[link-ref-def(3,1):True::fred: fred: :/url:::::]",
        "[BLANK(4,1):]",
    ]
    expected_gfm = """<p><a href="/url">  fred</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_shortcut_link_with_tabs_before_label():
    """
    Test case:  shortcut link label with tabs before
    """

    # Arrange
    source_markdown = """[\t\tfred]

[ fred]: /url"""
    expected_tokens = [
        "[para(1,1):]",
        "[link(1,1):shortcut:/url:::::\t\tfred:False::::]",
        "[text(1,2):\t\tfred:]",
        "[end-link::]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[link-ref-def(3,1):True::fred: fred: :/url:::::]",
    ]
    expected_gfm = """<p><a href="/url">\t\tfred</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_shortcut_link_with_form_feeds_before_label():
    """
    Test case:  shortcut link label with form feeds before
    """

    # Arrange
    source_markdown = """[\u000c\u000cfred]

[ fred]: /url"""
    expected_tokens = [
        "[para(1,1):]",
        "[link(1,1):shortcut:/url:::::\u000c\u000cfred:False::::]",
        "[text(1,2):\u000c\u000cfred:]",
        "[end-link::]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[link-ref-def(3,1):True::fred: fred: :/url:::::]",
    ]
    expected_gfm = """<p><a href="/url">\u000c\u000cfred</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_inline_link_with_spaces_in_label():
    """
    Test case:  inline link label with spaces in
    """

    # Arrange
    source_markdown = """[fred  boy](/url)"""
    expected_tokens = [
        "[para(1,1):]",
        "[link(1,1):inline:/url:::::fred  boy:False::::]",
        "[text(1,2):fred  boy:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="/url">fred  boy</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_inline_link_with_tabs_in_label():
    """
    Test case:  inline link label with tabs in
    """

    # Arrange
    source_markdown = """[fred\t\tboy](/url)"""
    expected_tokens = [
        "[para(1,1):]",
        "[link(1,1):inline:/url:::::fred\t\tboy:False::::]",
        "[text(1,2):fred\t\tboy:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="/url">fred\t\tboy</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_inline_link_with_form_feeds_in_label():
    """
    Test case:  inline link label with form feeds in
    """

    # Arrange
    source_markdown = """[fred\u000c\u000cboy](/url)"""
    expected_tokens = [
        "[para(1,1):]",
        "[link(1,1):inline:/url:::::fred\u000c\u000cboy:False::::]",
        "[text(1,2):fred\u000c\u000cboy:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="/url">fred\u000c\u000cboy</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_shortcut_link_with_spaces_in_label():
    """
    Test case:  shortcut link label with spaces in
    """

    # Arrange
    source_markdown = """[fred  boy]

[fred boy]: /url"""
    expected_tokens = [
        "[para(1,1):]",
        "[link(1,1):shortcut:/url:::::fred  boy:False::::]",
        "[text(1,2):fred  boy:]",
        "[end-link::]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[link-ref-def(3,1):True::fred boy:: :/url:::::]",
    ]
    expected_gfm = """<p><a href="/url">fred  boy</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_shortcut_link_with_tabs_in_label():
    """
    Test case:  shortcut link label with tabs in
    """

    # Arrange
    source_markdown = """[fred\t\tboy]

[fred boy]: /url"""
    expected_tokens = [
        "[para(1,1):]",
        "[link(1,1):shortcut:/url:::::fred\t\tboy:False::::]",
        "[text(1,2):fred\t\tboy:]",
        "[end-link::]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[link-ref-def(3,1):True::fred boy:: :/url:::::]",
    ]
    expected_gfm = """<p><a href="/url">fred\t\tboy</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_shortcut_link_with_form_feeds_in_label():
    """
    Test case:  shortcut link label with form feeds in
    """

    # Arrange
    source_markdown = """[fred\u000c\u000cboy]

[fred boy]: /url"""
    expected_tokens = [
        "[para(1,1):]",
        "[link(1,1):shortcut:/url:::::fred\u000c\u000cboy:False::::]",
        "[text(1,2):fred\u000c\u000cboy:]",
        "[end-link::]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[link-ref-def(3,1):True::fred boy:: :/url:::::]",
    ]
    expected_gfm = """<p><a href="/url">fred\u000c\u000cboy</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_inline_link_with_spaces_after_label():
    """
    Test case:  inline link label with after before
    """

    # Arrange
    source_markdown = """[fred ](/url)"""
    expected_tokens = [
        "[para(1,1):]",
        "[link(1,1):inline:/url:::::fred :False::::]",
        "[text(1,2):fred :]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="/url">fred </a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_inline_link_with_tabs_after_label():
    """
    Test case:  inline link label with tabs after
    """

    # Arrange
    source_markdown = """[fred\t\t](/url)"""
    expected_tokens = [
        "[para(1,1):]",
        "[link(1,1):inline:/url:::::fred\t\t:False::::]",
        "[text(1,2):fred\t\t:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="/url">fred\t\t</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_inline_link_with_form_feeds_after_label():
    """
    Test case:  inline link label with form feeds after
    """

    # Arrange
    source_markdown = """[fred\u000c\u000c](/url)"""
    expected_tokens = [
        "[para(1,1):]",
        "[link(1,1):inline:/url:::::fred\u000c\u000c:False::::]",
        "[text(1,2):fred\u000c\u000c:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="/url">fred\u000c\u000c</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_shortcut_link_with_spaces_after_label():
    """
    Test case:  shortcut link label with spaces after
    """

    # Arrange
    source_markdown = """[fred  ]

[fred ]: /url"""
    expected_tokens = [
        "[para(1,1):]",
        "[link(1,1):shortcut:/url:::::fred  :False::::]",
        "[text(1,2):fred  :]",
        "[end-link::]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[link-ref-def(3,1):True::fred:fred : :/url:::::]",
    ]
    expected_gfm = """<p><a href="/url">fred  </a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_shortcut_link_with_tabs_after_label():
    """
    Test case:  shortcut link label with tabs after
    """

    # Arrange
    source_markdown = """[fred\t\t]

[fred ]: /url"""
    expected_tokens = [
        "[para(1,1):]",
        "[link(1,1):shortcut:/url:::::fred\t\t:False::::]",
        "[text(1,2):fred\t\t:]",
        "[end-link::]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[link-ref-def(3,1):True::fred:fred : :/url:::::]",
    ]
    expected_gfm = """<p><a href="/url">fred\t\t</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_shortcut_link_with_form_feeds_after_label():
    """
    Test case:  shortcut link label with form feeds after
    """

    # Arrange
    source_markdown = """[fred\u000c\u000c]

[fred ]: /url"""
    expected_tokens = [
        "[para(1,1):]",
        "[link(1,1):shortcut:/url:::::fred\u000c\u000c:False::::]",
        "[text(1,2):fred\u000c\u000c:]",
        "[end-link::]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[link-ref-def(3,1):True::fred:fred : :/url:::::]",
    ]
    expected_gfm = """<p><a href="/url">fred\u000c\u000c</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_inline_link_with_tabs_and_references():
    """
    Test case:  inline link label with tabs after
    """

    # Arrange
    source_markdown = """[fred\t&amp;\tboy](/url)"""
    expected_tokens = [
        "[para(1,1):]",
        "[link(1,1):inline:/url:::::fred\t&amp;\tboy:False::::]",
        "[text(1,2):fred\t\a&amp;\a\a&\a&amp;\a\a\tboy:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="/url">fred\t&amp;\tboy</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_inline_link_with_tabs_and_code_span():
    """
    Test case:  inline link label with tabs after
    """

    # Arrange
    source_markdown = """[fred\t`bob`\tboy](/url)"""
    expected_tokens = [
        "[para(1,1):]",
        "[link(1,1):inline:/url:::::fred\t`bob`\tboy:False::::]",
        "[text(1,2):fred\t:]",
        "[icode-span(1,9):bob:`::]",
        "[text(1,14):\tboy:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="/url">fred\t<code>bob</code>\tboy</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_inline_link_with_tabs_and_emphasis():
    """
    Test case:  inline link label with tabs after
    """

    # Arrange
    source_markdown = """[fred\t*bob\tthe*\tboy](/url)"""
    expected_tokens = [
        "[para(1,1):]",
        "[link(1,1):inline:/url:::::fred\t*bob\tthe*\tboy:False::::]",
        "[text(1,2):fred\t:]",
        "[emphasis(1,9):1:*]",
        "[text(1,10):bob\tthe:]",
        "[end-emphasis(1,20)::]",
        "[text(1,21):\tboy:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="/url">fred\t<em>bob\tthe</em>\tboy</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_inline_link_with_tabs_and_image():
    """
    Test case:  inline link label with tabs after
    """

    # Arrange
    source_markdown = """[fred\t![bob\tboy](/url)\tboy](/url)"""
    expected_tokens = [
        "[para(1,1):]",
        "[link(1,1):inline:/url:::::fred\t![bob\tboy](/url)\tboy:False::::]",
        "[text(1,2):fred\t:]",
        "[image(1,9):inline:/url::bob\tboy::::bob\tboy:False::::]",
        "[text(1,27):\tboy:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = (
        """<p><a href="/url">fred\t<img src="/url" alt="bob\tboy" />\tboy</a></p>"""
    )

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_inline_link_with_tabs_inside_of_tabs():
    """
    Test case:  inline link label with tabs after
    """

    # Arrange
    source_markdown = """this\tshould\t[fred\tboy](/url)\tbe\tbad\tmarkdown"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):this\tshould\t:]",
        "[link(1,17):inline:/url:::::fred\tboy:False::::]",
        "[text(1,18):fred\tboy:]",
        "[end-link::]",
        "[text(1,35):\tbe\tbad\tmarkdown:]",
        "[end-para:::True]",
    ]
    expected_gfm = (
        """<p>this\tshould\t<a href="/url">fred\tboy</a>\tbe\tbad\tmarkdown</p>"""
    )

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_inline_link_with_tabs_and_newlines():
    """
    Test case:  inline link label with tabs after
    """

    # Arrange
    source_markdown = """should\t[fred\t
\tboy](/url)\tpass"""
    expected_tokens = [
        "[para(1,1):\n\t]",
        "[text(1,1):should\t:]",
        "[link(1,9):inline:/url:::::fred\t\nboy:False::::]",
        "[text(1,10):fred\nboy::\t\n]",
        "[end-link::]",
        "[text(2,12):\tpass:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>should\t<a href="/url">fred\t
boy</a>\tpass</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_inline_link_with_spaces_before_destination():
    """
    Test case:  inline link label with spaces before the destination
    """

    # Arrange
    source_markdown = """[fred](  /url)"""
    expected_tokens = [
        "[para(1,1):]",
        "[link(1,1):inline:/url:::::fred:False::  ::]",
        "[text(1,2):fred:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="/url">fred</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_inline_link_with_tabs_before_destination():
    """
    Test case:  inline link label with tabs before the destination
    """

    # Arrange
    source_markdown = """[fred](\t\t/url)"""
    expected_tokens = [
        "[para(1,1):]",
        "[link(1,1):inline:/url:::::fred:False::\t\t::]",
        "[text(1,2):fred:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="/url">fred</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_inline_link_with_form_feeds_before_destination():
    """
    Test case:  inline link label with form feeds before the destination
    """

    # Arrange
    source_markdown = """[fred](\u000c\u000c/url)"""
    expected_tokens = [
        "[para(1,1):]",
        "[link(1,1):inline:/url:::::fred:False::\u000c\u000c::]",
        "[text(1,2):fred:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="/url">fred</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_inline_link_with_spaces_after_destination():
    """
    Test case:  inline link label with spaces after the destination
    """

    # Arrange
    source_markdown = """[fred](/url  )"""
    expected_tokens = [
        "[para(1,1):]",
        "[link(1,1):inline:/url:::::fred:False:::  :]",
        "[text(1,2):fred:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="/url">fred</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_inline_link_with_tabs_after_destination():
    """
    Test case:  inline link label with tabs after the destination
    """

    # Arrange
    source_markdown = """[fred](/url\t\t)"""
    expected_tokens = [
        "[para(1,1):]",
        "[link(1,1):inline:/url:::::fred:False:::\t\t:]",
        "[text(1,2):fred:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="/url">fred</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_inline_link_with_form_feeds_after_destination():
    """
    Test case:  inline link label with form feeds after the destination
    """

    # Arrange
    source_markdown = """[fred](/url\u000c\u000c)"""
    expected_tokens = [
        "[para(1,1):]",
        "[link(1,1):inline:/url:::::fred:False:::\u000c\u000c:]",
        "[text(1,2):fred:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="/url">fred</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_inline_link_with_spaces_before_title():
    """
    Test case:  inline link label with spaces before the title
    """

    # Arrange
    source_markdown = """[fred](/url  'title')"""
    expected_tokens = [
        "[para(1,1):]",
        "[link(1,1):inline:/url:title::::fred:False:'::  :]",
        "[text(1,2):fred:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="/url" title="title">fred</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_inline_link_with_tabs_before_title():
    """
    Test case:  inline link label with tabs before the title
    """

    # Arrange
    source_markdown = """[fred](/url\t\t'title')"""
    expected_tokens = [
        "[para(1,1):]",
        "[link(1,1):inline:/url:title::::fred:False:'::\t\t:]",
        "[text(1,2):fred:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="/url" title="title">fred</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_inline_link_with_form_feeds_before_title():
    """
    Test case:  inline link label with form feeds before the title
    """

    # Arrange
    source_markdown = """[fred](/url\u000c\u000c'title')"""
    expected_tokens = [
        "[para(1,1):]",
        "[link(1,1):inline:/url:title::::fred:False:'::\u000c\u000c:]",
        "[text(1,2):fred:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="/url" title="title">fred</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_inline_link_with_spaces_after_title():
    """
    Test case:  inline link label with spaces after the title
    """

    # Arrange
    source_markdown = """[fred](/url 'title'  )"""
    expected_tokens = [
        "[para(1,1):]",
        "[link(1,1):inline:/url:title::::fred:False:':: :  ]",
        "[text(1,2):fred:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="/url" title="title">fred</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_inline_link_with_tabs_after_title():
    """
    Test case:  inline link label with tabs after the title
    """

    # Arrange
    source_markdown = """[fred](/url 'title'\t\t)"""
    expected_tokens = [
        "[para(1,1):]",
        "[link(1,1):inline:/url:title::::fred:False:':: :\t\t]",
        "[text(1,2):fred:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="/url" title="title">fred</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_inline_link_with_form_feeds_after_title():
    """
    Test case:  inline link label with form feeds after the title
    """

    # Arrange
    source_markdown = """[fred](/url 'title'\u000c\u000c)"""
    expected_tokens = [
        "[para(1,1):]",
        "[link(1,1):inline:/url:title::::fred:False:':: :\u000c\u000c]",
        "[text(1,2):fred:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="/url" title="title">fred</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_full_link_with_tabs_in_reference():
    """
    Test case:  inline link label with tabs before the title
    """

    # Arrange
    source_markdown = """[foo][\t\tbar]

[ bar]: /url 'title'"""
    expected_tokens = [
        "[para(1,1):]",
        "[link(1,1):full:/url:title:::\t\tbar:foo:False::::]",
        "[text(1,2):foo:]",
        "[end-link::]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[link-ref-def(3,1):True::bar: bar: :/url:: :title:'title':]",
    ]
    expected_gfm = """<p><a href="/url" title="title">foo</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)
