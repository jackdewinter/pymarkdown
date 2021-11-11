"""
Module to provide classes to deal with extensions.
"""
import argparse
import logging
import re
import sys

from application_properties import ApplicationPropertiesFacade
from columnar import columnar

from pymarkdown.extensions.disallowed_raw_html import MarkdownDisallowRawHtmlExtension
from pymarkdown.extensions.extended_autolinks import MarkdownExtendedAutolinksExtension
from pymarkdown.extensions.extension_one import DebugExtension
from pymarkdown.extensions.front_matter_markdown_token import FrontMatterExtension
from pymarkdown.extensions.markdown_strikethrough import MarkdownStrikeThroughExtension
from pymarkdown.extensions.markdown_tables import MarkdownTablesExtension
from pymarkdown.extensions.pragma_token import PragmaExtension
from pymarkdown.extensions.task_list_items import MarkdownTaskListItemsExtension

LOGGER = logging.getLogger(__name__)


class ExtensionManager:
    """
    Manager object to take care of loading and accessing extension modules.
    """

    __extensions_prefix = "extensions"
    __argparse_subparser = None
    __root_subparser_name = "em_subcommand"
    __id_regex = re.compile("^[a-zA-Z0-9][a-zA-Z0-9-]*[a-zA-Z0-9]$")

    def __init__(self):
        self.__extension_objects = {}
        self.__extension_details = {}
        self.__enabled_extensions = []
        self.__properties = None
        self.__is_front_matter_enabled = None
        self.__is_linter_pragmas_enabled = None

    def initialize(
        self,
        args,
        properties,
    ):
        """
        Initializes the manager by adding extensions and registering them.
        """

        self.__properties = properties
        _ = args

        all_extensions = [
            FrontMatterExtension(),
            PragmaExtension(),
            MarkdownTablesExtension(),
            MarkdownTaskListItemsExtension(),
            MarkdownStrikeThroughExtension(),
            MarkdownExtendedAutolinksExtension(),
            MarkdownDisallowRawHtmlExtension(),
            DebugExtension(),
        ]

        for next_extension_object in all_extensions:
            next_extension = next_extension_object.get_details()
            self.__extension_details[next_extension.extension_id] = next_extension
            self.__extension_objects[
                next_extension.extension_id
            ] = next_extension_object
            _ = next_extension.extension_interface_version
            _ = next_extension.extension_configuration

    # pylint: disable=consider-using-dict-items
    def apply_configuration(self):
        """
        Apply any supplied configuration to each of the enabled extensions.
        """
        for next_extension_id in self.__extension_details:
            next_extension_detail = self.__extension_details[next_extension_id]
            (
                is_enabled,
                extension_specific_facade,
            ) = self.__determine_if_extension_enabled(next_extension_detail, None, None)
            LOGGER.info("extension %s: enabled=%s", next_extension_id, is_enabled)
            if is_enabled:
                self.__enabled_extensions.append(next_extension_id)

                next_extension_object = self.__extension_objects[next_extension_id]
                next_extension_object.apply_configuration(extension_specific_facade)

        self.__is_front_matter_enabled = (
            FrontMatterExtension().get_identifier() in self.__enabled_extensions
        )
        self.__is_linter_pragmas_enabled = (
            PragmaExtension().get_identifier() in self.__enabled_extensions
        )

    # pylint: enable=consider-using-dict-items

    @property
    def is_front_matter_enabled(self):
        """
        Check to see if front-matter support is enabled.
        """
        return self.__is_front_matter_enabled

    @property
    def is_linter_pragmas_enabled(self):
        """
        Check to see if linter-pragmas support is enabled.
        """
        return self.__is_linter_pragmas_enabled

    @staticmethod
    def argparse_subparser_name():
        """
        Gets the name of the subparser used to handle these extensions.
        """
        return "extensions"

    def handle_argparse_subparser(self, args):
        """
        Handle the parsing for this subparser.
        """
        subparser_value = getattr(args, ExtensionManager.__root_subparser_name)
        return_code = 0
        if subparser_value == "list":
            self.__handle_argparse_subparser_list(args)
        elif subparser_value == "info":
            return_code = self.__handle_argparse_subparser_info(args)
        else:
            ExtensionManager.__argparse_subparser.print_help()
            sys.exit(2)
        return return_code

    def __handle_argparse_subparser_list(self, args):
        list_re = None
        if args.list_filter:
            list_re = re.compile(
                "^" + args.list_filter.replace("*", ".*").replace("?", ".") + "$"
            )

        show_rows = []
        names = list(self.__extension_details.keys())
        names.sort()
        for next_extension_name in names:

            next_extension = self.__extension_details[next_extension_name]
            if next_extension.extension_id == "debug-extension" or (
                next_extension.extension_version == "0.0.0" and not args.show_all
            ):
                continue

            does_match = list_re.match(next_extension_name) if list_re else True
            if does_match:
                is_enabled_now = next_extension_name in self.__enabled_extensions
                display_row = [
                    next_extension.extension_id,
                    next_extension.extension_name,
                    str(next_extension.extension_enabled_by_default),
                    str(is_enabled_now),
                    next_extension.extension_version,
                ]
                show_rows.append(display_row)

        if show_rows:
            headers = [
                "id",
                "name",
                "enabled\n(default)",
                "enabled\n(current)",
                "version",
            ]
            table = columnar(show_rows, headers, no_borders=True)
            split_rows = table.split("\n")
            new_rows = [next_row.rstrip() for next_row in split_rows]
            print("\n".join(new_rows))
        else:
            print(f"No extension identifier matches the pattern '{args.list_filter}'.")

    def __handle_argparse_subparser_info(self, args):
        if args.info_filter not in self.__extension_details.keys():
            print(f"Unable to find an extension with an id of '{args.info_filter}'.")
            return 1

        found_extension = self.__extension_details[args.info_filter]
        show_rows = []
        next_row = ["Id", found_extension.extension_id]
        show_rows.append(next_row)
        next_row = ["Name", found_extension.extension_name]
        show_rows.append(next_row)
        next_row = ["Short Description", found_extension.extension_description]
        show_rows.append(next_row)
        next_row = ["Description Url", found_extension.extension_url]
        show_rows.append(next_row)
        # if found_plugin.plugin_configuration:
        #     next_row = ["Configuration Items", found_plugin.plugin_configuration]
        #     show_rows.append(next_row)

        headers = ["Item", "Description"]
        table = columnar(show_rows, headers, no_borders=True)
        split_rows = table.split("\n")
        new_rows = [next_row.rstrip() for next_row in split_rows]
        print("\n".join(new_rows))
        return 0

    @staticmethod
    def __list_filter_type(argument):
        test_argument = argument.replace("*", "").replace("?", "")
        if ExtensionManager.__id_regex.match(test_argument):
            return argument
        raise argparse.ArgumentTypeError(
            f"Value '{argument}' is not a valid pattern for an id."
        )

    @staticmethod
    def __info_filter_type(argument):
        if ExtensionManager.__id_regex.match(argument):
            return argument
        raise argparse.ArgumentTypeError(f"Value '{argument}' is not a valid id.")

    @staticmethod
    def add_argparse_subparser(subparsers):
        """
        Populate the argparse tree to allow for plugin support.
        """

        new_sub_parser = subparsers.add_parser(
            ExtensionManager.argparse_subparser_name(), help="extension commands"
        )
        ExtensionManager.__argparse_subparser = new_sub_parser
        plugin_subparsers = new_sub_parser.add_subparsers(
            dest=ExtensionManager.__root_subparser_name
        )

        sub_sub_parser = plugin_subparsers.add_parser(
            "list", help="list the available extensions"
        )
        sub_sub_parser.add_argument(
            "--all",
            dest="show_all",
            action="store_true",
            default=False,
            help="show all loaded extensions (default is False)",
        )
        sub_sub_parser.add_argument(
            dest="list_filter",
            default=None,
            help="filter",
            nargs="?",
            type=ExtensionManager.__list_filter_type,
        )
        sub_sub_parser = plugin_subparsers.add_parser(
            "info", help="information on a specific extension"
        )
        sub_sub_parser.add_argument(
            dest="info_filter",
            default=None,
            type=ExtensionManager.__info_filter_type,
            help="an id",
        )

    def __determine_if_extension_enabled(
        self,
        extension_object,
        command_line_enabled_rules,
        command_line_disabled_rules,
    ):
        """
        Given the enable and disable rule values, evaluate the enabled or disabled
        state of the extension in proper order.
        """

        _ = (command_line_enabled_rules, command_line_disabled_rules)

        new_value = None
        LOGGER.debug(
            "Extension '%s'",
            extension_object.extension_id,
        )

        # if command_line_disabled_rules:
        #     LOGGER.debug(
        #         "Disabled on command line: %s", str(command_line_disabled_rules)
        #     )
        #     for next_identifier in plugin_oextension_objectbject.plugin_identifiers:
        #         if next_identifier in command_line_disabled_rules:
        #             new_value = False
        #             LOGGER.debug("Plugin is disabled from command line.")
        #             break
        # if new_value is None and command_line_enabled_rules:
        #     LOGGER.debug("Enabled on command line: %s", str(command_line_enabled_rules))
        #     for next_identifier in plugin_object.plugin_identifiers:
        #         if next_identifier in command_line_enabled_rules:
        #             new_value = True
        #             LOGGER.debug("Plugin is enabled from command line.")
        #             break
        # if new_value is None:
        plugin_section_title = f"{ExtensionManager.__extensions_prefix}{self.__properties.separator}{extension_object.extension_id}{self.__properties.separator}"
        extension_specific_facade = ApplicationPropertiesFacade(
            self.__properties, plugin_section_title
        )
        new_value = extension_specific_facade.get_boolean_property(
            "enabled", default_value=None
        )
        if new_value is None:
            LOGGER.debug(
                "No other enable state found, setting to default of '%s'.",
                str(extension_object.extension_enabled_by_default),
            )
        else:
            LOGGER.debug(
                "Extension specific key 'enabled' found, value is '%s'.",
                str(new_value),
            )

        return (
            extension_object.extension_enabled_by_default
            if new_value is None
            else new_value
        ), extension_specific_facade
