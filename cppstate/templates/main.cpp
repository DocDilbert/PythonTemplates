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

#include <stdio.h>
//[[[cog cog.out('#include "{}.h"'.format(config.typename_of_state_machine))]]]
//[[[end]]] 

//[[[cog cog.out(ns_gen.generate_namespace_header())]]]
//[[[end]]]
int main()
{
    //[[[cog cog.outl("{} stateMachine;".format(config.typename_of_state_machine))]]]
    //[[[end]]]

    stateMachine.init();

    for (int i=0;i<5;i++)
    {
        printf("%i:\n",i);
        stateMachine.update();
    }
}

//[[[cog cog.out(ns_gen.generate_namespace_footer())]]]
//[[[end]]]

int main()
{
    //[[[cog 
    //  cog.outl("return {}::main();".format(ns_gen.get_main_namespace()))
    //]]]
    //[[[end]]]
}
