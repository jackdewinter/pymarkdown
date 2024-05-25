# Pragmas

| Item | Description |
| --- | --- |
| Extension Id | `pragmas` |
| GFM Extension Status | Unofficial |
| Configuration Item | `extensions.linter-pragmas.enabled` |
| Default Value | `True` |

## Summary

This extension allows for the parsing of "pragmas" that provide extra
information to the PyMarkdown parser.  This information is then used
by the PyMarkdown linter (plugin rule engine) to alter how rule
violations are processed.

The most common use case for pragmas is to disable any rule violations
on the following line after manual verification by the user.

While the reasoning behind pragmas is covered
[in this section](https://github.com/jackdewinter/pymarkdown/blob/main/docs/advanced_scanning.md#pragmas),
this document covers pragmas as a more general topic.

## Extension Specifics

The [GitHub Flavored Markdown](https://github.github.com/gfm/) specification
focuses on the parsing of Markdown and the uniform generation of HTML based on
that parsing.  As such, the authors of that document did not provide anything
in that specification that addresses the needs of GFM compliant linters, such
as PyMarkdown.

### History

The various linters and analyzers in existence today already have proven
mechanisms to deal with suppressing the notifications that each application
scans for.  Whether those notifications are called issues, failures, or
violations, the need is the same.  Each application provides a high-level
syntactical construct that allows the reporting of those items to be suppressed.
A small collection of those constructs are as follows:

- [PMD](https://pmd.github.io/latest/pmd_userdocs_suppressing_warnings.html)
  - Java Code Analyzer
  - `@SuppressWarnings("PMD.isse")`
- [PyLint](http://pylint.pycqa.org/en/latest/user_guide/message-control.html)
  - Python Code Linter
  - `# pylint: disable=issue`
- [Markdown Lint](https://github.com/DavidAnson/markdownlint#configuration)
  - Node.js Markdown Linter
  - `<!-- markdownlint-disable MD037 -->`

In each case, either a code object is either annotated with another code
object or the code is commented with a comment statement.  Both constructs
contain all the information needed to request the application to ignore
a given set of class of failures.

### Specifics

To provide a consistent and common way to suppress rule violations
for Markdown documents, the pragma format of a specialized HTML comment is
used.

For clarity in the following sections, any mention of the word "whitespace"
refers to either the space character or the tab character.

#### Pragma Statements

Pragmas must occur at the start of the line.  No initial whitespace is allowed.
The pragma appears to be a normal HTML comment, starting with the character
sequence `<!--` or the character sequence `<!---`, and ending with the character
sequence `-->`.  As some editors do not clearly show trailing whitespace
characters, any number of whitespace characters may follow
the closing character sequence.  Within the bounds of the HTML comment, the
pragma data is preceded by zero or more whitespace characters, the character
sequence `pyml` and a single space character. The remaining text is
the pragma command.

To put this into practical terms, a valid pragma line matches the following
regular expression:

```regex
^<!--[\t\s]*pyml\s(.*)[\t\s]*-->[\t\s]*$
```

where the group `(.*)` is the pragma command.

Regardless of whether the extracted pragma command is valid or not, once
a pragma statement has been identified, it is completely removed from the
parser's purview.  The pragma command is then stored in a separate list,
one dedicated for pragmas.  The line containing the pragma then seems to
disappear from the parser's point of view.  The reason for this is presented
in the
[last section](#removal-of-the-pragma-statement-from-the-markdown-token-stream)
of this document.

#### Pragma Commands

The extracted pragma commands are stored in a list for post-parsing processing.
This further processing
must occur after that parsing and before the linter is executed, as
pragma commands may affect which rule violations are emitted by the linter.
If there are any errors processing the pragma commands, errors will be
reported. These errors, which should look similar to rule violations,
will be raised for the failing pragma command.  Like how rule
violations are handled, pragma processing errors should not prevent
further processing of other pragma commands and the linter pass itself.

When processed, there are three outcomes for any pragma command.  The first
is that the command was a valid command and validly formed (see the next
section for more details), and it was consumed without any errors.  In that
outcome, nothing additional is output.

The second outcome is that there was no pragma command specified, in which
case, something like the following text is output:

```text
file.md:1:1: INLINE: Inline configuration specified without command.
```

Similarly, if the pragma command was not one of the available commands,
something similar to the following is output:

```text
Inline configuration command 'bad-command' not understood.
```

#### Available Commands

The only two commands currently in place are the `disable-next-line` command
and the `disable-num-lines` command.

Note that due to the reasons mentioned
[in this section](https://github.com/jackdewinter/pymarkdown/blob/main/docs/advanced_scanning.md#pragmas),
sufficient reasons must be presented as to why the number
of pragma commands should be increased.  As noted, this is not for
any other reason than to keep the system simple and performant.

##### Disable-next-line Command

After one or more whitespace characters, a comma-separated
list of identifiers specifies the rules to disable only for the line
directly following the line containing the pragma.

Errors will be issued if:

- a rule identifier (id or name) is not provided
- the rule identifier is not a valid or name

Therefore, a proper command to suppress rule id `md031` on the next line
is `disable-next-line md031` or `disable-next-line blanks-around-fences`.

##### Disable-num-lines Command

After one or more whitespace characters, a positive integer is followed by
one or more whitespace characters and then a comma-separated
list of identifiers.  The integer specifies the count of lines that the disable
command will span and the list of identifiers specify the rules to disable.
In essence, this is a multiline form of the `disable-next-line` command.
If there are any issues parsing the command's parameters, they will be reporting
in the same manner as the errors for the `disable-next-line` command.

Errors will be issued if:

- a count was not specified, and therefore, one or more rule identifiers were
  not specified
- a count was not specified as a positive integer
- one or more rule identifiers (id or name) were not provided
- the rule identifier is not a valid or name

Therefore, a proper command to suppress rule id `md031` on the next three lines
is `disable-num-lines 3 md031` or `disable-num-lines 3 blanks-around-fences`.

###### Why Was This Introduced?

Making this small change involved a lot of discussion and experimentation.
On one side, providing a `disable` command and an `enable` command might have
been more useful, but had a lot of simplicity issues.  What does the logic
look like if `disable` is called more than once?  Same question, but for
`enable`?  Is there a way to apply `disable` to everything?  We felt that
there were just too many questions.

On the other side, having a `disable` command that spans an explicit number of
lines provides the same functionality with only one complicated question.
What happens if we `disable` for 100 lines on the last line of the document?
The answer to that disable question has a simple answer.  The command will
record a range from that line to the 100th line following it, just like with
any other range.  Because it is on the last line of the document, it will
have no effect, but it will still record the range.

From that point of view, it was just an easy choice.

#### Removal Of The Pragma Statement From the Markdown Token Stream

The removal of the pragma statement takes some getting used to, but it is
logical and just makes sense. As the pragma statements provide the Markdown
document with the ability to communicate with the linter, it logically
should not appear in the token stream.  Take this example:

```Markdown
some paragraph

#  My Bad Atx Heading

some other paragraph
```

and assume that the Atx Heading element on line 3 raises a rule violation
for rule `no-multiple-space-atx` because it starts with multiple spaces. To
suppress that rule violation using a pragma, the appropriate pragma command
to add is `disable-next-line no-multiple-space-atx`, as follows:

```Markdown
some paragraph

<!--- pyml disable-next-line no-multiple-space-atx-->
#  My Bad Atx Heading

some other paragraph
```

If that pragma is not "invisible" to the parser, then adding the pragma statement would
cause Rule md022 to trigger, because an Atx Heading element is
not preceded by one blank line.  It does not make sense to have
to add a pragma to conceal the presence of another pragma.  The most
logical thing to do is to have that parser just ignore the presence of
the pragma, avoiding that need altogether.
