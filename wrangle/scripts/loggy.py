import logging
from colorama import Fore, Back, Style


LOG_TEMPLATE =  Back.BLACK + \
                Fore.WHITE + \
                '%(asctime)s %(name)s %(levelname)s: ' + \
                Style.RESET_ALL + \
                Back.BLACK + \
                Style.BRIGHT + \
                '{message_color}' + \
                '%(message)s' + \
                Style.RESET_ALL

class MyFormatter(logging.Formatter):
    def format(self, record):
        if record.levelno >= logging.ERROR:
            msgcolor = Fore.RED
        elif record.levelno >= logging.WARNING:
            msgcolor = Fore.YELLOW
        else:
            msgcolor = Fore.GREEN

        return logging.Formatter(LOG_TEMPLATE.format(message_color=msgcolor),
                                                     datefmt='%Y-%m-%d %H:%M:%S %z').format(record)



def loggy(name=""):
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(MyFormatter())

    mylogger = logging.getLogger(name)
    mylogger.addHandler(ch)
    mylogger.setLevel(logging.DEBUG)

    return mylogger
