"""Diess Modul enhält die Klassen ArgumentsFactory sowie Arguments.
"""


from pycpp.code import Block

class ArgumentsFactory(object):
    """ Diese Klasse erstellt Methoden Argumente aus Token Positionen
    """
    def __init__(self, tokens, description_lookup=None):
        self.description_lookup = description_lookup
        self.tokens = tokens

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

    def __call__(self, generator):
        args = Arguments()
        for (name_pos, type_pos, pass_by_pos) in generator:
            args.add(
                self.__search_for_token_at_pos(name_pos, self.tokens),
                self.__search_for_token_at_pos(type_pos, self.tokens),
                self.__search_for_token_at_pos(pass_by_pos, self.tokens)
            )


        if self.description_lookup:
            for arg in args:
                if arg.is_pass_by_pointer():
                    arg.description = self.description_lookup("*"+arg.name)
                elif arg.is_pass_by_reference():
                    arg.description = self.description_lookup("&"+arg.name)
                else:
                    arg.description = self.description_lookup(arg.name)
        return args


class Argument(object):
    """ Diese Klasse ist ein Daten Container für ein einzelnes Argument
        einer Methode.
    """
    def __init__(self, name_token, type_token, pass_by_token):
        self.name_token = name_token
        self.type_token = type_token
        self.pass_by_token = pass_by_token
        self.description = None

    def __eq__(self, other):
        if self.name_token != other.name_token:
            return False

        if self.type_token != other.type_token:
            return False

        if self.pass_by_token != other.pass_by:
            return False

        return True

    def is_pass_by_pointer(self):
        """ Gibt True zurück wenn es sich bei dem Argument um einen Pointer handelt.
        """
        if self.pass_by_token is None:
            return False

        if self.pass_by_token.val == '*':
            return True

        return False

    def is_pass_by_reference(self):
        """ Gibt True zurück wenn es sich bei dem Argument um eine Referenz handelt.
        """
        if self.pass_by_token is None:
            return False

        if self.pass_by_token.val == '&':
            return True

        return False

    @property
    def name(self):
        """ Der Name des Arguments als String
        """
        return self.name_token.val

    @property
    def type(self):
        """ Der Typ des Arguments als String
        """
        return self.type_token.val

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        buf = []
        buf.append(self.name)
        if self.description:
            buf.append(self.description)
        return '/// \\param %s' % (" ".join(buf))

class Arguments(object):
    """ Diese Klasse dient als Container mehrerer Methoden Argumente
    """

    def __init__(self):
        self.arglist = []

    def add(self, name, type_, pass_by):
        """ Füge ein Methoden Argument der Liste hinzu
        """
        self.arglist.append(Argument(name, type_, pass_by))

    def __len__(self):
        return len(self.arglist)

    def __iter__(self):
        return iter(self.arglist)

    def __str__(self):
        buf = '\n'.join([str(arg) for arg in self.arglist])
        return buf

    def __repr__(self):
        return self.__str__()
            