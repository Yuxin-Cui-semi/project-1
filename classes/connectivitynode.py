# """ This class represents the connectivity node (abstract)
class ConnectivityNode:

    def __init__(self, ID, name, nodecontainer, base_voltage):      
        self.ID = ID
        self.name = name
        self.nodecontainer = nodecontainer
        self.terminal_list = []
        self.type = 'CN'
        self.Num_attachTerms = 0
        self.CE_type = 'NA'
        self.base_voltage = base_voltage
        self.bus = ''
    
    def add_terminal(self, new_terminal):
        self.terminal_list.append(new_terminal)
        self.Num_attachTerms += 1
        