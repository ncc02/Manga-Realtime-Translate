import cv2
import numpy as np
import pyautogui
import easyocr
from googletrans import Translator
from PIL import ImageFont, ImageDraw, Image

# Initialize translation
translator = Translator()

# Initialize EasyOCR reader
reader = easyocr.Reader(['en'])

def capture_screen_region(x, y, width, height):
    screenshot = pyautogui.screenshot(region=(x - width // 2, y, width, height))
    # return cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    return cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2GRAY)


import textwrap

# Hàm tạo ảnh nền trắng với chiều cao dựa trên số dòng văn bản
def create_text_background_dynamic_height(width, text, font_path, font_size=20):
    # Tạo ảnh nền trắng với chiều cao dựa trên số dòng văn bản
    background = np.ones((1, width), dtype=np.uint8) * 255
    pil_img = Image.fromarray(background)
    draw = ImageDraw.Draw(pil_img)
    font = ImageFont.truetype(font_path, font_size)
    
    lines = textwrap.wrap(text, width= width // 10) 
    total_height = 0
    for line in lines:
        bbox = font.getbbox(line)
        total_height += bbox[3] if bbox else 0

    # Tạo ảnh nền trắng với chiều cao dựa trên tổng chiều cao của các dòng văn bản
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
import time
previous_text = "code by cuongtk2002"

import keyboard

# Khởi tạo biến cho kích thước ban đầu

widthG, heightG = 400, 200

# Hàm để điều chỉnh kích thước
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

# Đăng ký các sự kiện phím
keyboard.on_press_key('up', adjust_size, suppress=True)
keyboard.on_press_key('down', adjust_size, suppress=True)
keyboard.on_press_key('left', adjust_size, suppress=True)
keyboard.on_press_key('right', adjust_size, suppress=True)


while True:
    x, y = pyautogui.position()

    width, height = widthG, heightG
    img = capture_screen_region(x, y, width, height)

    text = reader.readtext(img, detail=0, paragraph=True)
    try:
        text = text[0] if text else ""
        translated_text = previous_text
        if text != previous_text:  # Chỉ dịch khi văn bản thay đổi
            translated_text = translator.translate(text, src='en', dest='vi').text
            previous_text = translated_text
            
    except Exception as e:
        # print("Error translating text:", e)
        translated_text = ""

    
    text_background = create_text_background_dynamic_height(width, translated_text, font_path, font_size=20)

    combined_img = np.vstack((img, text_background))

    cv2.imshow('Realtime Translate', combined_img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
