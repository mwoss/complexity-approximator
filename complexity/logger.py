import logging


def log_fun(fun):
    def decor(*args):
        log_msg_dec('Calling function: ' + fun.__name__ + ' with args: ' + str(args))
        return fun(*args)

    return decor


def log_msg_dec(msg):
    logging.warning(msg)


class Logger:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.handler = logging.FileHandler("{0}.log".format(__name__))
        self.format = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
        self.handler.setFormatter(self.format)
        self.logger.addHandler(self.handler)
        self.logger.setLevel(logging.INFO)

    def quit(self):
        logging.shutdown(self.handler)
        return

    def log_msg(self, msg, level):
        log_level = logging.getLevelName(level)
        self.logger.log(log_level, msg)

    def set_logging_lvl(self, level):
        log_level = logging.getLevelName(level)
        self.logger.setLevel(log_level)
