//[[[cog 
//  import cog
//  import cppstate
//  
//  # load configuration
//  states, states_ids, transitions = cppstate.helper.load_config()
//
//]]]
//[[[end]]]
#include <stdio.h>
#include "StateMachine.h"

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