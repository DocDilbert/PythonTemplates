//[[[cog 
//  import cog
//  import cppstate
//  
//  # load configuration
//  config = cppstate.config.load_config(config_file)
//
//  ns_gen = cppstate.namespacegenerator.NameSpaceGenerator(config)
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
//[[[cog cog.out('struct {}'.format(config.typename_of_state_data_structure))]]]
//[[[end]]] 
{
    int dummy;
};

//[[[cog 
//  ns_gen.generate_namespace_footer()
//]]]
//[[[end]]]