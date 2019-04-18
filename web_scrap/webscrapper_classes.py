
BLOB_STR_LENGTH = 10

class Response:
    def __init__(self, content_type):
        self.content_type=content_type
    
    def __str__(self): 
        return "{{content_type=\"{}\"}}".format(str(self.content_type))

    def __repr__(self):
        return "{{content_type=\"{}\"}}".format(str(self.content_type))
            
class ResponseContent:
    def __init__(self, content):
        self.content=content
    
    def __str__(self): 
        l = min(len(self.content),BLOB_STR_LENGTH)
        return "{{content=\"{}..\"}}".format(str(self.content[0:l]))

    def __repr__(self):
        l = min(len(self.content),BLOB_STR_LENGTH)
        return "{{content=\"{}..\"}}".format(str(self.content[0:l]))

