import sys
import os, errno
import json
from cogapp import Cog

cogapp = Cog()
def call_cog(infile, outfile, defines=None):
    
    options = []
    options+=['cog']
    options+=['-d']
    if defines:
        for name, value in defines.items():
            options+=['-D', '{}={}'.format(name,value)]

    options+=['-o',outfile]
    options+=[infile]
    cogapp.callableMain(options)

try:
    os.makedirs("autogen")
except OSError as e:
    if e.errno != errno.EEXIST:
        raise


with open('config.json') as f:
    config = json.load(f)

states = config['states']
state_to_id = {state: 'ID_'+state.upper() for state in states}
transitions = config['transitions']
settings = config['settings']
states_namespace = settings['states_namespace']

try:
    os.makedirs("autogen/"+states_namespace)
except OSError as e:
    if e.errno != errno.EEXIST:
        raise

for active_state in states:
    call_cog(
        infile="templates/State.h",
        outfile= "autogen/{}/{}.h".format(states_namespace, active_state),
        defines={"active_state": active_state}
    )
    call_cog(
        infile="templates/State.cpp",
        outfile= "autogen/{}/{}.cpp".format(states_namespace, active_state),
        defines={"active_state": active_state}
    )

call_cog(
    infile="templates/IState.h",
    outfile= "autogen/IState.h",
)
call_cog(
    infile="templates/IStateMachine.h",
    outfile= "autogen/IStateMachine.h",
)
call_cog(
    infile="templates/StateMachine.h",
    outfile= "autogen/StateMachine.h"
)
call_cog(
    infile="templates/StateMachine.cpp",
    outfile= "autogen/StateMachine.cpp"
)
call_cog(
    infile="templates/main.cpp",
    outfile= "autogen/main.cpp"
)
call_cog(
    infile="templates/StateData.h",
    outfile= "autogen/StateData.h"
)
call_cog(
    infile="templates/Makefile",
    outfile= "autogen/Makefile"
)

call_cog(
    infile="templates/StateMachine.wsd",
    outfile= "autogen/StateMachine.wsd"
)