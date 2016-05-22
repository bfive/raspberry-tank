#!/usr/bin/env python

import RPi.GPIO as GPIO
import time

enA = 17
inA1 = 18
inA2 = 21

enB = 22
inB1 = 23
inB2 = 24

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(True)

class Motor:
  class Mode:
    STOP = 0
    FORWARD = 1
    BACKWARD = 2

  def __init__(self, enable, in1, in2):
    self.enable = enable
    self.in1 = in1
    self.in2 = in2
    GPIO.setup(enable, GPIO.OUT)
    GPIO.setup(in1, GPIO.OUT)
    GPIO.setup(in2, GPIO.OUT)
    self.pwm = GPIO.PWM(enable, 50)
    self.pwm.start(0);

  def set_speed(self, speed):
    self.pwm.ChangeDutyCycle(speed)

  def set_mode(self, mode):
    if mode == Motor.Mode.STOP:
      GPIO.output(self.in1, 0)
      GPIO.output(self.in2, 0)
    elif mode == Motor.Mode.FORWARD:
      GPIO.output(self.in1, 1) # XXX not clear
      GPIO.output(self.in2, 0)
    elif mode == Motor.Mode.BACKWARD:
      GPIO.output(self.in1, 0)
      GPIO.output(self.in2, 1)
    else:
      assert False

  def stop(self):
    self.pwm.stop()

class Controller:
  def __init__(self):
    self.motorA = Motor(enA, inA1, inA2)
    self.motorB = Motor(enB, inB1, inB2)

  def stop(self):
    self.motorA.stop()
    self.motorB.stop()

try:
  c = Controller()
  for speed in range(0, 50, 5):
    c.motorA.set_speed(speed)
    time.sleep(2)
    c.motorA.set_mode(Motor.Mode.STOP)
    time.sleep(2)
    c.motorA.set_mode(Motor.Mode.FORWARD)
    c.motorB.set_speed(speed)
    time.sleep(2)
except KeyboardInterrupt:
  pass
finally:
  c.stop()
  GPIO.cleanup()

