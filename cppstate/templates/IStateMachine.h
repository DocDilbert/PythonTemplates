//[[[cog 
//  import cog
//  import cppstate
//  
//  # load configuration
//  states, id_of_state, transitions = cppstate.helper.load_config()
//
//]]]
//[[[end]]]
///
/// \file
/// \copyright Festo AG & Co. KG, Esslingen. All rights reserved.
/// \author TODO
///

#pragma once

#include "IState.h"

/// Abstract interface to a state machine
class IStateMachine
{
public:
	/// Set the next state of the state machine
	/// \param state the next state 
  	virtual void setNextState(StateId state) = 0;
};
