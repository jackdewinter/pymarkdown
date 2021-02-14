"""
Module to provide classes to deal with plugins.
"""
import inspect
import os
import sys
from abc import ABC, abstractmethod


# pylint: disable=too-few-public-methods
class ScanContext:
    """
    Class to provide context when reporting any errors.
    """

    def __init__(self, owning_manager, scan_file):
        self.owning_manager = owning_manager
        self.scan_file = scan_file

        self.line_number = 0


# pylint: enable=too-few-public-methods


class BadPluginError(Exception):
    """
    Class to allow for a critical error within a plugin to be encapsulated
    and reported.
    """

    # pylint: disable=too-many-arguments
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
    ):

        if not formatted_message:
            if file_name:
                if class_name:
                    if is_constructor:
                        formatted_message = (
                            "Plugin file named '"
                            + file_name
                            + "' threw an exception in the constructor for the class '"
                            + class_name
                            + "'."
                        )
                    else:
                        formatted_message = (
                            "Plugin file named '"
                            + file_name
                            + "' does not contain a class named '"
                            + class_name
                            + "'."
                        )
                else:
                    formatted_message = (
                        "Plugin file named '" + file_name + "' cannot be loaded."
                    )
            elif class_name:
                if field_name:
                    if is_empty:
                        formatted_message = (
                            "Plugin class '"
                            + class_name
                            + "' returned an empty value for field name '"
                            + field_name
                            + "'."
                        )
                    else:
                        formatted_message = (
                            "Plugin class '"
                            + class_name
                            + "' returned an improperly typed value for field name '"
                            + field_name
                            + "'."
                        )
                else:
                    formatted_message = (
                        "Plugin class '"
                        + class_name
                        + "' had a critical failure loading the plugin details."
                    )
            else:
                formatted_message = (
                    "Plugin id '"
                    + plugin_id
                    + "' had a critical failure during the '"
                    + str(plugin_action)
                    + "' action."
                )
        super().__init__(formatted_message)

    # pylint: enable=too-many-arguments


class Plugin(ABC):
    """
    Class to provide structure to scan through a file.
    Based off of concepts from https://github.com/hiddenillusion/example-code/commit/3e2daada652fe9b487574c784e0924bd5fcfe667
    """

    def __init__(self):
        self.__scan_context = None
        self.__configuration_map = None
        self.__is_next_token_implemented_in_plugin = True
        self.__is_next_line_implemented_in_plugin = True

    @abstractmethod
    def get_details(self):
        """
        Get the details for the plugin.
        """

    def get_configuration_value(self, value_name, default_value, valid_values=None):
        """
        From the configuration map, try and grab the specified value from the map.
        If the value is not present or is not the same type as the default value,
        the default value will be returned.
        """
        configuration_value = default_value
        if value_name in self.__configuration_map:
            retrieved_value = self.__configuration_map[value_name]
            if isinstance(retrieved_value, type(default_value)):
                if valid_values is None or retrieved_value in valid_values:
                    configuration_value = retrieved_value
        return configuration_value

    def set_configuration_map(self, map_to_use):
        """
        Set the configuration map with values for the plugin.
        """
        self.__configuration_map = map_to_use

        self.__is_next_token_implemented_in_plugin = (
            "next_token" in self.__class__.__dict__.keys()
        )
        self.__is_next_line_implemented_in_plugin = (
            "next_line" in self.__class__.__dict__.keys()
        )

    def set_context(self, context):
        """
        Set the context to use for any error reporting.
        """
        self.__scan_context = context

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

    def report_next_line_error(self, column_number, line_number_delta=0):
        """
        Report an error with the current line being processed.
        """
        self.__scan_context.owning_manager.log_scan_failure(
            self.__scan_context.scan_file,
            self.__scan_context.line_number + line_number_delta,
            column_number,
            self.get_details().plugin_id,
            self.get_details().plugin_name,
            self.get_details().plugin_description,
        )

    def report_next_token_error(self, token, extra_error_information=None):
        """
        Report an error with the current token being processed.
        """
        self.__scan_context.owning_manager.log_scan_failure(
            self.__scan_context.scan_file,
            token.line_number,
            token.column_number,
            self.get_details().plugin_id,
            self.get_details().plugin_name,
            self.get_details().plugin_description,
            extra_error_information=extra_error_information,
        )

    def initialize_from_config(self):
        """
        Event to allow the plugin to load configuration information.
        """

    def starting_new_file(self):
        """
        Event that the a new file to be scanned is starting.
        """

    def completed_file(self):
        """
        Event that the file being currently scanned is now completed.
        """

    def next_line(self, line):
        """
        Event that a new line is being processed.
        """

    def next_token(self, token):
        """
        Event that a new token is being processed.
        """


# pylint: disable=too-few-public-methods
class PluginDetails:
    """
    Class to provide details about a plugin, supplied by the plugin.
    """

    def __init__(
        self, plugin_id, plugin_name, plugin_description, plugin_enabled_by_default
    ):
        self.plugin_id = plugin_id
        self.plugin_name = plugin_name
        self.plugin_description = plugin_description
        self.plugin_enabled_by_default = plugin_enabled_by_default


# pylint: enable=too-few-public-methods


# pylint: disable=too-few-public-methods
class FoundPlugin:
    """
    Encapsulation of a plugin that was discovered.  While similar to the PluginDetails
    class, this is meant for an internal representation of the plugin, and not the
    external information provided.
    """

    def __init__(self, plugin_id, plugin_name, plugin_description, plugin_instance):
        self.plugin_id = plugin_id
        self.plugin_name = plugin_name
        self.plugin_description = plugin_description
        self.plugin_instance = plugin_instance


# pylint: enable=too-few-public-methods


class PluginManager:
    """
    Manager object to take care of load and accessing plugin modules.
    """

    def __init__(self):
        self.__registered_plugins = None
        self.__enabled_plugins = None
        self.__enabled_plugins_for_next_token = None
        self.__enabled_plugins_for_next_line = None
        self.__loaded_classes = None
        self.number_of_scan_failures = None

    def initialize(
        self, directory_to_search, additional_paths, enable_rules, disable_rules
    ):
        """
        Initializes the manager by scanning for plugins, loading them, and registering them.
        """
        self.number_of_scan_failures = 0

        self.__loaded_classes = []

        plugin_files = self.__find_eligible_plugins_in_directory(directory_to_search)
        self.__load_plugins(directory_to_search, plugin_files)

        if additional_paths:
            for next_additional_plugin in additional_paths:
                if not os.path.exists(next_additional_plugin):
                    formatted_message = (
                        "Plugin path '" + next_additional_plugin + "' does not exist."
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

        self.__register_plugins(enable_rules, disable_rules)

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

        extra_info = ""
        if extra_error_information:
            extra_info = " [" + extra_error_information + "]"

        print(
            "{0}:{1}:{2}: {3}: {4}{5} ({6})".format(
                scan_file,
                line_number,
                column_number,
                rule_id,
                rule_description,
                extra_info,
                rule_name,
            )
        )
        self.number_of_scan_failures += 1

    # pylint: enable=too-many-arguments

    @classmethod
    def __find_eligible_plugins_in_directory(cls, directory_to_search):
        """
        Given a directory to search, scan for eligible modules to load later.
        """

        plugin_files = [
            x
            for x in os.listdir(directory_to_search)
            if x.endswith(".py") and x[0:-3] != "__init__"
        ]
        return plugin_files

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
        self.__loaded_classes.append(plugin_class_instance)

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

    @classmethod
    def __determine_if_plugin_enabled(
        cls,
        plugin_enabled,
        plugin_object,
        command_line_enabled_rules,
        command_line_disabled_rules,
    ):
        """
        Given the enable and disable rules values, evaluate the enabled or disabled
        state of the plugin in proper order.
        """

        if (
            plugin_object.plugin_id in command_line_disabled_rules
            or plugin_object.plugin_name in command_line_disabled_rules
        ):
            plugin_enabled = False
        if (
            plugin_object.plugin_id in command_line_enabled_rules
            or plugin_object.plugin_name in command_line_enabled_rules
        ):
            plugin_enabled = True

        return plugin_enabled

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

    def __get_plugin_details(self, plugin_instance):
        """
        Query the plugin for details and verify that they are reasonable.
        """

        try:
            instance_details = plugin_instance.get_details()
            plugin_id = instance_details.plugin_id
            plugin_name = instance_details.plugin_name
            plugin_description = instance_details.plugin_description
            plugin_enabled_by_default = instance_details.plugin_enabled_by_default
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

        plugin_object = FoundPlugin(
            plugin_id, plugin_name, plugin_description, plugin_instance
        )
        return plugin_object, plugin_enabled_by_default

    def __register_individual_plugin(
        self, plugin_instance, command_line_enabled_rules, command_line_disabled_rules
    ):
        """
        Register an individual plugin for use.
        """

        plugin_object, plugin_enabled_by_default = self.__get_plugin_details(
            plugin_instance
        )
        self.__registered_plugins.append(plugin_object)
        if self.__determine_if_plugin_enabled(
            plugin_enabled_by_default,
            plugin_object,
            command_line_enabled_rules,
            command_line_disabled_rules,
        ):
            self.__enabled_plugins.append(plugin_object)

    def __register_plugins(self, enable_rules, disable_rules):
        """
        Scan the global namespace for all subclasses of the 'Plugin' class to use as
        plugins.
        """

        command_line_enabled_rules = set()
        command_line_disabled_rules = set()
        if enable_rules:
            for i in enable_rules.split(","):
                command_line_enabled_rules.add(i)
        if disable_rules:
            for i in disable_rules.split(","):
                command_line_disabled_rules.add(i)

        self.__registered_plugins = []
        self.__enabled_plugins = []
        for plugin_instance in self.__loaded_classes:
            self.__register_individual_plugin(
                plugin_instance, command_line_enabled_rules, command_line_disabled_rules
            )

    def apply_configuration(self, configuration_map):
        """
        Apply any supplied configuration to each of the enabled plugins.
        """

        self.__enabled_plugins_for_next_token = []
        self.__enabled_plugins_for_next_line = []

        for next_plugin in self.__enabled_plugins:
            try:
                valid_key_names = [next_plugin.plugin_id]
                for next_name in next_plugin.plugin_name.split(","):
                    valid_key_names.append(next_name.strip())

                plugin_specific_configuration = {}
                for next_key_name in valid_key_names:
                    if next_key_name in configuration_map:
                        plugin_specific_configuration = configuration_map[next_key_name]
                        break

                next_plugin.plugin_instance.set_configuration_map(
                    plugin_specific_configuration
                )
                next_plugin.plugin_instance.initialize_from_config()
            except Exception as this_exception:
                raise BadPluginError(
                    next_plugin.plugin_id, inspect.stack()[0].function
                ) from this_exception

            if next_plugin.plugin_instance.is_next_token_implemented_in_plugin:
                self.__enabled_plugins_for_next_token.append(next_plugin)
            if next_plugin.plugin_instance.is_next_line_implemented_in_plugin:
                self.__enabled_plugins_for_next_line.append(next_plugin)

    def starting_new_file(self, file_being_started):
        """
        Inform any listeners that a new current file has been started.
        """
        for next_plugin in self.__enabled_plugins:
            try:
                next_plugin.plugin_instance.starting_new_file()
            except Exception as this_exception:
                raise BadPluginError(
                    next_plugin.plugin_id, inspect.stack()[0].function
                ) from this_exception

        return ScanContext(self, file_being_started)

    def completed_file(self, context, line_number):
        """
        Inform any listeners that the current file has been completed.
        """
        context.line_number = line_number
        for next_plugin in self.__enabled_plugins:
            try:
                next_plugin.plugin_instance.set_context(context)
                next_plugin.plugin_instance.completed_file()
            except Exception as this_exception:
                raise BadPluginError(
                    next_plugin.plugin_id, inspect.stack()[0].function
                ) from this_exception

    def next_line(self, context, line_number, line):
        """
        Inform any listeners that a new line has been loaded.
        """
        context.line_number = line_number
        for next_plugin in self.__enabled_plugins_for_next_line:
            try:
                next_plugin.plugin_instance.set_context(context)
                next_plugin.plugin_instance.next_line(line)
            except Exception as this_exception:
                raise BadPluginError(
                    next_plugin.plugin_id, inspect.stack()[0].function
                ) from this_exception

    def next_token(self, context, token):
        """
        Inform any listeners of a new token that has been processed.
        """
        for next_plugin in self.__enabled_plugins_for_next_token:
            try:
                next_plugin.plugin_instance.set_context(context)
                next_plugin.plugin_instance.next_token(token)
            except Exception as this_exception:
                raise BadPluginError(
                    next_plugin.plugin_id, inspect.stack()[0].function
                ) from this_exception
