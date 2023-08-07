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
With this rule, you can automatically validate the references to various parts of the documentation,
such as links and images.

This helps to ensure the correctness and integrity of the documentation by identifying and flagging any invalid or
broken references.

## How it works

This rule validates all references in the scanned Markdown files checking the existence of the referenced image or
heading.

### Local Images and Files

When the linter classifies a token as an image the rule uses `os.path.exists` to check if that file exists in
the filesystem. If it does *not* exist it reports a linter error for that dangling reference.

### Anchors and Headings

This validation is a bit more involved, because it requires knowledge of all headings in all Markdown documents. But
a linter only scans each file once. This means, the rule might be validating a reference to a file that has not been
scanned and, therefore, its headings aren't known, yet. To work around this limitation, anchors are stored in a global
map grouping them by file. When an anchor (link to a heading) is validated, the rule checks to see if the file exists.
If the file exists and the global map has already been process and contains anchors for that file, all headings are 
compared to the anchor link in question using the kebab case rule for anchors. If none of the headings match the anchor,
an error is reported.

If the map does not contain any headings for the referenced file, the anchor link is stored in a global map of anchor
links grouped by referenced file. When the linter eventually scans the referenced file, all headings are processed as
before and now all stored anchors links for this file are validated.

When all markdown files have been scanned, all anchor links have been either validated or reported as errors. Either at
the moment of their initial scanning, or at the moment when their referenced file + heading was scanned.

## Examples

### Failure Scenarios

This rule triggers when an anchor link has no matching heading in any markdown file.

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

In this case the `readme.md` file has an anchor link to a heading `config` in the `docs.md`, but that heading is 
actually `Configuration`. This fails because `config` is not `configuration`.

### Correct Scenarios

This rule does not trigger when an anchor link has a matching heading in a markdown file.

```
scanned folder
 | docs.md
 \ readme.md
```

```Markdown
# readme.md

See the [documentation](docs#basic-configuration) for basic configuration options.
```

```Markdown
# docs.md

## Basic Configuration 

Here are the basic config options.
```

In this case the `readme.md` file has an anchor link `basic-configuration` in the `docs.md`. The heading in `docs.md`
after kebab case conversion is `basic-configuration`, which matches the anchor link.

## Configuration

| Prefixes                 |
|--------------------------|
| `plugins.md049.`         |
| `plugins.validate-refs.` |

| Value Name    | Type      | Default                      | Description                                                          |
|---------------|-----------|------------------------------|----------------------------------------------------------------------|
| `enabled`     | `boolean` | `False`                      | Whether the plugin rule is enabled.                                  |
