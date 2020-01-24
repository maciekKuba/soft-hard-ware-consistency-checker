#ifndef PIN_H
#define PIN_H

#include "stm32f10x.h"

typedef struct pin
{
	GPIO_TypeDef* GPIOx;
	uint16_t GPIO_PinNr;
} PIN_S;

#define PIN_INIT(GPIO_OBJ, PIN_NR, NAME) PIN_S NAME = {GPIO_OBJ, PIN_NR};
#define PIN_EXTERN(NAME) extern PIN_S NAME;
#endif
