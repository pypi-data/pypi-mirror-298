from typing import Any, Callable


def parse_dict(
        data: dict,
        mapping: dict[str, str | tuple[str]],
        default: Any = None,
        converter: dict[str, Callable[[str], Any]] = None,
        strict_mode: bool = False
) -> dict:
    """
    :param data: {: } original data
    :param mapping: {default field name: original data index name or recursive index name of original data}
    :param default: if a value is not found, this default value will be assigned to the value
    :param converter: if a value is in converter, the value will be converted according to the
    corresponding Callable
    :param strict_mode: when a value not be found, raise error if True else don't raise
    :return: {: } parsed dict data and return a new dict
    """
    final = {}
    for field_key, index in mapping.items():
        field_value = data
        if isinstance(index, str):
            field_value = field_value.get(index, default)
        elif isinstance(index, tuple):
            for sub_index in index:
                field_value = field_value.get(sub_index, default)
                if field_value == default:
                    break
        else:
            raise TypeError(f'func: parse_dict, index type: {type(index)}')

        if strict_mode is True:
            if field_value == default:
                raise KeyError(f'no value be found for key: {index}')

        if isinstance(converter, dict):
            converter_call = converter.get(field_value)
            if converter_call:
                field_value = converter_call(field_value)
        final[field_key] = field_value

    return final
