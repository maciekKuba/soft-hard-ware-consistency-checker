import cCodeDataRetriever as cCode
import netListDataRetriever as netFile
import sys

separator = '\t'

class CPinsDataCompared:
    def __init__(self,
            portName = None,
            portIndex = None,
            netName = None,
            function = None):
        self.portName = portName
        self.portIndex = portIndex
        self.netName = netName
        self.function = function

    def printMembers(self):
        stringToPrint = \
            str(self.portName) + separator +\
            str(self.portIndex) + separator +\
            str(self.netName) + separator + separator +\
            str(self.function)
        print(stringToPrint)

def compareData(refNum, cCodeFName, netFileFName):
    cCodeDataList = cCode.getDataFromCCode(cCodeFName)
    netFileDataList = netFile.getDataFromNetList(refNum,netFileFName)

    pinsDataNetNameMatch = []
    pinsDataNoNetNameMatch = []

    print("*** comparator() ***")

    '''Find commonly used pins in both sides of project'''
    for netFileEntry in netFileDataList:
        isEntryAdded = False
        for cCodeEntry in cCodeDataList:
            if netFileEntry.portName == cCodeEntry.portName and netFileEntry.portIndex == cCodeEntry.portIndex:
                if netFileEntry.netName == cCodeEntry.function:
                    pinsDataNetNameMatch.append(CPinsDataCompared(netFileEntry.portName,
                                      netFileEntry.portIndex,
                                      netFileEntry.netName,
                                      cCodeEntry.function))
                    isEntryAdded = True
                    break
                else:
                    pinsDataNoNetNameMatch.append(CPinsDataCompared(netFileEntry.portName,
                                      netFileEntry.portIndex,
                                      netFileEntry.netName,
                                      cCodeEntry.function))
                    isEntryAdded = True
                    break
        #Norepresentation in CCode
        if isEntryAdded == False and netFileEntry.isConnected and netFileEntry.portName:
            pinsDataNoNetNameMatch.append(CPinsDataCompared(netFileEntry.portName,
                                      netFileEntry.portIndex,
                                      netFileEntry.netName,
                                      "None"))

    print("Pins matching")
    print("Port" + separator + "Index" + separator + "Sch label" + separator + "CCode label")
    for noMatchEntry in pinsDataNetNameMatch:
        noMatchEntry.printMembers()
    
    print("\nPins not matching")
    print("Port" + separator + "Index" + separator + "Sch label" + separator + "CCode label")
    set(pinsDataNoNetNameMatch)
    for noMatchEntry in set(pinsDataNoNetNameMatch):
        noMatchEntry.printMembers()

if __name__ == "__main__":
    referenceNum, cCodeFilename, netFileFilename = sys.argv[1:4]
    compareData(referenceNum, cCodeFilename, netFileFilename)
