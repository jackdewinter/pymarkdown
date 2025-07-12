# API Support

While most users interact with the PyMarkdown application via the command line,
we understand that some of our users want to use a application programming interface
(API).  For these users, our team provides a Python API with an auto-generated
[API Listing](api/pymarkdownapi.md) of that API.  Our team created this API Support
document to augment the API Listing, providing easy-to-follow examples that
illustrate how our team envisions the use of those APIs.

Currently, only the equivalent of the `scan`, `scan --list`, and `fix` commands
are presented through this API, as they were the ones most requested. If you need
any other APIs to expose the command line functionality of PyMarkdown, please
follow our [feature request process](./usual.md).

## Introduction

The PyMarkdown API is meant to be an abstraction of the PyMarkdown command line,
allowing the use of PyMarkdown from within another application.  Currently
at interface version `1`, the API seeks to provide a useful interface
to the PyMarkdown application with low friction.

## Looking For More Examples?

In addition to this document, a useful source for code snippets are
the various test files under the project's
[`test/api` directory](https://github.com/jackdewinter/pymarkdown/tree/main/test/api).
As much as
possible, our team strived to connect the API test function with any corresponding
test function for the same scenario in the non-API part of the project.  Our
belief is that those connections will help any readers of those tests in their
understanding of the APIs and how they map to their command line equivalents.

## A Quick Word on Executing These Snippets in VSCode

Our team are usually big fans of VSCode and its Terminal window, but that is not
the case with these examples. Due to our frequent use of the Terminal window to
develop and test code snippets, we are aware that the Terminal window caches any
imported packages.  Thus, if you are importing the PyMarkdown package and want to
evaluate an updated version of PyMarkdown, you will likely have to restart
VSCode.  By restarting VSCode, you will clear the package cache and allow the
updated version of PyMarkdown to be installed properly.

## API Basics

The basic code to perform scanning on a given markdown path is as follows:

```python
from pymarkdown.api import PyMarkdownApi

source_path = "some-manner-of-path"
PyMarkdownApi().scan_path(source_path)
```

We tried to keep the starting scenario as simplistic as possible, so that code
snippet is the minimum code needed to execute the scanner on a given path.  In
this case, the
path is specified as `some-manner-of-path` which is either the path to a
file or to a directory.  Note that if `some-manner-of-path` specifies a file name,
it will be rejected because the filename does not end with `.md`.  But this function
can also take globbed arguments, such as `*.md` to specify all the Markdown files
in the current directory.

To keep the API easy to use, we focused on supplying the simple, bare-bones functionality
that we expect our users to utilize most of the time.  As such, we designed the
`PyMarkdownApi` object for quick instantiation, and a `scan_path` function that
is clearly named.  We hope that this will reduce the friction encountered
when integrating a new package into an application.

While the base invocation of the `scan_path` function is simple, there are two
normal concepts that are not yet represented in our examples. These concepts are
the collection of information and the handling of errors. The second concept
is critically important as the scanning of the non-existent path `some-manner-of-path`
will undoubtedly run into problems. Specifically, if you execute the above code
example as is, you will see output text that looks like:

```text
WARNING:pymarkdown.main:Provided path 'some-manner-of-path' does not exist.
WARNING:pymarkdown.main:No matching files found.
Traceback (most recent call last):
  File "bob.py", line 4, in <module>
    PyMarkdownApi().scan_path(source_path)
  File "C:\enlistments\pymarkdown\pymarkdown\api.py", line 297, in scan_path
    return self.__handle_scan_results(return_code, this_presentation)
  File "C:\enlistments\pymarkdown\pymarkdown\api.py", line 306, in __handle_scan_results
    self.__generate_exception(this_presentation)
  File "C:\enlistments\pymarkdown\pymarkdown\api.py", line 349, in __generate_exception
    raise PyMarkdownApiNoFilesFoundException(second_last_error_text)
pymarkdown.api.PyMarkdownApiNoFilesFoundException: Provided path 'some-manner-of-path' does not exist.
```

Note that the first two lines are reporting log messages from the PyMarkdown application.
As most logging defaults to a log level of `Warning` and output to the console,
seeing two lines of log messages with a log level of `WARNING` is not unexpected.
However, the remaining lines talking about an exception that was raised are messy
and do not help the reader any.

To address that problem, we need to talk about catching exceptions.

## PyMarkdown API Exceptions

When something goes wrong when executing a function of the `PyMarkdownApi` object,
the API raises a `PyMarkdownApiException` exception.  To make the previous example
handle those exceptions, we must change it slightly to add the needed exception
support:

```python
from pymarkdown.api import PyMarkdownApi, PyMarkdownApiException

source_path = "some-manner-of-path"
try:
    PyMarkdownApi().scan_path(source_path)
except PyMarkdownApiException:
    pass
```

By including a try/except block around the `scan_path` API call, the example now
handles the exception.  Based on the changes,  the output from executing the above
example is now:

```text
WARNING:pymarkdown.main:Provided path 'some-manner-of-path' does not exist.
WARNING:pymarkdown.main:No matching files found.
```

This is a slight improvement, as the PyMarkdownApi object's various [log calls](./api/pymarkdownapi.md)
can control whether the above text is emitted or sent to a file.  However, a better
way to deal with the exceptions is to put code in place of the `pass` statement.
Thus, a simple handling of exceptions with that example is:

```python
import sys
from pymarkdown.api import PyMarkdownApi, PyMarkdownApiException

source_path = "some-manner-of-path"
try:
    scan_result = PyMarkdownApi().log_error_and_above().scan_path(source_path)
except PyMarkdownApiException as this_exception:
    print(f"API Exception: {this_exception}", file=sys.stderr)
    sys.exit(1)
```

The reason that this example is better than the last example is that it is performing
a specific action to deal with the raised exception.  That action is to print the
information to stderr and exit the program, a typical approach to handling the exception
within a simple Python script.  If the API is being called
by a more complex application, that exception handling must be replaced with
something in keeping with the rest of the calling application.

## Scan Results

Having dealt with the basics and error handling, it is time to leverage what
you have learned so far to handle the results of the scans!  If you are not
familiar with the terminology we will use, refer to our [User Guide](./user-guide.md)
for a quick refresher.

### Positive Results

This might sound counter-intuitive, but a set of positive results from PyMarkdown
are results where no failures are reported.  Put succinctly, if PyMarkdown scans
the required Markdown documents and does not find any failures, the scan is
a success.

To demonstrate this, create a new Markdown file named `example.md` in the local
directory and set its content to the following Markdown:

```MArkdown
# This is a title

This is a document

```

We realize that this is a trivial example, but it is a good place to start. When
creating the file, please ensure that the file ends with a single newline. This
is because [Rule Md047](./plugins/rule_md047.md) exists to ensure that
every Markdown file ends with a single newline character.  Therefore, if the `example.md`
file does not terminate with a single newline, this will not generate a positive
result.

To make sure we can see that positive result, you need to modify the example from
above with two print statements at the end:

```python
import sys
from pymarkdown.api import PyMarkdownApi, PyMarkdownApiException

source_path = "example.md"
try:
    scan_result = PyMarkdownApi().log_error_and_above().scan_path(source_path)
except PyMarkdownApiException as this_exception:
    print(f"API Exception: {this_exception}", file=sys.stderr)
    sys.exit(1)

print(scan_result.scan_failures)
print(scan_result.pragma_errors)
```

These print statements will print the lists that are returned from the
`scan_path` function.  If everything is working properly, those two print
statements generate the following output:

```text
[]
[]
```

That is because both the `scan_failures` property and the `pragma_errors` property
of the returned `PyMarkdownScanPathResult` instance are clear of any failures.
This means that the application did not find any issues with the `example.md` file,
indicating a positive scan.

### Scan Failures

Now that we have a positive scan of a file, try and make these modifications to the
`example.md` file that you created in the last section:

- remove the last line of the document, making `This is a document` the last line
- after the text `This is a document`, insert a single space character
- change the text `# This is a title` to `## This almost a title`
- change the text `# This is a title` to `This is not a title`
- remove the blank line between `# This is a title` and `This is a document`

Each of these changes creates a Markdown document that is acceptable to Markdown
parsers, but Markdown which breaks at least one of PyMarkdown's rules.
Therefore, applying any of the changes results in a negative scan where at least
one failure is reported.

Using the first suggestion as an example, go to the `example.md` file and add multiple
newlines at the end of the document.  As described in the [Positive Results](#positive-results)
section of this document, doing so causes [Rule Md047](./plugins/rule_md047.md)
to trigger, generating a failure.  Therefore, when you execute the code example
from the last section with the modified `example.md` file, you will see the following
output (newlines added for readability):

```text
[PyMarkdownScanFailure(scan_file='example.md', line_number=3, column_number=18,
rule_id='MD047', rule_name='single-trailing-newline',
rule_description='Each file should end with a single newline character.',
extra_error_information='')]
[]
```

While this form of output is rather crude, it gives us a good amount of information.
The biggest piece of information is that the scanned Markdown file raised one issue
when scanned by PyMarkdown. By looking at the output along with the documentation
for the `PyMarkdownScanFailure` object in the [API document](./api/pymarkdownapi.md),
we can infer the following:

- `scan_file`: the issue was found in the file `example.md`
- `line_number` and `column_number`: the issue was one line 3, column 18
- `rule_id` and `rule_name`: the issue has ids `MD047` and `single-trailing-newline`
- `rule_description`: this issue was raised as it expected a single newline character
  at the end of the file
- `extra_error_information`: no extra information was provided

#### The Extra Error Information Field

The object `PyMarkdownScanFailure` contains the field `extra_error_information`
which is empty in the previous example.  With Rule Md047, either the file ends
with a single newline character or it does not.  There is no benefit to providing
the user with any extra information regarding that failure.

For other failures, having that extra field to relay information about the failure
is especially important. Consider the following example and [Rule Md007](./plugins/rule_md007.md).

```Markdown
# This is a test

 * this is level 1

```

Rule Md007 triggers if there is unneeded space before a list start.  Examining this
example manually, it is clear that the space before the list start character `*`
is not needed. When we place the above Markdown document in a file called `extra.md`
and scan it using our code snippet, the following text is output:

```text
[PyMarkdownScanFailure(scan_file='extra.md',line_number=3, column_number=2,
rule_id='MD007', rule_name='ul-indent',
rule_description='Unordered list indentation',
extra_error_information=' [Expected: 0, Actual=1]')]
[]
```

When Rule Md007 triggers a failure, the reason behind the failure may not be clearly
understood.  The extra information `[Expected: 0, Actual=1]` lets the user know
that 0 space characters were expected, but 1 space character was found. While it
may not be needed with this simplistic example, consider an example with multiple
levels of lists and block quotes.  In those examples, any extra information provided
to the user can help them understand why one of the rules triggered.

### Pragma Failures

In our [user guide](./user-guide.md#pragma-extension) document, we talked about Pragmas
and how they allow users to disable failures within a Markdown document. For
example, based on the failure information for the last section, to properly
suppress the failure in that example, the example needs to be changed
to the following:

```Markdown
# This is a test

x<!--- pyml disable-next-line ul-indent--->
 * this is level 1

```

However, any properly written tool deals with its own error cases.  That is where
the handling of pragma failures comes in.  Once the `<-- pyml` text or `<--- pyml`
text is detected, the pragma is extracted from the token stream for later processing.
When the document is finished, the pragmas are then parsed to see if they are validly
formed.  PyMarkdown considers any invalidly formed failures to be failures in the
same class as scan failures.  That is to say that the failures are reported, but
do not stop the parsing and linting of the Markdown files.

To see an example of such a failure, change the contents of `example.md` to the
following text and rescan the file:

```Markdown
# This is a test

x<!--- pyml disable-next-line invalid--->
 * this is level 1

```

When the file is scanned, the following results are reported:

```text
[PyMarkdownScanFailure(scan_file='example.md', line_number=4, column_number=2,
rule_id='MD007', rule_name='ul-indent', rule_description='Unordered list indentation',
extra_error_information=' [Expected: 0, Actual=1]')]
[PyMarkdownPragmaError(file_path='example.md', line_number=3,
pragma_error="Inline configuration command 'disable-next-line' unable to find a plugin with the id 'invalid'.")]
```

Because the pragma did not specify a valid rule to suppress, it correctly reports
that it was not able to find a plugin with the id `invalid`. The same type of
failure is generated with any case where the pragma format is not specifically
followed, or an invalid value is used.

## Other APIs

The bulk of the above sections refers to the `scan_path` function, as that is the
function used to scan Markdown files.  But the API has other functions that are
useful.

### fix_path

This function is like the `scan_path` function, except that it uses the powerful
PyMarkdown parser to determine if a fix can be applied to a scan failure and, if
so, fixes the scan failure.  Note that not all scan failures can be automatically
fixes, as mentioned in the [Fix Mode - Failure Correction](./user-guide.md#failure-correction-or-fix-mode)
documentation.

### scan_string

Instead of taking a path to one or more files to scan, the `scan_string` function
takes a single parameter which is a string to scan as a Markdown document.
Aside from that difference, the
rest of the functionality for that function is identical to the `scan_path` function.

### list_path

There are times with our team's testing of the PyMarkdown application where we want
to verify that PyMarkdown is scanning the right files. To that end, we constructed
the `list_path` function to be the equivalent of the `scan --list-files` command
line arguments for PyMarkdown. While this function (more completely documented under
[Advanced Scanning](./user-guide.md#advanced-scanning)) may not seem useful at
first glance, it has saved our development team's sanity on multiple occasions.
The `list_path` function performs no parsing of any Markdown documents, simply
returning an instance of the `PyMarkdownListPathResult` object holding the paths
of any files that are eligible to scan.

## Common APIs

These [other functions](./api/pymarkdownapi.md/#main-api) were added to provide support
for the function in the previous sections.

### Version

There are two APIs for determining version information relevant to the application,
both available from the `PyMarkdownApi` object. The `interface_version` value specifies
the version of the PyMarkdownApi object and is currently set to `1`.  The
`application_version` value specifies the version of the PyMarkdown application in
use and is equivalent to entering `pymarkdown version` on the command line.

### Logging

[Log control](./advanced_configuration.md/#logs) is available from the main `PyMarkdownApi`
object.  The `log` function is the equivalent of using the `--log-level` argument
on the command line. To provide a simpler approach, there are the `log_*_and above`
shortcut functions that specify the desired log level in their name.  For example,
the `log_info_and_above` function is equivalent to invoking `log("INFO")`.

The `log_to_file` function allows for the redirection of log information into a
file, the equivalent of the `--log-file` argument. Finally, the `enable_stack_trace`
function is the equivalent of the `--stack-trace` command line argument.

### General Configuration

The [General Command Line Setting](https://application-properties.readthedocs.io/en/latest/command-line/#general-command-line-settings)
command line arguments are available using the two `*_rule_by_identifier` functions.
The `disable_rule_by_identifier` function is the equivalent of the `--disable-rules`
argument, and the `enable_rule_by_identifier` function is the equivalent of the
`--enable-rules` argument.

### Specific Configuration

The [Specific Command Line Setting](https://application-properties.readthedocs.io/en/latest/command-line/#specific-command-line-settings)
command line arguments are available using the `set_property` and related functions.
Instead of asking the API user to understand the [Configuration Item Types](https://application-properties.readthedocs.io/en/latest/command-line/#configuration-item-types),
three helper functions are provided: `set_boolean_property`, `set_integer_property`,
and `set_string_property`.

### Configuration File

A [configuration file](https://application-properties.readthedocs.io/en/latest/command-line/#command-line-configuration-files)
can be specified by using the `configuration_file_path` function.  This is the equivalent
of using the `--config {file}` command line argument.

### Strict Configuration

[Strict configuration mode](https://application-properties.readthedocs.io/en/latest/command-line/#strict-configuration-mode)
can be enabled by calling the `enable_strict_configuration` function. This is the
equivalent of using the `--strict-config` command line argument.

### Other

The `add_plugin_path` function is the equivalent of the `--add-plugin` command line
argument.
