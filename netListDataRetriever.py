import xml.etree.ElementTree as ET
import re

def retrievePortPinData(rolesStr):
    match = re.search('(^|/)(P([A-Z]{1})(\d{,2}))', rolesStr)
    if match:
        return (match.group(3),match.group(4))
    else:
        #print("no matching port name")
        return None

class CPinData:
    def __init__(self, indexInPackage = None,
            portName = None,
            portIndex = None,
            roles = [],
            isConnected = False,
            netName = None):
        self.indexInPackage = indexInPackage
        self.portName = portName
        self.portIndex = portIndex
        self.roles = roles
        self.isConnected = isConnected
        self.netName = netName

    def setNetName(self, netName = None):
        self.netName = netName

    def setConnection(self):
        self.isConnected = True

    def printMembers(self):
        stringToPrint = str(self.indexInPackage) + "," +\
            str(self.portName) + "," +\
            str(self.portIndex) + "," +\
            str(self.roles) + "," +\
            str(self.isConnected) + "," +\
            str(self.netName)
        print(stringToPrint)

def getEntryByIndexInPack(list,index):
    for entry in list:
        if entry.indexInPackage == index:
            return entry

pinsDataList = []

def getDataFromNetList(refName,filename):
    referenceName = refName
    tree = ET.parse(filename)
    root = tree.getroot()

    print("*** getDataFromNetList() ***")

    '''Getting component from a list of components'''
    components = root.findall("components/comp[@ref='" + referenceName + "']")
    print(components)
    if not components:
        print("Not a valid referenceName")
    else:
        for comp in components:
            print("ref: " + comp.get("ref"))
            value = comp.find("value").text
            print("value: " + value)
            footprint = comp.find("footprint").text
            print("footprint: " + footprint)
            libsource = comp.find("libsource")
            lib = libsource.get("lib")
            part = libsource.get("part")
            print("lib: " + lib + "\npart: " + part)
            
    '''Getting pin data from libpart'''
    libparts = root.findall("libparts/libpart[@lib='" + lib + "']")
    for lpart in libparts:
        isMatchingLibPart = False
        if lpart.get("part") == part:
            isMatchingLibPart = True
        else:
            for al in lpart.findall("aliases/alias"):
                if al.text == part:
                    print(al.text)
                    isMatchingLibPart = True
                    break
        if not isMatchingLibPart:
            print("No matching libpart")
            return None
        else:
            pins = lpart.findall("pins/pin")
            for p in pins:
                pinPackageNum = p.get("num")
                pinRolesStr = p.get("name")
                pinPortData = retrievePortPinData(pinRolesStr)
                if pinPortData:
                    pinPortName = pinPortData[0]
                    pinPortPinNum = pinPortData[1]
                else:
                    pinPortName = None
                    pinPortPinNum = None
                pinRoles = pinRolesStr.split("/")
                pinsDataList.append(CPinData(pinPackageNum,
                                             pinPortName,
                                             pinPortPinNum,
                                             pinRoles.copy()))
            break
        
    '''Getting connection check and net names'''
    nets = root.findall("nets/net")
    '''Get nets related only to our component by it's reference code'''
    netsOfThePart = [ net for net in nets if net.findall('node[@ref="' + referenceName + '"]') ]
    for net in netsOfThePart:    
        pinNum = net.find('node[@ref="' + referenceName + '"]').get("pin")
        netName = net.get('name')
        match = re.search('(/){0,1}(\w+)', netName)
        netNameWOutGarbage = match.group(2)
        entryInPinList = getEntryByIndexInPack(pinsDataList, pinNum)
        entryInPinList.setNetName(netNameWOutGarbage)
        nodesInNet = net.findall('node')
        if len(nodesInNet) > 1:
            entryInPinList.setConnection()

    print()
    print("Pins having no connection")
    for item in pinsDataList:
        if not item.isConnected:
            item.printMembers()

    print("\n\n\n")
            
    return pinsDataList

if __name__ == "__main__":
    getDataFromNetList("U1","PCB_motherboard.xml")




    
