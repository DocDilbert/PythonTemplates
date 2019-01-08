from pycpp.code import Token
from pycpp.code import Block


class BlockCombine(object):
    def __init__(self, *, begin_token_type="BEGIN", end_token_type="END"):
        self.begin_token_type = begin_token_type
        self.end_token_type = end_token_type

    def tree(self, tokens):
        output = []
        for tok in tokens:

            if isinstance(tok, Block):
                if (tok.begin_del.type == self.begin_token_type and
                        tok.end_del.type == self.end_token_type):

                    # Verarbeite keine Blöcke die keinen Inhalt haben
                    if len(tok.content) > 0:
                        new_content = "".join([x.val for x in tok.content])
                        new_token = Token('STRING', new_content,
                                          tok.content[0].pos)
                        tok.content = [new_token]
                        
                    output.append(tok)
                    
                else:
                    temp = list(tok.content)
                    tok.content = self.tree(temp)
                    output.append(tok)
            else:
                output.append(tok)

        return output
