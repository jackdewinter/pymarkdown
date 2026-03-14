---
summary: Quick-Start documentation on PyMarkdown's Rule Plugins
authors:
  - Jack De Winter
---

# Quick Start: Managing Rule Plugins

This page helps you control which style rules PyMarkdown applies to your Markdown
files so that its checks match your project's needs. By the end, you'll know how
to configure PyMarkdown so it matches your Markdown style, instead of changing your
documents just to fit the defaults.

The commands in this section are used to enable or disable PyMarkdown's style checks,
called **rules**. When you run PyMarkdown, it applies rules to your files and reports
any problems it finds.

In practical terms:

- A **rule** is a single style check on your file.
- A **Rule Plugin** is the code that implements one rule and runs it during scanning.
- A **Rule Failure** is the reported message when that Rule Plugin detects a problem.

Once you are comfortable with the basics on this page, you can learn more in the
User Guide's [Rule Plugin](../user-guide.md#rule-plugins) section. It shows additional
ways to enable or disable Rule Plugins using configuration files and points to related
advanced
topics.

## What You Will Learn

> **Quick Start Guide Single Line Summary**
> This page provides more information on Rule Failure messages, disabling Rule Plugins,
> and suppressing a single Rule Failure in a Markdown document using Pragmas.

On this page, you will learn how to:

- read and understand PyMarkdown's Rule Failure messages
- turn specific Rule Plugins on or off to match your project's style
- suppress a single Rule Failure using Pragmas when you intentionally need to break
  a Rule Plugin

## Prerequisites

The following sections assume that you have already [installed PyMarkdown](./installation.md)
and have at least a basic familiarity with a terminal (running simple commands,
changing directories). If you are just exploring, you can still follow this page
without reading any other guides first.

If you are completely new to the command line, it is still safe to continue with
this page. However, you may find it easier if you:

- first read [Quick Start: General Command-Line Usage](./general.md) to learn how
  to open a terminal and run commands
- then read [Quick Start: Scanning Markdown Files](./scanning.md) to see a complete
  scanning example

After that, come back here to adjust how Rule Plugins behave.

### Interpreting Rule Failures

Understanding PyMarkdown's Rule Failures is essential for using Rule Plugins effectively.
This section uses a small example to explain each part of the output.

If you have already seen this example in the main Quick Start guide, this section
adds more explanation. You can continue here without going back.

#### Example: A Simple Failing File

If you created `sample.md` while following the "Quick Start: Installation" guide,
reuse that file. If not, create a new file named `sample.md` with the following
contents:

```Markdown
# First Heading
# Another First Heading
```

The next step is to run PyMarkdown on that file from the directory where you saved
`sample.md`. From a terminal opened in that directory, use one of the following
command lines to tell PyMarkdown that you want to scan that document:

<!-- pyml disable code-block-style-->
=== "Global Python Install"

    ```sh
    pymarkdown scan sample.md
    ```

=== "Pipenv Package Manager"

    ```sh
    pipenv run pymarkdown scan sample.md
    ```
<!-- pyml enable code-block-style-->

If you are not sure whether you are using Pipenv, assume you are using a global
Python install and use the **Global Python Install** command. You can always switch
to the Pipenv command later if you set up Pipenv.

Finally, after entering one of those commands, you should have been greeted with
the following output:

```text
sample.md:1:1: MD022: Headings should be surrounded by blank lines. [Expected: 1; Actual: 0; Below] (blanks-around-headings,blanks-around-headers)
sample.md:2:1: MD022: Headings should be surrounded by blank lines. [Expected: 1; Actual: 0; Above] (blanks-around-headings,blanks-around-headers)
sample.md:2:1: MD025: Multiple top-level headings in the same document (single-title,single-h1)
```

Earlier, in [Verifying PyMarkdown Installation](./installation.md#verifying-pymarkdown-installation),
you used this output to confirm that PyMarkdown was installed. But what does it
actually mean?

#### Breaking Down a Rule Failure Line

Let's take a closer look at the first line of the output and break it down:

- `sample.md:1:1:` - where the failure occurred
    - file `sample.md`, line `1`, column `1`
- `MD022: Headings should be surrounded by blank lines.` - Rule ID and human readable
  text about what failed
    - Rule ID `MD022` with a human readable name of
      `Headings should be surrounded by blank lines.`
- `[Expected: 1; Actual: 0; Below]` - optional extra data to give context to the
  failure
    - in this case, it indicates that it expected `1` blank line `below` (or after)
      the heading, but found `0` blank lines.
- `(blanks-around-headings,blanks-around-headers)` - aliases to the Rule Plugin
  that failed
    - this Rule Plugin can also be referred to by the identifiers `blanks-around-headings`
      and `blanks-around-headers`

By parsing that information, we can determine that the first failure (`MD022`/`blanks-around-headings`/`blanks-around-headers`)
was expecting 1 blank line below the first line, probably to give visual separation
from what followed in the document. (Rule Plugin identifiers are shown in the output
in upper case, but PyMarkdown treats `Md022` and `MD022` equivalently.) In that
case, the optional extra data was provided and gave needed context about the failure.

As we saw with `MD025` (`single-title` / `single-h1`), a document may have only
one top-level `#` heading. Any additional `#` headings trigger that Rule Plugin.

After examining each line of the output in detail, you should reach the following
conclusions:

- The `blanks-around-headings` Rule Plugin generated two Rule Failures because there
  is not a blank line between the two heading lines
- The `single-title` Rule Plugin generated a single failure because there are two
  top-level headings in the document

Now that you know how to read Rule Failures, the next step is to control which Rule
Plugins
run in the first place.

#### How To Fix those Rule Failures

One option is to insert a blank line between lines 1 and 2 and change line 2 from
a single `#` to `##`. That approach fixes the Markdown so that it complies with
the default Rule Plugins.

However, you might not always want to change your content. You may disagree with
the Rule Failures that Rule Plugin `MD022` or `MD025` reported, or you may have
a good
reason for your current headings. In those cases, you do not have to edit the document.
Instead, you can change which Rule Plugins apply by disabling specific Rule Plugins.

In other words, you can either:

- change the Markdown to satisfy the Rule Plugins, or
- change the Rule Plugins so they match your Markdown.

### Disabling Rule Plugins from the Command Line

Once you can read PyMarkdown's Rule Failures, the next question is which Rule Plugins
should
run at all. Sometimes you will want to turn off certain Rule Plugins so PyMarkdown
matches
your preferred style or how a specific tool renders Markdown.

Sometimes we guess wrong about which Rule Plugins should be enabled by default,
or users have good reasons to disable a Rule Plugin for their own tools.

> **Note:** As one example, our team uses [MkDocs](https://www.mkdocs.org/) to build
> this website. Different tools sometimes interpret Markdown differently, so you
> may need to adjust which Rule Plugins are enabled so that PyMarkdown's checks
> line up
> with how your tool renders Markdown. You do *not* need MkDocs to follow this guide.

#### Basic Disable Command

The easiest way to disable or enable Rule Plugins is on the command line. To disable
Rule Plugin `MD022`, we use the `--disable-rule` argument, followed by any of
the ids for the Rule Plugin itself:

<!-- pyml disable code-block-style-->
=== "Global Python Install"

    ```sh
    pymarkdown --disable-rule MD022 scan sample.md
    ```

=== "Pipenv Package Manager"

    ```sh
    pipenv run pymarkdown --disable-rule MD022 scan sample.md
    ```
<!-- pyml enable code-block-style-->

Because this disables that Rule Plugin for every command within PyMarkdown, the
two arguments must appear before the `scan` argument, which selects the **scan**
mode.

After entering one of those commands, the output changes from:

```text
sample.md:1:1: MD022: Headings should be surrounded by blank lines. [Expected: 1; Actual: 0; Below] (blanks-around-headings,blanks-around-headers)
sample.md:2:1: MD022: Headings should be surrounded by blank lines. [Expected: 1; Actual: 0; Above] (blanks-around-headings,blanks-around-headers)
sample.md:2:1: MD025: Multiple top-level headings in the same document (single-title,single-h1)
```

to:

```text
sample.md:2:1: MD025: Multiple top-level headings in the same document (single-title,single-h1)
```

#### Command Variants

- You can disable both Rule Plugins by changing `MD022` to `MD022,MD025`.
- You can also use human identifiers: `blanks-around-headings,single-title`.

#### When Command‑Line Disabling Is Not Enough

But what if you only want to disable that one specific failure of `MD025`/`single-title`,
while keeping the Rule Plugin enabled everywhere else? In that case, you need more
fine-grained
control than the `--disable-rule` option can provide.

The `--disable-rule` examples turn a Rule Plugin off everywhere; the next examples
will
show how to turn it off only for a single line.

> **Advanced topic (later):** Once you're comfortable with the basics on this page
> and want to store Rule Plugin settings in files instead of the command line, read
> [Enabling/Disabling Rule Plugins](../advanced_configuration.md#enablingdisabling-rule-plugins).

### Suppressing a Single Failure with Pragmas

Instead of turning a Rule Plugin off everywhere, Pragmas let you turn it off in
just one
place.

- **Disabling a Rule Plugin:** turns that check off for every file you scan.
- **Using a Pragma:** keeps the Rule Plugin enabled, but ignores it for one specific
  line or section.

PyMarkdown's [Pragmas](../advanced_plugins.md#suppressing-rule-failures-pragmas)
are the mechanism for that one‑off suppression.

Pragmas are most useful when you generally agree with a Rule Plugin but have a few
intentional
exceptions &mdash; for example, a page that truly needs two top‑level headings,
or a heading that must stay close to the content below it for design reasons. Even
as a new user, it is safe to use Pragmas.

A Pragma is a specially formatted line that tells PyMarkdown to handle the following
content differently, without affecting the rendered output. You can think of it
as a "PyMarkdown‑only comment" that changes how Rule Plugins are applied.

To keep this behavior hidden, Pragmas are designed to look like HTML comments. Even
if a Markdown application does not understand the Pragma, the worst that will happen
is an extra comment in the generated HTML.

Referring back to our file `sample.md`, we previously saw that disabling `MD025`
removed **all** Rule Failures from that Rule Plugin.

To keep `MD025` active but suppress only the failure on line 2, replace the contents
of `sample.md` with the following:

```Markdown
# First Heading
<!-- pyml disable-next-line MD025-->
# Another First Heading
```

This version is the same as before, except that we added a Pragma line
(`<!-- pyml disable-next-line MD025-->`) between the two headings.

If you run the `scan` command from above without the `--disable-rule` arguments,
you will now see that a failure for Rule Plugin `MD025` is no longer being reported.

Before applying that change, if you scan the `sample.md` file, you will see:

```text
sample.md:1:1: MD022: Headings should be surrounded by blank lines. [Expected: 1; Actual: 0; Below] (blanks-around-headings,blanks-around-headers)
sample.md:2:1: MD022: Headings should be surrounded by blank lines. [Expected: 1; Actual: 0; Above] (blanks-around-headings,blanks-around-headers)
sample.md:2:1: MD025: Multiple top-level headings in the same document (single-title,single-h1)
```

With that change applied, you will now see the following output:

```text
sample.md:1:1: MD022: Headings should be surrounded by blank lines. [Expected: 1; Actual: 0; Below] (blanks-around-headings,blanks-around-headers)
sample.md:2:1: MD022: Headings should be surrounded by blank lines. [Expected: 1; Actual: 0; Above] (blanks-around-headings,blanks-around-headers)
```

If you like, you can replace the identifier `MD025` with `single-title` or `single-h1`
without changing the output. Pragmas can use any identifier for a Rule Plugin, whether
it is the Rule ID or one of the Rule Plugin's aliases, to disable that Rule Plugin's
failure on a single
line.

But why are the `blanks-around-headings` failures still being reported?

#### How Pragmas Interact With PyMarkdown

When PyMarkdown scans a file, it treats Pragmas differently from normal Markdown.
First, PyMarkdown finds all the Pragmas and applies their instructions. Then it
pretends those lines are not there when it runs the Rule Plugins.

That means:

- A Pragma line does not count as content, so rules still see the same sequence
  of headings, paragraphs, and blank lines.
- However, because the Pragma line is still a "real" line in your file, the line
  numbers in error messages can shift.

In our `sample.md` example, the heading that was on line 2 moves to line 3 after
we insert the Pragma line in between. From the Rule Plugin's point of view, nothing
changed:

- it still sees one heading "followed immediately by another heading, with no blank
  line in between", and
- it still reports two `blanks-around-headings` Rule Failures.

The only difference is that those Rule Failures are now reported on lines 1 and
3 instead
of 1 and 2.

## Where to Go From Here?

On this page, you have learned how to:

- interpret Rule Failures
- disable entire Rule Plugins
- suppress individual Rule Failures with Pragmas

**Next**, in the Quick Start guide series:

- Use [Quick Start: Enabling PyMarkdown Extensions](./extensions.md) to learn how
  to enable PyMarkdown's extensions

**For** more information on topics mentioned here:

- Read [Enabling/Disabling Rule Plugins](../advanced_configuration.md#enablingdisabling-rule-plugins)
  for more advanced methods of enabling and disabling Rule Plugins

**If** you need some review:

- Select [Quick Start: Introduction](./index.md) for an overview of all Quick Start
  guides
- Select [Quick Start: Installation](./installation.md) for the steps required to
  install PyMarkdown
- Select [Quick Start: General Command Line Usage](./general.md) for information
  on the general use of PyMarkdown and the command line
- Select [Quick Start: Scanning Markdown Files](./scanning.md) to learn how to scan
  Markdown files with PyMarkdown
