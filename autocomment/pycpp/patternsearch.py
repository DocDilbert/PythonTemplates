import re
from pycpp.code import Block
from pycpp.serializer import Serializer
from pycpp.serializer import getTokenSummary

LNPAT = r'(\(\d+\))'
class PatternSearch:
    def __init__(self):
        self.pos = 0
        self.buf = ''
        self.regex = None
        self.tokens = None
    def search_pattern(self):
        if self.pos >= len(self.buf):
            return None
        else:
            m = self.regex.search(self.buf, self.pos)
            if m:
                print(m)
                self.pos = m.end()
                return m

            return None

    def isolate_pos(self, str_):
        elements = str_.split('(')
        elements = elements[1].split(')')
        return(int(elements[0]))

    def search_token_at_pos(self, pos, tokens):
        for tok in tokens:
            if isinstance(tok, Block):
                return self.search_token_at_pos(pos, tok.content)
            else:
                if tok.pos == pos:
                    return tok

    def getToken(self, match, groupname):
        token_pos = self.isolate_pos(match.group(groupname))
        token = self.search_token_at_pos(token_pos, self.tokens)
        return token

    def search(self, tokens):
        serializer = Serializer()
        self.tokens = tokens
        self.buf = serializer.toString(tokens, getTokenSummary)
        
        pattern = ''
        pattern += '(?P<returns>%sSTRING_)' % (LNPAT)
        pattern += '(%sWS_)' % (LNPAT)
        pattern += '(?P<name>%sSTRING_)' % (LNPAT)
        pattern += '(%sLP_)' % (LNPAT)
        pattern += '(%sRP_)' % (LNPAT)
        pattern += '(%sEOC_)' % (LNPAT)
        self.regex = re.compile(pattern)
        self.pos = 0

        while 1:
            match = self.search_pattern()
            if match is None:
                break
            else:
                match_parsed = {
                    'returns' : self.getToken(match, 'returns'),
                    'name' : self.getToken(match, 'name'),
                }
                yield(match_parsed)

