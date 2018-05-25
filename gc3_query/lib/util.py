import re

_cts_underscore_ascii = re.compile(r'(.)([A-Z][a-z]+)')
_cts_underscore_alpha = re.compile('([a-z0-9])([A-Z])')


def camelcase_to_snake(s: str) -> str:
    """ Convert CamelCase to snake_case

`    CamelCaseString -> camel_case_string`

    :param s:
    :return:
    """
    subbed = _cts_underscore_ascii.sub(r'\1_\2', s)
    return _cts_underscore_alpha.sub(r'\1_\2', subbed).lower()
