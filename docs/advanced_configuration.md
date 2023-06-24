# Advanced Configuration

The information contained in this document provides documentation on how to set
configuration values for the PyMarkdown project.

## Setting Configuration Properties

Outside of the Markdown files themselves, the next most important concept when
using this project are the configuration properties.  These configuration properties
alter how those Markdown files are parsed and how PyMarkdown interprets the rules
it applies to those Markdown files.

## Configuration Property Ordering

The configuration for this project follows a consistent theme when deciding what
configuration applies to a given item.  This theme is that the order of precedence
for interpreting configuration properties goes from the most specific provided configuration
value to the least specific provided configuration value.  In order, this is:

- general command line settings (`--add-plugin`, `--log-file`, etc.)
- specific command line setting (`-s log.level=INFO`, etc.)
- command line configuration file (`--config myconfig.json`)
- default configuration file (loading default `.pymarkdown` JSON file)
- alternate project configuration files (`tool.pymarkdown` section of `pyproject.toml` file)
- default value

### General Command Line Settings

General command line settings are any settings visible from the command line
using the `--help` argument, except for the for the `--config`/`-c` argument and
the `--set`/`-s` argument covered below. Currently, the list of those arguments
is:

- `-e`/`--enable-rules` and `-d`/`--disable-rules`
- `--add-plugin`
- `--strict-config`
- `--stack-trace`
- `--log-level {CRITICAL, ERROR, WARNING, INFO, DEBUG}`
- `--log-file LOG_FILE`

When used, these arguments offer the final say on the value assigned to a given
configuration property.  In the case where a general command line setting accepts
only one value, such as `--log-level` and `log-file`, the last entry on the command
line has precedence.  That is to say that a command line including
`--log-level INFO --log-level DEBUG` will result in the log level property being
set to `DEBUG`, as it appears last in the command line.

#### One Exception: Enabling/Disabling Rules From The Command Line

The core reasoning for this exception is to allow for clear and definitive user
control over PyMarkdown's behavior for its most common use: scanning Markdown files
with rules. As a user, if you decide that a given rule should be disabled or enabled
regardless of any configuration files, these settings will enforce that decision
for you.

The one deviation from the previously stated Configuration Property Ordering is
the disabling and enabling of rules from a command line setting using the `-d` and
`--disable-rules` arguments and the
`-e` and `--enable-rules` arguments.  Each of these arguments can be specified multiple
times, each appearance adding another value to an internal list. Unlike
the other settings, the precedence of these settings is only determined after all
other settings for the enabling or disabling of rules have been collected.  At
that time, any disabled rules from the command line have highest precedence, followed
by any enabled rules from the command line.  Once that precedence has been resolved,
the normal rule for precedence takes effect for any enabling or disabling of rules
through configuration properties.

To provide a concrete example, while a command line of:

```bash
pymarkdown -e Md041 -d Md041 scan .
```

seems unlikely, our team tested this according to the above rules to ensure that
there is predictable, consistent behavior.  Therefore, we are confident that the
example line above evaluates the same as if it was written as:

```bash
pymarkdown -d Md041 -e Md041 scan .
```

Furthermore, either of these two settings on their own will override any enabling
or disabling of the rules provided through any method of setting configuration
properties detailed below.

From experience, we find that our most common usage of these settings is to override
individual rules on a case-by-case basis while cleaning up a batch of rule failures.
In that scenario, one specific rule is selected, disabling all other rules while the
failures for that one rule are dealt with. We then remove the disable setting for
one of the rules, and fix those failures, repeating the process as necessary.
For small lists of failures, this is overkill, but we have found it to be a very
efficient way of handling large number of failures. There are probably other good
uses for these settings, but that is how our development team uses it!

Seeing how users leverage PyMarkdown in their projects, this feature is also used
if the user only desires to enable or disable one or two rules and is using a script
or [pre-commit](./pre-commit.md).  From what our users have shared with us, pre-commit
`.pre-commit-config.yaml` files like this are common:

```yaml
repos:
  - repo: https://github.com/jackdewinter/pymarkdown
    rev: v0.9.9
    hooks:
      - id: pymarkdown
        pass_filenames: false
        args: [ "-d", "Md041,Md042", "scan", "./docs" ]
```

In the example above, an often overlooked feature of these two arguments is used:
both enable and disable rule arguments accept a comma-separated list of rules.
Using this feature allows for more compressed lists of rule to enable or disable.
Once again, based on user feedback, once the user's own threshold for "too many
arguments" is reached, that user will then embed those enable arguments and disable
arguments into a [Command Line Configuration File](./advanced_configuration.md#command-line-configuration-file).

#### Subcommand Settings

PyMarkdown provides subcommands on the command line to provide directions on how
the user intends PyMarkdown to help them with their task.  These subcommands may
have arguments that modify the behavior of the subcommand.  As those arguments are
specific to a given subcommand, they are only offered as an argument for that subcommand.
For example, the argument of `--all` on the command line for the `plugin` subcommand:

```bash
pymarkdown plugins list --all
```

is modifying the `plugins` subcommand's specific behavior.  As such, it is not
available as a specific command line settings or a property value that can be
provided in a configuration file.

### Specific Command Line Setting

After the general command line settings, the specific command line settings have
the highest precedence.  These settings use the `-s` or `--set` arguments and
specify a single configuration property.  The specific property is identified using
a [flattened format](./advanced_configuration.md#flattened-hierarchical-property-names)
and an optional [configuration type](./advanced_configuration.md#specifying-configuration-property-types)
for the property value. If no configuration type is provided, the property uses
a default type of `string`.
These two concepts work together to provide for a condensed way to specify configuration properties.

For the PyMarkdown development team, these arguments have proven to be useful in
providing shorthand for setting properties that are isolated and near the top
of the configuration property precedence list.  Because of the high precedence, those
settings are less likely to be overridden.  As an example, a common command line that
we use to display enhanced logging output is:

```bash
pymarkdown --stack-trace -s log.level=INFO scan examples
```

This pattern is often a good first step at trying out configuration settings before
moving those configuration settings into a configuration file.  While it is correct
that the command line:

```bash
pymarkdown -s log.stack-trace=$!True --log-level INFO scan examples
```

is functionally equivalent to the above command line, for some reason the above
command line just rolls off our fingers better.  Due to the flexible ways that PyMarkdown
allows configuration to be specified, we can pick the form of the command line that
works best for us.

### Command Line Configuration File

While the command line is a useful way to set many configuration values, most users
find a useful collection of settings that they want to use often.  Instead of setting
each of those settings individually, users often choose to embed those settings
within a configuration file. This practice allows those configuration values to
be reused with a minimum of effort.

The `-c` or `--config` argument is used to specify a configuration file that contains
zero or more configuration settings to apply.  That argument is followed by the
name of a file that contains those configuration settings in a JSON format. The
specifics of that format are detailed more thoroughly in the [JSON Format](./advanced_configuration.md#json-format)
section. As that file format meets PyMarkdown's requirements for clear item typing
and a hierarchical format, there are no plans to support any other file types for
the primary configuration file.

As an example, the enhanced logging output snippet from the
[Specific Command Line Setting](#specific-command-line-setting) section can be
expressed in JSON format as:

```json
{
  "log": {
    "level": "INFO",
    "stack-trace" : true
  }
}
```

### Default Configuration File

As an alternative to a specified configuration file, there are times where there
is a need to tie a configuration file to a directory hierarchy. To support those
needs, when PyMarkdown starts up, it looks for a configuration file named
`.pymarkdown` in the current directory.  If that file is present, PyMarkdown
tries to load that file as if it was specified with the `-c` or `--config` arguments.

Note that because of precedence, a configuration file specified with the `-c` or
`--config` arguments will always override the values provided in a `.pymarkdown`
file.  To be very clear, if a configuration setting is provided in the default
configuration file and not overridden in a command line configuration file, it
remains active.  This pattern is very useful in setting general configuration
settings for the directory structure in the default configuration file, with
more focused settings being supplied through specific command line settings or
a command line configuration file.

Care should be taken in the application of the default configuration file.  As
mentioned above, the current directory is determined when PyMarkdown starts, not
when a given Markdown file is scanned.  If multiple default configuration files
are nested within a given directory structure, some manner of scripting will be
necessary to properly apply the right default configuration file to its corresponding
directory structure.

### Alternate Project Configuration Files

For anyone that has continued to read this far down in the hierarchy of configuration,
there is more!  If there is a `pyproject.toml` file in the current directory that
contains a `tool.pymarkdown` section, those values will be used for configuration.
The [TOML file format](https://docs.fileformat.com/programming/toml/) is easy to
use, and is provided as an alternative to the JSON format of the `.pymarkdown`
configuration file.

Note that any items contained within the section must use a key that is expressed
using a full
[flattened format](./advanced_configuration.md#flattened-hierarchical-property-names).
As TOML files provides typing information for the values, care must be taken to
associate the right type with the right value.

As an example, the enhanced logging output snippet from the
[Specific Command Line Setting](#specific-command-line-setting) section can be
expressed in TOML format as:

```toml
[tool.pymarkdown]
log.level = "INFO"
log.stack-trace = true
```

### Default Value

At the bottom of the precedence list is the default value for a configuration
property.  Most internal PyMarkdown calls to get a property value provide a default
value to use if no value was supplied.  These values are the ultimate fallback
values, expected to provide the most common usage experience to the user.

For plugins, this allows a handful of plugins to be disabled by default, as their
usage is either not common or outdated.  For extensions, it allows for extensions
to be added in such a way that they do not affect current behaviors.

## Further Configuration Property Topics

Here are some other topics that are useful when talking about configuration
properties.

### JSON Format

The configuration file is specified in a bare JSON format.  The primary reason
that the JSON format was selected was due to the provision of distinct types of
objects that may be specified: strings, numbers, booleans, lists, and dictionaries/maps.

Using the example of the `log.file` property and the `log.level` property from
above, those properties can be set with this configuration:

```json
{
    "log" : {
        "file": "log.txt",
        "level": "INFO"
    }
}
```

By placing that configuration in a file called `pymarkdown.cfg` (or any other filename
for that matter), that file can then be specified to the linter as:

```sh
pymarkdown -c pymarkdown.cfg scan examples
```

Executing that command, you should see the usual output from the command line:

```text
examples/example-1.md:3:16: MD047: Each file should end with a single newline character. (single-trailing-newline)
```

but you should also see a new file in the project directory called
`log.txt` that starts with the text:

```text
Determining files to scan.
Determining files to scan for path 'examples'.
Number of files found: 2
Scanning file 'examples/example-1.md'.
Scanning file 'examples/example-1.md' token-by-token.
coalesced_results
```

### Flattened-Hierarchical Property Names

When relaying information about a configuration property, that information is most
often conveyed using a hierarchical and flattened format.  For example, when referring
to the setting of the logging level, the property key of `log.level` is used.  This
specifies that within the hierarchy of `log` is a property called `level`. Furthermore,
it allows keys like `log.file` to denote that both the `log.file` property and the `log.level`
are in the same hierarchy.

Currently, this property key format is only used by PyMarkdown itself when specifying
configuration properties from the command line as a
[command line setting](./advanced_configuration.md#specific-command-line-setting).
However, it is very useful in communicating values to users due to its condensed
format.  For example, most rules specify a [prefix](./rules/rule_md001.md#configuration)
section that creates a proper flattened property name when combined with the
`value name` in the tables below the prefix section.

Basically, it is more concise to talk about setting the configuration property
`plugins.heading-increment.enabled` to `True` than it is to talk about:

```json
{
    "plugins" : {
        "heading-increment": {
          "enabled": true
        }
    }
}
```

### Specifying Configuration Property Types

To provide a more robust system of configuration, the configuration
system uses values that are typed as much as possible.  This extra
level of specification allows more confidence that the value that
is provided for that property is interpreted properly.  Note that
if you are using a configuration file format that already provides
type information, such as the JSON format, this extra information
is not required.

The type specification is performed using a prefix for the property value.
Assuming that the `*` character refers to any character, the following
table specifies the type behavior:

| Prefix | Type | Examples |
| --- | --- | --- |
| `*` or None | Default (String) | `abc` |
| `$*` (except for characters below) | Default (string) | `$abc` |
| `$$` | String | `$$abc` |
| `$#` | Integer | `$#1`, `$#-12345` |
| `$!` | Boolean | `$!True`, `$!anything-else-is-false` |

The only two interpretations that require further explanation are
the integer and the boolean types.  The integer type attempts to
translate any characters past the prefix as a signed integer.  The
boolean type compares any characters past the prefix in a case-insensitive
manner against the sequence `true`, setting the value to `True` if
that comparison is true.

For the integer translation, if the value `$#1.1` is provided, the
behavior afterwards depends on how that value is referenced.  In the
case of the `--set` command line argument, the `ValueError` will surface
to the command line and the application will stop.  If provided as
part of a configuration format that does not provide typing, the
`ValueError` will usually result in the default value being used for
that configuration property.

Some examples of this are:

- specify that all ordered lists must begin with the string `0` instead of
  the string `1`

  ```text
  pymarkdown --set plugins.md029.style=zero scan test.md
  ```

  OR

  ```text
  pymarkdown --set plugins.md029.style=$zero scan test.md
  ```

  OR

  ```text
  pymarkdown --set plugins.md029.style=$$zero scan test.md
  ```

- enabling the extension to interpret front matter (boolean value)

  ```text
  pymarkdown --set extensions.front-matter.enabled=$!True scan test.md
  ```

- setting the allowed line length to `10` (integer value)

  ```text
  pymarkdown -s plugins.md013.heading_line_length=$#10 scan test.md
  ```

### Specifying Strict Configuration Mode

During the development of the linter, there were specific times that we wanted
to be sure that the configuration values that we specified were exactly as we specified
them.  As we started doing exploratory testing of the PyMarkdown project, we also
realized that we are sticklers that want to ensure that any configuration properties
that we assign are correct and that those values are not reverting to default values.

Specified from the command line using the `--strict-config` flag (or
through the configuration as `mode.strict-config=$!True`), this
option turns on the strict mode for the configuration system.
Once enabled, when the application reads values from the configuration,
it will stop the application if:

- a value was provided for the configuration value, but it was the wrong type
- a value was provided for the configuration value, but it does not match
  a specified filter for that value

Using the `log.level` example from above, the value is specifically required
to be one of the following values: `CRITICAL`, `ERROR`, `WARNING`, `INFO`,
or `DEBUG`.  Therefore, both an integer value of `1` and a string value of
`information` would fail for different reasons.  Normally, these would
cause the configuration system to silently fail and not set the specified
value. As a result of that, the default value for that configuration
value will be used with no warning being issued.

However, with the strict configuration mode enabled, the following command
line:

```sh
pymarkdown --strict-config -s log.level=$#1 scan examples
```

produces the following output:

```text
Configuration Error: The value for property 'log.level' must be of type 'str'.
```

and the following command line:

```sh
pymarkdown --strict-config -s log.level=information scan examples
```

produces the following output:

```text
Configuration Error: The value for property 'log.level' is not valid: Value 'information' is not a valid log level.
```

This feature is more burdensome on the user, but it is provided as an option for
those users who want to make sure their provided configuration values are used
properly.

### Handling Multiple Identifiers For The Same Rule

A rule plugin can have two or more identifiers, one id plus
multiple aliases. If multiple identifiers belonging to a
single plugin rule are used for separate configuration
hierarchies, there must be a predictable ordering used
to resolve which hierarchy is used.  In order, the rule
plugin's id comes first, followed by each alias in the
order that they are entered in the plugin rule itself.
This rule applies to the group of configuration values
as a group.

For example, suppose there is a configuration file with
the contents of:

```json
{
"plugins" : {
    "heading-style-h1" : { 
        "enabled" : true,
        "style" : "consistent"
    },
    "md003" : { 
        "enabled" : false
    }
}
```

According to the documentation on [Rule md003](/docs/rules/rule_md003.md),
the id for that rule is `md003` and it has one alias `heading-style-h1`.
This means that the `plugins.md003` configuration takes
precedence over the `plugins.heading-style-h1` configuration,
due to the rules specified above, regardless of its position in
the configuration file. Also, assuming that
the `"enabled" : false` configuration value was `"enabled" : true`
instead, even though the `plugins.heading-style-h1.style`
configuration value is set, it will not be used.  For that
configuration value to be used, the `plugins.md003` configuration
hierarchy must be removed completely as the entire hierarchy
has precedence, not just individual configuration properties.

## Available Configuration Values

### Configuration

These directly affect the collection of configuration values and how they are interpreted.

| Key | Command Line | Type | Description |
| -- | -- | -- |-- |
| --                    | --config {file}           | string    | Path to the configuration file to use. |
| --                    | --set {key}={value}       | string    | Manually set an individual configuration property. |
| mode.strict-config    | --strict-config           | boolean   | Throw an error if the configuration is bad, instead of assuming default values. (Default: `false`) |

### Logs

These affect the logging for the application.

| Key | Command Line | Type | Description |
| -- | -- | -- |-- |
| log.file          | --log-file        | string  | Destination file for log messages. |
| log.level         | --log-level       | string* | Minimum level required to log messages. Valid values are: `CRITICAL`, `ERROR`, `WARNING`, `INFO`, or `DEBUG`. (Default: `WARNING`)  |
| log.stack-trace | --stack-trace | boolean | if an error occurs, print out the stack trace for debug purposes.  Also sets the initial logging (config processing) to debug. (Default: `false`) |

These configuration values affect how the application logs information.  The two
easiest to explain are the `*file` and `*level` values.  These configuration values
specify what the log level is for the application and whether to redirect any logged
information away from the standard output (stdout) to the specified log file.

The `log.stack-trace` configuration value and the `--stack-trace` command line flag are
a bit more nuanced in their behavior.  Due to implementation reasons, the configuration
value form of the flag can only be accessed once the logging system has been initialized,
that is after the configuration file has been loaded and a possible
[strict configuration mode](#Specifying Strict Configuration Mode) has been
enacted.
Generally speaking, this flag enables the application to provide additional information
on why a critical error occurred.  As the name of the value suggests, the reporting of a
critical error occurring will include a Python stack trace if this flag is set.  While
this information will be confusing to the typical user of the application, that information
is vital to help diagnose critical errors.

This behavior gets nuanced when there is a need to obtain a stack trace to debug
an issue with the small amount of Python code that exists before the logging system
is initialized.  In this case, the `--stack-trace` command line option will work
to obtain that stack trace as documented.  But, since the logging system that
includes the combined stack trace function has not yet been initialized, the
`log.stack-trace` configuration value will not be effective.

### Plugins

These affect the collection of rule plugins and whether they are called.

| Key | Command Line | Type | Description |
| -- | -- | -- |-- |
| *special* | --enable-rules,-e   | string    | Comma separated list of rules to enable. |
| *special* | --disable-rules,-d  | string    | Comma separated list of rules to disable. |
| plugins.additional_paths | --add-plugin     | string    | Path to a plugin containing a new rule to apply. |

Enabling and disabling of plugins can be accomplished in two ways.  From the
command line, the `--enable-rules` and `--disable-rules` arguments allow for a comma-separated
set of rule identifiers to be specified in the next argument.  If a configuration file option
is required, the plugin rule can be enabled as specified in the [Plugins Section](#plugins-section) below.

Additional rule plugins can be added to the configuration in one of two ways.  To test new rule plugins,
the recommended way to add a rule plugin is to use the `--add-plugin` command line argument or more times.
Each `--add-plugin` argument is followed by another argument that specifies a file or a directory to load
any new plugins from.  For a more permanent solution, the `plugins.additional_paths` configuration value
can be used in a similar manner, specifying one or more paths using a comma-separated string containing
the paths.

### Extensions Section

#### Front Matter

This configuration affects how document front matter is interpreted for the parser.

| Key | Command Line | Type | Description |
| -- | -- | -- |-- |
| `extensions.front-matter.enabled` | - | Boolean | Enable the parser to recognize front-matter. |

For more information on Markdown Front-Matter, see [this document](/docs/extensions/front-matter.md).

#### Pragmas

This configuration affects whether HTML-style comments can be interpreted as linter commands.

| Key | Command Line | Type | Description |
| -- | -- | -- |-- |
| `extensions.linter-pragmas.enabled` | - | Boolean | Enable the parser to recognize pragmas. |

For more information on PyMarkdown Pragmas, see [this document](/docs/extensions/pragmas.md).

### Plugins Section

| Key | Command Line | Type | Description |
| -- | -- | -- |-- |
| `plugins.{id}.enabled` | --enable-rules, --disable-rules | Boolean | Enable the rule. |
| `plugins.{id}.other` | - | Various | Specify other configuration properties specific to the rule. |

The list of configuration values for rule plugins is slightly
different than the configuration for the rest of the system.
For each rule plugin, there is a main boolean configuration
value, in the form `plugins.{id}.enabled`, that specifies the rule
plugin's enabled state.  In that string, the sequence `{id}`
can be any one of the valid identifiers for a plugin rule.

Once enabled, each rule plugin is responsible for its own
properties located under the hierarchy of `plugins.{id}.`.
The list of configuration values available for each standard
plugin rule is given in the `Configuration` section for
each [standard rule plugin](/docs/rules.md).
