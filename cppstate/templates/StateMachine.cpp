//[[[cog 
//  import cog
//  import cppstate
//  
//  # load configuration
//  states, states_ids, transitions = cppstate.helper.load_config()
//
//]]]
//[[[end]]]
#include "StateMachine.h"

StateMachine::StateMachine() :
    //[[[cog 
    //  initializers = []
    //  initializers += ["istate(&{})".format(states[0].lower())]
    //  initializers += ["lastState(ID_{})".format(states[0].upper())]
    //  initializers += ["callEntry(true)"]
    //  initializers += ["{}(*this)".format(state_name.lower()) for state_name in states]
    //  cog.outl(",\n".join(initializers))
    //]]]
    //[[[end]]]
{
}

void StateMachine::init(StateData& stateData)
{
    //[[[cog 
    //  for state_name in states:
    //    cog.outl("{}.init(stateData);".format(state_name.lower()))
    //]]]
    //[[[end]]]
}

IState* StateMachine::getIStateFromId(StateId stateId)
{
    switch(stateId)
    {
        //[[[cog 
        //  last_state = states[-1]
        //  for state_name in states:
        //    sid = states_ids[state_name]
        //    cog.outl("case {}:".format(sid))
        //    cog.outl("{")
        //    cog.outl("    return &{};".format(state_name.lower()))
        //    cog.outl("}")
        //    if state_name != last_state:
        //      cog.outl()
        //]]]
        //[[[end]]]
    }
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

void StateMachine::setNextState(StateId state)
{
    // self transitions also call entry()
    callEntry = true;

    lastState = istate->getId();  
    istate = getIStateFromId(state);
}