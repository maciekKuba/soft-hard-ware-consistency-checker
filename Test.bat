*** getDataFromCCode() ***
Port	Index	Label
A	5	SPI1_SCK
A	12	TIMER2
B	6	TX
C	3	adc
D	1	TIMER


*** getDataFromNetList() ***
Microcontroller data
ref: U1
value: STM32F100R6Tx
footprint: LQFP64
lib: stm32
part: STM32F100R6Tx
STM32F100R6Tx

Pins utilized in a schematic
Index pack	Port	Index port	Avail. roles	Is connected	Label
4		C	15		['PC15', 'ADC1_EXTI15', 'RCC_OSC32_OUT']	True	ADC2
11		C	3		['PC3', 'ADC1_IN13']	True	ADC
21		A	5		['ADC1_IN5', 'DAC_OUT2', 'SPI1_SCK', 'PA5']	True	Net-(R4-Pad1)
31		None	None		['VSS']	True	GND
45		A	12		['TIM1_ETR', 'USART1_RTS', 'PA12']	True	TIMER2
54		D	2		['PD2', 'TIM3_ETR']	True	TIMER
58		B	6		['I2C1_SCL', 'TIM16_CH1N', 'USART1_TX', 'PB6']	True	UART_TX
64		None	None		['VDD']	True	3V3


*** comparator() ***
Pins matching
Port	Index	Sch label	CCode label
A	12	TIMER2		TIMER2

Pins not matching
Port	Index	Sch label	CCode label
A	5	Net-(R4-Pad1)		SPI1_SCK
B	6	UART_TX		TX
C	15	ADC2		None
D	2	TIMER		None
C	3	ADC		adc
D	1	Net-(U1-Pad6)		TIMER
