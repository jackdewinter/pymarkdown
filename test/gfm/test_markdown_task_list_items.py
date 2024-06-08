"""
https://github.github.com/gfm/#task-list-items-extension-
"""

from test.utils import act_and_assert

config_map = {"extensions": {"markdown-task-list-items": {"enabled": True}}}


def test_task_list_items_279_x():
    """
    Test case 279:  Nothing happens to the inline context unless the configuration is enabled, which it is not.
    """

    # Arrange
    source_markdown = """- [ ] foo
- [x] bar"""
    expected_tokens = [
        "[ulist(1,1):-::2:]",
        "[para(1,3):]",
        "[text(1,3):[ ] foo:]",
        "[end-para:::True]",
        "[li(2,1):2::]",
        "[para(2,3):]",
        "[text(2,3):[x] bar:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>\n<li>[ ] foo</li>\n<li>[x] bar</li>\n</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


def test_task_list_items_279_a():
    """
    Test case 279:  If the character between the brackets is a whitespace character, the checkbox is unchecked. Otherwise, the checkbox is checked.
    """

    # Arrange
    source_markdown = """- [ ] foo
- [x] bar"""
    expected_tokens = [
        "[ulist(1,1):-::2:]",
        "[para(1,3):]",
        "[task-list(1,3): ]",
        "[text(1,6): foo:]",
        "[end-para:::True]",
        "[li(2,1):2::]",
        "[para(2,3):]",
        "[task-list(2,3):x]",
        "[text(2,6): bar:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>\n<li><input type="checkbox"> foo</li>\n<li><input checked="" type="checkbox"> bar</li>\n</ul>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


def test_task_list_items_279_b():
    """
    Test case 279:  variation, with non-acceptable character inside
    """

    # Arrange
    source_markdown = """- [ ] foo
- [y] bar"""
    expected_tokens = [
        "[ulist(1,1):-::2:]",
        "[para(1,3):]",
        "[task-list(1,3): ]",
        "[text(1,6): foo:]",
        "[end-para:::True]",
        "[li(2,1):2::]",
        "[para(2,3):]",
        "[text(2,3):[y] bar:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li><input type="checkbox"> foo</li>
<li>[y] bar</li>
</ul>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


def test_task_list_items_279_c():
    """
    Test case 279:  variation, with multiple characters inside
    """

    # Arrange
    source_markdown = """- [ ] foo
- [xx] bar"""
    expected_tokens = [
        "[ulist(1,1):-::2:]",
        "[para(1,3):]",
        "[task-list(1,3): ]",
        "[text(1,6): foo:]",
        "[end-para:::True]",
        "[li(2,1):2::]",
        "[para(2,3):]",
        "[text(2,3):[xx] bar:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li><input type="checkbox"> foo</li>
<li>[xx] bar</li>
</ul>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


def test_task_list_items_279_d():
    """
    Test case 279:  variation, with no whitespace after
    """

    # Arrange
    source_markdown = """- [ ] foo
- [x]bar"""
    expected_tokens = [
        "[ulist(1,1):-::2:]",
        "[para(1,3):]",
        "[task-list(1,3): ]",
        "[text(1,6): foo:]",
        "[end-para:::True]",
        "[li(2,1):2::]",
        "[para(2,3):]",
        "[text(2,3):[x]bar:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li><input type="checkbox"> foo</li>
<li>[x]bar</li>
</ul>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


def test_task_list_items_279_e():
    """
    Test case 279:  variation, with non-whitespace text before
    """

    # Arrange
    source_markdown = """- [ ] foo
- a [x]bar"""
    expected_tokens = [
        "[ulist(1,1):-::2:]",
        "[para(1,3):]",
        "[task-list(1,3): ]",
        "[text(1,6): foo:]",
        "[end-para:::True]",
        "[li(2,1):2::]",
        "[para(2,3):]",
        "[text(2,3):a [x]bar:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li><input type="checkbox"> foo</li>
<li>a [x]bar</li>
</ul>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


def test_task_list_items_279_f():
    """
    Test case 279:  variation, does not work with block quotes
    """

    # Arrange
    source_markdown = """> [ ] foo
> a [x]bar"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> ]",
        "[para(1,3):\n]",
        "[text(1,3):[ ] foo\na [x]bar::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>[ ] foo
a [x]bar</p>
</blockquote>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


def test_task_list_items_280_x():
    """
    Test case 280:  Nothing happens to the inline context unless the configuration is enabled, which it is not.
    """

    # Arrange
    source_markdown = """- [x] foo
  - [ ] bar
  - [x] baz
- [ ] bim"""
    expected_tokens = [
        "[ulist(1,1):-::2:]",
        "[para(1,3):]",
        "[text(1,3):[x] foo:]",
        "[end-para:::True]",
        "[ulist(2,3):-::4:  ]",
        "[para(2,5):]",
        "[text(2,5):[ ] bar:]",
        "[end-para:::True]",
        "[li(3,3):4:  :]",
        "[para(3,5):]",
        "[text(3,5):[x] baz:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[li(4,1):2::]",
        "[para(4,3):]",
        "[text(4,3):[ ] bim:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>[x] foo
<ul>
<li>[ ] bar</li>
<li>[x] baz</li>
</ul>
</li>
<li>[ ] bim</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


def test_task_list_items_280_a():
    """
    Test case 280:  Task lists can be arbitrarily nested:
    """

    # Arrange
    source_markdown = """- [x] foo
  - [ ] bar
  - [x] baz
- [ ] bim"""
    expected_tokens = [
        "[ulist(1,1):-::2:]",
        "[para(1,3):]",
        "[task-list(1,3):x]",
        "[text(1,6): foo:]",
        "[end-para:::True]",
        "[ulist(2,3):-::4:  ]",
        "[para(2,5):]",
        "[task-list(2,5): ]",
        "[text(2,8): bar:]",
        "[end-para:::True]",
        "[li(3,3):4:  :]",
        "[para(3,5):]",
        "[task-list(3,5):x]",
        "[text(3,8): baz:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[li(4,1):2::]",
        "[para(4,3):]",
        "[task-list(4,3): ]",
        "[text(4,6): bim:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li><input checked="" type="checkbox"> foo
<ul>
<li><input type="checkbox"> bar</li>
<li><input checked="" type="checkbox"> baz</li>
</ul>
</li>
<li><input type="checkbox"> bim</li>
</ul>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


def test_task_list_items_280_b():
    """
    Test case 280:  task lists are only at the start of the first paragraph
    """

    # Arrange
    source_markdown = """- [x] foo
  - [ ] bar

    [x] baz
"""
    expected_tokens = [
        "[ulist(1,1):-::2:]",
        "[para(1,3):]",
        "[task-list(1,3):x]",
        "[text(1,6): foo:]",
        "[end-para:::True]",
        "[ulist(2,3):-::4:  :\n    \n]",
        "[para(2,5):]",
        "[task-list(2,5): ]",
        "[text(2,8): bar:]",
        "[end-para:::True]",
        "[BLANK(3,1):]",
        "[para(4,5):]",
        "[text(4,5):[x] baz:]",
        "[end-para:::True]",
        "[BLANK(5,1):]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li><input checked="" type="checkbox"> foo
<ul>
<li>
<p><input type="checkbox"> bar</p>
<p>[x] baz</p>
</li>
</ul>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )
