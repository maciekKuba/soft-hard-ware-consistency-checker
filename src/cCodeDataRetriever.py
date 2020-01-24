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
    f = open(filename, "r")

    print("*** getDataFromCCode() ***")
    separator = '\t'
    print("Port" + separator + "Index" + separator + "Label")
    lineStr = f.readline()
    while lineStr != "":
        match = re.search('(//){0,1}PIN_INIT\(\s*GPIO([A-Z])\s*,\s*(\d{1,2})\s*,\s*(\w+)\s*\)', lineStr)
        if match and ( match.group(1) == None ) :
            print(match.group(2) + separator + match.group(3) + separator + match.group(4))
            pinsDataCCodeList.append(CPinDataCCode(match.group(2), match.group(3), match.group(4)))
        lineStr = f.readline()

    f.close()

    print("\n")

    return pinsDataCCodeList

if __name__ == "__main__":
    getDataFromCCode("./CCodeExample/pin.c")
