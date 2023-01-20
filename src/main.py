import sys
import os
song_dir = "/root/song_directory"
if os.path.exists(song_dir):
    sys.path.append(song_dir)

from .AudioPlayer import AudioPlayer
import threading

from ..OLED import OLED_1in5
from PIL import Image, ImageDraw, ImageFont
import RPi.GPIO as GPIO

class UserInterface:

    def __init__(self) -> None:
        #initializes the display and clears it
        self.display = OLED_1in5.OLED_Display()
        self.display.Init()
        self.display.clear()

        #config audio codec
        self.player = AudioPlayer(self.songs_list)

        #config gpio
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)

        #setup buttons
        GPIO.setup(11, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(11, GPIO.FALLING)
        GPIO.setup(15, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(15, GPIO.FALLING)
        GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(16, GPIO.FALLING, callback=threading.Thread(target=self.player.play_song, args=(self.displayed_songs[self.selector_index],)))

        # Creating the elements that will persist throughout runtime
        self.song_queue = Image.new('L', (self.display.width, self.display.height), 0)
        self.song_queue_image = ImageDraw.Draw(self.song_queue)
        self.font = ImageFont.truetype('/root/mp3-player/OLED/Font.ttc', 12)

        #the index of the songs displayed on the screen, defaults to None
        #the modifiers for the index when a page turns
        self.selector_index = None
        self.page = 1
        self.page_modifier = 4 * self.page
        self.start = 1
        self.end = 4

        #rect holders
        self.rect1 = self.song_queue_image.rectangle([(0, 0), (128, 32)], (0, 0, 0))
        self.rect2 = self.song_queue_image.rectangle([(0, 32), (128, 64)], (127, 127, 127))
        self.rect3 = self.song_queue_image.rectangle([(0,64), (128, 96)], (0, 0, 0))
        self.rect4 = self.song_queue_image.rectangle([(0, 96), (128, 128)], (127, 127, 127))

        #song name holders
        self.song1 = self.song_queue_image.text((10, 16), '', font=self.font, anchor='mm', fill='white')
        self.song1 = self.song_queue_image.text((10, 48), '', font=self.font, anchor='mm', fill='white')
        self.song1 = self.song_queue_image.text((10, 80), '', font=self.font, anchor='mm', fill='white')
        self.song1 = self.song_queue_image.text((10, 112), '', font=self.font, anchor='mm', fill='white')


        # entire list of songs and displayed
        self.songs_list = [u"%s" % i.removesuffix('.wav') for i in os.listdir(song_dir) if os.path.isfile(os.path.join(song_dir, i)) and i.endswith('.wav')]
        self.displayed_songs = self.songs_list[:3]

    def get_songs(self):
        self.songs_list = [u"%s" % i.removesuffix('.wav') for i in os.listdir(song_dir) if os.path.isfile(os.path.join(song_dir, i)) and i.endswith('.wav')]


    def display_selected(self):
        if self.selector_index is not None:
            if self.selector_index == 0:
                self.reset_colour()
                self.rect1 = self.song_queue_image.rectangle([(0, 0), (128, 32)], (211, 211, 211))
                self.song1 = self.song_queue_image.text((10, 16), f"{self.displayed_songs[0]}", font=self.font, anchor='mm', fill='teal')
            elif self.selector_index == 1:
                self.reset_colour()
                self.rect2 = self.song_queue_image.rectangle([(0, 32), (128, 64)], (211, 211, 211))
                self.song1 = self.song_queue_image.text((10, 16), f"{self.displayed_songs[1]}", font=self.font, anchor='mm', fill='teal')
            elif self.selector_index == 2:
                self.reset_colour()
                self.rect3 = self.song_queue_image.rectangle([(0,64), (128, 96)], (211, 211, 211))
                self.song1 = self.song_queue_image.text((10, 16), f"{self.displayed_songs[2]}", font=self.font, anchor='mm', fill='teal')
            elif self.selector_index == 3:
                self.reset_colour()
                self.rect4 = self.song_queue_image.rectangle([(0, 96), (128, 128)], (211, 211, 211))
                self.song1 = self.song_queue_image.text((10, 16), f"{self.displayed_songs[3]}", font=self.font, anchor='mm', fill='teal')

    def reset_colour(self):
        self.rect1 = self.song_queue_image.rectangle([(0, 0), (128, 32)], (0, 0, 0))
        self.rect2 = self.song_queue_image.rectangle([(0, 32), (128, 64)], (127, 127, 127))
        self.rect3 = self.song_queue_image.rectangle([(0,64), (128, 96)], (0, 0, 0))
        self.rect4 = self.song_queue_image.rectangle([(0, 96), (128, 128)], (127, 127, 127))

        self.song1 = self.song_queue_image.text((10, 16), f"{self.displayed_songs[0]}", font=self.font, anchor='mm', fill='white')
        self.song1 = self.song_queue_image.text((10, 48), f"{self.displayed_songs[1]}", font=self.font, anchor='mm', fill='white')
        self.song1 = self.song_queue_image.text((10, 80), f"{self.displayed_songs[2]}", font=self.font, anchor='mm', fill='white')
        self.song1 = self.song_queue_image.text((10, 112), f"{self.displayed_songs[3]}", font=self.font, anchor='mm', fill='white')

    def build_screen(self):
        #builds the general screen elements on startup
        if self.selector_index == None:
            self.selector_index = 0
            self.reset_colour()
        
        #checks for updates to buttons states and updates them accordingly
        self.scrolled_off_screen()
        self.display_selected()

    def scrolled_off_screen(self):
        if self.page == 1:
            if self.selector_index > 4:
                self.page += 1
                self.selector_index = 0
                self.displayed_songs = self.songs_list[self.start + self.page_modifier - 1:self.end + self.page_modifier - 1]

        else:
            if self.selector_index > 4:
                self.page += 1
                self.selector_index = 0
                self.displayed_songs = self.songs_list[self.start + self.page_modifier - 1:self.end + self.page_modifier - 1]
            elif self.selector_index < 0:
                self.page -= 1
                self.selector_index = 4
                self.displayed_songs = self.songs_list[self.start + self.page_modifier - 1:self.end + self.page_modifier - 1]

    def poll_buttons(self):
        if GPIO.event_detected(11):
            self.selector_index += 1
        elif GPIO.event_detected(15):
            self.selector_index -= 1
        
        return

if __name__ == "__main__":
    #main screen loop
    ui = UserInterface()
    while True:
        
        ui.poll_buttons()
        ui.scrolled_off_screen()

        ui.display_selected()

