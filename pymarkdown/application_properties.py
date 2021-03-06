"""
Module that provides for an encapsulation of properties for an application.
"""
import copy
import logging

from pymarkdown.parser_logger import ParserLogger

POGGER = ParserLogger(logging.getLogger(__name__))


class ApplicationProperties:
    """
    Class that provides for an encapsulation of properties for an application.
    """

    __separator = "."

    """
    Class to provide for a container of properties that belong to the application.
    """

    def __init__(self):
        """
        Initializes an new instance of the ApplicationProperties class.
        """
        self.__flat_property_map = {}

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

    def load_from_dict(self, config_map):
        """
        Load the properties from a provided dictionary.
        """

        if not isinstance(config_map, dict):
            raise ValueError("Specified parameter was not a dictionary.")

        self.__flat_property_map.clear()
        self.__scan_map(config_map, "")

    def get_boolean_property(self, property_name, default_value=None):
        """
        Get a boolean property from the configuration.
        """

        if not isinstance(property_name, str):
            raise ValueError("The propertyName argument must be a string.")
        if default_value is not None and not isinstance(default_value, bool):
            raise ValueError("The default value must either be None or a boolean.")

        property_value = default_value
        property_name = property_name.lower()
        if property_name in self.__flat_property_map:
            found_value = self.__flat_property_map[property_name]
            if isinstance(found_value, bool):
                property_value = found_value
        return property_value

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
