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

#pragma once

#include "IState.h"
#include "IStateMachine.h"
#include "StateData.h"
//[[[cog 
//  for state in states:
//      cog.outl('#include "{}.h"'.format(state))
//]]]
//[[[end]]]

//[[[cog 
//  nameSpaceGenerator.generate_namespace_header()
//]]]
//[[[end]]]

/// A generic state machine implementation
class StateMachine : public IStateMachine
{
public:
    /// Constructor
    StateMachine();

    /// This method initializes the state machine
    /// \param stateData data structure used by all states
    void init(StateData& stateData);

    /// Cyclic update method of the state machine
    void update();

private:
    /// Returns a pointer to an object which implements the IState interface. 
    /// \param stateId id of the requested state 
    /// \returns a pointer to an object which implements the IState interface. 
    IState* getIStateFromId(StateId stateId);

    /// \copydoc IStateMachine::update
    void setNextState(StateId state);

    /// Active state
    IState *istate;

    /// Id of the last active state
    StateId lastState;

    /// true when the entry method has to be called
    bool callEntry;
    //[[[cog 
    //  last_state = states[-1]
    //  for state in states:
    //    cog.outl("\n/// Concrete {} state object. This object implements the IState interface.".format(state))
    //    cog.outl("{}::{} {};".format(nameSpaceGenerator.get_path_to_state(), state, state.lower()))
    //]]]
    //[[[end]]]
};

//[[[cog 
//  nameSpaceGenerator.generate_namespace_footer()
//]]]
//[[[end]]]