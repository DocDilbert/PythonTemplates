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

states = [state['name'] for state in config['states']]
state_to_id = {state: 'ID_'+state.upper() for state in states}
transitions = config['transitions']
settings = config['settings']
namespace_of_states = settings['namespace_of_states'].split("::")[-1]
namespace_of_ids = settings['namespace_of_ids'].split("::")[-1]
typename_of_ids = settings['typename_of_ids']
typename_of_state_interface = settings['typename_of_state_interface']
typename_of_state_machine_interface=settings['typename_of_state_machine_interface']

try:
    os.makedirs("autogen/"+namespace_of_states)
except OSError as e:
    if e.errno != errno.EEXIST:
        raise

try:
    os.makedirs("autogen/"+namespace_of_ids)
except OSError as e:
    if e.errno != errno.EEXIST:
        raise

for active_state in states:
    call_cog(
        infile="templates/State.h",
        outfile= "autogen/{}/{}.h".format(namespace_of_states, active_state),
        defines={"active_state": active_state}
    )
    call_cog(
        infile="templates/State.cpp",
        outfile= "autogen/{}/{}.cpp".format(namespace_of_states, active_state),
        defines={"active_state": active_state}
    )

call_cog(
    infile="templates/IState.h",
    outfile= "autogen/{}/{}.h".format(namespace_of_states, typename_of_state_interface),
)
call_cog(
    infile="templates/StateIds.h",
    outfile= "autogen/{}/{}.h".format(namespace_of_ids, typename_of_ids),
)
call_cog(
    infile="templates/IStateMachine.h",
    outfile= "autogen/{}.h".format(typename_of_state_machine_interface),
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