"""
Dieses Modul enthält die Klasse MethodSearch. Diese Klasse dient
den auffinden von Methoden Signaturen in einem Token String.
"""

import re

LNPAT = r'(\(\d+\))'
WS = '(%sWS_)?'% (LNPAT)
WS_NL_WS = '(%sWS_)?(%sNL_)?(%sWS_)?'% (LNPAT, LNPAT, LNPAT)

class MethodSearch:
    """Die Klasse MethodSearch sucht nach  C++ Methoden Signaturen in einem
       String der Form:

       (Pos1)Token1_(Pos2)Token2_(Pos3)Token3_
    """

    def __init__(self, method_factory):
        self.buf = ''
        self.method_factory = method_factory
        pat = ''
        pat += '(%sSTRING_%s2COLONS_)*' % (LNPAT, LNPAT)
        pat += '(?P<returns>%sSTRING_)' % (LNPAT)
        pat += WS_NL_WS
        pat += '(?P<pass_by>%sMULTIPLY_|%sAND_)?' % (LNPAT, LNPAT)
        pat += WS_NL_WS
        pat += '(%sSTRING_%s2COLONS_)?' % (LNPAT, LNPAT)
        pat += '(?P<name>%sSTRING_)' % (LNPAT)
        pat += WS_NL_WS
        pat += '(%sLP_)' % (LNPAT)
        pat += '(?P<arguments>'
        pat += '('
        pat +=      WS_NL_WS
        pat +=      '(%sCONST_|%sENUM_)?' % (LNPAT, LNPAT)
        pat +=      WS_NL_WS
        pat +=      '(%sSTRING_%s2COLONS_)*' % (LNPAT, LNPAT)
        pat +=      '(%sSTRING_)' % (LNPAT)
        pat +=      WS_NL_WS
        pat +=      '(%sMULTIPLY_|%sAND_)?' % (LNPAT, LNPAT)
        pat +=      WS_NL_WS
        pat +=      '(%sSTRING_)' % (LNPAT)
        pat +=      WS_NL_WS
        pat +=      '(%sEQUALS_)?' % (LNPAT)
        pat +=      WS_NL_WS
        pat +=      '(%sSTRING_|%sNUMBER_)?' % (LNPAT, LNPAT)
        pat +=      WS_NL_WS
        pat +=      '(%sCOMMA_)?' % (LNPAT)
        pat +=      WS_NL_WS
        pat += ')*'
        pat += ')'
        pat += '(%sRP_)' % (LNPAT)
        pat += WS_NL_WS
        pat += '(%sCONST_)?' % (LNPAT)
        pat += WS_NL_WS
        pat += '(%sEOC_|%sBEGIN_)' % (LNPAT, LNPAT)
        self.meth_regex = re.compile(pat)

        argpat = ''
        argpat += WS_NL_WS
        argpat += '(%sCONST_)?' % (LNPAT)
        argpat += WS_NL_WS
        argpat += '(%sSTRING_%s2COLONS_)*' % (LNPAT, LNPAT)
        argpat += '(?P<type>%sSTRING_)' % (LNPAT)
        argpat += WS_NL_WS
        argpat += '(?P<pass_by>%sMULTIPLY_|%sAND_)?' % (LNPAT, LNPAT)
        argpat += WS_NL_WS
        argpat += '(?P<name>%sSTRING_)' % (LNPAT)
        argpat += WS_NL_WS
        argpat += '(%sCOMMA_)?' % (LNPAT)
        argpat += WS_NL_WS
        self.arg_regex = re.compile(argpat)

    def __isolate_pos_from_string(self, buf):
        """Diese Methode gibt die in einem String angegebene Position
           zurück.

        Args:
            buf (string): String der Form "(Position)Token_"

        Returns:
            int: Position
        """

        elements = buf.split('(')
        elements = elements[1].split(')')
        return int(elements[0])


    def __getTokenPos(self, match, groupname):
        """Diese Methode isoliert die Position in einem RegEx Gruppen Match.

        Args:
            match: Gefundene Übereinstimmung
            groupname (string): Name der Gruppe deren Position isoliert werden soll

        Returns:
            int: Isolierte Position
        """

        token_pos = self.__isolate_pos_from_string(match.group(groupname))
        return token_pos

    def __isolate_arguments(self, argstr):
        """Diese Methode dient dem separaten suchen von Methoden Argumenten und 
           der Extraktion deren Position

        Args:
            argstr ([string]): String der die Methoden Tokens der Argumente enthält
        """

        pos = 0
        for argmatch in self.arg_regex.finditer(argstr, pos):
            pos = argmatch.end()

            pass_by = -1
            if argmatch.group('pass_by'):
                pass_by = self.__getTokenPos(argmatch, 'pass_by')

            yield (
                self.__getTokenPos(argmatch, 'name'),
                self.__getTokenPos(argmatch, 'type'),
                pass_by
            )

    def search(self, buf):
        """Suche in einem Token String der Form
         
            "(Pos1)Token1_(Pos2)Token2_(Pos3)Token3_"

           nach einer C++ Methodendefinition.

        Args:
            buf ([string]): Token Steing

        Returns:
            Ein Iterator der die Positionen der gefundenen Methoden enthält.
        """

        pos = 0
        self.buf = buf

        for match in self.meth_regex.finditer(self.buf, pos):
            pos = match.end()

            pass_by = -1
            if match.group('pass_by'):
                pass_by = self.__getTokenPos(match, 'pass_by')

            yield self.method_factory(
                self.__getTokenPos(match, 'name'),
                self.__getTokenPos(match, 'returns'),
                pass_by,
                self.__isolate_arguments(match.group('arguments'))
            )
