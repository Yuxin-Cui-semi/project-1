# """ This class represents a PowerTransformer
class PowerTransformer:

    def __init__(self, ID, name, equipment_container):      
        self.ID = ID
        self.name = name
        self.equipment_container = equipment_container
        self.type = 'CE'
        self.CE_type = 'Transformer'
        self.Num_attachTerms = 0
        
        self.terminal_list = []
    
    def add_terminal(self, new_terminal):
        self.terminal_list.append(new_terminal)
        self.Num_attachTerms += 1
