//[[[cog 
//  import cog
//  from cppstate.config import load_config
//  from cppstate.statehelper import StateHelper
//  from cppstate.namespacegenerator import NameSpaceGenerator
//  
//  # load configuration
//  config = load_config(config_file)
//
//  ns_gen = NameSpaceGenerator(config)
//]]]
//[[[end]]]
///
/// \file
/// \copyright Festo AG & Co. KG, Esslingen. All rights reserved.
/// \author TODO
///
///[[[cog cog.out('/// Definition of class "{}"".'.format(config.typename_of_state_machine))]]]
///[[[end]]] 
///

#pragma once

#include "FMCTypes.h"
#include "FMCReturnCodes.h"
//[[[cog cog.out('#include "{}.h"'.format(config.typename_of_state_interface))]]]
//[[[end]]] 
//[[[cog cog.out('#include "{}.h"'.format(config.typename_of_state_machine_interface))]]]
//[[[end]]] 
//[[[cog cog.out('#include "{}.h"'.format(config.typename_of_state_data_structure))]]]
//[[[end]]] 
//[[[cog 
//  if config.is_observeable:
//      cog.out('#include "{}.h"\n'.format(config.typename_of_observer))
//      cog.out('#include "List.h"')
//]]]
//[[[end]]] 
//[[[cog 
//  for state in config.states:
//      cog.outl('#include "{}.h"'.format(state))
//]]]
//[[[end]]]

//[[[cog cog.out(ns_gen.generate_namespace_header())]]]
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
    //[[[cog cog.out('void init();'.format())]]]
    //[[[end]]] 

    /// Cyclic update method of the state machine
    void update();

    /// This method resets the statemachine to its init state and init transition
    void reset();

    /// Id of the currently active state
    //[[[cog cog.outl("{}{} getActiveStateId();".format(ns_gen.get_namespace_to_id(), config.typename_of_ids))]]]
    //[[[end]]]
    //[[[cog 
    //  if config.is_observeable:
    //      cog.outl("\n/// Registers an observer to the statemachine.")
    //      cog.outl("/// \\retval RC_SUCCESS if the registration was successfull.")
    //      cog.outl("/// \\retval RC_OUT_OF_MEMORY if the registration failed.")
    //      cog.outl("FMCReturnCode registerObserver(Interfaces::{}& observer);".format(config.typename_of_observer))
    //]]]
    //[[[end]]]
private:
    /// Returns a pointer to an object which implements the IState interface. 
    /// \param stateId id of the requested state 
    /// \returns a pointer to an object which implements the IState interface. 
    ///          If the stateId is unknown a nullptr is returned. 
    //[[[cog cog.outl("{}{}* getIStateFromId({}{} stateId);".format(ns_gen.get_namespace_to_state(),config.typename_of_state_interface, ns_gen.get_namespace_to_id(), config.typename_of_ids))]]]
    //[[[end]]]

    /// \copydoc IStateMachine::setNextState
    //[[[cog cog.outl("void setNextState({}{} state) override;".format(ns_gen.get_namespace_to_id(), config.typename_of_ids))]]]
    //[[[end]]]

    /// Active state
    //[[[cog cog.outl("{}{} *istate;".format(ns_gen.get_namespace_to_state(), config.typename_of_state_interface))]]]
    //[[[end]]]

    /// Id of the last active state
    //[[[cog cog.outl("{}{} lastState;".format(ns_gen.get_namespace_to_id(), config.typename_of_ids))]]]
    //[[[end]]]

    /// true when the entry method has to be called
    BOOL callEntry;
    
    // Container where state data is stored.
    //[[[cog cog.out('{} stateData;'.format(config.typename_of_state_data_structure))]]]
    //[[[end]]]
    //[[[cog 
    //  last_state = config.states[-1]
    //  for state in config.states:
    //    cog.outl("\n/// Concrete {} state object. This object implements the IState interface.".format(state))
    //    cog.outl("{}{} {};".format(ns_gen.get_namespace_to_state(), state, state.lower()))
    //]]]
    //[[[end]]]
    //[[[cog 
    //  if config.is_observeable:
    //      cog.outl()
    //      cog.outl("/// Number of maximal subscribable observers")
    //      cog.outl("constexpr static const UINT32 MAX_OBSERVERS = 2;\n")
    //      cog.outl("/// holds subscribers who want to be informed about state changes")
    //      cog.outl("Utilities::List<Interfaces::{}*, MAX_OBSERVERS> observers;".format(config.typename_of_observer))
    //      cog.outl()
    //      cog.outl("/// Notifies all observer that the entry method was called")
    //      cog.outl("void notifyObserversOnEntry({0}{1} from, {0}{1} to);".format(ns_gen.get_namespace_to_id(), config.typename_of_ids))
    //      cog.outl()
    //      cog.outl("/// Notifies all observer that the execute method was called")
    //      cog.outl("void notifyObserversOnExecute({}{} state);".format(ns_gen.get_namespace_to_id(), config.typename_of_ids))
    //      cog.outl()
    //      cog.outl("/// Notifies all observer that the exit method was called")
    //      cog.outl("void notifyObserversOnExit({0}{1} from, {0}{1} to);".format(ns_gen.get_namespace_to_id(), config.typename_of_ids))
    //]]]
    //[[[end]]]
};
//[[[cog cog.out(ns_gen.generate_namespace_footer())]]]
//[[[end]]]