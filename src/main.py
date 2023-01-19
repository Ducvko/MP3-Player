import itertools
import sys
import os
song_dir = "/root/song_directory"
if os.path.exists(song_dir):
    sys.path.append(song_dir)

from ..OLED import OLED_1in5
from PIL import Image, ImageDraw, ImageFont
import RPi.GPIO as GPIO

#initializes the display and clears it
display = OLED_1in5.OLED_Display()
display.Init()
display.clear()

# Creating the elements that will persist throughout runtime
song_queue = Image.new('L', (display.width, display.height), 0)
song_queue_image = ImageDraw.Draw(song_queue)
font = ImageFont.truetype('/root/mp3-player/OLED/Font.ttc', 12)

#the index of the songs displayed on the screen, defaults to None
#the modifiers for the index when a page turns
selector_index = None
page = 1
page_modifier = 4 * page
start = 1
end = 4

#rect holders
rect1 = song_queue_image.rectangle([(0, 0), (128, 32)], (0, 0, 0))
rect2 = song_queue_image.rectangle([(0, 32), (128, 64)], (127, 127, 127))
rect3 = song_queue_image.rectangle([(0,64), (128, 96)], (0, 0, 0))
rect4 = song_queue_image.rectangle([(0, 96), (128, 128)], (127, 127, 127))


# entire list of songs and displayed
songs_list = [u"%s" % i.removesuffix('.wav') for i in os.listdir(song_dir) if os.path.isfile(os.path.join(song_dir, i)) and i.endswith('.wav')]
displayed_songs = songs_list[:3]


def get_songs():
    songs_list = [u"%s" % i.removesuffix('.wav') for i in os.listdir(song_dir) if os.path.isfile(os.path.join(song_dir, i)) and i.endswith('.wav')]


def display_selected():
    if selector_index == None:
        selector_index = 0
        reset_colour()
    elif selector_index is not None:
        if selector_index == 0:
            reset_colour()
            rect1 = song_queue_image.rectangle([(0, 0), (128, 32)], (211, 211, 211))
        elif selector_index == 1:
            reset_colour()
            rect2 = song_queue_image.rectangle([(0, 32), (128, 64)], (211, 211, 211))
        elif selector_index == 2:
            reset_colour()
            rect3 = song_queue_image.rectangle([(0,64), (128, 96)], (211, 211, 211))
        elif selector_index == 3:
            reset_colour()
            rect4 = song_queue_image.rectangle([(0, 96), (128, 128)], (211, 211, 211))

def reset_colour():
    rect1 = song_queue_image.rectangle([(0, 0), (128, 32)], (0, 0, 0))
    rect2 = song_queue_image.rectangle([(0, 32), (128, 64)], (127, 127, 127))
    rect3 = song_queue_image.rectangle([(0,64), (128, 96)], (0, 0, 0))
    rect4 = song_queue_image.rectangle([(0, 96), (128, 128)], (127, 127, 127))

def poll_buttons():
    return

            

def scrolled_off_screen():
    if page == 1:
        if selector_index > 4:
            page += 1
            selector_index = 0
            displayed_songs = songs_list[start + page_modifier - 1:end + page_modifier - 1]

    else:
        if selector_index > 4:
            page += 1
            selector_index = 0
            displayed_songs = songs_list[start + page_modifier - 1:end + page_modifier - 1]
        elif selector_index < 0:
            page -= 1
            selector_index = 4
            displayed_songs = songs_list[start + page_modifier - 1:end + page_modifier - 1]




if __name__ == "__main__":
    #main screen loop
    while True:
        
        poll_buttons()
        
        display_selected()

        scrolled_off_screen()
