""" A generic regex-based Lexer/tokenizer tool.
"""

import re
from pycpp.code import Token, TokenNewLine


def token_factory(type_, val, pos):
    """ Diese Fabrik Funktion erstellt ein Token
    """
    return Token(type_, val, pos)


def token_newline_factory(unused1, unused2, pos):
    """ Diese Fabrik Funktion erstellt ein TokenNewLine
    """
    del unused1
    del unused2

    return TokenNewLine(pos)


CPP_RULES = [
    (r' +', 'WS', token_factory),
    (r'\t+', 'TAB', token_factory),
    (r'\n', 'NL', token_newline_factory),
    (r'\d+', 'NUMBER', token_factory),
    (r'\\', 'BACKSLASH', token_factory),
    (r'&', 'AND', token_factory),
    (r'\.', 'DOT', token_factory),
    (r'<', 'LESS', token_factory),
    (r'>', 'MORE', token_factory),
    (r'::', '2COLONS', token_factory),
    (r':', 'COLON', token_factory),
    (r';', 'EOC', token_factory),
    (r',', 'COMMA', token_factory),
    (r'!', 'NOT', token_factory),
    (r'const', 'CONST', token_factory),
    (r'enum', 'ENUM', token_factory),
    (r'[a-zA-Z_ÜÄÖüöä]\w*', 'STRING', token_factory),
    (r'#', 'HASH', token_factory),
    (r'\?', 'QUESTIONMARK', token_factory),
    (r'"', 'QUOTE', token_factory),
    (r'///', 'DOXYGENCOMMENT', token_factory),
    (r'//', 'COMMENT', token_factory),
    (r'/\*', 'COMMENT_BEGIN', token_factory),
    (r'\*/', 'COMMENT_END', token_factory),
    (r'{', 'BEGIN', token_factory),
    (r'}', 'END', token_factory),
    (r'\+', 'PLUS', token_factory),
    (r'\-', 'MINUS', token_factory),
    (r'\*', 'MULTIPLY', token_factory),
    (r'\/', 'DIVIDE', token_factory),
    (r'\(', 'LP', token_factory),
    (r'\)', 'RP', token_factory),
    (r'\[', 'LSQB', token_factory),
    (r'\]', 'RSQB', token_factory),
    (r'=', 'EQUALS', token_factory),
    (r'\$', 'DOLLAR', token_factory),
    (r'\'', 'APOSTROPHE', token_factory),
    (r'\`', 'APOSTROPHE2', token_factory),
    (r'\|', 'LINE', token_factory),
    (r'\%', 'PERCENT', token_factory),
    (r'\^', 'CARET', token_factory),
    (r'\~', 'TILDE', token_factory),
]

class LexerError(Exception):
    """ Lexer error exception.

        pos:
            Position in the input line where the error occurred.
    """

    def __init__(self, pos):
        super().__init__(self)
        self.pos = pos


class Lexer(object):
    """ A simple regex-based lexer/tokenizer.
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
            match = self.regex.match(self.buf, self.pos)
            if match:
                groupname = match.lastgroup
                tok_type = self.group_type[groupname]
                tok_factory = self.factory[groupname]
                tok = tok_factory(tok_type, match.group(groupname), self.pos)
                self.pos = match.end()
                return tok

            print(self.buf[self.pos-12:self.pos+12])
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
