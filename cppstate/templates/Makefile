#[[[cog 
#  import cog
#  import json
#  import cppstate
#  with open('config.json') as f:
#    config = json.load(f)
#  states = config['states']
#  states_ids = {state: 'ID_'+state.upper() for state in states}
#  transitions = config['transitions']
#]]]
#[[[end]]]

dir_guard = @mkdir -p $(@D)
OUT_O_DIR = objs


all: main.exe

#[[[cog 
#  objects = []
#  objects += ["$(OUT_O_DIR)/main.o", "$(OUT_O_DIR)/StateMachine.o"]
#  objects += ['$(OUT_O_DIR)/{}.o'.format(name) for name in states]
#  cog.out('main.exe: {}'.format(' '.join(objects)))
#]]]
#[[[end]]]
	#[[[cog 
	#  states_o = ['$(OUT_O_DIR)/{}.o'.format(name) for name in states]
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
#  for state_name in states:
#      cog.outl('$(OUT_O_DIR)/{}.o: {}.cpp'.format(state_name, state_name))
#      cog.outl('\t$(dir_guard)')
#      cog.outl('\tg++ -c $< -o $@')
#      cog.outl()
#]]]
#[[[end]]]
clean:
	rm -rf $(OUT_O_DIR)
	rm -f main.exe

.PHONY: all