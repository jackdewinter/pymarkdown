"""
Module to provide classes to deal with plugins.
"""

import argparse
import inspect
import logging
import os
import re
import sys
from io import TextIOWrapper
from typing import Any, Dict, List, Optional, Pattern, Set, Tuple

from application_properties import ApplicationProperties, ApplicationPropertiesFacade
from columnar import columnar

from pymarkdown.extensions.pragma_token import PragmaExtension
from pymarkdown.general.main_presentation import MainPresentation
from pymarkdown.general.parser_helper import ParserHelper
from pymarkdown.plugin_manager.bad_plugin_error import BadPluginError
from pymarkdown.plugin_manager.fix_line_record import FixLineRecord
from pymarkdown.plugin_manager.fix_token_record import FixTokenRecord
from pymarkdown.plugin_manager.found_plugin import FoundPlugin
from pymarkdown.plugin_manager.plugin_details import PluginDetailsV2
from pymarkdown.plugin_manager.plugin_scan_context import PluginScanContext
from pymarkdown.plugin_manager.plugin_scan_failure import PluginScanFailure
from pymarkdown.plugin_manager.rule_plugin import RulePlugin
from pymarkdown.return_code_helper import ApplicationResult
from pymarkdown.tokens.markdown_token import MarkdownToken

LOGGER = logging.getLogger(__name__)

# pylint: disable=too-many-lines


# pylint: disable=too-many-instance-attributes
class PluginManager:
    """
    Manager object to take care of load and accessing plugin modules.
    """

    __plugin_prefix = "plugins"
    __root_subparser_name = "pm_subcommand"
    __argparse_subparser: Optional[argparse.ArgumentParser] = None
    __id_regex = re.compile("^[a-z]{2,3}\\d{3}$")
    __name_regex = re.compile("^[a-zA-Z0-9][a-zA-Z0-9-]*[a-zA-Z0-9]$")
    __filter_regex = re.compile("^[a-zA-Z0-9-]+$")
    __version_regex = re.compile("^(0|[1-9]\\d*)\\.(0|[1-9]\\d*)\\.(0|[1-9]\\d*)$")

    def __init__(
        self,
        presentation: MainPresentation,
    ) -> None:
        (
            self.number_of_scan_failures,
            self.number_of_pragma_failures,
            self.__show_stack_trace,
            self.__show_fix_debug,
        ) = (0, 0, False, False)
        self.__loaded_classes: List[Tuple[RulePlugin, str]] = []

        self.__presentation = presentation

        self.__document_pragmas: Dict[int, Set[str]] = {}
        self.__document_pragma_ranges: List[Tuple[int, int, Set[str]]]

        self.__registered_plugins: List[FoundPlugin] = []
        self.__enabled_plugins: List[FoundPlugin] = []
        self.__enabled_plugins_for_starting_new_file: List[FoundPlugin] = []
        self.__enabled_plugins_for_next_token: List[FoundPlugin] = []
        self.__enabled_plugins_for_next_line: List[FoundPlugin] = []
        self.__enabled_plugins_for_completed_file: List[FoundPlugin] = []
        self.__all_ids: Dict[str, FoundPlugin] = {}

    # pylint: disable=too-many-arguments
    def initialize(
        self,
        directory_to_search: str,
        additional_paths: List[str],
        enable_rules_from_command_line: str,
        disable_rules_from_command_line: str,
        properties: ApplicationProperties,
        show_stack_trace: bool,
        show_fix_debug: bool,
    ) -> None:
        """
        Initializes the manager by scanning for plugins, loading them, and registering them.
        """
        (
            self.number_of_scan_failures,
            self.number_of_pragma_failures,
            self.__loaded_classes,
            self.__show_stack_trace,
            self.__show_fix_debug,
        ) = (0, 0, [], show_stack_trace, show_fix_debug)

        plugin_files = self.__find_eligible_plugins_in_directory(directory_to_search)
        self.__load_plugins(directory_to_search, plugin_files)

        all_additional_paths = list(additional_paths or [])
        if more_paths := properties.get_string_property("plugins.additional_paths"):
            all_additional_paths.extend(more_paths.split(","))

        if all_additional_paths:
            for next_additional_plugin in all_additional_paths:
                if not os.path.exists(next_additional_plugin):
                    formatted_message = (
                        f"Plugin path '{next_additional_plugin}' does not exist."
                    )
                    raise BadPluginError(formatted_message=formatted_message)
                if os.path.isdir(next_additional_plugin):
                    plugin_files = self.__find_eligible_plugins_in_directory(
                        next_additional_plugin
                    )
                    self.__load_plugins(next_additional_plugin, plugin_files)
                else:
                    self.__load_plugins(
                        os.path.dirname(next_additional_plugin),
                        [os.path.basename(next_additional_plugin)],
                    )

        self.__register_plugins(
            enable_rules_from_command_line, disable_rules_from_command_line, properties
        )

    # pylint: enable=too-many-arguments

    @staticmethod
    def argparse_subparser_name() -> str:
        """
        Gets the name of the subparser used to handle these plugins.
        """
        return "plugins"

    @staticmethod
    def __list_filter_type(argument: str) -> str:
        test_argument = argument.replace("*", "").replace("?", "")
        if PluginManager.__filter_regex.match(test_argument):
            return argument
        raise argparse.ArgumentTypeError(
            f"Value '{argument}' is not a valid pattern for an id or a name."
        )

    @staticmethod
    def __info_filter_type(argument: str) -> str:
        if PluginManager.__id_regex.match(argument) or PluginManager.__name_regex.match(
            argument
        ):
            return argument
        raise argparse.ArgumentTypeError(
            f"Value '{argument}' is not a valid id or name."
        )

    @staticmethod
    def add_argparse_subparser(subparsers: argparse._SubParsersAction) -> None:  # type: ignore
        """
        Populate the argparse tree to allow for plugin support.
        """

        new_sub_parser = subparsers.add_parser(
            PluginManager.argparse_subparser_name(), help="plugin commands"
        )
        PluginManager.__argparse_subparser = new_sub_parser
        plugin_subparsers = new_sub_parser.add_subparsers(
            dest=PluginManager.__root_subparser_name
        )

        sub_sub_parser = plugin_subparsers.add_parser(
            "list", help="list the available plugins"
        )
        sub_sub_parser.add_argument(
            "--all",
            dest="show_all",
            action="store_true",
            default=False,
            help="show all loaded plugins (default is False)",
        )
        sub_sub_parser.add_argument(
            dest="list_filter",
            default=None,
            help="filter",
            nargs="?",
            type=PluginManager.__list_filter_type,
        )
        sub_sub_parser = plugin_subparsers.add_parser(
            "info", help="information on a specific plugin"
        )
        sub_sub_parser.add_argument(
            dest="info_filter",
            default=None,
            type=PluginManager.__info_filter_type,
            help="an id",
        )

    def __add_row_for_next_plugin(
        self,
        next_plugin_id: str,
        args: argparse.Namespace,
        show_rows: List[List[str]],
        list_re: Optional[Pattern[str]],
    ) -> None:
        # if next_plugin_id.startswith("md9"):
        #     continue
        next_plugin_list: List[FoundPlugin] = []
        for next_plugin in self.__registered_plugins:
            if next_plugin.plugin_id == next_plugin_id:
                next_plugin_list.append(next_plugin)
        assert len(next_plugin_list) == 1
        next_plugin = next_plugin_list[0]
        if next_plugin.plugin_version != "0.0.0" or args.show_all:
            self.__show_row_if_matches(list_re, next_plugin_id, next_plugin, show_rows)

    def __handle_argparse_subparser_list(
        self, args: argparse.Namespace
    ) -> ApplicationResult:
        list_re = None
        if args.list_filter:
            list_re = re.compile(
                "^" + args.list_filter.replace("*", ".*").replace("?", ".") + "$"
            )

        show_rows: List[List[str]] = []
        ids = self.all_plugin_ids
        ids.sort()
        for next_plugin_id in ids:
            self.__add_row_for_next_plugin(next_plugin_id, args, show_rows, list_re)
        if show_rows:
            headers = [
                "id",
                "names",
                "enabled\n(default)",
                "enabled\n(current)",
                "version",
                "fix",
            ]
            self.__print_columnar_data(headers, show_rows)
            return ApplicationResult.SUCCESS
        self.__presentation.print_system_error(
            f"No plugin rule identifiers matches the pattern '{args.list_filter}'."
        )
        return ApplicationResult.NO_FILES_TO_SCAN

    def __show_row_if_matches(
        self,
        list_re: Optional[Pattern[str]],
        next_plugin_id: str,
        next_plugin: FoundPlugin,
        show_rows: List[List[str]],
    ) -> None:
        does_match = True
        if list_re:
            does_match = list_re.match(next_plugin_id) is not None
            if not does_match:
                for next_name in next_plugin.plugin_names:
                    does_match = list_re.match(next_name) is not None
                    if does_match:
                        break
        if does_match:
            is_enabled_now = next_plugin in self.__enabled_plugins
            display_row = [
                next_plugin_id,
                ", ".join(next_plugin.plugin_names),
                str(next_plugin.plugin_enabled_by_default),
                str(is_enabled_now),
                next_plugin.plugin_version,
                "Yes" if next_plugin.plugin_supports_fix else "No",
            ]
            show_rows.append(display_row)

    def __print_columnar_data(
        self, headers: List[str], show_rows: List[List[str]]
    ) -> None:
        table = columnar(show_rows, headers, no_borders=True)
        split_rows = table.split(ParserHelper.newline_character)
        new_rows = [next_row.rstrip() for next_row in split_rows]
        self.__presentation.print_system_output(
            ParserHelper.newline_character.join(new_rows)
        )

    def __handle_argparse_subparser_info(
        self, args: argparse.Namespace
    ) -> ApplicationResult:
        matching_plugins: List[FoundPlugin] = list(
            filter(
                lambda x: args.info_filter in x.plugin_identifiers,
                self.__registered_plugins,
            )
        )
        if not matching_plugins:
            self.__presentation.print_system_error(
                f"Unable to find a plugin with an id or name of '{args.info_filter}'."
            )
            return ApplicationResult.NO_FILES_TO_SCAN

        found_plugin = matching_plugins[0]
        show_rows = [
            ["Id", found_plugin.plugin_id],
            ["Name(s)", ",".join(found_plugin.plugin_names)],
            ["Short Description", found_plugin.plugin_description],
        ]
        if found_plugin.plugin_url:
            next_row = ["Description Url", found_plugin.plugin_url]
            show_rows.append(next_row)
        if found_plugin.plugin_configuration:
            next_row = ["Configuration Items", found_plugin.plugin_configuration]
            show_rows.append(next_row)

        headers = ["Item", "Description"]
        self.__print_columnar_data(headers, show_rows)
        return ApplicationResult.SUCCESS

    def handle_argparse_subparser(self, args: argparse.Namespace) -> ApplicationResult:
        """
        Handle the parsing for this subparser.
        """
        subparser_value = getattr(args, PluginManager.__root_subparser_name)
        if subparser_value == "list":
            return self.__handle_argparse_subparser_list(args)
        if subparser_value == "info":
            return self.__handle_argparse_subparser_info(args)
        assert PluginManager.__argparse_subparser
        PluginManager.__argparse_subparser.print_help()
        return ApplicationResult.COMMAND_LINE_ERROR

    def log_scan_failure(self, scan_failure: PluginScanFailure) -> None:
        """
        Log the scan failure in the appropriate format.
        """

        rule_id = scan_failure.rule_id.lower()
        if (
            self.__document_pragmas
            and scan_failure.line_number in self.__document_pragmas
        ):
            id_set = self.__document_pragmas[scan_failure.line_number]
            if rule_id in id_set:
                return

        if self.__document_pragma_ranges:
            for i, j, k in self.__document_pragma_ranges:
                if i <= scan_failure.line_number <= j and rule_id in k:
                    return

        extra_info = (
            f" [{scan_failure.extra_error_information}]"
            if scan_failure.extra_error_information
            else ""
        )
        rule_id = scan_failure.rule_id.upper()

        adjusted_failure = PluginScanFailure(
            scan_failure.scan_file,
            scan_failure.line_number,
            scan_failure.column_number,
            rule_id,
            scan_failure.rule_name,
            scan_failure.rule_description,
            extra_info,
        )
        self.__presentation.print_scan_failure(adjusted_failure)
        self.number_of_scan_failures += 1

    def log_pragma_failure(
        self, scan_file: str, line_number: int, pragma_error: str
    ) -> None:
        """
        Log the pragma failure in the appropriate format.
        """
        self.__presentation.print_pragma_failure(scan_file, line_number, pragma_error)
        self.number_of_pragma_failures += 1

    def compile_pragmas(self, scan_file: str, pragma_lines: Dict[int, str]) -> None:
        """
        Go through the list of extracted pragmas and compile them.
        """

        for next_line_number in pragma_lines:
            PragmaExtension.compile_single_pragma(
                scan_file,
                next_line_number,
                pragma_lines,
                self.__all_ids,
                self.__document_pragmas,
                self.__document_pragma_ranges,
                self.log_pragma_failure,
            )

    @property
    def enabled_plugins(self) -> List[FoundPlugin]:
        """
        Get a list of the plugins that are currently enabled.
        """
        return self.__enabled_plugins

    @classmethod
    def __find_eligible_plugins_in_directory(
        cls, directory_to_search: str
    ) -> List[str]:
        """
        Given a directory to search, scan for eligible modules to load later.
        """

        return [
            x
            for x in os.listdir(directory_to_search)
            if x.endswith(".py") and x[:-3] != "__init__"
        ]

    @classmethod
    def __snake_to_camel(cls, word: str) -> str:
        return "".join(x.capitalize() or "_" for x in word.split("_"))

    def __attempt_to_load_plugin(
        self, next_plugin_module: str, plugin_class_name: str, next_plugin_file: str
    ) -> None:
        """
        Attempt to cleanly load the specified plugin.
        """
        try:
            mod = __import__(next_plugin_module)
        except Exception as this_exception:
            raise BadPluginError(file_name=next_plugin_file) from this_exception

        if not hasattr(mod, plugin_class_name):
            raise BadPluginError(
                file_name=next_plugin_file, class_name=plugin_class_name
            ) from None
        my_class = getattr(mod, plugin_class_name)

        try:
            plugin_class_instance = my_class()
        except Exception as this_exception:
            raise BadPluginError(
                file_name=next_plugin_file,
                class_name=plugin_class_name,
                is_constructor=True,
            ) from this_exception
        self.__loaded_classes.append((plugin_class_instance, next_plugin_file))

    def __load_plugins(self, directory_to_search: str, plugin_files: List[str]) -> None:
        """
        Given an array of discovered modules, load them into the global namespace.
        """

        if os.path.abspath(directory_to_search) not in sys.path:
            sys.path.insert(0, os.path.abspath(directory_to_search))

        for next_plugin_file in plugin_files:
            next_plugin_module = next_plugin_file[:-3]
            plugin_class_name = self.__snake_to_camel(next_plugin_module)
            self.__attempt_to_load_plugin(
                next_plugin_module, plugin_class_name, next_plugin_file
            )

    def __determine_if_plugin_enabled(
        self,
        plugin_object: FoundPlugin,
        command_line_enabled_rules: Set[str],
        command_line_disabled_rules: Set[str],
        properties: ApplicationProperties,
    ) -> bool:
        """
        Given the enable and disable rule values, evaluate the enabled or disabled
        state of the plugin in proper order.
        """

        LOGGER.debug(
            "Plugin '%s', identifiers: %s",
            plugin_object.plugin_id,
            plugin_object.plugin_identifiers,
        )

        new_value = self.__handle_command_line_settings(
            plugin_object, command_line_disabled_rules, command_line_enabled_rules
        )
        if new_value is None:
            if plugin_specific_facade := self.__find_configuration_for_plugin(
                plugin_object, properties
            ):
                LOGGER.debug(
                    "Plugins specific configuration found, searching for key 'enabled'."
                )
                new_value = plugin_specific_facade.get_boolean_property(
                    "enabled", default_value=None
                )
                if new_value:
                    LOGGER.debug(
                        "Plugin specific key 'enabled' found, value is '%s'.",
                        str(new_value),
                    )
        if new_value is None:
            LOGGER.debug(
                "No other enable state found, setting to default of '%s'.",
                str(plugin_object.plugin_enabled_by_default),
            )

        return (
            plugin_object.plugin_enabled_by_default if new_value is None else new_value
        )

    @classmethod
    def __handle_command_line_settings(
        cls,
        plugin_object: FoundPlugin,
        command_line_disabled_rules: Set[str],
        command_line_enabled_rules: Set[str],
    ) -> Optional[bool]:
        new_value = None
        if command_line_disabled_rules:
            LOGGER.debug(
                "Disabled on command line: %s", str(command_line_disabled_rules)
            )
            for next_identifier in plugin_object.plugin_identifiers:
                if next_identifier in command_line_disabled_rules:
                    new_value = False
                    LOGGER.debug("Plugin is disabled from command line.")
                    break
        if new_value is None and command_line_enabled_rules:
            LOGGER.debug("Enabled on command line: %s", str(command_line_enabled_rules))
            for next_identifier in plugin_object.plugin_identifiers:
                if next_identifier in command_line_enabled_rules:
                    new_value = True
                    LOGGER.debug("Plugin is enabled from command line.")
                    break
        return new_value

    @classmethod
    def __verify_string_field(
        cls, plugin_instance: RulePlugin, field_name: str, field_value: Any
    ) -> None:
        """
        Verify that the detail field is a valid string.
        """

        if not isinstance(field_value, str):
            raise BadPluginError(
                class_name=type(plugin_instance).__name__, field_name=field_name
            )
        if not field_value:
            raise BadPluginError(
                class_name=type(plugin_instance).__name__,
                field_name=field_name,
                is_empty=True,
            )

    @classmethod
    def __verify_boolean_field(
        cls, plugin_instance: RulePlugin, field_name: str, field_value: Any
    ) -> None:
        """
        Verify that the detail field is a valid boolean.
        """

        if not isinstance(field_value, bool):
            raise BadPluginError(
                class_name=type(plugin_instance).__name__, field_name=field_name
            )

    @classmethod
    def __verify_integer_field(
        cls, plugin_instance: RulePlugin, field_name: str, field_value: Any
    ) -> None:
        """
        Verify that the detail field is a valid integer.
        """

        if not isinstance(field_value, int):
            raise BadPluginError(
                class_name=type(plugin_instance).__name__, field_name=field_name
            )

    def __get_plugin_details(
        self, plugin_instance: RulePlugin, instance_file_name: str
    ) -> FoundPlugin:
        """
        Query the plugin for details and verify that they are reasonable.
        """

        (
            plugin_id,
            plugin_name,
            plugin_description,
            plugin_enabled_by_default,
            plugin_version,
            plugin_interface_version,
            plugin_url,
            plugin_configuration,
            plugin_names,
            plugin_supports_fix,
            plugin_fix_level,
        ) = self.__unpack_plugin_details(plugin_instance)

        self.__verify_string_field(plugin_instance, "plugin_id", plugin_id)
        self.__verify_string_field(plugin_instance, "plugin_name", plugin_name)
        self.__verify_string_field(
            plugin_instance, "plugin_description", plugin_description
        )
        self.__verify_boolean_field(
            plugin_instance, "plugin_enabled_by_default", plugin_enabled_by_default
        )
        self.__verify_string_field(plugin_instance, "plugin_version", plugin_version)
        self.__verify_integer_field(
            plugin_instance, "plugin_interface_version", plugin_interface_version
        )
        if plugin_url:
            self.__verify_string_field(plugin_instance, "plugin_url", plugin_url)
        if plugin_configuration:
            self.__verify_string_field(
                plugin_instance, "plugin_configuration", plugin_configuration
            )
        if plugin_supports_fix:
            self.__verify_integer_field(
                plugin_instance, "plugin_fix_level", plugin_fix_level
            )

        plugin_object = FoundPlugin(
            plugin_id,
            plugin_names,
            plugin_description,
            plugin_instance,
            plugin_enabled_by_default,
            plugin_version,
            plugin_interface_version,
            instance_file_name,
            plugin_url,
            plugin_configuration,
            plugin_supports_fix,
            plugin_fix_level,
            [plugin_id, *plugin_names],
        )

        if plugin_object.plugin_interface_version not in (1, 2):
            raise BadPluginError(
                formatted_message=f"Plugin '{instance_file_name}' with an interface version "
                + f"('{plugin_object.plugin_interface_version}') that is not '1' or '2'."
            )

        return plugin_object

    # pylint: disable=too-many-locals
    def __unpack_plugin_details(self, plugin_instance: RulePlugin) -> Tuple[
        str,
        str,
        str,
        bool,
        str,
        int,
        Optional[str],
        Optional[str],
        List[str],
        bool,
        int,
    ]:
        try:
            instance_details = plugin_instance.get_details()
            plugin_supports_fix = False
            plugin_fix_level = -1
            (
                plugin_id,
                plugin_name,
                plugin_description,
                plugin_enabled_by_default,
                plugin_version,
                plugin_interface_version,
                plugin_url,
                plugin_configuration,
            ) = (
                instance_details.plugin_id,
                instance_details.plugin_name,
                instance_details.plugin_description,
                instance_details.plugin_enabled_by_default,
                instance_details.plugin_version,
                instance_details.plugin_interface_version,
                instance_details.plugin_url,
                instance_details.plugin_configuration,
            )
            if (
                isinstance(instance_details, PluginDetailsV2)
                and plugin_interface_version == 2
            ):
                plugin_supports_fix = instance_details.plugin_supports_fix
                plugin_fix_level = instance_details.plugin_fix_level
        except Exception as this_exception:
            raise BadPluginError(
                class_name=type(plugin_instance).__name__,
            ) from this_exception

        plugin_id = plugin_id.strip().lower()

        plugin_names = []
        for next_name in plugin_name.lower().split(","):
            if next_name := next_name.strip():
                plugin_names.append(next_name)

        return (
            plugin_id,
            plugin_name,
            plugin_description,
            plugin_enabled_by_default,
            plugin_version,
            plugin_interface_version,
            plugin_url,
            plugin_configuration,
            plugin_names,
            plugin_supports_fix,
            plugin_fix_level,
        )

    # pylint: enable=too-many-locals

    def __register_plugin_id(
        self, plugin_object: FoundPlugin, instance_file_name: str, next_key: str
    ) -> None:
        if not PluginManager.__id_regex.match(next_key):
            raise ValueError(
                f"Unable to register plugin '{instance_file_name}' with id '{next_key}' as "
                + "id is not a valid id in the form 'aannn' or 'aaannn'."
            )

        if next_key in self.__all_ids:
            found_plugin = self.__all_ids[next_key]
            raise ValueError(
                f"Unable to register plugin '{instance_file_name}' with id '{next_key}' as "
                + f"plugin '{found_plugin.plugin_file_name}' is already registered with that id."
            )
        self.__all_ids[next_key] = plugin_object

    def __register_plugin_names(
        self, plugin_object: FoundPlugin, instance_file_name: str
    ) -> None:
        for next_key in plugin_object.plugin_names:
            if not PluginManager.__name_regex.match(next_key):
                raise ValueError(
                    f"Unable to register plugin '{instance_file_name}' with name '{next_key}' as "
                    + "name is not a valid name in the form 'an-an'."
                )
            if next_key in self.__all_ids:
                found_plugin = self.__all_ids[next_key]
                raise ValueError(
                    f"Unable to register plugin '{instance_file_name}' with name '{next_key}' as "
                    + f"plugin '{found_plugin.plugin_file_name}' is already registered with that name."
                )
            self.__all_ids[next_key] = plugin_object

    # pylint: disable=too-many-arguments
    def __register_individual_plugin(
        self,
        plugin_instance: RulePlugin,
        instance_file_name: str,
        command_line_enabled_rules: Set[str],
        command_line_disabled_rules: Set[str],
        properties: ApplicationProperties,
    ) -> None:
        """
        Register an individual plugin for use.
        """

        plugin_object = self.__get_plugin_details(plugin_instance, instance_file_name)

        next_key = plugin_object.plugin_id
        self.__register_plugin_id(plugin_object, instance_file_name, next_key)
        self.__register_plugin_names(plugin_object, instance_file_name)
        if not plugin_object.plugin_description.strip():
            raise ValueError(
                f"Unable to register plugin '{instance_file_name}' with a description string that is blank."
            )
        if not PluginManager.__version_regex.match(plugin_object.plugin_version):
            raise ValueError(
                f"Unable to register plugin '{instance_file_name}' with a version string "
                + "that is not a valid semantic version."
            )

        self.__registered_plugins.append(plugin_object)
        if self.__determine_if_plugin_enabled(
            plugin_object,
            command_line_enabled_rules,
            command_line_disabled_rules,
            properties,
        ):
            self.__enabled_plugins.append(plugin_object)

    # pylint: enable=too-many-arguments

    def __register_plugins(
        self,
        enable_rules_from_command_line: str,
        disable_rules_from_command_line: str,
        properties: ApplicationProperties,
    ) -> None:
        """
        Scan the global namespace for all subclasses of the 'Plugin' class to use as
        plugins.
        """

        command_line_enabled_rules: Set[str] = set()
        command_line_disabled_rules: Set[str] = set()
        self.__registered_plugins = []
        self.__enabled_plugins = []
        self.__all_ids = {}
        if enable_rules_from_command_line:
            for next_rule_identifier in enable_rules_from_command_line.lower().split(
                ","
            ):
                command_line_enabled_rules.add(next_rule_identifier.strip())
        if disable_rules_from_command_line:
            for next_rule_identifier in disable_rules_from_command_line.lower().split(
                ","
            ):
                command_line_disabled_rules.add(next_rule_identifier.strip())

        for plugin_instance, instance_file_name in self.__loaded_classes:
            self.__register_individual_plugin(
                plugin_instance,
                instance_file_name,
                command_line_enabled_rules,
                command_line_disabled_rules,
                properties,
            )

        # Non-windows system may report these in weird orders, so sort them to have
        # a predictable order.
        self.__enabled_plugins = sorted(
            self.__enabled_plugins, reverse=False, key=lambda plugin: plugin.plugin_id
        )

    @property
    def all_plugin_ids(self) -> List[str]:
        """
        Get a list of all plugins by their id.
        """

        return [next_plugin.plugin_id for next_plugin in self.__registered_plugins]

    @classmethod
    def __find_configuration_for_plugin(
        cls,
        next_plugin: FoundPlugin,
        properties: ApplicationProperties,
        always_return_facade: bool = False,
    ) -> Optional[ApplicationPropertiesFacade]:
        plugin_specific_facade, first_facade = None, None
        for next_key_name in next_plugin.plugin_identifiers:
            plugin_section_title = (
                f"{PluginManager.__plugin_prefix}{properties.separator}"
                + f"{next_key_name}{properties.separator}"
            )
            section_facade_candidate = ApplicationPropertiesFacade(
                properties, plugin_section_title
            )
            if not first_facade:
                first_facade = section_facade_candidate
            if section_facade_candidate.property_names:
                plugin_specific_facade = section_facade_candidate
                break

        if always_return_facade and not plugin_specific_facade:
            plugin_specific_facade = first_facade
        return plugin_specific_facade

    def apply_configuration(self, properties: ApplicationProperties) -> None:
        """
        Apply any supplied configuration to each of the enabled plugins.
        """

        (
            self.__enabled_plugins_for_starting_new_file,
            self.__enabled_plugins_for_next_token,
            self.__enabled_plugins_for_next_line,
            self.__enabled_plugins_for_completed_file,
        ) = ([], [], [], [])

        for next_plugin in self.__enabled_plugins:
            try:
                plugin_specific_facade = self.__find_configuration_for_plugin(
                    next_plugin, properties, always_return_facade=True
                )

                assert plugin_specific_facade
                next_plugin.plugin_instance.set_configuration_map(
                    plugin_specific_facade
                )
                next_plugin.plugin_instance.initialize_from_config()
            except Exception as this_exception:
                raise BadPluginError(
                    next_plugin.plugin_id,
                    inspect.stack()[0].function,
                    cause=this_exception,
                ) from this_exception

            if next_plugin.plugin_instance.is_next_token_implemented_in_plugin:
                self.__enabled_plugins_for_next_token.append(next_plugin)
            if next_plugin.plugin_instance.is_next_line_implemented_in_plugin:
                self.__enabled_plugins_for_next_line.append(next_plugin)
            if next_plugin.plugin_instance.is_completed_file_implemented_in_plugin:
                self.__enabled_plugins_for_completed_file.append(next_plugin)
            if next_plugin.plugin_instance.is_starting_new_file_implemented_in_plugin:
                self.__enabled_plugins_for_starting_new_file.append(next_plugin)

    # pylint: disable=too-many-arguments
    def starting_new_file(
        self,
        file_being_started: str,
        fix_mode: bool = False,
        temp_output: Optional[TextIOWrapper] = None,
        fix_token_map: Optional[Dict[MarkdownToken, List[FixTokenRecord]]] = None,
        constraint_id_list: Optional[List[str]] = None,
    ) -> PluginScanContext:
        """
        Inform any listeners that a new current file has been started.
        """
        self.__document_pragmas = {}
        self.__document_pragma_ranges = []

        for next_plugin in self.__enabled_plugins_for_starting_new_file:
            if constraint_id_list and next_plugin.plugin_id not in constraint_id_list:
                continue
            try:
                next_plugin.plugin_instance.starting_new_file()
            except Exception as this_exception:
                raise BadPluginError(
                    next_plugin.plugin_id,
                    inspect.stack()[0].function,
                    cause=this_exception,
                ) from this_exception

        context = PluginScanContext(
            self, file_being_started, fix_mode, temp_output, fix_token_map
        )
        context.set_last_line_fixed(None)
        return context

    # pylint: enable=too-many-arguments

    def __completed_file_fix_mode_middle(
        self,
        context: PluginScanContext,
        current_fix_line: Optional[str],
        next_plugin: FoundPlugin,
        line_number: int,
    ) -> Tuple[Optional[str], FixLineRecord]:
        if current_fix_line is not None:
            plugin_id_list = ",".join(next_plugin.plugin_names)
            formatted_message = f"Plugin {next_plugin.plugin_id}({plugin_id_list}) attempted to rewrite a completion line."
            raise BadPluginError(  # pragma: no cover
                formatted_message=formatted_message
            )
        current_fix_line = context.current_fix_line
        line_append_record = FixLineRecord(
            "completed_file", line_number, next_plugin.plugin_id
        )
        return current_fix_line, line_append_record

    def __completed_file_fix_mode_end(
        self,
        context: PluginScanContext,
        current_fix_line: Optional[str],
        line_append_record: Optional[FixLineRecord],
    ) -> None:
        if current_fix_line is not None:
            if self.__show_fix_debug:
                replaced_line = current_fix_line.replace("\n", "\\n").replace(
                    "\t", "\\t"
                )
                print(f"cf-ltw:{replaced_line}:")
            context.file_output.write(current_fix_line)

            assert line_append_record is not None
            context.add_fix_line_record(line_append_record)

    def completed_file(
        self,
        context: PluginScanContext,
        line_number: int,
        context_map: Optional[Dict[str, PluginScanContext]] = None,
    ) -> None:
        """
        Inform any listeners that the current file has been completed.
        """
        context.line_number = line_number
        current_fix_line: Optional[str] = None
        line_append_record: Optional[FixLineRecord] = None

        # This skip added for the assert True.  Without the assert True, code coverage
        # believes that only one of the paths were covered.
        # sourcery skip: remove-assert-true
        for next_plugin in self.__enabled_plugins_for_completed_file:
            if context_map:
                if next_plugin.plugin_id not in context_map:
                    continue
                context = context_map[next_plugin.plugin_id]
            # if context.in_fix_mode and not next_plugin.plugin_supports_fix:
            #     continue
            try:
                if context.in_fix_mode:
                    context.set_current_fix_line(None)
                next_plugin.plugin_instance.completed_file(context)
                if context.in_fix_mode and context.current_fix_line is not None:
                    (
                        current_fix_line,
                        line_append_record,
                    ) = self.__completed_file_fix_mode_middle(
                        context, current_fix_line, next_plugin, line_number
                    )
                assert True
            except Exception as this_exception:
                raise BadPluginError(
                    next_plugin.plugin_id,
                    inspect.stack()[0].function,
                    cause=this_exception,
                ) from this_exception
        if context.in_fix_mode:
            self.__completed_file_fix_mode_end(
                context, current_fix_line, line_append_record
            )

    def __next_line_fix_mode_end(
        self,
        context: PluginScanContext,
        line: str,
        is_last_line_in_file: bool,
        was_newline_added_at_end_of_file: bool,
    ) -> None:
        was_line_fixed = True
        if is_last_line_in_file:
            if self.__show_fix_debug:
                print(
                    f"was_newline_added_at_end_of_file={was_newline_added_at_end_of_file}"
                )
                assert context.last_line_fixed is not None
                replaced_line = context.last_line_fixed.replace("\n", "\\n").replace(
                    "\t", "\\t"
                )
                print(f"fixed:{replaced_line}:")
            is_line_empty = not line
            was_modified = (
                context.last_line_fixed is not None
                and context.last_line_fixed.endswith("\n")
            )
            if self.__show_fix_debug:
                print(f"is_line_empty={is_line_empty}")
                print(f"was_modified={was_modified}")
            line_to_write = line
            was_line_fixed = not (is_line_empty and was_modified)
            # if was_newline_added_at_end_of_file and was_line_fixed:
            #     line_to_write += "\n"
        else:
            line_to_write = line + "\n"

        if self.__show_fix_debug:
            replaced_line = line_to_write.replace("\n", "\\n").replace("\t", "\\t")
            print(f"nl-ltw:{replaced_line}:")
        context.file_output.write(line_to_write)
        if was_line_fixed:
            context.set_last_line_fixed(line_to_write)

    def __next_line_fix_mode_before(
        self, context: PluginScanContext, line: str, next_plugin: FoundPlugin
    ) -> None:
        context.set_current_fix_line(None)
        if self.__show_fix_debug:
            replaced_line = line.replace("\n", "\\n").replace("\t", "\\t")
            print(f"{next_plugin.plugin_id}-before:{replaced_line}:")

    def __next_line_fix_mode_after(
        self,
        context: PluginScanContext,
        line: str,
        line_number: int,
        next_plugin: FoundPlugin,
    ) -> str:
        assert context.current_fix_line is not None
        line = context.current_fix_line
        if self.__show_fix_debug:
            replaced_line = line.replace("\n", "\\n").replace("\t", "\\t")
            print(f"{next_plugin.plugin_id}-after :{replaced_line}:")
        line_append_record = FixLineRecord(
            "next_line", line_number, next_plugin.plugin_id
        )
        context.add_fix_line_record(line_append_record)
        return line

    # pylint: disable=too-many-arguments
    def next_line(
        self,
        context: PluginScanContext,
        line_number: int,
        line: str,
        is_last_line_in_file: bool,
        was_newline_added_at_end_of_file: bool,
        context_map: Optional[Dict[str, PluginScanContext]] = None,
    ) -> None:
        """
        Inform any listeners that a new line has been loaded.
        """
        context.line_number = line_number
        for next_plugin in self.__enabled_plugins_for_next_line:
            if context_map:
                if next_plugin.plugin_id not in context_map:
                    continue
                context = context_map[next_plugin.plugin_id]
            # if context.in_fix_mode and not next_plugin.plugin_supports_fix:
            #     continue
            try:
                if context.in_fix_mode:
                    self.__next_line_fix_mode_before(context, line, next_plugin)
                next_plugin.plugin_instance.next_line(context, line)
                if context.current_fix_line is not None:
                    line = self.__next_line_fix_mode_after(
                        context, line, line_number, next_plugin
                    )
            except Exception as this_exception:
                actual_line = line if self.__show_stack_trace else None

                raise BadPluginError(
                    next_plugin.plugin_id,
                    inspect.stack()[0].function,
                    line_number=line_number,
                    actual_line=actual_line,
                    cause=this_exception,
                ) from this_exception

        if context.in_fix_mode:
            self.__next_line_fix_mode_end(
                context, line, is_last_line_in_file, was_newline_added_at_end_of_file
            )

    # pylint: enable=too-many-arguments

    def next_token(
        self,
        context: PluginScanContext,
        token: MarkdownToken,
        context_map: Optional[Dict[str, PluginScanContext]] = None,
    ) -> None:
        """
        Inform any listeners of a new token that has been processed.
        """
        for next_plugin in self.__enabled_plugins_for_next_token:
            if context_map:
                if next_plugin.plugin_id not in context_map:
                    continue
                context = context_map[next_plugin.plugin_id]

            # if context.in_fix_mode and not next_plugin.plugin_supports_fix:
            #     continue
            try:
                next_plugin.plugin_instance.next_token(context, token)
            except Exception as this_exception:
                actual_token = token if self.__show_stack_trace else None

                raise BadPluginError(
                    next_plugin.plugin_id,
                    inspect.stack()[0].function,
                    line_number=token.line_number,
                    column_number=token.column_number,
                    actual_token=actual_token,
                    cause=this_exception,
                ) from this_exception


# pylint: enable=too-many-instance-attributes
