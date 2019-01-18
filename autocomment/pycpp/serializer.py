""" Dieses Modul enthält die Klasse :class:`~.Serializer`.
Diese Klasse dient der Anwendung einer Funktion auf eine Liste von
Tokens und Blöcken.

"""

from pycpp.code import Block

def get_token_value(tok):
    """ Diese Funktion gibt das Attribut val des gegebenen Tokens zurück.

    Args:
        tok ([Token]): Das Token welches abgefragt werden soll

    Returns:
        [String]: .val Argument des Token
    """
    return tok.val


def get_token_type(tok):
    """ Diese Funktion gibt das Attribut type des gegeben Tokens zurück.

    Args:
        tok ([Token]): Das Token welches abgefragt werden soll

    Returns:
        [String]: .type Argument des Token
    """
    return tok.type


def get_token_summary(tok):
    """ Diese Funktion gibt für ein Token einen formatieren String aus.:
    
    Der ausgebene String hat folgende Form:
    :: 
    
    (pos)TokenType_

    Diese Art String wird von der Klasse :class:`~MethodSearch`
    vorrausgesetzt.

    Args:
        tok ([Token]): Das Token welches abgefragt werden soll

    Returns:
        [String]: String der Form "(pos)TokenType_"

    """
    return '('+str(tok.pos)+')' + tok.type + '_'


class Serializer:
    """ Die Aufgabe dieser Klasse ist eine Liste von Tokens und Blöcken
    zu einem String zusammenzufassen. Welcher Teilstring für ein Token
    verwendet wird, kann vorgegeben werden.
    """

    def __init__(self):
        pass

    def to_string(self, tokens, func_get_token_string=get_token_value):
        """Wende auf die Token Liste tokens die Funktion func_get_token_string an
        und füge die von dieser Funktion zurückgegebenen String zu einem zusammen.

        Args:
            tokens: Liste von Tokens
            func_get_token_string: Funktion die angewendet werden soll. Defaults to getTokenValue.

        Returns:
            [String]: Aneinandergereihter String
        """

        output = ''
        for tok in tokens:
            if isinstance(tok, Block):
                output += func_get_token_string(tok.begin_del)
                output += self.to_string(tok.content, func_get_token_string)
                output += func_get_token_string(tok.end_del)
            else:
                output += func_get_token_string(tok)

        return output
