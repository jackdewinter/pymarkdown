# Advanced Configuration

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

### Command Line Setting

### Configuration Setting

```
  --config CONFIGURATION_FILE, -c CONFIGURATION_FILE
                        path to the configuration file to use
- configuration file, format, etc
```

## XX

### Logging

log.file
log.level

  --stack-trace         if an error occurs, print out the stack trace for debug purposes
  --log-level {CRITICAL,ERROR,WARNING,INFO,DEBUG}
                        minimum level required to log messages
  --log-file LOG_FILE   destination file for log messages

- if debug of configuration, stack trace sets initial logging (config processing) to debug

### Adding A Plugin

  --add-plugin ADD_PLUGIN
                        path to a plugin containing a new rule to apply
adding a plugin

### Front Matter

front matter enabled.
extensions.front-matter.enabled

### Plugin Properties
plugins.{id}.enabled
plugins.{id}.properties

## Configuration

- need way of listing all plugins, info
- need way of listing all extensions
