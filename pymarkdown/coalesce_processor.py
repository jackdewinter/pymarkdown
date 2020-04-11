"""
Processing to coalesce a text tokens with a list of tokens.
"""


# pylint: disable=too-few-public-methods
class CoalesceProcessor:
    """
    Handle the text coalesce processing of the token stream.
    """

    @staticmethod
    def coalesce_text_blocks(first_pass_results):
        """
        Take a pass and combine any two adjacent text blocks into one.
        """

        coalesced_list = []
        coalesced_list.extend(first_pass_results[0:1])
        for coalesce_index in range(1, len(first_pass_results)):
            did_process = False
            print(
                "coalesce_text_blocks>>>>"
                + str(first_pass_results[coalesce_index])
                + "<<"
            )
            if coalesced_list[-1].is_text:
                print(">>coalesce_text_blocks>>>>" + str(coalesced_list[-1]) + "<<")
                if first_pass_results[coalesce_index].is_text or (
                    first_pass_results[coalesce_index].is_blank_line
                    and coalesced_list[-2].is_code_block
                ):

                    print("text-text>>" + str(coalesced_list[-2]) + "<<")
                    remove_leading_spaces = 0
                    if coalesced_list[-2].is_indented_code_block:
                        remove_leading_spaces = len(coalesced_list[-2].extra_data)
                    elif coalesced_list[-2].is_paragraph:
                        remove_leading_spaces = -1

                    print("remove_leading_spaces>>" + str(remove_leading_spaces))
                    print("combine1>>" + str(coalesced_list[-1]))
                    print("combine2>>" + str(first_pass_results[coalesce_index]))
                    coalesced_list[-1].combine(
                        first_pass_results[coalesce_index], remove_leading_spaces
                    )
                    print("combined>>" + str(coalesced_list[-1]))
                    did_process = True
            if not did_process:
                coalesced_list.append(first_pass_results[coalesce_index])

        for coalesce_index in range(1, len(coalesced_list)):
            if coalesced_list[coalesce_index].is_text and (
                coalesced_list[coalesce_index - 1].is_paragraph
                or coalesced_list[coalesce_index - 1].is_setext
            ):
                print(
                    "full_paragraph_text>" + str(coalesced_list[coalesce_index]) + "<"
                )
                print(
                    "full_paragraph_text>"
                    + str(len(coalesced_list[coalesce_index].token_text))
                    + ">"
                    + coalesced_list[coalesce_index].token_text
                    + "<"
                )
                removed_ws = coalesced_list[coalesce_index].remove_final_whitespace()
                print(
                    "full_paragraph_text>"
                    + str(len(coalesced_list[coalesce_index].token_text))
                    + ">"
                    + coalesced_list[coalesce_index].token_text
                    + "<"
                )
                print(
                    "full_paragraph_text>"
                    + str(coalesced_list[coalesce_index - 1])
                    + ">"
                )
                coalesced_list[coalesce_index - 1].set_final_whitespace(removed_ws)
                print(
                    "full_paragraph_text>"
                    + str(coalesced_list[coalesce_index - 1])
                    + ">"
                )

        return coalesced_list


# pylint: enable=too-few-public-methods
