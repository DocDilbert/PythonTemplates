#[[[cog 
#  import cog
#  import cppstate
#  
#  # load configuration
#  states, id_of_state, transitions = cppstate.helper.load_config()
#
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
#]]]
#[[[end]]]

all: main.exe

main.exe: $(OBJECTS)
	g++ -o main.exe $(OBJECTS)

$(OUT_O_DIR)/%.o: %.cpp
	$(dir_guard)
	g++ -c $< -o $@

clean:
	rm -rf $(OUT_O_DIR)
	rm -f main.exe

doc: StateMachine.wsd
	$(PLANTUML) StateMachine.wsd

.PHONY: all