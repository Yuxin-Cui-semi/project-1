# Yuxin Cui
# Assignment 1  EH2745

# Import the necessary library: ElementTree library, pandapower
# plotting module
import xml.etree.ElementTree as ET
import pandapower as pp
import pandapower.plotting.to_html as simple_plotly

# Import class defined as equipment etc.
from classes.acline import ACLineSegment
from classes.basevoltage import BaseVoltage
from classes.breaker import Breaker
from classes.busbarsection import BusbarSection
from classes.connectivitynode import ConnectivityNode
from classes.energyconsumer import EnergyConsumer
from classes.generatingunit import GeneratingUnit
from classes.linearshuntcompensator import LinearShuntCompensator
from classes.powertransformer import PowerTransformer
from classes.powertransformerend import PowerTransformerEnd
from classes.ratiotapchanger import RatioTapChanger
from classes.regulatingcontrol import RegulatingControl
from classes.substation import Substation
from classes.synchronousmachine import SynchronousMachine
from classes.terminal import Terminal
from classes.voltagelevel import VoltageLevel

# Create two trees by parsing the XML file referenced.
# Using ENTSO-E  model files used in Interoperability testing
tree_eq = ET.parse('MicroGridTestConfiguration_T1_BE_EQ_V2.xml')
tree_ssh = ET.parse('MicroGridTestConfiguration_T1_BE_SSH_V2.xml')

# Here the root of the tree could be accessed
microgrid_eq = tree_eq.getroot()
microgrid_ssh = tree_ssh.getroot()


# Storing namespace identifiers in strings and reuse when searching for tags
ns = {'cim':'http://iec.ch/TC57/2013/CIM-schema-cim16#',
      'entsoe':'http://entsoe.eu/CIM/SchemaExtension/3/1#',
      'rdf':'{http://www.w3.org/1999/02/22-rdf-syntax-ns#}'}

# Building the lists which store imformation
acline_list = []
base_voltage_list = []
breaker_list = []
busbar_list = []
connectivity_node_list = []
energy_consumer_list = []
generating_unit_list = []
linear_shunt_compensator_list = []
power_transformer_list = []
power_transformer_end_list = []
ratio_tap_changer_list = []
regulating_control_list = []
substation_list = []
synchronous_machine_list = []
terminal_list = []
voltage_level_list = []


# To find all corresponding data(attribute) that exist  in the document and 
# store them in a list
# sevral dictionary are also build for the connection with base voltages,
# equipment container and voltage level

# Base Voltage
for bv in microgrid_eq.findall('cim:BaseVoltage', ns):
    ID = bv.get(ns['rdf'] + 'ID')
    name = bv.find('cim:IdentifiedObject.name', ns).text
    nominal_voltage = bv.find('cim:BaseVoltage.nominalVoltage', ns).text
   
    base_voltage_list.append(BaseVoltage(ID, name, nominal_voltage))

# here we build the dict of base voltage which contain ids of base voltage and
# voltage level, which is a subclass of EquipmentContainer. 
# what should be noticed here is that the id of voltage level does not contain
# '#'.
base_voltage_dict = {}
for bvd in microgrid_eq.findall('cim:VoltageLevel', ns):
    bv_id = bvd.find('cim:VoltageLevel.BaseVoltage', ns).get(ns['rdf']+'resource')
    vl_id = bvd.get(ns['rdf'] + 'ID')
    base_voltage_dict[vl_id] = bv_id
    
# Create a dictionary to find the value of base voltage
base_voltage_value_dict = {}
for voltage in base_voltage_list:
    bv_id = voltage.ID
    bv_value = voltage.nominal_voltage
    base_voltage_value_dict[bv_id]= bv_value
    
# Voltage Level
for vl in microgrid_eq.findall('cim:VoltageLevel', ns):
    ID = vl.get(ns['rdf'] + 'ID')
    name = vl.find('cim:IdentifiedObject.name', ns).text
    substation = vl.find('cim:VoltageLevel.Substation', ns).get(ns['rdf']+'resource')
    base_voltage = vl.find('cim:VoltageLevel.BaseVoltage', ns).get(ns['rdf']+'resource')
    
   
    voltage_level_list.append(VoltageLevel(ID, name, substation.replace('#',''), 
                                           base_voltage.replace('#','')))
 
# ACLineSegment
for acline in microgrid_eq.findall('cim:ACLineSegment', ns):
    ID = acline.get(ns['rdf'] + 'ID')
    name = acline.find('cim:IdentifiedObject.name', ns).text
    equipment_container = acline.find('cim:Equipment.EquipmentContainer', ns).get(ns['rdf']+'resource')
    r = acline.find('cim:ACLineSegment.r', ns).text
    x = acline.find('cim:ACLineSegment.x', ns).text
    bch = acline.find('cim:ACLineSegment.bch', ns).text
    length = acline.find('cim:Conductor.length', ns).text
    gch = acline.find('cim:ACLineSegment.gch', ns).text
    base_voltage = acline.find('cim:ConductingEquipment.BaseVoltage', ns).get(ns['rdf']+'resource')
    
    acline_list.append(ACLineSegment(ID, name, equipment_container.replace('#',''), r, x, bch, length, gch, 
                 base_voltage.replace('#','')))
        
# Breaker
# Here the first time to find the base voltage of breaker by using the dict.
# In the dict, the id of VoltageLevel contains a '#', thats why using 
# 'equipment_container[1:]' in the dict
for breaker in microgrid_eq.findall('cim:Breaker', ns):
    ID = breaker.get(ns['rdf'] + 'ID')
    name = breaker.find('cim:IdentifiedObject.name', ns).text
    state = breaker.find('cim:Switch.normalOpen', ns).text
    equipment_container = breaker.find('cim:Equipment.EquipmentContainer', ns).get(ns['rdf']+'resource')
    base_voltage = base_voltage_dict[equipment_container[1:]]
    
    breaker_list.append(Breaker(ID, name, state, equipment_container.replace('#',''), 
                                base_voltage.replace('#','')))

# Busbar
for bus in microgrid_eq.findall('cim:BusbarSection', ns):
    ID = bus.get(ns['rdf'] + 'ID')
    name = bus.find('cim:IdentifiedObject.name', ns).text
    equipment_container = bus.find('cim:Equipment.EquipmentContainer', ns).get(ns['rdf']+'resource')
    base_voltage = base_voltage_dict[equipment_container[1:]]
    
    busbar_list.append(BusbarSection(ID, name, equipment_container.replace('#',''), 
                                base_voltage.replace('#','')))


# Energy Consumer 
P = []
Q = []
for econsumer_s in microgrid_ssh.findall('cim:EnergyConsumer', ns):
    p = econsumer_s.find('cim:EnergyConsumer.p', ns).text
    q = econsumer_s.find('cim:EnergyConsumer.q', ns).text    
    P.append(p)
    Q.append(q)
    
for i,econsumer in enumerate(microgrid_eq.findall('cim:EnergyConsumer', ns)):
    ID = econsumer.get(ns['rdf'] + 'ID')
    name = econsumer.find('cim:IdentifiedObject.name', ns).text
    equipment_container = econsumer.find('cim:Equipment.EquipmentContainer', ns).get(ns['rdf']+'resource')
    base_voltage = base_voltage_dict[equipment_container[1:]]
    
    energy_consumer_list.append(EnergyConsumer(ID, name, P[i], Q[i], 
                                               equipment_container.replace('#',''), 
                                               base_voltage.replace('#','')))
    
# Generating Unit 
for gu in microgrid_eq.findall('cim:GeneratingUnit', ns):
    ID = gu.get(ns['rdf'] + 'ID')
    name = gu.find('cim:IdentifiedObject.name', ns).text
    maxP = gu.find('cim:GeneratingUnit.maxOperatingP', ns).text
    minP = gu.find('cim:GeneratingUnit.minOperatingP', ns).text
    nomP = gu.find('cim:GeneratingUnit.nominalP', ns).text
    equipment_container = gu.find('cim:Equipment.EquipmentContainer', ns).get(ns['rdf']+'resource')
    
    generating_unit_list.append(GeneratingUnit(ID, name, maxP, minP, nomP, 
                                               equipment_container.replace('#','')))
                                
# Linear shunt compensator
for lsc in microgrid_eq.findall('cim:LinearShuntCompensator', ns):
    ID = lsc.get(ns['rdf'] + 'ID')
    name = lsc.find('cim:IdentifiedObject.name', ns).text
    b = lsc.find('cim:LinearShuntCompensator.bPerSection', ns).text
    g = lsc.find('cim:LinearShuntCompensator.gPerSection', ns).text
    equipment_container = lsc.find('cim:Equipment.EquipmentContainer', ns).get(ns['rdf']+'resource')
    voltage = lsc.find('cim:ShuntCompensator.nomU', ns).text
    q = float(b)*float(voltage)**2
    
    linear_shunt_compensator_list.append(LinearShuntCompensator(ID, name, b, g,
                                         equipment_container.replace('#',''),
                                         voltage, q))

# transformers                                       
for tf in microgrid_eq.findall('cim:PowerTransformer', ns):
    ID = tf.get(ns['rdf'] + 'ID')
    name = tf.find('cim:IdentifiedObject.name', ns).text
    equipment_container = tf.find('cim:Equipment.EquipmentContainer', ns).get(ns['rdf']+'resource')
                                
    power_transformer_list.append(PowerTransformer(ID, name, equipment_container.replace('#','')))
                                  
# Transformer end
for tfe in microgrid_eq.findall('cim:PowerTransformerEnd', ns):
    ID = tfe.get(ns['rdf'] + 'ID')
    name = tfe.find('cim:IdentifiedObject.name', ns).text
    r = tfe.find('cim:PowerTransformerEnd.r', ns).text
    x = tfe.find('cim:PowerTransformerEnd.x', ns).text
    b = tfe.find('cim:PowerTransformerEnd.b', ns).text
    g = tfe.find('cim:PowerTransformerEnd.g', ns).text
    base_voltage = tfe.find('cim:TransformerEnd.BaseVoltage', ns).get(ns['rdf']+'resource')
    powertransformer_ID = tfe.find('cim:PowerTransformerEnd.PowerTransformer', ns).get(ns['rdf']+'resource')
    terminal = tfe.find('cim:TransformerEnd.Terminal', ns).get(ns['rdf']+'resource')
    end_number = tfe.find('cim:TransformerEnd.endNumber', ns).text 

    power_transformer_end_list.append(PowerTransformerEnd(ID, name, r, x, b, g,
                                                          base_voltage.replace('#',''), 
                                                          powertransformer_ID.replace('#',''),
                                                          terminal.replace('#',''), 
                                                          end_number))                               
# Ratio tap changer
for rtc in microgrid_eq.findall('cim:RatioTapChanger', ns):
    ID = rtc.get(ns['rdf'] + 'ID')
    name = rtc.find('cim:IdentifiedObject.name', ns).text
    step = rtc.find('cim:TapChanger.normalStep', ns).text
                                
    ratio_tap_changer_list.append(RatioTapChanger(ID, name, step))
    
# Regulating control
for rc in microgrid_eq.findall('cim:RegulatingControl', ns):
    ID = rc.get(ns['rdf'] + 'ID')
    name = rc.find('cim:IdentifiedObject.name', ns).text
for rc in microgrid_ssh.findall('cim:RegulatingControl', ns):
    target_value = rc.find('cim:RegulatingControl.targetValue', ns).text
    
    regulating_control_list.append(RegulatingControl(ID, name, target_value))
    
# Substation
for substation in microgrid_eq.findall('cim:Substation', ns):
    ID = substation.get(ns['rdf'] + 'ID')
    name = substation.find('cim:IdentifiedObject.name', ns).text
    region = substation.find('cim:Substation.Region', ns).get(ns['rdf']+'resource')
    
    substation_list.append(Substation(ID, name, region.replace('#','')))
    
# Synchronous Machine

P = []
Q = []

for synm_s in microgrid_ssh.findall('cim:SynchronousMachine', ns):
    p = synm_s.find('cim:RotatingMachine.p', ns).text
    q = synm_s.find('cim:RotatingMachine.q', ns).text
    
    P.append(p)
    Q.append(q)
    
for i,synm in enumerate(microgrid_eq.findall('cim:SynchronousMachine', ns)):
    ID = synm.get(ns['rdf'] + 'ID')
    name = synm.find('cim:IdentifiedObject.name', ns).text
    rated_s = synm.find('cim:RotatingMachine.ratedS', ns).text
    regulating_control = synm.find('cim:RegulatingCondEq.RegulatingControl', ns).get(ns['rdf']+'resource')
    generating_unit = synm.find('cim:RotatingMachine.GeneratingUnit', ns).get(ns['rdf']+'resource')
    equipment_container = synm.find('cim:Equipment.EquipmentContainer', ns).get(ns['rdf']+'resource')
    base_voltage = base_voltage_dict[equipment_container[1:]]
    
    
    synchronous_machine_list.append(SynchronousMachine(ID, name, P[i], Q[i], rated_s, 
                                               regulating_control.replace('#',''), 
                                               generating_unit.replace('#',''), 
                                               equipment_container.replace('#',''), 
                                               base_voltage.replace('#','')))
    
# here comes the topology of the grid after introducing required equipment
# the first step is to figure all the nodes and terminals. 
# here involve the connection between nodes, terminals and equipments
# the nodes are connected to terminal, and terminals are connected with equipments and nodes
# so the the association type between nodes and terminals should be aggregation
# which is shown in the class ConnectivityNode.



# Terminals
for terminal in microgrid_eq.findall('cim:Terminal', ns):
    ID = terminal.get(ns['rdf'] + 'ID')
    name = terminal.find('cim:IdentifiedObject.name', ns).text
    CE = terminal.find('cim:Terminal.ConductingEquipment', ns).get(ns['rdf']+'resource')
    CN = terminal.find('cim:Terminal.ConnectivityNode', ns).get(ns['rdf']+'resource')
    
    terminal_list.append(Terminal(ID, name,CE.replace('#',''), CN.replace('#','')))

# Connectivity nodes
for connectn in microgrid_eq.findall('cim:ConnectivityNode', ns):
    ID = connectn.get(ns['rdf'] + 'ID')
    name = connectn.find('cim:IdentifiedObject.name', ns).text
    nodecontainer = connectn.find('cim:ConnectivityNode.ConnectivityNodeContainer', ns).get(ns['rdf']+'resource')
    base_voltage = base_voltage_dict[nodecontainer[1:]]
    connectn_class = ConnectivityNode(ID, name, nodecontainer.replace('#',''), 
                                      base_voltage.replace('#',''))
    
    #here if the id of connectivity nodes are equal to terminal's, we add the 
    #terminal into connectity node attribute
    
    for terminal in terminal_list:
        if ID.replace('#','') == terminal.CN[0:]:
            connectn_class.add_terminal(terminal)
    connectivity_node_list.append(connectn_class)
    
# assume nodes are 'special equipment', so it is easy to find out the relationship 
# between conducting equipment and terminal. Every conducting equipment has two 
# terminals to conduct with. 

for n in range(len(breaker_list)):
    ID = breaker_list[n].ID
    for terminal in terminal_list:
        if ID == terminal.CE[0:]:
            breaker_list[n].add_terminal(terminal)
            
for n in range(len(power_transformer_list)):
    ID = power_transformer_list[n].ID
    for terminal in terminal_list:
        if ID == terminal.CE[0:]:
            power_transformer_list[n].add_terminal(terminal)
            
for n in range(len(synchronous_machine_list)):
    ID = synchronous_machine_list[n].ID
    for terminal in terminal_list:
        if ID == terminal.CE[0:]:
            synchronous_machine_list[n].add_terminal(terminal)
            
for n in range(len(linear_shunt_compensator_list)):
    ID = linear_shunt_compensator_list[n].ID
    for terminal in terminal_list:
        if ID == terminal.CE[0:]:
            linear_shunt_compensator_list[n].add_terminal(terminal)
            
for n in range(len(energy_consumer_list)):
    ID = energy_consumer_list[n].ID
    for terminal in terminal_list:
        if ID == terminal.CE[0:]:
            energy_consumer_list[n].add_terminal(terminal)
            
for n in range(len(acline_list)):
    ID = acline_list[n].ID
    for terminal in terminal_list:
        if ID == terminal.CE[0:]:
            acline_list[n].add_terminal(terminal)
            
for n in range(len(busbar_list)):
    ID = busbar_list[n].ID
    for terminal in terminal_list:
        if ID == terminal.CE[0:]:
            busbar_list[n].add_terminal(terminal)
            
# here build a conducting equipment list
conducting_equipment_list = (breaker_list + power_transformer_list + synchronous_machine_list
                             + linear_shunt_compensator_list + energy_consumer_list +
                              acline_list + busbar_list)
            
# create an empty network
net = pp.create_empty_network()

# the function of finding next node
def find_next_code(pre_node, cur_node):
    if cur_node.type == 'TE':
        if pre_node.type == 'CE':
            next_node_id = cur_node.CN
            for node in connectivity_node_list:
                if next_node_id == node.ID:
                    return(node)
        if pre_node.type == 'CN':
            next_node_id = cur_node.CE
            for node in conducting_equipment_list:
                if next_node_id == node.ID:
                    return(node)
    if cur_node.type ==  'CN':
        for terminal in terminal_list:
            if cur_node.ID == terminal.CN[0:]:
                next_node = terminal
                return next_node
    if cur_node.type == 'CE':
        for terminal in terminal_list:
            if cur_node.ID == terminal.CN[0:]:
                next_node = terminal
                return next_node

            
# I would like to use the method of a traversal algorithm which is discussed in 
# the conference paper 
# 'An efficient method of extracting network information from CIM asset model'

# Step 0, Initialize
CN_stack = []
CE_stack = []
everything_stack = []
everything_stack_list = []

# Step 1 and 2 are shown in the above 'find_next_code' node

# Step 3
# find CN which is connected to busbar
CN_busbar_list = []
for i in connectivity_node_list:
    for j in i.terminal_list:
        if i.type == 'CN':
            pre_node = i
            cur_node = j
            next_node = find_next_code(pre_node, cur_node)
            if next_node.CE_type == 'Bus':
                CN_busbar_list.append(i)
                
# CNs which are not connected to busbar
CN_n_busbar_list = []
for i in connectivity_node_list:
    if i not in CN_busbar_list:
        CN_n_busbar_list.append(i)
        
# the connection between CNs and others
for i in connectivity_node_list:
    if i.Num_attachTerms > 0:
        for j in i.terminal_list:
            if j.traversal_flag == 0:
                CN_stack = [i] # push CN as soon as it is visited
                everything_stack = [i]
                cur_node = i
                i.Num_attachTerms = i.Num_attachTerms - 1
                j.traversal_flag = 1
                pre_node = cur_node
                cur_node = j
                next_node = find_next_code(pre_node, cur_node)
                # here the type of next node is CE node
                CE_stack.append(next_node)
                everything_stack.append(next_node)
                m = next_node
                if m.Num_attachTerms > 1:
                    for n in m.terminal_list:
                        if n.traversal_flag == 0:
                            n.traversal_flag = 1
                            pre_node = m
                            cur_node = n
                            next_node = find_next_code(pre_node, cur_node)
                            # here the type of next node is CN node
                            CN_stack.append(next_node)
                            everything_stack.append(next_node)
            if everything_stack not in everything_stack_list:
                everything_stack_list.append(everything_stack)

                
net = pp.create_empty_network()

# create bus
# conducting equipment__Bus
for bus in busbar_list:
    bus.bus = pp.create_bus(net, name= bus.name, vn_kv = base_voltage_value_dict[bus.base_voltage], type='b')
for CN in CN_n_busbar_list:
    CN.bus = pp.create_bus(net, name= CN.name, vn_kv = base_voltage_value_dict[bus.base_voltage], type='n')
for CN in CN_busbar_list:
    for terminal in CN.terminal_list:
            pre_node = CN
            cur_node = terminal
            next_node = find_next_code(pre_node, cur_node)
            if next_node.CE_type == 'Bus':
                CN.bus = next_node.bus
net.bus

# create transformer
for module in everything_stack_list:
    for device in module:
        if device.CE_type == 'Transformer':
            if base_voltage_value_dict[module[0].base_voltage] > base_voltage_value_dict[module[2].base_voltage]:
                bus_hv = module[0].bus
                bus_lv = module[2].bus
            else:
                bus_hv = module[2].bus
                bus_lv = module[0].bus
            pp.create_transformer(net, bus_hv, bus_lv, name = device.name, std_type = "25 MVA 110/20 kV")
net.trafo
# print(pp_transformer_list)


# create lines
for module in everything_stack_list:
    for device in module:
        if device.CE_type == 'Line':
            pp.create_line(net, module[0].bus, module[2].bus, length_km = device.length, 
                           std_type = "N2XS(FL)2Y 1x300 RM/35 64/110 kV",  name= device.name)

net.line
# print(pp_line_list)


# create switches
for module in everything_stack_list:
    for device in module:
        if device.CE_type == 'Breaker':
            if device.state == 'false':
                pp.create_switch(net, module[0].bus, module[2].bus, et="b", type="CB", closed=True)
            else:
                pp.create_switch(net, module[0].bus, module[2].bus, et="b", type="CB", closed=False)
net.switch
# print(pp_breaker_list)


# create generators
for module in everything_stack_list:
    for device in module:
        if device.CE_type == 'Generator':
            pp.create_sgen(net, module[0].bus, p_mw=device.p, q_mvar=device.q, 
                           name = device.name)       
net.sgen
# print(pp_generator_list)

# create load
for module in everything_stack_list:
    for device in module:
        if device.CE_type == 'Load':
            pp.create_load(net, module[0].bus, p_mw=device.p, q_mvar=device.q, 
                           scaling=0.6, name = device.name)   
net.load
# print(pp_load_list)

# create shunt
for module in everything_stack_list:
    for device in module:
        if device.CE_type == 'Compensator':
            pp.create_shunt(net, module[0].bus, q_mvar=device.q, p_mw=device.p, name = device.name)
net.shunt
# print(pp_shunt_list)

simple_plotly(net, 'microgrid.html')                            
                
        

                
    
            

            
    
    

            
    
            

        
    

                                                  


    
    
    
    

                                
                                        
    




    
    
    
    

















