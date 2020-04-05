"""
Link reference definition helper
"""
from pymarkdown.link_helper import LinkHelper
from pymarkdown.parser_helper import ParserHelper
from pymarkdown.stack_token import LinkDefinitionStackToken


# pylint: disable=too-few-public-methods
class LinkReferenceDefinitionHelper:
    """
    Class to helper with the parsing of link reference definitions.
    """

    __lrd_start_character = "["

    @staticmethod
    def process_link_reference_definition(
        token_stack,
        line_to_parse,
        start_index,
        original_line_to_parse,
        extracted_whitespace,
    ):
        """
        Process a link deference definition.  Note, this requires a lot of work to
        handle properly because of partial definitions across lines.
        """
        did_pause_lrd = False
        lines_to_requeue = []
        force_ignore_first_as_lrd = False

        was_started = False
        is_blank_line = not line_to_parse and not start_index
        if token_stack[-1].was_link_definition_started:
            was_started = True
            print(
                ">>continuation_lines>>"
                + str(token_stack[-1].continuation_lines)
                + "<<"
            )
            line_to_parse = token_stack[-1].get_joined_lines(line_to_parse)
            start_index, extracted_whitespace = ParserHelper.extract_whitespace(
                line_to_parse, 0
            )
            print(">>line_to_parse>>" + line_to_parse.replace("\n", "\\n") + "<<")

        if was_started:
            print(">>parse_link_reference_definition>>was_started")
            (
                did_complete_lrd,
                end_lrd_index,
                parsed_lrd_tuple,
            ) = LinkReferenceDefinitionHelper.__parse_link_reference_definition(
                token_stack,
                line_to_parse,
                start_index,
                extracted_whitespace,
                is_blank_line,
            )
            print(
                ">>parse_link_reference_definition>>was_started>>did_complete_lrd>>"
                + str(did_complete_lrd)
                + ">>end_lrd_index>>"
                + str(end_lrd_index)
                + ">>len(line_to_parse)>>"
                + str(len(line_to_parse))
            )

            if not (
                did_complete_lrd
                or (
                    not is_blank_line
                    and not did_complete_lrd
                    and (end_lrd_index == len(line_to_parse))
                )
            ):
                print(
                    ">>parse_link_reference_definition>>was_started>>GOT HARD FAILURE"
                )
                (
                    is_blank_line,
                    line_to_parse,
                    did_complete_lrd,
                    end_lrd_index,
                    parsed_lrd_tuple,
                ) = LinkReferenceDefinitionHelper.__process_lrd_hard_failure(
                    token_stack, original_line_to_parse, lines_to_requeue
                )
        else:
            (
                did_complete_lrd,
                end_lrd_index,
                parsed_lrd_tuple,
            ) = LinkReferenceDefinitionHelper.__parse_link_reference_definition(
                token_stack,
                line_to_parse,
                start_index,
                extracted_whitespace,
                is_blank_line,
            )
            print(
                ">>parse_link_reference_definition>>did_complete_lrd>>"
                + str(did_complete_lrd)
                + ">>end_lrd_index>>"
                + str(end_lrd_index)
                + ">>len(line_to_parse)>>"
                + str(len(line_to_parse))
            )
        if (
            end_lrd_index >= 0
            and end_lrd_index == len(line_to_parse)
            and not is_blank_line
        ):
            LinkReferenceDefinitionHelper.__add_line_for_lrd_continuation(
                token_stack, was_started, original_line_to_parse
            )
            did_pause_lrd = True
        elif was_started:
            force_ignore_first_as_lrd = LinkReferenceDefinitionHelper.__stop_lrd_continuation(
                token_stack,
                did_complete_lrd,
                parsed_lrd_tuple,
                end_lrd_index,
                original_line_to_parse,
                is_blank_line,
            )
        else:
            print(">>parse_link_reference_definition>>other")

        return (
            did_complete_lrd or end_lrd_index != -1,
            did_complete_lrd,
            did_pause_lrd,
            lines_to_requeue,
            force_ignore_first_as_lrd,
        )

    @staticmethod
    def __is_link_reference_definition(
        token_stack, line_to_parse, start_index, extracted_whitespace
    ):
        """
        Determine whether or not we have the start of a link reference definition.
        """

        if token_stack[-1].is_paragraph:
            return False

        if (
            ParserHelper.is_length_less_than_or_equal_to(extracted_whitespace, 3)
        ) and ParserHelper.is_character_at_index_one_of(
            line_to_parse,
            start_index,
            LinkReferenceDefinitionHelper.__lrd_start_character,
        ):
            return True
        return False

    @staticmethod
    def __verify_link_definition_end(line_to_parse, new_index):
        """
        Verify that the link reference definition's ends properly.
        """

        print("look for EOL-ws>>" + line_to_parse[new_index:] + "<<")
        new_index, _ = ParserHelper.extract_any_whitespace(line_to_parse, new_index)
        print("look for EOL>>" + line_to_parse[new_index:] + "<<")
        if new_index < len(line_to_parse):
            print(">> characters left at EOL, bailing")
            return False, -1
        return True, new_index

    @staticmethod
    def __parse_link_reference_definition(
        token_stack, line_to_parse, start_index, extracted_whitespace, is_blank_line,
    ):
        """
        Handle the parsing of what appears to be a link reference definition.
        """
        did_start = LinkReferenceDefinitionHelper.__is_link_reference_definition(
            token_stack, line_to_parse, start_index, extracted_whitespace
        )
        if not did_start:
            return False, -1, None

        print("\nparse_link_reference_definition")
        inline_title = ""
        inline_link = None
        keep_going, new_index, collected_destination = LinkHelper.extract_link_label(
            line_to_parse, start_index + 1
        )
        if keep_going:
            keep_going, new_index, inline_link = LinkHelper.extract_link_destination(
                line_to_parse, new_index, is_blank_line
            )
        if keep_going:
            keep_going, new_index, inline_title = LinkHelper.extract_link_title(
                line_to_parse, new_index, is_blank_line
            )
        if keep_going:
            (
                keep_going,
                new_index,
            ) = LinkReferenceDefinitionHelper.__verify_link_definition_end(
                line_to_parse, new_index
            )
        if keep_going:
            collected_destination = LinkHelper.normalize_link_label(
                collected_destination
            )
            if not collected_destination:
                new_index = -1
                keep_going = False
        if not keep_going:
            return False, new_index, None

        assert new_index != -1

        print(">>collected_destination(norml)>>" + str(collected_destination))
        print(">>inline_link>>" + str(inline_link) + "<<")
        print(">>inline_title>>" + str(inline_title) + "<<")
        parsed_lrd_tuple = (collected_destination, (inline_link, inline_title))
        return True, new_index, parsed_lrd_tuple

    @staticmethod
    def __add_line_for_lrd_continuation(
        token_stack, was_started, original_line_to_parse
    ):
        """
        As part of processing a link reference definition, add a line to the continuation.
        """

        if was_started:
            print(">>parse_link_reference_definition>>start already marked")
        else:
            print(">>parse_link_reference_definition>>marking start")
            token_stack.append(LinkDefinitionStackToken())
        token_stack[-1].add_continuation_line(original_line_to_parse)

    # pylint: disable=too-many-arguments
    @staticmethod
    def __stop_lrd_continuation(
        token_stack,
        did_complete_lrd,
        parsed_lrd_tuple,
        end_lrd_index,
        original_line_to_parse,
        is_blank_line,
    ):
        """
        As part of processing a link reference definition, stop a continuation.
        """

        force_ignore_first_as_lrd = False
        print(">>parse_link_reference_definition>>no longer need start")
        del token_stack[-1]
        if did_complete_lrd:
            assert parsed_lrd_tuple
            LinkHelper.add_link_definition(parsed_lrd_tuple[0], parsed_lrd_tuple[1])
            assert not (end_lrd_index < -1 and original_line_to_parse)
        else:
            assert is_blank_line
            force_ignore_first_as_lrd = True
        return force_ignore_first_as_lrd

    # pylint: enable=too-many-arguments

    @staticmethod
    def __process_lrd_hard_failure(
        token_stack, original_line_to_parse, lines_to_requeue
    ):
        """
        In cases of a hard failure, we have had continuations to the original line
        that make it a bit more difficult to figure out if we have an actual good
        LRD in the mix somehow.  So take lines off the end while we have lines.
        """
        is_blank_line = None
        line_to_parse = None
        did_complete_lrd = None
        end_lrd_index = None
        parsed_lrd_tuple = None

        do_again = True
        token_stack[-1].add_continuation_line(original_line_to_parse)
        while do_again and token_stack[-1].continuation_lines:
            print(
                "continuation_lines>>" + str(token_stack[-1].continuation_lines) + "<<"
            )

            lines_to_requeue.append(token_stack[-1].continuation_lines[-1])
            print(">>continuation_line>>" + str(token_stack[-1].continuation_lines[-1]))
            del token_stack[-1].continuation_lines[-1]
            print(
                ">>lines_to_requeue>>"
                + str(lines_to_requeue)
                + ">>"
                + str(len(lines_to_requeue))
            )
            print(
                ">>continuation_lines>>"
                + str(token_stack[-1].continuation_lines)
                + "<<"
            )
            is_blank_line = True
            line_to_parse = token_stack[-1].get_joined_lines("")
            line_to_parse = line_to_parse[0:-1]
            start_index, extracted_whitespace = ParserHelper.extract_whitespace(
                line_to_parse, 0
            )
            print(">>line_to_parse>>" + line_to_parse.replace("\n", "\\n") + "<<")
            (
                did_complete_lrd,
                end_lrd_index,
                parsed_lrd_tuple,
            ) = LinkReferenceDefinitionHelper.__parse_link_reference_definition(
                token_stack,
                line_to_parse,
                start_index,
                extracted_whitespace,
                is_blank_line,
            )
            print(
                ">>parse_link_reference_definition>>was_started>>did_complete_lrd>>"
                + str(did_complete_lrd)
                + ">>end_lrd_index>>"
                + str(end_lrd_index)
                + ">>len(line_to_parse)>>"
                + str(len(line_to_parse))
            )
            do_again = not did_complete_lrd
        return (
            is_blank_line,
            line_to_parse,
            did_complete_lrd,
            end_lrd_index,
            parsed_lrd_tuple,
        )


# pylint: enable=too-few-public-methods
