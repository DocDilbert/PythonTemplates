import cog
import json

class Config:
    def __init__(self, parsed_json):
        state_list = [state for state in parsed_json['states']] 
        self.states = [state['name'] for state in state_list]
        self.state_ids = [state['id'] for state in state_list]
        self.id_of_state = {state: state_id for state, state_id in zip(self.states, self.state_ids)}
        self.init_state = parsed_json['init_state']['to']
        self.init_state_id = parsed_json['init_state']['id']
        self.transitions = parsed_json['transitions']

        settings = parsed_json['settings']
        
        self.namespace=settings['namespace']
        self.namespace_of_states=settings['namespace_of_states']
        self.namespace_of_ids=settings['namespace_of_ids']

        self.states_are_in_subnamespace=settings['states_are_in_subnamespace']
        self.ids_are_in_subnamespace=settings['ids_are_in_subnamespace']

        self.typename_of_ids = settings['typename_of_ids']
        self.typename_of_state_interface = settings['typename_of_state_interface']
        self.typename_of_state_machine_interface = settings['typename_of_state_machine_interface']
        self.typename_of_state_data_structure = settings['typename_of_state_data_structure']
        self.typename_of_state_machine = settings['typename_of_state_machine']

def load_config(filename):
    with open(filename) as f:
        config = json.load(f)
    
    return Config(config)

class NameSpaceGenerator:
    def __init__(self, config):
        self.namespace = config.namespace.split("::")
        self.namespace_of_states = config.namespace_of_states.split("::")
        self.namespace_of_ids =config.namespace_of_ids.split("::")
        self.states_are_in_subnamespace = config.states_are_in_subnamespace
        self.ids_are_in_subnamespace = config.ids_are_in_subnamespace

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
        for name in self.namespace:
            cog.outl("namespace {}\n{{".format(name))

    def generate_namespace_footer(self):
        for _ in self.namespace:
            cog.outl("}}".format())

    def generate_namespace_header_for_states(self):
        for name in self.namespace_of_states:
            cog.outl("namespace {}\n{{".format(name))

    def generate_namespace_footer_for_states(self):
        for _ in self.namespace_of_states:
            cog.outl("}}".format())

    def generate_namespace_header_for_ids(self):
        for name in self.namespace_of_ids:
            cog.outl("namespace {}\n{{".format(name))

    def generate_namespace_footer_for_ids(self):
        for _ in self.namespace_of_ids:
            cog.outl("}}".format())

class StateHelper:
    def __init__(self, name, config):
        self.__name = name
        self.__indent = ""
        self.__indentSpaceCount = 0
        self.__id_of_state=config.id_of_state
        self.__transitions=[transition for transition in config.transitions if transition['from']==name]
        self.__ns_gen = NameSpaceGenerator(config)

    def get_id(self, from_=None):
        if from_:
            return self.__id_of_state[from_]
        else:
            return self.__id_of_state[self.__name]

    def out_indent(self, str):
        cog.outl("{}{}".format(self.__indent, str))
   
    def __out_nl(self):
        self.out_indent("")

    def out_begin(self):
        self.out_indent("{")

    def out_end(self):
        self.out_indent("}")

    def out_code(self, code):
        self.out_indent("{};".format(code))

    def out_comment(self, comment):
        self.out_indent("// {}".format(comment))

    def raise_indent(self):
        self.__indentSpaceCount=self.__indentSpaceCount+4
        self.__indent=" "*self.__indentSpaceCount

    def lower_indent(self):
        self.__indentSpaceCount=self.__indentSpaceCount-4
        self.__indent=" "*self.__indentSpaceCount   

    def out_transition_check(self, name, to_state):
        self.out_indent("if (check{}())".format(name))
        self.out_begin()
        self.raise_indent()
        self.out_code("stateMachine.setNextState({}{})".format(self.__ns_gen.get_namespace_to_id(), self.get_id(to_state)))
        self.out_code("return")
        self.lower_indent()
        self.out_end()

    def generate_process_transitions(self):
        self.out_indent("void {}::processTransitions()".format(
            self.__name
        ))
        self.out_begin()
        self.raise_indent()

        if self.__transitions:
            last = self.__transitions[-1]
            for transition in self.__transitions:
                self.out_transition_check(transition['name'], transition['to'])

                if transition!=last:
                    self.__out_nl()
        else:
            self.out_comment("Check for transitions here ...")
        self.lower_indent()
        self.out_end()

    def __out_state_check(self, name):
        self.out_indent("bool {}::{}()".format(
            self.__name, 
            "check{}".format(name)
        ))
        self.out_begin()
        self.raise_indent()
        self.out_comment("If transition must be executed return true.")
        self.out_code("return false")
        self.lower_indent()
        self.out_end()

    def __out_state_check_prototype(self, transition_from, transition_to, transition_name):
        self.out_indent(
            "/// Returns true when a transition from {} to {} is requested.".format(transition_from, transition_to)
        )
        self.out_indent("bool {}();".format(
            "check{}".format(transition_name)
        ))
        
    def generate_state_checks(self):
        if not self.__transitions:
            return

        for transition in self.__transitions:
            self.__out_state_check(transition['name'])
            self.__out_nl()
    
    def generate_state_check_prototypes(self):
        if not self.__transitions:
            return

        for transition in self.__transitions:
            self.__out_state_check_prototype(transition['from'], transition['to'],transition['name'])
            self.__out_nl()