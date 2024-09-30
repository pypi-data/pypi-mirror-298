[![Stand With Ukraine](https://raw.githubusercontent.com/vshymanskyy/StandWithUkraine/main/banner-direct-single.svg)](https://stand-with-ukraine.pp.ua)

# [DCS] Split By First Line

The components is part of [Content Settings Family](https://django-content-settings.readthedocs.io/) and allows you to put a multiple values in one setting using a splitter defined in the first line of the 

## Overview

### SplitByFirstLine

Split a given text value into multiple values using a splitter that is defined inside of the value. The result of splitting will be converted using type inside of the `split_type` attribute. Each value can be given under the same name suffix (but lowercased), but also the returned value can be chosen by the function `split_default_chooser` attribute. The first line will be used as a splitter if the value from the `split_default_key` attribute is in this line. It may sound confusing, but let me show you an example:

```python
from content_settings.types.array import SplitByFirstLine

MY_VAR = SplitByFirstLine(
 split_default_key="MAIN",
 split_type=SimpleDecimal()
)

# now the variable will work as simple Decimal, with the extra suffix __main that returns the same value
# but if you update the value in admin to:
"""=== MAIN ===
10.67
=== SECOND ===
4.12
"""
# your variable will work a bit different
content_settings.MY_VAR == Decimal("10.67")
content_settings.MY_VAR__main == Decimal("10.67")
content_settings.MY_VAR__second == Decimal("4.12")

# the first line in the value === MAIN === defines the splitter rule, which means the following value will work the same
"""!!! MAIN !!!
10.67
!!! SECOND !!!
4.12
"""
```

It has a wide variety of attributes:

- **split_type** - the type which will be used for each value. You can use a dict to set a specific type for each key
- **split_default_key** - the key which will be used for the first line
- **split_default_chooser** - the function which will be used for choosing default value
- **split_not_found** - what should be done if the required key is not found. `NOT_FOUND.DEFAULT` - return default value, `NOT_FOUND.KEY_ERROR` raise an exception and `NOT_FOUND.VALUE` return value from **split_not_found_value**
- **split_key_validator** - a function that validates a key. You can use a function `split_validator_in` for the validator value
- **split_key_validator_failed** - two passible values `SPLIT_FAIL.IGNORE`(default) and `SPLIT_FAIL.RAISE`. What should the system do if validation is failed. `SPLIT_FAIL.IGNORE` - just use the line with an invalid key as a value for the previous key. `SPLIT_FAIL.RAISE` - raise `ValidationError`

### SplitTranslation

same as `SplitByFirstLine` but the default value will be chosen based on current django translation `django.utils.translation.get_language`
