import cog
class StateClass:
    def __init__(self, name):
        self.__name = name
        self.__indent = ""
        self.__indentSpaceCount = 0

    def get_id(self):
        return "ID_"+self.__name.upper()

    def out_indent(self, str):
        cog.outl("{}{}".format(self.__indent, str))
   
    def out_private(self):
        self.out_indent("private:")

    def out_public(self):
        self.out_indent("public:")

    def out_class(self):
        self.out_indent("class {} : public IState".format(self.__name))

     
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

    def out_method(self,*, name, arguments="", returns="void"):
        self.out_indent("{} {}({})".format(
            returns,
            name, 
            arguments
        ))

    def raise_indent(self):
        self.__indentSpaceCount=self.__indentSpaceCount+4
        self.__indent=" "*self.__indentSpaceCount

    def lower_indent(self):
        self.__indentSpaceCount=self.__indentSpaceCount-4
        self.__indent=" "*self.__indentSpaceCount   

    def out(self):
        self.out_class()
        self.out_begin()
        self.out_public()
        self.raise_indent()

        self.out_method(name="getId", returns="StateId")
        self.out_begin()
        self.raise_indent()
        self.out_code("return "+self.get_id())
        self.lower_indent()
        self.out_end()
        
        cog.outl()

        self.out_method(name="update")
        self.out_begin()
        self.raise_indent()
        self.out_comment("Check for transitions here ...")
        self.lower_indent()
        self.out_end()

        cog.outl()

        self.out_method(name="setNextState", arguments="StateId state")
        self.out_begin()
        self.raise_indent()
        self.out_code("stateMachine.setNextState(state)")
        self.lower_indent()
        self.out_end()

        self.lower_indent()

        cog.outl()

        self.out_private()

        self.raise_indent()
        self.out_member(type="IStateMachine&", name="stateMachine" )
        self.lower_indent()
        self.out_end()