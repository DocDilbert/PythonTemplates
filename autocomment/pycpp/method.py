class MethodFactory(object):
    def __init__(self, attributes_factory):
        self.attributes_factory = attributes_factory

    def __call__(self, name_token, returns_token, pass_by, arguments_generator):
        method = Method(name_token, returns_token, pass_by,
                        self.attributes_factory(arguments_generator))
        return method


class Method(object):
    def __init__(self, name_token, returns_token, pass_by, arguments):
        self.name_token = name_token
        self.returns_token = returns_token
        self.pass_by = pass_by
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
