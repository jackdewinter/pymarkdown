# Advanced Scanning

## Glob Support

In addition to scanning exact directories and exact files,
glob paths may be used.  While the documentation for
[glob.glob](https://docs.python.org/3/library/glob.html)
spells out everything in details, the quick and dirty answer
is simple.

If you specify a path of `*-id.md`, all files that end with
`-id.md` will be scanned. If you specify a path of `?-id.md`,
all files that start with a single character followed by
`-id.md` will be scanned.  If you specify a path of `*/*-id.md`,
any file ending with `-id.md` in the directory subdirectoy
of the current directory will be scanned.  Bringing these
together, if you specify a path of `*/a?c*-id.md`, any file
in any subdirectory that starts with an `a`, then any character,
then `c`, and ends with `-id.md` will be scanned.

Note that due to internal checking, only files that end with
`*.md` will be scanned.  This was added as a safety feature
to prevent the scanning of non-Markdown files.

## Test It Out

If you believe that a file should be included in the scanning
and it doesn't seem to be, the list files option can help you
diagnose the issue.

Used with the `scan` command, the `-l` or `--list-files` option
will determine the files to scan from the provided paths as normal.
Instead of scanning the found files, the relative path to each
found file is output to the command line.

For example, if you execute this command in the project directory:

```shell
python main.py scan -l examples
```

the output will be:

```text
examples/example-1.md
examples/example-2.md
```

Based on the setup specified in the
[Prerequistes section](https://github.com/jackdewinter/pymarkdown#prerequisites)
of the main README.md file, this is correct as that directory contains those
two files.

## Pragmas

### Reasoning

While the [Advanced Configuration document](/docs/advanced_configuration.md)
takes care of configuration the scanner at a macro level, there are
always instances where document authors need to override the rule violations
that were discovered.

A favorite one of these for me is
[Rule MD026](https://github.com/jackdewinter/pymarkdown/blob/main/docs/rule_md026.md)
which protects against punctuation characters at the end of Headings.
To be honest, 95% of the time I agree with that rule and will fix
the document to prevent this rule from triggering.  But there are also
cases where I don't agree with this rule.  Specifically, the two cases
that I run into are ending a heading with `...` or `!`.

At a high level, I agree that ending a heading with one of those two sequences
is a bad thing to do.  But due to my writing style, even after trying to
find another way of stating the header that does not include either sequence,
there are times that I really believe those sequences are the best option.
Only in those cases, after I have reviewed them and tried to rewrite them,
do I want to effectively mark those violations as "reviewed and please ignore".

### How Do I Deal With These?

It is times like this that
[pragmas](https://jackdewinter.github.io/2021/05/17/markdown-linter-road-to-initial-release-dotting-the-is/#pragmas)
come into play.  The linter supports a very simple form or pragmas that allow
a specific set of rules to be ignored for a single line.  To accomplish
this, a line of one of the following two forms is placed in the Markdown
document.  This text must be at the start of the line and be the only thing
on the entire line.

```Markdown
<!-- pyml disable-next-line no-multiple-space-atx-->
```

or

```Markdown
<!--- pyml disable-next-line no-multiple-space-atx,md019-->
```

The first part of the HTML comment, the text up to the end of
the `disable-next-line` is getting the pragma in context and
ensuring that it knows that the next line is to be ignored.
After one or more whitespace characters, the rest of the line
up to the `-->` sequence is a comma-separated list of rules
that are to be disabled for that next line.  The identifier
used in that list can either be the rule's id, such as `md019`,
or one of the rules aliases, such as `no-multiple-space-atx`.
Any duplication of the identifiers is ignored.  As such, both
Markdown pragmas above will disable Rule md019 on the line
following the pragma:

```Markdown
# Top Level Header

<!--- pyml disable-next-line no-multiple-space-atx-->
##     Too Many Spaces At the Start Of This One

More text here.
```

### Why Not Allow Disabling For More Than One Line?

Partially because it is a slippery slope argument.  Allowing for
the disabling of a rule for the next line just makes sense for me.
Handle exceptions that come up during documents.  After that, I
am concerned that adding one more command will actually entail
adding 5+ commands just to ensure that the one command can be
controlled properly.  At the start, I decided I wanted to keep
things simple if possible.

Partially because it is easier and more performant.  From a
low level perspective, this is implemented as a list of line numbers
and the rule ids that should be ignored if a violation is reported.
That is a very quick check with few downsides.  Starting to add
`enable` or `disable` or `restore` or any other commands probably
mean enabling all rules and applying any pragmas after the rules
had fired.  In my mind, That would degrade the performance of the
linter unnecessarily.

Partially because it just makes more sense to me.  While I can
make arguments for other pragma commands, I can replicate most
of those commands by creating a different configuration file
for different Markdown hierarchies.  For me, a pragma should
be used to handle exceptions, not to handle the general case.

Now, that being said, I am willing to be influenced on this
topic.  But as a starting point, this is where I landed.
