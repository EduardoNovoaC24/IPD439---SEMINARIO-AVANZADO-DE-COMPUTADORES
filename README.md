# IPD439---SEMINARIO-AVANZADO-DE-COMPUTADORES
Este repositorio esta destinado a las diferentes tareas que se realizaran en el curso de magister de ciencias de la electronica. 

\subsubsection*{Descripción del código implementado 1_main.c}

El código desarrollado permite seleccionar, mediante una macro de compilación, el modo de bajo consumo que será evaluado experimentalmente. Para ello, se definieron seis modos posibles: Sleep, Stop 0, Stop 1, Stop 2, Standby y Shutdown. Antes de entrar al modo seleccionado, el programa ejecuta una señal visual mediante el LED de usuario conectado al pin \texttt{PA5}. Luego, el LED se apaga y el microcontrolador entra al modo de bajo consumo correspondiente.

En los modos Sleep, Stop 0, Stop 1 y Stop 2, el despertar del microcontrolador se realiza mediante una interrupción externa generada por el botón de usuario conectado al pin \texttt{PC13}. Esta interrupción permite que el núcleo salga del estado de espera y continúe la ejecución del programa. Después del despertar, se llama nuevamente a \texttt{SystemClock\_Config()} para restaurar la configuración del reloj del sistema, especialmente necesaria después de los modos Stop.

Para los modos Standby y Shutdown, el comportamiento es distinto, ya que el microcontrolador no continúa la ejecución desde la instrucción posterior a la entrada al modo de bajo consumo. En estos casos, el sistema despierta mediante el pin \texttt{PA0/WKUP1} y reinicia la ejecución del programa desde el inicio. Por esta razón, estos modos se utilizaron principalmente para medir la corriente estacionaria alcanzada durante el estado de bajo consumo.
