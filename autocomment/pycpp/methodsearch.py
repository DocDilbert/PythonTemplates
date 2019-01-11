import re
from pycpp.code import Block
from pycpp.serializer import Serializer
from pycpp.serializer import getTokenSummary

LNPAT = r'(\(\d+\))'


class MethodSearch:
    def __init__(self):
        self.buf = ''
        self.tokens = None

        pat = ''
        pat += '(%sSTRING_%s2COLONS_)*' % (LNPAT, LNPAT)
        pat += '(?P<returns>%sSTRING_)' % (LNPAT)
        pat += '(%sWS_)?' % (LNPAT)
        pat += '(?P<pass_by>%sMULTIPLY_|%sAND_)?' % (LNPAT, LNPAT)
        pat += '(%sWS_)?' % (LNPAT)
        pat += '(?P<name>%sSTRING_)' % (LNPAT)
        pat += '(%sLP_)' % (LNPAT)
        pat += '(?P<arguments>'
        pat += '('
        pat += '(%sWS_)?' % (LNPAT)
        pat += '(%sCONST_)?' % (LNPAT)
        pat += '(%sWS_)?' % (LNPAT)
        pat += '(%sSTRING_%s2COLONS_)*' % (LNPAT, LNPAT)
        pat += '(%sSTRING_)' % (LNPAT)
        pat += '(%sWS_)?' % (LNPAT)
        pat += '(%sMULTIPLY_|%sAND_)?' % (LNPAT, LNPAT)
        pat += '(%sWS_)?' % (LNPAT)
        pat += '(%sSTRING_)' % (LNPAT)
        pat += '(%sWS_)?' % (LNPAT)
        pat += '(%sNL_)?' % (LNPAT)
        pat += '(%sWS_)?' % (LNPAT)
        pat += '(%sCOMMA_)?' % (LNPAT)
        pat += '(%sWS_)?' % (LNPAT)
        pat += '(%sNL_)?' % (LNPAT)
        pat += '(%sWS_)?' % (LNPAT)
        pat += ')*'
        pat += ')'
        pat += '(%sRP_)' % (LNPAT)
        pat += '(%sWS_)?' % (LNPAT)
        pat += '(%sCONST_)?' % (LNPAT)
        pat += '(%sWS_)?' % (LNPAT)
        pat += '(%sEOC_)' % (LNPAT)
        self.meth_regex = re.compile(pat)

        argpat = ''
        argpat += '(%sWS_)?' % (LNPAT)
        argpat += '(%sCONST_)?' % (LNPAT)
        argpat += '(%sWS_)?' % (LNPAT)
        argpat += '(%sSTRING_%s2COLONS_)*' % (LNPAT, LNPAT)
        argpat += '(?P<type>%sSTRING_)' % (LNPAT)
        argpat += '(%sWS_)?' % (LNPAT)
        argpat += '(?P<pass_by>%sMULTIPLY_|%sAND_)?' % (LNPAT, LNPAT)
        argpat += '(%sWS_)?' % (LNPAT)
        argpat += '(?P<name>%sSTRING_)' % (LNPAT)
        argpat += '(%sWS_)?' % (LNPAT)
        argpat += '(%sNL_)?' % (LNPAT)
        argpat += '(%sWS_)?' % (LNPAT)
        argpat += '(%sCOMMA_)?' % (LNPAT)
        argpat += '(%sWS_)?' % (LNPAT)
        argpat += '(%sNL_)?' % (LNPAT)
        argpat += '(%sWS_)?' % (LNPAT)
        self.arg_regex = re.compile(argpat)

    def __isolate_pos_from_string(self, str_):
        elements = str_.split('(')
        elements = elements[1].split(')')
        return int(elements[0])

    def __search_for_token_at_pos(self, pos, tokens):
        for tok in tokens:
            if isinstance(tok, Block):
                found_token = self.__search_for_token_at_pos(pos, tok.content)
                if found_token:
                    return found_token
            else:
                if tok.pos == pos:
                    return tok

    def __getToken(self, match, groupname):
        token_pos = self.__isolate_pos_from_string(match.group(groupname))
        token = self.__search_for_token_at_pos(token_pos, self.tokens)
        return token

    def __isolate_arguments(self, argstr):
        pos = 0
        for argmatch in self.arg_regex.finditer(argstr, pos):
            pos = argmatch.end()

            pass_by = ''
            if argmatch.group('pass_by'):
                pass_by = self.__getToken(argmatch, 'pass_by')

                if pass_by.val == '*':
                    pass_by = 'pointer'
                elif pass_by.val == '&':
                    pass_by = 'reference'
            else:
                pass_by = 'value'

            arg_parsed = {
                'name': self.__getToken(argmatch, 'name'),
                'type': self.__getToken(argmatch, 'type'),
                'pass_by': pass_by,
            }
            yield arg_parsed

    def search(self, tokens):
        serializer = Serializer()

        self.tokens = tokens
        self.buf = serializer.toString(tokens, getTokenSummary)

        pos = 0

        for match in self.meth_regex.finditer(self.buf, pos):
            pos = match.end()
            
            pass_by = ''
            if match.group('pass_by'):
                pass_by = self.__getToken(match, 'pass_by')

                if pass_by.val == '*':
                    pass_by = 'pointer'
                elif pass_by.val == '&':
                    pass_by = 'reference'
            else:
                pass_by = 'value'

            match_parsed = {
                'returns': self.__getToken(match, 'returns'),
                'name': self.__getToken(match, 'name'),
                'args': list(self.__isolate_arguments(match.group('arguments'))),
                'pass_by': pass_by
            }
            yield match_parsed
