# Rule - MD049

| Aliases       |
|---------------|
| `md049`       |
| validate-refs |

## Summary

Ensure that all references to parts of the documentation are valid.

## Reasoning

### Ensuring Correctness

Invalid URLs for links and images can be a significant issue in documentation.
Manually validating each link and image is a time-consuming task.
With this rule, you can automatically validate the references to various
parts of the documentation, such as links and images.

This helps to ensure the correctness and integrity of the documentation by
identifying and flagging any invalid or broken references.

## How it works

This rule validates all references in the scanned Markdown files, checking the
existence of the referenced asset/image or heading.

### Local Images and asset files

When the linter classifies a token as an image or a linked asset with a relative
URL, the rule uses `os.path.exists` to check if that file exists in the
filesystem. It uses the current working directory of the pymarkdown process as
its base path and concatenates the URL of the referenced file. If it does *not*
exist, it reports a linter error for that dangling reference.
Therefore, linked images and assets *don't* need to be in a special `asset`
folder.

You can whitelist (exclude) URLs by regex. See [Configuration](#configuration).

For example, to not check any URLs containing `Sandbox`, just set

```ini
plugins.validate-refs.regex=".*\/Sandbox/.*"
```

### Anchors and Headings

This plugin also supports the validation of anchors to markdown headings.
The heading could be in the same markdown file or in another markdown file that
is scanned in the same pymarkdown run.

To scan each file only once, all anchors are stored in a global map grouped by
filename. When an anchor (link to a heading) is validated, the rule checks if
the file exists and is a Markdown file.

There are two possible cases:

1. If the headings of the file have already been processed, the rule compares
the anchor with all headings of the referenced file using kebab case
comparison. If none of the headings match the anchor, an error is reported.

2. If the map does not contain headings for the referenced file, the anchor
link is stored in a separate list. When the linter scans the referenced file
later, all headings are processed as before and compared with the stored
anchors. Like before, if an anchor in the list does not match a heading, an
error will be reported.

## Examples

### Failure Scenarios

This rule triggers when an anchor link has no matching heading in any markdown
file.

```
scanned folder
 | docs.md
 \ readme.md
```

```Markdown
# readme.md

See the [documentation](docs#config) for basic configuration options.
```

```Markdown
# docs.md

## Configuration

Here are the basic config options.
```

In this case the `readme.md` file has an anchor link to a heading `config` in
the `docs.md`, but that heading is actually `Configuration`.
Therefore this rule will produce an error to caputre this, because
`#config` does not match the heading `configuration`.

### Correct Scenarios

This rule does not trigger when an anchor link has a matching heading in a
markdown file.

```
scanned folder
 | docs.md
 \ readme.md
```

```Markdown
# readme.md

See the [documentation](docs#basic-configuration) for basic configuration
options.
```

```Markdown
# docs.md

## Basic Configuration 

Here are the basic config options.
```

In this case the `readme.md` file has an anchor link `basic-configuration` in
the `docs.md`. The heading in `docs.md` after kebab case conversion is
`basic-configuration`, which matches the anchor link.

It is also possible to lint to local headings.

```Markdown
# Documentation

* [Chapter 1](#chapter-1)

## Chapter 1

Some text ...
```

## Configuration

| Prefixes                 |
|--------------------------|
| `plugins.md049.`         |
| `plugins.validate-refs.` |

| Value Name | Type      | Default | Description                                             |
|------------|-----------|---------|---------------------------------------------------------|
| `enabled`  | `boolean` | `False` | Whether the plugin rule is enabled.                     |
| `regex`    | `string`  |         | Regex to exclude (whitlist) some links from validation. |
