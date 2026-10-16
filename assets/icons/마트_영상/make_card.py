"""카드(신용카드·체크카드) 아이콘 생성기 — 앞면(IC칩·카드 번호).

'계산하다' 아이콘(Fluent Credit card)은 카드 뒷면이라, 헷갈리지 않게 앞면으로 직접 그린다.
- 3d/카드.png

필요 패키지: pillow
실행: python make_card.py
"""
import os

from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
SS = 4
W = H = 256


def card():
    big = Image.new("RGBA", (W * SS, H * SS), (0, 0, 0, 0))
    x0, y0, x1, y1 = 16 * SS, 56 * SS, 240 * SS, 200 * SS
    r = 18 * SS
    # 그림자
    sh = Image.new("RGBA", big.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle((x0 + 4 * SS, y0 + 8 * SS, x1 + 4 * SS, y1 + 8 * SS), r, fill=(50, 30, 120, 100))
    big.alpha_composite(sh.filter(ImageFilter.GaussianBlur(8 * SS)))
    # 몸체: 왼쪽 위 보라 → 오른쪽 아래 파랑 대각선 그라데이션
    grad = Image.new("RGBA", big.size, (0, 0, 0, 0))
    gd = ImageDraw.Draw(grad)
    c0, c1 = (124, 92, 255), (46, 160, 255)
    span = (x1 - x0) + (y1 - y0)
    for k in range(0, span, SS):
        t = k / span
        col = tuple(int(c0[i] + (c1[i] - c0[i]) * t) for i in range(3)) + (255,)
        gd.line((x0 + k, y0, x0, y0 + k), fill=col, width=SS + 2)
        gd.line((x0 + k - (y1 - y0), y1, x0 + k, y0), fill=col, width=SS + 2)
    mask = Image.new("L", big.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle((x0, y0, x1, y1), r, fill=255)
    body = Image.new("RGBA", big.size, (0, 0, 0, 0))
    body.paste(grad, (0, 0), mask)
    # 위쪽 하이라이트 (3D 느낌)
    hl = Image.new("L", big.size, 0)
    ImageDraw.Draw(hl).rounded_rectangle((x0, y0, x1, y0 + 50 * SS), r, fill=60)
    hl = Image.composite(hl, Image.new("L", big.size, 0), mask).filter(ImageFilter.GaussianBlur(6 * SS))
    white = Image.new("RGBA", big.size, (255, 255, 255, 0))
    white.putalpha(hl)
    body.alpha_composite(white)
    big.alpha_composite(body)

    d = ImageDraw.Draw(big)
    # IC칩
    cx0, cy0 = 38 * SS, 92 * SS
    d.rounded_rectangle((cx0, cy0, cx0 + 40 * SS, cy0 + 30 * SS), 6 * SS, fill=(250, 210, 90, 255), outline=(200, 150, 40, 255), width=SS)
    for yy in (cy0 + 10 * SS, cy0 + 20 * SS):
        d.line((cx0 + 2 * SS, yy, cx0 + 38 * SS, yy), fill=(200, 150, 40, 255), width=SS)
    d.line((cx0 + 20 * SS, cy0 + 2 * SS, cx0 + 20 * SS, cy0 + 28 * SS), fill=(200, 150, 40, 255), width=SS)
    # 비접촉 결제 표시 ))))
    for k, rr in enumerate((8, 14, 20)):
        bx, by = 90 * SS, 107 * SS
        d.arc((bx - rr * SS, by - rr * SS, bx + rr * SS, by + rr * SS), -45, 45, fill=(255, 255, 255, 220), width=3 * SS)
    # 카드 번호
    font = ImageFont.truetype("C:/Windows/Fonts/consolab.ttf", 15 * SS)
    d.text((38 * SS, 150 * SS), "••••  ••••  ••••  1234", font=font, fill=(255, 255, 255, 240), anchor="lm")
    # 카드사 로고 (겹친 원 두 개)
    lx, ly, lr = 196 * SS, 178 * SS, 12 * SS
    logo = Image.new("RGBA", big.size, (0, 0, 0, 0))
    ld = ImageDraw.Draw(logo)
    ld.ellipse((lx - lr - 8 * SS, ly - lr, lx + lr - 8 * SS, ly + lr), fill=(255, 95, 90, 230))
    ld.ellipse((lx - lr + 8 * SS, ly - lr, lx + lr + 8 * SS, ly + lr), fill=(255, 190, 60, 210))
    big.alpha_composite(logo)
    return big.resize((W, H), Image.LANCZOS)


if __name__ == "__main__":
    card().save(os.path.join(HERE, "3d", "카드.png"))
    print("done")
