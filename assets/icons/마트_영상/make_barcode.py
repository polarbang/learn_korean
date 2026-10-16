"""바코드 아이콘 + 스캔 애니메이션 생성기.

- 3d/바코드.png : 입체감 있는 흰 라벨 위 EAN-13 바코드 (880 = 한국 상품코드)
- mov/바코드_스캔.mov : 빨간 레이저가 위아래로 훑고 '삑' 하고 초록 테두리가 번쩍 (ProRes 4444, 투명 배경, CapCut용)

필요 패키지: pillow, imageio-ffmpeg
실행: python make_barcode.py
"""
import os
import subprocess

import imageio_ffmpeg
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
SS = 4
W = H = 256
CODE = "880123456789"  # 체크 숫자는 자동 계산

L = ["0001101", "0011001", "0010011", "0111101", "0100011", "0110001", "0101111", "0111011", "0110111", "0001011"]
G = ["0100111", "0110011", "0011011", "0100001", "0011101", "0111001", "0000101", "0010001", "0001001", "0010111"]
R = ["1110010", "1100110", "1101100", "1000010", "1011100", "1001110", "1010000", "1000100", "1001000", "1110100"]
PARITY = ["LLLLLL", "LLGLGG", "LLGGLG", "LLGGGL", "LGLLGG", "LGGLLG", "LGGGLL", "LGLGLG", "LGLGGL", "LGGLGL"]


def ean13(code12):
    s = sum(int(d) * (3 if i % 2 else 1) for i, d in enumerate(code12))
    full = code12 + str((10 - s % 10) % 10)
    first, left, right = int(full[0]), full[1:7], full[7:]
    bits = "101"
    for d, p in zip(left, PARITY[first]):
        bits += (L if p == "L" else G)[int(d)]
    bits += "01010"
    for d in right:
        bits += R[int(d)]
    bits += "101"
    return full, bits


def label():
    full, bits = ean13(CODE)
    big = Image.new("RGBA", (W * SS, H * SS), (0, 0, 0, 0))
    x0, y0, x1, y1 = 20 * SS, 44 * SS, 236 * SS, 212 * SS
    # 그림자
    sh = Image.new("RGBA", big.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle((x0 + 4 * SS, y0 + 8 * SS, x1 + 4 * SS, y1 + 8 * SS), 22 * SS, fill=(60, 50, 120, 90))
    big.alpha_composite(sh.filter(ImageFilter.GaussianBlur(8 * SS)))
    # 라벨 (위는 흰색, 아래로 갈수록 연보라 — Fluent 3D 톤)
    card = Image.new("RGBA", big.size, (0, 0, 0, 0))
    grad = Image.new("RGBA", big.size, (0, 0, 0, 0))
    gd = ImageDraw.Draw(grad)
    for y in range(y0, y1):
        t = (y - y0) / (y1 - y0)
        gd.line((x0, y, x1, y), fill=(int(255 - 20 * t), int(255 - 22 * t), 255, 255))
    mask = Image.new("L", big.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle((x0, y0, x1, y1), 22 * SS, fill=255)
    card.paste(grad, (0, 0), mask)
    big.alpha_composite(card)
    # 막대
    d = ImageDraw.Draw(big)
    module = 7  # 1.75px (SS 4배 기준) — 왼쪽 첫 숫자 자리 확보
    bx = (W * SS - len(bits) * module) // 2
    top, bot, guard_bot = 66 * SS, 166 * SS, 176 * SS
    guards = {i for i in list(range(3)) + list(range(45, 50)) + list(range(92, 95))}
    for i, b in enumerate(bits):
        if b == "1":
            d.rectangle((bx + i * module, top, bx + (i + 1) * module - 1, guard_bot if i in guards else bot), fill=(28, 28, 40, 255))
    # 숫자
    font = ImageFont.truetype("C:/Windows/Fonts/consola.ttf", 17 * SS)
    d.text((bx - 12 * SS, 172 * SS), full[0], font=font, fill=(28, 28, 40, 255), anchor="lm")
    d.text((bx + 24 * module, 180 * SS), full[1:7], font=font, fill=(28, 28, 40, 255), anchor="mm")
    d.text((bx + 71 * module, 180 * SS), full[7:], font=font, fill=(28, 28, 40, 255), anchor="mm")
    return big.resize((W, H), Image.LANCZOS)


def scan_frames(base, fps=30):
    frames = []
    top, bot = 62, 182
    sweep = 30  # 1초: 아래로 갔다가 위로
    for f in range(60):
        img = base.copy()
        if f < sweep:
            t = f / (sweep - 1)
            y = top + (bot - top) * (1 - abs(1 - 2 * t))
            glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            gd = ImageDraw.Draw(glow)
            gd.rectangle((14, y - 5, W - 14, y + 5), fill=(255, 40, 40, 140))
            img.alpha_composite(glow.filter(ImageFilter.GaussianBlur(5)))
            ImageDraw.Draw(img).line((14, y, W - 14, y), fill=(255, 30, 30, 255), width=3)
        elif f < sweep + 12:  # '삑' — 초록 테두리 번쩍
            a = int(255 * (1 - (f - sweep) / 12))
            ring = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            ImageDraw.Draw(ring).rounded_rectangle((16, 40, 240, 216), 24, outline=(52, 199, 89, a), width=8)
            img.alpha_composite(ring)
        frames.append(img)
    return frames


def encode(frames, path):
    ff = imageio_ffmpeg.get_ffmpeg_exe()
    p = subprocess.Popen([ff, "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgba", "-s", f"{W}x{H}",
                          "-r", "30", "-i", "-", "-c:v", "prores_ks", "-profile:v", "4",
                          "-pix_fmt", "yuva444p10le", "-vendor", "apl0", path], stdin=subprocess.PIPE)
    for fr in frames:
        p.stdin.write(fr.tobytes())
    p.stdin.close()
    if p.wait() != 0:
        raise RuntimeError(path)


if __name__ == "__main__":
    base = label()
    base.save(os.path.join(HERE, "3d", "바코드.png"))
    os.makedirs(os.path.join(HERE, "mov"), exist_ok=True)
    frames = scan_frames(base)
    encode(frames, os.path.join(HERE, "mov", "바코드_스캔.mov"))
    # 확인용 프레임
    strip = Image.new("RGBA", (4 * W, H), (110, 120, 130, 255))
    for i, f in enumerate([0, 8, 15, 33]):
        strip.alpha_composite(frames[f], (i * W, 0))
    strip.save(os.path.join(os.environ.get("TEMP", HERE), "barcode_strip.png"))
    print("done", ean13(CODE)[0])
