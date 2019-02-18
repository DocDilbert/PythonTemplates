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

#pragma once

//[[[cog 
//  ns_gen.generate_namespace_header_for_ids()
//]]]
//[[[end]]]

/// Enumerates all possible states
//[[[cog cog.outl("enum {}".format(config.typename_of_ids))]]]
//[[[end]]]
{
    //[[[cog cog.outl("{} = -1,".format(config.init_state_id))]]]
    //[[[end]]]
    //[[[cog cog.outl(",\n".join(config.id_of_state.values()))]]]
    //[[[end]]]
};

//[[[cog 
//  ns_gen.generate_namespace_footer_for_ids()
//]]]
//[[[end]]]