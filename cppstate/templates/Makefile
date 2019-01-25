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
all: main.exe

main.exe: main.o StateMachine.o States
	#[[[cog 
	#  states_o = ['{}.o'.format(name) for name in states]
	#  states_o += ['main.o', 'StateMachine.o']
	#  cog.outl('g++ -o main.exe {}'.format(' '.join(states_o)))
	#]]]
	#[[[end]]]

main.o: main.cpp 
	g++ -c main.cpp

StateMachine.o: StateMachine.cpp
	g++ -c StateMachine.cpp

#[[[cog 
#  states_cpp = ['{}.o'.format(name) for name in states]
#  cog.out('States: {}'.format(' '.join(states_cpp)))
#]]]
#[[[end]]]

#[[[cog 
#  for state_name in states:
#      cog.outl('{}.o: {}.cpp'.format(state_name, state_name))
#      cog.outl('\tg++ -c {}.cpp'.format(state_name))
#      cog.outl()
#]]]
#[[[end]]]

.PHONY: all