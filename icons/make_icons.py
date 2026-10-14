"""Fluent Emoji에 없는 단어 아이콘 생성기 (Fluent 3D 스타일 맞춤).

- 합성: Fluent Emoji 3D 이모지 여러 개를 겹치거나 색을 바꿔서 만든다 (MIT, 출처 표기 불필요)
- 직접 그림: 냉장고·도마·파처럼 이모지가 아예 없는 것은 그라데이션+하이라이트로 그린다 (make_card.py와 같은 방식)

결과: made/<단어>.png (256×256, 투명 배경). 만든 뒤 assets.py로 등록한다:
  python assets.py set <id> --file icons/made/<단어>.png --name "..." --license "MIT (Fluent Emoji 기반 자체 제작)"

필요: pillow, 그리고 assets.py가 받아 둔 .cache/fluentui-emoji
실행: python make_icons.py            # 전체
      python make_icons.py 냉장고 파   # 일부만
"""
import colorsys
import json
import os
import sys

from PIL import Image, ImageChops, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(HERE, "made")
W = H = 256
SS = 4

_INDEX = {i["name"]: i for i in json.load(open(os.path.join(ROOT, ".cache", "emoji_index.json"), encoding="utf-8"))}


# ---------- 합성 도구 ----------
def emoji(name, scale=1.0, rotate=0):
    im = Image.open(os.path.join(ROOT, _INDEX[name]["file"])).convert("RGBA").resize((W, H), Image.LANCZOS)
    if scale != 1.0:
        im = im.resize((int(W * scale), int(H * scale)), Image.LANCZOS)
    if rotate:
        im = im.rotate(rotate, Image.BICUBIC, expand=True)
    return im


def canvas():
    return Image.new("RGBA", (W, H), (0, 0, 0, 0))


def put(base, im, cx, cy):
    """im의 중심을 (cx, cy)에 놓는다."""
    base.alpha_composite(im, (int(cx - im.width / 2), int(cy - im.height / 2)))
    return base


def hue_shift(im, deg, sat=1.0):
    px = im.load()
    out = im.copy()
    po = out.load()
    for y in range(im.height):
        for x in range(im.width):
            r, g, b, a = px[x, y]
            if not a:
                continue
            h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
            r2, g2, b2 = colorsys.hsv_to_rgb((h + deg / 360) % 1, min(1, s * sat), v)
            po[x, y] = (int(r2 * 255), int(g2 * 255), int(b2 * 255), a)
    return out


def tint(im, mul):
    r, g, b, a = im.split()
    r, g, b = (ch.point(lambda v, m=m: min(255, int(v * m))) for ch, m in zip((r, g, b), mul))
    return Image.merge("RGBA", (r, g, b, a))


def colorize(im, dark, light):
    """밝기만 남기고 dark→light 색으로 다시 칠한다."""
    from PIL import ImageOps
    out = ImageOps.colorize(im.convert("L"), dark, light).convert("RGBA")
    out.putalpha(im.getchannel("A"))
    return out


def dim(im, keep=0.55):
    """불 꺼진 느낌: 채도를 빼고 어둡게."""
    gray = im.convert("LA").convert("RGBA")
    gray.putalpha(im.getchannel("A"))
    return tint(Image.blend(gray, im, 0.15), (keep, keep, keep + 0.05))


# ---------- 직접 그리기 도구 ----------
def big():
    return Image.new("RGBA", (W * SS, H * SS), (0, 0, 0, 0))


def done(im):
    return im.resize((W, H), Image.LANCZOS)


def s(*v):
    return tuple(int(x * SS) for x in v)


def grad_shape(size, box, c0, c1, radius, vertical=True):
    """box 안을 c0→c1 그라데이션으로 칠한 둥근 사각형 레이어."""
    layer = Image.new("RGBA", size, (0, 0, 0, 0))
    x0, y0, x1, y1 = box
    g = ImageDraw.Draw(layer)
    n = (y1 - y0) if vertical else (x1 - x0)
    for k in range(n):
        t = k / max(1, n - 1)
        col = tuple(int(c0[i] + (c1[i] - c0[i]) * t) for i in range(3)) + (255,)
        if vertical:
            g.line((x0, y0 + k, x1, y0 + k), fill=col)
        else:
            g.line((x0 + k, y0, x0 + k, y1), fill=col)
    mask = Image.new("L", size, 0)
    ImageDraw.Draw(mask).rounded_rectangle(box, radius, fill=255)
    out = Image.new("RGBA", size, (0, 0, 0, 0))
    out.paste(layer, (0, 0), mask)
    return out, mask


def highlight(im, mask, box, alpha=70, blur=6):
    x0, y0, x1, y1 = box
    hl = Image.new("L", im.size, 0)
    ImageDraw.Draw(hl).rounded_rectangle(box, SS * 10, fill=alpha)
    hl = Image.composite(hl, Image.new("L", im.size, 0), mask).filter(ImageFilter.GaussianBlur(blur * SS))
    white = Image.new("RGBA", im.size, (255, 255, 255, 0))
    white.putalpha(hl)
    im.alpha_composite(white)


def shadow(im, box, radius, color=(40, 50, 90, 70), dy=6, blur=8):
    sh = Image.new("RGBA", im.size, (0, 0, 0, 0))
    x0, y0, x1, y1 = box
    ImageDraw.Draw(sh).rounded_rectangle((x0, y0 + dy * SS, x1, y1 + dy * SS), radius, fill=color)
    im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(blur * SS)))


# ---------- 직접 그림 ----------
def fridge():
    im = big()
    body = s(58, 14, 198, 244)
    shadow(im, body, 26 * SS)
    layer, mask = grad_shape(im.size, body, (236, 242, 252), (176, 190, 214), 26 * SS, vertical=False)
    im.alpha_composite(layer)
    highlight(im, mask, s(58, 14, 120, 244), alpha=80, blur=8)
    d = ImageDraw.Draw(im)
    # 냉동실/냉장실 경계
    d.line(s(62, 92, 194, 92), fill=(140, 154, 182, 255), width=3 * SS)
    d.line(s(62, 95, 194, 95), fill=(250, 252, 255, 200), width=SS)
    # 손잡이
    for y0, y1 in ((40, 76), (110, 170)):
        hb = s(76, y0, 88, y1)
        d.rounded_rectangle(hb, 6 * SS, fill=(120, 134, 168, 255))
        d.rounded_rectangle(s(78, y0 + 2, 84, y1 - 4), 3 * SS, fill=(170, 184, 214, 255))
    # 다리
    for x in (78, 170):
        d.rounded_rectangle(s(x, 240, x + 10, 248), 2 * SS, fill=(110, 120, 150, 255))
    return done(im)


def cutting_board():
    im = big()
    board = s(28, 70, 214, 222)
    tab = s(196, 120, 246, 172)
    shadow(im, s(28, 70, 246, 222), 24 * SS, color=(120, 70, 30, 40), dy=4, blur=5)
    for box, rad in ((tab, 22 * SS), (board, 24 * SS)):
        layer, mask = grad_shape(im.size, box, (241, 196, 140), (206, 140, 82), rad)
        im.alpha_composite(layer)
    _, mask = grad_shape(im.size, board, (0, 0, 0), (0, 0, 0), 24 * SS)
    highlight(im, mask, s(28, 70, 214, 110), alpha=70)
    d = ImageDraw.Draw(im)
    # 손잡이 구멍
    d.ellipse(s(216, 136, 232, 152), fill=(0, 0, 0, 0))
    hole = Image.new("L", im.size, 255)
    ImageDraw.Draw(hole).ellipse(s(216, 136, 232, 152), fill=0)
    im.putalpha(Image.composite(im.getchannel("A"), Image.new("L", im.size, 0), hole))
    # 나뭇결
    for y, x0, x1 in ((112, 52, 150), (146, 80, 196), (180, 46, 128), (196, 140, 190)):
        d.arc(s(x0, y - 6, x1, y + 6), 200, 340, fill=(190, 128, 72, 160), width=2 * SS)
    # 옆면 두께
    d.rounded_rectangle(s(30, 214, 212, 226), 8 * SS, fill=(170, 108, 58, 255))
    return done(im)


def green_onion():
    im = big()
    stalks = ((-14, 112), (0, 128), (14, 144))
    for ang, cx in stalks:
        lay = big()
        x0, x1 = cx - 13, cx + 13
        # 초록 잎 (위) → 하얀 줄기 (아래)
        green, gmask = grad_shape(lay.size, s(x0, 18, x1, 160), (150, 214, 92), (58, 150, 60), 13 * SS, vertical=False)
        lay.alpha_composite(green)
        white, wmask = grad_shape(lay.size, s(x0, 140, x1, 228), (252, 250, 236), (220, 226, 200), 13 * SS, vertical=False)
        lay.alpha_composite(white)
        # 초록→흰 경계를 부드럽게
        fade = Image.new("RGBA", lay.size, (0, 0, 0, 0))
        fd = ImageDraw.Draw(fade)
        for k in range(24):
            t = k / 23
            fd.line(s(x0, 132 + k, x1, 132 + k), fill=(200 + int(50 * t), 232, 170 + int(60 * t), int(200 * (1 - abs(t - 0.5) * 2))))
        lay.alpha_composite(Image.composite(fade, Image.new("RGBA", lay.size, (0, 0, 0, 0)), wmask))
        highlight(lay, Image.composite(gmask, wmask, wmask), s(x0, 18, cx - 2, 228), alpha=90, blur=3)
        # 뿌리
        d = ImageDraw.Draw(lay)
        for dx in (-8, -3, 2, 7):
            d.line(s(cx + dx, 226, cx + dx * 1.8, 246), fill=(214, 200, 160, 255), width=2 * SS)
        lay = lay.rotate(ang, Image.BICUBIC, center=s(cx, 228))
        im.alpha_composite(lay)
    return done(im)


# ---------- 합성 ----------
def door_open():
    base = canvas()
    door = emoji("Door")
    bbox = door.getbbox()
    x0, y0, x1, y1 = bbox
    d = ImageDraw.Draw(base)
    d.rounded_rectangle((x0, y0, x1, y1), 10, fill=(70, 52, 50, 255))          # 문틀 안쪽 (어두움)
    d.rounded_rectangle((x0 + 6, y0 + 6, x1 - 6, y1), 8, fill=(255, 236, 170, 255))  # 밖에서 들어오는 빛
    panel = door.crop(bbox)
    w, h = panel.size
    nw = int(w * 0.45)
    # 왼쪽 경첩을 축으로 열린 문: 오른쪽 모서리가 위아래로 커지며 다가온다
    coeffs = find_coeffs([(0, 0), (nw, -h * 0.08), (nw, h * 1.08), (0, h)], [(0, 0), (w, 0), (w, h), (0, h)])
    opened = panel.transform((nw, int(h * 1.16)), Image.PERSPECTIVE, coeffs, Image.BICUBIC)
    shifted = canvas()
    shifted.alpha_composite(opened, (x0 - nw // 3, y0 - int(h * 0.08)))
    base.alpha_composite(shifted)
    return base


def find_coeffs(dst, src):
    """PIL PERSPECTIVE 계수 (dst 좌표 → src 좌표)."""
    import numpy as np  # noqa: 지역 import — 이 함수만 numpy 필요
    A, B = [], []
    for (x, y), (u, v) in zip(dst, src):
        A.append([x, y, 1, 0, 0, 0, -u * x, -u * y]); B.append(u)
        A.append([0, 0, 0, x, y, 1, -v * x, -v * y]); B.append(v)
    return np.linalg.solve(np.array(A, float), np.array(B, float)).tolist()


def jar_lid():
    jar = emoji("Jar", 0.82)
    x0, y0, x1, y1 = jar.getbbox()
    cut = y0 + int((y1 - y0) * 0.15)
    body = jar.crop((0, cut, jar.width, jar.height))
    lid = jar.crop((0, 0, jar.width, cut)).rotate(-22, Image.BICUBIC, expand=True)
    base = canvas()
    ox = (W - jar.width) // 2
    oy = H - jar.height
    base.alpha_composite(body, (ox, oy + cut))
    base.alpha_composite(lid, (ox + 28, oy + cut - lid.height - 4))
    return base


def tuna_can():
    """납작한 참치캔 (따개 달린 은색 뚜껑 + 생선 라벨)."""
    im = big()
    x0, x1, top, bot, eh = 34, 222, 104, 196, 44   # eh: 타원 높이
    shadow(im, s(x0, top, x1, bot + eh / 2), 40 * SS, dy=6, blur=8)
    d = ImageDraw.Draw(im)
    # 아래 테두리 (은색 타원)
    d.ellipse(s(x0, bot - eh / 2, x1, bot + eh / 2), fill=(150, 160, 185, 255))
    # 몸통 라벨 (파랑 그라데이션) + 아래 둥근 부분
    lab = big()
    layer, _ = grad_shape(lab.size, s(x0, top, x1, bot), (255, 222, 110), (232, 158, 40), 0, vertical=False)
    lab.alpha_composite(layer)
    lmask = Image.new("L", lab.size, 0)
    md = ImageDraw.Draw(lmask)
    md.rectangle(s(x0, top, x1, bot - 4), fill=255)
    md.ellipse(s(x0, bot - 4 - eh / 2, x1, bot - 4 + eh / 2), fill=255)
    lab.putalpha(Image.composite(lab.getchannel("A"), Image.new("L", lab.size, 0), lmask))
    im.alpha_composite(lab)
    highlight(im, lmask, s(x0, top, x0 + 50, bot), alpha=70, blur=6)
    # 라벨 위쪽 파란 띠
    d.rectangle(s(x0, top + 8, x1, top + 18), fill=(40, 100, 200, 255))
    # 윗면 (은색 타원 + 홈 + 따개)
    d.ellipse(s(x0, top - eh / 2, x1, top + eh / 2), fill=(214, 222, 238, 255))
    d.ellipse(s(x0 + 10, top - eh / 2 + 5, x1 - 10, top + eh / 2 - 5), fill=(188, 198, 220, 255))
    d.ellipse(s(x0 + 16, top - eh / 2 + 8, x1 - 16, top + eh / 2 - 7), fill=(226, 232, 245, 255))
    d.rounded_rectangle(s(108, top - 10, 150, top + 6), 8 * SS, outline=(150, 160, 190, 255), width=4 * SS)
    d.ellipse(s(140, top - 6, 156, top + 6), fill=(170, 180, 205, 255))
    out = done(im)
    return put(out, emoji("Fish", 0.4, rotate=0), 128, 164)


def steam(xs, y0, y1, amp, width, c_bottom, c_top):
    """위로 올라가는 나란한 물결 곡선들 (김·열기). 아래 c_bottom → 위 c_top 색, 위로 갈수록 옅어짐."""
    import math
    lay = big()
    d = ImageDraw.Draw(lay)
    steps = 200
    paths = []
    for i, x in enumerate(xs):
        h = (y1 - y0) * (0.82 if i % 2 else 1.0)    # 가운데 곡선은 조금 짧게
        pts = []
        for k in range(steps + 1):
            t = k / steps                            # 0 = 아래, 1 = 위
            pts.append((t, x + amp * math.sin(t * 2 * math.pi * 1.25), y1 - h * t))
        paths.append(pts)
        for t, px, y in pts:
            col = tuple(int(c_bottom[j] + (c_top[j] - c_bottom[j]) * t) for j in range(3))
            r = width / 2 * (1 - 0.3 * t)
            d.ellipse(s(px - r, y - r, px + r, y + r), fill=col + (255,))
    for pts in paths:                                # 반사광 (가는 밝은 줄)
        for t, px, y in pts[12:-40]:
            r = width * 0.09
            px -= width * 0.2
            d.ellipse(s(px - r, y - r, px + r, y + r), fill=(255, 245, 230, 255))
    # 위로 갈수록 옅어지게: 그린 뒤 알파에 세로 그라데이션을 곱한다
    fade = Image.new("L", (1, lay.height))
    for yy in range(lay.height):
        t = min(1, max(0, (y1 * SS - yy) / ((y1 - y0) * SS)))
        fade.putpixel((0, yy), int(255 * (1 - 0.35 * t)))
    lay.putalpha(ImageChops.multiply(lay.getchannel("A"), fade.resize(lay.size)))
    return done(lay)


def hot():
    """뜨겁다: 김이 올라오는 붉은 곡선 3개만."""
    return steam((72, 128, 184), 20, 232, 13, 26, (255, 70, 60), (255, 180, 80))


def hot_cup():
    """뜨겁다: 머그잔 + 위로 올라오는 김."""
    base = put(canvas(), emoji("Hot beverage", 0.7), 124, 182)
    base.alpha_composite(steam((92, 124, 156), 6, 100, 7, 15, (255, 80, 60), (255, 180, 90)))
    return base


def fried_egg():
    """계란후라이: 울퉁불퉁한 흰자 + 볼록한 노른자."""
    import math
    im = big()
    cx, cy = 128, 136
    pts = []
    for k in range(180):
        a = 2 * math.pi * k / 180
        r = 100 + 9 * math.sin(3 * a + 0.6) + 6 * math.sin(5 * a + 2.1) + 4 * math.sin(8 * a)
        pts.append(s(cx + r * math.cos(a), cy + r * 0.78 * math.sin(a)))
    # 그림자
    sh = Image.new("RGBA", im.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).polygon([(x, y + 8 * SS) for x, y in pts], fill=(60, 70, 110, 70))
    im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(8 * SS)))
    # 흰자: 가장자리는 살짝 노릇, 안쪽은 하얗게
    mask = Image.new("L", im.size, 0)
    ImageDraw.Draw(mask).polygon(pts, fill=255)
    edge = Image.new("RGBA", im.size, (246, 222, 180, 255))
    white = Image.new("RGBA", im.size, (255, 255, 255, 255))
    inner = mask.filter(ImageFilter.GaussianBlur(10 * SS)).point(lambda v: max(0, v * 2 - 255))
    body = Image.composite(white, edge, inner)
    eggw = Image.new("RGBA", im.size, (0, 0, 0, 0))
    eggw.paste(body, (0, 0), mask)
    im.alpha_composite(eggw)
    # 흰자 아래쪽 그늘 (입체감)
    shade = Image.new("L", im.size, 0)
    ImageDraw.Draw(shade).ellipse(s(cx - 90, cy + 10, cx + 100, cy + 100), fill=55)
    shade = Image.composite(shade, Image.new("L", im.size, 0), mask).filter(ImageFilter.GaussianBlur(14 * SS))
    tone = Image.new("RGBA", im.size, (170, 180, 220, 0))
    tone.putalpha(shade)
    im.alpha_composite(tone)
    # 노른자: 방사형 그라데이션
    yx, yy, yr = cx - 6, cy - 8, 40
    for k in range(yr * SS, 0, -SS):
        t = k / (yr * SS)
        col = (255, int(214 - 62 * t), int(70 - 50 * t), 255)
        ImageDraw.Draw(im).ellipse((yx * SS - k, yy * SS - k * 0.92, yx * SS + k, yy * SS + k * 0.92), fill=col)
    # 노른자 테두리 그늘 + 반사광
    ring = Image.new("RGBA", im.size, (0, 0, 0, 0))
    ImageDraw.Draw(ring).ellipse(s(yx - yr, yy - yr * 0.92 + 4, yx + yr, yy + yr * 0.92 + 4), outline=(220, 120, 20, 120), width=4 * SS)
    im.alpha_composite(ring.filter(ImageFilter.GaussianBlur(2 * SS)))
    hl = Image.new("RGBA", im.size, (0, 0, 0, 0))
    ImageDraw.Draw(hl).ellipse(s(yx - 24, yy - 26, yx - 4, yy - 12), fill=(255, 255, 240, 230))
    im.alpha_composite(hl.filter(ImageFilter.GaussianBlur(3 * SS)))
    return done(im)


def take_out():
    """바구니에서 사과를 집어 올리는 손 + 위로 올라가는 움직임 선."""
    base = put(canvas(), emoji("Basket", 0.78), 128, 170)
    lines = big()
    d = ImageDraw.Draw(lines)
    for x, y0, y1 in ((100, 114, 136), (128, 120, 144), (156, 114, 136)):
        d.rounded_rectangle(s(x - 3.5, y0, x + 3.5, y1), 4 * SS, fill=(150, 170, 220, 230))
    base.alpha_composite(done(lines.filter(ImageFilter.GaussianBlur(SS))))
    put(base, emoji("Red apple", 0.42), 128, 76)
    return put(base, emoji("Pinching hand", 0.5, rotate=-160), 130, 32)


WOOD = ((232, 176, 110), (176, 112, 58))


def wood_bar(im, box, radius=6, vertical=True, hl=True):
    layer, mask = grad_shape(im.size, s(*box), *WOOD, radius * SS, vertical=not vertical)
    im.alpha_composite(layer)
    if hl:
        x0, y0, x1, y1 = box
        hb = (x0, y0, x0 + (x1 - x0) * 0.4, y1) if vertical else (x0, y0, x1, y0 + (y1 - y0) * 0.4)
        highlight(im, mask, s(*hb), alpha=70, blur=2)


def signpost():
    """표지판: 나무 기둥 + 양쪽을 가리키는 화살표 판 2개."""
    im = big()
    shadow(im, s(112, 30, 144, 246), 8 * SS, color=(120, 70, 30, 50), dy=4, blur=5)
    wood_bar(im, (114, 28, 142, 246), 8)
    for (x0, x1, y, right, c0, c1) in ((96, 230, 52, True, (120, 200, 120), (52, 140, 70)),
                                       (26, 160, 122, False, (110, 180, 236), (44, 116, 200))):
        tip = 26
        pts = ([(x0, y), (x1 - tip, y), (x1, y + 24), (x1 - tip, y + 48), (x0, y + 48)] if right else
               [(x1, y), (x0 + tip, y), (x0, y + 24), (x0 + tip, y + 48), (x1, y + 48)])
        mask = Image.new("L", im.size, 0)
        ImageDraw.Draw(mask).polygon([s(*p) for p in pts], fill=255)
        mask = mask.filter(ImageFilter.GaussianBlur(SS))
        sh = Image.new("RGBA", im.size, (40, 60, 40, 60))
        sh.putalpha(mask.point(lambda v: v * 60 // 255).filter(ImageFilter.GaussianBlur(5 * SS)))
        im.alpha_composite(sh, (0, 4 * SS))
        layer, _ = grad_shape(im.size, s(min(x0, x1), y, max(x0, x1), y + 48), c0, c1, 0)
        board = Image.new("RGBA", im.size, (0, 0, 0, 0))
        board.paste(layer, (0, 0), mask)
        im.alpha_composite(board)
        highlight(im, mask, s(x0, y, x1, y + 16), alpha=80, blur=3)
        d = ImageDraw.Draw(im)
        for k in range(3):
            lx = (x0 + 24 + k * 30) if right else (x1 - 54 - k * 30)
            d.rounded_rectangle(s(lx, y + 21, lx + 22, y + 27), 3 * SS, fill=(255, 255, 255, 200))
    return done(im)


def stairs():
    """계단: 오른쪽 위로 올라가는 돌계단 4칸."""
    im = big()
    n, x0, y_bot, step_w, step_h = 4, 30, 232, 49, 46
    sh = Image.new("RGBA", im.size, (0, 0, 0, 0))
    pts = [s(x0, y_bot)] + [p for k in range(n) for p in (s(x0 + k * step_w, y_bot - (k + 1) * step_h),
                                                         s(x0 + (k + 1) * step_w, y_bot - (k + 1) * step_h))]
    ImageDraw.Draw(sh).polygon(pts + [s(x0 + n * step_w, y_bot)], fill=(40, 50, 90, 70))
    im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(7 * SS)), (0, 5 * SS))
    for k in range(n):
        x = x0 + k * step_w
        top = y_bot - (k + 1) * step_h
        layer, mask = grad_shape(im.size, s(x, top, x0 + n * step_w, y_bot), (214, 208, 200), (150, 142, 134), 4 * SS)
        im.alpha_composite(layer)
        d = ImageDraw.Draw(im)
        d.rounded_rectangle(s(x, top, x0 + n * step_w, top + 10), 4 * SS, fill=(240, 236, 230, 255))
        d.line(s(x, top + 10, x0 + n * step_w, top + 10), fill=(120, 112, 104, 180), width=SS * 2)
    return done(im)


def tumbler():
    """텀블러: 스테인리스 원통 + 검은 뚜껑."""
    im = big()
    body = (84, 64, 172, 238)
    shadow(im, s(*body), 22 * SS, dy=6, blur=8)
    layer, mask = grad_shape(im.size, s(*body), (110, 196, 190), (40, 120, 126), 22 * SS, vertical=False)
    im.alpha_composite(layer)
    highlight(im, mask, s(92, 64, 116, 238), alpha=110, blur=3)
    d = ImageDraw.Draw(im)
    d.rounded_rectangle(s(84, 96, 172, 104), 2 * SS, fill=(30, 96, 100, 120))
    lid = (78, 22, 178, 70)
    layer, mask = grad_shape(im.size, s(*lid), (96, 100, 112), (40, 42, 52), 14 * SS, vertical=False)
    im.alpha_composite(layer)
    highlight(im, mask, s(86, 22, 108, 70), alpha=90, blur=3)
    d.rounded_rectangle(s(110, 12, 146, 26), 6 * SS, fill=(60, 62, 72, 255))
    return done(im)


def railing():
    """난간: 나무 기둥 3개 + 위쪽 손잡이 봉 (살짝 오르막)."""
    im = big()
    lay = big()
    for x in (40, 118, 196):
        wood_bar(lay, (x, 80, x + 22, 236), 6)
    wood_bar(lay, (22, 66, 236, 88), 11, vertical=False)
    wood_bar(lay, (30, 150, 228, 164), 7, vertical=False)
    im.alpha_composite(lay.rotate(8, Image.BICUBIC, center=s(128, 150)))
    return done(im)


def fence():
    """울타리: 끝이 뾰족한 나무 판자 5개 + 가로대 2개."""
    im = big()
    shadow(im, s(18, 50, 238, 230), 8 * SS, color=(120, 70, 30, 40), dy=5, blur=6)
    for k in range(5):
        x = 24 + k * 44
        mask = Image.new("L", im.size, 0)
        ImageDraw.Draw(mask).polygon([s(x, 72), s(x + 17, 46), s(x + 34, 72), s(x + 34, 228), s(x, 228)], fill=255)
        layer, _ = grad_shape(im.size, s(x, 46, x + 34, 228), *WOOD, 0, vertical=False)
        board = Image.new("RGBA", im.size, (0, 0, 0, 0))
        board.paste(layer, (0, 0), mask)
        im.alpha_composite(board)
        highlight(im, mask, s(x, 46, x + 12, 228), alpha=70, blur=2)
    for y in (100, 180):
        shadow(im, s(14, y, 242, y + 20), 6 * SS, color=(90, 50, 20, 70), dy=3, blur=3)
        wood_bar(im, (14, y, 242, y + 20), 6, vertical=False)
    return done(im)


def dumbbell():
    """운동기구: 덤벨 (회색 원판 + 손잡이 봉), 살짝 기울임."""
    im = big()
    shadow(im, s(24, 100, 232, 170), 20 * SS, dy=8, blur=8)
    layer, mask = grad_shape(im.size, s(70, 120, 186, 148), (220, 224, 232), (130, 136, 150), 10 * SS)
    im.alpha_composite(layer)
    for x0 in (26, 186):
        for dx, h in ((0, 52), (24, 70)) if x0 == 26 else ((20, 52), (-4, 70)):
            box = (x0 + dx, 134 - h, x0 + dx + 22 + (0 if h == 52 else 4), 134 + h)
            box = (box[0], 134 - h / 1.5, box[2], 134 + h / 1.5)
            layer, mask = grad_shape(im.size, s(*box), (96, 100, 116), (36, 38, 50), 9 * SS, vertical=False)
            im.alpha_composite(layer)
            highlight(im, mask, s(box[0], box[1], box[0] + 8, box[3]), alpha=90, blur=2)
    return done(im.rotate(-14, Image.BICUBIC))


RECIPES = {
    "표지판": signpost,
    "계단": stairs,
    "텀블러": tumbler,
    "난간": railing,
    "울타리": fence,
    "운동기구": dumbbell,
    "가다": lambda: put(put(canvas(), emoji("Dashing away", 0.5), 58, 170), emoji("Person walking facing right", 0.86), 148, 128),
    "힘들다": lambda: put(put(canvas(), emoji("Weary face", 0.8), 108, 142), emoji("Sweat droplets", 0.42), 210, 52),
    "사람들": lambda: put(put(put(canvas(), emoji("Woman", 0.56), 66, 104), emoji("Person curly hair", 0.56), 190, 104), emoji("Man", 0.64), 128, 168),
    "소원": lambda: put(put(put(canvas(), emoji("Folded hands", 0.8), 120, 140), emoji("Sparkles", 0.42), 200, 62), emoji("Glowing star", 0.3), 52, 64),
    "꺼내다": take_out,
    "참치": tuna_can,
    "계란후라이": fried_egg,
    "뜨겁다": hot_cup,
    "뜨겁다_곡선만": hot,
    "냉장고": fridge,
    "도마": cutting_board,
    "파": green_onion,
    "부엌": lambda: put(put(canvas(), emoji("House", 0.8), 108, 104), emoji("Cooking", 0.58), 180, 182),
    "김치": lambda: put(put(canvas(), tint(hue_shift(emoji("Leafy green", 0.9), -100, 1.1), (1.35, 1.1, 1.0)), 120, 124), emoji("Hot pepper", 0.45), 196, 196),
    "기름": lambda: put(put(canvas(), colorize(emoji("Droplet", 0.9), (150, 92, 0), (255, 236, 130)), 116, 120), emoji("Olive", 0.48), 190, 194),
    "컵": lambda: tint(emoji("Glass of milk"), (0.72, 0.88, 1.05)),
    "재료": lambda: put(put(put(canvas(), emoji("Carrot", 0.6), 178, 92), emoji("Onion", 0.6), 76, 100), emoji("Egg", 0.5), 132, 178),
    "뚜껑": jar_lid,
    "열다": door_open,
    "씻다": lambda: put(put(put(canvas(), emoji("Raised hand", 0.82), 116, 136), emoji("Bubbles", 0.5), 196, 70), emoji("Bubbles", 0.32), 52, 206),
    "썰다": lambda: put(put(canvas(), emoji("Onion", 0.62), 96, 166), emoji("Kitchen knife", 0.7, rotate=-20), 166, 92),
    "섞다": lambda: put(put(canvas(), emoji("Bowl with spoon", 0.85), 120, 150), emoji("Cyclone", 0.42), 198, 62),
    "끄다": lambda: dim(emoji("Light bulb")),
    "설거지하다": lambda: put(put(put(canvas(), emoji("Bowl with spoon", 0.75), 104, 154), emoji("Sponge", 0.5), 196, 190), emoji("Bubbles", 0.48), 190, 64),
    "짜다": lambda: put(put(canvas(), emoji("Squinting face with tongue", 0.82), 112, 120), emoji("Salt", 0.5), 196, 186),
    "배고프다": lambda: put(put(canvas(), emoji("Pleading face", 0.82), 112, 120), emoji("Fork and knife", 0.5), 196, 186),
    "목마르다": lambda: put(put(canvas(), emoji("Pleading face", 0.82), 112, 120), emoji("Droplet", 0.45), 198, 188),
}


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    names = sys.argv[1:] or list(RECIPES)
    for n in names:
        RECIPES[n]().save(os.path.join(OUT, f"{n}.png"))
        print("made", n)
