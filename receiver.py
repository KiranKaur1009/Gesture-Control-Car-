# receiver.py
# Receives commands from the nRF24L01 and controls the motors.

import utime
from machine import Pin, SPI
from nrf24l01 import NRF24L01
from motordriver import MotorDriver

# nRF24L01 Configuration
spi = SPI(1, sck=Pin(10), mosi=Pin(11), miso=Pin(8))
cfg = {"spi": spi, "csn": 13, "ce": 12}
rx_pipe = b'\xe1\xf0\xf0\xf0\xf0'

# Motor Driver Pin Configuration
motors = MotorDriver(enA=18, in1=16, in2=17, enB=21, in3=20, in4=19)

def main():
    print("Initializing Receiver...")
    nrf = NRF24L01(cfg["spi"], Pin(cfg["csn"]), Pin(cfg["ce"]))
    nrf.open_rx_pipe(rx_pipe)
    nrf.set_power_speed(NRF24L01.POWER_MAX, NRF24L01.SPEED_250K)
    nrf.start_listening()
    print("Receiver ready. Awaiting commands...")

    last_received_time = utime.ticks_ms()
    FAILSAFE_TIMEOUT = 500  # 500 milliseconds

    while True:
        if nrf.any():
            while nrf.any():
                buf = nrf.recv()
                command = buf.decode()
                
                print(f"Received command: {command}")
                
                if command == 'F':
                    motors.forward()
                elif command == 'B':
                    motors.backward()
                elif command == 'L':
                    motors.turn_left()
                elif command == 'R':
                    motors.turn_right()
                elif command == 'S':
                    motors.stop()
                    
            last_received_time = utime.ticks_ms()

        # Failsafe: if no message is received for a while, stop the car.
        if utime.ticks_diff(utime.ticks_ms(), last_received_time) > FAILSAFE_TIMEOUT:
            print("Failsafe triggered: No signal. Stopping motors.")
            motors.stop()
            # Reset timer to prevent continuous printing of failsafe message
            last_received_time = utime.ticks_ms()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Ensure motors are stopped on exit
        motors.stop()
        print("Motors stopped.")
