from __future__ import annotations

import copy
from enum import Enum
from typing import Optional


class SchemaType(Enum):
    """Enum for schema types."""

    OPENAI_API = 0
    OPENAI_TUNE = 1
    ANTHROPIC_CLAUDE = 2


class Config:
    """
    Configuration class for tool2schema.
    """

    def __init__(self, parent: Optional[Config] = None, **settings):
        self._parent = parent
        self._settings = settings
        self._initial_settings = copy.deepcopy(settings)

    @property
    def schema_type(self) -> SchemaType:
        """
        Type of the schema to create.
        """
        default_value = SchemaType.OPENAI_API
        if (fget := Config.schema_type.fget) is not None:
            return self._get_setting(fget.__name__, default_value)
        return default_value

    @schema_type.setter
    def schema_type(self, value: SchemaType):
        if (fget := Config.schema_type.fget) is not None:
            self._set_setting(fget.__name__, value)

    @property
    def ignore_parameters(self) -> list[str]:
        """
        List of parameter names to ignore when creating a schema.
        """
        default_value = ["self", "args", "kwargs"]
        if (fget := Config.ignore_parameters.fget) is not None:
            return self._get_setting(fget.__name__, default_value)
        return default_value

    @ignore_parameters.setter
    def ignore_parameters(self, value: list[str]):
        if (fget := Config.ignore_parameters.fget) is not None:
            self._set_setting(fget.__name__, value)

    @property
    def ignore_function_description(self) -> bool:
        """
        When true, omit the function description from the schema.
        """
        default_value = False
        if (fget := Config.ignore_function_description.fget) is not None:
            return self._get_setting(fget.__name__, default_value)
        return default_value

    @ignore_function_description.setter
    def ignore_function_description(self, value: bool):
        if (fget := Config.ignore_function_description.fget) is not None:
            self._set_setting(fget.__name__, value)

    @property
    def ignore_parameter_descriptions(self) -> bool:
        """
        When true, omit the parameter descriptions from the schema.
        """
        default_value = False
        if (fget := Config.ignore_parameter_descriptions.fget) is not None:
            return self._get_setting(fget.__name__, default_value)
        return default_value

    @ignore_parameter_descriptions.setter
    def ignore_parameter_descriptions(self, value: bool):
        if (fget := Config.ignore_parameter_descriptions.fget) is not None:
            self._set_setting(fget.__name__, value)

    @property
    def ignore_all_parameters(self) -> bool:
        """
        When true, omit all parameters from the schema.
        """
        default_value = False
        if (fget := Config.ignore_all_parameters.fget) is not None:
            return self._get_setting(fget.__name__, default_value)
        return default_value

    @ignore_all_parameters.setter
    def ignore_all_parameters(self, value: bool):
        if (fget := Config.ignore_all_parameters.fget) is not None:
            self._set_setting(fget.__name__, value)

    def reset_default(self):
        """
        Reset the configuration to the default settings.
        """
        self._settings = copy.deepcopy(self._initial_settings)

    def _get_setting(self, name: str, default):
        """
        Get a setting value from the settings dictionary or the parent configuration.
        If not found, return the default value.

        :param name: Name of the setting
        :param default: Default value, used when the setting is not found in
            the settings dictionary and this configuration has no parent
        :return: The requested setting value
        """
        fallback = default if not self._parent else getattr(self._parent, name)
        return self._settings.get(name, fallback)

    def _set_setting(self, name: str, value):
        """
        Set a setting value in the settings dictionary.

        :param name: Name of the setting
        :param value: Value to set
        """
        self._settings[name] = value
