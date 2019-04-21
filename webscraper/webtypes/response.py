from  datetime import datetime, timedelta

class Response:
    def __init__(self, status_code, date, content_type):
        self.content_type=content_type
        self.status_code=status_code
        self.date = date
        
    
    @classmethod
    def fromGMT(cls, status_code, date_gmt, content_type):
        dt = datetime.strptime(date_gmt, '%a, %d %b %Y %H:%M:%S %Z')

        # Assume time is in gmt ... got to local time instead
        dt += timedelta(hours=2)

        return cls(status_code, dt, content_type)

    def __str__(self): 
        return "{{status_code={}, date=\"{}\", content_type=\"{}\"}}".format(
            self.status_code, 
            self.date,
            self.content_type
        )

    def __repr__(self):
        return self.__str__()
