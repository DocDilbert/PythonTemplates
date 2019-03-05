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

namespace Interfaces
{

/// Abstract interface to observer a statemachine
//[[[cog cog.outl("class {}".format(config.typename_of_observer))]]]
//[[[end]]]
{
public:
    /// The entry method is called by the statemachine the first time this state is executed.
    //[[[cog cog.outl("virtual void entry({}{} state) = 0;".format(ns_gen.get_namespace_to_id(), config.typename_of_ids))]]]
    //[[[end]]]
    
    /// The execute method is called by the statemachine everytime after the state was processed
    //[[[cog cog.outl("virtual void execute({}{} state) = 0;".format(ns_gen.get_namespace_to_id(), config.typename_of_ids))]]]
    //[[[end]]]

    /// The exit method is called by the statemachine before the state is left.
    //[[[cog cog.outl("virtual void exit({}{} state) = 0;".format(ns_gen.get_namespace_to_id(), config.typename_of_ids))]]]
    //[[[end]]]
};

}