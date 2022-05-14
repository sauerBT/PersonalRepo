from opcua import ua, Server, instantiate
from opcua.common.xmlexporter import XmlExporter
from random import randint
import time
import datetime

# setup our server
server = Server()
url = "opc.tcp://127.0.0.1:12345"
server.set_endpoint(url)

# setup our own namespace, not really necessary but should as spec
uri = "K-Tron_OPC-UA_Server"
idx = server.register_namespace(uri)

 # get Objects node, this is where we should put our nodes
objects = server.get_objects_node()
# initialize the node list
node_list = []
# populating our address space - DataAssembly
DataAssembly = objects.add_folder(idx, "DataAssembly")
IE_Desc = DataAssembly.add_property(idx, "DataAssembly Description", " The DataAssembly is the root object of each interface in the Module Type Package. All other interfaces must inherit from this element.")

# populating our address space - IndicatorElement
IndicatorElement = DataAssembly.add_folder(idx, "IndicatorElement")
IE_Desc = IndicatorElement.add_property(idx, "IndicatorElement Description", "The IndicatorElement is used to visualise PEA-internal values in the POL.")
BinView = IndicatorElement.add_folder(idx, "BinView")
DIntView = IndicatorElement.add_folder(idx, "DIntView")
AnaView = IndicatorElement.add_folder(idx, "AnaView")
StringView = IndicatorElement.add_folder(idx, "StringView")

# populating our address space - OperationElement
OperationElement = DataAssembly.add_folder(idx, "OperationElement")
OE_Desc = OperationElement.add_property(idx, "OperationElement Description", "The OperationElement is used to transfer values from the POL to the PEA.")
BinMan = OperationElement.add_folder(idx, "BinMan")
DIntMan = OperationElement.add_folder(idx, "DIntMan")
AnaMan = OperationElement.add_folder(idx, "AnaMan")

# populating our address space - ActiveElement
ActiveElement = DataAssembly.add_folder(idx, "ActiveElement")
AE_Desc = ActiveElement.add_property(idx, "ActiveElement Description",  "The ActiveElement is used to allow the operator at the POL to access active elements of the PEA single control level.")
BinVlv = ActiveElement.add_folder(idx, "BinVlv")
AnaVlv = ActiveElement.add_folder(idx, "AnaVlv")
BinDry = ActiveElement.add_folder(idx, "BinDry")
AnaDry = ActiveElement.add_folder(idx, "AnaDry")
PIDCtrl = ActiveElement.add_folder(idx, "PIDCtrl")


# variables to update
MaxFloInternal = 50

# populating our address space - Adding devices to BinView
KTronBinView = BinView.add_object(idx, "KTron")
KD_DISP_ACT = KTronBinView.add_variable(idx, "KCM-KD_DISP_ACT", 0) #UPDATE VARIABLE NAME
DB_INV = KTronBinView.add_variable(idx, "DB_INV", 0)
ALM_STP_IN_ACT = KTronBinView.add_variable(idx, "ALM_STP_IN_ACT", 0)
DSBL_IN_ACT = KTronBinView.add_variable(idx, "DSBL_IN_ACT", 0)
L_MD_ACT = KTronBinView.add_variable(idx, "L_MD_ACT", 0)
AUTO_CAL_ACT = KTronBinView.add_variable(idx, "AUTO_CAL_ACT", 0)
CVAR = KTronBinView.add_variable(idx, "CVAR", 0)
RUNNING = KTronBinView.add_variable(idx, "RUNNING", 0)
DRIVE_ENBL = KTronBinView.add_variable(idx, "DRIVE_ENBL", 0)
GRAV_MD_ACT = KTronBinView.add_variable(idx, "GRAV_MD_ACT", 0)
ALM_RLY_ACT = KTronBinView.add_variable(idx, "ALM_RLY_ACT", 0)
ALM_STP_OUT_ACT = KTronBinView.add_variable(idx, "ALM_STP_OUT_ACT", 0)
H_ALM_ACT = KTronBinView.add_variable(idx, "H_ALM_ACT", 0)
S_ALM_ACT = KTronBinView.add_variable(idx, "S_ALM_ACT", 0)
KSU_II_ACT = KTronBinView.add_variable(idx, "KSU_II_ACT", 0)
KCM_INIT_CMPLT = KTronBinView.add_variable(idx, "KCM_INIT_CMPLT", 0)
FDR_EMPTYING = KTronBinView.add_variable(idx, "FDR_EMPTYING", 0)
HCU_LOADING = KTronBinView.add_variable(idx, "HCU_LOADING", 0)
RUN_WAIT = KTronBinView.add_variable(idx, "RUN_WAIT", 0)
LINK_INIT_COMPLT = KTronBinView.add_variable(idx, "K-LINK_INIT_COMPLT", 0)
PERT_ACT = KTronBinView.add_variable(idx, "PERT_ACT", 0)

# populating our address space - Adding devices to AnaView
KTronAnaView = AnaView.add_folder(idx, "KTron")
MassFlow = KTronAnaView.add_variable(idx, "MassFlow", 0)
MassFlowSclMax = KTronAnaView.add_variable(idx, "MassFlowSclMax", 0)
Totalizer = KTronAnaView.add_variable(idx, "Totalizer", 0)
DriveCommand = KTronAnaView.add_variable(idx, "DriveCommand", 0)
MotorSpeed = KTronAnaView.add_variable(idx, "MotorSpeed", 0)
AvgFeedFactor = KTronAnaView.add_variable(idx, "AvgFeedFactor", 0)
NetWeight = KTronAnaView.add_variable(idx, "NetWeight", 0)
RefillLevelMin = KTronAnaView.add_variable(idx, "RefillLevelMin", 0)
RefillLevelMax = KTronAnaView.add_variable(idx, "RefillLevelMax", 0)

# populating our address space - Adding devices to AnaMan
KTronAnaMan = AnaMan.add_folder(idx, "KTron")
"""
def add_DataAssembly_variable(): 
    objects = self.opc.get_objects_node() 
    VMan = objects.add_variable('ns=3;s=stringid;', '3:stringnodefromstring', [68])
    VOut = objects.add_variable('ns=3;s=stringid;', '3:stringnodefromstring', [68]) 
    nid = ua.NodeId('stringid', 3) 
    qn = ua.QualifiedName('stringnodefromstring', 3) 
    assert nid == VMan.nodeid
    assert qn == VMan.get_browse_name()
"""
MaxF_VMan = KTronAnaMan.add_variable('ns=2;s=MaxFlo.VMan;', "2:MaxFlo.VMan",MaxFloInternal)
#MaxF_VMan = KTronAnaMan.add_variable('ns=2;s=MaxFlo.VMan;', "2:MaxFlo.VMan",MaxFloInternal)

#MaximumFlowVMan = MaximumFlow.add_variable(idx, "VMan", MassFlowMax)
MassFlowSP = KTronAnaMan.add_variable(idx, "MassFlowSP", 0)
MassFlowSPMin = MassFlowSP.add_variable(idx, "MassFlowSPMin", 0)
node_list = [MassFlowSP]

Count = 0
Rand = 0
interv = 0
#Interval.set_value(float(interv))
dt = float(input("Enter OPC-UA server update interval in seconds: "))

server.start()
print("Server started at {}".format(url))
try:
    while True:
        Count = Count + 1
        Rand = randint(200, 999)
        print(server.get_node("ns=2;s=MaxFlo.VMan;"))
        #Interv.read_value()
        server.get_node("ns=2;s=MaxFlo.VMan;").set_value(int(Count))
        NetWeight.set_value(float(Rand))

        print(datetime.datetime.now())
        time.sleep(dt)
finally:
    print("Building server export")
    exporter = XmlExporter(server)
    exporter.build_etree(node_list)
    exporter.write_xml('ua-export.xml')
    #server.export_xml(server.get_node(2), "C:\\Users\\bsauer\\Downloads\\Python\\007_OPC-UA_Server")
    server.stop()
    print("Server Offline")