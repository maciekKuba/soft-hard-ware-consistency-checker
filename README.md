# soft-hard-ware-consistency-checker
Software and Hardware Consistency Checker

## Goal
The script performs consistency check of microcontroller's pins assignment between software and PCB projects.
Less eye checks. 
Less forgotten changes and cut-and-bypassed lines on just etched new PCB a while ago. 
Less hacky solders.
Less bugs in configuration.

### General operation
It compares data of pins assignment taken from C file and netlist file from PCB project.

## Requirements

Python 3.

The tool supports netfiles outputted from KiCad (tested under KiCad 4).
Also, it requires use of imposed C file format.

### C file format
There are required 2 files - a source and a header.
For header, please look into repository. Just copy and paste into your project's sources/headers directory.
C file (does not need to be separate file) must contain pins assignments as follows:

    //PIN_INIT(GPIOA, 4, xxx)
    PIN_INIT(GPIOA, 5, SPI_CK)

The macro PIN_INIT() creates an object of following type (see pin.h):
    
    typedef struct pin
    {
    	GPIO_TypeDef* GPIOx;
    	uint16_t GPIO_PinNr;
    } PIN_S;

You should use such created objects in your code to configure pins.

Commented line means unassigned pin.
The macro PIN_INIT() takes following arguments:
	port, index in the port, function name.

In case of keeping the assignment in separate file, ensure you use PIN_EXTERN() macro in files where you use the pin structure object.

### Schematic
In the schematic assign all used pins a label.
The label should match the function name in a C code file.
Otherwise, the script will catch the mismatch to warn you.

## How to use?
Run xsltproc.exe in KiCad for getting intermediate netlist file in XML format:

    "C:/Program Files/KiCad/bin/xsltproc.exe" "%I" "--nowrite"

You can run it from the BOM section in KiCad EESCHEMA.
No worries about errors thrown there. You most likely get a sufficient netlist file.
  
Run comparator.py script with following arguments passed into:

    python comparator.py "yourMicrocontrollerRefNameInSchematic" "yourCFilename.c" "yourNetlist.xml"
    
You can also check how that works by running Test.bat file which uses provided exemplary data of C file and KiCad project.
The code view:
![Alt text](docs/CCodeScreenshot.png?raw=true "Title")

The schematic view:
![Alt text](docs/KiCadScreenshot.png?raw=true "Title")

The result should be similar to this one:

    Pins matching
    Port    Index   Sch label       CCode label
    A       12      TIMER2          TIMER2
    
    Pins not matching
    Port    Index   Sch label       CCode label
    D       2       TIMER           None
    D       1       Net-(U1-Pad6)   TIMER
    C       15      ADC2            None
    A       5       Net-(R4-Pad1)   SPI1_SCK
    C       3       ADC             adc
    B       6       UART_TX         TX

## Operation in details
### C file data.
Gathering pin data from C code file contaning function (role) assigned to pins.
Retrieved data for each pin: 

* port name,
* index in a port, 
* occupied function.

### Netlist xml file data.
Gathering pin generic data from the netlist file. It collects data about each pin in a package.
Retrieved data for each pin:

*	index in a package,
*	port name,
*	index in a port,
*	available roles,
*	is connected,
*	netlist name.

The script utilizes *xml* python module to retrieve the data.
Netlist data are used as a reference to C file data.

### Comparison

After data from C file and netlist are gathered, the script looks for pins commonly used in both files and selects those having differece between net-name in netlist and function name in C file. Data regarding to selected pins is printed out.

## Limitations 
(in spite of known limitations or any uknown yet, please notify me if you see some would be nice to be supported already)
1. Supports only one entity of microcontroller device in a schematic.
2. Port pin indication can be matched to following regex '(^|/)(P([A-Z]{1})(\d{,2}))'
3. There is no coverage for case of interconnected pins within a microcontrollers.
4. C file have no more than one assignment a line.
5. Line with assignment cannot begin with white character.
6. Designed for use with STM32 microcontrollers. Port names as well as GPIO struct name is taken from STM32 firmware.
7. Supports only '//' comment indication in C source file.

## Improvement areas
1. Replacement of lists with maps for quicker execution of scripts.
2. Parsing direct netlist file rather than indirect xml.	
