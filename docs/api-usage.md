# API Usage

Introduced in the `0.9.12` release, the API is meant to supply an abstraction
for using the PyMarkdown application from within another application.  Currently
at interface version `1`, the API seeks to provide a useful interface
to the PyMarkdown application with low friction.

The [PyDoc3](https://pdoc3.github.io/pdoc/) application is used to generate
the [Markdown API documentation](./api) as part of the build process.  That given
application was chosen for its simplicity and its ability to generate decent
Markdown to properly document the PyMarkdown API.

Note that in addition to this document, a useful source for code snippets are
the various test files under the [test/api directory](../test/api/).  As much as
possible, we have strived to connect the API test function with any corresponding
test function for the same scenario in the non-API part of the project.  If you
believe we have missed a scenario test function or have ideas on how to improve
on our scenario tests, please let us know.

## Table Of Contents

- [A Quick Word on Executing These Snippets](#a-quick-word-on-executing-these-snippets)
- [Basics](#basics)
- [PyMarkdown API Exceptions](#pymarkdown-api-exceptions)
- [Positive Scan Results](#positive-scan-results)
- [Introducing Scan Failures](#introducing-scan-failures)
- [Introducing Pragma Failures](#introducing-pragma-failures)
- [Alternatives To Scan_Path](#alternatives-to-scan_path)
- [Future Documentation](#future-documentation)

## A Quick Word on Executing These Snippets

Usually, we are big fans of VSCode and its Terminal window, but with these examples
that is not the case.  As we tend to develop and test code, often with the help
of the
Terminal window, we are aware that the Terminal window caches any packages once
imported.  If you are using the Terminal window and change versions of
PyMarkdown or other packages to test out a new version, please keep in mind that
you will probably have to restart VSCode to clear the cache to allow for any new
packages to be applied properly.

## Basics

The basic code to perform scanning on a given markdown path is as follows:

```python
from pymarkdown.api import PyMarkdownApi

source_path = "some-manner-of-path"
PyMarkdownApi().scan_path(source_path)
```

We tried to keep the starting scenario as simplistic as possible, so that code
snippet is the minimum code needed to execute the scanner on a given path.  In
this case, the
path is specified as `some-manner-of-path` which could either be the path to a
file or to a directory.  Note that if `some-manner-of-path` specifies a file name,
it will be rejected because the filename does not end with `.md`.  But this function
can also take globbed arguments, such as `*.md` to specify all the Markdown files
in the current directory.

To make the API easy to use, we focused on supplying a simple, bare-bones function
that we expect our users to use most of the time.  As such, we believe that the
`PyMarkdownApi` object can be quickly instantiated and that the `scan_path` function
is clearly named.  We hope that this will allow developers to have an easy time
integrating API into their applications.

While the base invocation of the `scan_path` function is simple, there are two
things that are not yet represented in our examples. These are that we are not
collecting any
information about any issues with the Markdown text and that we are not handling
any errors that occurred when scanning the non-existent path `some-manner-of-path`.
In this specific scenario, if you execute that code snippet it as is, you will see
error text that looks like:

```text
WARNING:pymarkdown.main:Provided path 'some-manner-of-path' does not exist.
WARNING:pymarkdown.main:No matching files found.
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "<some-path>\pymarkdown\api.py", line 296, in scan_path
    return self.__handle_scan_results(return_code, this_presentation)
  File "<some-path>\pymarkdown\api.py", line 308, in __handle_scan_results
    self.__generate_exception(this_presentation)
  File "<some-path>\pymarkdown\api.py", line 351, in __generate_exception
    raise PyMarkdownApiNoFilesFoundException(second_last_error_text)
pymarkdown.api.PyMarkdownApiNoFilesFoundException: Provided path 'some-manner-of-path' does not exist.
```

Note that the first two lines are reporting log messages from the PyMarkdown application.
As most logging defaults to a log level of `Warning` and output to the console,
you should expect to see the two lines of log messages.  However, the remaining
lines talking about an exception that was raised are messy and do not help us
any.

To address that problem, we need to talk about catching exceptions.

## PyMarkdown API Exceptions

When something goes wrong with the `PyMarkdownApi` object, the API raises a
`PyMarkdownApiException` exception.  Therefore, to make the above sample handle
scan errors, we must change the sample slightly to add the needed support
for those exceptions:

```python
from pymarkdown.api import PyMarkdownApi, PyMarkdownApiException

source_path = "some-manner-of-path"
try:
    PyMarkdownApi().scan_path(source_path)
except PyMarkdownApiException:
    pass
```

By including a try/except block around the `scan_path` API call, the sample now
properly handles the exception and the output from executing the above code
snippet should now be:

```text
WARNING:pymarkdown.main:Provided path 'some-manner-of-path' does not exist.
WARNING:pymarkdown.main:No matching files found.
```

This looks better as we can control the log file using the [Python logging package](https://docs.python.org/3/library/logging.html)
with ease.  But as we are simply using a `pass` statement, we are not doing anything
useful with the exception.  A better handling of the exception would be:

```python
import sys
from pymarkdown.api import PyMarkdownApi, PyMarkdownApiException

source_path = "some-manner-of-path"
try:
    PyMarkdownApi().scan_path(source_path)
except PyMarkdownApiException as this_exception:
    print(f"API Exception: {this_exception}", file=sys.stderr)
    sys.exit(1)
```

The reason that this example is better than the last one is that it is doing
something specific with the raised error.  That action is to print the information
to stdout and exit the program, which is a typical approach to handling the
error when contained within a simple Python script.  If the API is being called
by a more complex application, that exception handling should be replaced with
something in keeping with the rest of the calling application.

## Positive Scan Results

This is the point where all this planning and examples for the API starts to pay
off!  Before continuing any further, we must write a trivial Markdown example
that should easily pass PyMarkdown's inspection.  Create a new file called `sample.md`
in the local directory and set its content to the following Markdown:

```MArkdown
# This is a title

This is a document

```

When copying the content into the `sample.md` file, please make sure that the new
file concludes with a single newline.  Once that is done, execute the following
code snippet:

```python
import sys
from pymarkdown.api import PyMarkdownApi, PyMarkdownApiException

source_path = "sample.md"
try:
    scan_result = PyMarkdownApi().scan_path(source_path)
except PyMarkdownApiException as this_exception:
    print(f"API Exception: {this_exception}", file=sys.stderr)
    sys.exit(1)

print(scan_result.scan_failures)
print(scan_result.pragma_errors)
```

If everything is working properly, you should see the following output:

```text
[]
[]
```

That is because both the `scan_failures` property and the `pragma_errors` property
of the returned `PyMarkdownScanPathResult` instance are clear of any failures.  This means
that the application could not find any issues with the `sample.md` file.

## Introducing Scan Failures

Now that we have a clean scan of a file, try and make these modifications to the
`sample.md` file that you created in the last section:

- remove the last line of the document, making `This is a document` the last line
- after the text `This is a document`, insert a single space character
- change the text `# This is a title` to `## This almost a title`
- change the text `# This is a title` to `This is not a title`
- remove the blank line between `# This is a title` and `This is a document`

In each of these cases, the resultant modifications produce acceptable Markdown
for parsers, but Markdown which breaks one of the rules of PyMarkdown.  Using the
first suggested modification as an example, executing the code snippet will produce
the following output:

```text
[PyMarkdownScanFailure(scan_file='sample.md', line_number=3, column_number=18,
rule_id='MD047', rule_name='single-trailing-newline',
rule_description='Each file should end with a single newline character.',
extra_error_information='')]
[]
```

While the output is rather crude, it gives us a good amount of information.  The
big information is that the Markdown snippet raises one issue when scanned by
PyMarkdown. By looking at the output along with the documentation on the `PyMarkdownScanFailure`
object in the [API document](./api.md), we can deduce the following:

- `scan_file`: the issue was found in the file `sample.md`
- `line_number` and `column_number`: the issue was one line 3, column 18
- `rule_id` and `rule_name`: the issue has ids `MD047` and `single-trailing-newline`
- `rule_description`: this issue was raised as it expected a single newline character
  at the end of the file
- `extra_error_information`: no extra information was provided

For a good example that includes the `extra_error_information` field, reset the first
modification, apply the second modification, and rescan the file.  The results
should be:

```text
[PyMarkdownScanFailure(scan_file='sample.md', line_number=3, column_number=19,
rule_id='MD009', rule_name='no-trailing-spaces', rule_description='Trailing spaces',
extra_error_information=' [Expected: 0 or 2; Actual: 1]')]
[]
```

This reported issue looks like the earlier issue, but the `extra_error_information`
field now holds the information `[Expected: 0 or 2; Actual: 1]`.  By reading the issue
and looking at the `sample.md` file, it is reasonable to assume that rule id `MD009`
(with name `no-trailing-spaces`) expects each line to end with `0` space characters
or `2` space characters.  As stated by the issue, it encountered `1` trailing space
character, so it triggered the failure.

With simple Python programming, a developer using the PyMarkdown API can create
their own handling of the `PyMarkdownScanFailure` instances, customized to their
own needs.

## Introducing Pragma Failures

Based on Wikipedia, which had the most comprehensive information on pragmas, a
[pragma](https://en.wikipedia.org/wiki/Directive_(programming)) is "a language
construct that specifies how a... translator should process its input."  For the
PyMarkdown project [pragmas](./extensions/pragmas.md) allow for the suppression
of rules being triggered by PyMarkdown itself.

Reusing the `sample.md` file from the last section, if we change it to the following
text:

```MArkdown
This is a title

```

produces the following output:

```text
[PyMarkdownScanFailure(scan_file='sample.md', line_number=1, column_number=1,
rule_id='MD041', rule_name='first-line-heading,first-line-h1',
rule_description='First line in file should be a top level heading', extra_error_information='')]
[]
```

If we do not want to suppress this failure for every reporting of this issue, a
pragma can be added to an individual file to just disable that one instance of
the failure being reported.  To fix up the above text snippet, we would change
that snippet to:

```MArkdown
<!--- pyml disable-next-line first-line-heading-->
This is a title

```

which will result in the PyMarkdown API returning no scan failures and no pragma
failures.

But, as with any tool, there are error cases.  That is where the handling of pragma
failures comes in.  Once the `<-- pyml` text or `<--- pyml` text is detected, the
pragma is extracted from the token stream for later processing.  When the document
is finished, the pragmas are parsed to see if they are validly formed and specify
that the reporting of a scan failure should be ignored.  PyMarkdown considers any
invalidly formed failures to be failures in the same class as scan failures.  That
is to say that the failures are reported, but do not stop the parsing and linting
of the Markdown files.

To see an example of such a failure, change the contents of `sample.md` to the
following text and rescan the file:

```MArkdown
<!--- pyml disable-next-line invalid-->
This is a title

```

When the file is scanned, the following results should be reported:

```text
[PyMarkdownScanFailure(scan_file='sample.md', line_number=2, column_number=1,
rule_id='MD041', rule_name='first-line-heading,first-line-h1',
rule_description='First line in file should be a top level heading', extra_error_information='')]
[PyMarkdownPragmaError(file_path='sample.md', line_number=1,
pragma_error="Inline configuration command 'disable-next-line' specified a plugin with a blank id.")]
```

Because the pragma was not constructed properly, it correctly reported that a blank
plugin id was parsed.  Furthermore, as the pragma was not properly constructed, it
did not suppress rule `MD041` from reporting a failure and the failure was therefore
reported.

## Alternatives To Scan_Path

The above sections all refer to the `scan_path` function that is used to scan one
or more paths that exist within the operating system.  As some of our own future
scenarios include being able to scan an in-memory string object, we added support
for that usage with the `scan_string` function.

The `scan_string` function takes a single parameter is the actual Markdown to scan
instead of a path to one or more files to scan.  Aside from that difference, the
rest of the functionality for that function is identical to the `scan_path` function.

In addition to the `scan_string` function, there are certain times during debugging
where we want to verify that PyMarkdown is scanning the files that we believe we
specified in the path argument.  To that end, we constructed the `list_path` function
to be essentially equivalent to the `scan --list-files` arguments for PyMarkdown.
While this function (more completely documented under [List Files To Scan](./advanced_scanning.md#test-it-out))
may not seem useful at first glance, it has saved us time during debugging sessions
on more than one occasion.  As no parsing of any found Markdown documents occurs,
the `list_path` function returns an instance of the `PyMarkdownListPathResult`
object that only holds the paths of any files that are eligible to scan.

## Future Documentation

We had planned to complete the documentation for the remaining functions,
but we were eager to get the basic API and documentation out so our users could start
using the API.  The majority of our API mirrors functionality that is available on the
command line, and hopefully does not need much explanation (yet).

- version APIs for the `PyMarkdownApi` object
  - `application_version` is equivalent to `pymarkdown version`
  - `interface_version` is new and is currently `1`

- [Advanced Configuration - Configuration](./advanced_configuration.md#configuration)
  - `configuration_file_path` is the equivalent of the `--config {file}` argument
  - `enable_strict_configuration` is the equivalent of the `--strict-config` argument
    and is more thoroughly covered in [Specifying Strict Configuration Mode](./advanced_configuration.md#specifying-strict-configuration-mode)
  - `set_property` is the equivalent of the `--set {key}={value}` argument
    - `set_boolean_property`, `set_integer_property`, and `set_string_property`
      are functions that automatically take care of translating these types of
      properties according to their [Configuration Property Types](./advanced_configuration.md#specifying-configuration-property-types)
- [Advanced Configuration - Logs](./advanced_configuration.md#logs)
  - `log` is the equivalent of the `--log-level` argument
    - `log_*_and above` are shortcuts to using the `log` function, with the log-level
      already in place
      - i.e. `log_info_and_above` is equivalent to `log("INFO")`
  - `log_to_file` is the equivalent of the `--log-file` argument
  - `enable_stack_trace` is the equivalent of the `--stack-trace` argument
- [Advanced Configuration - Plugins](./advanced_configuration.md#plugins)
  - `add_plugin_path` is the equivalent of the `--add-plugin` argument
  - `disable_rule_by_identifier` is the equivalent of the `--disable-rules` argument
  - `enable_rule_by_identifier` is the equivalent of the `--enable-rules` argument
