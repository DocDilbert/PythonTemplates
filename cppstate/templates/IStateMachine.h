//[[[cog 
//  import cog
//  from cppstate.config import load_config
//  from cppstate.statehelper import StateHelper
//  from cppstate.namespacegenerator import NameSpaceGenerator
//  
//  # load configuration
//  config = load_config(config_file)
//  ns_gen = NameSpaceGenerator(config)
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

//[[[cog cog.out(ns_gen.generate_namespace_header())]]]
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

//[[[cog cog.out(ns_gen.generate_namespace_footer())]]]
//[[[end]]]