/*
 * flash_data.h
 *
 *  Created on: Mar 23, 2026
 *      Author: eduardonovoac
 */

#ifndef INC_FLASH_DATA_H_
#define INC_FLASH_DATA_H_

#include <stdint.h>

/* Tamaño del buffer de prueba almacenado en Flash */
#define FLASH_BUFFER_SIZE 1024

/* Arreglo constante ubicado en memoria Flash */
extern const uint8_t src_flash[FLASH_BUFFER_SIZE];

#endif /* INC_FLASH_DATA_H_ */
