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
#include <stdio.h>
#include "StateMachine.h"

//[[[cog 
//  nameSpaceGenerator.generate_namespaces_header()
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
//  nameSpaceGenerator.generate_namespaces_footer()
//]]]
//[[[end]]]

int main()
{
    //[[[cog 
    //  cog.outl("return {}::main();".format(nameSpaceGenerator.get_path()))
    //]]]
    //[[[end]]]
}
