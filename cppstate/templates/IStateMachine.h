//[[[cog 
//  import cog
//  import cppstate
//  
//  # load configuration
//  states, id_of_state, transitions, config = cppstate.helper.load_config()
//
//  ns_gen = cppstate.helper.NameSpaceGenerator("config.json")
//]]]
//[[[end]]]
///
/// \file
/// \copyright Festo AG & Co. KG, Esslingen. All rights reserved.
/// \author TODO
///

#pragma once

//[[[cog 
//  ns_gen.generate_namespace_header()
//]]]
//[[[end]]]

#include "IState.h"

/// Abstract interface to a state machine
class IStateMachine
{
public:
	/// Set the next state of the state machine
	/// \param state the next state 
	//[[[cog 
	//  cog.outl("virtual void setNextState({}::StateId state) = 0;".format(ns_gen.get_path_to_state()))
	//]]]
	//[[[end]]]
};

//[[[cog 
//  ns_gen.generate_namespace_footer()
//]]]
//[[[end]]]