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

//[[[cog cog.out('#include "{}.h"'.format(config.typename_of_state_interface))]]]
//[[[end]]] 
//[[[cog cog.out('#include "{}.h"'.format(config.typename_of_state_machine_interface))]]]
//[[[end]]] 
//[[[cog cog.out('#include "{}.h"'.format(config.typename_of_state_data_structure))]]]
//[[[end]]] 
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
//[[[cog cog.out('class {} : public {}'.format(config.typename_of_state_machine, config.typename_of_state_machine_interface))]]]
//[[[end]]] 
{
public:
    /// Constructor
    //[[[cog cog.out('{}();'.format(config.typename_of_state_machine))]]]
    //[[[end]]] 

    /// This method initializes the state machine
    /// \param stateData data structure used by all states
    //[[[cog cog.out('void init({}& stateData);'.format(config.typename_of_state_data_structure))]]]
    //[[[end]]] 

    /// Cyclic update method of the state machine
    void update();

    /// This method resets the statemachine to its init state and init transition
    void reset();
    
private:
    /// Returns a pointer to an object which implements the IState interface. 
    /// \param stateId id of the requested state 
    /// \returns a pointer to an object which implements the IState interface. 
    //[[[cog 
    //  cog.outl("{}{}* getIStateFromId({}::{} stateId);".format(ns_gen.get_namespace_to_state(),config.typename_of_state_interface, ns_gen.get_namespace_to_id(), config.typename_of_ids))
    //]]]
    //[[[end]]]

    /// \copydoc IStateMachine::update
    //[[[cog 
    //  cog.outl("void setNextState({}::{} state) override;".format(ns_gen.get_namespace_to_id(), config.typename_of_ids))
    //]]]
    //[[[end]]]

    /// Active state
    //[[[cog 
    //  cog.outl("{}{} *istate;".format(ns_gen.get_namespace_to_state(), config.typename_of_state_interface))
    //]]]
    //[[[end]]]

    /// Id of the last active state
    //[[[cog 
    //  cog.outl("{}::{} lastState;".format(ns_gen.get_namespace_to_id(), config.typename_of_ids))
    //]]]
    //[[[end]]]

    /// true when the entry method has to be called
    bool callEntry;
    //[[[cog 
    //  last_state = config.states[-1]
    //  for state in config.states:
    //    cog.outl("\n/// Concrete {} state object. This object implements the IState interface.".format(state))
    //    cog.outl("{}{} {};".format(ns_gen.get_namespace_to_state(), state, state.lower()))
    //]]]
    //[[[end]]]
};

//[[[cog 
//  ns_gen.generate_namespace_footer()
//]]]
//[[[end]]]