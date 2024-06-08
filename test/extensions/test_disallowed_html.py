"""
Tests for the optional markdown-disallow-raw-html processing
"""

from test.utils import act_and_assert, assert_that_exception_is_raised

import pytest

config_map = {"extensions": {"markdown-disallow-raw-html": {"enabled": True}}}


@pytest.mark.gfm
def test_disallowed_html_bad_change_type():
    """
    Test to make sure that nothing changes if we try and specify a change_tag_names that is not a string.
    """

    # Arrange
    new_config_map = {
        "mode": {"strict-config": True},
        "extensions": {
            "markdown-disallow-raw-html": {"enabled": True, "change_tag_names": 1}
        },
    }

    source_markdown = """something"""
    expected_tokens = []
    expected_gfm = """something"""
    expected_error = "The value for property 'extensions.markdown-disallow-raw-html.change_tag_names' must be of type 'str'."

    # Act & Assert
    assert_that_exception_is_raised(
        ValueError,
        expected_error,
        act_and_assert,
        source_markdown,
        expected_gfm,
        expected_tokens,
        config_map=new_config_map,
    )


@pytest.mark.gfm
def test_disallowed_html_bad_empty_string():
    """
    Test to make sure that nothing changes if we try and specify a change_tag_names that is empty.
    """

    # Arrange
    new_config_map = {
        "mode": {"strict-config": True},
        "extensions": {
            "markdown-disallow-raw-html": {"enabled": True, "change_tag_names": ""}
        },
    }

    source_markdown = """something"""
    expected_tokens = []
    expected_gfm = """something"""
    expected_error = "Configuration item 'extensions.markdown-disallow-raw-html.change_tag_names' contains at least one empty string."

    # Act & Assert
    assert_that_exception_is_raised(
        ValueError,
        expected_error,
        act_and_assert,
        source_markdown,
        expected_gfm,
        expected_tokens,
        config_map=new_config_map,
    )


@pytest.mark.gfm
def test_disallowed_html_bad_only_commas():
    """
    Test to make sure that nothing changes if we try and specify a change_tag_names that is only commas.
    """

    # Arrange
    new_config_map = {
        "mode": {"strict-config": True},
        "extensions": {
            "markdown-disallow-raw-html": {"enabled": True, "change_tag_names": ",,,,"}
        },
    }

    source_markdown = """something"""
    expected_tokens = []
    expected_gfm = """something"""
    expected_error = "Configuration item 'extensions.markdown-disallow-raw-html.change_tag_names' contains at least one empty string."

    # Act & Assert
    assert_that_exception_is_raised(
        ValueError,
        expected_error,
        act_and_assert,
        source_markdown,
        expected_gfm,
        expected_tokens,
        config_map=new_config_map,
    )


@pytest.mark.gfm
def test_disallowed_html_bad_no_prefix():
    """
    Test to make sure that nothing changes if we try and specify a change_tag_names that contains at least one element that does not start with a + or -.
    """

    # Arrange
    new_config_map = {
        "mode": {"strict-config": True},
        "extensions": {
            "markdown-disallow-raw-html": {
                "enabled": True,
                "change_tag_names": "something",
            }
        },
    }

    source_markdown = """something"""
    expected_tokens = []
    expected_gfm = """something"""
    expected_error = "Configuration item 'extensions.markdown-disallow-raw-html.change_tag_names' elements must either start with '+' or '-'."

    # Act & Assert
    assert_that_exception_is_raised(
        ValueError,
        expected_error,
        act_and_assert,
        source_markdown,
        expected_gfm,
        expected_tokens,
        config_map=new_config_map,
    )


@pytest.mark.gfm
def test_disallowed_html_bad_no_valid_tag_name():
    """
    Test to make sure that nothing changes if we try and specify a change_tag_names that contains at least one elements that is not a valid tag name.
    """

    # Arrange
    new_config_map = {
        "mode": {"strict-config": True},
        "extensions": {
            "markdown-disallow-raw-html": {
                "enabled": True,
                "change_tag_names": "+some thing",
            }
        },
    }

    source_markdown = """something"""
    expected_tokens = []
    expected_gfm = """something"""
    expected_error = "Configuration item 'extensions.markdown-disallow-raw-html.change_tag_names' contains an element 'some thing' that is not a valid tag name."

    # Act & Assert
    assert_that_exception_is_raised(
        ValueError,
        expected_error,
        act_and_assert,
        source_markdown,
        expected_gfm,
        expected_tokens,
        config_map=new_config_map,
    )


@pytest.mark.gfm
def test_disallowed_html_top_disabled():
    """
    Test to make sure that without disallowed turned on, HTML blocks are treated normally.
    """

    # Arrange
    source_markdown = """<script>
  <!-- some script stuff -->
</script>
"""
    expected_tokens = [
        "[html-block(1,1)]",
        "[text(1,1):<script>\n  <!-- some script stuff -->\n</script>:]",
        "[end-html-block:::False]",
        "[BLANK(4,1):]",
    ]
    expected_gfm = """<script>
  <!-- some script stuff -->
</script>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, config_map=None)


@pytest.mark.gfm
def test_disallowed_html_top_enabled_and_not_disallowed():
    """
    Test to make sure that with disallowed turned on, but with a HTML block that is allowed.
    """

    # Arrange
    source_markdown = """<something>
  <!-- some script stuff -->
</something>
"""
    expected_tokens = [
        "[html-block(1,1)]",
        "[text(1,1):<something>\n  <!-- some script stuff -->\n</something>:]",
        "[end-html-block:::False]",
        "[BLANK(4,1):]",
    ]
    expected_gfm = """<something>
  <!-- some script stuff -->
</something>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


@pytest.mark.gfm
def test_disallowed_html_top_enabled_and_now_disallowed():
    """
    Test to make sure that with disallowed turned on, but with a HTML block that is disallowed through configuration.
    """

    # Arrange
    new_config_map = {
        "mode": {"strict-config": True},
        "extensions": {
            "markdown-disallow-raw-html": {
                "enabled": True,
                "change_tag_names": "+something",
            }
        },
    }
    source_markdown = """<something>
  <!-- some script stuff -->
</something>
"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):\a<\a&lt;\asomething>:]",
        "[end-para:::False]",
        "[html-block(2,1)]",
        "[text(2,3):<!-- some script stuff -->:  ]",
        "[end-html-block:::False]",
        "[html-block(3,1)]",
        "[text(3,1):</something>:]",
        "[end-html-block:::False]",
        "[BLANK(4,1):]",
    ]
    expected_gfm = """<p>&lt;something></p>
  <!-- some script stuff -->
</something>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=new_config_map
    )


@pytest.mark.gfm
def test_disallowed_html_top_enabled():
    """
    Test to make sure that with disallowed turned on, disallowed tag names are translated.
    """

    # Arrange
    source_markdown = """<script>
  <!-- some script stuff -->
</script>
"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):\a<\a&lt;\ascript>:]",
        "[end-para:::False]",
        "[html-block(2,1)]",
        "[text(2,3):<!-- some script stuff -->:  ]",
        "[end-html-block:::False]",
        "[html-block(3,1)]",
        "[text(3,1):</script>:]",
        "[end-html-block:::False]",
        "[BLANK(4,1):]",
    ]
    expected_gfm = """<p>&lt;script></p>
  <!-- some script stuff -->
</script>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


@pytest.mark.gfm
def test_disallowed_html_top_enabled_no_longer_disallowed():
    """
    Test to make sure that with disallowed turned on but with config to remove a disallowed tag name, it is acceptable.
    """

    # Arrange
    new_config_map = {
        "mode": {"strict-config": True},
        "extensions": {
            "markdown-disallow-raw-html": {
                "enabled": True,
                "change_tag_names": "-script",
            }
        },
    }
    source_markdown = """<script>
  <!-- some script stuff -->
</script>
"""
    expected_tokens = [
        "[html-block(1,1)]",
        "[text(1,1):<script>\n  <!-- some script stuff -->\n</script>:]",
        "[end-html-block:::False]",
        "[BLANK(4,1):]",
    ]
    expected_gfm = """<script>
  <!-- some script stuff -->
</script>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=new_config_map
    )


@pytest.mark.gfm
def test_disallowed_html_top_with_attributes_disabled():
    """
    Test to make sure that without disallowed turned on, HTML blocks with attributes are treated normally.
    """

    # Arrange
    source_markdown = """<script type="text/javascript">
  <!-- some script stuff -->
</script>
"""
    expected_tokens = [
        "[html-block(1,1)]",
        '[text(1,1):<script type="text/javascript">\n  <!-- some script stuff -->\n</script>:]',
        "[end-html-block:::False]",
        "[BLANK(4,1):]",
    ]
    expected_gfm = """<script type="text/javascript">
  <!-- some script stuff -->
</script>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, config_map=None)


@pytest.mark.gfm
def test_disallowed_html_top_with_attributes_enabled():
    """
    Test to make sure that with disallowed turned on, disallowed HTML blocks with attributes are treated properly.
    """

    # Arrange
    source_markdown = """<script type="text/javascript">
  <!-- some script stuff -->
</script>
"""
    expected_tokens = [
        "[para(1,1):]",
        '[text(1,1):\a<\a&lt;\ascript type="text/javascript">:]',
        "[end-para:::False]",
        "[html-block(2,1)]",
        "[text(2,3):<!-- some script stuff -->:  ]",
        "[end-html-block:::False]",
        "[html-block(3,1)]",
        "[text(3,1):</script>:]",
        "[end-html-block:::False]",
        "[BLANK(4,1):]",
    ]
    expected_gfm = """<p>&lt;script type="text/javascript"></p>
  <!-- some script stuff -->
</script>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


@pytest.mark.gfm
def test_disallowed_html_top_with_openclose_disabled():
    """
    Test to make sure that without disallowed turned on, HTML blocks with autoclose are treated properly.
    """

    # Arrange
    source_markdown = """<script/>
  <!-- some script stuff -->
</script>
"""
    expected_tokens = [
        "[para(1,1):]",
        "[raw-html(1,1):script/]",
        "[end-para:::False]",
        "[html-block(2,1)]",
        "[text(2,3):<!-- some script stuff -->:  ]",
        "[end-html-block:::False]",
        "[html-block(3,1)]",
        "[text(3,1):</script>:]",
        "[end-html-block:::False]",
        "[BLANK(4,1):]",
    ]
    expected_gfm = """<p><script/></p>
  <!-- some script stuff -->
</script>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, config_map=None)


@pytest.mark.gfm
def test_disallowed_html_top_with_openclose_enabled():
    """
    Test to make sure that with disallowed turned on, disallowed HTML blocks with autoclose are treated properly.
    """

    # Arrange
    source_markdown = """<script/>
  <!-- some script stuff -->
</script>
"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):\a<\a&lt;\ascript/>:]",
        "[end-para:::False]",
        "[html-block(2,1)]",
        "[text(2,3):<!-- some script stuff -->:  ]",
        "[end-html-block:::False]",
        "[html-block(3,1)]",
        "[text(3,1):</script>:]",
        "[end-html-block:::False]",
        "[BLANK(4,1):]",
    ]
    expected_gfm = """<p>&lt;script/></p>
  <!-- some script stuff -->
</script>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


@pytest.mark.gfm
def test_disallowed_html_top_with_space_disabled():
    """
    Test to make sure that without disallowed turned on, HTML blocks preceeded by spaces are treated properly.
    """

    # Arrange
    source_markdown = """  <script>
  <!-- some script stuff -->
  </script>
"""
    expected_tokens = [
        "[html-block(1,1)]",
        "[text(1,3):<script>\n  <!-- some script stuff -->\n  </script>:  ]",
        "[end-html-block:::False]",
        "[BLANK(4,1):]",
    ]
    expected_gfm = """  <script>
  <!-- some script stuff -->
  </script>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, config_map=None)


@pytest.mark.gfm
def test_disallowed_html_top_with_space_enabled():
    """
    Test to make sure that with disallowed turned on, HTML blocks preceeded by spaces are treated properly.
    """

    # Arrange
    source_markdown = """  <script>
  <!-- some script stuff -->
  </script>
"""
    expected_tokens = [
        "[para(1,3):  ]",
        "[text(1,3):\a<\a&lt;\ascript>:]",
        "[end-para:::False]",
        "[html-block(2,1)]",
        "[text(2,3):<!-- some script stuff -->:  ]",
        "[end-html-block:::False]",
        "[html-block(3,1)]",
        "[text(3,3):</script>:  ]",
        "[end-html-block:::False]",
        "[BLANK(4,1):]",
    ]
    expected_gfm = """<p>&lt;script></p>
  <!-- some script stuff -->
  </script>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


@pytest.mark.gfm
def test_disallowed_html_top_with_list_disabled():
    """
    Test to make sure that without disallowed turned on, HTML blocks within lists with spaces are treated properly.
    """

    # Arrange
    source_markdown = """- <script>
  <!-- some script stuff -->
  </script>
"""
    expected_tokens = [
        "[ulist(1,1):-::2::  \n  \n]",
        "[html-block(1,3)]",
        "[text(1,3):<script>\n<!-- some script stuff -->\n</script>:]",
        "[end-html-block:::False]",
        "[BLANK(4,1):]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<script>
<!-- some script stuff -->
</script>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, config_map=None)


@pytest.mark.gfm
def test_disallowed_html_top_with_list_enabled():
    """
    Test to make sure that with disallowed turned on, HTML blocks within lists with spaces are treated properly.
    """

    # Arrange
    source_markdown = """- <script>
  <!-- some script stuff -->
  </script>
"""
    expected_tokens = [
        "[ulist(1,1):-::2::  \n  \n]",
        "[para(1,3):]",
        "[text(1,3):\a<\a&lt;\ascript>:]",
        "[end-para:::False]",
        "[html-block(2,3)]",
        "[text(2,3):<!-- some script stuff -->:]",
        "[end-html-block:::False]",
        "[html-block(3,3)]",
        "[text(3,3):</script>:]",
        "[end-html-block:::False]",
        "[BLANK(4,1):]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>&lt;script>
<!-- some script stuff -->
</script>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


@pytest.mark.gfm
def test_disallowed_html_top_with_list_and_tab_disabled():
    """
    Test to make sure that without disallowed turned on, HTML blocks within lists with tabs are treated properly.
    """

    # Arrange
    source_markdown = """-\t<script>
\t<!-- some script stuff -->
\t</script>
""".replace(
        "\\t", "\t"
    )
    expected_tokens = [
        "[ulist(1,1):-::4::\t\n\t\n::2]",
        "[html-block(1,5)]",
        "[text(1,5):<script>\n<!-- some script stuff -->\n</script>:]",
        "[end-html-block:::False]",
        "[BLANK(4,1):]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<script>
<!-- some script stuff -->
</script>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, config_map=None)


@pytest.mark.gfm
def test_disallowed_html_top_with_list_and_tab_enabled():
    """
    Test to make sure that with disallowed turned on, HTML blocks within lists with tabs are treated properly.
    """

    # Arrange
    source_markdown = """-\t<script>
\t<!-- some script stuff -->
\t</script>
""".replace(
        "\\t", "\t"
    )
    expected_tokens = [
        "[ulist(1,1):-::4::\t\n\t\n::2]",
        "[para(1,5):]",
        "[text(1,5):\a<\a&lt;\ascript>:]",
        "[end-para:::False]",
        "[html-block(2,5)]",
        "[text(2,5):<!-- some script stuff -->:]",
        "[end-html-block:::False]",
        "[html-block(3,5)]",
        "[text(3,5):</script>:]",
        "[end-html-block:::False]",
        "[BLANK(4,1):]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>&lt;script>
<!-- some script stuff -->
</script>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


@pytest.mark.gfm
def test_disallowed_html_top_with_block_disabled():
    """
    Test to make sure that without disallowed turned on, HTML blocks within block quotes with spaces are treated properly.
    """

    # Arrange
    source_markdown = """> <script>
> <!-- some script stuff -->
> </script>
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n]",
        "[html-block(1,3)]",
        "[text(1,3):<script>\n<!-- some script stuff -->\n</script>:]",
        "[end-html-block:::False]",
        "[end-block-quote:::True]",
        "[BLANK(4,1):]",
    ]
    expected_gfm = """<blockquote>
<script>
<!-- some script stuff -->
</script>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, config_map=None)


@pytest.mark.gfm
def test_disallowed_html_top_with_block_enabled():
    """
    Test to make sure that with disallowed turned on, HTML blocks within block quotes with spaces are treated properly.
    """

    # Arrange
    source_markdown = """> <script>
> <!-- some script stuff -->
> </script>
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> ]",
        "[para(1,3):]",
        "[text(1,3):\a<\a&lt;\ascript>:]",
        "[end-para:::False]",
        "[html-block(2,3)]",
        "[text(2,3):<!-- some script stuff -->:]",
        "[end-html-block:::False]",
        "[html-block(3,3)]",
        "[text(3,3):</script>:]",
        "[end-html-block:::False]",
        "[end-block-quote:::False]",
        "[BLANK(4,1):]",
    ]
    expected_gfm = """<blockquote>
<p>&lt;script></p>
<!-- some script stuff -->
</script>
</blockquote>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


@pytest.mark.gfm
def test_disallowed_html_top_with_block_and_tab_disabled():
    """
    Test to make sure that without disallowed turned on, HTML blocks within block quotes with tabs are treated properly.
    """

    # Arrange
    source_markdown = """> \t<script>
> \t<!-- some script stuff -->
> \t</script>
""".replace(
        "\\t", "\t"
    )
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n]",
        "[html-block(1,3)]",
        "[text(1,5):<script>\n\t<!-- some script stuff -->\n\t</script>:\t]",
        "[end-html-block:::False]",
        "[end-block-quote:::True]",
        "[BLANK(4,1):]",
    ]
    expected_gfm = """<blockquote>
\t<script>
\t<!-- some script stuff -->
\t</script>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, config_map=None)


@pytest.mark.gfm
def test_disallowed_html_top_with_block_and_tab_enabled():
    """
    Test to make sure that with disallowed turned on, HTML blocks within block quotes with tabs are treated properly.
    """

    # Arrange
    source_markdown = """> \t<script>
> \t<!-- some script stuff -->
> \t</script>
""".replace(
        "\\t", "\t"
    )
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> ]",
        "[para(1,5):\t]",
        "[text(1,5):\a<\a&lt;\ascript>:]",
        "[end-para:::False]",
        "[html-block(2,3)]",
        "[text(2,5):<!-- some script stuff -->:\t]",
        "[end-html-block:::False]",
        "[html-block(3,3)]",
        "[text(3,5):</script>:\t]",
        "[end-html-block:::False]",
        "[end-block-quote:::False]",
        "[BLANK(4,1):]",
    ]
    expected_gfm = """<blockquote>
<p>&lt;script></p>
\t<!-- some script stuff -->
\t</script>
</blockquote>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


@pytest.mark.gfm
def test_disallowed_html_inner_disabled():
    """
    Test to make sure that without disallowed turned on, inside of HTML blocks are treated normally.
    """

    # Arrange
    source_markdown = """<html>
  <script>
    <!-- some script stuff -->
  </script>
</html>
"""
    expected_tokens = [
        "[html-block(1,1)]",
        "[text(1,1):<html>\n  <script>\n    <!-- some script stuff -->\n  </script>\n</html>:]",
        "[end-html-block:::False]",
        "[BLANK(6,1):]",
    ]
    expected_gfm = """<html>
  <script>
    <!-- some script stuff -->
  </script>
</html>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, config_map=None)


@pytest.mark.gfm
def test_disallowed_html_inner_enabled():
    """
    Test to make sure that with disallowed turned on, inside of HTML blocks are treated normally.
    """

    # Arrange
    source_markdown = """<html>
  <script>
    <!-- some script stuff -->
  </script>
</html>
"""
    expected_tokens = [
        "[html-block(1,1)]",
        "[text(1,1):<html>\n  \a<\a&lt;\ascript>\n    <!-- some script stuff -->\n  </script>\n</html>:]",
        "[end-html-block:::False]",
        "[BLANK(6,1):]",
    ]
    expected_gfm = """<html>
  &lt;script>
    <!-- some script stuff -->
  </script>
</html>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


@pytest.mark.gfm
def test_disallowed_html_inner_enabled_and_not_disallowed():
    """
    Test to make sure that without disallowed turned on, inside of HTML blocks are treated normally.
    """

    # Arrange
    source_markdown = """<html>
  <something>
    <!-- some script stuff -->
  </something>
</html>
"""
    expected_tokens = [
        "[html-block(1,1)]",
        "[text(1,1):<html>\n  <something>\n    <!-- some script stuff -->\n  </something>\n</html>:]",
        "[end-html-block:::False]",
        "[BLANK(6,1):]",
    ]
    expected_gfm = """<html>
  <something>
    <!-- some script stuff -->
  </something>
</html>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


@pytest.mark.gfm
def test_disallowed_html_double_disabled():
    """
    Test to make sure that without disallowed turned on, a "double start" inside of HTML blocks are treated normally.
    """

    # Arrange
    source_markdown = """<html>
  <script<script>
    <!-- some script stuff -->
  </script>
</html>
"""
    expected_tokens = [
        "[html-block(1,1)]",
        "[text(1,1):<html>\n  <script<script>\n    <!-- some script stuff -->\n  </script>\n</html>:]",
        "[end-html-block:::False]",
        "[BLANK(6,1):]",
    ]
    expected_gfm = """<html>
  <script<script>
    <!-- some script stuff -->
  </script>
</html>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, config_map=None)


@pytest.mark.gfm
def test_disallowed_html_double_enabled():
    """
    Test to make sure that with disallowed turned on, a "double start" inside of HTML blocks are treated normally.
    """

    # Arrange
    source_markdown = """<html>
  <script<script>
    <!-- some script stuff -->
  </script>
</html>
"""
    expected_tokens = [
        "[html-block(1,1)]",
        "[text(1,1):<html>\n  <script\a<\a&lt;\ascript>\n    <!-- some script stuff -->\n  </script>\n</html>:]",
        "[end-html-block:::False]",
        "[BLANK(6,1):]",
    ]
    expected_gfm = """<html>
  <script&lt;script>
    <!-- some script stuff -->
  </script>
</html>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


@pytest.mark.gfm
def test_disallowed_html_inner_with_attributes_disabled():
    """
    Test to make sure that without disallowed turned on, an inside of HTML blocks with attributes are treated normally.
    """

    # Arrange
    source_markdown = """<html>
  <script type="text/javascript">
    <!-- some script stuff -->
  </script>
</html>
"""
    expected_tokens = [
        "[html-block(1,1)]",
        '[text(1,1):<html>\n  <script type="text/javascript">\n    <!-- some script stuff -->\n  </script>\n</html>:]',
        "[end-html-block:::False]",
        "[BLANK(6,1):]",
    ]
    expected_gfm = """<html>
  <script type="text/javascript">
    <!-- some script stuff -->
  </script>
</html>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, config_map=None)


@pytest.mark.gfm
def test_disallowed_html_inner_with_attributes_enabled():
    """
    Test to make sure that with disallowed turned on, an inside of HTML blocks with attributes are treated normally.
    """

    # Arrange
    source_markdown = """<html>
  <script type="text/javascript">
    <!-- some script stuff -->
  </script>
</html>
"""
    expected_tokens = [
        "[html-block(1,1)]",
        '[text(1,1):<html>\n  \a<\a&lt;\ascript type="text/javascript">\n    <!-- some script stuff -->\n  </script>\n</html>:]',
        "[end-html-block:::False]",
        "[BLANK(6,1):]",
    ]
    expected_gfm = """<html>
  &lt;script type="text/javascript">
    <!-- some script stuff -->
  </script>
</html>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


@pytest.mark.gfm
def test_disallowed_html_inner_with_openclose_disabled():
    """
    Test to make sure that without disallowed turned on, an inside of HTML blocks with auto-close are treated normally.
    """

    # Arrange
    source_markdown = """<html>
  <script/>
    <!-- some script stuff -->
  </script>
</html>
"""
    expected_tokens = [
        "[html-block(1,1)]",
        "[text(1,1):<html>\n  <script/>\n    <!-- some script stuff -->\n  </script>\n</html>:]",
        "[end-html-block:::False]",
        "[BLANK(6,1):]",
    ]
    expected_gfm = """<html>
  <script/>
    <!-- some script stuff -->
  </script>
</html>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, config_map=None)


@pytest.mark.gfm
def test_disallowed_html_inner_with_openclose_enabled():
    """
    Test to make sure that with disallowed turned on, an inside of HTML blocks with auto-close are treated normally.
    """

    # Arrange
    source_markdown = """<html>
  <script/>
    <!-- some script stuff -->
  </script>
</html>
"""
    expected_tokens = [
        "[html-block(1,1)]",
        "[text(1,1):<html>\n  \a<\a&lt;\ascript/>\n    <!-- some script stuff -->\n  </script>\n</html>:]",
        "[end-html-block:::False]",
        "[BLANK(6,1):]",
    ]
    expected_gfm = """<html>
  &lt;script/>
    <!-- some script stuff -->
  </script>
</html>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


@pytest.mark.gfm
def test_disallowed_html_raw_disabled():
    """
    Test to make sure that without disallowed turned on, raw HTML is treated normally.
    """

    # Arrange
    source_markdown = "This is a <noframes> example."
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):This is a :]",
        "[raw-html(1,11):noframes]",
        "[text(1,21): example.:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>This is a <noframes> example.</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, config_map=None)


@pytest.mark.gfm
def test_disallowed_html_raw_enabled():
    """
    Test to make sure that with disallowed turned on, disallowed raw HTML is treated normally.
    """

    # Arrange
    source_markdown = "This is a <noframes> example."
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):This is a \a<\a&lt;\anoframes> example.:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>This is a &lt;noframes> example.</p>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


@pytest.mark.gfm
def test_disallowed_html_raw_enabled_and_not_disallowed():
    """
    Test to make sure that without disallowed turned on, RAW HTML is treated normally.
    """

    # Arrange
    source_markdown = "This is a <something> example."
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):This is a :]",
        "[raw-html(1,11):something]",
        "[text(1,22): example.:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>This is a <something> example.</p>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


@pytest.mark.gfm
def test_disallowed_html_raw_with_attributes_disabled():
    """
    Test to make sure that without disallowed turned on, RAW HTML is treated normally.
    """

    # Arrange
    source_markdown = "This is a <noframes some=True> example."
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):This is a :]",
        "[raw-html(1,11):noframes some=True]",
        "[text(1,31): example.:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>This is a <noframes some=True> example.</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, config_map=None)


@pytest.mark.gfm
def test_disallowed_html_raw_with_attributes_enabled():
    """
    Test to make sure that without disallowed turned on, RAW HTML is treated normally.
    """

    # Arrange
    source_markdown = "This is a <noframes some=True> example."
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):This is a \a<\a&lt;\anoframes some=True> example.:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>This is a &lt;noframes some=True> example.</p>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


@pytest.mark.gfm
def test_disallowed_html_raw_with_openclose_disabled():
    """
    Test to make sure that without disallowed turned on, RAW HTML is treated normally.
    """

    # Arrange
    source_markdown = "This is a <noframes/> example."
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):This is a :]",
        "[raw-html(1,11):noframes/]",
        "[text(1,22): example.:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>This is a <noframes/> example.</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, config_map=None)


@pytest.mark.gfm
def test_disallowed_html_raw_with_openclose_enabled():
    """
    Test to make sure that without disallowed turned on, RAW HTML is treated normally.
    """

    # Arrange
    source_markdown = "This is a <noframes/> example."
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):This is a \a<\a&lt;\anoframes/> example.:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>This is a &lt;noframes/> example.</p>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )
