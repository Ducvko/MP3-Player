import threading
import sys
import os
song_dir = "/root/song_directory"
if os.path.exists(song_dir):
    sys.path.append(song_dir)

import RPi.GPIO as GPIO
import wave

class AudioPlayer:

    def __init__(self) -> None:
        GPIO.setmode(GPIO.BOARD)
        
        self.output_pin = 8
        self.duty_cycle = 0.5

        GPIO.setup(self.output_pin, GPIO.OUT)
        self.song
        


    def play_song(self, song_name: str):
        for root, dirs, files in os.walk(song_dir):
            if song_name + '.wav' in files:
                self.song = os.path.join(root, song_name + '.wav')
                break

        file = wave.open(self.song, 'rb')
        pwm_frequency = file.getframerate()
        pwm = GPIO.PWM(self.output_pin, pwm_frequency)

        pwm.start(self.duty_cycle)

        data = file.readframes(file.getnframes())
        while data:
            pwm.ChangeDutyCycle(self.duty_cycle)
        
        pwm.stop()

        GPIO.cleanup()

        file.close()
