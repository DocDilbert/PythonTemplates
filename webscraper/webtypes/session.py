from datetime import datetime
import dateutil.parser

class Session:
    def __init__(self, start_datetime=None, end_datetime=None):
        self.start_datetime = start_datetime
        self.end_datetime = end_datetime

    @classmethod
    def from_timestamps(cls, start_timestamp, end_timestamp):
        start_datetime = datetime.fromtimestamp(start_timestamp)
        end_datetime = datetime.fromtimestamp(end_timestamp)
        return cls(start_datetime, end_datetime)

    def update_start_datetime(self):
        self.start_datetime = datetime.now()

    def update_end_datetime(self):
        self.end_datetime = datetime.now()

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
        return self.end_datetime - self.start_datetime