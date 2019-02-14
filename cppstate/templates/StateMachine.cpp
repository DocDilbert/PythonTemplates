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

#include "StateMachine.h"

//[[[cog 
//  ns_gen.generate_namespace_header()
//]]]
//[[[end]]]

StateMachine::StateMachine() :
    //[[[cog 
    //  initializers = []
    //  initializers += ["istate(&{})".format(config.states[0].lower())]
    //  initializers += ["lastState({}::{})".format(ns_gen.get_path_to_id(), config.init_state_id)]
    //  initializers += ["callEntry(true)"]
    //  initializers += ["{}(*this)".format(state.lower()) for state in config.states]
    //  cog.outl(",\n".join(initializers))
    //]]]
    //[[[end]]]
{
}

void StateMachine::init(StateData& stateData)
{
    //[[[cog 
    //  for state in config.states:
    //    cog.outl("{}.init(stateData);".format(state.lower()))
    //]]]
    //[[[end]]]
}
    
void StateMachine::update()
{
    if (callEntry)
    {
        // only call entry once 
        istate->entry(lastState);
        callEntry = false;
    }
    istate->execute();
}

//[[[cog 
//  cog.outl("{0}::IState* StateMachine::getIStateFromId({1}::StateId stateId)".format(ns_gen.get_path_to_state(), ns_gen.get_path_to_id()))
//]]]
//[[[end]]]
{
    switch(stateId)
    {
        //[[[cog 
        //  last_state = config.states[-1]
        //  for state in config.states:
        //    sid = config.id_of_state[state]
        //    cog.outl("case {}::{}:".format(ns_gen.get_path_to_id(), sid))
        //    cog.outl("{")
        //    cog.outl("    return &{};".format(state.lower()))
        //    cog.outl("}")
        //    if state != last_state:
        //      cog.outl()
        //]]]
        //[[[end]]]
    }
}

//[[[cog 
//  cog.outl("void StateMachine::setNextState({}::StateId state)".format(ns_gen.get_path_to_id()))
//]]]
//[[[end]]]
{
    // self transitions also call entry()
    callEntry = true;
    istate->exit(state); // call exit method of state
    lastState = istate->getId();  
    istate = getIStateFromId(state);
}

//[[[cog 
//  ns_gen.generate_namespace_footer()
//]]]
//[[[end]]]