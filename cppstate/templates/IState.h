//[[[cog 
//  import cog
//  import cppstate
//  
//  # load configuration
//  states, id_of_state, transitions = cppstate.helper.load_config()
//
//]]]
//[[[end]]]
#pragma once

enum StateId
{
    //[[[cog cog.outl(",\n".join(id_of_state.values()))]]]
    //[[[end]]]
};

class IState 
{
public:

    /// This method returns the Id of the state
    virtual StateId getId() = 0;

    /// The entry method is called by the statemachine the first time this
    /// state is executed
    virtual void entry(StateId lastState) = 0;

    /// The exit method is called by the statemachine the before the state is left.
    virtual void exit(StateId lastState) = 0;

    /// The update method is called every time when the state is 
    /// active
    virtual void update() = 0;
};