# Frequently Asked Questions

## Is Markdown Front-Matter supported?

Yes.  To enable and understand this behavior, please refer to our
documentation on [Front-Matter](./extensions/front-matter.md).

## Why are my configuration changes not working?

That is a large can of worms to attack in one document.  But from our own experience,
these issues usually falls into a handful of explanations.

- Typing errors.
    - Most common.
    - No really good way to find these other than double checking the configuration
      item name against the documentation.
- Not saving the new configuration changes.
    - This happens more times than we wish to admit.  Pays to double check before
      going to more extensive debuging measures.
- Not using `--strict-config` on the command line.
    - With strict mode enabled, if the configuration item's name is correct but the
      value type is not correct, PyMarkdown will error.  Otherwise, it will only
      error if there is no default value, and almost everything has values.
    - This catches problems with values that are the wrong type.
    - If specifying values on the command line or with a configuration file that
      does not natively support typing, need to provide type hints.
    - For more, [see this section](./advanced_configuration.md#configuration-item-types).

## I am using a `--set` command, but it is not working?

This issue is a bit more focused than the previous question. In this case,
it could have something to do with your shell and escape characters.
Check out [this section](./advanced_configuration.md#configuration-item-types)
for more information.
