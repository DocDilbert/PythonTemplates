# token.py
#


class Token(object):
    """ A simple Token structure.
        Contains the token type, value and position.
    """
    def __init__(self, type, val, pos):
        self.type = type
        self.val = val
        self.pos = pos

    def __str__(self):
        return '%s(%s) at %s' % (self.type, self.val, self.pos)

    def __repr__(self):
        return '(%s(%s) at %s)' % (self.type, self.val, self.pos)

    def __eq__(self,other):
        
        if self.type != other.type:
            return False

        if self.val != other.val:
            return False

        if self.pos != other.pos:
            return False
        
        return True

    def __ne__(self,other):
        return not(self.__eq__(self,other))