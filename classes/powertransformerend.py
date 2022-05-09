class PowerTransformerEnd:

    def __init__(self, ID, name, r, x, b, g, base_voltage, powertransformer_ID, terminal, end_number):      
        self.ID = ID
        self.name = name
        self.r = r
        self.x = x
        self.b = b
        self.g = g
        self.base_voltage = base_voltage
        self.powertransformer_ID = powertransformer_ID
        self.terminal = terminal
        self.end_number = end_number
       
        self.terminal_list = []
    
    def add_terminal(self, new_terminal):
        self.terminal_list.append(new_terminal)
       