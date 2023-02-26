# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=invalid-name
import timeit

import pytest

from pymarkdown.parser_helper import ParserHelper


def xtest_block_quotes_extra_perf1():
    n = 500
    ex = (
        "\n"
        + "from pymarkdown.tokenized_markdown import TokenizedMarkdown\n"
        + "source_markdown = '> a``html\\n> maybe``\\n>\\n> end'\n"
        + "tokenizer = TokenizedMarkdown()\n"
        + "actual_tokens = tokenizer.transform(source_markdown, show_debug=False)\n"
    )
    n = 1
    ex = (
        "import logging\n"
        + "LOGGER = logging.getLogger(__name__)\n"
        + "logging.getLogger().setLevel(logging.WARNING)\n"
        + "for i in range(0,100000):\n"
        + "   LOGGER.debug('this is something to log1-->')\n"
    )

    x = timeit.timeit(ex, number=n)
    print(">>" + str(x))
    print(">>" + str(float(x) / float(n)))
    raise AssertionError("TBD")


def bob1():
    search_string = "1234567890z"
    search_for = "abcdefghijklmnopqrstuvwxyz"
    ParserHelper.index_any_of(search_string, search_for)


def fred():  # sourcery skip: inline-immediately-returned-variable
    f = "this is a test!"
    g = "1"
    h = "yyyyy"
    hh = "yyyyy33"
    i = "".join([f, g, h, hh])
    return i


def barney():
    # sourcery skip: inline-immediately-returned-variable, inline-variable, simplify-fstring-formatting
    f = "this is a test!"
    g = "1"
    h = "yyyyy"
    hh = "yyyyy33"
    i = f"{f}{g}{h}{hh}"
    return i


def xtest_block_quotes_extra_perf3x():
    # sourcery skip: inline-variable, simplify-fstring-formatting
    a = "a"
    b = 1
    c = f"{a}{b}"
    assert c == "a1"


@pytest.mark.timeout(120)
def xtest_block_quotes_extra_perf3():
    assert fred() == barney()
    for _ in range(5):
        xx = timeit.timeit("barney()", globals=globals(), number=100)
    for _ in range(5):
        xx = timeit.timeit("fred()", globals=globals(), number=100)

    for y in range(5):
        xx = timeit.timeit("barney()", globals=globals(), number=10000000)
        print(str(xx) + ">>" + str(y))
    for y in range(5):
        xx = timeit.timeit("fred()", globals=globals(), number=10000000)
        print(str(xx) + ">>" + str(y))
    raise AssertionError("TBD")


# pylint: enable=missing-module-docstring
# pylint: enable=missing-function-docstring
# pylint: enable=invalid-name
