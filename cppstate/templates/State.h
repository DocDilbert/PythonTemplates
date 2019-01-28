//[[[cog 
//  import cog
//  import cppstate.helper
//  
//  # load configuration
//  states, id_of_state, transitions = cppstate.helper.load_config()
//
//  active_state_transitions = [transition for transition in transitions if transition['from']==active_state]
//  state_obj = cppstate.helper.Helper(active_state, active_state_transitions)
//]]]
//[[[end]]]
#pragma once

#include "IState.h"
#include "IStateMachine.h"
#include "StateData.h"

//[[[cog 
//  cog.out("class {} : public IState".format(active_state))
//]]]
//[[[end]]] 
{
public:
    /// Constructor
    //[[[cog 
    //  cog.out("{}(IStateMachine& stateMachine);".format(active_state));
    //]]]
    //[[[end]]]

    ///
    void init(StateData& stateData);

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
    //[[[cog 
    //   exitTos = ["// callback when exiting to {}\n void exitCallBackTo{}();\n".format(state, state) for state in states]
    //   cog.out("\n".join(exitTos))
    //]]]
    //[[[end]]]

    ///
    void setNextState(StateId state);

    StateData* stateData;
    IStateMachine& stateMachine;
};

