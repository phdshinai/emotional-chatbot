from PIL import Image, ImageDraw
import time

W, H = 240, 280
BG = (0, 0, 0)
WHITE = (255, 255, 255)
CYAN = (100, 220, 255)
PINK = (255, 180, 200)
YELLOW = (255, 230, 100)

def create_base():
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)
    return img, draw

# 눈 위치 (두 줄만으로 귀엽게)
LX, RX, EY = 80, 160, 130  # 왼쪽X, 오른쪽X, 눈Y

def draw_neutral(draw):
    # ◉ ◉ 동그란 눈
    draw.ellipse((LX-22, EY-28, LX+22, EY+28), fill=WHITE)
    draw.ellipse((LX-10, EY-12, LX+10, EY+12), fill=BG)
    draw.ellipse((LX-4,  EY-18, LX+4,  EY-10), fill=WHITE)
    draw.ellipse((RX-22, EY-28, RX+22, EY+28), fill=WHITE)
    draw.ellipse((RX-10, EY-12, RX+10, EY+12), fill=BG)
    draw.ellipse((RX-4,  EY-18, RX+4,  EY-10), fill=WHITE)

def draw_happy(draw):
    # ∪ ∪ 초승달 눈
    draw.arc((LX-24, EY-10, LX+24, EY+30), start=0, end=180, fill=WHITE, width=8)
    draw.arc((RX-24, EY-10, RX+24, EY+30), start=0, end=180, fill=WHITE, width=8)
    # 볼터치
    draw.ellipse((LX-35, EY+30, LX+5,  EY+50), fill=PINK)
    draw.ellipse((RX-5,  EY+30, RX+35, EY+50), fill=PINK)

def draw_sad(draw):
    # 슬픈 눈 + 눈물
    draw.ellipse((LX-20, EY-24, LX+20, EY+24), fill=WHITE)
    draw.ellipse((LX-8,  EY+2,  LX+8,  EY+18), fill=BG)
    draw.ellipse((RX-20, EY-24, RX+20, EY+24), fill=WHITE)
    draw.ellipse((RX-8,  EY+2,  RX+8,  EY+18), fill=BG)
    # 눈물
    draw.ellipse((LX-4, EY+26, LX+4, EY+44), fill=CYAN)
    draw.ellipse((RX-4, EY+26, RX+4, EY+44), fill=CYAN)

def draw_calm(draw):
    # 반달 눈 (편안한)
    draw.arc((LX-22, EY-14, LX+22, EY+20), start=180, end=360, fill=WHITE, width=8)
    draw.arc((RX-22, EY-14, RX+22, EY+20), start=180, end=360, fill=WHITE, width=8)

def draw_concerned(draw):
    # 걱정 눈 (눈썹 모임)
    draw.ellipse((LX-20, EY-22, LX+20, EY+22), fill=WHITE)
    draw.ellipse((LX-7,  EY-8,  LX+7,  EY+8),  fill=BG)
    draw.ellipse((RX-20, EY-22, RX+20, EY+22), fill=WHITE)
    draw.ellipse((RX-7,  EY-8,  RX+7,  EY+8),  fill=BG)
    # 걱정 눈썹
    draw.line((LX-18, EY-34, LX+18, EY-26), fill=WHITE, width=5)
    draw.line((RX-18, EY-26, RX+18, EY-34), fill=WHITE, width=5)

def draw_blink(draw):
    # — — 납작하게 감은 눈
    draw.ellipse((LX-22, EY-5, LX+22, EY+5), fill=WHITE)
    draw.ellipse((RX-22, EY-5, RX+22, EY+5), fill=WHITE)

def draw_surprised(draw):
    # ○ ○ 크게 뜬 눈
    draw.ellipse((LX-26, EY-32, LX+26, EY+32), fill=WHITE)
    draw.ellipse((LX-10, EY-14, LX+10, EY+14), fill=BG)
    draw.ellipse((RX-26, EY-32, RX+26, EY+32), fill=WHITE)
    draw.ellipse((RX-10, EY-14, RX+10, EY+14), fill=BG)

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
    elif emotion == "surprised":
        draw_surprised(draw)
    else:
        draw_neutral(draw)
    return img

def blink_animation(display):
    pass