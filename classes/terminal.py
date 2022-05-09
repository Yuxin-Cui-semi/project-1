class Terminal:

    def __init__(self, ID, name, CE, CN):      
        self.ID = ID
        self.name = name
        self.CE = CE
        self.CN = CN
        self.type = 'TE'
        self.traversal_flag = 0
        # the attribute called 'traversal_flag' to every terminal with the initial
        # value at zero ('An Efficient Method for Extracting Network
        # Information from the CIM Asset Model')
    

