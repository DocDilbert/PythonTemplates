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

/// Definition of a state class
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

    /// Constructor
    void init(StateData& stateData);

    /// Returns the id of this state
    StateId getId();

    /// This method is called at the entry point of the state
    /// \param lastState The id of the state from which the transition occured
    void entry(StateId lastState);
    
    /// This method is called when the state is active
    void update();

    /// This method is called at the exit point of the state
    /// \param nextState The id of the state to which the transition will lead
    void exit(StateId nextState);

private:
    //[[[cog 
    //  state_obj.generate_state_check_prototypes()
    //]]]
    //[[[end]]]
    /// This method processes all possible state transition checks from this state to other states
    void processTransitions();

    /// A pointer to the StateData structure. This structure is a container for all
    /// references needed by each state.
    StateData* stateData; 

    /// A reference to the statemachine. Used to set the next state
    IStateMachine& stateMachine;
};

