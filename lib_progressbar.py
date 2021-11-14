# Global libaries
import sys
from typing import Generator, Iterable
from datetime import datetime, timedelta

# local Libaries
from lib_time import chhop_microseconds


def progress_bar(item_iterable, bar_length: int = 20, prefix: str = 'PROCESSING: ') -> Generator:
    """
    Usage Example:
    for i in progress_bar(range(100)):
        sleep(0.1)
    :param prefix: 'PROCESSING: '
    :param item_iterable:
    :param bar_length: std = 60
    :return:
    """
    if not item_iterable:
        return

    start_time = datetime.now()
    item_count = len(item_iterable)

    if item_count == 0:
        return

    def update():
        bar_progress = int(bar_length * index / item_count)
        runtime = datetime.now() - start_time
        remaining_time = max(runtime / max(index - 1, 1) * item_count - runtime, timedelta(seconds=0))
        string = str(f'\r{prefix}'
                     f'[{"#" * bar_progress}{"." * (bar_length - bar_progress)}] '
                     f'{index}/{item_count} '
                     f'Runtime: {chhop_microseconds(runtime)} '
                     f'Remaining: {chhop_microseconds(remaining_time)}')
        sys.stdout.write(string)
        sys.stdout.flush()

    for index, item in enumerate(item_iterable, start=1):
        update()
        yield item

    sys.stdout.write(" - Done! \n")
    sys.stdout.flush()
