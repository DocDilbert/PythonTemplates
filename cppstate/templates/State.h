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
    /// Constructor
    //[[[cog 
    //  cog.out("{}(IStateMachine& stateMachine);".format(state_name));
    //]]]
    //[[[end]]]

    ///
    void init();

    ///
    StateId getId();

    //[[[cog 
    //  state_obj.generate_state_check_prototypes()
    //]]]
    //[[[end]]]
    ///
    void processTransitions();

    ///
    void entry(StateId lastState);
    
    ///
    void update();

private:
    ///
    void setNextState(StateId state);

    IStateMachine& stateMachine;
};

