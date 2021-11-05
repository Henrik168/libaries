# Global Libaries
import threading
from time import sleep
from queue import Queue
from enum import auto
import RPi.GPIO as GPIO

# Local Libraries
from lib_log import Log


class GpioHandler(threading.Thread):
    FALLING = auto()
    RISING = auto()

    def __init__(self, log: Log,
                 queue_input: Queue = None,
                 queue_output: Queue = None):

        self.log = log
        if not queue_input:
            queue_input = Queue()
        if not queue_output:
            queue_output = Queue()
        self.queue_input = queue_input
        self.queue_output = queue_output

        # Define GPIO counting
        GPIO.setmode(GPIO.BCM)
        # GPIO dict to store GPIO Information and Buffer
        self.gpio_dict = dict()

        self.queue_output = queue_output

        threading.Thread.__init__(self)
        self.daemon = True
        self.exception = None

    def close(self):
        GPIO.cleanup()

    def register_gpio_input(self, gpio: int, edge: auto = RISING):
        """Register new Inputs
         creates a buffer list for each input
         set up GPIO """
        if gpio in self.gpio_dict.keys():
            raise KeyError(f'GPIO: {gpio} is already registered.')
        if edge not in (self.RISING, self.FALLING):
            raise KeyError(f'Edge variable has to be Rising: {self.RISING} or Falling: {self.FALLING} not: {edge}.')

        # setup GPIO
        GPIO.setup(gpio, GPIO.IN)
        # setup dictionary to store GPIO Information
        self.gpio_dict[gpio] = dict(buffer=[int(GPIO.input(gpio))] * 3, edge=edge, last_value=bool(GPIO.input(gpio)))

    def debounce_gpio(self, gpio: int) -> bool:
        """Returns True if the Input is HIGH during 2 or more of the last three measurements.
        """
        self.gpio_dict[gpio]['buffer'].append(int(GPIO.input(gpio)))
        self.gpio_dict[gpio]['buffer'].pop(0)
        return sum(self.gpio_dict[gpio]['buffer']) > 1

    def read_GPIO(self, gpio: int) -> bool:
        value = self.debounce_gpio(gpio)
        last_value = self.gpio_dict[gpio]['last_value']
        self.gpio_dict[gpio]['last_value'] = value
        if value == last_value:
            return False
        if self.gpio_dict[gpio]['edge'] == self.FALLING:
            return last_value
        else:
            return value

    def run(self):
        self.log.logger.info('Start Gpio Handler.')
        try:
            while True:
                for gpio in self.gpio_dict:
                    if self.read_GPIO(gpio):
                        self.log.logger.info(f'GPIO {gpio} pressed!')
                        self.queue_output.put(gpio)
                sleep(0.1)
        except Exception as e:
            self.exception = e

    def get_exception(self):
        return self.exception
