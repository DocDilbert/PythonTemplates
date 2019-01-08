# code.py
#


class Code(object):
    pass


class Closure(Code):
    def __init__(self, begin_del=None, end_del=None, content=None):
        self.begin_del = begin_del
        self.end_del = end_del
        if content is not None:
            self.content = list(content)
        else:
            self.content = list()

    def add(self, token):
        self.content.append(token)

    def serialize(self):
        output = []
        for t in self.content:
            if isinstance(t, Closure):
                output += t.serialize_closure()
            else:
                output.append(t)
        return output

    def print_closure(self, trailing):
        trailing = "--" + trailing
        output = ""
        for t in self.content:
            if isinstance(t, Closure):
                output += t.print_closure(trailing)
                output += "\n"
            else:
                output += trailing + str(t)
                output += "\n"
        return output

    def __str__(self):
        trailing = ">"
        return self.print_closure(trailing)

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        if len(self.content) != len(other.content):
            return False
        if self.begin_del != other.begin_del:
            return False
        if self.end_del != other.end_del:
            return False
        for self_element, other_element in zip(self.content, other.content):
            if self_element != other_element:
                return False

        return True

    def __ne__(self, other):
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

    def __eq__(self, other):

        if self.type != other.type:
            return False

        if self.val != other.val:
            return False

        if self.pos != other.pos:
            return False

        return True

    def __ne__(self, other):
        return not(self.__eq__(other))


class TokenNewLine(Token):
    def __init__(self, pos):
        super().__init__("NEWLINE", "\n", pos)

    def __str__(self):
        return '%s(\\n) at %s' % (self.type, self.pos)

    def __repr__(self):
        return '(%s(\\n) at %s)' % (self.type, self.pos)   

    def __eq__(self, other):
        if isinstance(other, TokenNewLine):
            return super().__eq__(other)
        else:
            return False