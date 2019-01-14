""" Dieses Modul enthält die Klasse Serializer.
Diese Klasse dient der Anwendung einer Funktion auf eine Liste von
Tokens und Blöcken.

"""

from pycpp.code import Block

def getTokenValue(tok):
    """ Diese Funktion gibt das Argument val des Eingangswertes zurück.

    Args:
        tok ([Token]): Das Token welches abgefragt werden soll

    Returns:
        [String]: .val Argument des Token
    """
    return tok.val


def getTokenType(tok):
    """ Diese Funktion gibt das Argument type des Eingangswertes zurück.

    Args:
        tok ([Token]): Das Token welches abgefragt werden soll

    Returns:
        [String]: .type Argument des Token
    """
    return tok.type


def getTokenSummary(tok):
    """ Diese Funktion gibt einen formatieren String der Art:

        "(pos)TokenType_"

        zurück. Diese Art String wird von der Klasse MethodSearch
        vorrausgesetzt.

    Args:
        tok ([Token]): Das Token welches abgefragt werden soll

    Returns:
        [String]: String der Form "(pos)TokenType_"

    """
    return '('+str(tok.pos)+')' + tok.type + '_'


class Serializer:
    """ Die Aufgabe dieser Klasse ist eine Liste von Tokens und Blöcken
    zu einem String zusammenzufassen
    """
    def __init__(self):
        pass

    def toString(self, tokens, func_getTokenString=getTokenValue):
        """Wende auf die Token Liste tokens die Funktion func_getTokenString an
           und füge die von dieser Funktion zurückgegebenen String zu einem zusammen.

        Args:
            tokens: Liste von Tokens
            func_getTokenString: Funktion die angewendet werden soll. Defaults to getTokenValue.

        Returns:
            [String]: Aneinandergereihter String
        """

        output = ''
        for tok in tokens:
            if isinstance(tok, Block):
                output += func_getTokenString(tok.begin_del)
                output += self.toString(tok.content, func_getTokenString)
                output += func_getTokenString(tok.end_del)
            else:
                output += func_getTokenString(tok)

        return output
