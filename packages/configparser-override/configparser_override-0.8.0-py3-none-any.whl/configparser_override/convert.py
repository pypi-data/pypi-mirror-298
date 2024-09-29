from __future__ import annotations

import ast
import dataclasses
import logging
from pathlib import Path
from types import UnionType
from typing import (
    TYPE_CHECKING,
    Any,
    Dict,
    List,
    Mapping,
    Optional,
    Set,
    Tuple,
    Type,
    Union,
    get_args,
    get_origin,
    get_type_hints,
)

if TYPE_CHECKING:
    import configparser

    from configparser_override.types import Dataclass

from configparser_override.exceptions import ConversionError, LiteralEvalMiscast

logger = logging.getLogger(__name__)


def _is_optional_type(type_hint: Any) -> bool:
    """
    Check if a given type hint is an optional type.

    :param type_hint: The type hint to check.
    :type type_hint: Any
    :return: True if the type hint is optional, False otherwise.
    :rtype: bool
    """
    return get_origin(type_hint) in [Union, UnionType] and type(None) in get_args(
        type_hint
    )


class ConfigConverter:
    """
    A class to convert configuration data from a ConfigParser object to a dictionary
    or dataclass.

    :param config: The configuration parser object.
    :type config: configparser.ConfigParser
    :param boolean_states: Optional mapping of custom boolean states,
        defaults to None and uses the internal mapping of the ConfigParser object.
    :type boolean_states: Optional[Mapping[str, bool]], optional
    """

    def __init__(
        self,
        config: configparser.ConfigParser,
        boolean_states: Optional[Mapping[str, bool]] = None,
    ) -> None:
        self.config = config
        if boolean_states:
            self.boolean_states = boolean_states
        else:
            self.boolean_states = self.config.BOOLEAN_STATES

    def to_dict(self) -> dict[str, dict[str, str]]:
        """
        Convert the configuration data to a nested dictionary.

        :return: The configuration data as a dictionary.
        :rtype: dict[str, dict[str, str]]

        **Examples:**

        .. code-block:: python

            >>> config = configparser.ConfigParser()
            >>> config.read_string(\"\"\"
            ... [section1]
            ... key1 = value1
            ... [section2]
            ... key2 = value2
            ... \"\"\")
            >>> converter = ConfigConverter(config)
            >>> config_dict = converter.to_dict()
            >>> config_dict['section1']['key1']
            'value1'
        """
        config_dict: dict[str, dict[str, str]] = {}
        for sect in self.config.sections():
            # Add nested sections
            config_dict[sect] = {}
            for opt in self.config.options(sect):
                config_dict[sect][opt] = self.config.get(section=sect, option=opt)
        # Add default nested section
        config_dict[self.config.default_section] = {}
        for opt in self.config.defaults():
            config_dict[self.config.default_section][opt] = self.config.get(
                section=self.config.default_section, option=opt
            )
        return config_dict

    def to_dataclass(self, dataclass: Type[Dataclass]) -> Dataclass:
        """
        Convert the configuration data to a dataclass instance.

        :param dataclass: The dataclass type to convert the configuration data into.
        :type dataclass: Dataclass
        :return: An instance of the dataclass populated with the configuration data.
        :rtype: Dataclass

        **Examples:**

        .. code-block:: python

            >>> from dataclasses import dataclass

            >>> @dataclass
            ... class Section1:
            ...     key: str

            >>> @dataclass
            ... class ExampleConfig:
            ...     section1: Section1

            >>> config = configparser.ConfigParser()
            >>> config.read_string(\"\"\"
            ... [section1]
            ... key = value
            ... \"\"\")
            >>> converter = ConfigConverter(config)
            >>> config_as_dataclass = converter.to_dataclass(ExampleConfig)
            >>> assert config_as_dataclass.section1.key == "value" # True
        """
        config_dict = self.to_dict()
        return self._dict_to_dataclass(
            input_dict=config_dict,
            dataclass=dataclass,
        )

    def _dict_to_dataclass(
        self, input_dict: dict, dataclass: Type[Dataclass]
    ) -> Dataclass:
        """
        Convert a dictionary to a dataclass instance.

        :param input_dict: The input dictionary to convert.
        :type input_dict: dict
        :param dataclass: The dataclass type to convert the dictionary into.
        :type dataclass: Dataclass
        :return: An instance of the dataclass populated with the dictionary data.
        :rtype: Dataclass
        :raises AttributeError: If required fields are missing in the source config.
        """
        type_hints = get_type_hints(dataclass)

        _dict_with_types: dict[str, Any] = {}
        for field in dataclasses.fields(dataclass):
            field_name = field.name
            field_type = type_hints[field_name]
            if field_name in input_dict:
                _dict_with_types[field_name] = self._cast_value(
                    value=input_dict[field_name],
                    type_hint=field_type,
                )
            elif not _is_optional_type(field_type):
                raise AttributeError(f"Missing field in source config: {field_name}")
        return dataclass(**_dict_with_types)

    def _cast_value(self, value: Any, type_hint: Any) -> Any:
        if dataclasses.is_dataclass(type_hint):
            _type_hint = type_hint if isinstance(type_hint, type) else type(type_hint)
            return self._dict_to_dataclass(value, _type_hint)
        if type_hint is Any:
            return value
        if type_hint in [int, float, complex, str, Path]:
            return type_hint(value)
        if type_hint is bytes:
            return str(value).encode()
        if type_hint is bool:
            return self._cast_bool(value)
        _origin = get_origin(type_hint)
        if _origin in [list, List]:
            return self._cast_list(value, type_hint)
        if _origin in [dict, Dict]:
            return self._cast_dict(value, type_hint)
        if _origin in [set, Set]:
            return self._cast_set(value, type_hint)
        if _origin in [tuple, Tuple]:
            return self._cast_tuple(value, type_hint)
        if _origin in (Optional, Union, UnionType):
            return self._cast_union(value, type_hint)
        if type_hint is type(None):
            return None
        raise ValueError(f"Unsupported type: {type_hint}")

    def _cast_bool(self, value: Any) -> bool:
        if str(value).lower() in self.boolean_states:
            return self.boolean_states[str(value).lower()]
        else:
            raise ValueError(f"{value=} not in possible {self.boolean_states=}")

    def _cast_list(self, value: Any, type_hint: Any) -> list:
        _evaluated_option = ast.literal_eval(value) if isinstance(value, str) else value
        if isinstance(_evaluated_option, list):
            _types = get_args(type_hint)
            for typ in _types:
                try:
                    return [self._cast_value(item, typ) for item in _evaluated_option]
                except Exception as e:
                    logger.debug(f"Failed to cast {value=} into {typ=}, error: {e}")
                    continue
            raise ConversionError(
                f"Not possible to cast {value} into a list of {_types}"
            )
        raise LiteralEvalMiscast(
            f"{value} casted as {type(_evaluated_option)} expected {type_hint}"
        )

    def _cast_set(self, value: Any, type_hint: Any) -> set:
        _evaluated_option = ast.literal_eval(value) if isinstance(value, str) else value
        if isinstance(_evaluated_option, set):
            _types = get_args(type_hint)
            for typ in _types:
                try:
                    return {self._cast_value(item, typ) for item in _evaluated_option}
                except Exception as e:
                    logger.debug(f"Failed to cast {value=} into {typ=}, error: {e}")
                    continue
            raise ConversionError(
                f"Not possible to cast {value} into a set of {_types}"
            )
        raise LiteralEvalMiscast(
            f"{value} casted as {type(_evaluated_option)} expected {type_hint}"
        )

    def _cast_tuple(self, value: Any, type_hint: Any) -> tuple:
        _evaluated_option = ast.literal_eval(value) if isinstance(value, str) else value
        if isinstance(_evaluated_option, tuple):
            _types = get_args(type_hint)
            for typ in _types:
                try:
                    return tuple(
                        self._cast_value(item, typ) for item in _evaluated_option
                    )
                except Exception as e:
                    logger.debug(f"Failed to cast {value=} into {typ=}, error: {e}")
                    continue
            raise ConversionError(
                f"Not possible to cast {value} into a tuple of {_types}"
            )
        raise LiteralEvalMiscast(
            f"{value} casted as {type(_evaluated_option)} expected {type_hint}"
        )

    def _cast_dict(self, value: Any, type_hint: Any) -> dict:
        _evaluated_option = ast.literal_eval(value) if isinstance(value, str) else value
        if isinstance(_evaluated_option, dict):
            k_typ, v_typ = get_args(type_hint)
            try:
                return {
                    self._cast_value(k, k_typ): self._cast_value(v, v_typ)
                    for k, v in _evaluated_option.items()
                }
            except Exception as e:
                logger.debug(
                    f"Failed to cast {value=} into {k_typ=}, {v_typ=}, error: {e}"
                )
                raise ConversionError(
                    f"Not possible to cast {value} into a dict of keys of type {k_typ}, and values of type {v_typ}, Error: {e}"
                ) from e
        raise LiteralEvalMiscast(
            f"{value} casted as {type(_evaluated_option)} expected {type_hint}"
        )

    def _cast_union(self, value: Any, type_hint: Any) -> Any:
        for typ in get_args(type_hint):
            try:
                return self._cast_value(value, typ)
            except Exception as e:
                logger.debug(f"Failed to cast {value=} into {typ=}, error: {e}")
                continue
        raise ConversionError(f"Not possible to cast {value} into type {type_hint}")
