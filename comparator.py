import cCodeDataRetriever as cCode
import netListDataRetriever as netFile
import sys

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
            str(self.portName) + "," +\
            str(self.portIndex) + "," +\
            str(self.netName) + "," +\
            str(self.function)
        print(stringToPrint)

def compareData(refNum, cCodeFName, netFileFName):
    cCodeDataList = cCode.getDataFromCCode(cCodeFName)
    netFileDataList = netFile.getDataFromNetList(refNum,netFileFName)

    pinsDataNoNetNameMatch = []

    print("*** comparator() ***")

    '''Find commonly used pins in both sides of project'''
    for netFileEntry in netFileDataList:
        for cCodeEntry in cCodeDataList:
            if netFileEntry.portName == cCodeEntry.portName and netFileEntry.portIndex == cCodeEntry.portIndex:
                if netFileEntry.netName != cCodeEntry.function:
                    pinsDataNoNetNameMatch.append(CPinsDataCompared(netFileEntry.portName,
                                      netFileEntry.portIndex,
                                      netFileEntry.netName,
                                      cCodeEntry.function))

    for noMatchEntry in pinsDataNoNetNameMatch:
        noMatchEntry.printMembers()



if __name__ == "__main__":
    referenceNum, cCodeFilename, netFileFilename = sys.argv[1:4]
    compareData(referenceNum, cCodeFilename, netFileFilename)
    
            

 
