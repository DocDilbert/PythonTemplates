//[[[cog 
//  import cog
//  import cppstate
//  
//  # load configuration
//  config = cppstate.helper.load_config()
//
//  state_helper = cppstate.helper.StateHelper(active_state, config)
//
//  ns_gen = cppstate.helper.NameSpaceGenerator("config.json")
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

//[[[cog 
//  ns_gen.generate_namespace_header_for_states()
//]]]
//[[[end]]]

//[[[cog 
//  # Constructor
//  cog.outl("{}::{}(IStateMachine& stateMachine) :".format(active_state, active_state))
//  cog.out("    stateData(nullptr),")
//  cog.out("    stateMachine(stateMachine)")
//]]]
//[[[end]]]
{
}

//[[[cog 
//  cog.outl('void {}::init(StateData& stateData)'.format(active_state))
//]]]
//[[[end]]]
{
    this->stateData = &stateData;

    // Insert init code here
}

//[[[cog 
//  cog.outl('{}::{} {}::getId()'.format(ns_gen.get_namespace_to_id(), config.typename_of_ids, active_state))
//]]]
//[[[end]]]
{
    //[[[cog 
    //  cog.out("return {}::{};".format(ns_gen.get_namespace_to_id(), config.id_of_state[active_state]))
    //]]]
    //[[[end]]]
}

//[[[cog 
//  cog.outl('void {}::entry({}::{} lastState)'.format(active_state, ns_gen.get_namespace_to_id(), config.typename_of_ids))
//]]]
//[[[end]]]
{
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
    // Insert state code here

    // TODO: Remove debug code
    //[[[cog 
    //  cog.outl('printf("execute: {}\\n");'.format(active_state))
    //]]]
    //[[[end]]]

    processTransitions();
}

//[[[cog 
//  cog.outl('void {}::exit({}::{} nextState)'.format(active_state, ns_gen.get_namespace_to_id(), config.typename_of_ids))
//]]]
//[[[end]]]
{
    // TODO: Remove debug code
    //[[[cog 
    //  cog.outl('printf("exit: {}\\n");'.format(active_state))
    //]]]
    //[[[end]]]
}

//[[[cog 
//  state_helper.generate_state_checks()
//]]]
//[[[end]]]
//[[[cog 
//  state_helper.generate_process_transitions()
//]]]
//[[[end]]]

//[[[cog 
//  ns_gen.generate_namespace_footer_for_states()
//]]]
//[[[end]]]