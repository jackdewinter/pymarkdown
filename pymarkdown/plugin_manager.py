"""
Module to provide classes to deal with plugins.
"""
import argparse
import inspect
import logging
import os
import re
import sys
from abc import ABC, abstractmethod

from application_properties import ApplicationPropertiesFacade
from columnar import columnar

from pymarkdown.extensions.pragma_token import PragmaExtension
from pymarkdown.parser_helper import ParserHelper

LOGGER = logging.getLogger(__name__)

# pylint: disable=too-many-lines


# pylint: disable=too-few-public-methods
class ScanContext:
    """
    Class to provide context when reporting any errors.
    """

    def __init__(self, owning_manager, scan_file):
        self.owning_manager, self.scan_file, self.line_number = (
            owning_manager,
            scan_file,
            0,
        )
        self.__reported = []

    # pylint: disable=too-many-arguments
    def add_triggered_rule(
        self,
        scan_file,
        line_number,
        column_number,
        rule_id,
        rule_name,
        rule_description,
        extra_error_information,
    ):
        """
        Add the triggering information for a rule.
        """
        new_entry = (
            scan_file,
            line_number,
            column_number,
            rule_id,
            rule_name,
            rule_description,
            extra_error_information,
        )
        self.__reported.append(new_entry)

    # pylint: enable=too-many-arguments

    def report_on_triggered_rules(self):
        """
        Report on the various points where rules were triggered,
        in sorted order.
        """
        reported_and_sorted = sorted(self.__reported)

        for next_entry in reported_and_sorted:
            self.owning_manager.log_scan_failure(
                scan_file=next_entry[0],
                line_number=next_entry[1],
                column_number=next_entry[2],
                rule_id=next_entry[3],
                rule_name=next_entry[4],
                rule_description=next_entry[5],
                extra_error_information=next_entry[6],
            )
        self.__reported.clear()


# pylint: enable=too-few-public-methods


class BadPluginError(Exception):
    """
    Class to allow for a critical error within a plugin to be encapsulated
    and reported.
    """

    # pylint: disable=too-many-arguments, too-many-branches
    def __init__(
        self,
        plugin_id=None,
        plugin_action=None,
        file_name=None,
        class_name=None,
        field_name=None,
        is_constructor=False,
        is_empty=False,
        formatted_message=None,
        line_number=0,
        column_number=0,
        actual_line=None,
        actual_token=None,
        cause=None,
    ):

        if not formatted_message:
            if file_name:
                if class_name:
                    if is_constructor:
                        formatted_message = f"Plugin file named '{file_name}' threw an exception in the constructor for the class '{class_name}'."
                    else:
                        formatted_message = f"Plugin file named '{file_name}' does not contain a class named '{class_name}'."
                else:
                    formatted_message = (
                        f"Plugin file named '{file_name}' cannot be loaded."
                    )
            elif class_name:
                if field_name:
                    if is_empty:
                        formatted_message = f"Plugin class '{class_name}' returned an empty value for field name '{field_name}'."
                    else:
                        formatted_message = f"Plugin class '{class_name}' returned an improperly typed value for field name '{field_name}'."
                else:
                    formatted_message = f"Plugin class '{class_name}' had a critical failure loading the plugin details."
            else:
                if cause and isinstance(cause, ValueError):
                    formatted_message = str(cause)
                else:
                    formatted_message = f"Plugin id '{plugin_id.upper()}' had a critical failure during the '{plugin_action}' action."
            if line_number:
                position_message = (
                    f"({line_number},{column_number})"
                    if column_number
                    else f"(Line {line_number})"
                )
                formatted_message = f"{position_message}: {formatted_message}"
            if actual_line:
                formatted_message = f"{formatted_message}\nActual Line: {actual_line}"
            if actual_token:
                formatted_message = f"{formatted_message}\nActual Token: {ParserHelper.make_value_visible(actual_token)}"
        super().__init__(formatted_message)

    # pylint: enable=too-many-arguments, too-many-branches


class Plugin(ABC):
    """
    Class to provide structure to scan through a file.
    Based off of concepts from https://github.com/hiddenillusion/example-code/commit/3e2daada652fe9b487574c784e0924bd5fcfe667
    """

    def __init__(self):
        (
            self.__plugin_specific_facade,
            self.__is_next_token_implemented_in_plugin,
            self.__is_next_line_implemented_in_plugin,
            self.__is_starting_new_file_implemented_in_plugin,
            self.__is_completed_file_implemented_in_plugin,
        ) = (None, True, True, True, True)

    @abstractmethod
    def get_details(self):
        """
        Get the details for the plugin.
        """

    @property
    def plugin_configuration(self):
        """
        Get the configuration facade associated with this plugin.
        """
        return self.__plugin_specific_facade

    def set_configuration_map(self, plugin_specific_facade):
        """
        Set the configuration map with values for the plugin.
        """
        self.__plugin_specific_facade = plugin_specific_facade

        self.__is_next_token_implemented_in_plugin = (
            "next_token" in self.__class__.__dict__.keys()
        )
        self.__is_next_line_implemented_in_plugin = (
            "next_line" in self.__class__.__dict__.keys()
        )
        self.__is_starting_new_file_implemented_in_plugin = (
            "starting_new_file" in self.__class__.__dict__.keys()
        )
        self.__is_completed_file_implemented_in_plugin = (
            "completed_file" in self.__class__.__dict__.keys()
        )

    @property
    def is_starting_new_file_implemented_in_plugin(self):
        """
        Return whether the starting_new_file function is implemented in the plugin.
        """
        return self.__is_starting_new_file_implemented_in_plugin

    @property
    def is_next_line_implemented_in_plugin(self):
        """
        Return whether the next_line function is implemented in the plugin.
        """
        return self.__is_next_line_implemented_in_plugin

    @property
    def is_next_token_implemented_in_plugin(self):
        """
        Return whether the next_token function is implemented in the plugin.
        """
        return self.__is_next_token_implemented_in_plugin

    @property
    def is_completed_file_implemented_in_plugin(self):
        """
        Return whether the completed_file function is implemented in the plugin.
        """
        return self.__is_completed_file_implemented_in_plugin

    def report_next_line_error(
        self, context, column_number, line_number_delta=0, extra_error_information=None
    ):
        """
        Report an error with the current line being processed.
        """
        context.add_triggered_rule(
            context.scan_file,
            context.line_number + line_number_delta,
            column_number,
            self.get_details().plugin_id,
            self.get_details().plugin_name,
            self.get_details().plugin_description,
            extra_error_information,
        )

    # pylint: disable=too-many-arguments
    def report_next_token_error(
        self,
        context,
        token,
        extra_error_information=None,
        line_number_delta=0,
        column_number_delta=0,
        use_original_position=False,
    ):
        """
        Report an error with the current token being processed.
        """
        context.add_triggered_rule(
            context.scan_file,
            (token.original_line_number if use_original_position else token.line_number)
            + line_number_delta,
            (
                token.original_column_number
                if use_original_position
                else token.column_number
            )
            + column_number_delta
            if column_number_delta >= 0
            else -column_number_delta,
            self.get_details().plugin_id,
            self.get_details().plugin_name,
            self.get_details().plugin_description,
            extra_error_information,
        )

    # pylint: enable=too-many-arguments

    def initialize_from_config(self):
        """
        Event to allow the plugin to load configuration information.
        """

    def starting_new_file(self):
        """
        Event that the a new file to be scanned is starting.
        """

    def completed_file(self, context):
        """
        Event that the file being currently scanned is now completed.
        """

    def next_line(self, context, line):
        """
        Event that a new line is being processed.
        """

    def next_token(self, context, token):
        """
        Event that a new token is being processed.
        """


# pylint: disable=too-few-public-methods,too-many-instance-attributes
class PluginDetails:
    """
    Class to provide details about a plugin, supplied by the plugin.
    """

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        plugin_id,
        plugin_name,
        plugin_description,
        plugin_enabled_by_default,
        plugin_version,
        plugin_interface_version,
        plugin_url=None,
        plugin_configuration=None,
    ):
        (
            self.plugin_id,
            self.plugin_name,
            self.plugin_description,
            self.plugin_enabled_by_default,
            self.plugin_version,
            self.plugin_interface_version,
            self.plugin_url,
            self.plugin_configuration,
        ) = (
            plugin_id,
            plugin_name,
            plugin_description,
            plugin_enabled_by_default,
            plugin_version,
            plugin_interface_version,
            plugin_url,
            plugin_configuration,
        )

    # pylint: enable=too-many-arguments


# pylint: enable=too-few-public-methods,too-many-instance-attributes


# pylint: disable=too-few-public-methods,too-many-instance-attributes
class FoundPlugin:
    """
    Encapsulation of a plugin that was discovered.  While similar to the PluginDetails
    class, this is meant for an internal representation of the plugin, and not the
    external information provided.
    """

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        plugin_id,
        plugin_name,
        plugin_description,
        plugin_instance,
        plugin_enabled_by_default,
        plugin_version,
        plugin_interface_version,
        instance_file_name,
        plugin_url,
        plugin_configuration,
    ):
        """
        Initializes a new instance of the FoundPlugin class.
        """
        (
            self.__plugin_id,
            self.__plugin_names,
            self.__plugin_description,
            self.__plugin_instance,
            self.__plugin_enabled_by_default,
            self.__plugin_version,
            self.__plugin_interface_version,
            self.__plugin_file_name,
            self.__plugin_url,
            self.__plugin_configuration,
        ) = (
            plugin_id.strip().lower(),
            [],
            plugin_description,
            plugin_instance,
            plugin_enabled_by_default,
            plugin_version,
            plugin_interface_version,
            instance_file_name,
            plugin_url,
            plugin_configuration,
        )
        for next_name in plugin_name.lower().split(","):
            next_name = next_name.strip()
            if next_name:
                self.__plugin_names.append(next_name)

    # pylint: enable=too-many-arguments

    @property
    def plugin_id(self):
        """
        Gets the id associated with the plugin.
        """
        return self.__plugin_id

    @property
    def plugin_names(self):
        """
        Gets the names associated with the plugin.
        """
        return self.__plugin_names

    @property
    def plugin_identifiers(self):
        """
        Gets the identifiers (id+names) for the plugin.
        """
        plugin_keys = [self.plugin_id]
        plugin_keys.extend(self.plugin_names)
        return plugin_keys

    @property
    def plugin_description(self):
        """
        Gets the description of the plugin.
        """
        return self.__plugin_description

    @property
    def plugin_instance(self):
        """
        Gets the actual instance of the plugin.
        """
        return self.__plugin_instance

    @property
    def plugin_file_name(self):
        """
        Gets the filename where the plugin's class is stored.
        """
        return self.__plugin_file_name

    @property
    def plugin_version(self):
        """
        Gets the version of the plugin.
        """
        return self.__plugin_version

    @property
    def plugin_interface_version(self):
        """
        Gets the interface version of the plugin.
        """
        return self.__plugin_interface_version

    @property
    def plugin_url(self):
        """
        Gets the optional url for the plugin.
        """
        return self.__plugin_url

    @property
    def plugin_configuration(self):
        """
        Gets the optional configuration items for the plugin.
        """
        return self.__plugin_configuration

    @property
    def plugin_enabled_by_default(self):
        """
        Gets a value indicating whether the plugin is enabled by default.
        """
        return self.__plugin_enabled_by_default


# pylint: enable=too-few-public-methods,too-many-instance-attributes


# pylint: disable=too-many-instance-attributes
class PluginManager:
    """
    Manager object to take care of load and accessing plugin modules.
    """

    __plugin_prefix = "plugins"
    __root_subparser_name = "pm_subcommand"
    __argparse_subparser = None
    __id_regex = re.compile("^[a-z]{2,3}[0-9]{3,3}$")
    __name_regex = re.compile("^[a-zA-Z0-9][a-zA-Z0-9-]*[a-zA-Z0-9]$")
    __filter_regex = re.compile("^[a-zA-Z0-9-]+$")
    __version_regex = re.compile("^(0|[1-9]\\d*)\\.(0|[1-9]\\d*)\\.(0|[1-9]\\d*)$")

    def __init__(self):
        (
            self.__registered_plugins,
            self.__enabled_plugins,
            self.__enabled_plugins_for_starting_new_file,
            self.__enabled_plugins_for_next_token,
            self.__enabled_plugins_for_next_line,
            self.__enabled_plugins_for_completed_file,
            self.__loaded_classes,
            self.number_of_scan_failures,
            self.number_of_pragma_failures,
            self.__show_stack_trace,
            self.__document_pragmas,
            self.__all_ids,
        ) = (None, None, None, None, None, None, None, None, None, False, None, None)

    # pylint: disable=too-many-arguments
    def initialize(
        self,
        directory_to_search,
        additional_paths,
        enable_rules_from_command_line,
        disable_rules_from_command_line,
        properties,
        show_stack_trace,
    ):
        """
        Initializes the manager by scanning for plugins, loading them, and registering them.
        """
        (
            self.number_of_scan_failures,
            self.number_of_pragma_failures,
            self.__loaded_classes,
            self.__show_stack_trace,
        ) = (0, 0, [], show_stack_trace)

        plugin_files = self.__find_eligible_plugins_in_directory(directory_to_search)
        self.__load_plugins(directory_to_search, plugin_files)

        all_additional_paths = []
        if additional_paths:
            all_additional_paths.extend(additional_paths)
        more_paths = properties.get_string_property("plugins.additional_paths")
        if more_paths:
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
    def argparse_subparser_name():
        """
        Gets the name of the subparser used to handle these plugins.
        """
        return "plugins"

    @staticmethod
    def __list_filter_type(argument):
        test_argument = argument.replace("*", "").replace("?", "")
        if PluginManager.__filter_regex.match(test_argument):
            return argument
        raise argparse.ArgumentTypeError(
            f"Value '{argument}' is not a valid pattern for an id or a name."
        )

    @staticmethod
    def __info_filter_type(argument):
        if PluginManager.__id_regex.match(argument) or PluginManager.__name_regex.match(
            argument
        ):
            return argument
        raise argparse.ArgumentTypeError(
            f"Value '{argument}' is not a valid id or name."
        )

    @staticmethod
    def add_argparse_subparser(subparsers):
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

    # pylint: disable=too-many-locals,too-many-branches
    def __handle_argparse_subparser_list(self, args):
        list_re = None
        if args.list_filter:
            list_re = re.compile(
                "^" + args.list_filter.replace("*", ".*").replace("?", ".") + "$"
            )

        show_rows = []
        ids = self.all_plugin_ids
        ids.sort()
        for next_plugin_id in ids:
            # if next_plugin_id.startswith("md9"):
            #     continue
            next_plugin_list = []
            for next_plugin in self.__registered_plugins:
                if next_plugin.plugin_id == next_plugin_id:
                    next_plugin_list.append(next_plugin)
            assert len(next_plugin_list) == 1
            next_plugin = next_plugin_list[0]
            if next_plugin.plugin_version == "0.0.0" and not args.show_all:
                continue
            does_match = True
            if list_re:
                does_match = list_re.match(next_plugin_id)
                if not does_match:
                    for next_name in next_plugin.plugin_names:
                        does_match = list_re.match(next_name)
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
                ]
                show_rows.append(display_row)

        if show_rows:
            headers = [
                "id",
                "names",
                "enabled\n(default)",
                "enabled\n(current)",
                "version",
            ]
            table = columnar(show_rows, headers, no_borders=True)
            split_rows = table.split("\n")
            new_rows = [next_row.rstrip() for next_row in split_rows]
            print("\n".join(new_rows))
        else:
            print(
                f"No plugin rule identifiers matches the pattern '{args.list_filter}'."
            )

    # pylint: enable=too-many-locals,too-many-branches

    def __handle_argparse_subparser_info(self, args):
        found_plugin = list(
            filter(
                lambda x: args.info_filter in x.plugin_identifiers,
                self.__registered_plugins,
            )
        )
        if not found_plugin:
            print(
                f"Unable to find a plugin with an id or name of '{args.info_filter}'."
            )
            return 1

        found_plugin = found_plugin[0]
        show_rows = []
        next_row = ["Id", found_plugin.plugin_id]
        show_rows.append(next_row)
        next_row = ["Name(s)", ",".join(found_plugin.plugin_names)]
        show_rows.append(next_row)
        next_row = ["Short Description", found_plugin.plugin_description]
        show_rows.append(next_row)
        if found_plugin.plugin_url:
            next_row = ["Description Url", found_plugin.plugin_url]
            show_rows.append(next_row)
        if found_plugin.plugin_configuration:
            next_row = ["Configuration Items", found_plugin.plugin_configuration]
            show_rows.append(next_row)

        headers = ["Item", "Description"]
        table = columnar(show_rows, headers, no_borders=True)
        split_rows = table.split("\n")
        new_rows = [next_row.rstrip() for next_row in split_rows]
        print("\n".join(new_rows))
        return 0

    def handle_argparse_subparser(self, args):
        """
        Handle the parsing for this subparser.
        """
        subparser_value = getattr(args, PluginManager.__root_subparser_name)
        return_code = 0
        if subparser_value == "list":
            self.__handle_argparse_subparser_list(args)
        elif subparser_value == "info":
            return_code = self.__handle_argparse_subparser_info(args)
        else:
            PluginManager.__argparse_subparser.print_help()
            sys.exit(2)
        return return_code

    # pylint: disable=too-many-arguments
    def log_scan_failure(
        self,
        scan_file,
        line_number,
        column_number,
        rule_id,
        rule_name,
        rule_description,
        extra_error_information=None,
    ):
        """
        Log the scan failure in the appropriate format.
        """

        if self.__document_pragmas and line_number in self.__document_pragmas:
            id_set = self.__document_pragmas[line_number]
            rule_id = rule_id.lower()
            if rule_id in id_set:
                return

        extra_info = f" [{extra_error_information}]" if extra_error_information else ""

        print(
            "{0}:{1}:{2}: {3}: {4}{5} ({6})".format(
                scan_file,
                line_number,
                column_number,
                rule_id.upper(),
                rule_description,
                extra_info,
                rule_name,
            )
        )
        self.number_of_scan_failures += 1

    # pylint: enable=too-many-arguments

    def log_pragma_failure(self, scan_file, line_number, pragma_error):
        """
        Log the pragma failure in the appropriate format.
        """

        print("{0}:{1}:1: INLINE: {2}".format(scan_file, line_number, pragma_error))
        self.number_of_pragma_failures += 1

    # pylint: disable=too-many-locals
    def compile_pragmas(self, scan_file, pragma_lines):
        """
        Go through the list of extracted pragmas and compile them.
        """

        for next_line_number in pragma_lines.keys():
            PragmaExtension.compile_single_pragma(
                scan_file,
                next_line_number,
                pragma_lines,
                self.__all_ids,
                self.__document_pragmas,
                self.log_pragma_failure,
            )

    # pylint: enable=too-many-locals

    @classmethod
    def __find_eligible_plugins_in_directory(cls, directory_to_search):
        """
        Given a directory to search, scan for eligible modules to load later.
        """

        return [
            x
            for x in os.listdir(directory_to_search)
            if x.endswith(".py") and x[0:-3] != "__init__"
        ]

    @classmethod
    def __snake_to_camel(cls, word):

        return "".join(x.capitalize() or "_" for x in word.split("_"))

    def __attempt_to_load_plugin(
        self, next_plugin_module, plugin_class_name, next_plugin_file
    ):
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

    def __load_plugins(self, directory_to_search, plugin_files):
        """
        Given an array of discovered modules, load them into the global namespace.
        """

        if os.path.abspath(directory_to_search) not in sys.path:
            sys.path.insert(0, os.path.abspath(directory_to_search))

        for next_plugin_file in plugin_files:
            next_plugin_module = next_plugin_file[0:-3]
            plugin_class_name = self.__snake_to_camel(next_plugin_module)
            self.__attempt_to_load_plugin(
                next_plugin_module, plugin_class_name, next_plugin_file
            )

    def __determine_if_plugin_enabled(
        self,
        plugin_object,
        command_line_enabled_rules,
        command_line_disabled_rules,
        properties,
    ):
        """
        Given the enable and disable rule values, evaluate the enabled or disabled
        state of the plugin in proper order.
        """

        new_value = None
        LOGGER.debug(
            "Plugin '%s', identifiers: %s",
            plugin_object.plugin_id,
            plugin_object.plugin_identifiers,
        )

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
        if new_value is None:
            plugin_specific_facade = self.__find_configuration_for_plugin(
                plugin_object, properties
            )
            if plugin_specific_facade:
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

    # pylint: enable=too-many-arguments

    @classmethod
    def __verify_string_field(cls, plugin_instance, field_name, field_value):
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
    def __verify_boolean_field(cls, plugin_instance, field_name, field_value):
        """
        Verify that the detail field is a valid boolean.
        """

        if not isinstance(field_value, bool):
            raise BadPluginError(
                class_name=type(plugin_instance).__name__, field_name=field_name
            )

    @classmethod
    def __verify_integer_field(cls, plugin_instance, field_name, field_value):
        """
        Verify that the detail field is a valid integer.
        """

        if not isinstance(field_value, int):
            raise BadPluginError(
                class_name=type(plugin_instance).__name__, field_name=field_name
            )

    def __get_plugin_details(self, plugin_instance, instance_file_name):
        """
        Query the plugin for details and verify that they are reasonable.
        """

        try:
            instance_details = plugin_instance.get_details()
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
        except Exception as this_exception:
            raise BadPluginError(
                class_name=type(plugin_instance).__name__,
            ) from this_exception

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

        plugin_object = FoundPlugin(
            plugin_id,
            plugin_name,
            plugin_description,
            plugin_instance,
            plugin_enabled_by_default,
            plugin_version,
            plugin_interface_version,
            instance_file_name,
            plugin_url,
            plugin_configuration,
        )

        if plugin_object.plugin_interface_version != 1:
            raise BadPluginError(
                formatted_message=f"Plugin '{instance_file_name}' with an interface version ('{plugin_object.plugin_interface_version}') that is not '1'."
            )

        return plugin_object

    # pylint: disable=too-many-arguments
    def __register_individual_plugin(
        self,
        plugin_instance,
        instance_file_name,
        command_line_enabled_rules,
        command_line_disabled_rules,
        properties,
    ):
        """
        Register an individual plugin for use.
        """

        plugin_object = self.__get_plugin_details(plugin_instance, instance_file_name)

        next_key = plugin_object.plugin_id
        if not PluginManager.__id_regex.match(next_key):
            raise ValueError(
                f"Unable to register plugin '{instance_file_name}' with id '{next_key}' as id is not a valid id in the form 'aannn' or 'aaannn'."
            )

        if next_key in self.__all_ids:
            found_plugin = self.__all_ids[next_key]
            raise ValueError(
                f"Unable to register plugin '{instance_file_name}' with id '{next_key}' as plugin '{found_plugin.plugin_file_name}' is already registered with that id."
            )
        self.__all_ids[next_key] = plugin_object

        for next_key in plugin_object.plugin_names:
            if not PluginManager.__name_regex.match(next_key):
                raise ValueError(
                    f"Unable to register plugin '{instance_file_name}' with name '{next_key}' as name is not a valid name in the form 'an-an'."
                )
            if next_key in self.__all_ids:
                found_plugin = self.__all_ids[next_key]
                raise ValueError(
                    f"Unable to register plugin '{instance_file_name}' with name '{next_key}' as plugin '{found_plugin.plugin_file_name}' is already registered with that name."
                )
            self.__all_ids[next_key] = plugin_object
        if not plugin_object.plugin_description.strip():
            raise ValueError(
                f"Unable to register plugin '{instance_file_name}' with a description string that is blank."
            )
        if not PluginManager.__version_regex.match(plugin_object.plugin_version):
            raise ValueError(
                f"Unable to register plugin '{instance_file_name}' with a version string that is not a valid semantic version."
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
        enable_rules_from_command_line,
        disable_rules_from_command_line,
        properties,
    ):
        """
        Scan the global namespace for all subclasses of the 'Plugin' class to use as
        plugins.
        """

        (
            command_line_enabled_rules,
            command_line_disabled_rules,
            self.__registered_plugins,
            self.__enabled_plugins,
            self.__all_ids,
        ) = (set(), set(), [], [], {})
        if enable_rules_from_command_line:
            for next_rule_identifier in enable_rules_from_command_line.lower().split(
                ","
            ):
                command_line_enabled_rules.add(next_rule_identifier)
        if disable_rules_from_command_line:
            for next_rule_identifier in disable_rules_from_command_line.lower().split(
                ","
            ):
                command_line_disabled_rules.add(next_rule_identifier)

        for plugin_instance, instance_file_name in self.__loaded_classes:
            self.__register_individual_plugin(
                plugin_instance,
                instance_file_name,
                command_line_enabled_rules,
                command_line_disabled_rules,
                properties,
            )

    @property
    def all_plugin_ids(self):
        """
        Get a list of all plugins by their id.
        """

        return [next_plugin.plugin_id for next_plugin in self.__registered_plugins]

    @classmethod
    def __find_configuration_for_plugin(
        cls, next_plugin, properties, always_return_facade=False
    ):
        plugin_specific_facade = None
        first_facade = None
        for next_key_name in next_plugin.plugin_identifiers:
            plugin_section_title = f"{PluginManager.__plugin_prefix}{properties.separator}{next_key_name}{properties.separator}"
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

    def apply_configuration(self, properties):
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

    def starting_new_file(self, file_being_started):
        """
        Inform any listeners that a new current file has been started.
        """
        self.__document_pragmas = {}
        for next_plugin in self.__enabled_plugins_for_starting_new_file:
            try:
                next_plugin.plugin_instance.starting_new_file()
            except Exception as this_exception:
                raise BadPluginError(
                    next_plugin.plugin_id,
                    inspect.stack()[0].function,
                    cause=this_exception,
                ) from this_exception

        return ScanContext(self, file_being_started)

    def completed_file(self, context, line_number):
        """
        Inform any listeners that the current file has been completed.
        """
        context.line_number = line_number
        for next_plugin in self.__enabled_plugins_for_completed_file:
            try:
                next_plugin.plugin_instance.completed_file(context)
            except Exception as this_exception:
                raise BadPluginError(
                    next_plugin.plugin_id,
                    inspect.stack()[0].function,
                    cause=this_exception,
                ) from this_exception

    def next_line(self, context, line_number, line):
        """
        Inform any listeners that a new line has been loaded.
        """
        context.line_number = line_number
        for next_plugin in self.__enabled_plugins_for_next_line:
            try:
                next_plugin.plugin_instance.next_line(context, line)
            except Exception as this_exception:
                actual_line = line if self.__show_stack_trace else None

                raise BadPluginError(
                    next_plugin.plugin_id,
                    inspect.stack()[0].function,
                    line_number=line_number,
                    actual_line=actual_line,
                    cause=this_exception,
                ) from this_exception

    def next_token(self, context, token):
        """
        Inform any listeners of a new token that has been processed.
        """
        for next_plugin in self.__enabled_plugins_for_next_token:
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
