//[[[cog 
//  import cog
//  import cppstate.helper
//  
//  # load configuration
//  states, states_ids, transitions = cppstate.helper.load_config()
//
//  state_transitions = [transition for transition in transitions if transition['from']==state_name]
//  state_obj = cppstate.helper.Helper(state_name, state_transitions)
//]]]
//[[[end]]]
#pragma once

#include "IState.h"
#include "IStateMachine.h"
#include "StateData.h"

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
    //   exitTos = ["// callback when exiting to {}\n void exitCallBackTo{}();\n".format(sname, sname) for sname in states]
    //   cog.out("\n".join(exitTos))
    //]]]
    //[[[end]]]

    ///
    void setNextState(StateId state);

    StateData* stateData;
    IStateMachine& stateMachine;
};

