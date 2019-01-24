//[[[cog 
//  import cog
//  import json
//  import cppstate
//  with open('config.json') as f:
//    config = json.load(f)
//  states = config['states']
//  states_ids = {state: 'ID_'+state.upper() for state in states}
//  transitions = config['transitions']
//  state_transitions = [transition for transition in transitions if transition['from']==state_name]
//  state_obj = cppstate.state_class.StateClass(state_name, state_transitions)
//]]]
//[[[end]]]
#pragma once

#include "IState.h"
#include "IStateMachine.h"
 
//[[[cog 
//  cog.out("class {} : public IState".format(state_name))
//]]]
//[[[end]]] 
{
public:
    //[[[cog 
    //  # Constructor
    //  cog.out("{}(IStateMachine& stateMachine) : stateMachine(stateMachine)".format(state_name))
    //]]]
    //[[[end]]]
    {
    }

    void init()
    {
        // Insert init code here
    }

    StateId getId()
    {
        //[[[cog 
        //  cog.out("return ID_{};".format(state_name.upper()))
        //]]]
        //[[[end]]]
    }

    //[[[cog 
    //  state_obj.generate_state_checks()
    //  state_obj.generate_processTransitions()
    //]]]
    //[[[end]]]

    void entry(StateId lastState)
    {
    }

    void update()
    {
        processTransitions();
        // Insert state code here
    }

private:
    void setNextState(StateId state)
    {
        stateMachine.setNextState(state);
    }

    IStateMachine& stateMachine;
};

