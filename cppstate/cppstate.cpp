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
//    cog.outl('class '+s+': public IState')
//    cog.outl('{')
//    cog.outl('public:')
//    cog.outl('  {}::{}(IStateMachine& statemachine)'.format(s, s))
//    cog.outl('  {')
//    cog.outl('    this->statemachine = statemachine;')
//    cog.outl('  }')
//    cog.outl()
//    cog.outl('  StateId getId()')
//    cog.outl('  {')
//    cog.outl('    return '+states_ids[s]+";")
//    cog.outl('  }')
//    cog.outl()
//    cog.outl('  void update()')
//    cog.outl('  {')
//    cog.outl('  	// Check for transitions here ...')
//    cog.outl('  }')
//    cog.outl()
//    cog.outl('  void setNextState(StateId state)')
//    cog.outl('  {')
//    cog.outl('  	// Insert transition logic here ...')
//    cog.outl()
//    cog.outl('  	context.setNexState(state)')
//    cog.outl('  }')
//    cog.outl()
//    cog.outl('private:')
//    cog.outl('  IStateMachine& statemachine;')
//    cog.outl('}')
//    cog.outl()
//]]]
//[[[end]]]
