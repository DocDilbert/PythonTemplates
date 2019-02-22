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
///[[[cog cog.out('/// Definition of class "{}"".'.format(config.typename_of_state_interface))]]]
///[[[end]]]
///

#pragma once

//[[[cog cog.outl('#include "{}.h"'.format(config.typename_of_ids))]]]
//[[[end]]]

//[[[cog cog.out(ns_gen.generate_namespace_header_for_states())]]]
//[[[end]]]

/// Abstract interface to a state
//[[[cog cog.outl("class {}".format(config.typename_of_state_interface))]]]
//[[[end]]]
{
public:
    /// This method returns the Id of the state
    //[[[cog cog.outl("virtual {}{} getId() = 0;".format(ns_gen.get_namespace_to_id(), config.typename_of_ids))]]]
    //[[[end]]]

    /// The entry method is called by the statemachine the first time this state is executed.
    //[[[cog cog.outl("virtual void entry({}{} lastState) = 0;".format(ns_gen.get_namespace_to_id(), config.typename_of_ids))]]]
    //[[[end]]]
    
    /// The execute method is called when the state is active.
    virtual void execute() = 0;

    /// The exit method is called by the statemachine the before the state is left.
    //[[[cog cog.outl("virtual void exit({}{} lastState) = 0;".format(ns_gen.get_namespace_to_id(), config.typename_of_ids))]]]
    //[[[end]]]

    /// The reset method is called by the state machine when it is reset to its init state.
    //[[[cog cog.outl("virtual void reset() = 0;".format())]]]
    //[[[end]]]
};

//[[[cog cog.out(ns_gen.generate_namespace_footer_for_states())]]]
//[[[end]]]