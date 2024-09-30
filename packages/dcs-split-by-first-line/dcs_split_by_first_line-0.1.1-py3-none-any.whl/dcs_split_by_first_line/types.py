from typing import Any, Optional, List, Callable, Dict
from enum import Enum, auto

from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

from content_settings.types.basic import (
    SimpleText,
    SimpleTextPreview,
    PREVIEW,
)
from content_settings.types.mixins import AdminPreviewSuffixesMixin
from content_settings.types.each import EachMixin, Keys, Values


class NOT_FOUND(Enum):
    DEFAULT = auto()
    KEY_ERROR = auto()
    VALUE = auto()


class SPLIT_FAIL(Enum):
    IGNORE = auto()
    RAISE = auto()


def split_validator_in(values: List[str]) -> Callable:
    """
    Returns a validator function that checks if a given value is in the specified list of values.
    It uses for SplitTextByFirstLine.split_key_validator.
    """

    def _(value: str) -> bool:
        return value in values

    return _


class SplitTextByFirstLine(SimpleText):
    """
    Split text by the separator that can be found in the first line.
    The result is a dictionary where the keys are the separators and the values are the text after the separator.

    If your defaukt key is "EN", the first line can be "===== EN =====" to initialize the separator.
    The next separator is initialized by the next line that starts with "=====", ends with "=====" and has a key in the middle.

    It has the following new attributes:

    * split_default_key: Optional[str] = None - the key which will be used for the first line
    * split_default_chooser: Optional[Callable] = None - the function which will be used for chosing default value
    * split_not_found - what should be done if the required key not found. `NOT_FOUND.DEFAULT` - return default value, `NOT_FOUND.KEY_ERROR` raise an exception and `NOT_FOUND.VALUE` return value from split_NOT_FOUND.VALUE
    * split_not_found_value: Any = None - value that will be returned if the required key not found and split_not_found is `NOT_FOUND.VALUE`
    * split_key_validator: Optional[Callable[[str], bool]] = None - function that validates a key. You can use a function `split_validator_in` for validator value
    * split_key_validator_failed: str = SPLIT_FAIL.IGNORE - what should be done if the key is not valid. `SPLIT_FAIL.IGNORE` - just use line with unvalid key as value for the previous key. `SPLIT_FAIL.RAISE` - raise `ValidationError`

    """

    split_default_key: Optional[str] = None
    split_default_chooser: Optional[Callable[[str], str]] = None
    split_not_found: NOT_FOUND = NOT_FOUND.DEFAULT
    split_not_found_value: Any = None
    split_key_validator: Optional[Callable[[str], bool]] = None
    split_key_validator_failed: SPLIT_FAIL = SPLIT_FAIL.IGNORE
    admin_preview_as: PREVIEW = PREVIEW.HTML

    def get_split_default_key(self):
        return self.split_default_key

    def split_default_choose(self, value):
        if self.split_default_chooser is None:
            return self.get_split_default_key()
        else:
            return self.split_default_chooser(value)

    def get_split_not_found(self):
        return self.split_not_found

    def get_split_not_found_value(self):
        return self.split_not_found_value

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        assert (
            self.get_split_default_key()
        ), "split_default_key should be set and it should not be empty"
        assert isinstance(
            self.get_split_default_key(), str
        ), "split_default_key should be str"

        assert self.split_default_chooser is None or callable(
            self.split_default_chooser
        ), "split_default_chooser should be callable or None"
        assert self.split_key_validator is None or callable(
            self.split_key_validator
        ), "split_key_validator should be callable or None"
        assert self.split_key_validator_failed in (
            SPLIT_FAIL.IGNORE,
            SPLIT_FAIL.RAISE,
        ), "split_key_validator_failed should be one of SPLIT_FAIL.IGNORE, SPLIT_FAIL.RAISE"
        assert self.get_split_not_found() in (
            NOT_FOUND.DEFAULT,
            NOT_FOUND.KEY_ERROR,
            NOT_FOUND.VALUE,
        ), "split_not_found should be one of NOT_FOUND.DEFAULT, NOT_FOUND.KEY_ERROR, NOT_FOUND.VALUE"

    def is_split_key_valid(self, key: str) -> bool:
        return self.split_key_validator is None or self.split_key_validator(key)

    def split_value(self, value: str) -> Dict[str, str]:
        """
        The main function of the type. Split the value into a dictionary of values.
        """
        lines = value.splitlines()
        if (
            not lines
            or self.get_split_default_key() not in lines[0]
            or lines[0].count(self.get_split_default_key()) > 1
        ):
            return {self.get_split_default_key(): value}

        before, after = lines[0].split(self.get_split_default_key())
        ret = {self.get_split_default_key(): []}
        cur_iter = ret[self.get_split_default_key()]
        for num, line in enumerate(lines[1:], start=2):
            if line.startswith(before) and line.endswith(after):
                line_key = line[len(before) : len(line) - len(after)]
                if self.is_split_key_valid(line_key):
                    cur_iter = ret[line_key] = []
                    continue

                if self.split_key_validator_failed == SPLIT_FAIL.RAISE:
                    raise ValidationError(
                        f"Invalid split key: {line_key} in line {num}"
                    )

            cur_iter.append(line)

        return {k: "\n".join(v) for k, v in ret.items()}

    def to_python(self, value):
        return self.split_value(value)

    def give(self, value, suffix=None):
        if suffix is None:
            suffix = self.split_default_choose(value)

        try:
            ret_val = value[suffix.upper()]
        except KeyError:
            if self.get_split_not_found() == NOT_FOUND.KEY_ERROR:
                raise
            elif self.get_split_not_found() == NOT_FOUND.DEFAULT:
                ret_val = value[self.get_split_default_key()]
            elif self.get_split_not_found() == NOT_FOUND.VALUE:
                ret_val = self.get_split_not_found_value()

        return ret_val


class SplitByFirstLine(AdminPreviewSuffixesMixin, EachMixin, SplitTextByFirstLine):
    """
    The same as SplitTextByFirstLine, but results are converted to the specified type.

    split_type attribute is used to specify the type of the values. It can be a dict to specify the type for each key.
    """

    split_type = SimpleTextPreview()

    def get_admin_preview_suffixes_default(self):
        return self.get_split_default_key()

    def get_admin_preview_suffixes(self, value: dict, name: str, **kwargs):
        keys = list(value.keys())
        keys.remove(self.get_split_default_key())
        return tuple(keys)

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        if isinstance(self.split_type, dict):
            self.each = Keys(**self.split_type)
        else:
            self.each = Values(self.split_type)

    def get_admin_preview_under_menu_object(self, value, name, suffix=None, **kwargs):
        if suffix is None:
            suffix = self.get_split_default_key()
        cs_type = self.split_type
        if isinstance(cs_type, dict):
            cs_type = self.split_type.get(suffix.upper(), SimpleTextPreview())

        value = SplitTextByFirstLine.give(self, value, suffix)
        return cs_type.get_admin_preview_object(value, name, **kwargs)


class SplitTranslation(SplitByFirstLine):
    """
    SplitByFirstLine where the default value will be chosen by the current language
    """

    split_default_key = "EN"
    split_not_found = NOT_FOUND.DEFAULT

    def get_help_format(self):
        yield _("Translated Text. ")
        yield _("The first line can initialize the translation splitter. ")
        yield _("The initial language is %(split_default_key)s. ") % {
            "split_default_key": self.split_default_key
        }
        yield _("The first line can be '===== %(split_default_key)s ====='. ") % {
            "split_default_key": self.split_default_key
        }
        yield _("The format for the value inside the translation is: ")
        yield from self.split_type.get_help_format()

    def split_default_choose(self, value):
        from django.utils.translation import get_language

        return get_language().upper().replace("-", "_")
