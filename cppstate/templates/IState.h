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

//[[[cog cog.outl('#include "{}.h"'.format(config.typename_of_ids))]]]
//[[[end]]]

//[[[cog ns_gen.generate_namespace_header_for_states()]]]
//[[[end]]]

/// Abstract interface to a state
class IState 
{
public:

    /// This method returns the Id of the state
    //[[[cog cog.outl("virtual {}::{} getId() = 0;".format(ns_gen.get_namespace_to_id(), config.typename_of_ids))]]]
    //[[[end]]]

    /// The entry method is called by the statemachine the first time this
    /// state is executed
    //[[[cog cog.outl("virtual void entry({}::{} lastState) = 0;".format(ns_gen.get_namespace_to_id(), config.typename_of_ids))]]]
    //[[[end]]]
    
    /// The execute method is called every time when the state is 
    /// active
    virtual void execute() = 0;

    /// The exit method is called by the statemachine the before the state is left.
    //[[[cog cog.outl("virtual void exit({}::{} lastState) = 0;".format(ns_gen.get_namespace_to_id(), config.typename_of_ids))]]]
    //[[[end]]]
};

//[[[cog ns_gen.generate_namespace_footer_for_states()]]]
//[[[end]]]