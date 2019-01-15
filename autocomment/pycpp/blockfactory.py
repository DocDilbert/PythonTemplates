""" Dieses Modul enthält die Klasse BlockFactory. Diese
Klasse sucht in einer Liste von Tokens Blöcke in dem sie
nach einem start und end Token sucht.
"""

from pycpp.code import Block


class BlockFactory(object):
    """ Diese Klasse sucht in einer Liste von Tokens
        Blöcke in dem sie nach einem start und end Token sucht.
    """
    def __init__(
            self, *,
            begin_del_type="BEGIN",
            end_del_type="END",
            trail_start=">",
            trail_advance="--"
    ):
        self.trail_start = trail_start
        self.trail_advance = trail_advance
        self.tokens = []
        self.begin_del_type = begin_del_type
        self.end_del_type = end_del_type

    def tree(self, tokens):
        """ Die eigentliche Methode die nach start und end Blöcken sucht

            Returns:
                Eine neue Liste die die gefundenen Blöcke enthält
        """
        output = Block()
        actual = output
        closure_tree = []

        for token in tokens:
            if isinstance(token, Block):
                output.add(
                    Block(
                        token.begin_del,
                        token.end_del,
                        self.tree(token.content),
                        trail_start=token.trail_start,
                        trail_advance=token.trail_advance
                        )
                    )
            else:
                if token.type == self.begin_del_type:
                    temp = Block(
                        trail_start=self.trail_start,
                        trail_advance=self.trail_advance
                    )
                    temp.begin_del = token
                    closure_tree.append(actual)
                    actual.add(temp)
                    actual = temp

                # do not use end tokens which have no corresponding begin token
                elif token.type == self.end_del_type and len(closure_tree) > 0:
                    actual.end_del = token
                    actual = closure_tree.pop()
                else:
                    actual.add(token)

        return output.content
