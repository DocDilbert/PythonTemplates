""" Dieses Modul enthält die Klassen Block, Token und TokenNewLine
"""

class Block(object):
    """ Ein Block enthält mehrere Tokens oder weitere Blöcke.
    """

    def __init__(self,
                 begin_del=None,
                 end_del=None,
                 content=None,
                 *,
                 trail_start=">",
                 trail_advance="--"):
        self.trail_start = trail_start
        self.trail_advance = trail_advance
        self.begin_del = begin_del
        self.end_del = end_del
        if content is not None:
            self.content = list(content)
        else:
            self.content = list()

    def add(self, token):
        """ Füge ein Token oder einen Block diesem Block hinzu
        """
        self.content.append(token)

    def block_to_string(self, trailing, init_insert_trail=True):
        """ Geht die hierachie eines Blockes durch und generiert
            einen String.
        """
        trailing = self.trail_advance + trailing
        output = ""
        insert_trail = init_insert_trail
        for tok in self.content:
            if isinstance(tok, Block):
                output += tok.block_to_string(trailing, False)
            else:
                if insert_trail:
                    output += trailing
                    insert_trail = False

                output += str(tok)
                if isinstance(tok, TokenNewLine):
                    output += "\n"
                    insert_trail = True

        if isinstance(self.end_del, TokenNewLine):
            output += "\n"
            output += trailing

        return output

    def __str__(self):
        trailing = self.trail_start
        return self.block_to_string(trailing)

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
        return not self.__eq__(other)


class Token(object):
    """ A simple Token structure.
        Contains the token type, value and position.
    """

    def __init__(self, type_, val, pos):
        self.type = type_
        self.val = val
        self.pos = pos

    def __str__(self):
        return '%s("%s"#%s)' % (self.type, self.val, self.pos)

    def __repr__(self):
        return '(%s("%s"#%s)' % (self.type, self.val, self.pos)

    def __eq__(self, other):

        if self.type != other.type:
            return False

        if self.val != other.val:
            return False

        if self.pos != other.pos:
            return False

        return True

    def __ne__(self, other):
        return not self.__eq__(other)


class TokenNewLine(Token):
    """ Equivalent zur Token Klasse. Allerdings wird der Newline
        Charakter bei __str__ sowie __repr__ unterdrückt.
    """
    def __init__(self, pos):
        super().__init__("NL", "\n", pos)
        self.testdata = 1

    def __str__(self):
        return '%s("\\n"#%s)' % (self.type, self.pos)

    def __repr__(self):
        return '(%s("\\n"#%s)' % (self.type, self.pos)

    def __eq__(self, other):
        if isinstance(other, TokenNewLine):
            return super().__eq__(other)
        else:
            return False
