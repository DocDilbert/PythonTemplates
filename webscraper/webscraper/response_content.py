BLOB_STR_LENGTH = 10

class ResponseContent:
    def __init__(self, content):
        self.content=content
    
    def __str__(self): 
        l = min(len(self.content),BLOB_STR_LENGTH)
        return "{{content=\"{} ...\"}}".format(str(self.content[0:l]))

    def __repr__(self):
        return self.__str__()
