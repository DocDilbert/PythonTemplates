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
#pragma once

#include "IState.h"
#include "IStateMachine.h"
#include "StateData.h"
//[[[cog 
//  for state_name in states:
//      cog.outl('#include "{}.h"'.format(state_name))
//]]]
//[[[end]]]

class StateMachine : public IStateMachine
{
public:
    ///
    StateMachine();

    ///
    void init(StateData& stateData);

    ///
    IState* getIStateFromId(StateId stateId);

    ///
    void update();

    ///
    void setNextState(StateId state);

private:
    IState *istate;
    StateId lastState;
    bool callEntry;

    //[[[cog 
    //  last_state = states[-1]
    //  for state_name in states:
    //    cog.outl("{} {};".format(state_name, state_name.lower()))
    //]]]
    //[[[end]]]
};