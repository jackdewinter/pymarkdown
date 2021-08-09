# """
# Module to provide tests related to the MD026 rule.
# """
# import os
# from test.markdown_scanner import MarkdownScanner

# import pytest

# @pytest.mark.rules
# def test_md027_good_block_quote_indent():
#     """
#     Test to make sure we get the expected behavior after scanning a good file from the
#     test/resources/rules/MD026 directory that has atx headings that do not end with
#     punctuation.
#     """

#     # Arrange
#     scanner = MarkdownScanner()
#     supplied_arguments = [
#         "scan",
#         "test/resources/rules/md027/good_block_quote_indent.md",
#     ]

#     expected_return_code = 0
#     expected_output = ""
#     expected_error = ""

#     # Act
#     execute_results = scanner.invoke_main(arguments=supplied_arguments)

#     # Assert
#     execute_results.assert_results(
#         expected_output, expected_error, expected_return_code
#     )

# @pytest.mark.rules
# def test_md027_bad_block_quote_indent():
#     """
#     Test to make sure we get the expected behavior after scanning a good file from the
#     test/resources/rules/MD026 directory that has atx headings that do not end with
#     punctuation.
#     """

#     # Arrange
#     scanner = MarkdownScanner()
#     supplied_arguments = [
#         "scan",
#         "test/resources/rules/md027/bad_block_quote_indent.md",
#     ]

#     expected_return_code = 1
#     expected_output = ""
#     expected_error = ""

#     # Act
#     execute_results = scanner.invoke_main(arguments=supplied_arguments)

#     # Assert
#     execute_results.assert_results(
#         expected_output, expected_error, expected_return_code
#     )

# @pytest.mark.rules
# def test_md027_bad_block_quote_only_one_properly_indented():
#     """
#     Test to make sure we get the expected behavior after scanning a good file from the
#     test/resources/rules/MD026 directory that has atx headings that do not end with
#     punctuation.
#     """

#     # Arrange
#     scanner = MarkdownScanner()
#     supplied_arguments = [
#         "scan",
#         "test/resources/rules/md027/bad_block_quote_only_one_properly_indented.md",
#     ]

#     expected_return_code = 1
#     expected_output = ""
#     expected_error = ""

#     # Act
#     execute_results = scanner.invoke_main(arguments=supplied_arguments)

#     # Assert
#     execute_results.assert_results(
#         expected_output, expected_error, expected_return_code
#     )

# @pytest.mark.rules
# def test_md027_bad_misalligned_double_quote():
#     """
#     Test to make sure we get the expected behavior after scanning a good file from the
#     test/resources/rules/MD026 directory that has atx headings that do not end with
#     punctuation.
#     """

#     # Arrange
#     scanner = MarkdownScanner()
#     supplied_arguments = [
#         "scan",
#         "test/resources/rules/md027/bad_misalligned_double_quote.md",
#     ]

#     expected_return_code = 1
#     expected_output = ""
#     expected_error = ""

#     # Act
#     execute_results = scanner.invoke_main(arguments=supplied_arguments)

#     # Assert
#     execute_results.assert_results(
#         expected_output, expected_error, expected_return_code
#     )

# @pytest.mark.rules
# def test_md027_good_alligned_double_quote():
#     """
#     Test to make sure we get the expected behavior after scanning a good file from the
#     test/resources/rules/MD026 directory that has atx headings that do not end with
#     punctuation.
#     """

#     # Arrange
#     scanner = MarkdownScanner()
#     supplied_arguments = [
#         "scan",
#         "test/resources/rules/md027/good_alligned_double_quote.md",
#     ]

#     expected_return_code = 0
#     expected_output = ""
#     expected_error = ""

#     # Act
#     execute_results = scanner.invoke_main(arguments=supplied_arguments)

#     # Assert
#     execute_results.assert_results(
#         expected_output, expected_error, expected_return_code
#     )

# @pytest.mark.rules
# def test_md027_bad_misalligned_quote_within_list():
#     """
#     Test to make sure we get the expected behavior after scanning a good file from the
#     test/resources/rules/MD026 directory that has atx headings that do not end with
#     punctuation.
#     """

#     # Arrange
#     scanner = MarkdownScanner()
#     supplied_arguments = [
#         "scan",
#         "test/resources/rules/md027/bad_misalligned_quote_within_list.md",
#     ]

#     expected_return_code = 1
#     expected_output = ""
#     expected_error = ""

#     # Act
#     execute_results = scanner.invoke_main(arguments=supplied_arguments)

#     # Assert
#     execute_results.assert_results(
#         expected_output, expected_error, expected_return_code
#     )

# @pytest.mark.rules
# def test_md027_good_alligned_quote_within_list():
#     """
#     Test to make sure we get the expected behavior after scanning a good file from the
#     test/resources/rules/MD026 directory that has atx headings that do not end with
#     punctuation.
#     """

#     # Arrange
#     scanner = MarkdownScanner()
#     supplied_arguments = [
#         "scan",
#         "test/resources/rules/md027/good_alligned_quote_within_list.md",
#     ]

#     expected_return_code = 0
#     expected_output = ""
#     expected_error = ""

#     # Act
#     execute_results = scanner.invoke_main(arguments=supplied_arguments)

#     # Assert
#     execute_results.assert_results(
#         expected_output, expected_error, expected_return_code
#     )
