# !/usr/bin/python
# coding: utf8

# Global Libaries
import threading
from time import sleep
from queue import Queue
from io import FileIO

# Local Libaries
from lib_log import Log
from lib_requests import http_request


class MessageData:
    has_data: bool = False
    last_message: str = None
    chatroom_id: int = None
    sender_id: int = None
    sender_name: str = None

    def __init__(self, result: dict = None):
        if result:
            self.has_data = True
            self.last_message = str(result["message"]["text"])
            self.chatroom_id = result["message"]["chat"]["id"]
            self.sender_id = result["message"]["from"]["id"]
            self.sender_name = result["message"]["from"]["first_name"]


class TelegrammError(Exception):
    # Error in Handlind Telegram
    pass


class TelegramMessage(threading.Thread):
    def __init__(self, bot_token: str,
                 log: Log,
                 chatroom_id: str = None,
                 queue_input: Queue = None,
                 queue_output: Queue = None):
        self.log = log

        if not queue_input:
            queue_input = Queue()
        if not queue_output:
            queue_output = Queue()
        self.queue_input = queue_input
        self.queue_output = queue_output

        self.bot_token = bot_token
        self.url = "https://api.telegram.org/bot" + self.bot_token
        self.chatroom_id = chatroom_id
        self.update_id = 0

        threading.Thread.__init__(self)
        self.daemon = True
        self.exception = None

    def request_bot_info(self) -> dict:
        # Request Bot Info
        result = http_request(self.url + "/getMe")
        if not result["result"]["username"]:
            raise TelegrammError('Missing data result["result"]["username"]')
        return result["result"]["username"]

    def send_text(self, message: str) -> None:
        # Send Text Message
        params = {"chat_id": self.chatroom_id, "text": message}
        result = http_request(self.url + "/sendMessage", params)
        if not result["ok"]:
            raise TelegrammError(f'Error sending Text Message: {message} to Chatroom{self.chatroom_id}')

    def send_photo(self, file: FileIO) -> None:
        if not file:
            raise TelegrammError(f'Got not FileIO Object to send a photo.')
        # send file to chat
        params = {"chat_id": self.chatroom_id}
        payload = {"photo": file}
        result = http_request(self.url + "/sendPhoto", params, payload)

        if not result["ok"]:
            self.send_text(result['description'])
            raise TelegrammError(f'Error sending Photo to Chatroom: {self.chatroom_id} Response: {result}')

    def request_last_messages(self) -> None:
        """
        Request Last messages.
        :return:
        """
        params = {"offset": self.update_id + 1}
        response = http_request(self.url + "/getUpdates", params)

        if not response["ok"]:
            raise TelegrammError(f'Failure in Response: {response}')

        if len(response["result"]) == 0:
            return

        # store last update ID for requesting just newer Messages
        self.update_id = response["result"][-1]["update_id"]

        # store messages to output queue
        for element in response["result"]:
            self.queue_output.put(MessageData(element))

    def run(self):
        self.log.logger.info('Start Telegram.')
        max_sec = 120
        sec_wait = 1

        while True:
            try:
                self.request_last_messages()

                if not self.queue_input.empty():
                    fn, data = self.queue_input.get()
                    fn(data)
                    self.queue_input.task_done()
                    continue

                sec_wait = 1
                sleep(1)

            except TelegrammError as e:
                self.log.logger.warning(e)
            except ConnectionError as e:
                self.log.logger.warning(e)
                self.log.logger.warning(f'Waiting for {sec_wait} seconds to retry.')
                sleep(sec_wait)
                sec_wait = min(max_sec, sec_wait * 2)  # limit waiting Time to max_sec
            except Exception as e:
                self.log.logger.exception(e)
                self.exception = e
                raise Exception(e)

    def get_exception(self):
        return self.exception
