from PIL import Image, ImageDraw
import time

DISPLAY_SIZE = (240, 240)
BG_COLOR = (0, 0, 0)
EYE_COLOR = (255, 255, 255)
PUPIL_COLOR = (0, 0, 0)
HIGHLIGHT_COLOR = (255, 255, 255)
TEAR_COLOR = (100, 200, 255)
BLUSH_COLOR = (255, 150, 150)

def create_base():
    img = Image.new("RGB", DISPLAY_SIZE, BG_COLOR)
    draw = ImageDraw.Draw(img)
    return img, draw

def draw_neutral(draw):
    # 왼쪽 눈
    draw.ellipse((55, 80, 105, 145), fill=EYE_COLOR)
    draw.ellipse((70, 95, 90, 115), fill=PUPIL_COLOR)
    draw.ellipse((72, 97, 80, 105), fill=HIGHLIGHT_COLOR)
    # 오른쪽 눈
    draw.ellipse((135, 80, 185, 145), fill=EYE_COLOR)
    draw.ellipse((150, 95, 170, 115), fill=PUPIL_COLOR)
    draw.ellipse((152, 97, 160, 105), fill=HIGHLIGHT_COLOR)

def draw_happy(draw):
    # 초승달 눈 (위로 휜 곡선)
    draw.arc((55, 90, 105, 140), start=200, end=340, fill=EYE_COLOR, width=12)
    draw.arc((135, 90, 185, 140), start=200, end=340, fill=EYE_COLOR, width=12)
    # 볼터치
    draw.ellipse((40, 140, 80, 160), fill=BLUSH_COLOR)
    draw.ellipse((160, 140, 200, 160), fill=BLUSH_COLOR)

def draw_sad(draw):
    # 눈동자 아래로
    draw.ellipse((55, 85, 105, 150), fill=EYE_COLOR)
    draw.ellipse((70, 108, 90, 128), fill=PUPIL_COLOR)
    draw.ellipse((72, 110, 80, 118), fill=HIGHLIGHT_COLOR)
    draw.ellipse((135, 85, 185, 150), fill=EYE_COLOR)
    draw.ellipse((150, 108, 170, 128), fill=PUPIL_COLOR)
    draw.ellipse((152, 110, 160, 118), fill=HIGHLIGHT_COLOR)
    # 눈물
    draw.ellipse((75, 148, 88, 170), fill=TEAR_COLOR)
    draw.ellipse((155, 148, 168, 170), fill=TEAR_COLOR)

def draw_calm(draw):
    # 반쯤 감긴 눈
    draw.ellipse((55, 95, 105, 145), fill=EYE_COLOR)
    draw.rectangle((55, 95, 105, 118), fill=BG_COLOR)
    draw.ellipse((70, 108, 90, 128), fill=PUPIL_COLOR)
    draw.ellipse((135, 95, 185, 145), fill=EYE_COLOR)
    draw.rectangle((135, 95, 185, 118), fill=BG_COLOR)
    draw.ellipse((150, 108, 170, 128), fill=PUPIL_COLOR)

def draw_concerned(draw):
    # 눈썹 살짝 모임
    draw.ellipse((55, 85, 105, 150), fill=EYE_COLOR)
    draw.ellipse((70, 100, 90, 120), fill=PUPIL_COLOR)
    draw.ellipse((72, 102, 80, 110), fill=HIGHLIGHT_COLOR)
    draw.ellipse((135, 85, 185, 150), fill=EYE_COLOR)
    draw.ellipse((150, 100, 170, 120), fill=PUPIL_COLOR)
    draw.ellipse((152, 102, 160, 110), fill=HIGHLIGHT_COLOR)
    # 걱정 눈썹
    draw.line((60, 72, 100, 80), fill=EYE_COLOR, width=6)
    draw.line((140, 80, 180, 72), fill=EYE_COLOR, width=6)

def draw_blink(draw):
    # 납작한 눈
    draw.ellipse((55, 108, 105, 122), fill=EYE_COLOR)
    draw.ellipse((135, 108, 185, 122), fill=EYE_COLOR)

def get_expression(emotion):
    img, draw = create_base()
    if emotion == "happy":
        draw_happy(draw)
    elif emotion == "sad":
        draw_sad(draw)
    elif emotion == "calm":
        draw_calm(draw)
    elif emotion == "concerned":
        draw_concerned(draw)
    elif emotion == "blink":
        draw_blink(draw)
    else:
        draw_neutral(draw)
    return img

def blink_animation(display):
    """깜빡임 애니메이션"""
    for _ in range(2):
        img, draw = create_base()
        draw_neutral(draw)
        display.ShowImage(img)
        time.sleep(2.5)
        img, draw = create_base()
        draw_blink(draw)
        display.ShowImage(img)
        time.sleep(0.15)