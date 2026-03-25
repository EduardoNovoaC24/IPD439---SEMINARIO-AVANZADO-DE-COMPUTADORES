import time
import serial
import matplotlib.pyplot as plt

ARDUINO_PORT = "/dev/ttyACM0"
NUCLEO_PORT = "/dev/ttyACM1"
BAUD = 115200
FS = 100

def wait_for_capture_from_nucleo(ser_nucleo, freq):
    samples = []
    capturing = False

    print(f"\nArduino configurado a {freq} Hz.")
    print("Presiona el botón azul de la Nucleo para capturar...")

    while True:
        raw = ser_nucleo.readline()
        if not raw:
            continue

        line = raw.decode(errors="ignore").strip()
        if not line:
            continue

        print(line)

        if line == "START":
            samples = []
            capturing = True
            print("Captura iniciada")
            continue

        if line == "END":
            print("Captura finalizada")
            break

        if capturing:
            try:
                samples.append(int(line))
            except ValueError:
                pass

    return samples

def plot_samples(samples, freq_hz):
    if not samples:
        print(f"No se recibieron muestras para {freq_hz} Hz")
        return

    t = [i / FS for i in range(len(samples))]

    plt.figure(figsize=(10, 4))
    plt.plot(t, samples, marker="o", markersize=2)
    plt.title(f"Señal adquirida por STM32 - {freq_hz} Hz")
    plt.xlabel("Tiempo [s]")
    plt.ylabel("Cuenta ADC")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f"captura_{freq_hz}Hz.png", dpi=200)
    plt.show()

def set_arduino_frequency(ser_arduino, freq_hz):
    ser_arduino.reset_input_buffer()
    ser_arduino.write(f"{freq_hz}\n".encode())
    ser_arduino.flush()
    time.sleep(0.5)

    while ser_arduino.in_waiting:
        msg = ser_arduino.readline().decode(errors="ignore").strip()
        if msg:
            print("Arduino:", msg)

def main():
    ser_arduino = serial.Serial(ARDUINO_PORT, BAUD, timeout=1)
    ser_nucleo = serial.Serial(NUCLEO_PORT, BAUD, timeout=1)

    time.sleep(2)

    ser_arduino.reset_input_buffer()
    ser_nucleo.reset_input_buffer()

    for freq in [1, 5, 10]:
        set_arduino_frequency(ser_arduino, freq)
        samples = wait_for_capture_from_nucleo(ser_nucleo, freq)
        plot_samples(samples, freq)

    ser_arduino.close()
    ser_nucleo.close()

if __name__ == "__main__":
    main()
