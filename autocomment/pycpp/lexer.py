# lexer.py
#
# A generic regex-based Lexer/tokenizer tool.
#

import re
from pycpp.code import Token, TokenNewLine

def token_factory(type_, val, pos):
    return Token(type_, val, pos)


def token_newline_factory(type_, val, pos):
    return TokenNewLine(pos)

CPP_RULES = [
    (r' +',              'WS', token_factory),
    (r'\t+',             'TAB', token_factory),
    (r'\n',              'NL', token_newline_factory),
    (r'\d+',             'NUMBER', token_factory),
    (r'\\',              'BACKSLASH', token_factory),
    (r'&',               'AND', token_factory),
    (r'\.',              'DOT', token_factory),
    (r'<',               'LESS', token_factory),
    (r'>',               'MORE', token_factory),
    (r':',               'DOUBLEPOINT', token_factory),
    (r';',               'EOC', token_factory),
    (r',',               'COMMA', token_factory),
    (r'!',               'NOT', token_factory),
    (r'[a-zA-Z_]\w*',    'STRING', token_factory),
    (r'#',               'HASH', token_factory),
    (r'\?',              'QUESTIONMARK', token_factory),
    (r'"',               'QUOTE', token_factory),
    (r'///',             'DOXYGENCOMMENT', token_factory),
    (r'//',              'COMMENT', token_factory),
    (r'/\*',             'COMMENT_BEGIN', token_factory),
    (r'\*/',             'COMMENT_END', token_factory),
    (r'{',               'BEGIN', token_factory),
    (r'}',               'END', token_factory),
    (r'\+',              'PLUS', token_factory),
    (r'\-',              'MINUS', token_factory),
    (r'\*',              'MULTIPLY', token_factory),
    (r'\/',              'DIVIDE', token_factory),
    (r'\(',              'LP', token_factory),
    (r'\)',              'RP', token_factory),
    (r'=',               'EQUALS', token_factory),
]


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
        self.factory = {}
        self.buf = None
        self.pos = 0
        for regex, type_, factory in CPP_RULES:
            groupname = 'GROUP%s' % idx
            regex_parts.append('(?P<%s>%s)' % (groupname, regex))
            self.group_type[groupname] = type_
            self.factory[groupname] = factory
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
                tok_factory = self.factory[groupname]
                tok = tok_factory(tok_type, m.group(groupname), self.pos)
                self.pos = m.end()
                return tok

            # if we're here, no rule matched
            raise LexerError(self.pos)

    def tokens(self):
        """ Returns an iterator to the tokens found in the buffer.
        """
        while 1:
            tok = self.token()
            if tok is None:
                break
            yield tok


if __name__ == '__main__':
    pass

    #lx = Lexer(rules, skip_whitespace=True)
    #lx.input('erw = _abc + 12*(R4-623902)  ')

    # try:
   #     for tok in lx.tokens():
   #         print(tok)
   # except LexerError as err:
   #     print('LexerError at position %s' % err.pos)
