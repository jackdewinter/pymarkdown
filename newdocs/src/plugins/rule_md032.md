# Rule - MD032

| Property | Value |
| --- | -- |
| Aliases | `md032`, `blanks-around-lists` |
| Autofix Available | Pending |
| Enabled By Default | Yes |

## Summary

List blocks should be surrounded by blank lines.

## Reasoning

### Readability

By separating
List elements from the other elements in a document, their
existence in the document is highlighted.  In addition, some parsers
may not properly recognize the List elements without the extra
blank lines on both sides.

## Examples

### Failure Scenarios

This rule triggers when the List element is either not
prefaced with Blank Lines:

````Markdown
This is text.
+ a list
````

or followed by Blank Lines:

````Markdown
1. a list
# This is any non-text block
````

### Correct Scenarios

This rule does not trigger when there is a single
Blank Line both before and after the List element:

````Markdown
This is text and a blank line.

+ a list

This is a blank line and some text.
````

This rule will also not trigger if the List element is at the
very start or the very end of the document.  

In addition, this rule will not trigger if a List element
is found directly within the scope of another List element. If
a List element is found directly within the scope of a Block
Quote element, then this rule behaves normally.

#### Additional Scenarios - Paragraphs and Indented Code Blocks

Due to the [GitHub Flavored Markdown](https://github.github.com/gfm/) specification's
there are three scenarios that appear to be violations of this rule, but are not. In
all of these scenarios, if the text on line four is not meant to be part of the list,
an inserted blank line will properly convey that intent to most parsers.

The first scenario is the text:

````Markdown
This is text and a blank line.

+ a list
This is some text.
````

Because of the specification's use of [Lazy Continuation Lines](https://github.github.com/gfm/#example-268),
the fourth line in the above example is considered a "lazy" continuation of
the list started on line three. Essentially, the list has a single list item
with the text `a list This is some text.`.  

The second scenario is following a list with an indented code block:

````Markdown
This is text and a blank line.

+ a list
    This is some text.
````

While there may be the writer's intent to follow the list with an indented code
block, most parsers will clearly see line four as a continuation of the list
started on line three, but with two extrace spaces of indentation.

#### Additional Scenarios - Multiline Leaf Elements

Finally, the third scenario is any list that is followed by a multiline leaf element,
such as the link reference definition element, the setext Headings element, or the
table element. As noted in the first two scenarios, having plain text that does
not explicitly start a new container block or leaf block usually causes the parsers
to assume that the plain text is part of the list itself.  In that situation, most
parsers explicitly check to see if that new line is part of a list continuation
or if a new element has been specified.

In the case of multiline elements, it is difficult to determine from a single line
whether a given multiline element is valid.  While the following example:

````Markdown
+ a list

[lrd]:
/url
````

is clearly a list element followed by a link reference definition (due to the newline
between the two), the following example creates doubt as to the correct parsing of the
example:

````Markdown
+ a list
[lrd]:
/url
````

To properly parse this, our parser and other parsers would need to mark their position
and state, parse the possible link reference definition, restoring the marked position
and state if the parsing failed.  As the majority of parsers do not perform that
extra level of care, our parser follows that majority and assumes that lines two
and three are part of the list started on line one.

It therefore follows that if our parser treats that scenario as a continuation of the
list item, this rule sees a single list item with nothing after it.  Therefore,
the rule does not trigger in this scenario and reduces to be in the same set as
the first scenario in the previous section.

## Fix Description

The auto-fix feature for this rule is scheduled to be added soon after the v1.0.0
release.

## Configuration

| Prefixes |
| --- |
| `plugins.md032.` |
| `plugins.blanks-around-lists.` |

| Value Name | Type | Default | Description |
| -- | -- | -- | -- |
| `enabled` | `boolean` | `True` | Whether the plugin rule is enabled. |

## Origination of Rule

This rule is largely inspired by the MarkdownLint rule
[MD032](https://github.com/DavidAnson/markdownlint/blob/main/doc/Rules.md#md032---lists-should-be-surrounded-by-blank-lines).
