import json
import io
import os
import inspect
import sys
import io
import service
import logger

from functools import partial

logging = logger.Logger()
logging.setLevel(logger.INFO)


class CLI:
    commands = None
    inputstream = None
    service = None
    allowed_characters = set('123456789*0#')

    def __init__(self, commands, inputstream):
        self.commands = commands
        self.inputstream = inputstream
        self.service = service.Service()

    def validate(self, digits):
        return all(char in self.allowed_characters for char in digits)

    def execute(self):

        if len(self.commands) == 1:

            f = io.BytesIO()
            for chunk in iter(partial(self.inputstream.read, 16384), b''):
                f.write(chunk)

            digits = f.getvalue().decode().strip()

            if self.validate(digits) and digits != "":
                logging.info("Digits: " + digits)
                self.service.command(digits)
            elif digits == "":
                logging.warning("Empty input. Disregarding command.")
            else:
                logging.warning("Input contains invalid characters. Disregarding command.")

            return None

        elif self.commands[1] == "logs":
            return self.service.tail()

        return None
