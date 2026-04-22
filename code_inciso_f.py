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


ser.write(bytes([0x7F]))
resp_sync = ser.read(1)

if not resp_sync:
    print("Sin respuesta al 0x7F")
    ser.close()
    raise SystemExit

print("ACK sync:", resp_sync.hex())


ser.write(bytes([0x01, 0xFE]))


respuesta = ser.read(5)

if not respuesta or len(respuesta) < 5:
    print("Sin respuesta completa a Get Version")
    ser.close()
    raise SystemExit

print("Respuesta Get Version:", respuesta.hex())
print("Bytes individuales:", [hex(b) for b in respuesta])

ack_ini = respuesta[0]
version = respuesta[1]
opt1 = respuesta[2]
opt2 = respuesta[3]
ack_fin = respuesta[4]

print(f"ACK inicial: 0x{ack_ini:02X}")
print(f"Versión bootloader: 0x{version:02X}")
print(f"Option byte 1: 0x{opt1:02X}")
print(f"Option byte 2: 0x{opt2:02X}")
print(f"ACK final: 0x{ack_fin:02X}")

major = version >> 4
minor = version & 0x0F
print(f"Versión interpretada: V{major}.{minor}")

ser.close()
