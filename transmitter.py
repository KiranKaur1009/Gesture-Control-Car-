# transmitter.py
# Reads MPU-6050 sensor data and transmits commands via nRF24L01.

import ustruct
import utime
from machine import Pin, SPI, I2C
from nrf24l01 import NRF24L01

# MPU-6050 Constants
MPU6050_ADDR = 0x68
PWR_MGMT_1 = 0x6B
ACCEL_XOUT_H = 0x3B

# nRF24L01 Configuration
spi = SPI(1, sck=Pin(10), mosi=Pin(11), miso=Pin(8))
cfg = {"spi": spi, "csn": 13, "ce": 12}
tx_pipe = b'\xe1\xf0\xf0\xf0\xf0'

# Gesture Thresholds
FORWARD_THRESHOLD = 4000
BACKWARD_THRESHOLD = -4000
LEFT_THRESHOLD = -4000
RIGHT_THRESHOLD = 4000

# --- MPU-6050 Initialization ---
i2c = I2C(0, scl=Pin(5), sda=Pin(4))
i2c.writeto_mem(MPU6050_ADDR, PWR_MGMT_1, b'\x00')

def read_accel(reg):
    """Reads a 16-bit signed value from the MPU-6050."""
    data = i2c.readfrom_mem(MPU6050_ADDR, reg, 2)
    val = ustruct.unpack('>h', data)[0]
    return val

def get_gesture():
    """Determines the gesture based on accelerometer tilt."""
    ax = read_accel(ACCEL_XOUT_H)
    ay = read_accel(ACCEL_XOUT_H + 2)

    if ay > FORWARD_THRESHOLD:
        return b'F'  # Forward
    elif ay < BACKWARD_THRESHOLD:
        return b'B'  # Backward
    elif ax > RIGHT_THRESHOLD:
        return b'R'  # Right
    elif ax < LEFT_THRESHOLD:
        return b'L'  # Left
    else:
        return b'S'  # Stop

def main():
    print("Initializing Transmitter...")
    nrf = NRF24L01(cfg["spi"], Pin(cfg["csn"]), Pin(cfg["ce"]))
    nrf.open_tx_pipe(tx_pipe)
    nrf.set_power_speed(NRF24L01.POWER_MAX, NRF24L01.SPEED_250K) # Max power, min speed for range
    print("Transmitter ready. Start gesturing.")

    while True:
        command = get_gesture()
        
        try:
            nrf.send(command)
            print(f"Sent command: {command.decode()}")
        except OSError:
            print("Failed to send command.")
        
        utime.sleep_ms(100)

if __name__ == "__main__":
    main()
