# -*- coding: utf-8 -*-

# global libraries
from datetime import datetime
from os import path
from csv import reader, writer, QUOTE_MINIMAL
from typing import Generator, Any


def get_file_timestamp(file_path: str, str_format: str = '%Y.%m.%d') -> str:
    """
    Return string representation of timestamp (time object).
    :param file_path: path to file
    :param str_format: Format String. The default is '%Y.%m.%d'.
                   Examples: '%d.%m.%Y %H:%M:%S'
    :return:
    """
    return datetime.fromtimestamp(path.getmtime(file_path)).strftime(str_format)


def read_file(file_path: str, encoding: str = 'utf-8-sig') -> Generator:
    """
    read file and strip newlines, spaces, etc.
    :param file_path: path to the file
    :param encoding: Exampels: 'utf-8-sig'
                               'latin1'
                               'utf-16'
                               'utf-8'
    :return: a list, each row reprsents a line of file
    """
    with open(file_path, 'r', encoding=encoding) as file:
        return (line.strip() for line in file.readlines())


def read_file_binary(file_path: str) -> Generator:
    """
    read file binary and strip newlines, spaces, etc.
    :param file_path: path to the file
    :return: Returns a list of rows
    """
    with open(file_path, 'rb') as file:
        return (line.strip() for line in file.readlines())


def write_file(file_path: str, rows: list, add_line_sep: bool = True) -> None:
    """
    write a list to a file. Each row reperesent a line
    :param add_line_sep:
    :param rows: List of Rows to write to file
    :param file_path: path to the file
    :return:
    """
    mode = "a" if path.isfile(file_path) else "w"
    with open(file_path, mode) as file:
        for row in rows:
            file.write(str(row))
            file.write('\n') if add_line_sep else None


def read_csv(file_path: str, encoding: str = 'utf-8-sig', delimiter: str = ';') -> list:
    """
    read file and strip newlines, spaces, etc.
    :param delimiter: Examples ';' or ',' or ':'
    :param file_path: path to the file
    :param encoding: Exampels: 'utf-8-sig'
                               'latin1'
                               'utf-16'
                               'utf-8'
    :return: a list, each row reprsents a line of file
    """
    with open(file_path, 'r', encoding=encoding, newline='') as csv_file:
        csv_reader = reader(csv_file, delimiter=delimiter, quoting=QUOTE_MINIMAL, lineterminator='\n')
        return [row for row in csv_reader]


def write_csv(file_path: str, rows: list, decimal_char: str = ",") -> None:
    """
    write a nested list to csv File. Outer List defines the rows, inner List defines the columns
    :param decimal_char:
    :param file_path: path to the file
    :param rows: nested list which represents a table
    :return:
    """

    def decimal_parser(data: Any) -> str:
        if isinstance(data, float):
            data = str(data).replace(".", decimal_char)
        return data

    mode = "a" if path.isfile(file_path) else "w"
    with open(file_path, mode, newline='') as csv_file:
        csv_writer = writer(csv_file, delimiter=';', quotechar='|', quoting=QUOTE_MINIMAL, dialect='excel')
        for row in rows:
            parsed_row = [decimal_parser(item) for item in row]
            csv_writer.writerow(parsed_row)
