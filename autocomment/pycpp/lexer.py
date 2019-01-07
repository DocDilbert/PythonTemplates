#-------------------------------------------------------------------------------
# lexer.py
#
# A generic regex-based Lexer/tokenizer tool.
# See the if __main__ section in the bottom for an example.
#
# Eli Bendersky (eliben@gmail.com)
# This code is in the public domain
# Last modified: August 2010
#-------------------------------------------------------------------------------
import re
import sys


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


class LexerError(Exception):
    """ Lexer error exception.

        pos:
            Position in the input line where the error occurred.
    """
    def __init__(self, pos):
        self.pos = pos


class Lexer(object):
    """ A simple regex-based lexer/tokenizer.

        See below for an example of usage.
    """

    rules = [
        (r'\s+',             'WHITESPACE'),   
        (r'\d+',             'NUMBER'),
        (r'[a-zA-Z_]\w+',    'STRING'),
        (r'//',              'COMMENT'),
        (r'/\*',             'COMMENT_BEGIN'),
        (r'\*/',             'COMMENT_END'),
        (r'{',               'CB_BEGIN'), # CB ist die Kurzform von Code Block
        (r'}',               'CB_END'),   # CB ist die Kurzform von Code Block
        (r'\+',              'PLUS'),
        (r'\-',              'MINUS'),
        (r'\*',              'MULTIPLY'),
        (r'\/',              'DIVIDE'),
        (r'\(',              'LP'),
        (r'\)',              'RP'),
        (r'=',               'EQUALS'),
    ]

    def __init__(self):
        """ Create a lexer.
        """
        # All the regexes are concatenated into a single one
        # with named groups. Since the group names must be valid
        # Python identifiers, but the token types used by the
        # user are arbitrary strings, we auto-generate the group
        # names and map them to token types.
        #
        idx = 1
        regex_parts = []
        self.group_type = {}

        for regex, type in self.rules:
            groupname = 'GROUP%s' % idx
            regex_parts.append('(?P<%s>%s)' % (groupname, regex))
            self.group_type[groupname] = type
            idx += 1

        self.regex = re.compile('|'.join(regex_parts))

    def input(self, buf):
        """ Initialize the lexer with a buffer as input.
        """
        self.buf = buf
        self.pos = 0

    def token(self):
        """ Return the next token (a Token object) found in the
            input buffer. None is returned if the end of the
            buffer was reached.
            In case of a lexing error (the current chunk of the
            buffer matches no rule), a LexerError is raised with
            the position of the error.
        """
        if self.pos >= len(self.buf):
            return None
        else:
            m = self.regex.match(self.buf, self.pos)
            if m:
                groupname = m.lastgroup
                tok_type = self.group_type[groupname]
                tok = Token(tok_type, m.group(groupname), self.pos)
                self.pos = m.end()
                return tok

            # if we're here, no rule matched
            raise LexerError(self.pos)

    def tokens(self):
        """ Returns an iterator to the tokens found in the buffer.
        """
        while 1:
            tok = self.token()
            if tok is None: break
            yield tok


if __name__ == '__main__':
    pass

    #lx = Lexer(rules, skip_whitespace=True)
    #lx.input('erw = _abc + 12*(R4-623902)  ')

    #try:
   #     for tok in lx.tokens():
   #         print(tok)
   # except LexerError as err:
   #     print('LexerError at position %s' % err.pos)

