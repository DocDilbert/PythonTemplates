//[[[cog 
//  import cog
//  import cppstate
//  
//  # load configuration
//  states, id_of_state, transitions, config = cppstate.helper.load_config()
//
//  ns_gen = cppstate.helper.NameSpaceGenerator("config.json")
//]]]
//[[[end]]]
#include <stdio.h>
#include "StateMachine.h"

//[[[cog 
//  ns_gen.generate_namespace_header()
//]]]
//[[[end]]]
int main()
{
    StateMachine stateMachine;
    StateData stateData;

    stateMachine.init(stateData);

    for (int i=0;i<5;i++)
    {
        printf("%i:\n",i);
        stateMachine.update();
    }
}

//[[[cog 
//  ns_gen.generate_namespace_footer()
//]]]
//[[[end]]]

int main()
{
    //[[[cog 
    //  cog.outl("return {}::main();".format(ns_gen.get_path()))
    //]]]
    //[[[end]]]
}
