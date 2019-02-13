//[[[cog 
//  import cog
//  import cppstate
//  
//  # load configuration
//  states, id_of_state, transitions, config = cppstate.helper.load_config()
//
//  active_state_transitions = [transition for transition in transitions if transition['from']==active_state]
//  state_helper = cppstate.helper.StateHelper(active_state, active_state_transitions)
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
//  cog.outl('StateId {}::getId()'.format(active_state))
//]]]
//[[[end]]]
{
    //[[[cog 
    //  cog.out("return ID_{};".format(active_state.upper()))
    //]]]
    //[[[end]]]
}

//[[[cog 
//  cog.outl('void {}::entry(StateId lastState)'.format(active_state))
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
//  cog.outl('void {}::update()'.format(active_state))
//]]]
//[[[end]]]
{
    // Insert state code here

    // TODO: Remove debug code
    //[[[cog 
    //  cog.outl('printf("update: {}\\n");'.format(active_state))
    //]]]
    //[[[end]]]

    processTransitions();
}

//[[[cog 
//  cog.outl('void {}::exit(StateId nextState)'.format(active_state))
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