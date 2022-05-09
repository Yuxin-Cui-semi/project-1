# """ This class represents a AC Line
class ACLineSegment:

    def __init__(self, ID, name, equipment_container, r, x, bch, length, gch, 
                 base_voltage):      
        self.ID = ID
        self.name = name
        self.equipment_container = equipment_container
        self.r = r
        self.x = x
        self.bch = bch
        self.length = length
        self.gch = gch
        self.base_voltage = base_voltage
        self.type = 'CE'
        self.CE_type = 'Line'
        self.Num_attachTerms = 0
        
        self.terminal_list = []
    
    def add_terminal(self, new_terminal):
        self.terminal_list.append(new_terminal)
        self.Num_attachTerms += 1        
       
