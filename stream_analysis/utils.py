from collections import defaultdict
from typing import Callable

import regex as re


def convert_none(env_var: str, convert_cb: Callable | None = None):
    """
    Convert 'null', 'None', and empty strings to Python's None.
    """
    if env_var in ['null', 'None', 'NULL', '']:
        return None
    return convert_cb(env_var) if callable(convert_cb) else env_var


def get_secure_dict(d: dict) -> defaultdict:
    '''
    Converts a nested dictionary into a defaultdict structure, ensuring that
    any missing keys will return `None` instead of raising a KeyError.

    If a key is not present in the dictionary, accessing it will return `None` by default.

    Args:
        d (dict): The dictionary to be converted. Can include nested dictionaries.

    Returns:
        defaultdict: A `defaultdict` structure where missing keys return `None`,
            with all nested dictionaries also converted into `defaultdict`.

    Example:
        data = {
            "author": {
                "name": "John Doe",
                "details": {
                    "age": 30
                }
            }
        }

        secure_data = get_secure_dict(data)

        # Access existing keys
        print(secure_data['author']['name'])  # Output: John Doe
        print(secure_data['author']['details']['age'])  # Output: 30

        # Access missing keys (no KeyError raised)
        print(secure_data['author']['id'])  # Output: None
        print(secure_data['author']['details']['nationality'])  # Output: None
    '''
    root = defaultdict(lambda: None)
    stack = [(root, d)]

    while stack:
        parent, current_dict = stack.pop()

        for key, value in current_dict.items():
            if isinstance(value, dict):
                new_dict = defaultdict(lambda: None)
                parent[key] = new_dict
                stack.append((new_dict, value))
            else:
                parent[key] = value

    return root


def strip_symbols(s: str) -> str:
    '''
    Remove symbols, punctuation, and control characters from the start and end of a string.

    Args:
        s (str): The input string.

    Returns:
        str: The string with symbols, punctuation, and control characters removed from the edges.
    '''
    return re.sub(r'^[\p{S}\p{P}\p{C}]+|[\p{S}\p{P}\p{C}]+$', '', s).strip()


def clean_string(s: str, words: list = [], replacement: str = '') -> str:
    '''
    Cleans the input string by removing specified words, symbols, punctuation, 
    and control characters.

    This function uses a regular expression pattern to remove:
    - Custom words provided in the `words` list.
    - Emoji-like patterns, enclosed in colons (e.g., ":emoji:").
    - Text inside parentheses followed by non-word characters.
    - Mentions in the format "@username".
    - Strings composed entirely of question marks (e.g., "????").
    - Any symbol, punctuation, or control characters (matching Unicode properties \\p{S}, \\p{P}, \\p{C}).

    Args:
        s (str): The input string.
        words (list, optional): A list of words to remove from the string. Defaults to an empty list.

    Returns:
        str: The cleaned string with specified patterns and words removed, with leading and trailing whitespace stripped.
    '''
    default = r'(:[^:]+:)|(\(.*?\)[^\w\s]*)|(^\@\w+\s$)|(^\?+$)|\p{S}|\p{P}|\p{C}'
    pattern = re.compile(
        r'\b(' + '|'.join(words) + r')\b|' + default, re.IGNORECASE)

    previous_text = None
    _s = s

    while previous_text != _s:
        _s = _s.strip()
        previous_text = _s
        _s = pattern.sub(replacement, _s)

    return _s.strip() if _s else ''


def minutes_to_hhmm(minutes):
    hours = int(minutes // 60)
    mins = int(minutes % 60)
    return f'{hours:02d}:{mins:02d}'
