# Pragmas

| Item | Description |
| --- | --- |
| Extension Id | `linter-pragmas` |
| GFM Extension Status | Unofficial |
| Configuration Item | `extensions.linter-pragmas.enabled` |
| Default Value | `True` |

## Configuration

| Prefixes |
| --- |
| `extensions.linter-pragmas.` |

| Value Name | Type | Default | Description |
| -- | -- | -- | -- |
| `enabled` | `boolean` | `False` | Whether the extension is enabled. |

## Summary

This extension allows the PyMarkdown parser to look for "pragmas" that provide
metadata about a Markdown document.  This information is then used by the rule
engine to alter how failures are processed.

The most common use case for pragmas is to disable rule violations for a specific
rule on the line that follows the pragma.  As a logical extension of this, there
is also a form of the pragmas that disables rule violations for a specified number
of lines after the pragma.

## Examples

The following Markdown text:

```Markdown
some paragraph

#  My Bad Atx Heading

some other paragraph
```

causes PyMarkdown to report a failure of `no-multiple-space-atx` on line 3.
With this extension enabled, the following Markdown text:

```Markdown
some paragraph

<!--- pyml disable-next-line no-multiple-space-atx-->
#  My Bad Atx Heading

some other paragraph
```

will not cause PyMarkdown to report a failure.

## Specifics

The [GitHub Flavored Markdown](https://github.github.com/gfm/) specification
focuses on the parsing of Markdown and the uniform generation of HTML based on
that parsing.  As such, the authors of that document did not provide any guidance
in the specification that addresses the needs of GFM compliant linters.  The
pragmas extension was created to specifically solve the problem of being able
to suppress a specific instance of a rule failure being reported.

### Nomenclature

The word [pragma](https://en.wikipedia.org/wiki/Directive_(programming)) is a
term used to specify an instruction that tells a language compiler or interpreter
how to interpret the object it is processing.

### History

Existing linters have proven mechanisms to deal
with the suppression of notifications that they generate.  Whether
those notifications are called issues, failures, or violations, the need is the same.
Each of these applications needs a mechanism embedded within the object being
scanned that tells the application that the notification is not required as
it has been manually verified by the user.

Consider the case of a text document and a word processor.  Once you load
the document into the word processor application, various numbers of red and
blue lines will appear in your view of the document.  Based on age old
[editing standards](https://en.wikipedia.org/wiki/Blue_pencil_(editing)), the
red lines typically show spelling errors while the blue lines typically show
grammar and other errors.  However, when you click on those lines in most
word processors, a context menu comes up and gives you options: different
ways in which to correct the error or an option to ignore the error.

Linting applications are no different.  There are a set of rules that the user
has asked to be applied to the object being scanned.  When an error is found,
users either want to fix the error or to ignore that failure without
turning that rule off.  Relating to the word processor example above, if you have
a spelling error in your document, you do not want to turn off all spell checking
because you disagree with one error.  You want options to deal with it on a more
granular level.

When looking at other linters for ideas on how to present failure suppressions
to the user, we looked at popular linting applications for inspiration:

- [PMD](https://pmd.github.io/latest/pmd_userdocs_suppressing_warnings.html) -
    Java Code Analyzer
    - `@SuppressWarnings("PMD.issue")`
- [PyLint](http://pylint.pycqa.org/en/latest/user_guide/message-control.html) -
    Python Code Linter
    - `# pylint: disable=issue`
- [Markdown Lint](https://github.com/DavidAnson/markdownlint#configuration) -
    Node.js Markdown Linter
    - `<!-- markdownlint-disable issue -->`

We quickly noted that in each case, the suppression mechanism is either a code annotation
or a specific form of comment that the application can process.  Another important
feature is that the suppression object contains all required information needed to
identify the suppression.

There were also negative things that we noted. The first thing is that the PMD
suppression attaches to an object, such as a class or a method, and applies to
anything within the scope of that object.  The second thing is that PyLint suppressions
are enabled or disabled from the point of the suppression, until the end of the
file or the opposite enabled/disable is found.  As the PyMarkdown linter is written
in Python and we use PyLint on our code, we can relate many stories of disabling
an issue early on in a module, causing us to miss a real problem later in that
same module.  We ran into this issue so often that we wrote a simple parser to
help us detect these cases in our Python code, allowing us to address them.

Based on those experiences, our team decided that we prefer to have the
suppression specified exactly where it is needed without the need for checking
scope and without the need for looking for matching disable/enable statements.

### Implementation

After looking at examples from other applications, our team decided that
for Markdown documents, a specialized HTML comment block (multiline text that starts
with `<!--` or `<!---` and ends with `-->` or `--->`) was the best option.  In addition,
we decided to break the "statement" part of interpreting pragmas away from the "interpretation"
part of interpreting pragmas.

#### Pragma Statements

Pragmas must occur at the start of the line.  No initial whitespace is allowed.
The pragma is a normal HTML comment, starting with the character
sequence `<!--` or `<!---`, and ending with the character
sequence `-->` or `--->`.  As some editors do not clearly show trailing whitespace
characters, any number of whitespace characters may follow
the closing character sequence.  Within the bounds of the HTML comment, the
pragma data is preceded by zero or more whitespace characters, the character
sequence `pyml` and a single space character. The remaining text within the
command block is referred to as the pragma command.

To put this into practical terms, a valid pragma line matches the following
regular expression:

```regex
^<!--[\t\s]*pyml\s(.*)[\t\s]*-->[\t\s]*$
```

where the group `(.*)` is the pragma command.

##### Removal From Document Stream

Regardless of whether the extracted pragma command is valid or not, once
a pragma statement has been identified, it is completely removed from the
parser's purview.  The pragma command is then stored in a separate list along
with its location metadata.

The removal of the pragma statement from the parser's view takes getting used to,
but it is a logical action. Each pragma provides instructions to the parser on how
to handle that part of the document, it does not provide content for the document.
As pragmas do not provide content, the processing would get complicated if the pragma
statement was not removed from the parser's view.

Take this Markdown as an example:

```Markdown
some paragraph

#  My Bad Atx Heading

some other paragraph
```

With PyMarkdown's default settings, the Atx Heading element on line 3 raises a failure
for rule `no-multiple-space-atx` because the heading starts with multiple spaces.
To suppress that rule violation using a pragma, the appropriate pragma command
to add is `disable-next-line no-multiple-space-atx`, as follows:

```Markdown
some paragraph

<!--- pyml disable-next-line no-multiple-space-atx-->
#  My Bad Atx Heading

some other paragraph
```

If that pragma is not "invisible" to the parser, then adding the pragma statement
has a cascading effort, causing Rule Md022 to trigger.  That is because Rule Md022
mandates that Heading elements are surrounded by blank lines. Then you would need
to have a pragma to suppress that failure... which we believe is just inefficient
and messy.

By removing the pragma (and therefore the pragma line) from the parser's viewpoint,
everything is simplified.  The pragma data is stored in separate storage so it
can be acted on properly, while not interfering with the parser's work of processing
the Markdown text.

#### Pragma Commands

As mentioned above, pragma commands are stored in a list for post-parsing processing.
Any errors processing the pragma commands are handled in the same manner as with
rule failures.

When a valid pragma command is processed, the extension does not emit any information.
If there are any errors, an `INLINE` error is generated with a clear indication of
the error that was raised.  For example, given the following three invalid pragma
commands:

```Markdown
 <!--- pyml -->
 <!--- pyml bad -->
 <!--- pyml disable-num-lines a a -->
```

the following failures are generated:

```text
{filename,row,col}: INLINE: Inline configuration specified without command.
{filename,row,col}: INLINE: Inline configuration command 'bad' not understood.
{filename,row,col}: INLINE: Inline configuration command 'disable-num-lines' specified a count 'a' that is not a valid positive integer.
```

Note that as with rule failures, pragma command failures do not stop the parsing
of the Markdown document.

#### Available Commands

The two commands currently in place are the `disable-next-line` command
and the `disable-num-lines` command. By keeping things simple, our team
hopes to keep pragmas understandable and their implementation simple.

##### Disable-next-line Command

The `disable-next-line` command is followed by at least one whitespace character
and a comma-separated list of identifiers. Those identifiers specify one or more
rules that will have their ability to generate failures suppressed for the
line after the pragma command.

Command parsing failures are issued if:

- a rule identifier (id or name) is not provided
- the rule identifier is not a valid id or name

Therefore, a proper command to suppress rule id `md031` on the next line
is `disable-next-line md031` or `disable-next-line blanks-around-fences`.

```Markdown
some paragraph
<!--- pyml disable-next-line blanks-around-fences-->
#  My Bad Atx Heading
some other paragraph
```

##### Disable-num-lines Command

The `disable-num-lines` command is followed by at least one whitespace character,
a positive integer, at least one whitespace character, and a comma-separated list
of identifiers. Those identifiers specify one or more
rules that will have any generation of failures suppressed for the specified number
of lines after the pragma command.

Command parsing failures are issued if:

- a count was not specified, and therefore, one or more rule identifiers were
  not specified
- a count was not specified as a positive integer
- one or more rule identifiers (id or name) were not provided
- the rule identifier is not a valid id or name

Therefore, a proper command to suppress rule id `md031` on the next three lines
is `disable-num-lines 3 md031` or `disable-num-lines 3 blanks-around-fences`.

```Markdown
<!--- pyml disable-num-lines 3 blanks-around-fences-->
some paragraph
#  My Bad Atx Heading
some other paragraph
```
