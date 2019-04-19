from urllib.parse import urlparse, urlunparse

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
   