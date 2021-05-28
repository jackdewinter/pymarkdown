# Advanced Rule Plugins

The information contained in this document provides
documentation on how to find information about the
currently loaded rule plugins.

## Listing Rule Plugin Information

For information on what rule plugins are currently present, the following
command is used:

```shell
pymarkdown plugins list
```

This command lists all the rules in a table using the following format:

`rule-id aliases enabled-default enabled-current version`

- `rule-id` - Unique identifier assigned to the rule.
- `aliases` - One or more aliases used to reference the rule.
- `enabled-default` - Whether the rule is enabled by default.
- `enabled-current` - Whether the rule is currently enabled.
- `version` - Version associated with the rule.  If the rule is a project
  rule, this version will always be the version of the project.

In addition, the `list` command may be followed by text that
specifies a Glob pattern used to match against the rule plugins.
For example, with the default configuration, using the command
`plugins list md00?` produces this output:

```text
ID     NAMES                    ENABLED (DEFAULT)  ENABLED (CURRENT)  VERSION

md047  first-heading-h1, first  False              False              0.5.0
       -header-h1
```

If more verbose information is needed on a given rule plugin, the
`plugins info` command can be used with the `rule-id` for the
rule plugin or one of the `aliases` used to refer to the rule plugin.
If provided with a `rule-id` of `md047` or an alias of `single-trailing-newline`,
this command produces the following output:

```text
Id:md047
Name(s):single-trailing-newline
Description:Each file should end with a single newline character.
```

- Note that better support for this command is priortized as
  required for the general release and should happen fairly quickly.
