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
#include <stdio.h>
#include "StateMachine.h"

//[[[cog 
//  ns_gen.generate_namespace_header()
//]]]
//[[[end]]]
int main()
{
    StateMachine stateMachine;
    //[[[cog 
    //  cog.outl("{} stateData;".format(config.typename_of_state_data_structure))
    //]]]
    //[[[end]]]
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
    //  cog.outl("return {}::main();".format(ns_gen.get_main_namespace()))
    //]]]
    //[[[end]]]
}
