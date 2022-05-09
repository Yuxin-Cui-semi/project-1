# """ This class represents a breaker
class Breaker:

    def __init__(self, ID, name, state, equipment_container, base_voltage):      
        self.ID = ID
        self.name = name
        self.state = state
        self.equipment_container = equipment_container
        self.base_voltage = base_voltage
        self.type = 'CE'
        self.CE_type = 'Breaker'
        self.Num_attachTerms = 0
        
        self.terminal_list = []
    
    def add_terminal(self, new_terminal):
        self.terminal_list.append(new_terminal)
        self.Num_attachTerms += 1

