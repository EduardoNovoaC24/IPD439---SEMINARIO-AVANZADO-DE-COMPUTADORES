import serial
import time

PORT = "/dev/ttyACM0"
BAUDRATE = 115200
START_ADDR = 0x08000000
NUM_BYTES = 256  # 0x100


def xor_checksum(data: bytes) -> int:
    x = 0
    for b in data:
        x ^= b
    return x & 0xFF


def read_exact(ser: serial.Serial, n: int, what: str) -> bytes:
    data = ser.read(n)
    if len(data) != n:
        raise RuntimeError(
            f"No llegaron {n} bytes para {what}. Llegaron {len(data)}."
        )
    return data


def expect_ack(ser: serial.Serial, what: str) -> None:
    b = read_exact(ser, 1, what)[0]
    if b == 0x79:
        print(f"ACK OK en {what}: 0x79")
        return
    if b == 0x1F:
        raise RuntimeError(f"NACK en {what}: 0x1F")
    raise RuntimeError(f"Respuesta inesperada en {what}: 0x{b:02X}")


def hexdump(data: bytes, base_addr: int = 0) -> None:
    for i in range(0, len(data), 16):
        chunk = data[i:i+16]
        hex_bytes = " ".join(f"{b:02X}" for b in chunk)
        print(f"{base_addr + i:08X}: {hex_bytes}")


def main() -> None:
    print("Abriendo puerto serial...")
    ser = serial.Serial(
        port=PORT,
        baudrate=BAUDRATE,
        bytesize=serial.EIGHTBITS,
        parity=serial.PARITY_EVEN,
        stopbits=serial.STOPBITS_ONE,
        timeout=1
    )

    try:
        time.sleep(0.2)
        ser.reset_input_buffer()
        ser.reset_output_buffer()

        
        print("Enviando 0x7F para sincronizar...")
        ser.write(bytes([0x7F]))
        expect_ack(ser, "sync")

        
        print("Enviando comando Read Memory (0x11 0xEE)...")
        ser.write(bytes([0x11, 0xEE]))
        expect_ack(ser, "Read Memory command")

        
        addr_bytes = START_ADDR.to_bytes(4, byteorder="big")
        addr_ck = xor_checksum(addr_bytes)
        print(
            "Enviando dirección:",
            " ".join(f"0x{b:02X}" for b in addr_bytes),
            f"checksum=0x{addr_ck:02X}"
        )
        ser.write(addr_bytes + bytes([addr_ck]))
        expect_ack(ser, "address")

        n = NUM_BYTES - 1
        n_comp = n ^ 0xFF
        print(f"Enviando longitud: N=0x{n:02X}, complemento=0x{n_comp:02X}")
        ser.write(bytes([n, n_comp]))
        expect_ack(ser, "length")

        print(f"Leyendo {NUM_BYTES} bytes...")
        data = read_exact(ser, NUM_BYTES, "flash data")

        print("\nDump leído desde flash:")
        hexdump(data, START_ADDR)


        with open("flash_256.bin", "wb") as fbin:
            fbin.write(data)

        with open("flash_256.txt", "w") as ftxt:
            for i in range(0, len(data), 16):
                chunk = data[i:i+16]
                hex_bytes = " ".join(f"{b:02X}" for b in chunk)
                ftxt.write(f"{START_ADDR + i:08X}: {hex_bytes}\n")

        print("\nArchivos guardados:")
        print(" - flash_256.bin")
        print(" - flash_256.txt")

    finally:
        ser.close()
        print("Puerto cerrado.")


if __name__ == "__main__":
    main()
