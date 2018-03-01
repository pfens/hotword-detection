import snowboydecoder
import sys
import signal
import os

import serial

ser = serial.Serial('/dev/ttyACM?',9600) #treba staviti vrednost



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
    ser.write('blink,')

# capture SIGINT signal, e.g., Ctrl+C
signal.signal(signal.SIGINT, signal_handler)

detector = snowboydecoder.HotwordDetector(model, sensitivity=0.55)
print('Listening... Press Ctrl+C to exit')

# main loop
detector.start(detected_callback,
               interrupt_check=interrupt_callback,
               sleep_time=0.03)

detector.terminate()
