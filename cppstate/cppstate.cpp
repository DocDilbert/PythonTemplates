//[[[cog 
//  import cog
//  import json
//  import cppstate
//  with open('config.json') as f:
//    config = json.load(f)
//  states = config['states']
//  states_ids = {state: 'ID_'+state.upper() for state in states}
//]]]
//[[[end]]]

enum StateId
{
  //[[[cog cog.outl("\n".join(states_ids.values())) ]]]
  //[[[end]]]
}

class IStateMachine
{
  public:
  	virtual void setNextState(StateId state) = 0;
}


class IState 
{
  public:
    virtual State getId() = 0;
    virtual void update() = 0;
}


//[[[cog 
//  for s in states:
//    state = cppstate.state_class.StateClass(s)
//    state.out()
//    cog.outl()
//]]]
//[[[end]]]