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

#include <stdio.h>
//[[[cog 
//  cog.outl('#include "{}.h"'.format(config.typename_of_base_state))
//]]]
//[[[end]]]

//[[[cog 
//  ns_gen.generate_namespace_header_for_states()
//]]]
//[[[end]]]

//[[[cog 
//  # Constructor
//  cog.outl("{}::{}({}{}& stateMachine) :".format(config.typename_of_base_state, config.typename_of_base_state, ns_gen.get_namespace_to_statemachine(), config.typename_of_state_machine_interface))
//  cog.outl("    stateData(nullptr),")
//  cog.outl("    stateMachine(stateMachine)")
//]]]
//[[[end]]]
{
}

//[[[cog cog.out("void {}::init({}{}& stateData)".format(config.typename_of_base_state, ns_gen.get_namespace_to_statemachine(), config.typename_of_state_data_structure));]]]
//[[[end]]]
{
    this->stateData = &stateData;

    // Insert init code here
}

//[[[cog cog.outl('{}{} {}::getId()'.format(ns_gen.get_namespace_to_id(), config.typename_of_ids, config.typename_of_base_state))]]]
//[[[end]]]
{
    
}

//[[[cog 
//  cog.outl('void {}::entry({}{} lastState)'.format(config.typename_of_base_state, ns_gen.get_namespace_to_id(), config.typename_of_ids))
//]]]
//[[[end]]]
{
}

//[[[cog 
//  cog.outl('void {}::execute()'.format(config.typename_of_base_state))
//]]]
//[[[end]]]
{
    // Insert state code here
}

//[[[cog 
//  cog.outl('void {}::exit({}{} nextState)'.format(config.typename_of_base_state, ns_gen.get_namespace_to_id(), config.typename_of_ids))
//]]]
//[[[end]]]
{
}


//[[[cog 
//  ns_gen.generate_namespace_footer_for_states()
//]]]
//[[[end]]]