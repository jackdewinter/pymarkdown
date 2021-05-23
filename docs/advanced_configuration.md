# Advanced Configuration

[more]
[add sections in main document]

## Setting Configuration Values

The configuration for this project follows a consistent theme when
deciding what configuration appplies to a given item.  Sepcifically,
the order is command line setting, configuration setting, and
default setting.  The special case for this ordering is the disabling
and enabling rules from the command line using the `-d` and
`---disable-rules` flags along with the `-e` and `--enable-rules`
flags.  For this special case, the command line setting is
further defined as disabling a rule takes priority over enabling
a rule.  While it is highly unlikely that someone will specify
both actions at the same time, we felt it was important to specify
the order to eliminate any possible confusion.

### Command Line Settings

Command line settings are any setting that is visible from the
command line using `--help` with the exception of the `--config`/`-c`
command and the `--set`/`-s` command covered below.  When used,
these commands offer the final say on how the application will
behave.

This list may change, but the current list of command line
settings are:

- `--add-plugin`
- `--strict-config`
- `--stack-trace`
- `--log-level {CRITICAL,ERROR,WARNING,INFO,DEBUG}`
- `--log-file LOG_FILE`

Both the `scan` and the `plugins` commands have modifiers that
change how they behave.  However, these are modifiers to the
commands themselves and are only available as a command line
setting:

- `scan`
  - `-l`/`--list-files`
- `plugins`
  - `list`
    - `--all`

### Configuration Settings

While the command line is a useful way to set many configuration
values, most people find a solid collection of settings that
they want to use and embed those settings within a configuration
file.  Alternatively, there are times where you may want to
test a change to that configuration file before commiting it
to the file.  Both of these methods are covered in this section.

#### Hierarchical and Flattened Properties

When realying a configuration property, that property is usually
conveyed in both a hierarchical and flattened format.  For
example, when referring to the setting of the logging level,
the propery key of `log.level` is used.  This specifies that
within the hierarchy of `log` is a property called `level`.
Furthermore, it allows keys like `log.file` to denote that
both the `log.file` property and the `log.level` are in the
same hierarchy.

values?

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
`log.level` property from above, these value would be
set using this configuration:

```json
{
    "log" : {
        "file": "log.txt",
        "level": "INFO"
    }
}
```

Placing that configuration in a file called `pymarkdown.cfg`
(or any other filename for that matter), that file can then
be specified to the linter as:

```sh
python main.py -c pymarkdown.cfg scan examples
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

There are specific times that specifying a single configuration
value is useful.  For me, those times are usually when I am testing
a new configuration setting or when I just need to set a single
value while scanning a directory.  That is where the `--set` or
`-s` command line option helps.

When I was testing the configuration for the above log configuration,
I used the following command line to verify that the settings
were correct:

```sh
python main.py --stack-trace -s log.level=INFO -s log.file=log.txt scan examples
```

#### Specifying Configuration Types

To provide a more robust system of configuration, the configuration
system uses values that are typed as much as possible.  This extra
level of specification allows more confidence that the value that
is provided for that property is interpretted properly.  Note that
if you are using a configuration file format that already provides
type information, such as the JSON format, this extra information
is not required.

This specification is performed using a prefix for the property value.
Assuming that the `*` character refers to any character, the following
table specifies the type behavior:

| Prefix | Type | Examples |
| --- | --- | --- |
| `*` | Default (String) | `abc` |
| `$*` (except for characters beloew) | Default (string) | `$abc` |
| `$$` | String | `$$abc` |
| `$#` | Integer | `$#1`, `$#-12345` |
| `$!` | Boolean | `$!True`, `$!anything-else-is-false` |

The only two interpretations that require further explanation are
the integer and the boolean types.  The integer type translates any
characters past the prefix as a signed integer and the boolen type
compares any characters past the prefix in a case-insensitive manner
against the sequence `true`.

For the integer translation, if the value `$#1.1` is provided, the
behavior afterwards depends on how that value is referenced.  In the
case of the `--set` command line argument, the `ValueError` will be surfaced
to the command line and the application will stop.  If provided as
part of a configuration format that does not provide typing, the
`ValueError` will usually result in the default value being used for
that configuration key.

#### Specifying Strict Configuration Mode

During the development of the linter, there were specific times that
I wanted to be sure that the configuration values that I specified
were exactly as I specified them.  As I started doing exploratory
testing of the project, I realized that I am enough of a stickler
to want to ensure that my configuration values are correct and that
the values that I am setting are not reverting to default values.

Specifed from the command line as the `--strict-config` flag or
through the configuration as `mode.strict-config=$!True`, this
option turns on the strict mode flag of the configuration system.
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
python main.py --strict-config -s log.level=$#1 scan examples
```

will produce the following output:

```text
Configuration Error: The value for property 'log.level' must be of type 'str'.
```

and the following command line:

```sh
python main.py --strict-config -s log.level=information scan examples
```

will produce the following output:

```text
Configuration Error: The value for property 'log.level' is not valid: Value 'information' is not a valid log level.
```

## Available Configuration Values

### Configuration

| Key | Command Line | Type | Description |
| -- | -- | -- |-- |
| -- | --config {file}    | string | Path to the configuration file to use. |
| -- | --set {key}={value}       | string | Manualy set an individual configuration property. |
| mode.strict-config| --strict-config   | boolean | Throw an error if the configuration is bad, instead of assuming default values. |

### Logs

| Key | Command Line | Type | Description |
| -- | -- | -- |-- |
| log.file          | --log-file        | string  | Destination file for log messages. |
| log.level         | --log-level       | string* | Minimum level required to log messages. |

### Plugins

| Key | Command Line | Type | Description |
| -- | -- | -- |-- |
| -- | --enable-rules   | string    | Comma separated list of rules to enable. |
| -- | --disable-rules  | string    | Comma separated list of rules to disable. |
| -- | --add-plugin     | string    | Path to a plugin containing a new rule to apply. |

### Other

| Key | Command Line | Type | Description |
| -- | -- | -- |-- |
| -- | --stack-trace | boolean | if an error occurs, print out the stack trace for debug purposes.  Also sets the initial logging (config processing) to debug. |

### Extensions Section

#### Front Matter

| Key | Command Line | Type | Description |
| -- | -- | -- |-- |
| `extensions.front-matter.enabled` | - | Boolean | Enable the parser to recognize front-matter. |

For more information on Markdown Front-Matter, see [this document](/docs/extensions/front-matter.md).

### Plugins Section

| Key | Command Line | Type | Description |
| -- | -- | -- |-- |
| `plugins.{id}.enabled` | --enable-rules, --disable-rules | Boolean | ... |
| `plugins.{id}.other` | - | Various | ... |

The list of configuration values for rule plugins is slightly
different than the configuration for the rest of the system.
For each rule plugin, there is a main boolean configuration
value in the form `plugins.{id}.enabled` that specifies the rule
plugin's enabled state.  In that string, the sequence `{id}`
can be any one of the valid identifier for the plugin rule.

Once enabled, each rule plugin is responsible for its own
properties located under the hierarchy of `plugins.{id}.`.
The list of configuration values avaiable for each standard
plugin rule is given in the `Configuration` section for
each [standard rule plugin](/docs/rules.md).

Since a rule plugin can have two or more identifiers,
one id plus multiple aliases, there has to be a predicatable
ordering used to resolve issues where configuration is
provided for multiple identifiers belonging to a single
plugin rule.  In order, the rule plugin's id comes first,
then each alias in the order that they are entered in the
plugin rule itself.  This rule applies to the group of
configuration values as a group.

For example, suppose there is a configuration file with
the contents of:

```json
{
"plugins" : {
    "md019" : { 
        "enabled" : false
    },
    "heading-style-h1" : { 
        "enabled" : true,
        "style" : "consistent"
    }
}
```

First thing to notice here is that the `plugins.md019`
configuration will take precedence over the `plugins.heading-style-h1`
configuration specified after it.  Regardless of its position
in the configuration, the `plugins.md019` has precedence. Also,
assuming for minute that the `"enabled" : false` disables the
rule plugin, even though the `plugins.heading-style-h1.style`
configuration value is set, it will not be used.  For that
configuration value to be used, the `plugins.md019` configuration
must be removed.
