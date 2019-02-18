#[[[cog 
#  import cog
#  from cppstate.config import load_config
#  from cppstate.statehelper import StateHelper
#  from cppstate.namespacegenerator import NameSpaceGenerator
#  
#  # load configuration
#  config = load_config(config_file)
# 
#  ns_gen = NameSpaceGenerator(config)
#]]]
#[[[end]]]

JAVA = java
PLANTUML_JAR = C:/Dev/PlantUml/plantuml.jar

PLANTUML = @$(JAVA) -Dapple.awt.UIElement=true -jar $(PLANTUML_JAR)

dir_guard = @mkdir -p $(@D)
OUT_O_DIR = objs

#[[[cog 
#  objects = []
#  objects += ["$(OUT_O_DIR)/main.o", "$(OUT_O_DIR)/{}.o".format(config.typename_of_state_machine)]
#  objects += ["$(OUT_O_DIR)/{0}.o".format(config.typename_of_base_state)]
#  objects += ['$(OUT_O_DIR)/{}.o'.format(state) for state in config.states]
#  cog.outl('OBJECTS = ')
#  cog.out('\n'.join("OBJECTS += {}".format(obj) for obj in objects))
#  cog.outl('\n')
#  cog.outl("VPATH += ./{}".format(ns_gen.get_path_to_state_file()))
#  cog.outl("VPATH += ./{}".format(ns_gen.get_path_to_id_file()))
#  cog.outl('\n')
#  cog.outl('INCLUDES  = -I.')
#  cog.outl("INCLUDES += -I./{}".format(ns_gen.get_path_to_state_file()))
#  cog.outl("INCLUDES += -I./{}".format(ns_gen.get_path_to_id_file()))
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