import re

class CPinDataCCode:
    def __init__(self,
            portName = None,
            portIndex = None,
            function = None,):
        self.portName = portName
        self.portIndex = portIndex
        self.function = function

pinsDataCCodeList = []

def getDataFromCCode(filename):
    f = open("pin.c", "r")

    print("*** getDataFromCCode() ***")
    
    lineStr = f.readline()
    while lineStr != "":
        match = re.search('(//){0,1}PIN_INIT\(\s*GPIO([A-Z])\s*,\s*(\d{1,2})\s*,\s*(\w+)\s*\)', lineStr)
        if match and ( match.group(1) == None ) :
            print(match.group(2) + "," + match.group(3) + "," + match.group(4))
            pinsDataCCodeList.append(CPinDataCCode(match.group(2), match.group(3), match.group(4)))
        lineStr = f.readline()

    f.close()

    print("\n\n\n")

    return pinsDataCCodeList

if __name__ == "__main__":
    getDataFromCCode("pin.c")
