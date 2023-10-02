# Rule - MD051

| Aliases         |
|-----------------|
| `md051`         |
| `unused-assets` |

## Summary

This rule searches for assets within a specified folder that are not referenced
in any scanned Markdown file. The goal is to find orphan files that are no
longer needed and are cluttering the documentation directory.

## Reasoning

### Clean up old assets

Over time, the asset folder tends to accumulate files, making it difficult to
determine which ones are still in use and which ones have become obsolete. This
lack of clarity can hinder the maintainability of the project. By implementing
this rule, you can effectively identify and remove unused files, ensuring a more
organized and manageable asset collection. Regularly cleaning up outdated assets
improves the overall maintainability of the project and reduces potential
confusion for developers and contributors.

## How it works

At the start of the process, the rule examines each Markdown file, searching for
references to files and images based on the linter's classifications. This
initial scan is conducted across all Markdown files, forming a comprehensive
list of references for future comparison.

Once the scanning of Markdown files is complete, the rule shifts its focus to
the filesystem. It identifies all files that match the `assetsglob` pattern and
further narrows down the selection by checking against the `assetsregex` pattern
(as detailed in the Configuration section). The paths of the matching files are
gathered in a separate set. Base for all paths are the current working directory
of the pymarkdown process.

Subsequently, this set of existing files is compared against the previously
collected set of referenced files. Any files that exist but are not present in
the set of referenced files are identified as errors and reported by the linter.

## Examples

### Failure Scenarios

This rule triggers when an asset is not referenced in any markdown file and
matches the configured regex.

```
scanned folder
 |-assets
 |  \ unused.png
 \ readme.md
```

```Markdown
# This is a Readme.

Some text.
```

In this case, the set of referenced files is empty, but the set of files on the
filesystem contains `assets/unused.png`, because it matches the default
`assetsregex` and `assetsglob` (see [Configuration](#configuration)). The rule
will log an error for this file.

### Correct Scenarios

This rule does not trigger when the asset is referenced in a scanned markdown
file.

```
scanned folder
 |-assets
 |  \ used.png
 \ readme.md
```

```Markdown
# This is a Readme.

Some text.

![Image](assets/used.png)
```

In this case no error is produced, because the file `assets/used.png` is
referenced in the `readme.md` file on the last line.

## Configuration

| Prefixes                 |
|--------------------------|
| `plugins.md051.`         |
| `plugins.unused-assets.` |

| Value Name    | Type      | Default                      | Description                                                          |
|---------------|-----------|------------------------------|----------------------------------------------------------------------|
| `enabled`     | `boolean` | `False`                      | Whether the plugin rule is enabled.                                  |
| `assetsregex` | `string`  | `.*\.(jpg\|jpeg\|png\|gif)$` | Regex to match which assets should trigger this rule                 |
| `assetsglob`  | `string`  | `**/assets/**/*`             | Filesystem glob to configure the asset folder that should be scanned |
