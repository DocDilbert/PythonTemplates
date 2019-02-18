import sys
import os, errno
import json
from cogapp import Cog
import argparse
from cppstate.config import load_config

def call_cog(infile, outfile, defines=None):
    
    options = []
    options+=['cog']
    options+=['-d']
    if defines:
        for name, value in defines.items():
            options+=['-D', '{}={}'.format(name,value)]

    options+=['-o',outfile]
    options+=[infile]
    cogapp = Cog()
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

    config = load_config(config_file)
        

    # Verzeichnisse erstellen
    try:
        os.makedirs("autogen")
        os.makedirs("autogen/"+config.namespace_of_ids.split('::')[-1])
        os.makedirs("autogen/"+config.namespace_of_states.split('::')[-1])
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    for active_state in config.states:
        call_cog(
            infile="templates/State.h",
            outfile= "autogen/{}/{}.h".format(config.namespace_of_states.split('::')[-1], active_state),
            defines={"active_state": active_state, "config_file":config_file},
        )
        call_cog(
            infile="templates/State.cpp",
            outfile= "autogen/{}/{}.cpp".format(config.namespace_of_states.split('::')[-1], active_state),
            defines={"active_state": active_state, "config_file":config_file},
        )
    call_cog(
        infile="templates/BaseState.h",
        outfile= "autogen/{}/{}.h".format(config.namespace_of_states.split('::')[-1], config.typename_of_base_state),
        defines={"config_file":config_file},
    )
    call_cog(
        infile="templates/BaseState.cpp",
        outfile= "autogen/{}/{}.cpp".format(config.namespace_of_states.split('::')[-1], config.typename_of_base_state),
        defines={"config_file":config_file},
    )
    call_cog(
        infile="templates/IState.h",
        outfile= "autogen/{}/{}.h".format(config.namespace_of_states.split('::')[-1], config.typename_of_state_interface),
        defines={"config_file":config_file},
    )
    call_cog(
        infile="templates/StateIds.h",
        outfile= "autogen/{}/{}.h".format(config.namespace_of_ids.split('::')[-1], config.typename_of_ids),
        defines={"config_file":config_file},
    )
    call_cog(
        infile="templates/IStateMachine.h",
        outfile= "autogen/{}.h".format(config.typename_of_state_machine_interface),
        defines={"config_file":config_file},
    )
    call_cog(
        infile="templates/StateMachine.h",
        outfile= "autogen/{}.h".format(config.typename_of_state_machine),
        defines={"config_file":config_file},
    )
    call_cog(
        infile="templates/StateMachine.cpp",
        outfile= "autogen/{}.cpp".format(config.typename_of_state_machine),
        defines={"config_file":config_file},
    )
    call_cog(
        infile="templates/main.cpp",
        outfile= "autogen/main.cpp",
        defines={"config_file":config_file},
    )
    call_cog(
        infile="templates/StateData.h",
        outfile= "autogen/{}.h".format(config.typename_of_state_data_structure),
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
