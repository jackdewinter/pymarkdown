# Development Documentation

When updating our documentation in preparation for our 1.0.0 release, we decided
that we wanted to provide solid information on how to add your own customizations
to PyMarkdown.

## Architecture

As we want to make sure you have the option to understand the architecture of PyMarkdown,
we have plans to include a detailed document with that architecture. To make sure it has
the level of detail we believe is necessary, we are hoping to have that done by end of
Q3 2026. That document will lead into developing extensions to PyMarkdown and why it is
difficult.

## Developing Markdown Extensions

Extensions to the PyMarkdown parsing engine are difficult for two main reasons. The first
reason is that parsing a given element is usually tied in some way to every other element
that can be parsed. Can the extension element interupt a paragraph? Is it an element
that modifies inline text, or is it a leaf block or container block element? Is it a
multiline element like the Link Reference Definition, where you do not know that the
element is done until you process the next line? And even then, sometimes you have to
backtrack to get back to the real end to the element. Even simple seeming elements have
many rules that apply to itself and how it interacts with the other elements.

The other reason is the testing required. Inline elements required the least amount of
testing, followed by leaf block elements and then container block elements. To meet
the PyMarkdown standards for implementing a new extension, we expect one-hundred percent
line coverage for each extension, and as close to one-hundred percent scenario coverage
as possible. And those tests take lots of time and lots of data samples to get right.

In short, while we accept suggestions for other Markdown extensions, we do not advocate
creating your own extensions. However, creating your own Rule Plugins is a different matter.

## Developing Rule Plugins

PyMarkdown was designed from the ground up to allow Rule Plugins to be added dynamically
through the [`--add-plugin`](./user-guide.md/#-add-plugin-rule-plugins) command-line
argument. And there is a pivotal difference between Markdown Extensions and Rule Plugins
that allow this to happen: where in the process Rule Plugins are applied.

As noted above, adding a new Markdown Extension to PyMarkdown is a big endeavor. The main reason
for the large amount of effort is required is that extensions change the way that Markdown documents
are parsed. As an example, if you enable the [`markdown-tables`](./extensions/markdown-tables.md)
extension, PyMarkdown's parser is allowed to evaluate whether the Markdown tables elements
are present and valid. If that extension is not enabled, PyMarkdown just interprets it as
normal text.

Rule Plugins are different in that they are applied to the tokens produced by the parser through
PyMarkdown's rule engine. Unlike Markdown extensions, where enabling or disabling an extension
changes the produced tokens, Rule Plugins can be enabled or disabled without affecting the
produced tokens and even other Rule Plugins. Because of that distinction, Rule Plugins can
be created and tested in isolation from other parts of PyMarkdown, drastically reducing
the testing effort required to complete a custom Rule Plugin.

**NOTE:** To provide relatable information about these Rule Plugins, the following sections
will reference Rule Plugin `MD001` and its source code to provide practical information
on the topic being talked about.

## Rule Plugin Architecture

Each Rule Plugin is descended from the `RulePlugin` class imported from
`pymarkdown.plugin_manager.rule_plugin` module. That class is an abstract class
with only one abstract method: the `get_details` method.
This method is called first thing after the module is loaded to determine the
capabilities of the Rule Plugin.
The remaining methods
are used by either the "scan" workflow or the "fix" workflow to enact the tasks
needed from within those workflows.

Each Rule Plugin must be contained in a module whose file name is an algorirthmic
interpretation of the class name. Using `RuleMd001` as an example, the module for
that Rule Plugin is `pymarkdown\plugins\rule_md_001.py`. More precisely, the
class name is the result of taking the file name `rule_md_001.py`, removing the
extension (which is always `.py`), splitting the remaining string up by `_` characters
and captializing the first letter of each split, and then joining them back together again.
Following this pattern, `rule_md_001.py`
becomes `rule_md_001`, which becomes `["rule","md","001"]` and then `["Rule","Md","001"]`,
and finally `RuleMd001`.

### Rule Plugin Details

As noted above, the `get_details` method is the first method called for every Rule Plugin
that is successfully loaded. While some attributes in the returned `PluginDetailsV3` object
are purely decorative, such as the `plugin_description` field, other fields like the `plugin_id`
field and the `plugin_interface_version` field provide vital information about the Rule Plugin's
capabilities to PyMarkdown's rule engine. That information allows the rule engine to make the
best use of the Rule Plugin and its capabilities.

Here is a list of all the fields in the `PluginDetailsV3` class. The provide examples are from
Rule Plugin `Md001`, and some fields use the `...` sequence to denote they have been shortened for readability:

| Field                     | Type          | Description | Example |
| ---                       | ---           | --- | --- |
| plugin_id                 | str           | Unique identifier of the form `AAANNN` or `AANNN` | `"MD001"` |
| plugin_name               | str           | Unique human readable name(s) (letters, numbers, and `-`), comma-separated. | `"heading-increment,header-increment"` |
| plugin_description        |str            | One sentence description for the Rule Plugin. | `"Heading levels ... a time."` |
| plugin_enabled_by_default | bool          | Whether the Rule Plugin is enabled as default. | `True` |
| plugin_version            | str           | Semantic version of the Rule Plugin. | `"0.6.0"` |
| plugin_url                | Optional[str] | Optional URL to more exhaustive documentation on the Rule Plugin.| `"https://.../rule_md001.md"` |
| plugin_configuration      | Optional[str] | Optional comma-separated list of configuration values, for display only. | `"front_matter_title"` |
| plugin_interface_version  |int            | Interface version. For the `PluginDetailsV3` class, this is `3`. | `3` |
| plugin_supports_fix       | bool          | Whether the Rule Plugin supports the **autofix** capability. | `True` |
| plugin_fix_level          | int           | Relative ordering within the Fix workflow. | `1` |

The Rule Plugin `MD001` code for this method is as follows:

```python
def get_details(self) -> PluginDetailsV2:
    """
    Get the details for the plugin.
    """
    return PluginDetailsV3(
        plugin_name="heading-increment,header-increment",
        plugin_id="MD001",
        plugin_enabled_by_default=True,
        plugin_description="Heading levels should only increment by one level at a time.",
        plugin_version="0.6.0",
        plugin_url="https://pymarkdown.readthedocs.io/en/latest/plugins/rule_md001.md",
        plugin_configuration="front_matter_title",
        plugin_supports_fix=True,
    )
```

On its own, this information should paint a solid picture of what Rule Plugin `MD001` does: it looks for skipping heading
levels, is enabled by default, can be impacted by its `"front_matter_title"` configuration item, and supports the **autofix** capability.

Next, let's see how that information is used.

## Rule Plugin Lifecycle

The PyMarkdown rule engine is a simple engine with a relatively simple workflow. Its only tasks
are to load any available Rule Plugins and make sure they are configured properly, then running through
each token and line for every enabled Rule Plugin.

### Initialization

The initialization part of the workflow is simple. Once the Rule Plugin has been loaded successfully
and the `get_details` method has returned with the `PluginDetailsV3` object, the PyMarkdown rule engine then
makes a call to the Rule Plugin's `set_configuration_map` method to set the configuration for it to use.
Once the configuration has been established, the `initialize_from_config` is called to load any configuration
items needed during its lifetime.

#### Rule Plugin `MD001` Example

The Rule Plugin `MD001` code for this method is as follows:

```python
def initialize_from_config(self) -> None:
    """
    Event to allow the plugin to load configuration information.
    """
    self.__front_matter_title = (
        self.plugin_configuration.get_string_property_with_default(
            "front_matter_title", "title"
        )
    )
```

The Rule Plugin `MD001` lets the base class handle the processing of the `set_configuration_map`
method, as that is a simple method and easily reused between Rule Plugins. The object passed to that
method is an instance of the `MyApplicationPropertiesFacade` class. This class provides a simple
facade that only allows the Rule Plugin to access its own configuration items. This is aided by
the usual three configiruation methods from the `application_properties` package: `get_boolean_property`,
`get_integer_property`, and `get_string_property`. In addition, to make Rule Plugins more readable,
the `MyApplicationPropertiesFacade` class also offers `*_with_default` versions of those three methods
that make the default mandatory.

#### `query_config`

There are times where users want to verify that the configuration they specified for a Rule Plugin
is what that Rule Plugin is using.  This can be accomplished by entering the command-line `pymarkdown plugins info md001`, resulting in output that is similar to:

```text
  ITEM               DESCRIPTION

  Id                 md001
  Name(s)            heading-increment,header-increment
  Short Description  Heading levels should only increment by one level at a time.
  Description Url    https://pymarkdown.readthedocs.io/en/latest/plugins/rule_md001.md


  CONFIGURATION ITEM  TYPE    VALUE

  front_matter_title  string  "title"
```

This information is useful in that it shows the user some of the information that was returned by the `get_details`
method, as well as what the Rule Plugin reports as its current configuration. The first three lines can help the user
validate that the Rule Plugin that they are inquiring about is the correct one.  If provided, the `Description Url`
field gives them a web page that they can go to for more in-depth information. Finally, the report on what the
configuration items are and what they are currently set to helps the user validate that the configuration that they
intended for that Rule Plugin is being applied. That report is enabled by the `query_config` method.

##### Rule Plugin `MD001` Example

The Rule Plugin `MD001` code for this method is as follows:

```python
def query_config(self) -> List[QueryConfigItem]:
    """
    Query to find out the configuration that the rule is using.
    """
    return [QueryConfigItem("front_matter_title", self.__front_matter_title)]
```

Note that the information returned by this method provides for the simple reflection of the configuration
set up by the `initialize_from_config` method as shown above.

### Per Document Scanning

Unless a terminal exception is encountered, the workflow for scanning a single document is:

1. call the PyMarkdown parser to generate a list of tokens to represent that document
2. call the `starting_new_file` method for each enabled Rule Plugin
3. for each token generated in step 1, for each enabled Rule Plugin, call the `next_token` method with that token
4. for each line of the current document, for each enabled Rule Plugin, call the `next_line` method with the raw line
5. call the `completed_file` method for each enabled Rule Plugin

Why is the workflow organized like this for scaning documents? The first step, the second stop, and the last steps
make the most sense with respect to their ordering. The first step generates the tokens needed by the rule engine,
with the second step and last step creating the boundaries around the scanned document. Those boundaries are
important as it allows the Rule Plugin to initialize any class variables when the `starting_new_file` method
is called and it allows the Rule Plugin to cleanup any dangling logic when the `completed_file` method is called.

But what about step 3 and step 4 and why are they both called all the time? The answer is both context and
performance. Regardless of what is before and after each of steps 3 and step 4, they both need to be called
on each Markdown document. The trivial order to invoke these methods would seem to be: `starting_new_file`,
`next_token`, `completed_file`, `starting_new_file`, `next_line`, `completed_file`.

While the trivial order makes sense, it leaves out the ability for the `next_token` pass to provide guidance
to the `next_line` pass. This information is key to providing performant Rule Plugins that deal with
Markdown document lines, but need extra guidance on what leaf element is associated with that line.
A great example of this is Rule Plugins [`MD013`](./plugins/rule_md013.md). The code for
[Rule Plugin `MD013`](../../pymarkdown/plugins/rule_md_013.py) checks for line lengths limits being
exceeded, allowing for separate maximum line lengths for code blocks, headings, and tables. During the
`next_token` pass, the Rule Plugin keeps track of the leaf blocks in the document. Then, when the
`next_line` pass is running, it uses that list to understand if it needs to use the general maximum line
length, or one of the specialized ones.

Could this have been done using something like regular expressions? Its possible. But when we already
have an accurate parsing of the document in the list of tokens, it seems wasteful to not use that list
to help the Rule Plugins that needed it. With this workflow in place and some simple tracking, those
Rule Plugins can accurately know what leaf element belongs to a line in the document without any guesswork.

#### Rule Plugin `MD001` Example

The Rule Plugin `MD001` code for the `starting_new_file` method and the `next_token` method is as follows. Note
that this Rule Plugin does not need to perform any cleanup, so no `completed_file` method is defined.

```python
def starting_new_file(self) -> None:
    """
    Event that the a new file to be scanned is starting.
    """
    self.__last_heading_count = 0

def next_token(self, context: PluginScanContext, token: MarkdownToken) -> None:
    """
    Event that a new token is being processed.
    """
    hash_count = None
    if token.is_atx_heading or token.is_setext_heading:
        setext_token = cast(SetextHeadingMarkdownToken, token)
        hash_count = setext_token.hash_count
    elif token.is_front_matter:
        front_matter_token = cast(FrontMatterMarkdownToken, token)
        if self.__front_matter_title in front_matter_token.matter_map:
            hash_count = 1

    if hash_count:
        if self.__last_heading_count and (hash_count > self.__last_heading_count):
            delta = hash_count - self.__last_heading_count
            if delta > 1:
                if context.in_fix_mode:
                    hash_count = self.__last_heading_count + 1
                    self.register_fix_token_request(
                        context, token, "next_token", "hash_count", hash_count
                    )
                else:
                    extra_data = f"Expected: h{self.__last_heading_count + 1}; Actual: h{hash_count}"
                    self.report_next_token_error(
                        context, token, extra_error_information=extra_data
                    )
        self.__last_heading_count = hash_count
```

In the `starting_new_file` method, the Rule Plugin simply sets the `__last_heading_count` class variable
to `0`, allowing the calculation of whether a heading level was skipped to start at a known value. Then,
in the `next_token` method implementation, the Rule Plugin only pays attention to the three types of tokens
that can impact heading levels: a Front-Matter token, an Atx Heading token, and a SetExt Heading token.
If it extracted the `hash_count` value from one of those tokens, then it checks to see if the heading
level increased, and if so, further checks to see if the heading level increased by more than one.
When the Rule Plugin is used to scan the document and the heading level increased by more than one, the
`report_next_token_error` method is called to report the Rule Failure.

Note that if this was a line based rule, such as [Rule Plugin `MD013`](../../pymarkdown/plugins/rule_md_013.py),
the Rule Plugin would use the `report_next_line_error` method instead of the `report_next_token_error`
method to report the Rule Failure.

### Per Document Fixing

Fixing documents is both the same as scanning as well as being a bit different. The first part to
understand is that the difference between calling a Rule Plugin to scan a document and calling a Rule
Plugin to fix that same document is what to do if a Rule Plugin is triggered. As evident in the prior
example of `MD001`, the total difference between the two paths through the Rule Plugin are four lines
of code. If in scan mode, the `extra_data` variable is populated and used in the call to the
`report_next_token_error` method. If in fix mode, the `hash_count` variable is updated and used in the
call to the `register_fix_token_request` method.

It should be noted that a four line difference is not always the case. In some of the more complicated
Rule Plugins, the fixing portion of the Rule Plugin can require greater than half of the statements in
that Rule Plugin. It just depends on complexity.

The second part to understand about fixing documents is that it is an iterative process.

Our team's initial fix passes were cleanly fixing Markdown documents until we came to a scenarion
where two of our Rule Plugins that support the **autofix** capability wanted to change the same
token using the `register_fix_token_request` method. While that scenario involved changing two
separate attributes of the specific token, we wanted to handle the case where two separate Rule
plugins wanted to change the same attribute of the same token.

After a couple of failed attempts to create an algortithm that would fairly determine how two
Rule Plugins could change the same token, we decided on a more simplistic approach: the `plugin_fix_level`
field of the `PluginDetailsV2` class.
We realized that what we were attempting to do was to codify an ordering to follow that made
sense to us, but was hard to codify cleanly. Instead, by specifying an ordering to follow using
the `plugin_fix_level` value, we could specify which fixes should be done before other fixes. For example, trivial fixes such as
replacing tabs with spaces ([md009](http://127.0.0.1:8000/plugins/rule_md009/)) should be performed before more complicated fixes such as fixing multiple spaces after the block quote symbol ( [md027](http://127.0.0.1:8000/plugins/rule_md027/) ).

To further simplify the fixing process, making it iterative was a clear choice. With the `plugin_fix_level`
level established for each Rule Plugin, the rule engine was retooled to leverage the `plugin_fix_level` value
to prioritize fixing the documents into loops.

The first time the rule engine tries to fix a file, it does a normal scan using the five steps outlined in the
[Per Document Scanning](#per-document-scanning) section above to determine which Rule Failures
are being reported by that document.
The rule engine then uses the `plugin_fix_level` field for any Rule Plugins that reported a Rule Failure,
and builds a list of Rule PLugins that support the **autofix** capability and what their `plugin_fix_level`
value is. The rule engine that does a fix pass for only the minimum `plugin_fix_level` values reported,
following the same five steps as for scanning.

at this point, the rule engine checks to see if there are any more Rule Failures other than the ones
that it just fixed.  If so, it execute the same loop again, this time specifying that the minimum
`plugin_fix_level` must be one higher that it was during the previous pass. This...

In the end, does the fix workflow perform extra repetitions to fix the document? It depends on who you
ask. For our team, the question always came back to "what is the worst case scenario, and can the fixing
workflow handle it?". As we feel that this implementation, while it has multiple full loops through the
document, handles our worst case scenario properly. As such, we believe this workflow is just the right fit.

## Implementing A Custom Rule Plugin

With that information digested, we can go on to the creation of a custom Rule Plugin. To provide
a concrete example, this documentation will walk through the process of creating the Rule Plugin
`PMD001`

### Step 1: Define the Rule Behind the Plugin

The first step in creating a Rule Plguin is to clearly define the rule that the Rule Plugin will
implement. For the rule behind `PMD001`, we are going to create an optional custom Rule Plugin
that will allow us to specify attributes to use along with the Fenced Code Block Markdown element.
The main purpose of this Rule Plugin is to allow PyMarkdown's normal linting script to ensure that
each Fenced Code Block used in the `./newdocs/src` directory is properly annotated.

To be clear, the page that you are reading right now was generated by MkDocs after being
written in Markdown. To generate the example in the [Rule Plugin Details](#rule-plugin-details) section above,
the following Fenced Code Block element was used (with `...` used to omit lines to make it more concise):

````text
```python
def get_details(self) -> PluginDetailsV2:
...
```
````

Using MkDocs to generate the page you are reading presented us with some options regarding decorations
for the rendered code block. The first one that we like to use is the `title` attribute to ensure that
each code block has a recognizable title.  This takes the form of `title="<title name>"` and is added
after the code block's lnaguage is specified. Similarly, using the text `linenums="<starting number>"`
with a `starting number` greater than `0` will display line numbers to the left of the rendered code block.

If we add those two attributes after the code block's language, like so:

````text
```python title="get_details example" linenums="1"
def get_details(self) -> PluginDetailsV2:
..
```
````

then we get a code block that displays like this:

```python title="get_details example" linenums="1"
def get_details(self) -> PluginDetailsV2:
..
```

The Rule Plugin that we will create will blah blah.

Note that as this Rule Plugin is specifically for the PyMarkdown project and scanning its own `./newdocs/src`
directory, we can be a bit more sloppy with the formats, as they are essentially for private use.

### Step 2: Plan The Configuration

For the configuration of this Rule Plugin there are X things to consider. The first thing is how to specify
both values in a configuration item's string. While it is a bit kludgey, the easiest format is to take a
simple string list approach, separating individual items by a comma. Then within each item, we will specify
the different bits of information as `language;<0-1 linenums>;<title regular expression>`, with missing items
defaulting to `0` for `linenums` and `.*` for `title regular expression`.

The second thing to consider is what to do if a specified language is not present in the configuration.
[tbd throw rule failure]

### Step 3: Plan The Scanning Workflow

Unlike other Rule Plugins that require tracking of multiple tokens to determine if a given
Rule Plugin should be triggered, this 

### Step 4: Decide If the Rule Plugin Supports **autofix**

[tbd]

### Step 5: Write The Easy Stuff First

As detailed above, the two things

```python
"""
Module to implement a custom Rule Plugin for required attributes on Fenced Code Blocks.
"""
from pymarkdown.plugin_manager.plugin_details import PluginDetailsV2, PluginDetailsV3
from pymarkdown.plugin_manager.rule_plugin import RulePlugin

class RulePmd001(RulePlugin):
    """
    Class to implement a custom Rule Plugin for required attributes on Fenced Code Blocks.
    """

    def __init__(self) -> None:
        """
        Initialize an instance of the RuleMd001 class.
        """

    def get_details(self) -> PluginDetailsV2:
        """
        Get the details for the plugin.
        """
        return PluginDetailsV3(
            plugin_name="fenced-code-block-required-attributes",
            plugin_id="PMD001",
            plugin_enabled_by_default=True,
            plugin_description="Fenced code block must include required attributes.",
            plugin_version="0.0.1",
            plugin_configuration="front_matter_title",
        )
```

### Step 6: Add Configuration

change
```
from pymarkdown.plugin_manager.plugin_details import PluginDetailsV2, PluginDetailsV3
```
to
```
from typing import List
from pymarkdown.plugin_manager.plugin_details import PluginDetailsV2, PluginDetailsV3, QueryConfigItem
```

### Step 7: Add Scan

```
from pymarkdown.plugin_manager.plugin_scan_context import PluginScanContext
from pymarkdown.tokens.markdown_token import MarkdownToken
```

Other things that will be added:

- how to create a plugin
- how to add it




- Write basic scenario tests that describe when the rule should and should not
  trigger under normal conditions.
- Implement the Rule Plugin to satisfy those tests.
- Extend the tests to include container token types (Block Quotes and Lists),
  then update the implementation to handle those contexts as well.

Following this pattern keeps each rule focused and predictable, even as documents
become more complex.

Adding support for **fix** mode is more involved. To add a safe **autofix**, we:

- Define what a "safe" fix looks like for that rule, if applicable.
- Implement the fix so it only changes what is necessary.
- Test it against a wide range of documents to avoid breaking valid content.

This extra work is why new fix‑mode features can take longer to ship than the rules
themselves.

    def register_fix_token_request(
    def register_replace_tokens_request(
