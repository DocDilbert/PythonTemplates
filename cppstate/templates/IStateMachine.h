//[[[cog 
//  import cog
//  import cppstate
//  
//  # load configuration
//  config = cppstate.helper.load_config()
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
//[[[cog cog.out('#include "{}.h"'.format(config.typename_of_state_interface))]]]
//[[[end]]] 

//[[[cog ns_gen.generate_namespace_header()]]]
//[[[end]]]

/// Abstract interface to a state machine
//[[[cog cog.out('class {}'.format(config.typename_of_state_machine_interface))]]]
//[[[end]]] 
{
public:
	/// Set the next state of the state machine
	/// \param state the next state 
	//[[[cog 
	//  cog.outl("virtual void setNextState({}{} state) = 0;".format(ns_gen.get_namespace_to_id(), config.typename_of_ids))
	//]]]
	//[[[end]]]
};

//[[[cog 
//  ns_gen.generate_namespace_footer()
//]]]
//[[[end]]]