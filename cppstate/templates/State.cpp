//[[[cog 
//  import cog
//  import json
//  import cppstate
//  with open('config.json') as f:
//    config = json.load(f)
//  states = config['states']
//  states_ids = {state: 'ID_'+state.upper() for state in states}
//  transitions = config['transitions']
//  state_transitions = [transition for transition in transitions if transition['from']==state_name]
//  state_obj = cppstate.state_class.StateClass(state_name, state_transitions)
//]]]
//[[[end]]]
//[[[cog 
//  cog.outl('#include "{}.h"'.format(state_name))
//]]]
//[[[end]]]


//[[[cog 
//  # Constructor
//  cog.out("{}::{}(IStateMachine& stateMachine) : stateMachine(stateMachine)".format(state_name, state_name))
//]]]
//[[[end]]]
{
}

//[[[cog 
//  cog.outl('void {}::init()'.format(state_name))
//]]]
//[[[end]]]
{
    // Insert init code here
}

//[[[cog 
//  cog.outl('StateId {}::getId()'.format(state_name))
//]]]
//[[[end]]]
{
    //[[[cog 
    //  cog.out("return ID_{};".format(state_name.upper()))
    //]]]
    //[[[end]]]
}

//[[[cog 
//  state_obj.generate_state_checks()
//]]]
//[[[end]]]
//[[[cog 
//  state_obj.generate_processTransitions()
//]]]
//[[[end]]]

//[[[cog 
//  cog.outl('void {}::entry(StateId lastState)'.format(state_name))
//]]]
//[[[end]]]
{
}

//[[[cog 
//  cog.outl('void {}::update()'.format(state_name))
//]]]
//[[[end]]]
{
    processTransitions();
    // Insert state code here
}

//[[[cog 
//  cog.outl('void {}::setNextState(StateId state)'.format(state_name))
//]]]
//[[[end]]]
{
    stateMachine.setNextState(state);
}