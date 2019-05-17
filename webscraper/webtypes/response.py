from datetime import datetime, timedelta
import bz2
BLOB_STR_LENGTH = 10
COMPRESSION_LEVEL = 9

class Response:
    def __init__(self, status_code, date, content_type, *, content=None, bz2Content=None):

        self.content_type = content_type
        self.status_code = status_code
        self.date = date
        self.must_decompress = False
        self.must_compress = False
        if content is not None and bz2Content is None:
            self.content = content

        elif content is None and bz2Content is not None:
            self.bz2Content = bz2Content
            
        else:
            raise Exception("No content was given to create Response object")
        

    @classmethod
    def fromGMT(cls, status_code, date_gmt, content_type, *, content=None, bz2Content=None):
        dt = datetime.strptime(date_gmt, "%a, %d %b %Y %H:%M:%S %Z")

        # Assume time is in gmt ... got to local time instead
        dt += timedelta(hours=2)

        return cls(status_code, dt, content_type, content = content, bz2Content = bz2Content)

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

    def getContent(self):
        if self.must_decompress:
            return bz2.decompress(self.__bz2Content)
        else:
            return self.__content

    def setContent(self, x):
        self.must_compress = True
        self.must_decompress = False
        self.__content = x

    content = property(getContent, setContent)

    def getBz2Content(self):
        if self.must_compress:
            return bz2.compress(self.__content, COMPRESSION_LEVEL)
        else:
            return self.__bz2Content

    def setBz2Content(self, x):
        #self.__content = bz2.decompress(x)
        self.__bz2Content = x
        self.must_decompress = True
        self.must_compress = False

    bz2Content = property(getBz2Content, setBz2Content)
