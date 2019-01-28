//[[[cog 
//  import cog
//  import cppstate.helper
//  
//  # load configuration
//  states, id_of_state, transitions = cppstate.helper.load_config()
//
//  active_state_transitions = [transition for transition in transitions if transition['from']==active_state]
//  state_obj = cppstate.helper.Helper(active_state, active_state_transitions)
//]]]
//[[[end]]]
#include <stdio.h>
//[[[cog 
//  cog.outl('#include "{}.h"'.format(active_state))
//]]]
//[[[end]]]


//[[[cog 
//  # Constructor
//  cog.out("{}::{}(IStateMachine& stateMachine) : stateMachine(stateMachine)".format(active_state, active_state))
//]]]
//[[[end]]]
{
}

//[[[cog 
//  cog.outl('void {}::init(StateData& stateData)'.format(active_state))
//]]]
//[[[end]]]
{
    this->stateData = &stateData;

    // Insert init code here
}

//[[[cog 
//  cog.outl('StateId {}::getId()'.format(active_state))
//]]]
//[[[end]]]
{
    //[[[cog 
    //  cog.out("return ID_{};".format(active_state.upper()))
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
//  cog.outl('void {}::entry(StateId lastState)'.format(active_state))
//]]]
//[[[end]]]
{
    // TODO: Debug code
    //[[[cog 
    //  cog.outl('printf("entry: {}\\n");'.format(active_state))
    //]]]
    //[[[end]]]
}

//[[[cog 
//  cog.outl('void {}::update()'.format(active_state))
//]]]
//[[[end]]]
{
    // Insert state code here

    // TODO: Debug code
    //[[[cog 
    //  cog.outl('printf("update: {}\\n");'.format(active_state))
    //]]]
    //[[[end]]]

    processTransitions();
}

//[[[cog 
//   exitTos = ["void {}::exitCallBackTo{}()\n{{\n    // insert callback code here\n    printf(\"exitCallBackTo{}()\\n\");\n}}\n".format(active_state, sname, sname) for sname in states]
//   cog.out("\n".join(exitTos))
//]]]
//[[[end]]]

//[[[cog 
//  cog.outl('void {}::setNextState(StateId state)'.format(active_state))
//]]]
//[[[end]]]
{
    switch(state)
    {
        //[[[cog 
        //   cases = []
        //   cases += ["case ID_{}:\n{{\n    exitCallBackTo{}();\n    break;\n}}".format(state.upper(), state) for state in states]
        //   cases += ["default:\n{\n    break;\n}"]
        //   cog.outl("\n".join(cases))
        //]]]
        //[[[end]]]
    }
    stateMachine.setNextState(state);
}