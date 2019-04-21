class Response:
    def __init__(self, status_code, date, content_type):
        self.content_type=content_type
        self.status_code=status_code
        self.date = date
        
    def __str__(self): 
        return "{{status_code={}, date=\"{}\", content_type=\"{}\"}}".format(
            self.status_code, 
            self.date,
            self.content_type
        )

    def __repr__(self):
        return self.__str__()
