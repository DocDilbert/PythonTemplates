//[[[cog 
//  import cog
//  import cppstate
//  
//  # load configuration
//  states, id_of_state, transitions = cppstate.helper.load_config()
//
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