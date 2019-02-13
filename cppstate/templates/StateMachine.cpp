//[[[cog 
//  import cog
//  import cppstate
//  
//  # load configuration
//  states, id_of_state, transitions = cppstate.helper.load_config()
//
//  nameSpaceGenerator = cppstate.helper.NameSpaceGenerator("config.json")
//]]]
//[[[end]]]
///
/// \file
/// \copyright Festo AG & Co. KG, Esslingen. All rights reserved.
/// \author TODO
///

#include "StateMachine.h"

//[[[cog 
//  nameSpaceGenerator.generate_namespace_header()
//]]]
//[[[end]]]

StateMachine::StateMachine() :
    //[[[cog 
    //  initializers = []
    //  initializers += ["istate(&{})".format(states[0].lower())]
    //  initializers += ["lastState({}::ID_{})".format(nameSpaceGenerator.get_path_to_state(), states[0].upper())]
    //  initializers += ["callEntry(true)"]
    //  initializers += ["{}(*this)".format(state.lower()) for state in states]
    //  cog.outl(",\n".join(initializers))
    //]]]
    //[[[end]]]
{
}

void StateMachine::init(StateData& stateData)
{
    //[[[cog 
    //  for state in states:
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
    istate->update();
}

//[[[cog 
//  cog.outl("{0}::IState* StateMachine::getIStateFromId({0}::StateId stateId)".format(nameSpaceGenerator.get_path_to_state()))
//]]]
//[[[end]]]
{
    switch(stateId)
    {
        //[[[cog 
        //  last_state = states[-1]
        //  for state in states:
        //    sid = id_of_state[state]
        //    cog.outl("case {}::{}:".format(nameSpaceGenerator.get_path_to_state(), sid))
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
//  cog.outl("void StateMachine::setNextState({}::StateId state)".format(nameSpaceGenerator.get_path_to_state()))
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
//  nameSpaceGenerator.generate_namespace_footer()
//]]]
//[[[end]]]