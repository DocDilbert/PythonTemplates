import sys
import os, errno
import json
from cogapp import Cog

global testvar
testvar = "HALLO"
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

for state_name in states:
    call_cog(
        infile="templates/State.h",
        outfile= "autogen/{}.h".format(state_name),
        defines={"state_name": state_name}
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
    infile="templates/main.cpp",
    outfile= "autogen/main.cpp"
)