# randstrgen/generator.py

import secrets
import string
from typing import List, Optional

# Mapping from type names to character sets
CHAR_TYPE_MAP = {
    'uppercase': string.ascii_uppercase,
    'lowercase': string.ascii_lowercase,
    'letter':    string.ascii_letters,  # Both uppercase and lowercase
    'digits':    string.digits,
    'symbols':   string.punctuation,
}

def generate_random_string(
    length: int,
    char_types: Optional[List[str]] = None,
    first_char_type: Optional[str] = None
) -> str:
    """
    Generates a random string with the specified length and character types.

    :param length: The total length of the random string.
    :param char_types: A list of character types to include. Options are
                       'uppercase', 'lowercase', 'letter', 'digits', 'symbols'.
                       Defaults to ['uppercase', 'digits'] if not specified.
    :param first_char_type: If specified, the first character will be of this type.
                            Options are the same as for char_types.
    :return: A random string.
    :raises ValueError: If invalid parameters are provided.
    """
    if length <= 0:
        raise ValueError("Length must be a positive integer.")

    if not char_types:
        char_types = ['uppercase', 'digits']

    # Build the character pool
    try:
        characters = ''.join([CHAR_TYPE_MAP[ct] for ct in char_types])
    except KeyError as e:
        raise ValueError(f"Invalid character type specified: {e.args[0]}")

    if not characters:
        raise ValueError("Character pool is empty. Please select valid character types.")

    # Handle the first character
    if first_char_type:
        if first_char_type not in CHAR_TYPE_MAP:
            raise ValueError(f"Invalid first_char_type specified: {first_char_type}")
        first_char = secrets.choice(CHAR_TYPE_MAP[first_char_type])
        if length == 0:
            raise ValueError("Length must be at least 1 when specifying a first_char_type.")
        length -= 1
    else:
        first_char = ''

    # Generate the remaining characters
    random_string = ''.join(secrets.choice(characters) for _ in range(length))

    return first_char + random_string

def generate_random_strings(
    count: int,
    length: int,
    char_types: Optional[List[str]] = None,
    first_char_type: Optional[str] = None
) -> List[str]:
    """
    Generates a list of random strings.

    :param count: The number of random strings to generate.
    :param length: The length of each random string.
    :param char_types: Character types to include.
    :param first_char_type: Type for the first character.
    :return: A list of random strings.
    :raises ValueError: If invalid parameters are provided.
    """
    if count <= 0:
        raise ValueError("Count must be a positive integer.")

    return [
        generate_random_string(length, char_types, first_char_type)
        for _ in range(count)
    ]
