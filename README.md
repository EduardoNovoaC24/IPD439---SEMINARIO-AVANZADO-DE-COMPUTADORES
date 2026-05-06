# IPD439---SEMINARIO-AVANZADO-DE-COMPUTADORES
Este repositorio esta destinado a las diferentes tareas que se realizaran en el curso de magister de ciencias de la electronica. 

## Descripción del código implementado: `1_main.c`

El archivo `1_main.c` contiene el programa utilizado para evaluar experimentalmente los modos de bajo consumo del microcontrolador STM32L476RGT6U en la tarjeta Nucleo-L476RG.

El código permite seleccionar, mediante una macro de compilación, el modo de bajo consumo que será probado. Para ello, se definieron seis modos posibles:

- Sleep
- Stop 0
- Stop 1
- Stop 2
- Standby
- Shutdown

Antes de entrar al modo seleccionado, el programa ejecuta una señal visual mediante el LED de usuario conectado al pin `PA5`. Luego, el LED se apaga y el microcontrolador entra al modo de bajo consumo correspondiente.

En los modos `Sleep`, `Stop 0`, `Stop 1` y `Stop 2`, el despertar del microcontrolador se realiza mediante una interrupción externa generada por el botón de usuario conectado al pin `PC13`. Esta interrupción permite que el núcleo salga del estado de espera y continúe la ejecución del programa.

Después del despertar, se llama nuevamente a la función `SystemClock_Config()` para restaurar la configuración del reloj del sistema. Esta llamada es especialmente importante después de los modos Stop, ya que durante estos modos se modifican o detienen relojes internos del microcontrolador.

Para los modos `Standby` y `Shutdown`, el comportamiento es distinto. En estos casos, el microcontrolador no continúa la ejecución desde la instrucción posterior a la entrada al modo de bajo consumo. En lugar de eso, despierta mediante el pin `PA0/WKUP1` y reinicia la ejecución del programa desde el inicio.

Por esta razón, los modos `Standby` y `Shutdown` se utilizaron principalmente para medir la corriente estacionaria alcanzada durante el estado de bajo consumo.

### Funcionamiento general

El flujo general del programa es el siguiente:

1. Se inicializa el microcontrolador mediante las funciones generadas por STM32CubeIDE.
2. Se habilita el reloj del periférico de potencia.
3. Se apaga el LED de usuario conectado a `PA5`.
4. Se ejecuta una señal visual inicial para confirmar que el programa comenzó correctamente.
5. En el bucle principal, el LED parpadea antes de entrar al modo seleccionado.
6. El microcontrolador entra al modo de bajo consumo definido por la macro `SELECTED_LOW_POWER_MODE`.
7. En `Sleep` y `Stop`, el sistema despierta mediante la interrupción externa del botón `PC13`.
8. Al despertar, se reconfigura el reloj del sistema.
9. El LED parpadea nuevamente para indicar que el microcontrolador volvió a Run Mode.
10. En `Standby` y `Shutdown`, el despertar provoca un reinicio del programa.

### Selección del modo de bajo consumo

El modo de bajo consumo se selecciona modificando la siguiente macro en el archivo `main.c`:

```c
#define SELECTED_LOW_POWER_MODE MODE_SLEEP
