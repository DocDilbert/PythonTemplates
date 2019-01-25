//[[[cog 
//  import cog
//  import json
//  import cppstate
//  with open('config.json') as f:
//    config = json.load(f)
//
//  states = config['states']
//  states_ids = {state: 'ID_'+state.upper() for state in states}
//  transitions = config['transitions']
//]]]
//[[[end]]]
#include "StateMachine.h"

StateMachine::StateMachine() :
    //[[[cog 
    //  last_state = states[-1]
    //  for state_name in states:
    //    cog.out("{}(*this)".format(state_name.lower()))
    //    if state_name != last_state:
    //      cog.outl(",")
    //]]]
    //[[[end]]]
{
}

void StateMachine::init()
{
    //[[[cog 
    //  for state_name in states:
    //    cog.outl("{}.init();".format(state_name.lower()))
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
    if (lastState!=UNDEFINED)
    {
        // only call entry once 
        istate->entry(lastState);
        lastState = UNDEFINED;
    }
    istate->update();
}

void StateMachine::setNextState(StateId state)
{
    // self transitions also call entry()
    lastState = istate->getId();  
    istate = getIStateFromId(state);
}