from cppstate.namespacegenerator import NameSpaceGenerator

class StateHelper:
    def __init__(self, name, config):
        self.__buf = ""
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
        self.__buf+="{}{}\n".format(self.__indent, str)
   
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
        self.__buf = ""
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

        return self.__buf

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
        self.__buf=""
        if not self.__transitions:
            return

        for transition in self.__transitions:
            self.__out_state_check(transition['name'])
            self.__out_nl()

        return self.__buf
    
    def generate_state_check_prototypes(self):
        self.__buf=""
        if not self.__transitions:
            return

        for transition in self.__transitions:
            self.__out_state_check_prototype(transition['from'], transition['to'],transition['name'])
            self.__out_nl()

        return self.__buf