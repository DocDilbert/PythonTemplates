import json

class Config:
    def __init__(self, parsed_json):
        state_list = [state for state in parsed_json['states']] 
        self.states = [state['name'] for state in state_list]
        self.state_ids = [state['id'] for state in state_list]
        self.id_of_state = {state: state_id for state, state_id in zip(self.states, self.state_ids)}
        self.init_state = parsed_json['init_transition']['to']
        self.init_state_id = parsed_json['init_transition']['id']
        self.transitions = parsed_json['transitions']

        settings = parsed_json['settings']
        
        self.namespace=settings['namespace']
        self.namespace_of_states=settings['namespace_of_states']
        self.namespace_of_ids=settings['namespace_of_ids']

        self.typename_of_ids = settings['typename_of_ids']
        self.typename_of_state_interface = settings['typename_of_state_interface']
        self.typename_of_state_machine_interface = settings['typename_of_state_machine_interface']
        self.typename_of_state_data_structure = settings['typename_of_state_data_structure']
        self.typename_of_state_machine = settings['typename_of_state_machine']

def load_config(filename):
    with open(filename) as f:
        config = json.load(f)
    
    return Config(config)

