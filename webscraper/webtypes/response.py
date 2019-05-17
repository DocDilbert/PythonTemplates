from datetime import datetime, timedelta

BLOB_STR_LENGTH = 10


class Response:
    def __init__(self, status_code, date, content_type, content):
        self.content_type = content_type
        self.status_code = status_code
        self.date = date
        self.content = content

    @classmethod
    def fromGMT(cls, status_code, date_gmt, content_type, content):
        dt = datetime.strptime(date_gmt, "%a, %d %b %Y %H:%M:%S %Z")

        # Assume time is in gmt ... got to local time instead
        dt += timedelta(hours=2)

        return cls(status_code, dt, content_type, content)

    def __str__(self):

        l = min(len(self.content), BLOB_STR_LENGTH)

        return "{{status_code:{}, date:\"{}\", content_type:\"{}\", content:\"{} ...\"}}".format(
            self.status_code,
            self.date,
            self.content_type,
            str(self.content[0:l])
        )

    def __repr__(self):
        return self.__str__()
