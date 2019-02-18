//[[[cog 
//  import cog
//  from cppstate.config import load_config
//  from cppstate.statehelper import StateHelper
//  from cppstate.namespacegenerator import NameSpaceGenerator
//  
//  # load configuration
//  config = load_config(config_file)
//  state_helper = StateHelper(active_state, config)
//  ns_gen = NameSpaceGenerator(config)
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

//[[[cog cog.out(ns_gen.generate_namespace_header_for_states())]]]
//[[[end]]]

/// Definition of a state class.
//[[[cog cog.out("class {} : public {}".format(active_state, config.typename_of_state_interface))]]]
//[[[end]]] 
{
public:
    /// Constructor
    //[[[cog cog.out("{}({}{}& stateMachine);".format(active_state, ns_gen.get_namespace_to_statemachine(), config.typename_of_state_machine_interface));]]]
    //[[[end]]]

    /// Init Method
    //[[[cog cog.out("void init({}{}& stateData);".format(ns_gen.get_namespace_to_statemachine(), config.typename_of_state_data_structure));]]]
    //[[[end]]]

    /// Returns the id of this state
    //[[[cog cog.outl("{}{} getId();".format(ns_gen.get_namespace_to_id(), config.typename_of_ids))]]]
    //[[[end]]]

    /// This method is called at the entry point of the state.
    /// \param lastState The id of the state from which the transition occured
    //[[[cog 
    //  cog.outl("void entry({}{} lastState) override;".format(ns_gen.get_namespace_to_id(),config.typename_of_ids))
    //]]]
    //[[[end]]]
    
    /// This method is called when the state is active.
    void execute() override;

    /// This method is called at the exit point of the state.
    /// \param nextState The id of the state to which the transition will lead
    //[[[cog cog.outl("void exit({}{} lastState) override;".format(ns_gen.get_namespace_to_id(), config.typename_of_ids))]]]
    //[[[end]]]

private:
    //[[[cog cog.out(state_helper.generate_state_check_prototypes())]]]
    //[[[end]]]
    /// This method processes all possible state transition checks from this state to other states.
    void processTransitions();

    /// A pointer to the StateData structure. This structure is a container for all
    /// references needed by each state.
    //[[[cog cog.out("{}{}* stateData; ".format(ns_gen.get_namespace_to_statemachine(),config.typename_of_state_data_structure));]]]
    //[[[end]]]

    /// A reference to the statemachine. Used to set the next state.
    //[[[cog cog.outl("{}{}& stateMachine;".format(ns_gen.get_namespace_to_statemachine(),config.typename_of_state_machine_interface, ns_gen.get_namespace_to_id(), config.typename_of_ids))]]]
    //[[[end]]]
};

//[[[cog cog.out(ns_gen.generate_namespace_footer_for_states())]]]
//[[[end]]]