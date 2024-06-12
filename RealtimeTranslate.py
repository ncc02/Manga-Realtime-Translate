import cv2
import numpy as np
import pyautogui
import easyocr
from googletrans import Translator
from PIL import ImageFont, ImageDraw, Image
import time
import keyboard
import textwrap

# Initialize translation
translator = Translator()

# Initialize EasyOCR reader
reader = easyocr.Reader(['en'])

def capture_screen_region(x, y, width, height):
    screenshot = pyautogui.screenshot(region=(x - width // 2, y, width, height))
    return cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2GRAY)

# Create dynamic height text background
def create_text_background_dynamic_height(width, text, font_path, font_size=20):
    background = np.ones((1, width), dtype=np.uint8) * 255
    pil_img = Image.fromarray(background)
    draw = ImageDraw.Draw(pil_img)
    font = ImageFont.truetype(font_path, font_size)
    
    lines = textwrap.wrap(text, width= width // 10) 
    total_height = 0
    for line in lines:
        bbox = font.getbbox(line)
        total_height += bbox[3] if bbox else 0

    text_background = np.ones((total_height, width), dtype=np.uint8) * 255
    pil_text_img = Image.fromarray(text_background)
    draw = ImageDraw.Draw(pil_text_img)

    y = 0
    for line in lines:
        draw.text((10, y), line, font=font, fill=(0))
        y += font.getbbox(line)[3]

    return np.array(pil_text_img)

# Font path for Unicode support
font_path = "C:/Windows/Fonts/Arial.ttf"
previous_text = "code by cuongtk2002"

# Initialize variables for screen region size
widthG, heightG = 400, 200

# Adjust size based on key events
def adjust_size(key_event):
    global widthG, heightG
    if key_event.name == 'up':
        heightG -= 50
    elif key_event.name == 'down':
        heightG += 50
    elif key_event.name == 'left':
        widthG -= 50
    elif key_event.name == 'right':
        widthG += 50

# Register key events
keyboard.on_press_key('up', adjust_size, suppress=True)
keyboard.on_press_key('down', adjust_size, suppress=True)
keyboard.on_press_key('left', adjust_size, suppress=True)
keyboard.on_press_key('right', adjust_size, suppress=True)

previous_mouse_pos = pyautogui.position()

while True:
    current_mouse_pos = pyautogui.position()

    # Check if the mouse position has changed
    if current_mouse_pos != previous_mouse_pos:
        x, y = current_mouse_pos
        width, height = widthG, heightG
        img = capture_screen_region(x, y, width, height)

        text = reader.readtext(img, detail=0, paragraph=True)
        try:
            text = text[0] if text else ""
            translated_text = previous_text
            if text != previous_text:
                translated_text = translator.translate(text, src='en', dest='vi').text
                previous_text = translated_text
        except Exception as e:
            translated_text = ""

        text_background = create_text_background_dynamic_height(width, translated_text, font_path, font_size=20)
        combined_img = np.vstack((img, text_background))
        cv2.imshow('Realtime Translate', combined_img)

    # Update previous mouse position
    previous_mouse_pos = current_mouse_pos

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
