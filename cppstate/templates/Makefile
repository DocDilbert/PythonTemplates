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
PLANTUML_JAR = /usr/local/Cellar/plantuml/1.2019.0/libexec/plantuml.jar

PLANTUML = @$(JAVA) -Dapple.awt.UIElement=true -jar $(PLANTUML_JAR)

dir_guard = @mkdir -p $(@D)
OUT_O_DIR = objs

all: main.exe

#[[[cog 
#  objects = []
#  objects += ["$(OUT_O_DIR)/main.o", "$(OUT_O_DIR)/StateMachine.o"]
#  objects += ['$(OUT_O_DIR)/{}.o'.format(state) for state in states]
#  cog.out('main.exe: {}'.format(' '.join(objects)))
#]]]
#[[[end]]]
	#[[[cog 
	#  states_o = ['$(OUT_O_DIR)/{}.o'.format(state) for state in states]
	#  states_o += ['$(OUT_O_DIR)/main.o', '$(OUT_O_DIR)/StateMachine.o']
	#  cog.outl('g++ -o main.exe {}'.format(' '.join(states_o)))
	#]]]
	#[[[end]]]

$(OUT_O_DIR)/main.o: main.cpp 
	$(dir_guard)
	g++ -c $< -o $@

$(OUT_O_DIR)/StateMachine.o: StateMachine.cpp
	$(dir_guard)
	g++ -c $< -o $@

#[[[cog 
#  for state in states:
#      cog.outl('$(OUT_O_DIR)/{}.o: {}.cpp'.format(state, state))
#      cog.outl('\t$(dir_guard)')
#      cog.outl('\tg++ -c $< -o $@')
#      cog.outl()
#]]]
#[[[end]]]
clean:
	rm -rf $(OUT_O_DIR)
	rm -f main.exe

doc: StateMachine.wsd
	$(PLANTUML) StateMachine.wsd

.PHONY: all