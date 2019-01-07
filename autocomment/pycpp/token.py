# token.py
#

class Code(object):
    def __eq__(self,other):
        return False

    def __neq__(self, other):
        return True

class Closure(Code):

    def __init__(self, content = None):
        if content is not None:
            self.content = list(content)
        else:
            self.content = list()

    def add(self, token):
        self.content.append(token)

    def print_closure(self, trailing):
        trailing = "--" + trailing
        output = ""
        for t in self.content:
            if isinstance(t, Closure):
                output += t.print_closure(trailing)
                output += "\n"
            else:
                output += trailing  + str(t)
                output += "\n"
        return output

    def __str__(self):
        trailing = ">"
        return self.print_closure(trailing)

    def __repr__(self):
        return self.__str__()
    def __eq__(self,other):
        if len(self.content)!= len(other.content):
            return False

        for self_element, other_element in zip(self.content, other.content):
            if self_element != other_element:
                return False
        
        return True

    def __ne__(self,other):
        return not(self.__eq__(other))

class Token(Code):
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
        return not(self.__eq__(other))