class GeneratingUnit:

    def __init__(self, ID, name, maxP, minP, nomP, equipment_container):      
        self.ID = ID
        self.name = name
        self.maxP = maxP
        self.minP = minP
        self.nomP = nomP     
        self.equipment_container = equipment_container
        
        self.terminal_list = []
    
    def add_terminal(self, new_terminal):
        self.terminal_list.append(new_terminal)
   
       
