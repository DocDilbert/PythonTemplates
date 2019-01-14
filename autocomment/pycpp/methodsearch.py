import re
from pycpp.code import Block

LNPAT = r'(\(\d+\))'


class MethodSearch:
    def __init__(self, method_factory):
        self.buf = ''
        self.method_factory = method_factory

        pat = ''
        pat += '(%sSTRING_%s2COLONS_)*' % (LNPAT, LNPAT)
        pat += '(?P<returns>%sSTRING_)' % (LNPAT)
        pat += '(%sWS_)?' % (LNPAT)
        pat += '(?P<pass_by>%sMULTIPLY_|%sAND_)?' % (LNPAT, LNPAT)
        pat += '(%sWS_)?' % (LNPAT)
        pat += '(%sSTRING_%s2COLONS_)?' % (LNPAT,LNPAT)
        pat += '(?P<name>%sSTRING_)' % (LNPAT)
        pat += '(%sWS_)?' % (LNPAT)
        pat += '(%sLP_)' % (LNPAT)
        pat += '(?P<arguments>'
        pat += '('
        pat += '(%sWS_)?' % (LNPAT)
        pat += '(%sNL_)?' % (LNPAT)
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
        pat += '(%sEQUALS_)?' % (LNPAT)
        pat += '(%sWS_)?' % (LNPAT)
        pat += '(%sNL_)?' % (LNPAT)
        pat += '(%sWS_)?' % (LNPAT)
        pat += '(%sSTRING_)?' % (LNPAT)
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
        pat += '(%sNL_)?' % (LNPAT)
        pat += '(%sWS_)?' % (LNPAT)
        pat += '(%sEOC_|%sBEGIN_)' % (LNPAT, LNPAT)
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


    def __getTokenPos(self, match, groupname):
        token_pos = self.__isolate_pos_from_string(match.group(groupname))
        return token_pos

    def __isolate_arguments(self, argstr):
        pos = 0
        for argmatch in self.arg_regex.finditer(argstr, pos):
            pos = argmatch.end()

            pass_by = -1
            if argmatch.group('pass_by'):
                pass_by = self.__getTokenPos(argmatch, 'pass_by')

            arg_parsed = (
                self.__getTokenPos(argmatch, 'name'),
                self.__getTokenPos(argmatch, 'type'),
                pass_by
            )
            yield arg_parsed

    def search(self, buf):
        pos = 0
        self.buf = buf

        for match in self.meth_regex.finditer(self.buf, pos):
            pos = match.end()

            pass_by = -1
            if match.group('pass_by'):
                pass_by = self.__getTokenPos(match, 'pass_by')

            yield self.method_factory(self.__getTokenPos(match, 'name'),
                                      self.__getTokenPos(match, 'returns'),
                                      pass_by,
                                      self.__isolate_arguments(match.group('arguments')))
