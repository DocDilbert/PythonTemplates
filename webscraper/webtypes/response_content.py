import bz2

BLOB_STR_LENGTH = 10
COMPRESSION_LEVEL = 9 
class ResponseContent:
    def __init__(self, content):
        self.content=content
    
    def __str__(self): 
        l = min(len(self.content),BLOB_STR_LENGTH)
        return "{{content=\"{} ...\"}}".format(str(self.content[0:l]))

    def __repr__(self):
        return self.__str__()

    def compress(self):
        return bz2.compress(self.content,COMPRESSION_LEVEL)

    @classmethod 
    def from_decompress(cls, content):
        return cls(bz2.decompress(content)) 
