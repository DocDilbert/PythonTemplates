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

//[[[cog cog.out('#include "{}.h"'.format(config.typename_of_state_machine))]]]
//[[[end]]] 

//[[[cog 
//  ns_gen.generate_namespace_header()
//]]]
//[[[end]]]

//[[[cog cog.out('{0}::{0}() :'.format(config.typename_of_state_machine))]]]
//[[[end]]] 
    //[[[cog 
    //  initializers = []
    //  initializers += ["istate(&{})".format(config.states[0].lower())]
    //  initializers += ["lastState({}::{})".format(ns_gen.get_namespace_to_id(), config.init_state_id)]
    //  initializers += ["callEntry(true)"]
    //  initializers += ["{}(*this)".format(state.lower()) for state in config.states]
    //  cog.outl(",\n".join(initializers))
    //]]]
    //[[[end]]]
{
}

//[[[cog cog.out('void {}::init({}& stateData)'.format(config.typename_of_state_machine, config.typename_of_state_data_structure))]]]
//[[[end]]] 
{
    //[[[cog 
    //  for state in config.states:
    //    cog.outl("{}.init(stateData);".format(state.lower()))
    //]]]
    //[[[end]]]
    reset();
}
    

//[[[cog cog.out('void {}::update()'.format(config.typename_of_state_machine))]]]
//[[[end]]] 
{
    if (callEntry)
    {
        // only call entry once 
        istate->entry(lastState);
        callEntry = false;
    }
    istate->execute();
}

//[[[cog cog.out('void {}::reset()'.format(config.typename_of_state_machine))]]]
//[[[end]]] 
{
    //[[[cog 
    //  cog.outl("istate = &{};".format(config.states[0].lower()))
    //  cog.outl('lastState = {}::{};'.format(ns_gen.get_namespace_to_id(), config.init_state_id))
    //]]]
    //[[[end]]]   
    callEntry = true;  
}

//[[[cog 
//  cog.outl("{}{}* {}::getIStateFromId({}::{} stateId)".format(ns_gen.get_namespace_to_state(), config.typename_of_state_interface, config.typename_of_state_machine, ns_gen.get_namespace_to_id(), config.typename_of_ids))
//]]]
//[[[end]]]
{
    switch(stateId)
    {
        //[[[cog 
        //  last_state = config.states[-1]
        //  for state in config.states:
        //    sid = config.id_of_state[state]
        //    cog.outl("case {}::{}:".format(ns_gen.get_namespace_to_id(), sid))
        //    cog.outl("{")
        //    cog.outl("    return &{};".format(state.lower()))
        //    cog.outl("}")
        //    if state != last_state:
        //      cog.outl()
        //]]]
        //[[[end]]]
    }
}

//[[[cog 
//  cog.outl("void {}::setNextState({}::{} state)".format(config.typename_of_state_machine, ns_gen.get_namespace_to_id(), config.typename_of_ids))
//]]]
//[[[end]]]
{
    // self transitions also call entry()
    callEntry = true;
    istate->exit(state); // call exit method of state
    lastState = istate->getId();  
    istate = getIStateFromId(state);
}

//[[[cog 
//  ns_gen.generate_namespace_footer()
//]]]
//[[[end]]]