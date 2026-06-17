# motordriver.py
# A simple class to control an L298N motor driver.

from machine import Pin, PWM

class MotorDriver:
    def __init__(self, enA, in1, in2, enB, in3, in4):
        # Configure pins for Left Motor
        self.pwm_a = PWM(Pin(enA))
        self.in1 = Pin(in1, Pin.OUT)
        self.in2 = Pin(in2, Pin.OUT)
        
        # Configure pins for Right Motor
        self.pwm_b = PWM(Pin(enB))
        self.in3 = Pin(in3, Pin.OUT)
        self.in4 = Pin(in4, Pin.OUT)
        
        self.pwm_a.freq(1000)
        self.pwm_b.freq(1000)
        
        # Default speed (0-100%)
        self.speed = 80

    def _set_speed_duty(self, speed_percent):
        """Converts speed (0-100) to PWM duty cycle (0-65535)."""
        return int(speed_percent / 100 * 65535)

    def forward(self):
        duty = self._set_speed_duty(self.speed)
        self.in1.high()
        self.in2.low()
        self.in3.high()
        self.in4.low()
        self.pwm_a.duty_u16(duty)
        self.pwm_b.duty_u16(duty)

    def backward(self):
        duty = self._set_speed_duty(self.speed)
        self.in1.low()
        self.in2.high()
        self.in3.low()
        self.in4.high()
        self.pwm_a.duty_u16(duty)
        self.pwm_b.duty_u16(duty)

    def turn_left(self):
        duty = self._set_speed_duty(self.speed)
        self.in1.low()   # Left motor backward
        self.in2.high()
        self.in3.high()  # Right motor forward
        self.in4.low()
        self.pwm_a.duty_u16(duty)
        self.pwm_b.duty_u16(duty)

    def turn_right(self):
        duty = self._set_speed_duty(self.speed)
        self.in1.high()  # Left motor forward
        self.in2.low()
        self.in3.low()   # Right motor backward
        self.in4.high()
        self.pwm_a.duty_u16(duty)
        self.pwm_b.duty_u16(duty)

    def stop(self):
        self.in1.low()
        self.in2.low()
        self.in3.low()
        self.in4.low()
        self.pwm_a.duty_u16(0)
        self.pwm_b.duty_u16(0)
