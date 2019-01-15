""" Dieses Modul enthält die Klasse BlockCombine.
"""
from pycpp.code import Token
from pycpp.code import Block

class BlockCombine(object):
    """ Die Klasse BlockBine dient dem zusammenfassen
        des Inhaltes eines Blockes zu einem einzelnen STRING Token.
    """
    def __init__(self, *, subs_type='STRING', begin_token_type="BEGIN", end_token_type="END"):
        self.begin_token_type = begin_token_type
        self.end_token_type = end_token_type
        self.subs_type = subs_type

    def tree(self, tokens):
        """ Diese Method sucht in der Liste tokens nach den angegebenen Blöcken und
            fasst deren Inhalt zu einem STRING Token zusammen
        """
        output = []
        for tok in tokens:

            if isinstance(tok, Block):
                if (tok.begin_del.type == self.begin_token_type and
                        tok.end_del.type == self.end_token_type):

                    # Verarbeite keine Blöcke die keinen Inhalt haben
                    if len(tok.content) > 0:
                        new_content = "".join([x.val for x in tok.content])
                        new_token = Token(
                            self.subs_type, new_content,
                            tok.content[0].pos
                        )
                        tok.content = [new_token]

                    output.append(tok)

                else:
                    temp = list(tok.content)
                    tok.content = self.tree(temp)
                    output.append(tok)
            else:
                output.append(tok)

        return output
