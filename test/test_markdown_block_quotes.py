"""
https://github.github.com/gfm/#block-quotes
"""
from pymarkdown.tokenized_markdown import TokenizedMarkdown

from .utils import assert_if_lists_different


def test_block_quotes_206():
    """
    Test case 206:  Here is a simple example:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """> # Foo
> bar
> baz"""
    expected_tokens = [
        "[block-quote:]",
        "[atx:1:Foo:: ::]",
        "[para:]",
        "[text:bar\nbaz:]",
        "[end-para]",
        "[end-block-quote]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_block_quotes_207():
    """
    Test case 207:  The spaces after the > characters can be omitted:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """># Foo
>bar
> baz"""
    expected_tokens = [
        "[block-quote:]",
        "[atx:1:Foo:: ::]",
        "[para:]",
        "[text:bar\nbaz:]",
        "[end-para]",
        "[end-block-quote]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_block_quotes_208():
    """
    Test case 208:  (part 1) The > characters can be indented 1-3 spaces:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """   > # Foo
   > bar
 > baz"""
    expected_tokens = [
        "[block-quote:   ]",
        "[atx:1:Foo:: ::]",
        "[para:]",
        "[text:bar\nbaz:]",
        "[end-para]",
        "[end-block-quote]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_block_quotes_209():
    """
    Test case 209:  Four spaces gives us a code block:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """    > # Foo
    > bar
    > baz"""
    expected_tokens = [
        "[icode-block:    ]",
        "[text:&gt; # Foo\n&gt; bar\n&gt; baz:]",
        "[end-icode-block]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_block_quotes_210():
    """
    Test case 210:  The Laziness clause allows us to omit the > before paragraph continuation text:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """> # Foo
> bar
baz"""
    expected_tokens = [
        "[block-quote:]",
        "[atx:1:Foo:: ::]",
        "[para:]",
        "[text:bar\nbaz:]",
        "[end-para]",
        "[end-block-quote]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_block_quotes_211():
    """
    Test case 211:  A block quote can contain some lazy and some non-lazy continuation lines:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """> bar
baz
> foo"""
    expected_tokens = [
        "[block-quote:]",
        "[para:]",
        "[text:bar\nbaz\nfoo:]",
        "[end-para]",
        "[end-block-quote]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_block_quotes_212():
    """
    Test case 212:  Laziness only applies to lines that would have been continuations of paragraphs had they been prepended with block quote markers.
    """
    # TODO add case with >

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """> foo
---"""
    expected_tokens = [
        "[block-quote:]",
        "[para:]",
        "[text:foo:]",
        "[end-para]",
        "[end-block-quote]",
        "[tbreak:-::---]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_block_quotes_213():
    """
    Test case 213:  then the block quote ends after the first line:
    """
    # TODO add case with >

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """> - foo
- bar"""
    expected_tokens = [
        "[block-quote:]",
        "[ulist:-::4:  ]",
        "[para:]",
        "[text:foo:]",
        "[end-para]",
        "[end-ulist]",
        "[end-block-quote]",
        "[ulist:-::2:]",
        "[para:]",
        "[text:bar:]",
        "[end-para]",
        "[end-ulist]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_block_quotes_214():
    """
    Test case 214:  (part 1) For the same reason, we can’t omit the > in front of subsequent lines of an indented or fenced code block:
    """
    # TODO add case with >

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """>     foo
    bar"""
    expected_tokens = [
        "[block-quote:]",
        "[icode-block:    ]",
        "[text:foo:]",
        "[end-icode-block]",
        "[end-block-quote]",
        "[icode-block:    ]",
        "[text:bar:]",
        "[end-icode-block]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_block_quotes_215():
    """
    Test case 215:  (part 2) For the same reason, we can’t omit the > in front of subsequent lines of an indented or fenced code block:
    """
    # TODO add case with >

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """> ```
foo
```"""
    expected_tokens = [
        "[block-quote:]",
        "[fcode-block:`:3::::]",
        "[end-fcode-block]",
        "[end-block-quote]",
        "[para:]",
        "[text:foo:]",
        "[end-para]",
        "[fcode-block:`:3::::]",
        "[end-fcode-block]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_block_quotes_216():
    """
    Test case 216:  Note that in the following case, we have a lazy continuation line:
    """
    # TODO add case with > to show same

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """> foo
    - bar"""
    expected_tokens = [
        "[block-quote:]",
        "[para:]",
        "[text:foo\n    - bar:]",
        "[end-para]",
        "[end-block-quote]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_block_quotes_217():
    """
    Test case 217:  (part 1) A block quote can be empty:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """>"""
    expected_tokens = ["[block-quote:]", "[BLANK:]", "[end-block-quote]"]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_block_quotes_218():
    """
    Test case 218:  (part 2) A block quote can be empty:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """>
>  
> """
    expected_tokens = [
        "[block-quote:]",
        "[BLANK:]",
        "[BLANK: ]",
        "[BLANK:]",
        "[BLANK:]",
        "[end-block-quote]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_block_quotes_219():
    """
    Test case 219:  A block quote can have initial or final blank lines:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """>
> foo
>  """
    expected_tokens = [
        "[block-quote:]",
        "[BLANK:]",
        "[para:]",
        "[text:foo:]",
        "[end-para]",
        "[BLANK: ]",
        "[BLANK:]",
        "[end-block-quote]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_block_quotes_220():
    """
    Test case 220:  A blank line always separates block quotes:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """> foo

> bar"""
    expected_tokens = [
        "[block-quote:]",
        "[para:]",
        "[text:foo:]",
        "[end-para]",
        "[end-block-quote]",
        "[BLANK:]",
        "[block-quote:]",
        "[para:]",
        "[text:bar:]",
        "[end-para]",
        "[end-block-quote]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_block_quotes_221():
    """
    Test case 221:  Consecutiveness means that if we put these block quotes together, we get a single block quote:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """> foo
> bar"""
    expected_tokens = [
        "[block-quote:]",
        "[para:]",
        "[text:foo\nbar:]",
        "[end-para]",
        "[end-block-quote]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_block_quotes_222():
    """
    Test case 222:  To get a block quote with two paragraphs, use:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """> foo
>
> bar"""
    expected_tokens = [
        "[block-quote:]",
        "[para:]",
        "[text:foo:]",
        "[end-para]",
        "[BLANK:]",
        "[para:]",
        "[text:bar:]",
        "[end-para]",
        "[end-block-quote]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_block_quotes_223():
    """
    Test case 223:  Block quotes can interrupt paragraphs:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """foo
> bar"""
    expected_tokens = [
        "[para:]",
        "[text:foo:]",
        "[end-para]",
        "[block-quote:]",
        "[para:]",
        "[text:bar:]",
        "[end-para]",
        "[end-block-quote]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_block_quotes_224():
    """
    Test case 224:  In general, blank lines are not needed before or after block quotes:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """> aaa
***
> bbb"""
    expected_tokens = [
        "[block-quote:]",
        "[para:]",
        "[text:aaa:]",
        "[end-para]",
        "[end-block-quote]",
        "[tbreak:*::***]",
        "[block-quote:]",
        "[para:]",
        "[text:bbb:]",
        "[end-para]",
        "[end-block-quote]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_block_quotes_225():
    """
    Test case 225:  (part 1) However, because of laziness, a blank line is needed between a block quote and a following paragraph:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """> bar
baz"""
    expected_tokens = [
        "[block-quote:]",
        "[para:]",
        "[text:bar\nbaz:]",
        "[end-para]",
        "[end-block-quote]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_block_quotes_226():
    """
    Test case 226:  (part 2) However, because of laziness, a blank line is needed between a block quote and a following paragraph:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """> bar

baz"""
    expected_tokens = [
        "[block-quote:]",
        "[para:]",
        "[text:bar:]",
        "[end-para]",
        "[end-block-quote]",
        "[BLANK:]",
        "[para:]",
        "[text:baz:]",
        "[end-para]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_block_quotes_227():
    """
    Test case 227:  (part 3) However, because of laziness, a blank line is needed between a block quote and a following paragraph:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """> bar
>
baz"""
    expected_tokens = [
        "[block-quote:]",
        "[para:]",
        "[text:bar:]",
        "[end-para]",
        "[BLANK:]",
        "[end-block-quote]",
        "[para:]",
        "[text:baz:]",
        "[end-para]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_block_quotes_228():
    """
    Test case 228:  (part 1) It is a consequence of the Laziness rule that any number of initial >s may be omitted on a continuation line of a nested block quote:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """> > > foo
bar"""
    expected_tokens = [
        "[block-quote:]",
        "[block-quote:]",
        "[block-quote:]",
        "[para:]",
        "[text:foo\nbar:]",
        "[end-para]",
        "[end-block-quote]",
        "[end-block-quote]",
        "[end-block-quote]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_block_quotes_229():
    """
    Test case 229:  (part 2) It is a consequence of the Laziness rule that any number of initial >s may be omitted on a continuation line of a nested block quote:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """>>> foo
> bar
>>baz"""
    expected_tokens = [
        "[block-quote:]",
        "[block-quote:]",
        "[block-quote:]",
        "[para:]",
        "[text:foo\nbar\nbaz:]",
        "[end-para]",
        "[end-block-quote]",
        "[end-block-quote]",
        "[end-block-quote]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_block_quotes_230():
    """
    Test case 230:  When including an indented code block in a block quote, remember that the block quote marker includes both the > and a following space. So five spaces are needed after the >:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """>     code

>    not code"""
    expected_tokens = [
        "[block-quote:]",
        "[icode-block:    ]",
        "[text:code:]",
        "[end-icode-block]",
        "[end-block-quote]",
        "[BLANK:]",
        "[block-quote:]",
        "[para:   ]",
        "[text:not code:]",
        "[end-para]",
        "[end-block-quote]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
