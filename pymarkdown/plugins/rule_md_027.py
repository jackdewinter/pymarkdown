"""
Module to implement a plugin that looks for hard tabs in the files.
"""
from pymarkdown.plugin_manager import Plugin, PluginDetails


class RuleMd027(Plugin):
    """
    Class to implement a plugin that looks for hard tabs in the files.
    """

    # def __init__(self):
    #     super().__init__()
    #     self.__xx = None
    #     self.__yy = None

    def get_details(self):
        """
        Get the details for the plugin.
        """
        return PluginDetails(
            # blockquote, whitespace, indentation
            plugin_name="no-multiple-space-blockquote",
            plugin_id="MD027",
            plugin_enabled_by_default=False,
            plugin_description="Multiple spaces after blockquote symbol",
            plugin_version="0.0.0",
            plugin_interface_version=1,
        )  # https://github.com/DavidAnson/markdownlint/blob/master/doc/Rules.md#md027---multiple-spaces-after-blockquote-symbol

    def starting_new_file(self):
        """
        Event that the a new file to be scanned is starting.
        """
        # self.__xx = []
        # self.__yy = {}

    def next_token(self, context, token):
        """
        Event that a new token is being processed.
        """
        # return
        # if token.is_block_quote_start:
        #     self.__xx.append(token)
        #     self.__yy[len(self.__xx)] = 0
        #     print("bq>" + str(self.__xx[-1]).replace("\n","\\n"))
        # elif token.is_list_start:
        #     self.__xx.append(token)
        # elif token.is_block_quote_end:
        #     sd = len(self.__xx)
        #     fg = self.__xx[-1].leading_spaces.count("\n")
        #     print(str(fg) + "--" + str(self.__yy[sd]))
        #     assert fg == self.__yy[sd]
        #     del self.__yy[self.__yy[sd]]
        #     del self.__xx[-1]
        # elif token.is_list_end:
        #     del self.__xx[-1]
        # elif self.__xx and self.__xx[-1].is_block_quote_start:
        #     sd = len(self.__xx)
        #     print(str(self.__yy[sd]) + "-->token>" + str(token))
        #     if token.is_paragraph_end:
        #         self.__yy[sd] += 1
        #     elif token.is_blank_line:
        #         self.__yy[sd] += 1
        #         fgg = self.__xx[-1].leading_spaces.split("\n")
        #         print(str(fgg))
        #     print(str(self.__yy[sd]) + "<--token>" + str(token))


# > this is text
# > within a block quote
# [block-quote(1,1)::> \n> \n]
#
# >  this is text
# >  within a block quote
# [block-quote(1,1)::> \n> \n]
# [token:[para(1,4): \n ]
