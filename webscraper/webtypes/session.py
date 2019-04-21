import datetime
import dateutil.parser

class Session:
    def __init__(self, start_datetime="not set", end_datetime="not set"):
        self.start_datetime = start_datetime
        self.end_datetime = end_datetime

    def update_start_datetime(self):
        self.start_datetime = datetime.datetime.now().isoformat()

    def update_end_datetime(self):
        self.end_datetime = datetime.datetime.now().isoformat()

    def __str__(self):
        return ("{{"
            "start_datetime={}, "
            "end_datetime={}"
        "}}").format(
            self.start_datetime, 
            self.end_datetime 
        )   

    def __repr__(self):
        return self.__str__()


    def get_delta_time(self):
        return dateutil.parser.parse(self.end_datetime) - dateutil.parser.parse(self.start_datetime)