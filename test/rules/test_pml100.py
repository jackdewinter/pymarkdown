"""
Module to provide tests related to the PML100 rule.
"""

from dataclasses import dataclass
from test.markdown_scanner import MarkdownScanner
from test.rules.utils import execute_query_configuration_test, pluginQueryConfigTest
from test.utils import assert_if_strings_different
from typing import Any, List

import pytest


@dataclass
class Pml100Test:
    """
    TBD
    """

    name: str
    args: List[str]
    stdin: str
    expected_stdout: str
    expected_stderr: str = ""
    expected_return_code: int = 1


@dataclass
class ErrorPml100Test:
    """
    TBD
    """

    name: str
    args: List[str]
    expected_stderr: str


pml100Tests = [
    Pml100Test(
        "normal",
        [],
        """<something>
  <!-- some script stuff -->
</something>
""",
        "",
        "",
        0,
    ),
    Pml100Test(
        "Disallowed HTML Start",
        ["enabled=$!True"],
        """<script>
  <!-- some script stuff -->
</script>
""",
        "stdin:1:1: PML100: Disallowed HTML [Tag Name: script] (disallowed-html)",
    ),
    Pml100Test(
        "Disallowed HTML Mid",
        ["enabled=$!True"],
        """<html>
  <script>
    <!-- some script stuff -->
  </script>
</html>
""",
        "stdin:2:3: PML100: Disallowed HTML [Tag Name: script] (disallowed-html)",
    ),
    Pml100Test(
        "Disallowed HTML Mid w/ attributes",
        ["enabled=$!True"],
        """<html>
  <script src=./foo.js>
    <!-- some script stuff -->
  </script>
</html>
""",
        "stdin:2:3: PML100: Disallowed HTML [Tag Name: script] (disallowed-html)",
    ),
    Pml100Test(
        "Disallowed HTML Mid w/ self-close",
        ["enabled=$!True"],
        """<html>
  <script/>
""",
        "stdin:2:3: PML100: Disallowed HTML [Tag Name: script] (disallowed-html)",
    ),
    Pml100Test(
        "Disallowed HTML End",
        ["enabled=$!True"],
        """<html>
  <script>
""",
        "stdin:2:3: PML100: Disallowed HTML [Tag Name: script] (disallowed-html)",
    ),
    Pml100Test(
        "Now Allowed HTML Start",
        ["enabled=$!True", "change_tag_names=-script"],
        """<script>
  <!-- some script stuff -->
</script>
""",
        "",
        "",
        0,
    ),
    Pml100Test(
        "New Disallowed HTML Start",
        ["enabled=$!True", "change_tag_names=+something"],
        """<something>
  <!-- some script stuff -->
</something>
""",
        "stdin:1:1: PML100: Disallowed HTML [Tag Name: something] (disallowed-html)",
    ),
    Pml100Test(
        "Disallowed HTML Start in List",
        ["enabled=$!True"],
        """- <script>
    <!-- some script stuff -->
  </script>
""",
        "stdin:1:3: PML100: Disallowed HTML [Tag Name: script] (disallowed-html)",
    ),
    Pml100Test(
        "Disallowed HTML Start in New List",
        ["enabled=$!True"],
        """- first item
- <script>
    <!-- some script stuff -->
  </script>
""",
        "stdin:2:3: PML100: Disallowed HTML [Tag Name: script] (disallowed-html)",
    ),
    Pml100Test(
        "Disallowed HTML Mid in List",
        ["enabled=$!True"],
        """- <html>
    <script>
      <!-- some script stuff -->
    </script>
  </html>
""",
        "stdin:2:5: PML100: Disallowed HTML [Tag Name: script] (disallowed-html)",
    ),
    Pml100Test(
        "Disallowed HTML Mid in New List",
        ["enabled=$!True"],
        """- first item
- <html>
    <script>
      <!-- some script stuff -->
    </script>
  </html>
""",
        "stdin:3:5: PML100: Disallowed HTML [Tag Name: script] (disallowed-html)",
    ),
    # list tab
    Pml100Test(
        "Disallowed HTML Start in BQuote",
        ["enabled=$!True"],
        """> <script>
>   <!-- some script stuff -->
> </script>
""",
        "stdin:1:3: PML100: Disallowed HTML [Tag Name: script] (disallowed-html)",
    ),
    Pml100Test(
        "Disallowed HTML Start in BQuote after Para",
        ["enabled=$!True"],
        """> What follows is HTML.
> <script>
>   <!-- some script stuff -->
> </script>
""",
        "stdin:2:3: PML100: Disallowed HTML [Tag Name: script] (disallowed-html)",
    ),
    Pml100Test(
        "Disallowed HTML Mid in BQuote",
        ["enabled=$!True"],
        """> <html>
>   <script>
>     <!-- some script stuff -->
>   </script>
> </html>
""",
        "stdin:2:5: PML100: Disallowed HTML [Tag Name: script] (disallowed-html)",
    ),
    Pml100Test(
        "Disallowed HTML Mid in BQuote after Para",
        ["enabled=$!True"],
        """> What follows is HTML.
> <html>
>   <script>
>     <!-- some script stuff -->
>   </script>
> </html>
""",
        "stdin:3:5: PML100: Disallowed HTML [Tag Name: script] (disallowed-html)",
    ),
    Pml100Test(
        "Disallowed HTML Start in List/List",
        ["enabled=$!True"],
        """- - <script>
      <!-- some script stuff -->
    </script>
""",
        "stdin:1:5: PML100: Disallowed HTML [Tag Name: script] (disallowed-html)",
    ),
    Pml100Test(
        "Disallowed HTML Start in List/New List",
        ["enabled=$!True"],
        """- - first inner list item
  - <script>
      <!-- some script stuff -->
    </script>
""",
        "stdin:2:5: PML100: Disallowed HTML [Tag Name: script] (disallowed-html)",
    ),
    Pml100Test(
        "Disallowed HTML Start in New List/List",
        ["enabled=$!True"],
        """- first outer list item
- - <script>
      <!-- some script stuff -->
    </script>
""",
        "stdin:2:5: PML100: Disallowed HTML [Tag Name: script] (disallowed-html)",
    ),
    Pml100Test(
        "Disallowed HTML Start in New List/New List",
        ["enabled=$!True"],
        """- first outer list item
- - first inner list item
  - <script>
      <!-- some script stuff -->
    </script>
""",
        "stdin:3:5: PML100: Disallowed HTML [Tag Name: script] (disallowed-html)",
    ),
    Pml100Test(
        "Disallowed HTML Mid in List/List",
        ["enabled=$!True"],
        """- - <html>
      <script>
        <!-- some script stuff -->
      </script>
    </html>
""",
        "stdin:2:7: PML100: Disallowed HTML [Tag Name: script] (disallowed-html)",
    ),
    Pml100Test(
        "Disallowed HTML Mid in List/New List",
        ["enabled=$!True"],
        """- - first inner list item
  - <html>
      <script>
        <!-- some script stuff -->
      </script>
    </html>
""",
        "stdin:3:7: PML100: Disallowed HTML [Tag Name: script] (disallowed-html)",
    ),
    Pml100Test(
        "Disallowed HTML Mid in New List/List",
        ["enabled=$!True"],
        """- first outer list item
- - <html>
      <script>
        <!-- some script stuff -->
      </script>
    </html>
""",
        "stdin:3:7: PML100: Disallowed HTML [Tag Name: script] (disallowed-html)",
    ),
    Pml100Test(
        "Disallowed HTML Mid in New List/New List",
        ["enabled=$!True"],
        """- first outer list item
- - first inner list item
  - <html>
      <script>
        <!-- some script stuff -->
      </script>
    </html>
""",
        "stdin:4:7: PML100: Disallowed HTML [Tag Name: script] (disallowed-html)",
    ),
    Pml100Test(
        "Disallowed HTML Start in List/BQ",
        ["enabled=$!True"],
        """- > <script>
  >   <!-- some script stuff -->
  > </script>
""",
        "stdin:1:5: PML100: Disallowed HTML [Tag Name: script] (disallowed-html)",
    ),
    Pml100Test(
        "Disallowed HTML Mid in List/BQ",
        ["enabled=$!True"],
        """- > <html>
  >   <script>
  >     <!-- some script stuff -->
  >   </script>
  > </html>
""",
        "stdin:2:7: PML100: Disallowed HTML [Tag Name: script] (disallowed-html)",
    ),
    Pml100Test(
        "Disallowed HTML Start in BQuote/BQuote",
        ["enabled=$!True"],
        """> > <script>
> >   <!-- some script stuff -->
> > </script>
""",
        "stdin:1:5: PML100: Disallowed HTML [Tag Name: script] (disallowed-html)",
    ),
    Pml100Test(
        "Disallowed HTML Start in BQuote/BQuote squish all",
        ["enabled=$!True"],
        """>> <script>
>>   <!-- some script stuff -->
>> </script>
""",
        "stdin:1:4: PML100: Disallowed HTML [Tag Name: script] (disallowed-html)",
    ),
    Pml100Test(
        "Disallowed HTML Mid in BQuote/BQuote squish first",
        ["enabled=$!True"],
        """>> <html>
> >   <script>
> >     <!-- some script stuff -->
> >   </script>
> > </html>
""",
        "stdin:2:7: PML100: Disallowed HTML [Tag Name: script] (disallowed-html)",
    ),
    Pml100Test(
        "Disallowed HTML Mid in BQuote/BQuote squish second",
        ["enabled=$!True"],
        """> > <html>
>>   <script>
> >     <!-- some script stuff -->
> >   </script>
> > </html>
""",
        "stdin:2:6: PML100: Disallowed HTML [Tag Name: script] (disallowed-html)",
    ),
    Pml100Test(
        "Disallowed HTML Start in BQuote/List",
        ["enabled=$!True"],
        """> - <script>
>     <!-- some script stuff -->
>   </script>
""",
        "stdin:1:5: PML100: Disallowed HTML [Tag Name: script] (disallowed-html)",
    ),
    Pml100Test(
        "Disallowed HTML Start in BQuote/New List",
        ["enabled=$!True"],
        """> - first outer list item
> - <script>
>     <!-- some script stuff -->
>   </script>
""",
        "stdin:2:5: PML100: Disallowed HTML [Tag Name: script] (disallowed-html)",
    ),
    Pml100Test(
        "Disallowed HTML Mid in BQuote/List",
        ["enabled=$!True"],
        """> - <html>
>     <script>
>       <!-- some script stuff -->
>     </script>
>   </html>
""",
        "stdin:2:7: PML100: Disallowed HTML [Tag Name: script] (disallowed-html)",
    ),
    Pml100Test(
        "Disallowed HTML Mid in BQuote/New List",
        ["enabled=$!True"],
        """> - first outer list item
> - <html>
>     <script>
>       <!-- some script stuff -->
>     </script>
>   </html>
""",
        "stdin:3:7: PML100: Disallowed HTML [Tag Name: script] (disallowed-html)",
    ),
    # triplets
    Pml100Test(
        "Disallowed HTML Start in List/List/List",
        ["enabled=$!True"],
        """- - - <script>
        <!-- some script stuff -->
      </script>
""",
        "stdin:1:7: PML100: Disallowed HTML [Tag Name: script] (disallowed-html)",
    ),
    Pml100Test(
        "Disallowed HTML Mid in List/List/List",
        ["enabled=$!True"],
        """- - - <html>
        <script>
          <!-- some script stuff -->
        </script>
      </html>
""",
        "stdin:2:9: PML100: Disallowed HTML [Tag Name: script] (disallowed-html)",
    ),
    Pml100Test(
        "Disallowed HTML Start in List/List/Block",
        ["enabled=$!True"],
        """- - > <script>
    >   <!-- some script stuff -->
    > </script>
""",
        "stdin:1:7: PML100: Disallowed HTML [Tag Name: script] (disallowed-html)",
    ),
    Pml100Test(
        "Disallowed HTML Mid in List/List/Block",
        ["enabled=$!True"],
        """- - > <html>
    >   <script>
    >     <!-- some script stuff -->
    >   </script>
    > </html>
""",
        "stdin:2:9: PML100: Disallowed HTML [Tag Name: script] (disallowed-html)",
    ),
    Pml100Test(
        "Disallowed HTML Start in List/Block/List",
        ["enabled=$!True"],
        """- > - <script>
  >     <!-- some script stuff -->
  >   </script>
""",
        "stdin:1:7: PML100: Disallowed HTML [Tag Name: script] (disallowed-html)",
    ),
    Pml100Test(
        "Disallowed HTML Mid in List/Block/List",
        ["enabled=$!True"],
        """- > - <html>
  >     <script>
  >       <!-- some script stuff -->
  >     </script>
  >   </html>
""",
        "stdin:2:9: PML100: Disallowed HTML [Tag Name: script] (disallowed-html)",
    ),
    Pml100Test(
        "Disallowed HTML Start in List/Block/Block",
        ["enabled=$!True"],
        """- > > <script>
  > >   <!-- some script stuff -->
  > > </script>
""",
        "stdin:1:7: PML100: Disallowed HTML [Tag Name: script] (disallowed-html)",
    ),
    Pml100Test(
        "Disallowed HTML Mid in List/Block/Block",
        ["enabled=$!True"],
        """- > > <html>
  > >   <script>
  > >     <!-- some script stuff -->
  > >   </script>
  > > </html>
""",
        "stdin:2:9: PML100: Disallowed HTML [Tag Name: script] (disallowed-html)",
    ),
    Pml100Test(
        "Disallowed HTML Start in Block/List/List",
        ["enabled=$!True"],
        """> - - <script>
>       <!-- some script stuff -->
>     </script>
""",
        "stdin:1:7: PML100: Disallowed HTML [Tag Name: script] (disallowed-html)",
    ),
    Pml100Test(
        "Disallowed HTML Mid in Block/List/List",
        ["enabled=$!True"],
        """> - - <html>
>       <script>
>         <!-- some script stuff -->
>       </script>
>     </html>
""",
        "stdin:2:9: PML100: Disallowed HTML [Tag Name: script] (disallowed-html)",
    ),
    Pml100Test(
        "Disallowed HTML Start in Block/List/Block",
        ["enabled=$!True"],
        """> - > <script>
>   >   <!-- some script stuff -->
>   > </script>
""",
        "stdin:1:7: PML100: Disallowed HTML [Tag Name: script] (disallowed-html)",
    ),
    Pml100Test(
        "Disallowed HTML Mid in Block/List/Block",
        ["enabled=$!True"],
        """> - > <html>
>   >   <script>
>   >     <!-- some script stuff -->
>   >   </script>
>   > </html>
""",
        "stdin:2:9: PML100: Disallowed HTML [Tag Name: script] (disallowed-html)",
    ),
    Pml100Test(
        "Disallowed HTML Start in Block/Block/List",
        ["enabled=$!True"],
        """> > - <script>
> >     <!-- some script stuff -->
> >   </script>
""",
        "stdin:1:7: PML100: Disallowed HTML [Tag Name: script] (disallowed-html)",
    ),
    Pml100Test(
        "Disallowed HTML Mid in Block/Block/List",
        ["enabled=$!True"],
        """> > - <html>
> >     <script>
> >       <!-- some script stuff -->
> >     </script>
> >   </html>
""",
        "stdin:2:9: PML100: Disallowed HTML [Tag Name: script] (disallowed-html)",
    ),
    Pml100Test(
        "Disallowed HTML Start in Block/Block/Block",
        ["enabled=$!True"],
        """> > > <script>
> > >   <!-- some script stuff -->
> > > </script>
""",
        "stdin:1:7: PML100: Disallowed HTML [Tag Name: script] (disallowed-html)",
    ),
    Pml100Test(
        "Disallowed HTML Mid in Block/Block/Block",
        ["enabled=$!True"],
        """> > > <html>
> > >   <script>
> > >     <!-- some script stuff -->
> > >   </script>
> > > </html>
""",
        "stdin:2:9: PML100: Disallowed HTML [Tag Name: script] (disallowed-html)",
    ),
    # bq tab
    Pml100Test(
        "Raw HTML allowed", ["enabled=$!True"], "This is a <docum> example.", "", "", 0
    ),
    Pml100Test(
        "Raw HTML",
        ["enabled=$!True"],
        "This is a <noframes> example.",
        "stdin:1:11: PML100: Disallowed HTML [Tag Name: noframes] (disallowed-html)",
    ),
    Pml100Test(
        "Raw HTML with attributes",
        ["enabled=$!True"],
        "This is a <noframes some=True> example.",
        "stdin:1:11: PML100: Disallowed HTML [Tag Name: noframes] (disallowed-html)",
    ),
    Pml100Test(
        "Raw HTML self-close",
        ["enabled=$!True"],
        "This is a <noframes/> example.",
        "stdin:1:11: PML100: Disallowed HTML [Tag Name: noframes] (disallowed-html)",
    ),
]


def id_test_parse_fn(val: Any) -> str:
    """
    Id functions to allow for parameterization to be used more meaningfully.
    """
    if isinstance(val, (Pml100Test, ErrorPml100Test)):
        return val.name.replace(" ", "-")
    raise AssertionError()


@pytest.mark.parametrize("test", pml100Tests, ids=id_test_parse_fn)
def test_pml100(test: Pml100Test) -> None:
    """
    TBD
    """
    # Arrange
    scanner = MarkdownScanner()

    supplied_arguments = [
        "--disable",
        "md005,md030,md032,md041,md047",
        "--set",
        "plugins.no-inline-html.enabled=$!False",
        "--strict-config",
        "scan-stdin",
    ]
    new_args = []
    for next_argument in test.args:
        new_args.extend(
            [
                "--set",
                f"plugins.disallowed-html.{next_argument}",
            ]
        )
    if new_args:
        supplied_arguments = new_args + supplied_arguments

    # Act
    execute_results = scanner.invoke_main(
        arguments=supplied_arguments, standard_input_to_use=test.stdin
    )

    # Assert
    execute_results.assert_results(
        test.expected_stdout, test.expected_stderr, test.expected_return_code
    )


pml100ErrorTests = [
    ErrorPml100Test(
        "bad change_tag_names type",
        ["enabled=$!True", "change_tag_names=$#1"],
        "\n\nBadPluginError encountered while configuring plugins:\nThe value for property 'plugins.disallowed-html.change_tag_names' must be of type 'str'.\n",
    ),
    ErrorPml100Test(
        "bad empty string",
        ["enabled=$!True", "change_tag_names="],
        "\n\nBadPluginError encountered while configuring plugins:\nConfiguration item 'plugins.disallowed-html.change_tag_names' contains at least one empty string.\n",
    ),
    ErrorPml100Test(
        "bad change_tag_names only commas",
        ["enabled=$!True", "change_tag_names=,,,,"],
        "\n\nBadPluginError encountered while configuring plugins:\nConfiguration item 'plugins.disallowed-html.change_tag_names' contains at least one empty string.\n",
    ),
    ErrorPml100Test(
        "bad change_tag_names no prefix",
        ["enabled=$!True", "change_tag_names=something"],
        "\n\nBadPluginError encountered while configuring plugins:\nConfiguration item 'plugins.disallowed-html.change_tag_names' elements must either start with '+' or '-'.\n",
    ),
    ErrorPml100Test(
        "bad change_tag_names invalid tag name",
        ["enabled=$!True", "change_tag_names=+some thing"],
        "\n\nBadPluginError encountered while configuring plugins:\nConfiguration item 'plugins.disallowed-html.change_tag_names' contains an element 'some thing' that is not a valid tag name.\n",
    ),
]


@pytest.mark.parametrize("test", pml100ErrorTests, ids=id_test_parse_fn)
def test_pml100_errors(test: ErrorPml100Test) -> None:
    """
    TBD
    """
    # Arrange
    scanner = MarkdownScanner()

    supplied_arguments = [
        "--strict-config",
        "scan-stdin",
    ]
    new_args = []
    for next_argument in test.args:
        new_args.extend(
            [
                "--set",
                f"plugins.disallowed-html.{next_argument}",
            ]
        )
    if new_args:
        supplied_arguments = new_args + supplied_arguments

    # Act
    execute_results = scanner.invoke_main(
        arguments=supplied_arguments, standard_input_to_use="something"
    )

    # Assert
    assert execute_results.return_code == 1
    assert execute_results.std_out.getvalue() == ""
    assert_if_strings_different(
        test.expected_stderr, execute_results.std_err.getvalue()
    )


def test_pml100_query_config():
    config_test = pluginQueryConfigTest(
        "pml100",
        """
  ITEM               DESCRIPTION

  Id                 pml100
  Name(s)            disallowed-html
  Short Description  Disallowed HTML
  Description Url    https://pymarkdown.readthedocs.io/en/latest/plugins/rule_
                     pml100.md


  CONFIGURATION ITEM  TYPE     VALUE

  change_tag_names    integer  None

""",
    )
    execute_query_configuration_test(config_test)
