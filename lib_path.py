# -*- coding: utf-8 -*-

# global libraries
import sys
import shutil
from os import path, makedirs, walk, sep
from datetime import datetime

# local libraries
from lib_str import check_string


def get_path(input_path: str) -> str:
    """
    Return the absolut path if path relativ to the main.py is passed in
    :param input_path:
    :return:
    """
    return path.abspath(path.join(path.dirname(sys.argv[0]), input_path))


def get_dir_path(input_path: str) -> str:
    """
    Return root path of relativ input path, checks if it is a directory
    :param input_path:
    :return:
    """
    output_path = get_path(input_path)
    if not path.isdir(output_path):
        raise NotADirectoryError(f"Directory: {output_path} does not exists!")
    return output_path


def get_file_path(input_path: str) -> str:
    """
    Return root path of relativ input path, checks if it is a file
    :param input_path:
    :return:
    """
    output_path = get_path(input_path)
    if not path.isfile(output_path):
        raise FileNotFoundError(f"File: {output_path} does not exists!")
    return output_path


def make_path(input_path: str) -> str:
    """
    Create a direcotry if it not exists.
    :param input_path:
    :return: the path as string
    """
    output_path = get_path(input_path)
    if path.isfile(output_path):
        raise NotADirectoryError(f"Path: {output_path} is a File!")
    if path.ismount(output_path):
        raise IsADirectoryError(f"Directory: {output_path} is a mount!")
    if not path.isdir(output_path):
        makedirs(output_path)

    return output_path


def get_DiskSpace(input_path):
    """
    returns free diskspace of a path
    :param input_path:
    :return:
    """
    dir_name = get_dir_path(input_path)
    total, used, free = shutil.disk_usage(dir_name)
    total = round(total / 2 ** 20, 3)
    used = round(used / 2 ** 20, 3)
    free = round(free / 2 ** 20, 3)
    return free


def get_timestamp(input_path: str) -> datetime:
    """
    returns datetime timestamp of path_item
    :param input_path:
    :return:
    """
    return datetime.fromtimestamp(path.getctime(input_path))


class Crawler:
    def __init__(self, relative: bool = False):
        """
        Create new instance of FileCrawler
        :param relative: if True returns just relative paths
        """
        self._relative = relative
        self._min_date = None
        self._max_date = None
        self._chars = None

    def set_date_filter(self, min_date: datetime, max_date: datetime = datetime.now()) -> None:
        """
        Sets a min and max date filter for files.
        :param min_date:
        :param max_date:
        :return: None
        """
        self._min_date = min_date
        self._max_date = max_date

    def set_char_filter(self, chars: list) -> None:
        """
        Sets a char filter for filenames.
        :param chars: list of chars which has to be in filename (one of them)
        :return: None
        """
        self._chars = chars

    def check_date(self, file_path: str) -> bool:
        """
        :param file_path: path to the file
        :return: return true if file age is within boundaries (min - max Date).
        """
        return self._min_date < get_timestamp(get_file_path(file_path)) < self._max_date

    def run(self, root_path: str):
        """
        Find all files in actual folder and all subfolder
        :param root_path: [str]
        :return: return a list, first element is path_items, second is the path, third is list of files
        """
        root_path = get_dir_path(root_path)
        result = []
        for root, dir_list, file_list in walk(root_path):
            if self._relative:
                root = path.relpath(root, root_path)
            if self._min_date:
                file_list = [file for file in file_list if self.check_date(path.join(root, file))]
            if self._chars:
                file_list = [file for file in file_list if check_string(path.join(root, file), self._chars)]
            if file_list:  # store if files available in directory
                result.append([root.split(sep), root, file_list])
        return result
