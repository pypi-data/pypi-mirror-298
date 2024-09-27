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
    letters: bool = False,
    uppercase: bool = True,
    lowercase: bool = True,
    digits: bool = True,
    symbols: bool = False,
    first_char_type: Optional[str] = None
) -> str:
    """
    Generates a random string with the specified length and character types.

    :param length: The total length of the random string.
    :param letters: Include both uppercase and lowercase letters.
    :param uppercase: Include uppercase letters (overridden if letters is True).
    :param lowercase: Include lowercase letters (overridden if letters is True).
    :param digits: Include digits.
    :param symbols: Include symbols.
    :param first_char_type: If specified, the first character will be of this type.
                            Options are 'letters', 'uppercase', 'lowercase', 'digits', 'symbols'.
    :return: A random string.
    :raises ValueError: If invalid parameters are provided.
    """
    if length <= 0:
        raise ValueError("Length must be a positive integer.")

    # Build the character pool
    characters = ''
    if letters:
        characters += CHAR_TYPE_MAP['letter']
    else:
        if uppercase:
            characters += CHAR_TYPE_MAP['uppercase']
        if lowercase:
            characters += CHAR_TYPE_MAP['lowercase']
    if digits:
        characters += CHAR_TYPE_MAP['digits']
    if symbols:
        characters += CHAR_TYPE_MAP['symbols']

    if not characters:
        raise ValueError("At least one character type must be selected.")

    # Handle the first character
    if first_char_type:
        if first_char_type not in CHAR_TYPE_MAP:
            raise ValueError(f"Invalid first_char_type specified: {first_char_type}")
        if first_char_type == 'letters' and not letters:
            raise ValueError("Cannot use 'letters' as first_char_type when letters is False")
        if first_char_type == 'uppercase' and not (letters or uppercase):
            raise ValueError("Cannot use 'uppercase' as first_char_type when both letters and uppercase are False")
        if first_char_type == 'lowercase' and not (letters or lowercase):
            raise ValueError("Cannot use 'lowercase' as first_char_type when both letters and lowercase are False")
        if first_char_type == 'digits' and not digits:
            raise ValueError("Cannot use 'digits' as first_char_type when digits is False")
        if first_char_type == 'symbols' and not symbols:
            raise ValueError("Cannot use 'symbols' as first_char_type when symbols is False")
        first_char = secrets.choice(CHAR_TYPE_MAP[first_char_type])
        length -= 1
    else:
        first_char = ''

    # Generate the remaining characters
    random_string = ''.join(secrets.choice(characters) for _ in range(length))

    return first_char + random_string

def generate_random_strings(
    count: int,
    length: int,
    letters: bool = False,
    uppercase: bool = True,
    lowercase: bool = True,
    digits: bool = True,
    symbols: bool = False,
    first_char_type: Optional[str] = None
) -> List[str]:
    """
    Generates a list of random strings.

    :param count: The number of random strings to generate.
    :param length: The length of each random string.
    :param letters: Include both uppercase and lowercase letters.
    :param uppercase: Include uppercase letters (overridden if letters is True).
    :param lowercase: Include lowercase letters (overridden if letters is True).
    :param digits: Include digits.
    :param symbols: Include symbols.
    :param first_char_type: Type for the first character.
    :return: A list of random strings.
    :raises ValueError: If invalid parameters are provided.
    """
    if count <= 0:
        raise ValueError("Count must be a positive integer.")

    return [
        generate_random_string(length, letters, uppercase, lowercase, digits, symbols, first_char_type)
        for _ in range(count)
    ]
