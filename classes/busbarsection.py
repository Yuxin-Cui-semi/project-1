# """ This class represents a busbar
class BusbarSection:

    def __init__(self, ID, name, equipment_container, base_voltage ):      
        self.ID = ID
        self.name = name
        self.equipment_container = equipment_container
        self.base_voltage = base_voltage
        self.type = 'CE'
        self.CE_type = 'Bus'
        self.Num_attachTerms = 0
        self.bus = ''
        
        self.terminal_list = []
    
    def add_terminal(self, new_terminal):
        self.terminal_list.append(new_terminal)
        self.Num_attachTerms += 1
       
