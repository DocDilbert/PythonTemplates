//[[[cog 
//  import cog
//  import json
//  import cppstate
//  with open('config.json') as f:
//    config = json.load(f)
//  states = config['states']
//  states_ids = {state: 'ID_'+state.upper() for state in states}
//  transitions = config['transitions']
//]]]
//[[[end]]]
#pragma once

#include "IState.h"
#include "IStateMachine.h"

//[[[cog 
//  state_transitions = [transition for transition in transitions if transition['from']==state_name]
//  state_obj = cppstate.state_class.StateClass(state_name, state_transitions)
//  state_obj.out()
//]]]
//[[[end]]]

