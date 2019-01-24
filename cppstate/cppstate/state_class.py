import cog

class StateClass:
    def __init__(self, name, transitions=None):
        self.__name = name
        self.__indent = ""
        self.__indentSpaceCount = 0
        self.__transitions=transitions       

    def get_id(self, from_=None):
        if from_:
            return "ID_"+from_.upper()
        else:
            return "ID_"+self.__name.upper()

    def out_indent(self, str):
        cog.outl("{}{}".format(self.__indent, str))
   
    def out_nl(self):
        self.out_indent("")

    def out_private(self):
        self.out_indent("private:")

    def out_public(self):
        self.out_indent("public:")

    def out_class(self):
        self.out_indent("class {} : public IState".format(self.__name))

    def out_constructor_prototype(self, initializer_list = True):
        ilist = ""
        if initializer_list:
            ilist=":"

        self.out_indent("{}(IStateMachine& stateMachine) {}".format(self.__name, ilist))

    def out_begin(self):
        self.out_indent("{")

    def out_end(self):
        self.out_indent("}")

    def out_code(self, code):
        self.out_indent("{};".format(code))

    def out_comment(self, comment):
        self.out_indent("// {}".format(comment))

    def out_member(self, *, name, type):
        self.out_indent("{} {};".format(type, name))

    def out_method_prototype(self,*, name, arguments="", returns="void"):
        self.out_indent("{} {}({})".format(
            returns,
            name, 
            arguments
        ))

    def out_state_check(self, name):
        self.out_method_prototype(name="check{}".format(name), returns="bool")
        self.out_begin()
        self.raise_indent()
        self.out_comment("If transition must be executed return true.")
        self.out_code("return false")
        self.lower_indent()
        self.out_end()

    def out_state_checks(self):
        if not self.__transitions:
            return

        for transition in self.__transitions:
            self.out_state_check(transition['name'])
            self.out_nl()

    def raise_indent(self):
        self.__indentSpaceCount=self.__indentSpaceCount+4
        self.__indent=" "*self.__indentSpaceCount

    def lower_indent(self):
        self.__indentSpaceCount=self.__indentSpaceCount-4
        self.__indent=" "*self.__indentSpaceCount   

    def generate_transition_check(self, name, to_state):
        self.out_indent("if (check{}())".format(name))
        self.out_begin()
        self.raise_indent()
        self.out_code("setNextState({})".format(self.get_id(to_state)))
        self.out_code("return")
        self.lower_indent()
        self.out_end()

    def generate_processTransitions(self):
        self.out_method_prototype(name="processTransitions")
        self.out_begin()
        self.raise_indent()

        if self.__transitions:
            last = self.__transitions[-1]
            for transition in self.__transitions:
                self.generate_transition_check(transition['name'], transition['to'])

                if transition!=last:
                    self.out_nl()
        else:
            self.out_comment("Check for transitions here ...")
        self.lower_indent()
        self.out_end()

    def out(self):
        self.out_class()
        self.out_begin()
        self.out_public()
        self.raise_indent()
        
        # Constructor
        self.out_constructor_prototype(True)
        self.out_indent("stateMachine(stateMachine)")
        self.out_begin()
        self.raise_indent()
        self.lower_indent()
        self.out_end()
        self.out_nl()

        # getId
        self.out_method_prototype(name="getId", returns="StateId")
        self.out_begin()
        self.raise_indent()
        self.out_code("return "+self.get_id())
        self.lower_indent()
        self.out_end()
        self.out_nl()

        # check methods
        self.out_state_checks()
        self.generate_processTransitions()
        self.out_nl()

         # entry
        self.out_method_prototype(name="entry")
        self.out_begin()
        self.raise_indent()
        self.lower_indent()
        self.out_end()
        self.out_nl()

        # update
        self.out_method_prototype(name="update")
        self.out_begin()
        self.raise_indent()
        self.out_code("processTransitions()")
        self.out_nl()
        self.out_comment("Insert state code here")
        self.lower_indent()
        self.out_end()

        self.out_nl()

        self.lower_indent()
        self.out_private()
        self.raise_indent()

        # setNextState
        self.out_method_prototype(name="setNextState", arguments="StateId state")
        self.out_begin()
        self.raise_indent()
        self.out_code("stateMachine.setNextState(state)")
        self.lower_indent()
        self.out_end()

        self.out_nl()

        self.out_member(type="IStateMachine&", name="stateMachine" )
        self.lower_indent()
        self.out_code("}")