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
//  ns_gen.generate_namespace_header()
//]]]
//[[[end]]]

/// This struct is a container for all references which are
/// needed by the state machine.
struct StateData
{
    int dummy;
};

//[[[cog 
//  ns_gen.generate_namespace_footer()
//]]]
//[[[end]]]