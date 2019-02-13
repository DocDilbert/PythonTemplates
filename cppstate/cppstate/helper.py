import cog
import json

def load_config():
    with open('config.json') as f:
        config = json.load(f)

    states = config['states']
    id_of_state = {state: 'ID_'+state.upper() for state in states}
    transitions = config['transitions']
    return (states, id_of_state, transitions)

class NameSpaceGenerator:
    def __init__(self, filename):
        config = None
        with open('config.json') as f:
            config = json.load(f)

        settings = config['settings']
        self.namespace = settings['namespace'].split('/')
        self.namespace_of_states = list(self.namespace)
        self.namespace_of_states.append(settings['namespace_of_states'])

    def get_path(self):
        return "::".join(self.namespace)

    def get_path_to_state(self):
        return self.namespace_of_states[-1]

    def generate_namespace_header(self):
        for name in self.namespace:
            cog.outl("namespace {}\n{{".format(name))

    def generate_namespace_footer(self):
        for name in self.namespace:
            cog.outl("}}".format(name))

    def generate_namespace_header_for_states(self):
        for name in self.namespace_of_states:
            cog.outl("namespace {}\n{{".format(name))

    def generate_namespace_footer_for_states(self):
        for name in self.namespace_of_states:
            cog.outl("}}".format(name))

class StateHelper:
    def __init__(self, name, transitions=None):
        self.__name = name
        self.__indent = ""
        self.__indentSpaceCount = 0
        self.__transitions=transitions       

    def get_id(self, from_=None):
        if from_:
            return "ID_" + from_.upper()
        else:
            return "ID_" + self.__name.upper()

    def out_indent(self, str):
        cog.outl("{}{}".format(self.__indent, str))
   
    def out_nl(self):
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
        self.out_code("stateMachine.setNextState({})".format(self.get_id(to_state)))
        self.out_code("return")
        self.lower_indent()
        self.out_end()

    def generate_processTransitions(self):
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
                    self.out_nl()
        else:
            self.out_comment("Check for transitions here ...")
        self.lower_indent()
        self.out_end()

    def out_state_check(self, name):
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

    def out_state_check_prototype(self, transition_from, transition_to, transition_name):
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
            self.out_state_check(transition['name'])
            self.out_nl()
    
    def generate_state_check_prototypes(self):
        if not self.__transitions:
            return

        for transition in self.__transitions:
            self.out_state_check_prototype(transition['from'], transition['to'],transition['name'])
            self.out_nl()