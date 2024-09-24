# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------
# pylint: disable=protected-access, arguments-differ, signature-differs, broad-except, too-many-lines

import copy
import calendar
import decimal
import functools
import sys
import logging
import base64
import re
import typing
import enum
import email.utils
from datetime import datetime, date, time, timedelta, timezone
from json import JSONEncoder
import xml.etree.ElementTree as ET
from typing_extensions import Self
import isodate
from azure.core.exceptions import DeserializationError
from azure.core import CaseInsensitiveEnumMeta
from azure.core.pipeline import PipelineResponse
from azure.core.serialization import _Null

if sys.version_info >= (3, 9):
    from collections.abc import MutableMapping
else:
    from typing import MutableMapping

_LOGGER = logging.getLogger(__name__)

__all__ = ["SdkJSONEncoder", "Model", "rest_field", "rest_discriminator"]

TZ_UTC = timezone.utc
_T = typing.TypeVar("_T")


def _timedelta_as_isostr(td: timedelta) -> str:
    """Converts a datetime.timedelta object into an ISO 8601 formatted string, e.g. 'P4DT12H30M05S'

    Function adapted from the Tin Can Python project: https://github.com/RusticiSoftware/TinCanPython

    :param timedelta td: The timedelta to convert
    :rtype: str
    :return: ISO8601 version of this timedelta
    """

    # Split seconds to larger units
    seconds = td.total_seconds()
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)

    days, hours, minutes = list(map(int, (days, hours, minutes)))
    seconds = round(seconds, 6)

    # Build date
    date_str = ""
    if days:
        date_str = "%sD" % days

    if hours or minutes or seconds:
        # Build time
        time_str = "T"

        # Hours
        bigger_exists = date_str or hours
        if bigger_exists:
            time_str += "{:02}H".format(hours)

        # Minutes
        bigger_exists = bigger_exists or minutes
        if bigger_exists:
            time_str += "{:02}M".format(minutes)

        # Seconds
        try:
            if seconds.is_integer():
                seconds_string = "{:02}".format(int(seconds))
            else:
                # 9 chars long w/ leading 0, 6 digits after decimal
                seconds_string = "%09.6f" % seconds
                # Remove trailing zeros
                seconds_string = seconds_string.rstrip("0")
        except AttributeError:  # int.is_integer() raises
            seconds_string = "{:02}".format(seconds)

        time_str += "{}S".format(seconds_string)
    else:
        time_str = ""

    return "P" + date_str + time_str


def _serialize_bytes(o, format: typing.Optional[str] = None) -> str:
    encoded = base64.b64encode(o).decode()
    if format == "base64url":
        return encoded.strip("=").replace("+", "-").replace("/", "_")
    return encoded


def _serialize_datetime(o, format: typing.Optional[str] = None):
    if hasattr(o, "year") and hasattr(o, "hour"):
        if format == "rfc7231":
            return email.utils.format_datetime(o, usegmt=True)
        if format == "unix-timestamp":
            return int(calendar.timegm(o.utctimetuple()))

        # astimezone() fails for naive times in Python 2.7, so make make sure o is aware (tzinfo is set)
        if not o.tzinfo:
            iso_formatted = o.replace(tzinfo=TZ_UTC).isoformat()
        else:
            iso_formatted = o.astimezone(TZ_UTC).isoformat()
        # Replace the trailing "+00:00" UTC offset with "Z" (RFC 3339: https://www.ietf.org/rfc/rfc3339.txt)
        return iso_formatted.replace("+00:00", "Z")
    # Next try datetime.date or datetime.time
    return o.isoformat()


def _is_readonly(p):
    try:
        return p._visibility == ["read"]
    except AttributeError:
        return False


class SdkJSONEncoder(JSONEncoder):
    """A JSON encoder that's capable of serializing datetime objects and bytes."""

    def __init__(self, *args, exclude_readonly: bool = False, format: typing.Optional[str] = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.exclude_readonly = exclude_readonly
        self.format = format

    def default(self, o):  # pylint: disable=too-many-return-statements
        if _is_model(o):
            if self.exclude_readonly:
                readonly_props = [p._rest_name for p in o._attr_to_rest_field.values() if _is_readonly(p)]
                return {k: v for k, v in o.items() if k not in readonly_props}
            return dict(o.items())
        try:
            return super(SdkJSONEncoder, self).default(o)
        except TypeError:
            if isinstance(o, _Null):
                return None
            if isinstance(o, decimal.Decimal):
                return float(o)
            if isinstance(o, (bytes, bytearray)):
                return _serialize_bytes(o, self.format)
            try:
                # First try datetime.datetime
                return _serialize_datetime(o, self.format)
            except AttributeError:
                pass
            # Last, try datetime.timedelta
            try:
                return _timedelta_as_isostr(o)
            except AttributeError:
                # This will be raised when it hits value.total_seconds in the method above
                pass
            return super(SdkJSONEncoder, self).default(o)


_VALID_DATE = re.compile(r"\d{4}[-]\d{2}[-]\d{2}T\d{2}:\d{2}:\d{2}" + r"\.?\d*Z?[-+]?[\d{2}]?:?[\d{2}]?")
_VALID_RFC7231 = re.compile(
    r"(Mon|Tue|Wed|Thu|Fri|Sat|Sun),\s\d{2}\s"
    r"(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s\d{4}\s\d{2}:\d{2}:\d{2}\sGMT"
)


def _deserialize_datetime(attr: typing.Union[str, datetime]) -> datetime:
    """Deserialize ISO-8601 formatted string into Datetime object.

    :param str attr: response string to be deserialized.
    :rtype: ~datetime.datetime
    :returns: The datetime object from that input
    """
    if isinstance(attr, datetime):
        # i'm already deserialized
        return attr
    attr = attr.upper()
    match = _VALID_DATE.match(attr)
    if not match:
        raise ValueError("Invalid datetime string: " + attr)

    check_decimal = attr.split(".")
    if len(check_decimal) > 1:
        decimal_str = ""
        for digit in check_decimal[1]:
            if digit.isdigit():
                decimal_str += digit
            else:
                break
        if len(decimal_str) > 6:
            attr = attr.replace(decimal_str, decimal_str[0:6])

    date_obj = isodate.parse_datetime(attr)
    test_utc = date_obj.utctimetuple()
    if test_utc.tm_year > 9999 or test_utc.tm_year < 1:
        raise OverflowError("Hit max or min date")
    return date_obj


def _deserialize_datetime_rfc7231(attr: typing.Union[str, datetime]) -> datetime:
    """Deserialize RFC7231 formatted string into Datetime object.

    :param str attr: response string to be deserialized.
    :rtype: ~datetime.datetime
    :returns: The datetime object from that input
    """
    if isinstance(attr, datetime):
        # i'm already deserialized
        return attr
    match = _VALID_RFC7231.match(attr)
    if not match:
        raise ValueError("Invalid datetime string: " + attr)

    return email.utils.parsedate_to_datetime(attr)


def _deserialize_datetime_unix_timestamp(attr: typing.Union[float, datetime]) -> datetime:
    """Deserialize unix timestamp into Datetime object.

    :param str attr: response string to be deserialized.
    :rtype: ~datetime.datetime
    :returns: The datetime object from that input
    """
    if isinstance(attr, datetime):
        # i'm already deserialized
        return attr
    return datetime.fromtimestamp(attr, TZ_UTC)


def _deserialize_date(attr: typing.Union[str, date]) -> date:
    """Deserialize ISO-8601 formatted string into Date object.
    :param str attr: response string to be deserialized.
    :rtype: date
    :returns: The date object from that input
    """
    # This must NOT use defaultmonth/defaultday. Using None ensure this raises an exception.
    if isinstance(attr, date):
        return attr
    return isodate.parse_date(attr, defaultmonth=None, defaultday=None)  # type: ignore


def _deserialize_time(attr: typing.Union[str, time]) -> time:
    """Deserialize ISO-8601 formatted string into time object.

    :param str attr: response string to be deserialized.
    :rtype: datetime.time
    :returns: The time object from that input
    """
    if isinstance(attr, time):
        return attr
    return isodate.parse_time(attr)


def _deserialize_bytes(attr):
    if isinstance(attr, (bytes, bytearray)):
        return attr
    return bytes(base64.b64decode(attr))


def _deserialize_bytes_base64(attr):
    if isinstance(attr, (bytes, bytearray)):
        return attr
    padding = "=" * (3 - (len(attr) + 3) % 4)  # type: ignore
    attr = attr + padding  # type: ignore
    encoded = attr.replace("-", "+").replace("_", "/")
    return bytes(base64.b64decode(encoded))


def _deserialize_duration(attr):
    if isinstance(attr, timedelta):
        return attr
    return isodate.parse_duration(attr)


def _deserialize_decimal(attr):
    if isinstance(attr, decimal.Decimal):
        return attr
    return decimal.Decimal(str(attr))


def _deserialize_int_as_str(attr):
    if isinstance(attr, int):
        return attr
    return int(attr)


_DESERIALIZE_MAPPING = {
    datetime: _deserialize_datetime,
    date: _deserialize_date,
    time: _deserialize_time,
    bytes: _deserialize_bytes,
    bytearray: _deserialize_bytes,
    timedelta: _deserialize_duration,
    typing.Any: lambda x: x,
    decimal.Decimal: _deserialize_decimal,
}

_DESERIALIZE_MAPPING_WITHFORMAT = {
    "rfc3339": _deserialize_datetime,
    "rfc7231": _deserialize_datetime_rfc7231,
    "unix-timestamp": _deserialize_datetime_unix_timestamp,
    "base64": _deserialize_bytes,
    "base64url": _deserialize_bytes_base64,
}


def get_deserializer(annotation: typing.Any, rf: typing.Optional["_RestField"] = None):
    if annotation is int and rf and rf._format == "str":
        return _deserialize_int_as_str
    if rf and rf._format:
        return _DESERIALIZE_MAPPING_WITHFORMAT.get(rf._format)
    return _DESERIALIZE_MAPPING.get(annotation)  # pyright: ignore


def _get_type_alias_type(module_name: str, alias_name: str):
    types = {
        k: v
        for k, v in sys.modules[module_name].__dict__.items()
        if isinstance(v, typing._GenericAlias)  # type: ignore
    }
    if alias_name not in types:
        return alias_name
    return types[alias_name]


def _get_model(module_name: str, model_name: str):
    models = {k: v for k, v in sys.modules[module_name].__dict__.items() if isinstance(v, type)}
    module_end = module_name.rsplit(".", 1)[0]
    models.update({k: v for k, v in sys.modules[module_end].__dict__.items() if isinstance(v, type)})
    if isinstance(model_name, str):
        model_name = model_name.split(".")[-1]
    if model_name not in models:
        return model_name
    return models[model_name]


_UNSET = object()


class _MyMutableMapping(MutableMapping[str, typing.Any]):  # pylint: disable=unsubscriptable-object
    def __init__(self, data: typing.Dict[str, typing.Any]) -> None:
        self._data = data

    def __contains__(self, key: typing.Any) -> bool:
        return key in self._data

    def __getitem__(self, key: str) -> typing.Any:
        return self._data.__getitem__(key)

    def __setitem__(self, key: str, value: typing.Any) -> None:
        self._data.__setitem__(key, value)

    def __delitem__(self, key: str) -> None:
        self._data.__delitem__(key)

    def __iter__(self) -> typing.Iterator[typing.Any]:
        return self._data.__iter__()

    def __len__(self) -> int:
        return self._data.__len__()

    def __ne__(self, other: typing.Any) -> bool:
        return not self.__eq__(other)

    def keys(self) -> typing.KeysView[str]:
        return self._data.keys()

    def values(self) -> typing.ValuesView[typing.Any]:
        return self._data.values()

    def items(self) -> typing.ItemsView[str, typing.Any]:
        return self._data.items()

    def get(self, key: str, default: typing.Any = None) -> typing.Any:
        try:
            return self[key]
        except KeyError:
            return default

    @typing.overload
    def pop(self, key: str) -> typing.Any: ...

    @typing.overload
    def pop(self, key: str, default: _T) -> _T: ...

    @typing.overload
    def pop(self, key: str, default: typing.Any) -> typing.Any: ...

    def pop(self, key: str, default: typing.Any = _UNSET) -> typing.Any:
        if default is _UNSET:
            return self._data.pop(key)
        return self._data.pop(key, default)

    def popitem(self) -> typing.Tuple[str, typing.Any]:
        return self._data.popitem()

    def clear(self) -> None:
        self._data.clear()

    def update(self, *args: typing.Any, **kwargs: typing.Any) -> None:
        self._data.update(*args, **kwargs)

    @typing.overload
    def setdefault(self, key: str, default: None = None) -> None: ...

    @typing.overload
    def setdefault(self, key: str, default: typing.Any) -> typing.Any: ...

    def setdefault(self, key: str, default: typing.Any = _UNSET) -> typing.Any:
        if default is _UNSET:
            return self._data.setdefault(key)
        return self._data.setdefault(key, default)

    def __eq__(self, other: typing.Any) -> bool:
        try:
            other_model = self.__class__(other)
        except Exception:
            return False
        return self._data == other_model._data

    def __repr__(self) -> str:
        return str(self._data)


def _is_model(obj: typing.Any) -> bool:
    return getattr(obj, "_is_model", False)


def _serialize(o, format: typing.Optional[str] = None):  # pylint: disable=too-many-return-statements
    if isinstance(o, list):
        return [_serialize(x, format) for x in o]
    if isinstance(o, dict):
        return {k: _serialize(v, format) for k, v in o.items()}
    if isinstance(o, set):
        return {_serialize(x, format) for x in o}
    if isinstance(o, tuple):
        return tuple(_serialize(x, format) for x in o)
    if isinstance(o, (bytes, bytearray)):
        return _serialize_bytes(o, format)
    if isinstance(o, decimal.Decimal):
        return float(o)
    if isinstance(o, enum.Enum):
        return o.value
    if isinstance(o, int):
        if format == "str":
            return str(o)
        return o
    try:
        # First try datetime.datetime
        return _serialize_datetime(o, format)
    except AttributeError:
        pass
    # Last, try datetime.timedelta
    try:
        return _timedelta_as_isostr(o)
    except AttributeError:
        # This will be raised when it hits value.total_seconds in the method above
        pass
    return o


def _get_rest_field(
    attr_to_rest_field: typing.Dict[str, "_RestField"], rest_name: str
) -> typing.Optional["_RestField"]:
    try:
        return next(rf for rf in attr_to_rest_field.values() if rf._rest_name == rest_name)
    except StopIteration:
        return None


def _create_value(rf: typing.Optional["_RestField"], value: typing.Any) -> typing.Any:
    if not rf:
        return _serialize(value, None)
    if rf._is_multipart_file_input:
        return value
    if rf._is_model:
        return _deserialize(rf._type, value)
    if isinstance(value, ET.Element):
        value = _deserialize(rf._type, value)
    return _serialize(value, rf._format)


class Model(_MyMutableMapping):
    _is_model = True
    # label whether current class's _attr_to_rest_field has been calculated
    # could not see _attr_to_rest_field directly because subclass inherits it from parent class
    _calculated: typing.Set[str] = set()

    def __init__(self, *args: typing.Any, **kwargs: typing.Any) -> None:
        class_name = self.__class__.__name__
        if len(args) > 1:
            raise TypeError(f"{class_name}.__init__() takes 2 positional arguments but {len(args) + 1} were given")
        dict_to_pass = {
            rest_field._rest_name: rest_field._default
            for rest_field in self._attr_to_rest_field.values()
            if rest_field._default is not _UNSET
        }
        if args:  # pylint: disable=too-many-nested-blocks
            if isinstance(args[0], ET.Element):
                existed_attr_keys = []
                model_meta = getattr(self, "_xml", {})

                for rf in self._attr_to_rest_field.values():
                    prop_meta = getattr(rf, "_xml", {})
                    xml_name = prop_meta.get("name", rf._rest_name)
                    xml_ns = prop_meta.get("ns", model_meta.get("ns", None))
                    if xml_ns:
                        xml_name = "{" + xml_ns + "}" + xml_name

                    # attribute
                    if prop_meta.get("attribute", False) and args[0].get(xml_name) is not None:
                        existed_attr_keys.append(xml_name)
                        dict_to_pass[rf._rest_name] = _deserialize(rf._type, args[0].get(xml_name))
                        continue

                    # unwrapped element is array
                    if prop_meta.get("unwrapped", False):
                        # unwrapped array could either use prop items meta/prop meta
                        if prop_meta.get("itemsName"):
                            xml_name = prop_meta.get("itemsName")
                            xml_ns = prop_meta.get("itemNs")
                            if xml_ns:
                                xml_name = "{" + xml_ns + "}" + xml_name
                        items = args[0].findall(xml_name)  # pyright: ignore
                        if len(items) > 0:
                            existed_attr_keys.append(xml_name)
                            dict_to_pass[rf._rest_name] = _deserialize(rf._type, items)
                        continue

                    # text element is primitive type
                    if prop_meta.get("text", False):
                        if args[0].text is not None:
                            dict_to_pass[rf._rest_name] = _deserialize(rf._type, args[0].text)
                        continue

                    # wrapped element could be normal property or array, it should only have one element
                    item = args[0].find(xml_name)
                    if item is not None:
                        existed_attr_keys.append(xml_name)
                        dict_to_pass[rf._rest_name] = _deserialize(rf._type, item)

                # rest thing is additional properties
                for e in args[0]:
                    if e.tag not in existed_attr_keys:
                        dict_to_pass[e.tag] = _convert_element(e)
            else:
                dict_to_pass.update(
                    {k: _create_value(_get_rest_field(self._attr_to_rest_field, k), v) for k, v in args[0].items()}
                )
        else:
            non_attr_kwargs = [k for k in kwargs if k not in self._attr_to_rest_field]
            if non_attr_kwargs:
                # actual type errors only throw the first wrong keyword arg they see, so following that.
                raise TypeError(f"{class_name}.__init__() got an unexpected keyword argument '{non_attr_kwargs[0]}'")
            dict_to_pass.update(
                {
                    self._attr_to_rest_field[k]._rest_name: _create_value(self._attr_to_rest_field[k], v)
                    for k, v in kwargs.items()
                    if v is not None
                }
            )
        super().__init__(dict_to_pass)

    def copy(self) -> "Model":
        return Model(self.__dict__)

    def __new__(cls, *args: typing.Any, **kwargs: typing.Any) -> Self:  # pylint: disable=unused-argument
        if f"{cls.__module__}.{cls.__qualname__}" not in cls._calculated:
            # we know the last nine classes in mro are going to be 'Model', '_MyMutableMapping', 'MutableMapping',
            # 'Mapping', 'Collection', 'Sized', 'Iterable', 'Container' and 'object'
            mros = cls.__mro__[:-9][::-1]  # ignore parents, and reverse the mro order
            attr_to_rest_field: typing.Dict[str, _RestField] = {  # map attribute name to rest_field property
                k: v for mro_class in mros for k, v in mro_class.__dict__.items() if k[0] != "_" and hasattr(v, "_type")
            }
            annotations = {
                k: v
                for mro_class in mros
                if hasattr(mro_class, "__annotations__")  # pylint: disable=no-member
                for k, v in mro_class.__annotations__.items()  # pylint: disable=no-member
            }
            for attr, rf in attr_to_rest_field.items():
                rf._module = cls.__module__
                if not rf._type:
                    rf._type = rf._get_deserialize_callable_from_annotation(annotations.get(attr, None))
                if not rf._rest_name_input:
                    rf._rest_name_input = attr
            cls._attr_to_rest_field: typing.Dict[str, _RestField] = dict(attr_to_rest_field.items())
            cls._calculated.add(f"{cls.__module__}.{cls.__qualname__}")

        return super().__new__(cls)  # pylint: disable=no-value-for-parameter

    def __init_subclass__(cls, discriminator: typing.Optional[str] = None) -> None:
        for base in cls.__bases__:
            if hasattr(base, "__mapping__"):  # pylint: disable=no-member
                base.__mapping__[discriminator or cls.__name__] = cls  # type: ignore  # pylint: disable=no-member

    @classmethod
    def _get_discriminator(cls, exist_discriminators) -> typing.Optional["_RestField"]:
        for v in cls.__dict__.values():
            if isinstance(v, _RestField) and v._is_discriminator and v._rest_name not in exist_discriminators:
                return v
        return None

    @classmethod
    def _deserialize(cls, data, exist_discriminators):
        if not hasattr(cls, "__mapping__"):  # pylint: disable=no-member
            return cls(data)
        discriminator = cls._get_discriminator(exist_discriminators)
        if discriminator is None:
            return cls(data)
        exist_discriminators.append(discriminator._rest_name)
        if isinstance(data, ET.Element):
            model_meta = getattr(cls, "_xml", {})
            prop_meta = getattr(discriminator, "_xml", {})
            xml_name = prop_meta.get("name", discriminator._rest_name)
            xml_ns = prop_meta.get("ns", model_meta.get("ns", None))
            if xml_ns:
                xml_name = "{" + xml_ns + "}" + xml_name

            if data.get(xml_name) is not None:
                discriminator_value = data.get(xml_name)
            else:
                discriminator_value = data.find(xml_name).text  # pyright: ignore
        else:
            discriminator_value = data.get(discriminator._rest_name)
        mapped_cls = cls.__mapping__.get(discriminator_value, cls)  # pyright: ignore # pylint: disable=no-member
        return mapped_cls._deserialize(data, exist_discriminators)

    def as_dict(self, *, exclude_readonly: bool = False) -> typing.Dict[str, typing.Any]:
        """Return a dict that can be JSONify using json.dump.

        :keyword bool exclude_readonly: Whether to remove the readonly properties.
        :returns: A dict JSON compatible object
        :rtype: dict
        """

        result = {}
        readonly_props = []
        if exclude_readonly:
            readonly_props = [p._rest_name for p in self._attr_to_rest_field.values() if _is_readonly(p)]
        for k, v in self.items():
            if exclude_readonly and k in readonly_props:  # pyright: ignore
                continue
            is_multipart_file_input = False
            try:
                is_multipart_file_input = next(
                    rf for rf in self._attr_to_rest_field.values() if rf._rest_name == k
                )._is_multipart_file_input
            except StopIteration:
                pass
            result[k] = v if is_multipart_file_input else Model._as_dict_value(v, exclude_readonly=exclude_readonly)
        return result

    @staticmethod
    def _as_dict_value(v: typing.Any, exclude_readonly: bool = False) -> typing.Any:
        if v is None or isinstance(v, _Null):
            return None
        if isinstance(v, (list, tuple, set)):
            return type(v)(Model._as_dict_value(x, exclude_readonly=exclude_readonly) for x in v)
        if isinstance(v, dict):
            return {dk: Model._as_dict_value(dv, exclude_readonly=exclude_readonly) for dk, dv in v.items()}
        return v.as_dict(exclude_readonly=exclude_readonly) if hasattr(v, "as_dict") else v


def _deserialize_model(model_deserializer: typing.Optional[typing.Callable], obj):
    if _is_model(obj):
        return obj
    return _deserialize(model_deserializer, obj)


def _deserialize_with_optional(if_obj_deserializer: typing.Optional[typing.Callable], obj):
    if obj is None:
        return obj
    return _deserialize_with_callable(if_obj_deserializer, obj)


def _deserialize_with_union(deserializers, obj):
    for deserializer in deserializers:
        try:
            return _deserialize(deserializer, obj)
        except DeserializationError:
            pass
    raise DeserializationError()


def _deserialize_dict(
    value_deserializer: typing.Optional[typing.Callable],
    module: typing.Optional[str],
    obj: typing.Dict[typing.Any, typing.Any],
):
    if obj is None:
        return obj
    if isinstance(obj, ET.Element):
        obj = {child.tag: child for child in obj}
    return {k: _deserialize(value_deserializer, v, module) for k, v in obj.items()}


def _deserialize_multiple_sequence(
    entry_deserializers: typing.List[typing.Optional[typing.Callable]],
    module: typing.Optional[str],
    obj,
):
    if obj is None:
        return obj
    return type(obj)(_deserialize(deserializer, entry, module) for entry, deserializer in zip(obj, entry_deserializers))


def _deserialize_sequence(
    deserializer: typing.Optional[typing.Callable],
    module: typing.Optional[str],
    obj,
):
    if obj is None:
        return obj
    if isinstance(obj, ET.Element):
        obj = list(obj)
    return type(obj)(_deserialize(deserializer, entry, module) for entry in obj)


def _sorted_annotations(types: typing.List[typing.Any]) -> typing.List[typing.Any]:
    return sorted(
        types,
        key=lambda x: hasattr(x, "__name__") and x.__name__.lower() in ("str", "float", "int", "bool"),
    )


def _get_deserialize_callable_from_annotation(  # pylint: disable=R0911, R0915, R0912
    annotation: typing.Any,
    module: typing.Optional[str],
    rf: typing.Optional["_RestField"] = None,
) -> typing.Optional[typing.Callable[[typing.Any], typing.Any]]:
    if not annotation:
        return None

    # is it a type alias?
    if isinstance(annotation, str):
        if module is not None:
            annotation = _get_type_alias_type(module, annotation)

    # is it a forward ref / in quotes?
    if isinstance(annotation, (str, typing.ForwardRef)):
        try:
            model_name = annotation.__forward_arg__  # type: ignore
        except AttributeError:
            model_name = annotation
        if module is not None:
            annotation = _get_model(module, model_name)

    try:
        if module and _is_model(annotation):
            if rf:
                rf._is_model = True

            return functools.partial(_deserialize_model, annotation)  # pyright: ignore
    except Exception:
        pass

    # is it a literal?
    try:
        if annotation.__origin__ is typing.Literal:  # pyright: ignore
            return None
    except AttributeError:
        pass

    # is it optional?
    try:
        if any(a for a in annotation.__args__ if a == type(None)):  # pyright: ignore
            if len(annotation.__args__) <= 2:  # pyright: ignore
                if_obj_deserializer = _get_deserialize_callable_from_annotation(
                    next(a for a in annotation.__args__ if a != type(None)), module, rf  # pyright: ignore
                )

                return functools.partial(_deserialize_with_optional, if_obj_deserializer)
            # the type is Optional[Union[...]], we need to remove the None type from the Union
            annotation_copy = copy.copy(annotation)
            annotation_copy.__args__ = [a for a in annotation_copy.__args__ if a != type(None)]  # pyright: ignore
            return _get_deserialize_callable_from_annotation(annotation_copy, module, rf)
    except AttributeError:
        pass

    # is it union?
    if getattr(annotation, "__origin__", None) is typing.Union:
        # initial ordering is we make `string` the last deserialization option, because it is often them most generic
        deserializers = [
            _get_deserialize_callable_from_annotation(arg, module, rf)
            for arg in _sorted_annotations(annotation.__args__)  # pyright: ignore
        ]

        return functools.partial(_deserialize_with_union, deserializers)

    try:
        if annotation._name == "Dict":  # pyright: ignore
            value_deserializer = _get_deserialize_callable_from_annotation(
                annotation.__args__[1], module, rf  # pyright: ignore
            )

            return functools.partial(
                _deserialize_dict,
                value_deserializer,
                module,
            )
    except (AttributeError, IndexError):
        pass
    try:
        if annotation._name in ["List", "Set", "Tuple", "Sequence"]:  # pyright: ignore
            if len(annotation.__args__) > 1:  # pyright: ignore
                entry_deserializers = [
                    _get_deserialize_callable_from_annotation(dt, module, rf)
                    for dt in annotation.__args__  # pyright: ignore
                ]
                return functools.partial(_deserialize_multiple_sequence, entry_deserializers, module)
            deserializer = _get_deserialize_callable_from_annotation(
                annotation.__args__[0], module, rf  # pyright: ignore
            )

            return functools.partial(_deserialize_sequence, deserializer, module)
    except (TypeError, IndexError, AttributeError, SyntaxError):
        pass

    def _deserialize_default(
        deserializer,
        obj,
    ):
        if obj is None:
            return obj
        try:
            return _deserialize_with_callable(deserializer, obj)
        except Exception:
            pass
        return obj

    if get_deserializer(annotation, rf):
        return functools.partial(_deserialize_default, get_deserializer(annotation, rf))

    return functools.partial(_deserialize_default, annotation)


def _deserialize_with_callable(
    deserializer: typing.Optional[typing.Callable[[typing.Any], typing.Any]],
    value: typing.Any,
):  # pylint: disable=too-many-return-statements
    try:
        if value is None or isinstance(value, _Null):
            return None
        if isinstance(value, ET.Element):
            if deserializer is str:
                return value.text or ""
            if deserializer is int:
                return int(value.text) if value.text else None
            if deserializer is float:
                return float(value.text) if value.text else None
            if deserializer is bool:
                return value.text == "true" if value.text else None
        if deserializer is None:
            return value
        if deserializer in [int, float, bool]:
            return deserializer(value)
        if isinstance(deserializer, CaseInsensitiveEnumMeta):
            try:
                return deserializer(value)
            except ValueError:
                # for unknown value, return raw value
                return value
        if isinstance(deserializer, type) and issubclass(deserializer, Model):
            return deserializer._deserialize(value, [])
        return typing.cast(typing.Callable[[typing.Any], typing.Any], deserializer)(value)
    except Exception as e:
        raise DeserializationError() from e


def _deserialize(
    deserializer: typing.Any,
    value: typing.Any,
    module: typing.Optional[str] = None,
    rf: typing.Optional["_RestField"] = None,
    format: typing.Optional[str] = None,
) -> typing.Any:
    if isinstance(value, PipelineResponse):
        value = value.http_response.json()
    if rf is None and format:
        rf = _RestField(format=format)
    if not isinstance(deserializer, functools.partial):
        deserializer = _get_deserialize_callable_from_annotation(deserializer, module, rf)
    return _deserialize_with_callable(deserializer, value)


class _RestField:
    def __init__(
        self,
        *,
        name: typing.Optional[str] = None,
        type: typing.Optional[typing.Callable] = None,  # pylint: disable=redefined-builtin
        is_discriminator: bool = False,
        visibility: typing.Optional[typing.List[str]] = None,
        default: typing.Any = _UNSET,
        format: typing.Optional[str] = None,
        is_multipart_file_input: bool = False,
        xml: typing.Optional[typing.Dict[str, typing.Any]] = None,
    ):
        self._type = type
        self._rest_name_input = name
        self._module: typing.Optional[str] = None
        self._is_discriminator = is_discriminator
        self._visibility = visibility
        self._is_model = False
        self._default = default
        self._format = format
        self._is_multipart_file_input = is_multipart_file_input
        self._xml = xml if xml is not None else {}

    @property
    def _class_type(self) -> typing.Any:
        return getattr(self._type, "args", [None])[0]

    @property
    def _rest_name(self) -> str:
        if self._rest_name_input is None:
            raise ValueError("Rest name was never set")
        return self._rest_name_input

    def __get__(self, obj: Model, type=None):  # pylint: disable=redefined-builtin
        # by this point, type and rest_name will have a value bc we default
        # them in __new__ of the Model class
        item = obj.get(self._rest_name)
        if item is None:
            return item
        if self._is_model:
            return item
        return _deserialize(self._type, _serialize(item, self._format), rf=self)

    def __set__(self, obj: Model, value) -> None:
        if value is None:
            # we want to wipe out entries if users set attr to None
            try:
                obj.__delitem__(self._rest_name)
            except KeyError:
                pass
            return
        if self._is_model:
            if not _is_model(value):
                value = _deserialize(self._type, value)
            obj.__setitem__(self._rest_name, value)
            return
        obj.__setitem__(self._rest_name, _serialize(value, self._format))

    def _get_deserialize_callable_from_annotation(
        self, annotation: typing.Any
    ) -> typing.Optional[typing.Callable[[typing.Any], typing.Any]]:
        return _get_deserialize_callable_from_annotation(annotation, self._module, self)


def rest_field(
    *,
    name: typing.Optional[str] = None,
    type: typing.Optional[typing.Callable] = None,  # pylint: disable=redefined-builtin
    visibility: typing.Optional[typing.List[str]] = None,
    default: typing.Any = _UNSET,
    format: typing.Optional[str] = None,
    is_multipart_file_input: bool = False,
    xml: typing.Optional[typing.Dict[str, typing.Any]] = None,
) -> typing.Any:
    return _RestField(
        name=name,
        type=type,
        visibility=visibility,
        default=default,
        format=format,
        is_multipart_file_input=is_multipart_file_input,
        xml=xml,
    )


def rest_discriminator(
    *,
    name: typing.Optional[str] = None,
    type: typing.Optional[typing.Callable] = None,  # pylint: disable=redefined-builtin
    visibility: typing.Optional[typing.List[str]] = None,
    xml: typing.Optional[typing.Dict[str, typing.Any]] = None,
) -> typing.Any:
    return _RestField(name=name, type=type, is_discriminator=True, visibility=visibility, xml=xml)


def serialize_xml(model: Model, exclude_readonly: bool = False) -> str:
    """Serialize a model to XML.

    :param Model model: The model to serialize.
    :param bool exclude_readonly: Whether to exclude readonly properties.
    :returns: The XML representation of the model.
    :rtype: str
    """
    return ET.tostring(_get_element(model, exclude_readonly), encoding="unicode")  # type: ignore


def _get_element(
    o: typing.Any,
    exclude_readonly: bool = False,
    parent_meta: typing.Optional[typing.Dict[str, typing.Any]] = None,
    wrapped_element: typing.Optional[ET.Element] = None,
) -> typing.Union[ET.Element, typing.List[ET.Element]]:
    if _is_model(o):
        model_meta = getattr(o, "_xml", {})

        # if prop is a model, then use the prop element directly, else generate a wrapper of model
        if wrapped_element is None:
            wrapped_element = _create_xml_element(
                model_meta.get("name", o.__class__.__name__),
                model_meta.get("prefix"),
                model_meta.get("ns"),
            )

        readonly_props = []
        if exclude_readonly:
            readonly_props = [p._rest_name for p in o._attr_to_rest_field.values() if _is_readonly(p)]

        for k, v in o.items():
            # do not serialize readonly properties
            if exclude_readonly and k in readonly_props:
                continue

            prop_rest_field = _get_rest_field(o._attr_to_rest_field, k)
            if prop_rest_field:
                prop_meta = getattr(prop_rest_field, "_xml").copy()
                # use the wire name as xml name if no specific name is set
                if prop_meta.get("name") is None:
                    prop_meta["name"] = k
            else:
                # additional properties will not have rest field, use the wire name as xml name
                prop_meta = {"name": k}

            # if no ns for prop, use model's
            if prop_meta.get("ns") is None and model_meta.get("ns"):
                prop_meta["ns"] = model_meta.get("ns")
                prop_meta["prefix"] = model_meta.get("prefix")

            if prop_meta.get("unwrapped", False):
                # unwrapped could only set on array
                wrapped_element.extend(_get_element(v, exclude_readonly, prop_meta))
            elif prop_meta.get("text", False):
                # text could only set on primitive type
                wrapped_element.text = _get_primitive_type_value(v)
            elif prop_meta.get("attribute", False):
                xml_name = prop_meta.get("name", k)
                if prop_meta.get("ns"):
                    ET.register_namespace(prop_meta.get("prefix"), prop_meta.get("ns"))  # pyright: ignore
                    xml_name = "{" + prop_meta.get("ns") + "}" + xml_name  # pyright: ignore
                # attribute should be primitive type
                wrapped_element.set(xml_name, _get_primitive_type_value(v))
            else:
                # other wrapped prop element
                wrapped_element.append(_get_wrapped_element(v, exclude_readonly, prop_meta))
        return wrapped_element
    if isinstance(o, list):
        return [_get_element(x, exclude_readonly, parent_meta) for x in o]  # type: ignore
    if isinstance(o, dict):
        result = []
        for k, v in o.items():
            result.append(
                _get_wrapped_element(
                    v,
                    exclude_readonly,
                    {
                        "name": k,
                        "ns": parent_meta.get("ns") if parent_meta else None,
                        "prefix": parent_meta.get("prefix") if parent_meta else None,
                    },
                )
            )
        return result

    # primitive case need to create element based on parent_meta
    if parent_meta:
        return _get_wrapped_element(
            o,
            exclude_readonly,
            {
                "name": parent_meta.get("itemsName", parent_meta.get("name")),
                "prefix": parent_meta.get("itemsPrefix", parent_meta.get("prefix")),
                "ns": parent_meta.get("itemsNs", parent_meta.get("ns")),
            },
        )

    raise ValueError("Could not serialize value into xml: " + o)


def _get_wrapped_element(
    v: typing.Any,
    exclude_readonly: bool,
    meta: typing.Optional[typing.Dict[str, typing.Any]],
) -> ET.Element:
    wrapped_element = _create_xml_element(
        meta.get("name") if meta else None, meta.get("prefix") if meta else None, meta.get("ns") if meta else None
    )
    if isinstance(v, (dict, list)):
        wrapped_element.extend(_get_element(v, exclude_readonly, meta))
    elif _is_model(v):
        _get_element(v, exclude_readonly, meta, wrapped_element)
    else:
        wrapped_element.text = _get_primitive_type_value(v)
    return wrapped_element


def _get_primitive_type_value(v) -> str:
    if v is True:
        return "true"
    if v is False:
        return "false"
    if isinstance(v, _Null):
        return ""
    return str(v)


def _create_xml_element(tag, prefix=None, ns=None):
    if prefix and ns:
        ET.register_namespace(prefix, ns)
    if ns:
        return ET.Element("{" + ns + "}" + tag)
    return ET.Element(tag)


def _deserialize_xml(
    deserializer: typing.Any,
    value: str,
) -> typing.Any:
    element = ET.fromstring(value)  # nosec
    return _deserialize(deserializer, element)


def _convert_element(e: ET.Element):
    # dict case
    if len(e.attrib) > 0 or len({child.tag for child in e}) > 1:
        dict_result: typing.Dict[str, typing.Any] = {}
        for child in e:
            if dict_result.get(child.tag) is not None:
                if isinstance(dict_result[child.tag], list):
                    dict_result[child.tag].append(_convert_element(child))
                else:
                    dict_result[child.tag] = [dict_result[child.tag], _convert_element(child)]
            else:
                dict_result[child.tag] = _convert_element(child)
        dict_result.update(e.attrib)
        return dict_result
    # array case
    if len(e) > 0:
        array_result: typing.List[typing.Any] = []
        for child in e:
            array_result.append(_convert_element(child))
        return array_result
    # primitive case
    return e.text
