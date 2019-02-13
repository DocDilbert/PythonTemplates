#[[[cog 
#  import cog
#  import cppstate
#  
#  # load configuration
#  states, id_of_state, transitions, config = cppstate.helper.load_config()
# 
#  ns_gen = cppstate.helper.NameSpaceGenerator("config.json")
#]]]
#[[[end]]]

JAVA = java
PLANTUML_JAR = C:/Dev/PlantUml/plantuml.jar

PLANTUML = @$(JAVA) -Dapple.awt.UIElement=true -jar $(PLANTUML_JAR)

dir_guard = @mkdir -p $(@D)
OUT_O_DIR = objs

#[[[cog 
#  objects = []
#  objects += ["$(OUT_O_DIR)/main.o", "$(OUT_O_DIR)/StateMachine.o"]
#  objects += ['$(OUT_O_DIR)/{}.o'.format(state) for state in states]
#  cog.outl('OBJECTS = ')
#  cog.out('\n'.join("OBJECTS += {}".format(obj) for obj in objects))
#  cog.outl('\n')
#  cog.outl("VPATH += ./{}".format(ns_gen.get_path_to_state()))
#  cog.outl('\n')
#  cog.outl('INCLUDES  = -I.')
#  cog.outl("INCLUDES += -I./{}".format(ns_gen.get_path_to_state()))
#]]]
#[[[end]]]

all: main.exe

main.exe: $(OBJECTS)
	g++ -o main.exe $(OBJECTS)

$(OUT_O_DIR)/%.o: %.cpp
	$(dir_guard)
	g++ $(INCLUDES) -c $< -o $@

clean:
	rm -rf $(OUT_O_DIR)
	rm -f main.exe

doc: StateMachine.wsd
	$(PLANTUML) StateMachine.wsd

.PHONY: all