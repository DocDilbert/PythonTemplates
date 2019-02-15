import sys
import os, errno
import json
from cogapp import Cog
import argparse

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

def main():
    parser = argparse.ArgumentParser(description='cpp statemachine template generator')

    # positional arguments:
    parser.add_argument(
        'config_file', 
        metavar='config.py', 
        type=str, 
        help='filename of the config file'
    )

    args = parser.parse_args()
    config_file = args.config_file
    
    with open(config_file) as f:
        config = json.load(f)

    states = [state['name'] for state in config['states']]
    settings = config['settings']
    namespace_of_states = settings['namespace_of_states'].split("::")[-1]
    namespace_of_ids = settings['namespace_of_ids'].split("::")[-1]
    typename_of_ids = settings['typename_of_ids']
    typename_of_state_interface = settings['typename_of_state_interface']
    typename_of_state_machine_interface=settings['typename_of_state_machine_interface']
    typename_of_state_data_structure = settings['typename_of_state_data_structure']
    typename_of_state_machine = settings['typename_of_state_machine']
    
    # Verzeichnisse erstellen
    try:
        os.makedirs("autogen")
        os.makedirs("autogen/"+namespace_of_ids)
        os.makedirs("autogen/"+namespace_of_states)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    for active_state in states:
        call_cog(
            infile="templates/State.h",
            outfile= "autogen/{}/{}.h".format(namespace_of_states, active_state),
            defines={"active_state": active_state, "config_file":config_file},
        )
        call_cog(
            infile="templates/State.cpp",
            outfile= "autogen/{}/{}.cpp".format(namespace_of_states, active_state),
            defines={"active_state": active_state, "config_file":config_file},
        )

    call_cog(
        infile="templates/IState.h",
        outfile= "autogen/{}/{}.h".format(namespace_of_states, typename_of_state_interface),
        defines={"config_file":config_file},
    )
    call_cog(
        infile="templates/StateIds.h",
        outfile= "autogen/{}/{}.h".format(namespace_of_ids, typename_of_ids),
        defines={"config_file":config_file},
    )
    call_cog(
        infile="templates/IStateMachine.h",
        outfile= "autogen/{}.h".format(typename_of_state_machine_interface),
        defines={"config_file":config_file},
    )
    call_cog(
        infile="templates/StateMachine.h",
        outfile= "autogen/{}.h".format(typename_of_state_machine),
        defines={"config_file":config_file},
    )
    call_cog(
        infile="templates/StateMachine.cpp",
        outfile= "autogen/{}.cpp".format(typename_of_state_machine),
        defines={"config_file":config_file},
    )
    call_cog(
        infile="templates/main.cpp",
        outfile= "autogen/main.cpp",
        defines={"config_file":config_file},
    )
    call_cog(
        infile="templates/StateData.h",
        outfile= "autogen/{}.h".format(typename_of_state_data_structure),
        defines={"config_file":config_file},
    )
    call_cog(
        infile="templates/Makefile",
        outfile= "autogen/Makefile",
        defines={"config_file":config_file},
    )

    call_cog(
        infile="templates/StateMachine.wsd",
        outfile= "autogen/StateMachine.wsd",
        defines={"config_file":config_file},
    )

if __name__ == "__main__":
    main()
