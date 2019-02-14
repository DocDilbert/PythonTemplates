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
//[[[cog cog.out('#include "{}.h"'.format(config.typename_of_state_machine))]]]
//[[[end]]] 

//[[[cog ns_gen.generate_namespace_header()]]]
//[[[end]]]
int main()
{
    
    //[[[cog 
    //  cog.outl("{} stateMachine;".format(config.typename_of_state_machine))
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
