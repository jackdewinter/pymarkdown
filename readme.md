# PyMarkdown

PyMarkdown is primarily a Markdown Linter.  To ensure that the Markdown
[linting](https://en.wikipedia.org/wiki/Lint_%28software%29)
is accomplished successfully, the rules engine that powers the linter
uses a Markdown parser that is both
[GitHub Flavored Markdown](https://github.github.com/gfm/)
compliant and
[CommonMark](https://spec.commonmark.org/)
compliant.  The rules provided in the base application can be easily extended
by writing new plugins and importing them into the rules engine through simple
configuration options.

## Installation

```text
pip install PyMarkdown
```

## Introduction

## Command Line

### Root Level

The command line help at the root level is as follows:

```text
usage: main.py [-h] [-e ENABLE_RULES] [-d DISABLE_RULES] [--add-plugin ADD_PLUGIN]
               [--config CONFIGURATION_FILE] [--stack-trace]
               [--log-level {CRITICAL,ERROR,WARNING,INFO,DEBUG}] [--log-file LOG_FILE]
               {plugins,scan,version} ...

Lint any found Markdown files.

positional arguments:
  {plugins,scan,version}
    plugins             plugin commands
    scan                scan the Markdown files in the specified paths
    version             version of the application

optional arguments:
  -h, --help            show this help message and exit
  -e ENABLE_RULES, --enable-rules ENABLE_RULES
                        comma separated list of rules to enable
  -d DISABLE_RULES, --disable-rules DISABLE_RULES
                        comma separated list of rules to disable
  --add-plugin ADD_PLUGIN
                        path to a plugin containing a new rule to apply
  --config CONFIGURATION_FILE, -c CONFIGURATION_FILE
                        path to the configuration file to use
  --stack-trace         if an error occurs, print out the stack trace for debug purposes
  --log-level {CRITICAL,ERROR,WARNING,INFO,DEBUG}
                        minimum level required to log messages
  --log-file LOG_FILE   destination file for log messages
```

This level of command includes three subcommands:

- [scan](dd)
  - the primary workflow for this application
- [plugins](dd)
  - a secondary workflow to provide information on plugins for rules
- [version](dd)
  - a secondary workflow to provide information on the current version of the application

#### Notes

- if debug of configuration, stack trace sets initial logging (config processing) to debug

### Scan

The command line help at the `scan` level is as follows:

```text
usage: main.py scan [-h] [-l] path [path ...]

positional arguments:
  path              one or more paths to scan for eligible Markdown files

optional arguments:
  -h, --help        show this help message and exit
  -l, --list-files  list the markdown files found and exit
```

### Plugins

The command line help at the `plugin` level is as follows:

```text
usage: main.py plugins [-h] {list,info} ...

positional arguments:
  {list,info}
    list       list the available plugins
    info       information of specific plugins

optional arguments:
  -h, --help   show this help message and exit
```

This level of command includes three subcommands:

- [list](dd)
  - a workflow to list every rule plugin that is registered with the application
- [info](dd)
  - a workflow to provide information on a single rule plugin

### List

The command line help at the `list` level is as follows:

```text
usage: main.py plugins list [-h] [list_filter]

positional arguments:
  list_filter  filter

optional arguments:
  -h, --help   show this help message and exit
```

### Info

The command line help at the `info` level is as follows:

```text
usage: main.py plugins info [-h] info_filter

positional arguments:
  info_filter  an id

optional arguments:
  -h, --help   show this help message and exit
```

### Version

This command emits a single line that show the version of the application.

## Configuration

log.file
log.level
plugins.{id}.enabled
plugins.{id}.properties
extensions.front-matter.enabled

plugin ordering: command line (disabled, enabled), config, default
others ordering: command line (if exposed), config, default

- need way of listing all plugins, info
- need way of listing all extensions

