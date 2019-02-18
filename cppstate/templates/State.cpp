//[[[cog 
//  import cog
//  from cppstate.config import load_config
//  from cppstate.statehelper import StateHelper
//  from cppstate.namespacegenerator import NameSpaceGenerator
//  
//  # load configuration
//  config = load_config(config_file)
//  state_helper = StateHelper(active_state, config)
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
//  cog.outl('#include "{}.h"'.format(active_state))
//]]]
//[[[end]]]

//[[[cog cog.out(ns_gen.generate_namespace_header_for_states())]]]
//[[[end]]]

//[[[cog 
//  # Constructor
//  cog.outl("{}::{}({}{}& stateMachine) :".format(active_state, active_state, ns_gen.get_namespace_to_statemachine(), config.typename_of_state_machine_interface))
//  cog.outl("    {}(stateMachine),".format(config.typename_of_base_state))
//  cog.outl("    stateData(nullptr),")
//  cog.outl("    stateMachine(stateMachine)")
//]]]
//[[[end]]]
{
}

//[[[cog cog.out("void {}::init({}{}& stateData)".format(active_state, ns_gen.get_namespace_to_statemachine(), config.typename_of_state_data_structure));]]]
//[[[end]]]
{
    this->stateData = &stateData;

    // Insert init code here
}

//[[[cog cog.outl('{}{} {}::getId()'.format(ns_gen.get_namespace_to_id(), config.typename_of_ids, active_state))]]]
//[[[end]]]
{
    //[[[cogcog.out("return {}{};".format(ns_gen.get_namespace_to_id(), config.id_of_state[active_state]))]]]
    //[[[end]]]
}

//[[[cog 
//  cog.outl('void {}::entry({}{} lastState)'.format(active_state, ns_gen.get_namespace_to_id(), config.typename_of_ids))
//]]]
//[[[end]]]
{
    //[[[cog cog.outl("{}::entry(lastState);".format(config.typename_of_base_state))]]]
    //[[[end]]]

    // TODO: Remove debug code
    //[[[cog 
    //  cog.outl('printf("entry: {}\\n");'.format(active_state))
    //]]]
    //[[[end]]]
}

//[[[cog 
//  cog.outl('void {}::execute()'.format(active_state))
//]]]
//[[[end]]]
{
    //[[[cog cog.outl("{}::execute();".format(config.typename_of_base_state))]]]
    //[[[end]]]
    
    // Insert state code here

    // TODO: Remove debug code
    //[[[cog 
    //  cog.outl('printf("execute: {}\\n");'.format(active_state))
    //]]]
    //[[[end]]]

    processTransitions();
}

//[[[cog 
//  cog.outl('void {}::exit({}{} nextState)'.format(active_state, ns_gen.get_namespace_to_id(), config.typename_of_ids))
//]]]
//[[[end]]]
{
    //[[[cog cog.outl("{}::exit(nextState);".format(config.typename_of_base_state))]]]
    //[[[end]]]
    
    // TODO: Remove debug code
    //[[[cog 
    //  cog.outl('printf("exit: {}\\n");'.format(active_state))
    //]]]
    //[[[end]]]
}

//[[[cog cog.out(state_helper.generate_state_checks())]]]
//[[[end]]]

//[[[cog cog.out(state_helper.generate_process_transitions())]]]
//[[[end]]]

//[[[cog cog.out(ns_gen.generate_namespace_footer_for_states())]]]
//[[[end]]]