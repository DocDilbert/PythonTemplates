def arguments_factory(generator):
    args = Arguments()
    [args.add(name_token, type_token, pass_by) for (name_token, type_token, pass_by) in generator]
    return args


class Argument(object):
    def __init__(self, name_token, type_token, pass_by):
        self.name_token = name_token
        self.type_token = type_token
        self.pass_by = pass_by
        self.description = None

    def __eq__(self, other):
        if self.name_token != other.name_token:
            return False

        if self.type_token != other.type_token:
            return False

        if self.pass_by != other.pass_by:
            return False

        return True

    @property
    def name(self):
        return self.name_token.val

    @property
    def type(self):
        return self.type_token.val

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):    
        buf = []
        buf.append(self.name)
        if self.description:
            buf.append(self.description)
        return '/// \\param %s' % (" ".join(buf))

class Arguments(object):

    def __init__(self):
        self.arglist = []

    def add(self, name, type_, pass_by):
        self.arglist.append(Argument(name, type_, pass_by))

    def __len__(self):
        return len(self.arglist)

    def __iter__(self):
        return iter(self.arglist)

    def generate_comment(self, argument_lookup = None):
        for argument in self:
            return '/// \\param %s  \n' % (argument.name)

    def __str__(self):
        buf = '\n'.join([str(arg) for arg in self.arglist])
        return buf
            