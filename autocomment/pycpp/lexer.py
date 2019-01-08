# lexer.py
#
# A generic regex-based Lexer/tokenizer tool.
#

import re
import sys
from pycpp.code import Token, TokenNewLine

def token_factory(type_, val, pos):
    return Token(type_, val, pos)

def token_newline_factory(type_, val, pos):
    return TokenNewLine(pos)

CPP_RULES = [
    (r' +',              'WHITESPACE', token_factory),
    (r'\t+',             'TAB', token_factory),
    (r'\n+',             'NEWLINE', token_newline_factory),
    (r'\d+',             'NUMBER', token_factory),
    (r'\\',              'BACKSLASH', token_factory),
    (r'&',               'AND', token_factory),
    (r'\.',              'DOT', token_factory),
    (r'<',               'LESS', token_factory),
    (r'>',               'MORE', token_factory),
    (r':',               'DOUBLEPOINT', token_factory),
    (r';',               'ENDOFCOMMAND', token_factory),
    (r',',               'COMMA', token_factory),
    (r'!',               'NOT', token_factory),
    (r'[a-zA-Z_]\w*',    'STRING', token_factory),
    (r'#',               'HASH', token_factory),
    (r'\?',              'QUESTIONMARK', token_factory),
    (r'"',               'ASTERISK', token_factory),
    (r'///',             'DOXYGENCOMMENT', token_factory),
    (r'//',              'COMMENT', token_factory),
    (r'/\*',             'COMMENT_BEGIN', token_factory),
    (r'\*/',             'COMMENT_END', token_factory),
    (r'{',               'CB_BEGIN', token_factory),  # CB ist die Kurzform von Code Block
    (r'}',               'CB_END', token_factory),   # CB ist die Kurzform von Code Block
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
        self.buf = None
        self.pos = 0
        for regex, type_, factory in CPP_RULES:
            groupname = 'GROUP%s' % idx
            regex_parts.append('(?P<%s>%s)' % (groupname, regex))
            self.group_type[groupname] = type_
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
            print(self.buf[self.pos-5:self.pos+5])
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
