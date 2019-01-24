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
#include "IState.h"
#include "IStateMachine.h"

class StateMachine : public IStateMachine
{
public:
    IState* getIStateFromId(StateId stateId)
    {
        //[[[cog 
        //  last_state = states[-1]
        //  for state_name in states:
        //    sid = states_ids[state_name]
        //    cog.outl("case {}:".format(sid))
        //    cog.outl("{")
        //    cog.outl("    return &{};".format(state_name.lower()))
        //    cog.outl("}")
        //    if state_name != last_state:
        //      cog.outl()
        //]]]
        //[[[end]]]
    }

    void update()
    {
        if (callEntry)
        {
          // only call entry once 
          istate->entry();
          callEntry = false;
        }
        istate->update();
    }

    void setNextState(StateId state)
    {
      this.istate = getIStateFromId(state);
      this.callEntry = true; // self transitions also call entry()
    }

private:
    StateId state;
    IState *istate;
    BOOL callEntry;

    //[[[cog 
    //  last_state = states[-1]
    //  for state_name in states:
    //    cog.outl("{} {};".format(state_name, state_name.lower()))
    //]]]
    //[[[end]]]
}