//[[[cog 
//  import cog
//  import cppstate
//  
//  # load configuration
//  states, id_of_state, transitions = cppstate.helper.load_config()
//
//]]]
//[[[end]]]
#pragma once

#include "IState.h"

class IStateMachine
{
public:
  	virtual void setNextState(StateId state) = 0;
};
