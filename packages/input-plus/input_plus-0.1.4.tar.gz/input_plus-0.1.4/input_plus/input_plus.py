import msvcrt
import re
import sys
from typing import Callable, Tuple


def input_plus(printer: Callable[[str], None],
               selector: Callable[[str], Tuple[bool, str]],
               validator: Callable[[str], bool] = None,
               special_actions: Callable[[bytes], None] = None) -> str:
    '''
    A function that allows for more advanced input handling than the built-in input function.

    Args:
        Printer: A function that takes the user input string and prints it to the console.
        Selector: A function that takes the user input string and returns a Tuple[bool, str].
            Bool: A boolean indicating if the input is valid.
            Str: The value to return if the input is valid.
            Use this verification to check if the input the user is attempting to submit is valid.
        Validator: A function that takes the user input string and returns a boolean indicating if the input is valid.
            Use this verification to check if the input the user is typing is valid. If False, the input will blocked.
        Special Actions: A function that takes user input string as bytes and performs a special action based on the input.
    '''
    input_string = ''
    printer(input_string)
    while True:
        input_char = msvcrt.getwch() # Get the input character
        is_special_key = False

        # Special actions
        if input_char == '\x00' or input_char == '\xe0':
            is_special_key = True
            input_char += msvcrt.getwch()

        char_code = input_char.encode()
        # Control characters
        if char_code == b'\x03': # Ctrl+C
            print()
            raise KeyboardInterrupt
        elif char_code == b'\x0d': # Enter key
            is_valid, value = selector(input_string)
            if is_valid:
                print()
                return value
        elif char_code == b'\x08': # Backspace
            input_string = input_string[:-1]
        elif char_code == b'\x17': # Ctrl+Backspace
            input_string = re.sub(r'((?<=\s)|(?<=^))\w*\s?$', '', input_string)
        elif char_code == b'\x1b': # Escape key
            raise Exception('User escaped input')

        # User inputs
        elif is_special_key and special_actions is not None: # Special keys
            special_actions(char_code)
        else: # Regular characters
            if validator is None or validator(f'{input_string}{input_char}'):
                input_string += input_char

        printer(input_string)