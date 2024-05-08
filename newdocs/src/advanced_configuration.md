---
summary: More information on configuration and how to apply it.
authors:
  - Jack De Winter
---

# Advanced Configuration

Configuration is one of those topics that almost every application has to deal with.
From simple command lines, to invoking features, to setting values for those features,
applications need a form of configuration management to provide the variables for
those tasks.
And early in the development phase of the PyMarkdown application, we knew
we needed a solid one ourselves.

## Skipping Ahead

As this is the Advanced Configuration document, we spend a significant amount
of time describing the configuration manager and how it resolves configuration
items. While we highly recommend you take the time to understand the configuration
manager before you try and change configuration values, whether to do that is your
decision to make.

If you intend to skip ahead, here are some sections that we believe you may find
relevant:

- [Configuration Files](#configuration-files)
    - the types of configuration files that we support, and how to access them
- [Command Line Configuration](#command-line-configuration)
    - how to specify configuration items from the command line.
    - If dealing with boolean values
      or integer values, pay attention to the [Configuration Item Types](#configuration-item-types)
      section
- [Enabling or Disabling Rules](#how-to-enable-or-disable-rules)
    - turning a set of rules on and off
- [Available Configuration Items](#available-configuration-items)
    - a full list of configuration items and options for how to change their values

## Nomenclature

Before we get too deep in our documentation, we thought it would be useful to
clearly describe the more important words and phrases we will be using.

### Configuration Manager

A component that takes care of managing multiple configuration input
sources and represents them as a logical and coherent set of configuration items.

### Configuration Item

A pairing of the rank and name of the configuration item along with its value.

### Hierarchical

The word [hierarchy](https://www.merriam-webster.com/dictionary/hierarchy) has many
definitions.  The one that comes closest to our use of it is:

> a ruling body of clergy organized into orders or ranks each subordinate to the
> one above it

Our configuration manager is hierarchical because it organizes its data into ranks,
where each rank determines the context of the rank below it.  For example, each group
of top-level items has a subordinate group of items below them, and those subordinate
items may also have their own subordinate items.

### Flattened Hierarchical

While a tradition hierarchy is expressed in a form such as:

```text
extensions
   my_extension
      my_value_1
      my_value_2
   my_other_extension
      my_value_1
```

some configuration files do not support this expression of the hierarchy.  To
accommodate those systems, our configuration manager supports a flattened form
of this hierarchy.  A flattened hierarchy achieved this by taking each rank,
appending a `.`
character to it, and then repeating this process for the next rank.  Given
the above hierarchy as an example, a flattened form would be:

```text
extensions.my_extension.my_value_1
extensions.my_extension.my_value_2
extensions.my_other_extension.my_value_1
```

The expression of the hierarchy has been brought down from 6 elements to
3 elements.  The cost for this compact format is that it is not as readable
as the non-flattened hierarchy.  The benefit is that even the simplest configuration
file formats can specify configuration item names with this format. As an extra
benefit, trying to convey a normal hierarchy can be time consuming, whereas
the flattened form is compact and simplifies communication of the hierarchy.

### Layered

The word `layered` implies that something has multiple distinct parts to it.  For
our configuration manager, we designed a data store that can handle input from various
sources, assigning each of those types of data sources to a given "layer".  When
viewed from an external point of view, these layers collapse to provide a single
view of the configuration data.

### String Value

A string value is a sequence of characters that is usually surrounded on both sides
by a boundary character.  For string values, that boundary character is either the
`'` character or the `"` character. For example, `"surrounded"` and
`'surrounded'` are examples of a string value.  Note that different formats may
have conditions on which of the boundary characters denote a string value for that
format.

### Integer Value

An integer value is a sequence of numeric characters which may include a single `-`
character or a single `+` character.  While some formats may accept a specified
value that includes a decimal point (`.` character), an integer value specifically
does not include any decimal point character.

### Boolean Value

A boolean value is a value that is either `true` or `false`.  Note that different
formats will have different rules regarding what values are considered `true` or
`false`, including whether any capitalization of the value is allowed.

### Case-insensitive

This refers to a comparison that is done without respect to the case of any
characters in the given string.  Using a case-insensitive comparison,
`False`, `false`, `FALSE`, and `FaLsE` are all equal.

## Work By Default

After taking stock of the requirements that we needed from a configuration manager,
we set out to create a configuration manager that we could feel proud of.  Given
our internal list of requirements, we
worked to balance the need for multiple sources of truth with the ability
to efficiently present that data to the application.  In the end, we are
pleased that we built a solid configuration manager that
meets our needs and has room for future extension.

While a lot of the decisions were easy, it took us a while to arrive at
the decision that we wanted our configuration manager to "work by default".
We use the phrase "work by default" as we have seen systems designed with
configuration managers that are extremely strict about what they accept. When
evaluating certain tools, we found that we spent 5-10 minutes setting various values
before we
were able to figure out if the tool worked for us.  We wanted to avoid giving
our users that sense of exasperation, if possible.

We do acknowledge that a strict configuration system is beneficial for large-scale,
back-end systems, especially ones without any reasonable user interface.  For our
application, we believe that when a user
starts to use the PyMarkdown application, the application should be lenient until
it is
told by the user to not be lenient.  In that way, unless the user specifically
asks the configuration manager to [check for bad configuration](#strict-configuration-mode),
the PyMarkdown application can continue with its work of scanning Markdown documents
for the user.

## Configuration Items

Back in the previous section on Nomenclature, we defined the terms
[Configuration Item](#configuration-item)
and [flattened hierarchical](#flattened-hierarchical) format.  Before we go forward,
we believe it is useful to be succinct in what we mean about a configuration item
and how we define such an object.

A configuration item contains two components: a hierarchical name
and a typed value.  We choose to store our configuration items within a hierarchical
structure, but not all file formats are able to convey that hierarchical format effectively.
In
addition, it is difficult for our team to express that exact hierarchical structure
in a text format that
does not involve multiple lines and wasteful whitespace.
As such, we describe the configuration item name using a flattened hierarchical format
that at least conveys the hierarchy information properly.

When we describe the value component of a configuration item, the value
is implicitly typed as a [string value](#string-value) unless otherwise specified.
Our configuration manager also supports a [boolean value](#boolean-value) and an
[integer value](#integer-value).  To date, we have not found any solid reason for
expanding our type system beyond those three type values.

## Configuration Ordering (Layering)

To provide the maximum flexibility to our users, our team designed a layered, hierarchical
configuration property management system.  To ensure that the layers
can collapse in a predictable manner, each layer is aggregated according to the
increasing
specificity of the configuration information.  As we believe the most specific
setting of data should have the highest priority, the aggregation occurs from the
least specific layer to the most specific layer.

What does that mean in plain words? It means that we work from the least
specific data source (default values) to the most specific data source
(general command line settings), applying each layer
of data as we get more specific.  Therefore, we apply the layers of data
in the following order:

- default value (implicit if no other value provided)
- alternate configuration file (`tool.pymarkdown` section of `pyproject.toml` file)
- default configuration file (for example, `.pymarkdown` file in current directory)
- configuration file specified on the command line by the arguments `--config {filename}`
- specific command line setting (for example, `--set log.level=INFO`)
- general command line settings (`--add-plugin`, `--log-file`)

By following this order, we can predictably build any required configuration item's
value in a manner that is logical and explainable.  While most people will only
use one of these data sources, we wanted to make sure that we clearly describe
this ordering for any users that have a more complex configuration involving
multiple data sources.

And to be truthful, sometimes we need to check our own documentation to
remind ourselves of this order.

### Default Value

Each time that PyMarkdown asks the configuration manager for a configuration item,
it provides
a default value to use if none other are provided.  This default ensures that a
predictable
value is returned if no layers have a value for the configuration item in question.
Note
that this layer is special in that it is implicit. If no value is assigned after
every other layer is applied, the default value is then applied.

### Alternate Configuration File

Support for the `pyproject.toml` file was added as a more generic way to support
PyMarkdown configuration.  For those users who prefer their project configuration
in
a single file, this supports a `tool.pymarkdown` section that allows the user to
specify
configuration items using a flattened hierarchy.

### Default Configuration File

Support for the JSON based `.pymarkdown` configuration file was added as our team
got tired of having to add a configuration file to the command line.  While the
initial default configuration files were in the JSON format, support for the YAML
based
`.pymarkdown.yml` and `.pymarkdown.yml` configuration files were added later.

### Command Line Configuration File

The first form of configuration for the PyMarkdown project was support for a JSON
configuration file on the command line.  Using the `--config` command line argument
allowed for a consistent and concise way to configure PyMarkdown for each needed
scenario. Currently, the configuration file may be one of: JSON, YAML or TOML.

### Command Line `--set` Argument

With other forms of configuration implemented, our team found that there was a
bit of a gap between the general command line arguments and the configuration files.
The `--set` argument was introduced to fill this gap, mainly added to be able to
set an argument or two on the command line without having to craft a new configuration
file.  Note that because the command line does not support any implicit hierarchical
format, these arguments use a [flattened hierarchical](#flattened-hierarchical) format.
Also, because the command line is not capable of conveying type information,
a [special type system](#configuration-item-types) was devised
to convey that information.

### General Command Line Argument

The second form of configuration for the PyMarkdown project was support
for simple but direct arguments that change how PyMarkdown processes the Markdown
files.
These arguments are specified in the User Guide document's section
on [General Command Line Arguments](./user-guide.md#general-command-line-arguments).
Our guideline for these arguments was that each argument should target a specific
behavior, with the documentation for that argument specifically highlighting how
they affect PyMarkdown's processing.

### Examples

It is always best if you can show things with practical examples, so we present
examples to highlight the configuration layering.  Note that the lines in the examples
have
been split for readability and would normally be split using the operating system's
split character.

Note that while we only give two examples in this section, the same principles
apply to interactions between the other layers as well.

#### 1 - General Command Line Argument

Take the command line:

```text
pipenv run pymarkdown --enable-rules md007
                      scan --recurse .
```

The argument `--enable-rules` falls under the General Command Line Argument layer.
Because the value is set at the highest layer, it will override any other setting
of that
configuration item in any of the lower layers.

#### 2 - Specific Command Line `--set` Argument

Adding on to the command line in the last section, we now have:

```text
pipenv run pymarkdown --enable-rules md007
                      --set extensions.front-matter.enabled=$!True
                      --set plugins.md007.enabled=$!False
                      scan --recurse .
```

First off, note that the `--set` argument has special formatting that is explained
in the section below on [Configuration Item Types](#configuration-item-types).
In this case, line 2 is asking
for the value of `True` to be assigned to the configuration item `extensions.front-matter.enabled`
and line 3 is asking for the value of `False` to be assigned to the
configuration item `plugins.md007.enabled`.

The argument on line 3 is a specific command line argument, but it is not as specific
as the `--enable-rules` argument on line 1. Hence, Rule Md007 will remain enabled
as the setting one line 1 was made at a higher layer.  Since line 2 is the only
place where the `front-matter` extension is enabled, the configuration item will
be set to that value.

## Default Configuration Values

At the very bottom of the layer list is the default value for a configuration
item.  All PyMarkdown calls to the configuration manager to get a value provide
a default
value to use if no value was supplied.  These values are the ultimate fallback
values, expected to provide the most common experience to the user.
For plugins, this allows a handful of plugins to be disabled by default, as their
usage is either not common or outdated.  For extensions, it allows for extensions
to be added in such a way that they do not affect current behaviors.

Our team strives to document each of these default values for you, as well
as documenting the default behavior.  We believe this is important, as it
allows you to understand the default behavior of our system.

## Configuration Files

When you want to set a small set of configuration item values once, setting those
values by the command line is very efficient.  However, once the collection of
configuration items grows beyond a small set or you must enter the same
values across multiple projects, which is where configuration
files come in handy.

One important fact about the configuration files that PyMarkdown supports:
they all have typed values.  That is to say that each type of configuration file
supports a native mechanism for specifying a string value, an integer value,
and a boolean value.

### Configuration File Types

The PyMarkdown application supports configuration files in three formats:
JSON, YAML and TOML.

#### JSON

The [JSON file format](https://www.w3schools.com/whatis/whatis_json.asp) is one
of the most widely used file formats for exchanging
data between systems.  The [JavaScript Object Notation](https://en.wikipedia.org/wiki/JSON)
format was created
in 2001 by David Crockford to enable standardized electronic data interchange
between browsers and backend system.  In fact, one of the first uses of JSON
was to allow browsers to refresh sections of their pages without having to
reload the entire page.  While that may seem ordinary now, that was novel when
it was introduced.  From there, its use just continued to grow due to its
readability and robustness.

Using the example from the previous section, [example 2](#2-specific-command-line-set-argument),
this is what that configuration looks like in JSON format.  To make the example
more interesting, we also
include the setting of `plugins.md007.code_block_line_length` to the integer value
of `160`.

```json
{
    "plugins": {
        "md007": {
            "enabled": true,
            "code_block_line_length" : 160
        }
    },
    "extensions": {
        "front-matter" : {
            "enabled" : true
        }
    }
}
```

There are three important things to understand about the JSON configuration
file format.  The first thing is that the values presented above are typed
values.  Due to the absence of `"` characters, the two `enabled` fields
denote a boolean `true` value, and the `code_block_line_length` field denotes
an integer `160` value.  As JSON is extremely strict about its structure, the
configuration manager can read this file and leverage that strictness.

The second thing to understand is the use of a normal hierarchical structure
instead of a flattened hierarchical structure.  While flattened structures
are useful when describing the configuration item, they are not efficient
when storing the configuration item.  As we can see by the above example,
there are two configuration items that reference Rule Md007: the `enabled`
item and the `code_block_line_length` item. This shared structure serves
as a visual reminder that they are related, while also reducing the count
of characters needed to represent those two configuration items.

The final thing to understand is that the hierarchy of a JSON file is
enforced through the choice of specific characters at each level. For
example, the line `"plugins": {` means that the JSON object `plugins`
contains another object.  The line `"enabled": true` means that the
JSON object `enabled` contains a boolean value of true.  Those characters,
and other similar characters, allow JSON to unambiguously represent the configuration
items. That strict representation is one of JSON's strengths.

##### Added Note

Please keep in mind that the JSON example above is what is referred to as a "pretty"
example,
a JSON file with a four-space indent at each level.  It can also be
rendered in a condensed format with a zero-space indent as:

```json
{
"plugins": {
"md007": {
"enabled": true,
"code_block_line_length" : 160
},
},
"extensions": {
"front-matter" : {
"enabled" : true
},
}
}
```

or as a single line:

```json
{"plugins":{"md007":{"enabled":true,"code_block_line_length":160},},"extensions":{"front-matter":{"enabled":true},}}
```

without any loss of hierarchy or data.  While that is possible, we highly
recommend that you use a form of the "pretty" JSON format for your human
readable configuration file, simply because it is more readable.

#### YAML

Like the JSON file format, the [YAML file format](https://yaml.org/) can
represent hierarchical data. This acronym, standing for the recursive
[YAML Ain't Markup Language](https://en.wikipedia.org/wiki/YAML), removes most
markup characters in favor of a more simplistic approach:

```yaml
plugins:
  md007:
    enabled: true
    code_block_line_length: 160
extensions:
  front-matter:
    enabled: true
```

Here, instead of the `{` and `}` characters of JSON, YAML uses whitespace to
denote hierarchy.  But it does not stop there, as shown in [this tutorial](https://www.cloudbees.com/blog/yaml-tutorial-everything-you-need-get-started).

<!-- pyml disable-next-line no-duplicate-heading-->
##### Added Note

From a configuration file viewpoint, it is not useful that YAML files may contain
multiple documents by using a `---` separator to denote a new document. However,
two things that YAML does have that are useful for configuration files are comments
and the string-block character.

Comments are a feature that is particularly useful in configuration files, as shown
in the following example:

```yaml
# See organization standards at https://internal.org.com/standards
plugins:
  md007:
    enabled: true
    code_block_line_length: 160

# Enable front-matter extensions, as MkDocs needs them.
extensions:
  front-matter:
    enabled: true
```

Where the block character (`|`) comes into play is when defining strings that
are long and span multiple lines.  If a string is long and spans multiple lines,
instead of the following (for a made-up Rule Smt001):

```YAML
plugins:
  SMT001:
    response: "Please send any questions\nto our organization mailbox\nat help@internal.org.com"
```

that string can be represented as:

```YAML
plugins:
  SMT001:
    response: |
Please send any questions
to our organization mailbox
at help@internal.org.com"
```

While both forms of the `response` field are equal, the block character field
value is the most readable.

##### Comparison To JSON

Between YAML having fewer moving parts and fewer format
characters, we feel that YAML mostly wins when it comes to readability.  If you
are a fan of using tab characters in configuration files, be aware that YAML
does allow tab characters, but only in situations where indentation does not apply.

The only issue our team has with YAML's readability (hence our statement that YAML
"mostly wins when it comes to readability") is how its string values are interpreted.
For example, in YAML:

```YAML
code_block_line_length: my string
```

is interpreted as a string, and:

```YAML
code_block_line_length: "160"
```

is interpreted as a string, but:

```YAML
code_block_line_length: 160
```

is interpreted as a number.  From our point of view, we would like to
be able to look at YAML field values and to determine their value quickly.
This could easily be mitigated by a team guideline that states that all YAML string
fields must use the `'` or `"` characters to denote the string.

#### TOML

Rounding out our list of configuration file formats is the [TOML file format](https://toml.io/en/).
With another acronym, [Tom's Obvious, Minimal Language](https://en.wikipedia.org/wiki/TOML)
has gained support as an easy to read and understand file format.  Keeping with
our established tradition, here is the same configuration presented in TOML
format.

```toml
[plugins.md007]
enabled = true
code_block_line_length = 160

[extensions.front-matter]
enabled = true
```

Not shown in the examples, all strings must be enclosed in either
the "single quote" character (otherwise known as the apostrophe character `'`)
or the quote character (`"`).  Along with providing for comments, it is a nice
middle ground reminiscent of the [Ini File Format](https://en.wikipedia.org/wiki/INI_file)
used on Windows machines.

<!-- pyml disable-next-line no-duplicate-heading-->
##### Added Note

While TOML does not normally support any visible hierarchical structure,
the format of a TOML file does allow for empty sections and indented values.
Those features of TOML allow the following TOML hierarchy to be valid:

```toml
[plugins]
  [plugins.md007]
    enabled = true
    code_block_line_length = 160

[extensions]
  [extensions.front-matter]
    enabled = true
```

even if it is not enforced.  Along those same lines, since the `.` character is
a valid part of a TOML property name, the following hierarchy is also possible:

```toml
[plugins]
md007.enabled = true
md007.code_block_line_length = 160

[extensions]
front-matter.enabled = true
```

<!-- pyml disable-next-line no-duplicate-heading-->
##### Comparison To JSON

After examining the JSON and YAML file formats, TOML is a decent compromise between
the strictness of JSON and the ease of reading of YAML.  However, in our opinion,
this tradeoff comes at the expense of a normal hierarchical
structure.  This tradeoff can be mitigated by one of the examples shown in the last
section, but that mitigation would have to be enforced by the team, not any TOML
tooling.

#### Which One Is Best?

The honest answer is that it depends.  Each of the three file formats has its strengths
and weaknesses.  If you and your team have a choice of which file format is best,
we strongly encourage you to look at the above examples and decide which one resonates
with you. If comments are important to you, then JSON is out.  If a clearly visible
hierarchy is important to you, TOML is probably out.  If you do not want to remember
the rules for typing strings, YAML is out.

We hope we have done a decent job of showing you the different file formats that
you can use for configuration.  The rest is up to you and your team.  And if you
change your mind in the future, sites like [this one](https://transform.tools/yaml-to-toml)
allow you to change the file format (with caveats) with ease.

### Command Line

The most visible way to specify a configuration file to PyMarkdown is to use the
command line `--config` argument.  That argument specifies a relative or absolute
path to the configuration file to load.  The configuration file may be in any one
of three formats discussed in the [last section](#configuration-file-types).
PyMarkdown will try and load the configuration file as JSON first,
then YAML, then TOML before erroring out.

Keep in mind that configuration files are the third most [specific layer](#configuration-ordering-layering)
of the PyMarkdown configuration layers.  Especially when debugging and focusing on
other subjects, it can be easy to forget that there are two other layers of settings
that will override those in the configuration file.

### Default Configuration Files

Once our team got used to having configuration files, we immediately started wondering
if there was a better way to load the configuration files than using the command
line.  We looked at other linters, such as PyLint and Flake8, and they both have
configuration files that are a single `.` character followed by their name.  If
these files are present
in the directory where the linter is executed from, it uses the configuration file
without any need for the `--config` argument.

Seeing a pattern that we liked, we added default configuration file support for
the filename `.pymarkdown` in the current directory.  At that time, we only had
support for JSON file formats, so the
`.pymarkdown` configuration file uses the JSON format.  After implementing that
feature, we received feedback from users that having a default YAML configuration
file would be useful to them.  As such, we added support for the filenames
`.pymarkdown.yml` and `.pymarkdown.yaml` that are YAML configuration files. Because
the configuration file is a default configuration file, our team felt that it was
important to highlight to the user that this default file is a YAML file, not
a JSON file.

### Project Configuration File

Support for the `pyproject.toml` file was added as a more generic way to support
PyMarkdown configuration.  Depending on the number of tools used by the project
team, the team may feel that their project's root directory has too many configuration
files. The math is simple. If even half the tools have their own default configuration
file
and you are using ten or more tools, your project will contain at least five tool-based
configuration files.  At that point, an alternative project level configuration
file starts to look attractive.

The `pyproject.toml` file is a standard TOML file that uses the `tool.pymarkdown`
section to contain any PyMarkdown configuration items.  The only difference between
using the `pyproject.toml` and a normal TOML configuration file is that the user
must place all configuration items within the `tool.pymarkdown` section.
Therefore, in all cases, the [flattened hierarchical](#flattened-hierarchical)
form of the configuration item name must be used.

```toml
[tool.pymarkdown]
plugins.md007.enabled = true
plugins.md007.code_block_line_length = 160
extensions.front-matter.enabled = true
```

## Command Line Configuration

Configuration items set from the command line are the most specific form
of configuration for the PyMarkdown application.  Unlike any of the configuration
items in configuration files, these settings are specifically targeted to a specific
invocation of the PyMarkdown application.

These arguments come in two classes: a specific command line setting and a general
command line setting.  To illustrate the usage of command line arguments to set
configuration items, the following configuration items will be used as a reference:

- `log.level` - string value of `INFO`
- `plugins.md007.code_block_line_length` - integer value of `160`
- `plugins.md007.enabled` - boolean value of `true`
- `extensions.front-matter.enabled` - boolean value of `true`

### Specific Command Line Settings

Specific command line settings use the `-s` or `--set` argument to
specify a single configuration property to set the value for.  The specific property
is identified using
its [flattened hierarchical format](#flattened-hierarchical)
and an optional [configuration type](#configuration-item-types)
for the property value. If no configuration type is provided, the property uses
a default type of `string`.
These two concepts work together to provide a condensed way to specify configuration
properties from the command line.

For the PyMarkdown development team, these arguments have proven to be useful in
providing shorthand for setting properties that are isolated and near the top
of the configuration item specificity list.  Because of its high ranking in the
configuration layers, these
settings are less likely to be overridden.  For example, a common command line that
we use to display enhanced logging output is:

```bash
pymarkdown --stack-trace -s log.level=INFO scan examples
```

While a handful of configuration items have general command line settings, most
configuration items do not.  [This section](#available-configuration-items) provides
up to date information on the command line arguments and any specific command line
counterparts.  From our list of reference configuration items, only the `log.level`
item and the `plugins.md007.enabled` items have general command line settings.
In general, count on any extension configuration items and rule
configuration items to only be accessible using the `--set` command.

### Configuration Item Types

To provide a more robust configuration system, the configuration
manager uses values that are typed.  This extra
level of specification allows increased confidence that the value that
is provided for that configuration item is interpreted properly.
If you are using a configuration file format that provides type information,
this extra information is not required. However, as the command line
does not provide this type information, our team needed to develop
a notation that indicates what type to apply to the command line `--set` argument.

The type specification notation is as a prefix that the user applies for the configuration
item value. If the `*` character refers to any character, the following
table specifies the type behavior:

| Prefix | Type | Examples |
| --- | --- | --- |
| `*` or None | Default (String) | `abc` |
| `$*` (except for characters below) | Default (String) | `$abc` |
| `$$` | String | `$$abc` |
| `$#` | Integer | `$#1`, `$#-12345` |
| `$!` | Boolean | `$!True`, `$!anything-else-is-false` |

The only two interpretations that likely require further explanation are
the integer and the boolean types.  The integer type attempts to
translate any characters past the prefix as a signed integer.  The
boolean type compares any characters past the prefix in a [case-insensitive](#case-insensitive)
manner against the sequence `true`, setting the configuration item's value to `True`
only if that comparison is true.

For our team, the decision to compare boolean values against `true` was an
easy one, with precedents in other tools.  But applying similar rules
to the integer conversion was not possible.  After thinking things through, we
landed on generating a ValueError for any invalid integer values, such as `$#1.1`.
There were alternatives, but this was the decision that felt the most
correct to us.  If a user took the time to use the integer prefix `$#`,
we felt they would want use to error out on any non-integer value.

#### Special Characters and Shells

On a Windows system, when entering configuration item type arguments that specify
a boolean type, the `!` character is used. Since this character is a special character,
you need to enter it as `^^!` on the command line to properly escape the `!` character.

```text
pipenv run pymarkdown --set extensions.front-matter.enabled=$^^!True scan -r .
```

On a Linux or MacOs system, most shells treat the `$` character as a special
character.  To escape this character, you need to enclose the argument with the
`'` character instead of the normal `"` character.

```text
pipenv run pymarkdown --set 'extensions.front-matter.enabled=$!True' scan -r .
```

#### Typing Examples

Using actual PyMarkdown configuration items, examples of our typing in action are:

<!-- pyml disable-num-lines 30 fenced-code-language-->
- indicate that the logging level should be set to
  show information log messages or higher (string value):

    ```
    pymarkdown --set log.level=INFO scan test.md
    ```

    OR

    ```
    pymarkdown --set log.level=$INFO scan test.md
    ```

    OR

    ```
    pymarkdown --set log.level=$$INFO scan test.md
    ```

- enabling the extension to interpret front matter (boolean value):

    ```
    pymarkdown --set extensions.front-matter.enabled=$!True scan test.md
    ```

- setting the maximum line length for code block lines to `160` (integer value)

    ```
    pymarkdown -s plugins.md007.code_block_line_length=$#160 scan test.md
    ```

### General Command Line Setting

Trying to determine which configuration items should have a more direct way of
setting their values was not an easy task for our team.  Enabling every setting
to have a direct command line invocation is not possible, so we had to derive
a guideline for when a configuration item would merit its own command line argument.

Reviewing our full list of [available configuration items](#available-configuration-items),
we believe that we did a decent job of applying the following guidelines to the
existing configuration values.

The first criteria that we decided on was to determine how frequently
that configuration item would be used.  A good example of this is the
`--enable-rules` and `--disable-rules` arguments. We figured that out of all
the configuration items in the PyMarkdown application, those two arguments
are probably the most used configuration items.  From there, we tried to
hit any other frequently used configuration settings, giving each a command line
argument.

The second criteria we used was to determine whether the configuration item
changed the behavior of the core PyMarkdown engine, or if it was related to
one of the rule plugins or extensions. When we looked at other applications
with plugins, we saw that the core functionality of those applications
seldom changed, while any functionality expressed through plugins is subject to change.
An example of this is the
`--return-code-scheme` general command line setting.  Since it directly affects
how return codes are returned from the core Markdown engine, we exposed
it as a general command line argument.  

## Strict Configuration Mode

During the development of the PyMarkdown linter, there were specific times where
we wanted to be sure that the configuration values that we specified were interpreted
exactly as we specified
them.  As we started doing exploratory testing of the PyMarkdown project, we also
realized that we are sticklers, wanting to ensure that any configuration properties
that we assign are correct and that those values are not reverting to default values.

However, our team's desire for that level of exactness seemed to be at
cross purposes to our decision to provide for a configuration manager that would
[work by default](#work-by-default).  That is where the genesis of the idea
that would become the configuration manager's strict mode was formed.

Specified from the command line using the `--strict-config` flag (or
through the configuration as `mode.strict-config=$!True`), this
configuration item turns on the strict mode for the configuration system.
Once enabled, when the application reads values from the configuration,
it will stop the application if:

- the user provided a value for the configuration value, but it was the wrong type
- the user provided a value for the configuration value, but it does not match
  a specified filter for that value

Using the `log.level` example from above, the documentation states that it is required
to be a string in the following set: `CRITICAL`, `ERROR`, `WARNING`, `INFO`,
or `DEBUG`.  Therefore, both an integer value of `1` and a string value of
`information` would fail for distinct reasons.  Normally, these would
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

This feature is more burdensome for the user, but it is provided as an option for
those users who want to make sure their provided configuration items are adhered
to exactly.

## Available Configuration Items

### Configuration

These items directly affect the collection of configuration values and how they
are interpreted.

<!--- pyml disable-num-lines 5 line-length-->
| Key | Command Line | Type | Description |
| -- | -- | -- |-- |
| --                    | --config {file}           | string    | Path to the configuration file to use. |
| --                    | --set {key}={value}       | string    | Manually set an individual configuration property. |
| mode.strict-config    | --strict-config           | boolean   | Throw an error if the configuration is bad, instead of assuming default values. (Default: `false`) |

### Logs

These items affect the logging for the application.

<!--- pyml disable-num-lines 5 line-length-->
| Key | Command Line | Type | Description |
| -- | -- | -- |-- |
| log.file          | --log-file        | string  | Destination file for log messages. |
| log.level         | --log-level       | string* | Minimum level required to log messages. Valid values are: `CRITICAL`, `ERROR`, `WARNING`, `INFO`, or `DEBUG`. (Default: `WARNING`)  |
| log.stack-trace | --stack-trace | boolean | if an error occurs, print out the stack trace for debug purposes.  Also sets the initial logging (config processing) to debug. (Default: `false`) |

These configuration values affect how the application logs information.  The two
easiest to explain are the `*file` and `*level` values.  These configuration values
specify what the log level is for the application and whether to redirect any logged
information away from the standard output (stdout) to the specified log file.

The `log.stack-trace` configuration item (and its `--stack-trace` command line flag)
are
a bit more nuanced in its behavior. The simple part of this setting's behavior is
to generate a debugging stack trace when an application error occurs.  From our
experience, this information is confusing to the typical users, but is information
critical to the diagnosis of any application error.

The nuanced part of this flag has to do with the application's initialization
process.  Because the configuration manager must be initialized to access the
`log.stack-trace` configuration item, there is a narrow window where there is
no control over log settings and whether to emit a stack trace for an application
error. As one of the only reasons to use the command line flag is to debug an
application error, it seems fitting to also enable debug debugging until the
configuration manager is properly initialized.
Normally we typically stick to a "one configuration item, one result" guideline,
but this seemed to be a good time to make an exception.

### Rule Plugins

These affect the collection of rule plugins and whether they are called.

<!--- pyml disable-num-lines 5 line-length-->
| Key | Command Line | Type | Description |
| -- | -- | -- |-- |
| *special* | --enable-rules,-e   | string    | Comma separated list of rules to enable. |
| *special* | --disable-rules,-d  | string    | Comma separated list of rules to disable. |
| plugins.additional_paths | --add-plugin     | string    | Path to a plugin containing a new rule to apply. |

The enabling and disabling of plugins can be accomplished in two ways.  From the
command line, the `--enable-rules` and `--disable-rules` arguments allow for the
user to specify a comma-separated
set of rule identifiers in the next argument.  If a configuration file option
is required, the rule plugin can be enabled as specified in the next section.

Additional rule plugins can be added to the configuration in one of two ways.  To
test new rule plugins,
the recommended way to add a rule plugin is to use the `--add-plugin` command line
argument once for each rule plugin to add.
Each `--add-plugin` argument is followed by another argument that specifies a file
or a directory to load
any new plugins from.  For a more permanent solution, the `plugins.additional_paths`
configuration value
can be used in a comparable manner, specifying one or more paths using a comma-separated
string containing the paths.

### Rule Plugin Settings

<!--- pyml disable-num-lines 4 line-length-->
| Key | Command Line | Type | Description |
| -- | -- | -- |-- |
| `plugins.{id}.enabled` | -- | Boolean | Specify whether the plugin rule is enabled. |
| `plugins.{id}.other` | -- | Various | Specify other configuration properties specific to the rule. |

The list of configuration values for rule plugins is slightly
different than the configuration for the rest of the system.
For each rule plugin, there is a main boolean configuration
value, in the form `plugins.{id}.enabled`, that specifies the rule
plugin's enabled state.  In that string, the sequence `{id}`
can be any one of the valid identifiers for a plugin rule.

Once enabled, each rule plugin is responsible for its own
properties located under the hierarchy of `plugins.{id}.`.
The list of configuration values available for each standard
plugin rule is shown in the `Configuration` section for
each [standard rule plugin](./advanced_plugins.md).

### Extensions

Extensions follow the same pattern as rule plugins, except that no general
command line settings are available.  From our experience, enabling extensions
is usually done from configuration files, and applied to an entire project.
As such, we do not believe having a general command line setting provides
any benefit to the user.

Like the rule plugins, the list of configuration items for each
extension is shown in the `Configuration` section for
each [extension](./advanced_extensions.md).

### Other

These items do not fit nicely into any other category.

<!--- pyml disable-num-lines 4 line-length-->
| Key | Command Line | Type | Description |
| -- | -- | -- |-- |
| -- | --continue-on-error | Boolean | Enable PyMarkdown to continue after application errors. |
| -- | --return-code-scheme | String | Specify a scheme to use when formulating the return code. |

These two arguments do not match to configuration items, and instead are interpreted
right from the command line. The argument `--continue-on-error` specifies that the
application can continue after an application error, while still emitting a return
code that indicates that application error.  The argument `--return-code-scheme`
alters the return code values based on a selected map of outcomes to return codes.
Both are better documented in the User Guide section on
[General Command Line Arguments](./user-guide.md#general-command-line-arguments).

## Common Topics

### How To Enable or Disable Rules

The easiest way to enable or disable rules is with the command line.

```text
pymarkdown -d MD041,md013 scan .
```

Whether specified by a configuration file or through the command line, the
enable and disable settings follow the normal rules of [Configuration Ordering](#configuration-ordering-layering).
That is to say that the above command line will override any enable/disable
setting using the `--set` command line or through a configuration file.

#### Exception: Enabling/Disabling Rules From The Command Line

One tenet that we strive to follow is to have a clearly defined behavior for
our application.  And for observant readers, there was a bit of undefined behavior
talked about in the last section.  Consider the following example:

```text
pymarkdown -e Md041 -d Md041 scan .
```

As PyMarkdown allows for both enabling and disabling of a plugin to occur on
the command line and assigns it to its highest layer, what happens if both
are specified for the same rule?

Encountering this rule during our own testing, we did some more research to
determine the scope of this issue.  With every other layer of the configuration
manager, there is a combined enable and disable setting, instead of having a
split setting.  As such, the scope of this issue was solely focused on the
command line.  Since we believe that users will disabling plugins more often
than enabling plugins, we decided that command line disables would have
priority over command line enables.

### Multiple Identifiers For The Same Rule Plugin

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

According to the documentation on [Rule md003](https://github.com/jackdewinter/pymarkdown/blob/main/docs/rules/rule_md003.md),
the id for that rule is `md003` and it has one alias `heading-style-h1`.
This means that the `plugins.md003` configuration takes
precedence over the `plugins.heading-style-h1` configuration,
due to the rules specified above, regardless of its position in
the configuration file. Also, if instead
the `"enabled" : false` configuration value was `"enabled" : true`, the `plugins.heading-style-h1.style`
configuration value is set but it will not be used by the configuration manager.
For that configuration value to be used, the `plugins.md003` configuration
hierarchy must be removed completely as the entire hierarchy
has precedence, not just individual configuration properties.

### Command Line Vs Configuration File

One question that comes up repeatedly, for PyMarkdown or for other projects,
is whether to use a configuration file or command line arguments. And that answer
largely relies on your context.  

From our experience, there are typically five reasons for using configuration files
over command line arguments:

- conciseness: you prefer to keep any configuration values in a single file for
  that application
- reusability: you want to reuse those values in other locations, such as scripts
- simplicity: you want to do more complicated configuration without specifying "extra"
  command line options
- single responsibility: you only want pre-commit hook configuration in the file,
  everything else goes elsewhere
- catch-all: because... personal taste

If you are only leveraging PyMarkdown from one part of your project and are not executing
it from anywhere else, the above reasons either may not apply or may not be
as impactful to your decision.  There may also be other reasons
not listed here, such as team guidelines, which sway the decision one way or the
other. It really does come down to a team choice.

For our team, we typically
prefer to have our configuration items in their own specific configuration file.
The main reasons
for this are reusability and readability.  Our team's guidelines are to have one
configuration file per tool (where possible) and to be as precise about the configuration
items as possible.  Therefore, we use a JSON configuration file that we specifically
invoke from the command line each time.  For us, that pedantic act of specifying
a configuration file explicitly works for us, and we can easily explain what
our rationale is to each other.

Following out of that decision is our use of the command line for new configuration
items.  The best way to explain it is that we view our configuration file as
"well-tested cold storage" and the command line as a test platform.  If we see
configuration on a command line, we know that it is something being tested, not
something that has been battle tested.  But those are our guidelines, that work
for our team.

This is a decision that you need to make with your project team.  And
when you make the decisions, please document them somewhere with enough information
so that you can revisit the decision later.  Team members and
reasons change over time, so it is good to remember the reasons behind your
decision.
