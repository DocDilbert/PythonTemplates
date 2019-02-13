//[[[cog 
//  import cog
//  import cppstate
//  
//  # load configuration
//  states, id_of_state, transitions = cppstate.helper.load_config()
//
//  nameSpaceGenerator = cppstate.helper.NameSpaceGenerator("config.json")
//]]]
//[[[end]]]
///
/// \file
/// \copyright Festo AG & Co. KG, Esslingen. All rights reserved.
/// \author TODO
///

#pragma once

//[[[cog 
//  nameSpaceGenerator.generate_namespace_header_for_states()
//]]]
//[[[end]]]

/// Enumerates all possible states
enum StateId
{
    //[[[cog cog.outl(",\n".join(id_of_state.values()))]]]
    //[[[end]]]
};

/// Abstract interface to a state
class IState 
{
public:

    /// This method returns the Id of the state
    virtual StateId getId() = 0;

    /// The entry method is called by the statemachine the first time this
    /// state is executed
    virtual void entry(StateId lastState) = 0;

    /// The update method is called every time when the state is 
    /// active
    virtual void update() = 0;

    /// The exit method is called by the statemachine the before the state is left.
    virtual void exit(StateId lastState) = 0;

};

//[[[cog 
//  nameSpaceGenerator.generate_namespace_footer_for_states()
//]]]
//[[[end]]]