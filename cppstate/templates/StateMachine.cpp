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
///[[[cog cog.out('/// Implementation of class "{}"".'.format(config.typename_of_state_machine))]]]
///[[[end]]]
///

//[[[cog cog.out('#include "{}.h"'.format(config.typename_of_state_machine))]]]
//[[[end]]] 

//[[[cog cog.out(ns_gen.generate_namespace_header())]]]
//[[[end]]]

//[[[cog cog.out('{0}::{0}() :'.format(config.typename_of_state_machine))]]]
//[[[end]]] 
    //[[[cog 
    //  initializers = []
    //  initializers += ["istate(&{})".format(config.init_state.lower())]
    //  initializers += ["lastState({}{})".format(ns_gen.get_namespace_to_id(), config.init_state_id)]
    //  initializers += ["callEntry(true)"]
    //  initializers += ["{}(*this)".format(state.lower()) for state in config.states]
    //  cog.outl(",\n".join(initializers))
    //]]]
    //[[[end]]]
{
}

//[[[cog cog.out('void {}::init()'.format(config.typename_of_state_machine))]]]
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
        //[[[cog 
        //  if config.is_observeable:
        //      cog.outl("notifyObserversOnEntry(lastState, istate->getId());\n")
        //]]]
        //[[[end]]]
        istate->entry(lastState);
        callEntry = false;
    }
    istate->execute();
    //[[[cog 
    //  if config.is_observeable:
    //      cog.outl("notifyObserversOnExecute(istate->getId());")
    //]]]
    //[[[end]]]
}

//[[[cog cog.out('void {}::reset()'.format(config.typename_of_state_machine))]]]
//[[[end]]] 
{
    istate->reset(); // perform reset of active state
    
    //[[[cog 
    //  cog.outl("istate = &{};".format(config.init_state.lower()))
    //  cog.outl('lastState = {}{};'.format(ns_gen.get_namespace_to_id(), config.init_state_id))
    //]]]
    //[[[end]]]   
    callEntry = true;  
}

//[[[cog cog.out('{}{} {}::getActiveStateId()'.format(ns_gen.get_namespace_to_id(), config.typename_of_ids,config.typename_of_state_machine))]]]
//[[[end]]] 
{
     return istate->getId();
}

//[[[cog
//  if config.is_observeable:
//      cog.outl("FMCReturnCode {}::registerObserver(Interfaces::{}& observer)".format(config.typename_of_state_machine, config.typename_of_observer))
//      cog.outl("{")
//      cog.outl("    if (!observers.isFull())")
//      cog.outl("    {")
//      cog.outl("        observers.add(&observer);")
//      cog.outl("        return RC_SUCCESS;")
//      cog.outl("    }")
//      cog.outl("    else")
//      cog.outl("    {")
//      cog.outl("        return RC_OUT_OF_MEMORY;")
//      cog.outl("    }")
//      cog.outl("}")
//]]]
//[[[end]]]

//[[[cog 
//  cog.outl("{}{}* {}::getIStateFromId({}{} stateId)".format(ns_gen.get_namespace_to_state(), config.typename_of_state_interface, config.typename_of_state_machine, ns_gen.get_namespace_to_id(), config.typename_of_ids))
//]]]
//[[[end]]]
{
    switch(stateId)
    {
        //[[[cog 
        //  last_state = config.states[-1]
        //  for state in config.states:
        //    sid = config.id_of_state[state]
        //    cog.outl("case {}{}:".format(ns_gen.get_namespace_to_id(), sid))
        //    cog.outl("{")
        //    cog.outl("    return &{};".format(state.lower()))
        //    cog.outl("}")
        //    if state != last_state:
        //      cog.outl()
        //]]]
        //[[[end]]]

        default:
        {
            return nullptr;
        }
    }
}

//[[[cog 
//  cog.outl("void {}::setNextState({}{} state)".format(config.typename_of_state_machine, ns_gen.get_namespace_to_id(), config.typename_of_ids))
//]]]
//[[[end]]]
{
    // self transitions also call entry()
    callEntry = true;
    istate->exit(state); // call exit method of state
    lastState = istate->getId();  
    //[[[cog 
    //  if config.is_observeable:
    //      cog.outl("notifyObserversOnExit(lastState, state);")
    //]]]
    //[[[end]]]
    istate = getIStateFromId(state);
}

//[[[cog 
//  if config.is_observeable:
//      cog.outl("void {0}::notifyObserversOnEntry({1}{2} from, {1}{2} to)".format(config.typename_of_state_machine, ns_gen.get_namespace_to_id(), config.typename_of_ids))
//      cog.outl("{")
//      cog.outl("    for(UINT32 i = 0; i < observers.getCount(); i++)")
//      cog.outl("    {")
//      cog.outl("        observers[i]->onEntry(from, to);")
//      cog.outl("    }")
//      cog.outl("}")
//      cog.outl()
//      cog.outl("void {0}::notifyObserversOnExecute({1}{2} state)".format(config.typename_of_state_machine, ns_gen.get_namespace_to_id(), config.typename_of_ids))
//      cog.outl("{")
//      cog.outl("    for(UINT32 i = 0; i < observers.getCount(); i++)")
//      cog.outl("    {")
//      cog.outl("        observers[i]->onExecute(state);")
//      cog.outl("    }")
//      cog.outl("}")
//      cog.outl()
//      cog.outl("void {0}::notifyObserversOnExit({1}{2} from, {1}{2} to)".format(config.typename_of_state_machine, ns_gen.get_namespace_to_id(), config.typename_of_ids))
//      cog.outl("{")
//      cog.outl("    for(UINT32 i = 0; i < observers.getCount(); i++)")
//      cog.outl("    {")
//      cog.outl("        observers[i]->onExit(from, to);")
//      cog.outl("    }")
//      cog.outl("}")
//]]]
//[[[end]]]

//[[[cog cog.out(ns_gen.generate_namespace_footer())]]]
//[[[end]]]