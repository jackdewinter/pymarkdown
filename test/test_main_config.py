"""
Module to provide tests related to the basic parts of the scanner.
"""
import os
import tempfile
from test.markdown_scanner import MarkdownScanner

from .utils import write_temporary_configuration


def test_markdown_with_dash_e_single_by_id_and_good_config():
    """
    Test to make sure we get enable a rule if '-e' is supplied and the id of the
    rule is provided. The test data for MD047 is used as it is a simple file that
    passes normally, it is used as a comparison.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md047", "end_with_blank_line.md"
    )
    supplied_configuration = {"plugins": {"md999": {"test_value": 2}}}
    configuration_file = None
    try:
        configuration_file = write_temporary_configuration(supplied_configuration)
        supplied_arguments = [
            "-e",
            "MD999",
            "-c",
            configuration_file,
            "scan",
            source_path,
        ]

        expected_return_code = 0
        expected_output = """MD999>>init_from_config
MD999>>test_value>>2
MD999>>other_test_value>>1
MD999>>starting_new_file>>
MD999>>token:[atx(1,1):1:0:]
MD999>>token:[text(1,3):This is a test: ]
MD999>>token:[end-atx::]
MD999>>token:[BLANK(2,1):]
MD999>>token:[para(3,1):]
MD999>>token:[text(3,1):The line after this line should be blank.:]
MD999>>token:[end-para:::True]
MD999>>token:[BLANK(4,1):]
MD999>>next_line:# This is a test
MD999>>next_line:
MD999>>next_line:The line after this line should be blank.
MD999>>next_line:
MD999>>completed_file
"""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
    finally:
        if configuration_file and os.path.exists(configuration_file):
            os.remove(configuration_file)


def test_markdown_with_dash_e_single_by_id_and_bad_config():
    """
    Test to make sure we get enable a rule if '-e' is supplied and the id of the
    rule is provided. The test data for MD047 is used as it is a simple file that
    passes normally, it is used as a comparison.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md047", "end_with_blank_line.md"
    )
    supplied_configuration = {"plugins": {"md999": {"test_value": "fred"}}}
    configuration_file = None
    try:
        configuration_file = write_temporary_configuration(supplied_configuration)
        supplied_arguments = [
            "-e",
            "MD999",
            "-c",
            configuration_file,
            "scan",
            source_path,
        ]

        expected_return_code = 0
        expected_output = """MD999>>init_from_config
MD999>>test_value>>1
MD999>>other_test_value>>1
MD999>>starting_new_file>>
MD999>>token:[atx(1,1):1:0:]
MD999>>token:[text(1,3):This is a test: ]
MD999>>token:[end-atx::]
MD999>>token:[BLANK(2,1):]
MD999>>token:[para(3,1):]
MD999>>token:[text(3,1):The line after this line should be blank.:]
MD999>>token:[end-para:::True]
MD999>>token:[BLANK(4,1):]
MD999>>next_line:# This is a test
MD999>>next_line:
MD999>>next_line:The line after this line should be blank.
MD999>>next_line:
MD999>>completed_file
"""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
    finally:
        if configuration_file and os.path.exists(configuration_file):
            os.remove(configuration_file)


def test_markdown_with_dash_e_single_by_id_and_bad_config_file():
    """
    Test to make sure we get an error if we provide a configuration file that is
    in a json format, but not valid.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md047", "end_with_blank_line.md"
    )
    supplied_configuration = {"plugins": {"myrule.md999": {"test_value": "fred"}}}
    configuration_file = None
    try:
        configuration_file = write_temporary_configuration(supplied_configuration)
        supplied_arguments = [
            "-e",
            "MD999",
            "-c",
            configuration_file,
            "scan",
            source_path,
        ]

        expected_return_code = 1
        expected_output = ""
        expected_error = (
            "Specified configuration file '"
            + configuration_file
            + "' is not valid: Keys strings cannot contain the separator character '.'.\n"
        )

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
    finally:
        if configuration_file and os.path.exists(configuration_file):
            os.remove(configuration_file)


def test_markdown_with_dash_e_single_by_id_and_non_json_config_file():
    """
    Test to make sure we get an error if we provide a configuration file that is
    not in a json format.

    This function shadows
    test_api_config_with_bad_contents
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md047", "end_with_blank_line.md"
    )
    supplied_configuration = "not a json file"
    configuration_file = None
    try:
        configuration_file = write_temporary_configuration(supplied_configuration)
        supplied_arguments = [
            "-e",
            "MD999",
            "-c",
            configuration_file,
            "scan",
            source_path,
        ]

        expected_return_code = 1
        expected_output = ""
        expected_error = (
            "Specified configuration file '"
            + configuration_file
            + "' is not a valid JSON file: Expecting value: line 1 column 1 (char 0).\n"
        )

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
    finally:
        if configuration_file and os.path.exists(configuration_file):
            os.remove(configuration_file)


def test_markdown_with_dash_e_single_by_id_and_non_present_config_file():
    """
    Test to make sure we get an error if we provide a configuration file that is
    not in a json format.

    This function shadows
    test_api_config_with_bad_path
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md047", "end_with_blank_line.md"
    )
    configuration_file = "not-exists"
    assert not os.path.exists(configuration_file)
    supplied_arguments = [
        "-e",
        "MD999",
        "-c",
        configuration_file,
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = ""
    expected_error = (
        "Specified configuration file 'not-exists' was not loaded: "
        + "[Errno 2] No such file or directory: 'not-exists'.\n"
    )

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_markdown_with_dash_e_single_by_id_and_good_select_config():
    """
    Test to make sure we get enable a rule if '-e' is supplied and the id of the
    rule is provided. The test data for MD047 is used as it is a simple file that
    passes normally, it is used as a comparison.

    This function shadows
    test_api_config_with_config_file_with_good_value
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md047", "end_with_blank_line.md"
    )
    supplied_configuration = {"plugins": {"md999": {"other_test_value": 2}}}
    configuration_file = None
    try:
        configuration_file = write_temporary_configuration(supplied_configuration)
        supplied_arguments = [
            "-e",
            "MD999",
            "-c",
            configuration_file,
            "scan",
            source_path,
        ]

        expected_return_code = 0
        expected_output = """MD999>>init_from_config
MD999>>test_value>>1
MD999>>other_test_value>>2
MD999>>starting_new_file>>
MD999>>token:[atx(1,1):1:0:]
MD999>>token:[text(1,3):This is a test: ]
MD999>>token:[end-atx::]
MD999>>token:[BLANK(2,1):]
MD999>>token:[para(3,1):]
MD999>>token:[text(3,1):The line after this line should be blank.:]
MD999>>token:[end-para:::True]
MD999>>token:[BLANK(4,1):]
MD999>>next_line:# This is a test
MD999>>next_line:
MD999>>next_line:The line after this line should be blank.
MD999>>next_line:
MD999>>completed_file
"""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
    finally:
        if configuration_file and os.path.exists(configuration_file):
            os.remove(configuration_file)


def test_markdown_with_dash_e_single_by_id_and_bad_select_config():
    """
    Test to make sure we get enable a rule if '-e' is supplied and the id of the
    rule is provided. The test data for MD047 is used as it is a simple file that
    passes normally, it is used as a comparison.

    This function is shadowed by
    test_api_config_with_config_file_with_bad_value
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md047", "end_with_blank_line.md"
    )
    supplied_configuration = {"plugins": {"MD999": {"other_test_value": 9}}}
    configuration_file = None
    try:
        configuration_file = write_temporary_configuration(supplied_configuration)
        supplied_arguments = [
            "-e",
            "MD999",
            "-c",
            configuration_file,
            "scan",
            source_path,
        ]

        expected_return_code = 0
        expected_output = """MD999>>init_from_config
MD999>>test_value>>1
MD999>>other_test_value>>1
MD999>>starting_new_file>>
MD999>>token:[atx(1,1):1:0:]
MD999>>token:[text(1,3):This is a test: ]
MD999>>token:[end-atx::]
MD999>>token:[BLANK(2,1):]
MD999>>token:[para(3,1):]
MD999>>token:[text(3,1):The line after this line should be blank.:]
MD999>>token:[end-para:::True]
MD999>>token:[BLANK(4,1):]
MD999>>next_line:# This is a test
MD999>>next_line:
MD999>>next_line:The line after this line should be blank.
MD999>>next_line:
MD999>>completed_file
"""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
    finally:
        if configuration_file and os.path.exists(configuration_file):
            os.remove(configuration_file)


def test_markdown_with_dash_e_single_by_id_and_config_causing_config_exception():
    """
    Test to make sure if we tell the test plugin to throw an exception during the
    call to `initialize_from_config`, that it is handled properly.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md047", "end_with_blank_line.md"
    )
    supplied_configuration = {"plugins": {"md999": {"test_value": 10}}}
    configuration_file = None
    try:
        configuration_file = write_temporary_configuration(supplied_configuration)
        supplied_arguments = [
            "-e",
            "MD999",
            "-c",
            configuration_file,
            "scan",
            source_path,
        ]

        expected_return_code = 1
        expected_output = """MD999>>init_from_config
MD999>>test_value>>10
MD999>>other_test_value>>1
"""
        expected_error = """BadPluginError encountered while configuring plugins:
Plugin id 'MD999' had a critical failure during the 'apply_configuration' action.
"""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
    finally:
        if configuration_file and os.path.exists(configuration_file):
            os.remove(configuration_file)


def test_markdown_with_dash_e_single_by_id_and_config_causing_next_token_exception():
    """
    Test to make sure if we tell the test plugin to throw an exception during the
    call to `next_token`, that it is handled properly.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md047", "end_with_blank_line.md"
    )
    supplied_configuration = {"plugins": {"md999": {"test_value": 20}}}
    configuration_file = None
    try:
        configuration_file = write_temporary_configuration(supplied_configuration)
        supplied_arguments = [
            "-e",
            "MD999",
            "-c",
            configuration_file,
            "scan",
            source_path,
        ]

        expected_return_code = 1
        expected_output = """MD999>>init_from_config
MD999>>test_value>>20
MD999>>other_test_value>>1
MD999>>starting_new_file>>
MD999>>token:[atx(1,1):1:0:]
"""
        expected_error = """BadPluginError encountered while scanning '{source_path}':
(1,1): Plugin id 'MD999' had a critical failure during the 'next_token' action.
""".replace(
            "{source_path}", source_path
        )

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
    finally:
        if configuration_file and os.path.exists(configuration_file):
            os.remove(configuration_file)


def test_markdown_with_bad_strict_config_type():
    """
    Test to make sure that we can set the strict configuration mode from
    the configuration file, capturing any bad errors.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md047", "end_with_blank_line.md"
    )
    supplied_configuration = {"mode": {"strict-config": 2}}
    configuration_file = None
    try:
        configuration_file = write_temporary_configuration(supplied_configuration)
        supplied_arguments = [
            "-c",
            configuration_file,
            "scan",
            source_path,
        ]

        expected_return_code = 1
        expected_output = ""
        expected_error = "Configuration Error: The value for property 'mode.strict-config' must be of type 'bool'."

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
    finally:
        if configuration_file and os.path.exists(configuration_file):
            os.remove(configuration_file)


def test_markdown_with_good_strict_config_type():
    """
    Test to make sure that we can set the strict configuration mode from
    the configuration file, capturing any bad errors.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md047", "end_with_blank_line.md"
    )
    supplied_configuration = {"mode": {"strict-config": True}, "log": {"file": 0}}
    configuration_file = None
    try:
        configuration_file = write_temporary_configuration(supplied_configuration)
        supplied_arguments = [
            "-c",
            configuration_file,
            "scan",
            source_path,
        ]

        expected_return_code = 1
        expected_output = ""
        expected_error = "Configuration Error: The value for property 'log.file' must be of type 'str'.\n"

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
    finally:
        if configuration_file and os.path.exists(configuration_file):
            os.remove(configuration_file)


def test_markdown_with_default_configuration_file_with_error():
    """
    Test to make sure that a default configuration will be read and have the
    same errors as if it was specified on the command line.

    This function shadows
    test_api_config_with_bad_contents_for_default_config
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md047", "end_with_blank_line.md"
    )
    default_configuration = {"mode": {"strict-config": True}, "log": {"file": 0}}

    # Note that the default configuration file is determined by the current working
    # directory, so this test creates a new directory and executes the parser from
    # within that directory.
    with tempfile.TemporaryDirectory() as tmp_dir_path:
        default_configuration_file = None
        try:
            default_configuration_file = write_temporary_configuration(
                default_configuration, file_name=".pymarkdown", directory=tmp_dir_path
            )
            supplied_arguments = [
                "scan",
                source_path,
            ]

            expected_return_code = 1
            expected_output = ""
            expected_error = "Configuration Error: The value for property 'log.file' must be of type 'str'.\n"

            # Act
            old_current_working_directory = os.getcwd()
            try:
                os.chdir(tmp_dir_path)
                execute_results = scanner.invoke_main(arguments=supplied_arguments)
            finally:
                os.chdir(old_current_working_directory)

            # Assert
            execute_results.assert_results(
                expected_output, expected_error, expected_return_code
            )
        finally:
            if default_configuration_file and os.path.exists(
                default_configuration_file
            ):
                os.remove(default_configuration_file)


def test_markdown_with_overlapping_configuration_files():
    """
    Test to make sure that information from a default configuration file and
    a specified configuration file give each other the right layering.
    i.e. specific config file should override default config file
    """

    # Arrange
    scanner = MarkdownScanner()
    xxx = """# This is a document

* a list
  - a sublist
  - a very long sublist item

this is a very long line
"""

    # The `ul-style` item is set by the default configuration and overridden as "asterisk" by the supplied configuration.
    # The `line-length` item is set by the default configuration as `10` and is not overridden.
    # This results in a `ul-style` of `asterisk` and a `line-length` of `10`.
    default_configuration = {
        "mode": {"strict-config": True},
        "plugins": {"ul-style": {"style": "dash"}, "line-length": {"line_length": 10}},
    }
    supplied_configuration = {
        "mode": {"strict-config": True},
        "plugins": {"ul-style": {"style": "asterisk"}},
    }

    with tempfile.TemporaryDirectory() as tmp_dir_path:
        configuration_file = None
        default_configuration_file = None
        try:
            configuration_file = write_temporary_configuration(
                supplied_configuration, directory=tmp_dir_path
            )
            default_configuration_file = write_temporary_configuration(
                default_configuration, file_name=".pymarkdown", directory=tmp_dir_path
            )
            supplied_arguments = ["-c", configuration_file, "scan-stdin"]

            expected_return_code = 1
            expected_output = (
                "stdin:4:3: MD004: Inconsistent Unordered List Start style "
                + "[Expected: asterisk; Actual: dash] (ul-style)\n"
                + "stdin:5:1: MD013: Line length [Expected: 10, Actual: 28] (line-length)\n"
                + "stdin:7:1: MD013: Line length [Expected: 10, Actual: 24] (line-length)"
            )
            expected_error = ""

            # Act
            old_current_working_directory = os.getcwd()
            try:
                os.chdir(tmp_dir_path)
                execute_results = scanner.invoke_main(
                    arguments=supplied_arguments, standard_input_to_use=xxx
                )
            finally:
                os.chdir(old_current_working_directory)

            # Assert
            execute_results.assert_results(
                expected_output, expected_error, expected_return_code
            )
        finally:
            if default_configuration_file and os.path.exists(
                default_configuration_file
            ):
                os.remove(default_configuration_file)
            if configuration_file and os.path.exists(configuration_file):
                os.remove(configuration_file)


def test_markdown_with_pyproject_configuration_file_with_error():
    """
    Test to make sure that a pyproject configuration will be read and have the
    same errors as if it was specified on the command line.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md047", "end_with_blank_line.md"
    )
    default_configuration = """
[tool.pymarkdown]
log.file = 2
a.c = "3"
"""

    # Note that the default configuration file is determined by the current working
    # directory, so this test creates a new directory and executes the parser from
    # within that directory.
    with tempfile.TemporaryDirectory() as tmp_dir_path:
        default_configuration_file = None
        try:
            default_configuration_file = write_temporary_configuration(
                default_configuration,
                file_name="pyproject.toml",
                directory=tmp_dir_path,
            )
            supplied_arguments = [
                "--strict-config",
                "scan",
                source_path,
            ]

            expected_return_code = 1
            expected_output = ""
            expected_error = "Configuration Error: The value for property 'log.file' must be of type 'str'.\n"

            # Act
            old_current_working_directory = os.getcwd()
            try:
                os.chdir(tmp_dir_path)
                execute_results = scanner.invoke_main(arguments=supplied_arguments)
            finally:
                os.chdir(old_current_working_directory)

            # Assert
            execute_results.assert_results(
                expected_output, expected_error, expected_return_code
            )
        finally:
            if default_configuration_file and os.path.exists(
                default_configuration_file
            ):
                os.remove(default_configuration_file)
