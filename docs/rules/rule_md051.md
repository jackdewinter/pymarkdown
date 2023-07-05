# Rule - MD051

| Aliases                                |
|----------------------------------------|
| `md051`                                |
| `unused-assets` |

## Summary

This rule searches for assets within a specified folder that are not referenced in any scanned Markdown file.

## Reasoning

### Clean up old assets

Over time, the asset folder tends to accumulate files, making it difficult to determine which ones are still in use and which ones have become obsolete. This lack of clarity can hinder the maintainability of the project. By implementing this rule, you can effectively identify and remove unused files, ensuring a more organized and manageable asset collection. By regularly cleaning up outdated assets, you improve the overall maintainability of the project and reduce potential confusion for developers and contributors.

## Examples

### Failure Scenarios

This rule triggers when an asset is not referenced in any markdown file and matces the configured regex:

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

### Correct Scenarios

This rule does not trigger when the asset is referenced in a scanned markdown file.

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


## Configuration

| Prefixes                 |
|--------------------------|
| `plugins.md051.`         |
| `plugins.unused-assets.` |

| Value Name    | Type      | Default                      | Description                                                          |
|---------------|-----------|------------------------------|----------------------------------------------------------------------|
| `enabled`     | `boolean` | `True`                       | Whether the plugin rule is enabled.                                  |
| `assetsregex` | `string`  | `.*\.(jpg\|jpeg\|png\|gif)$` | Regex to match which assets should trigger this rule                 |
| `assetsglob`  | `string`  | `**/assets/**/*`             | Filesystem glob to configure the asset folder that should be scanned |

