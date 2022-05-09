# """ This class represents a load act as energy consumer
class LinearShuntCompensator:

    def __init__(self, ID, name, b, g, equipment_container, voltage, q):      
        self.ID = ID
        self.name = name
        self.b = b
        self.g = g
        self.equipment_container = equipment_container
        self.voltage = voltage
        self.type = 'CE'
        self.CE_type = 'Compensator'
        self.Num_attachTerms = 0
        self.p = 0 # since it is a shunt compensator
        self.q = q
        
        self.terminal_list = []
    
    def add_terminal(self, new_terminal):
        self.terminal_list.append(new_terminal)
        self.Num_attachTerms += 1
       

