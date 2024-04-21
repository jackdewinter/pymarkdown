# Advanced Configuration

This document will be the new home of the content currently located
[here](https://github.com/jackdewinter/pymarkdown/blob/main/docs/advanced_configuration.md).

## Configuration Files

## Default Configuration Files

## Different Types

Other things that will be added:

- config files
- default config files
- config orderings
- set configuration, globally, per extension, and per rule
- strict mode

- [Command Line Settings](https://github.com/jackdewinter/pymarkdown/blob/main/docs/advanced_configuration.md#general-command-line-settings)
- [Configuration File Settings](https://github.com/jackdewinter/pymarkdown/blob/main/docs/advanced_configuration.md#command-line-configuration-file)
- [Available Configuration Values](https://github.com/jackdewinter/pymarkdown/blob/main/docs/advanced_configuration.md#available-configuration-values)

### Command Line Configuration

### Command Line Arguments Vs Configuration File

The one question that comes up again and again, for PyMarkdown or for other projects,
is whether to use a configuration file or command line arguments. And that answer
largely relies on your context.  

From our experience, there are typically five reasons for not using command line
arguments for setting up your PyMarkdown hook in Pre-Commit:

- conciseness: you prefer to keep any configuration values in a single file for
  that application
- reusability: you want to reuse those values in other locations, such as scripts
- simplicity: you want to do more complicated configuration without specifying "extra"
  command line options
- single responsibility: you only want pre-commit hook configuration in the file,
  everything else goes elsewhere
- catch-all: because... personal taste

If you are only leveraging the Pre-Commit hook for PyMarkdown and are not executing
PyMarkdown from anywhere else in your project, many of the above reasons either may
not apply or may not be as impactful to your decison.  There may also be other reasons
not listed here, such as team guidelines, that sway the decision one way or the other.

It really does come down to a team choice.  

### Enabling or Disabling Rules

As rules can be enabled or disabled on the command line, rules can also be enabled
or disabled in the `.pre-commit-config.yaml` file.

```yaml
repos:
    - repo: https://github.com/jackdewinter/pymarkdown
      rev: main
      hooks:
          - id: pymarkdown
            args:
                - -d
                - MD041,md013
                - scan
```

Note that if presenting the arguments on a single line and there are multiple rules
that are being enabled or disabled, the commma separated list must be enclosed in
quotes.  The quote characters allow Pre-Commit to understand that the comma inside
of the quotes is part of the data, not a character separating the data.

```yaml
repos:
    - repo: https://github.com/jackdewinter/pymarkdown
      rev: main
      hooks:
          - id: pymarkdown
            args: [-d, "MD041,MD013", scan ]
```
