import snowboydecoder
import sys
import signal
import os

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(18,GPIO.OUT)



interrupted = False


def signal_handler(signal, frame):
    global interrupted
    interrupted = True


def interrupt_callback():
    global interrupted
    return interrupted

if len(sys.argv) == 1:
    print("Error: need to specify model name")
    print("Usage: python demo.py your.model")
    sys.exit(-1)

model = sys.argv[1]

def detected_callback():
    #ser.write('blink')
    print "LED on"
    GPIO.output(18,GPIO.HIGH)
    time.sleep(1)
    print "LED off"
    GPIO.output(18,GPIO.LOW)

# capture SIGINT signal, e.g., Ctrl+C
signal.signal(signal.SIGINT, signal_handler)

detector = snowboydecoder.HotwordDetector(model, sensitivity=0.55)
print('Listening... Press Ctrl+C to exit')

# main loop
detector.start(detected_callback,
               interrupt_check=interrupt_callback,
               sleep_time=0.03)

detector.terminate()
