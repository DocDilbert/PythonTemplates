//[[[cog 
//  import cog
//  import cppstate
//  
//  # load configuration
//  config = cppstate.helper.load_config()
//
//  ns_gen = cppstate.helper.NameSpaceGenerator("config.json")
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
//  for state in config.states:
//      cog.outl('#include "{}.h"'.format(state))
//]]]
//[[[end]]]

//[[[cog 
//  ns_gen.generate_namespace_header()
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
    //[[[cog 
    //  cog.outl("{0}::IState* getIStateFromId({1}::StateId stateId);".format(ns_gen.get_path_to_state(), ns_gen.get_path_to_id()))
    //]]]
    //[[[end]]]

    /// \copydoc IStateMachine::update
    //[[[cog 
    //  cog.outl("void setNextState({}::StateId state);".format(ns_gen.get_path_to_id()))
    //]]]
    //[[[end]]]

    /// Active state
    //[[[cog 
    //  cog.outl("{}::IState *istate;".format(ns_gen.get_path_to_state()))
    //]]]
    //[[[end]]]

    /// Id of the last active state
    //[[[cog 
    //  cog.outl("{}::StateId lastState;".format(ns_gen.get_path_to_id()))
    //]]]
    //[[[end]]]

    /// true when the entry method has to be called
    bool callEntry;
    //[[[cog 
    //  last_state = config.states[-1]
    //  for state in config.states:
    //    cog.outl("\n/// Concrete {} state object. This object implements the IState interface.".format(state))
    //    cog.outl("{}::{} {};".format(ns_gen.get_path_to_state(), state, state.lower()))
    //]]]
    //[[[end]]]
};

//[[[cog 
//  ns_gen.generate_namespace_footer()
//]]]
//[[[end]]]