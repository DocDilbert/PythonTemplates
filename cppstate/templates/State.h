//[[[cog 
//  import cog
//  import cppstate.helper
//  
//  # load configuration
//  config = cppstate.helper.load_config()
//
//  state_helper = cppstate.helper.StateHelper(active_state, config)
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
//  ns_gen.generate_namespace_header_for_states()
//]]]
//[[[end]]]

/// Definition of a state class.
//[[[cog 
//  cog.out("class {} : public IState".format(active_state))
//]]]
//[[[end]]] 
{
public:
    /// Constructor
    //[[[cog cog.out("{}({}::IStateMachine& stateMachine);".format(active_state, ns_gen.get_namespace()));]]]
    //[[[end]]]

    /// Init Method
    //[[[cog cog.out("void init({}::StateData& stateData);".format(ns_gen.get_namespace()));]]]
    //[[[end]]]

    /// Returns the id of this state
    //[[[cog cog.outl("{}::{} getId();".format(ns_gen.get_namespace_to_id(), config.typename_of_ids))]]]
    //[[[end]]]

    /// This method is called at the entry point of the state.
    /// \param lastState The id of the state from which the transition occured
    //[[[cog 
    //  cog.outl("void entry({}::{} lastState);".format(ns_gen.get_namespace_to_id(),config.typename_of_ids))
    //]]]
    //[[[end]]]
    
    /// This method is called when the state is active.
    void execute();

    /// This method is called at the exit point of the state.
    /// \param nextState The id of the state to which the transition will lead
    //[[[cog cog.outl("void exit({}::{} lastState);".format(ns_gen.get_namespace_to_id(), config.typename_of_ids))]]]
    //[[[end]]]

private:
    //[[[cog state_helper.generate_state_check_prototypes()]]]
    //[[[end]]]
    /// This method processes all possible state transition checks from this state to other states.
    void processTransitions();

    /// A pointer to the StateData structure. This structure is a container for all
    /// references needed by each state.
    //[[[cog cog.out("{}::StateData* stateData; ".format(ns_gen.get_namespace()));]]]
    //[[[end]]]

    /// A reference to the statemachine. Used to set the next state.
    //[[[cog cog.outl("{}::IStateMachine& stateMachine;".format(ns_gen.get_namespace(), ns_gen.get_namespace_to_id(), config.typename_of_ids))]]]
    //[[[end]]]
};

//[[[cog ns_gen.generate_namespace_footer_for_states()]]]
//[[[end]]]