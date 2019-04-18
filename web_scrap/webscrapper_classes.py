from urllib.parse import urlparse, urlunparse

BLOB_STR_LENGTH = 10

class Session:
    def __init__(self):
        self.start_datetime = "not set"
        self.end_datetime = "not set"

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

class Request:
    def __init__(self, scheme, netloc, path, params, query, fragment):
        self.scheme = scheme 
        self.netloc = netloc
        self.path = path
        self.params = params
        self.query = query
        self.fragment = fragment

    @classmethod
    def from_url(cls, url):
        ( scheme, 
           netloc, 
           path, 
           params,
           query, 
           fragment
        ) = urlparse(url)
        return cls(scheme, netloc, path, params,query, fragment)

    def to_url(self):
        return urlunparse((
            self.scheme, 
            self.netloc, 
            self.path, 
            self.params, 
            self.query, 
            self.fragment
        ))

    def __str__(self): 
        return ("{{"
                "scheme={}, "
                "netloc={}, "
                "path={}, "
                "params={}, "
                "query={}, "
                "fragment={}"
            "}}").format(
                self.scheme, 
                self.netloc, 
                self.path, 
                self.params, 
                self.query, 
                self.fragment
            )

    def __repr__(self):
        return self.__str__()
   
class Response:
    def __init__(self, content_type):
        self.content_type=content_type
    
    def __str__(self): 
        return "{{content_type=\"{}\"}}".format(str(self.content_type))

    def __repr__(self):
        return self.__str__()

class ResponseContent:
    def __init__(self, content):
        self.content=content
    
    def __str__(self): 
        l = min(len(self.content),BLOB_STR_LENGTH)
        return "{{content=\"{}..\"}}".format(str(self.content[0:l]))

    def __repr__(self):
        return self.__str__()

