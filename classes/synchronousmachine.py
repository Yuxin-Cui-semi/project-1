class SynchronousMachine:

    def __init__(self, ID, name, p, q, rated_s, regulating_control, 
                 generating_unit, equipment_container, base_voltage):      
        self.ID = ID
        self.name = name
        self.p = p
        self.q = q
        self.rated_s = rated_s
        self.regulating_control = regulating_control
        self.generating_unit = generating_unit
        self.equipment_container = equipment_container
        self.base_voltage = base_voltage
        self.type = 'CE'
        self.CE_type = 'Generator'
        self.Num_attachTerms = 0
        
        self.terminal_list = []
    
    def add_terminal(self, new_terminal):
        self.terminal_list.append(new_terminal)
        self.Num_attachTerms += 1
