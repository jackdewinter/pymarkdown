"""
Module to provide for a leaf element that can be added to markdown parsing stream.
"""
import logging
import string

from pymarkdown.leaf_block_processor import LeafBlockProcessor
from pymarkdown.leaf_markdown_token import LeafMarkdownToken
from pymarkdown.markdown_token import MarkdownToken
from pymarkdown.parser_helper import ParserHelper, PositionMarker
from pymarkdown.parser_logger import ParserLogger

POGGER = ParserLogger(logging.getLogger(__name__))


class FrontMatterMarkdownToken(LeafMarkdownToken):
    """
    Class to provide for an encapsulation of the front matter data.
    """

    def __init__(
        self,
        boundary_line,
        collected_lines,
        matter_map,
        position_marker,
    ):
        self.__boundary_line = boundary_line
        self.__collected_lines = collected_lines
        self.__matter_map = matter_map

        LeafMarkdownToken.__init__(
            self,
            MarkdownToken._token_front_matter,
            "",
            position_marker=position_marker,
            is_extension=True,
        )
        self.__compose_extra_data_field()

    @property
    def boundary_line(self):
        """
        Returns the boundary line used to start and stop the front matter block.
        """
        return self.__boundary_line

    @property
    def collected_lines(self):
        """
        Returns the collected lines that comprise the front matter block.
        """
        return self.__collected_lines

    @property
    def matter_map(self):
        """
        Returns the processed lines from the front matter block.
        """
        return self.__matter_map

    def __compose_extra_data_field(self):
        """
        Compose the object's self.extra_data field from the local object's variables.
        """
        self._set_extra_data(
            MarkdownToken.extra_data_separator.join(
                [
                    self.__boundary_line,
                    str(self.__collected_lines),
                    str(self.__matter_map),
                ]
            )
        )

    @classmethod
    def calculate_block_token_height(cls, last_token):
        """
        Calculate the height of the token with the given properties.
        """
        return 2 + len(last_token.collected_lines)

    @classmethod
    def calculate_initial_whitespace(cls):
        """
        Calculate the amount of whitespace for the token.
        """
        return 0, False


class FrontMatterExtension:
    """
    Extension to implement the front matter extensions.
    """

    @staticmethod
    def handle_front_matter_token(output_html, next_token, transform_state):
        """
        Handle the front matter token.  Note that it does not contribute anything
        at all to the HTML output.
        """
        _ = (next_token, transform_state)

        return output_html

    @staticmethod
    def rehydrate_front_matter(current_token, previous_token):
        """
        Rehydrate the front matter text from the token.
        """
        _ = previous_token

        front_matter_parts = [current_token.boundary_line]
        front_matter_parts.extend(current_token.collected_lines)
        front_matter_parts.extend([current_token.boundary_line, ""])
        return ParserHelper.newline_character.join(front_matter_parts)

    @staticmethod
    def process_header_if_present(
        token_to_use, line_number, requeue, source_provider, tokenized_document
    ):
        """
        Take care of processing eligibility and processing for front matter support.
        """

        start_char, _ = LeafBlockProcessor.is_thematic_break(
            token_to_use, 0, "", whitespace_allowed_between_characters=False
        )
        if start_char == "-":
            (
                token_to_use,
                new_token,
                line_number,
                requeue_lines,
            ) = FrontMatterExtension.__handle_document_front_matter(
                token_to_use, source_provider
            )
            if new_token:
                tokenized_document.append(new_token)
            else:
                requeue.extend(requeue_lines)
                token_to_use = requeue[0]
                del requeue[0]
            POGGER.debug("self.tokenized_document>>$", tokenized_document)
            POGGER.debug("requeue>>$", requeue)
        return token_to_use, line_number, requeue

    @staticmethod
    def __handle_document_front_matter(token_to_use, source_provider):

        starting_line = token_to_use
        repeat_again = True
        have_closing = False
        collected_lines = []
        POGGER.info("Metadata prefix detected, scanning for metadata header.")
        while repeat_again:
            token_to_use = source_provider.get_next_line()
            if token_to_use and token_to_use.strip():
                start_char, _ = LeafBlockProcessor.is_thematic_break(
                    token_to_use, 0, "", whitespace_allowed_between_characters=False
                )
                have_closing = start_char and starting_line == token_to_use
                repeat_again = not have_closing
            else:
                repeat_again = token_to_use is not None
            if repeat_again:
                collected_lines.append(token_to_use)

        if not have_closing:
            POGGER.info(
                "Metadata prefix abandoned. End of document reached before closing fence encountered."
            )
            collected_lines.insert(0, starting_line)
            return None, None, 1, collected_lines

        POGGER.info("Metadata prefix collected. Verifying validity.")
        matter_map = FrontMatterExtension.__is_front_matter_valid(collected_lines)
        POGGER.debug("ret=$s,type=$s", matter_map, type(matter_map))
        if isinstance(matter_map, str):
            POGGER.info("Metadata validation failed: $", matter_map)
            collected_lines.insert(0, starting_line)
            collected_lines.append(starting_line)
            return None, None, 1, collected_lines

        POGGER.info("Metadata validation succeeded.")
        position_marker = PositionMarker(1, 0, starting_line)
        new_token = FrontMatterMarkdownToken(
            starting_line, collected_lines, matter_map, position_marker
        )
        return (
            source_provider.get_next_line(),
            new_token,
            3 + len(collected_lines),
            None,
        )

    @staticmethod
    def __is_front_matter_valid(collected_lines):

        ascii_letters_and_digits = f"{string.ascii_letters}{string.digits}_-"

        current_title = None
        current_value = None
        value_map = {}

        for next_line in collected_lines:
            POGGER.debug("Next fm:>$s<", next_line)
            if not next_line.strip():
                return "Blank line encountered before end of metadata."
            next_index, _ = ParserHelper.extract_whitespace(next_line, 0)
            if next_index >= 4:
                POGGER.debug("Indented line established.")
                if current_title:
                    current_value += "\n" + next_line.strip()
                    POGGER.debug("current_value>$<", current_value)
                else:
                    return "Continuation line encountered before a keyword line."
            else:
                POGGER.debug("Non-indented line established.")
                if current_title:
                    POGGER.debug("Adding '$' as '$'.", current_title, current_value)
                    value_map[current_title] = current_value

                (
                    next_index,
                    current_title,
                ) = ParserHelper.collect_while_one_of_characters(
                    next_line, next_index, ascii_letters_and_digits
                )
                if next_index < len(next_line) and next_line[next_index] == ":":
                    current_value = next_line[next_index + 1 :].strip()
                else:
                    return "Newline did not start with `keyword:`."
        if current_title:
            POGGER.debug("Adding final '$' as '$'.", current_title, current_value)
            value_map[current_title.lower()] = current_value
        if not value_map:
            return "No valid metadata header lines were found."
        return value_map
