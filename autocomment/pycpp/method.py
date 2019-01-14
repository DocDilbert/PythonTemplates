from pycpp.code import Block


class MethodFactory(object):
    def __init__(self, tokens, attributes_factory, returns_description_lookup=None):
        self.tokens = tokens
        self.attributes_factory = attributes_factory
        self.returns_description_lookup = returns_description_lookup

    def __search_for_token_at_pos(self, pos, tokens):
        for tok in tokens:
            if isinstance(tok, Block):
                found_token = self.__search_for_token_at_pos(pos, tok.content)
                if found_token:
                    return found_token
            else:
                if tok.pos == pos:
                    return tok

        return None

    def __call__(self, name_pos, returns_pos, pass_by_pos, arguments_generator):

        method = Method(
            self.__search_for_token_at_pos(name_pos, self.tokens),
            self.__search_for_token_at_pos(returns_pos, self.tokens),
            self.__search_for_token_at_pos(pass_by_pos, self.tokens),
            self.attributes_factory(arguments_generator)
        )

        if self.returns_description_lookup:
            method.return_description = self.returns_description_lookup(
                method.returns)

        return method


class Method(object):
    def __init__(self, name_token, returns_token, pass_by_token, arguments):
        self.name_token = name_token
        self.returns_token = returns_token
        self.pass_by_token = pass_by_token
        self.arguments = arguments
        self.return_description = None

    @property
    def name(self):
        return self.name_token.val

    @property
    def returns(self):
        return self.returns_token.val

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        buf = "/// %s" % (self.name)
        if len(self.arguments) > 0:
            buf += '\n'
            buf += str(self.arguments)

        if self.returns != "void":
            buf += '\n'
            buf += '/// \\return'
            if self.return_description:
                buf += ' %s' % (self.return_description)

        return buf
