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

//[[[cog 
//  ns_gen.generate_namespace_header_for_ids()
//]]]
//[[[end]]]

/// Enumerates all possible states
//[[[cog cog.outl("enum {}".format(config.typename_of_ids))]]]
//[[[end]]]
{
    //[[[cog cog.outl(",\n".join(config.id_of_state.values()))]]]
    //[[[end]]]
};

//[[[cog 
//  ns_gen.generate_namespace_footer_for_ids()
//]]]
//[[[end]]]