//[[[cog 
//  import cog
//  import json
//  import cppstate
//  with open('config.json') as f:
//    config = json.load(f)
//
//  states = config['states']
//  states_ids = {state: 'ID_'+state.upper() for state in states}
//  transitions = config['transitions']
//]]]
//[[[end]]]
#pragma once

enum StateId
{
    UNDEFINED,
    //[[[cog cog.outl(",\n".join(states_ids.values()))]]]
    //[[[end]]]
};

class IState 
{
public:

    /// This method returns the Id of the state
    virtual StateId getId() = 0;

    /// The entry method is called by statemachine the first time this
    /// state is executed
    virtual void entry(StateId lastState) = 0;

    /// The update method is called every time when the state is 
    /// active
    virtual void update() = 0;
};