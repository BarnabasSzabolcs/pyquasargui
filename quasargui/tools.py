import traceback
from typing import List


def flatten(lst: List[list]) -> list:
    return [item for sublist in lst for item in sublist]


def merge_classes(*args) -> str:
    if len(args) == 1:
        return ' '.join(args[0]) if isinstance(args[0], list) else args[0]
    elif len(args) == 0:
        return ''
    else:
        return (merge_classes(args[0]) + ' ' + merge_classes(*args[1:])).strip()


def build_props(defaults: dict, props: dict, specials: dict = None) -> dict:
    my_props = {}
    my_props.update(defaults)
    props = props or {}
    my_props.update(props)
    if specials is None:
        return my_props
    my_props.update({
        prop_name: value
        for prop_name, value in specials.items()
        if prop_name not in props
        if value is not None
    })
    return my_props


def str_between(source: str, from_str: str, to_str: str) -> str:
    if not from_str or not to_str:
        raise ValueError('from_str or to_str is empty (called with {})'.format(
            {'source': source, 'from_str': from_str, 'to_str': to_str}
        ))
    try:
        return source.split(from_str, 1)[1].split(to_str, 1)[0]
    except IndexError:
        return ''


def print_error(e):
    print("\n\nERROR {}: {}".format(e.__class__.__name__, e))
    print(traceback.format_exc())
