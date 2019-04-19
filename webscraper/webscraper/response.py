class Response:
    def __init__(self, status_code, content_type):
        self.content_type=content_type
        self.status_code=status_code
        
    def __str__(self): 
        return "{{status_code={}, content_type=\"{}\"}}".format(self.status_code, self.content_type)

    def __repr__(self):
        return self.__str__()
