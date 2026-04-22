	import serial
	import time
	
	puerto = "/dev/ttyACM0"
	
	ser = serial.Serial(
	port=puerto,
	baudrate=115200,
	bytesize=serial.EIGHTBITS,
	parity=serial.PARITY_EVEN,
	stopbits=serial.STOPBITS_ONE,
	timeout=1
	)
	
	time.sleep(0.2)
	
	# Sincronización
	ser.write(bytes([0x7F]))
	resp_sync = ser.read(1)
	
	if not resp_sync:
	print("Sin respuesta al 0x7F")
	ser.close()
	raise SystemExit
	
	print("ACK sync:", resp_sync.hex())
	
	# Enviar Get ID = 0x02 0xFD
	ser.write(bytes([0x02, 0xFD]))
	
	#  Leer respuesta
	respuesta = ser.read(5)
	
	if respuesta:
	print("Respuesta Get ID:", respuesta.hex())
	print("Bytes individuales:", [hex(b) for b in respuesta])
	else:
	print("Sin respuesta a Get ID")
	
	ser.close()
