class NameSpaceGenerator:
    def __init__(self, config):

        self.namespace = config.namespace.split("::")
        self.namespace_of_states = config.namespace_of_states.split("::")
        self.namespace_of_ids =config.namespace_of_ids.split("::")
        self.states_are_in_subnamespace = self.is_subnamespace(self.namespace, self.namespace_of_states)
        self.ids_are_in_subnamespace = self.is_subnamespace(self.namespace, self.namespace_of_ids)
        self.ids_are_in_equal_namespace = self.is_equal_namespace(self.namespace, self.namespace_of_ids)
    
    def is_subnamespace(self, namespace1, namespace2):
        if len(namespace2)<len(namespace1):
            return False
        for n1, n2 in zip(namespace1, namespace2):
            if n1!=n2:
                return False
        
        return True

    def is_equal_namespace(self, namespace1, namespace2):
        return namespace1 == namespace2

    def get_path_to_id_file(self):
        return self.namespace_of_ids[-1]

    def get_path_to_state_file(self):
        return self.namespace_of_states[-1]

    def get_main_namespace(self):
        return "::".join(self.namespace)

    def get_namespace_to_statemachine(self):
        if self.states_are_in_subnamespace:
            return ""
        else:
            return "::".join(self.namespace)+"::"

    def get_namespace_to_state(self):
        if self.states_are_in_subnamespace:
            return self.namespace_of_states[-1]+"::"
        else:
            return "::".join(self.namespace_of_states)+"::"

    
    def get_namespace_to_id(self):

        if self.ids_are_in_subnamespace:
            return self.namespace_of_ids[-1]+"::"
        else:
            return "::".join(self.namespace_of_ids)+"::"

            
    def generate_namespace_header(self):
        buf = ""
        for name in self.namespace:
            buf += "namespace {}\n{{\n".format(name)
        return buf

    def generate_namespace_footer(self):
        buf = ""
        for _ in self.namespace:
            buf += "}}\n".format()
        return buf

    def generate_namespace_header_for_states(self):
        buf = ""
        for name in self.namespace_of_states:
            buf += "namespace {}\n{{\n".format(name)
        return buf

    def generate_namespace_footer_for_states(self):
        buf = ""
        for _ in self.namespace_of_states:
            buf+= "}}\n".format()
        return buf

    def generate_namespace_header_for_ids(self):
        buf = ""
        for name in self.namespace_of_ids:
            buf += "namespace {}\n{{\n".format(name)
        return buf

    def generate_namespace_footer_for_ids(self):
        buf = ""
        for _ in self.namespace_of_ids:
            buf += "}}\n".format()
        return buf