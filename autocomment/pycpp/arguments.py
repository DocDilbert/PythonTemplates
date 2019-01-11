def arguments_factory(generator):
    args = Arguments()
    [args.add(name_token, type_token, pass_by) for (name_token, type_token, pass_by) in generator]
    return args


class Argument(object):
    def __init__(self, name_token, type_token, pass_by):
        self.name_token = name_token
        self.type_token = type_token
        self.pass_by = pass_by

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

class Arguments(object):

    def __init__(self):
        self.arglist = []

    def add(self, name, type_, pass_by):
        self.arglist.append(Argument(name, type_, pass_by))

    def __len__(self):
        return len(self.arglist)

    def __iter__(self):
        return iter(self.arglist)
