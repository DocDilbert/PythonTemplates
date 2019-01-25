//[[[cog 
//  import cog
//  import json
//  import cppstate
//  with open('config.json') as f:
//    config = json.load(f)
//  states = config['states']
//  states_ids = {state: 'ID_'+state.upper() for state in states}
//  transitions = config['transitions']
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