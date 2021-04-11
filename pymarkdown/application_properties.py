"""
Module that provides for an encapsulation of properties for an application.
"""
import copy
import json
import logging

LOGGER = logging.getLogger(__name__)


class ApplicationProperties:
    """
    Class that provides for an encapsulation of properties for an application.

    Eventually want to add:
    - set from command line
    - exposure to command line: i.e. list all properties, values, etc.
    - transformers, both per call and registered, to change from one value to another
      - i.e. what if a property is given on the command line as a string, but an integer is required?
    """

    __separator = "."
    __assignment_operator = "="
    __manual_property_type_prefix = "$"
    __manual_property_type_string = "$"
    __manual_property_type_integer = "#"
    __manual_property_type_boolean = "!"

    """
    Class to provide for a container of properties that belong to the application.
    """

    def __init__(self, strict_mode=False):
        """
        Initializes an new instance of the ApplicationProperties class.
        """
        self.__flat_property_map = {}
        self.__strict_mode = strict_mode

    @property
    def separator(self):
        """
        Separator used to split the hierarchy of the property names.
        """
        return self.__separator

    @property
    def number_of_properties(self):
        """
        Number of properties that exist in the map.
        """
        return len(self.__flat_property_map)

    @property
    def property_names(self):
        """
        List of each of the properties in the map.
        """
        return self.__flat_property_map.keys()

    @property
    def strict_mode(self):
        """
        Gets whether strict mode is on by default.
        """
        return self.__strict_mode

    def load_from_dict(self, config_map):
        """
        Load the properties from a provided dictionary.
        """

        if not isinstance(config_map, dict):
            raise ValueError("Specified parameter was not a dictionary.")

        LOGGER.debug("Loading from dictionary: {%s}", str(config_map))
        self.__flat_property_map.clear()
        self.__scan_map(config_map, "")

    @staticmethod
    def verify_full_part_form(property_key):
        """
        Given one part of a full key, verify that it is composed properly.
        """

        if (
            " " in property_key
            or "\t" in property_key
            or "\n" in property_key
            or ApplicationProperties.__assignment_operator in property_key
        ):
            raise ValueError(
                f"Each part of the property key must not contain a whitespace character or the '{ApplicationProperties.__separator}' character."
            )
        if not property_key:
            raise ValueError(
                "Each part of the property key must contain at least one character."
            )
        return property_key

    @staticmethod
    def verify_full_key_form(property_key):
        """
        Given a full key, verify that it is composed properly.
        """

        if property_key.startswith(
            ApplicationProperties.__separator
        ) or property_key.endswith(ApplicationProperties.__separator):
            raise ValueError(
                f"Full property key must not start or end with the '{ApplicationProperties.__separator}' character."
            )
        doubles = (
            f"{ApplicationProperties.__separator}{ApplicationProperties.__separator}"
        )
        doubles_index = property_key.find(doubles)
        if doubles_index != -1:
            raise ValueError(
                f"Full property key cannot contain multiples of the {ApplicationProperties.__separator} without any text between them."
            )
        split_key = property_key.split(ApplicationProperties.__separator)
        for next_key in split_key:
            ApplicationProperties.verify_full_part_form(next_key)
        return property_key

    @staticmethod
    def verify_manual_property_form(string_to_verify):
        """
        Verify the general form of a manual property string. i.e. key=value
        """

        if not isinstance(string_to_verify, str):
            raise ValueError("Manual property form must be a string.")
        equals_index = string_to_verify.find(
            ApplicationProperties.__assignment_operator
        )
        if equals_index == -1:
            raise ValueError(
                "Manual property key and value must be separated by the '=' character."
            )
        property_key = string_to_verify[0:equals_index]
        ApplicationProperties.verify_full_key_form(property_key)
        return string_to_verify

    def set_manual_property(self, combined_string):
        """
        Manually set a property for the object.
        """

        if not isinstance(combined_string, str):
            iterator = None
            try:
                iterator = iter(combined_string)
            except TypeError as this_exception:
                raise ValueError(
                    "Manual property form must either be a string or an iterable of strings."
                ) from this_exception
            for i in iterator:
                self.set_manual_property(i)
            return

        ApplicationProperties.verify_manual_property_form(combined_string)
        equals_index = combined_string.find(ApplicationProperties.__assignment_operator)
        property_key = combined_string[0:equals_index].lower()
        property_value = combined_string[equals_index + 1 :]

        if (
            property_value.startswith(
                ApplicationProperties.__manual_property_type_prefix
            )
            and len(property_value) >= 2
        ):
            if property_value[1] == ApplicationProperties.__manual_property_type_string:
                property_value = property_value[2:]
            elif (
                property_value[1]
                == ApplicationProperties.__manual_property_type_integer
            ):
                try:
                    property_value = int(property_value[2:])
                except ValueError as this_exception:
                    raise ValueError(
                        f"Manual property value '{property_value}' cannot be translated into an integer."
                    ) from this_exception
            elif (
                property_value[1]
                == ApplicationProperties.__manual_property_type_boolean
            ):
                property_value = property_value[2:].lower() == "true"
            else:
                property_value = property_value[1:]
        self.__flat_property_map[property_key] = copy.deepcopy(property_value)
        LOGGER.debug(
            "Adding configuration '%s' : {%s}", property_key, str(property_value)
        )

    # pylint: disable=unidiomatic-typecheck
    # pylint: disable=too-many-arguments
    # pylint: disable=broad-except
    # pylint: disable=raise-missing-from
    def get_property(
        self,
        property_name,
        property_type,
        default_value=None,
        valid_value_fn=None,
        is_required=False,
        strict_mode=None,
    ):
        """
        Get an property of a generic type from the configuration.
        """

        if strict_mode is None:
            strict_mode = self.__strict_mode

        if not isinstance(property_name, str):
            raise ValueError("The propertyName argument must be a string.")
        ApplicationProperties.verify_full_key_form(property_name)
        if not isinstance(property_type, type):
            raise ValueError(
                f"The property_type argument for '{property_name}' must be a type."
            )
        if default_value is not None and type(default_value) != property_type:
            raise ValueError(
                f"The default value for property '{property_name}' must either be None or a '{property_type.__name__}' value."
            )

        property_value = default_value
        property_name = property_name.lower()
        LOGGER.debug("property_name=%s", property_name)
        if property_name in self.__flat_property_map:
            found_value = self.__flat_property_map[property_name]
            is_eligible = type(found_value) == property_type
            if not is_eligible and strict_mode:
                raise ValueError(
                    f"The value for property '{property_name}' must be of type '{property_type.__name__}'."
                )
            if is_eligible and valid_value_fn:
                try:
                    valid_value_fn(found_value)
                except Exception as this_exception:
                    is_eligible = False
                    if strict_mode:
                        raise ValueError(
                            f"The value for property '{property_name}' is not valid: {str(this_exception)}"
                        )
            if is_eligible:
                property_value = found_value
        elif is_required:
            raise ValueError(
                f"A value for property '{property_name}' must be provided."
            )
        return property_value

    # pylint: enable=unidiomatic-typecheck
    # pylint: enable=too-many-arguments
    # pylint: enable=broad-except
    # pylint: enable=raise-missing-from

    def get_boolean_property(
        self, property_name, default_value=None, is_required=False
    ):
        """
        Get a boolean property from the configuration.
        """
        return self.get_property(
            property_name,
            bool,
            default_value=default_value,
            valid_value_fn=None,
            is_required=is_required,
            strict_mode=None,
        )

    # pylint: disable=too-many-arguments
    def get_integer_property(
        self,
        property_name,
        default_value=None,
        valid_value_fn=None,
        is_required=False,
        strict_mode=False,
    ):
        """
        Get an integer property from the configuration.
        """
        return self.get_property(
            property_name,
            int,
            default_value=default_value,
            valid_value_fn=valid_value_fn,
            is_required=is_required,
            strict_mode=strict_mode,
        )

    # pylint: enable=too-many-arguments

    # pylint: disable=too-many-arguments
    def get_string_property(
        self,
        property_name,
        default_value=None,
        valid_value_fn=None,
        is_required=False,
        strict_mode=None,
    ):
        """
        Get a string property from the configuration.
        """
        return self.get_property(
            property_name,
            str,
            default_value=default_value,
            valid_value_fn=valid_value_fn,
            is_required=is_required,
            strict_mode=strict_mode,
        )

    # pylint: enable=too-many-arguments

    def __scan_map(self, config_map, current_prefix):
        for next_key in config_map:
            if not isinstance(next_key, str):
                raise ValueError(
                    "All keys in the main dictionary and nested dictionaries must be strings."
                )
            if self.__separator in next_key:
                raise ValueError(
                    f"Keys strings cannot contain the separator character '{self.__separator}'."
                )

            next_value = config_map[next_key]
            if isinstance(next_value, dict):
                self.__scan_map(
                    next_value, f"{current_prefix}{next_key}{self.__separator}"
                )
            else:
                new_key = f"{current_prefix}{next_key}".lower()
                self.__flat_property_map[new_key] = copy.deepcopy(next_value)
                LOGGER.debug(
                    "Adding configuration '%s' : {%s}", new_key, str(next_value)
                )


class ApplicationPropertiesFacade:
    """
    Class to provide for a facade in front of an ApplicationProperties instance that
    only exposes part of the properties tree.
    """

    def __init__(self, base_properties, property_prefix):
        """
        Initializes an new instance of the ApplicationPropertiesFacade class.
        """
        if not isinstance(base_properties, ApplicationProperties):
            raise ValueError(
                "The base_properties of the facade must be an ApplicationProperties instance."
            )
        self.__base_properties = base_properties

        if not isinstance(property_prefix, str):
            raise ValueError("The property_prefix argument must be a string.")
        if not property_prefix.endswith(base_properties.separator):
            raise ValueError(
                f"The property_prefix argument must end with the separator character '{base_properties.separator}'."
            )
        self.__property_prefix = property_prefix

    # pylint: disable=too-many-arguments
    def get_property(
        self,
        property_name,
        property_type,
        default_value=None,
        valid_value_fn=None,
        is_required=False,
        strict_mode=False,
    ):
        """
        Get an property of a generic type from the configuration.
        """

        return self.__base_properties.get_property(
            f"{self.__property_prefix}{property_name}",
            property_type,
            default_value=default_value,
            valid_value_fn=valid_value_fn,
            is_required=is_required,
            strict_mode=strict_mode,
        )

    # pylint: enable=too-many-arguments

    def get_boolean_property(
        self, property_name, default_value=None, is_required=False
    ):
        """
        Get a boolean property from the configuration.
        """
        return self.__base_properties.get_boolean_property(
            f"{self.__property_prefix}{property_name}",
            default_value=default_value,
            is_required=is_required,
        )

    # pylint: disable=too-many-arguments
    def get_integer_property(
        self,
        property_name,
        default_value=None,
        valid_value_fn=None,
        is_required=False,
        strict_mode=False,
    ):
        """
        Get an integer property from the configuration.
        """
        return self.__base_properties.get_integer_property(
            f"{self.__property_prefix}{property_name}",
            default_value=default_value,
            valid_value_fn=valid_value_fn,
            is_required=is_required,
            strict_mode=strict_mode,
        )

    # pylint: enable=too-many-arguments

    # pylint: disable=too-many-arguments
    def get_string_property(
        self,
        property_name,
        default_value=None,
        valid_value_fn=None,
        is_required=False,
        strict_mode=False,
    ):
        """
        Get a string property from the configuration.
        """
        return self.__base_properties.get_string_property(
            f"{self.__property_prefix}{property_name}",
            default_value=default_value,
            valid_value_fn=valid_value_fn,
            is_required=is_required,
            strict_mode=strict_mode,
        )

    # pylint: enable=too-many-arguments

    @property
    def property_names(self):
        """
        List of each of the properties in the map.
        """
        facade_property_names = []
        for next_property_name in self.__base_properties.property_names:
            if next_property_name.startswith(self.__property_prefix):
                facade_property_names.append(
                    next_property_name[len(self.__property_prefix) :]
                )
        return facade_property_names


# pylint: disable=too-few-public-methods
class ApplicationPropertiesJsonLoader:
    """
    Class to provide for a manner to load an ApplicationProperties object from a JSON file.
    """

    @staticmethod
    def load_and_set(properties_object, configuration_file, handle_error_fn):
        """
        Load the specified file and set it into the given properties object.
        """

        try:
            with open(configuration_file) as infile:
                configuration_map = json.load(infile)
        except json.decoder.JSONDecodeError as this_exception:
            formatted_error = f"Specified configuration file '{configuration_file}' is not a valid JSON file ({str(this_exception)})."
            handle_error_fn(formatted_error)
        except IOError as this_exception:
            formatted_error = f"Specified configuration file '{configuration_file}' was not loaded ({str(this_exception)})."
            handle_error_fn(formatted_error)

        try:
            properties_object.load_from_dict(configuration_map)
        except ValueError as this_exception:
            formatted_error = f"Specified configuration file '{configuration_file}' is not valid ({str(this_exception)})."
            handle_error_fn(formatted_error)


# pylint: enable=too-few-public-methods
