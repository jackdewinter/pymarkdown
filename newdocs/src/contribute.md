---
summary: How to contribute to the application.
authors:
  - Jack De Winter
---

# Contributing

Thanks for your interest in contributing to this application!

Here is a roadmap of what this page covers:

- [How To Go About Helping Us](#how-to-go-about-helping-us)
- [Are There Any Guidelines?](#are-there-any-guidelines)
- [Types of Contributions](#types-of-contributions)
- [Next Steps](#next-steps)

## How To Go About Helping Us

If your idea does not immediately fit our roadmap, or you are simply looking for
a way to help, we will work with you to find a contribution that aligns with the
project's direction. This section explains how to think about that and what to
do next.

You might be in one of two situations:

1. **You have a concrete idea.**

    You submit it to our
    [issues list](https://github.com/jackdewinter/pymarkdown/issues),
    and we respond that it will take time or does not fit the project's direction.

    In that case:

    - Read our feedback carefully. We review each issue seriously and try to be clear
      about constraints and priorities.
    - If the idea is important to you, contributing is often the best way to move
      it forward while still respecting the project's direction.
    - While your idea may not fit our roadmap, we can work with you to figure out
      if your idea has merit outside of our project, and how you can realize that.

2. **You want to help but do not have a specific idea yet.**  

    You might be looking for something you can
    [sink your teeth into](https://dictionary.cambridge.org/dictionary/english/sink-teeth-into),
    want to build your open-source resume, or just want to explore the project.

If you are sincere about helping and can collaborate effectively with our
team, we will work with you to see how you can help us out.

## Are There Any Guidelines?

Yes, definitely. And we are relaxed about most of our guidelines. But there
are certain things we will not budge on.

### Test Coverage

We worked hard to get 100% code coverage and nearly 100% scenario coverage. Code
coverage is easy; covering every scenario is not. By being strict about this from
the start, we reduce the number of issues our users encounter. That also helps ensure
that most remaining reports are truly new scenarios we did not anticipate.

### Static Project Analysis

We rely heavily on static project analysis. In practice, this means that before
opening a Pull Request, you should run `clean.cmd` (on Windows) or `clean.sh`
(on Unix-like systems).

These scripts:

- Run our standard static checks (including those configured in Pre-Commit).
- Perform extra tasks that are simpler to manage in a script, such as verifying
  that the `Pipfile` used by Pipenv is up to date as the first task.

We keep these checks in a script, rather than only in our Pre‑Commit configuration,
so that we can adjust and extend them more easily. This approach has saved us from
configuration problems many times. As a result, we plan to keep it.

### One Major Change Per Pull Request

Our guideline is simple:

- **Submit only one major change per Pull Request.**
- Minor, closely related fixes are acceptable.
- If your PR bundles many unrelated changes (or your title has multiple "and"s),
  split it into smaller PRs to keep reviews focused.
    - **Do:** Group logically related changes that support a single goal.
    - **Don't:** Combine refactors, new features, and large cleanups in one PR.

Once you are familiar with these guidelines, the next step is to decide how you
would like to contribute.

## Types of Contributions

Before you pick a contribution type, make sure you have read
["Are There Any Guidelines?"]( #are-there-any-guidelines ).

Our contributions generally fall into three categories. These are not the
only categories, just the most frequently asked for ones. In short:

- If you want to tweak how an existing Rule Plugin behaves, add a configuration value.
- If you want to enforce a new kind of check, add a new Rule Plugin.
- If you want to support a new Markdown-like construct, add an extension.

The three main paths are:

- [Adding A New Configuration Value To An Existing Rule Plugin](#adding-a-new-configuration-value-to-an-existing-rule-plugin)
- [Add A New Rule Plugin](#add-a-new-rule-plugin)
- [Add A New Extension](#add-a-new-extension)

### Adding A New Configuration Value To An Existing Rule Plugin

Refine the behavior of an existing Rule Plugin without changing its core purpose.

> "This Rule Plugin is just what I want, except that it does not do..."

As an example:

> "Rule Plugin `MD013`/`line_length` is almost perfect, but I need a way to ignore
> fenced code blocks."

If the thing that it does not do is aligned with the purpose of the Rule Plugin,
we
are all for adding configuration options. One of the main problems our team has
with other Markdown linters is that some Rule Plugins are supposed to check one
thing.
In practice, they also end up checking something unrelated as a side effect.

If the configuration option matches the Rule Plugin's purpose, we are happy to
add it.
If it does not, we will usually suggest creating a new Rule Plugin that focuses
on the
specific behavior you have in mind instead.

For configuration-only changes, you will typically:

- Update the Rule Plugin's configuration definition (for example, in the same Python
  module as the Rule Plugin implementation).
- Adjust the Rule Plugin's configuration schema and default values.
- Extend the Rule Plugin's tests to cover the new configuration behavior.

In most cases, Rule Plugins live under `pymarkdown/rules/md0xx_*.py` or `pymarkdown/rules/pml0xx_*.py`,
and the scenario tests live under `tests/rules/` in files whose names are prefixed
with `test_`.

### Add A New Rule Plugin

Introduce a new, focused Rule Plugin to cover a behavior not handled today.

> "I wish there was a Rule Plugin that would check for..."

As an example:

> "I wish there was a Rule Plugin that would warn when a heading is followed by more
> than 3 paragraphs without a subheading."

This is an extension of the last section on new configuration, just with larger
scope. We believe that each Rule Plugin should have a single, well-defined trigger.
Configuration
values can supplement that behavior, but must remain aligned with that core purpose.

It should also be noted that the best way to propose a new Rule Plugin is to do research
and have a description that is well thought out.

We typically start our Rule Plugin development by writing the Rule Plugin's description
page first.
We write the Python code only after we are sure of the requirements. This is not
required, but we find it helps us out immensely. You can look at any existing Rule
Plugin
description in our documentation as a template.

Each Rule Plugin description page corresponds to a specific Rule Plugin in the codebase.
When creating a new Rule Plugin, you will:

- Add a Rule Plugin description page using an existing Rule Plugin as a template.
- Implement the rule in the Rule Plugin package (alongside other `PMLxxx` Rule Plugins).
- Add scenario tests for the Rule Plugin's behavior and configuration.

In practice, the Rule Plugin module will be `pymarkdown/rules/pml0xx_*.py`, and
the scenario
tests live under `tests/rules/` in files whose names are prefixed with `test_`.
Reuse the same primary identifier across these locations.

### Add A New Extension

Extend PyMarkdown's parsing or behavior to support new Markdown-like features.

> "Doesn't PyMarkdown support the ability to do... that I use on my website?"

As an example:

> "Doesn't PyMarkdown support GitHub-style task lists (`- [ ]` / `- [x]`) that I
> use in my project README?"

Extensions generally touch more parts of the system than Rule Plugins. For example,
the [Pragmas Extension](./extensions/pragmas.md) needs to run early in the parsing
sequence. That ensures Pragmas are handled before other processing.
The [StrikeThrough Extension](./extensions/strikethrough.md) instead builds on the
existing inline emphasis support by adding additional emphasis markers.

Extension implementations register themselves with the parser's extension manager.
In practice, extensions plug into specific stages of the parsing pipeline:

- "System-Wide" extensions perform some other action that impacts how the rest of
  PyMarkdown works
    - An example of this is how the [Pragma Extension](./extensions/pragmas.md)
      allows "notes" to be left in the document for the Rule Engine, while staying
      invisible to the rules themselves.
- "Container" extensions modify the main block processing and affect the positioning
  of other tokens.
    - Introducing a new container type &mdash; that is, an element that contains
      other elements &mdash; would be this type of extension.
- "Leaf" extensions run at a normal parsing level and provide the majority of the
  structure that becomes visible to the user.
    - An example of this is how the [Markdown Tables Extension](./extensions/markdown-tables.md)
      formats blocks of text in a table format instead of a paragraph format.
- "Inline" extensions augment or override inline token handling
    - An example of this is how the [StrikeThrough Extension](./extensions/strikethrough.md)
      affects emphasis.
- "Cosmetic" extensions provide small changes to how existing elements are parsed
    - An example of this is how the [Markdown Task List Items](./extensions/task-list-items.md)
      slightly modifies the normal List tokens to create Task Lists.

When we discuss a new extension idea with you, we will help you select the appropriate
hook points based on whether your extension needs early access or can reuse existing
tokens.

And then there are the scenario tests. We aim to cover both typical and problematic
ways an extension might be used, so that the extension behaves reliably in as many
situations as possible.

For example, extensions live under `pymarkdown/extensions/`, their documentation
under `newdocs/src/extensions/`, and scenario tests under `tests/rules/`. Reuse
the same extension identifier across these locations. Those scenario tests are run
as part of our normal test and `clean` workflows.

## Next Steps

If none of this has scared you off, you may want to consider helping our team
out with the development of this project. Even if it is only for something
small, we can help you learn what you need to contribute.

When you are ready, start by opening an issue in our
[issues list](https://github.com/jackdewinter/pymarkdown/issues) to discuss
your idea or proposed change, and then move on to a Pull Request once we have
aligned on the approach.
