class TimeException(Exception):
    def __init__(self, timeout):
        self.time = timeout

    def error_msg(self):
        return "Timeout, it passed " + str(self.time)


class FewMeasurePointsException(Exception):
    pass
