//[[[cog 
//  import cog
//  import cppstate.helper
//  
//  # load configuration
//  states, states_ids, transitions = cppstate.helper.load_config()
//
//  state_transitions = [transition for transition in transitions if transition['from']==state_name]
//  state_obj = cppstate.helper.Helper(state_name, state_transitions)
//]]]
//[[[end]]]
#include <stdio.h>
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
//  cog.outl('void {}::init(StateData& stateData)'.format(state_name))
//]]]
//[[[end]]]
{
    this->stateData = &stateData;

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
    // TODO: Debug code
    //[[[cog 
    //  cog.outl('printf("entry: {}\\n");'.format(state_name))
    //]]]
    //[[[end]]]
}

//[[[cog 
//  cog.outl('void {}::update()'.format(state_name))
//]]]
//[[[end]]]
{
    // Insert state code here

    // TODO: Debug code
    //[[[cog 
    //  cog.outl('printf("update: {}\\n");'.format(state_name))
    //]]]
    //[[[end]]]

    processTransitions();
}

//[[[cog 
//   exitTos = ["void {}::exitCallBackTo{}()\n{{\n    // insert callback code here\n    printf(\"exitCallBackTo{}()\\n\");\n}}\n".format(state_name, sname, sname) for sname in states]
//   cog.out("\n".join(exitTos))
//]]]
//[[[end]]]

//[[[cog 
//  cog.outl('void {}::setNextState(StateId state)'.format(state_name))
//]]]
//[[[end]]]
{
    switch(state)
    {
        //[[[cog 
        //   cases = []
        //   cases += ["case ID_{}:\n{{\n    exitCallBackTo{}();\n    break;\n}}".format(case.upper(), case) for case in states]
        //   cases += ["default:\n{\n    break;\n}"]
        //   cog.outl("\n".join(cases))
        //]]]
        //[[[end]]]
    }
    stateMachine.setNextState(state);
}