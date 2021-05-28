# Advanced Configuration

The information contained in this document provides
documentation on how to set configuration values for the
PyMarkdown project as well as what the list of available
configuration values are.

## Setting Configuration Properties

Outside of the Markdown files themselves, the next most
important thing is the configuration properties.  These
configuration properties alter how those Markdown files
are parsed and how the PyMarkdown interprets the rules
it applies to the Markdown files.

## Configuration Property Ordering

The configuration for this project follows a consistent theme when
deciding what configuration applies to a given item.  Specifically,
the order of precedence for interpreting configuration properties is:
command line setting, configuration value setting, and
finally default setting.

The special case for this ordering is the disabling
and the enabling of rules from the command line using the `-d` and
`---disable-rules` flags along with the `-e` and `--enable-rules`
flags.  For these special cases, the command line setting is
further defined to state that disabling a rule takes priority
over enabling a rule.  While it is highly unlikely that someone
will specify both actions at the same time, we felt it was
important to specify the order to eliminate any possible confusion.

### Command Line Settings

Command line settings are any setting that is visible from the
command line using `--help` except for the `--config`/`-c`
command and the `--set`/`-s` command covered below.  When used,
these commands offer the final say on what the value of a given
configuration value is.  In essence, the command line provides
the final say on how the application behaves.

The list of general command line settings is as follows:

- `--add-plugin`
- `--strict-config`
- `--stack-trace`
- `--log-level {CRITICAL, ERROR, WARNING, INFO, DEBUG}`
- `--log-file LOG_FILE`

Both the `scan` and the `plugins` commands have modifiers that
change how they behave.  However, these are modifiers to the
commands themselves and are only available as a command line
setting:

- `scan`
  - `-l`/`--list-files`
  - `-r`/`--recurse`
- `plugins`
  - `list`
    - `--all`

### Configuration File Settings

While the command line is a useful way to set many configuration
values, most people find a useful collection of settings that
they want to use and embed those settings within a configuration
file.  Alternatively, there are times where you may want to
test a change to that configuration file before committing it
to the file.  Both methods are covered in this section.

#### Hierarchical and Flattened Properties

When relaying information about a configuration property,
that property is most often conveyed in a hierarchical
and flattened format.  For
example, when referring to the setting of the logging level,
the property key of `log.level` is used.  This specifies that
within the hierarchy of `log` is a property called `level`.
Furthermore, it allows keys like `log.file` to denote that
both the `log.file` property and the `log.level` are in the
same hierarchy.

#### Specifying A Configuration File

Specified at the command line, the `--config` or `-c` setting
is followed by the name of a configuration file to load and use
to set any configuration values.  While there is only support
for a configuration file with a JSON format for the initial
release, support for multiple formats is planned for after
the initial release.

##### JSON Format

For the initial release, the configuration file must be
specified in a JSON format.  The primary reason that the
JSON format was selected was due to the provision of
distinct types of objects that may be specified: strings,
numbers, booleans, lists, and dictionaries/maps.

Using the example of the `log.file` property and the
`log.level` property from above, those can be set
with this configuration:

```json
{
    "log" : {
        "file": "log.txt",
        "level": "INFO"
    }
}
```

By placing that configuration in a file called `pymarkdown.cfg`
(or any other filename for that matter), that file can then
be specified to the linter as:

```sh
pymarkdown -c pymarkdown.cfg scan examples
```

Executing that command, you should see the usual output from
the command line:

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

#### Specifying A Single Configuration Value

There are times that specifying a single configuration
value is useful.  For me, those times are usually when I am testing
the setting of a configuration property or when I just need to set a single
value while scanning a directory.  That is where the `--set` or
`-s` command line option helps.

For example, when I was testing the configuration for the above log configuration,
I used the following command line to verify that the settings
were correct:

```sh
pymarkdown --stack-trace -s log.level=INFO -s log.file=log.txt scan examples
```

#### Specifying Configuration Types

To provide a more robust system of configuration, the configuration
system uses values that are typed as much as possible.  This extra
level of specification allows more confidence that the value that
is provided for that property is interpreted properly.  Note that
if you are using a configuration file format that already provides
type information, such as the JSON format, this extra information
may not be required.

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
case of the `--set` command line argument, the `ValueError` will be surfaced
to the command line and the application will stop.  If provided as
part of a configuration format that does not provide typing, the
`ValueError` will usually result in the default value being used for
that configuration property.

#### Specifying Strict Configuration Mode

During the development of the linter, there were specific times that
I wanted to be sure that the configuration values that I specified
were exactly as I specified them.  As I started doing exploratory
testing of the PyMarkdown project, I also realized that I am
enough of a stickler to want to ensure that any configuration
properties that I assign are correct and that those values are
not reverting to default values.

Specified from the command line using the `--strict-config` flag or
through the configuration as `mode.strict-config=$!True`, this
option turns on the strict mode for the configuration system.
Once enabled, when the application reads values from the configuration,
it will stop the application if:

- a value was provided for the configuration value, but it was the wrong type
- a value was provided for the configuration value, but it does not match
  a specified filter for that value

Using the `log.level` example from above, the value is specifically specified
as being one of the following values: `CRITICAL`, `ERROR`, `WARNING`, `INFO`,
or `DEBUG`.  There both an integer value of `1` and a string value of
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

### Plugins

These affect the collection of rule plugins and whether they are called.

| Key | Command Line | Type | Description |
| -- | -- | -- |-- |
| -- | --enable-rules   | string    | Comma separated list of rules to enable. |
| -- | --disable-rules  | string    | Comma separated list of rules to disable. |
| -- | --add-plugin     | string    | Path to a plugin containing a new rule to apply. |

### Other

| Key | Command Line | Type | Description |
| -- | -- | -- |-- |
| -- | --stack-trace | boolean | if an error occurs, print out the stack trace for debug purposes.  Also sets the initial logging (config processing) to debug. (Default: `false`) |

### Extensions Section

#### Front Matter

These affect how front matter is interpreted for the parser.

| Key | Command Line | Type | Description |
| -- | -- | -- |-- |
| `extensions.front-matter.enabled` | - | Boolean | Enable the parser to recognize front-matter. |

For more information on Markdown Front-Matter, see [this document](/docs/extensions/front-matter.md).

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

#### Handling Multiple Identifiers

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
