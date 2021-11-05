# -*- coding: utf-8 -*-


def check_string(string: str, chars: list) -> bool:
    """
    Returns True if one element of chars is in the string.
    :param string: String to check.
    :param chars: list of strings to check if one of it is in the string.
    :return: bool
    """
    return any((char in string) for char in chars)


def str2ascii(str_input: str) -> list:
    """
    convert a string to a list of asci dec values
    :param str_input:
    :return: A list of decimal values which represent string
    """
    return [ord(char) for char in str_input]


