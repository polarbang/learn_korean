"""공용 강조 에셋(동그라미·네모·밑줄·화살표 등) 생성기.

손으로 그린 듯한 마커 선이 그려지는(draw-on) 애니메이션을 만든다.
출력: mov/ (ProRes 4444, 투명 배경 — CapCut에서 사용), png/ (완성 정지 이미지),
      _preview/ (VP9 webm — preview.html 브라우저 미리보기 전용, CapCut에서는 배경이 검게 나옴)

필요 패키지: pillow, imageio-ffmpeg  (pip install pillow imageio-ffmpeg)
실행: python make_overlays.py            (전체)
      python make_overlays.py numbers    (일부만: lines / hands / numbers)
"""
import math
import os
import subprocess
import sys

import urllib.request

import imageio_ffmpeg
from PIL import Image, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()

SS = 3            # 슈퍼샘플링 배율 (안티앨리어싱)
FPS = 30
DRAW_FRAMES = 15  # 0.5초 동안 그려짐
HOLD_FRAMES = 45  # 1.5초 유지 (편집 때 길이 조절)
STROKE = 14       # 선 두께(px)
COLORS = {
    "red": (255, 59, 48),
    "yellow": (255, 214, 10),
    "white": (255, 255, 255),
    "black": (20, 20, 20),
}


def wobble(pts, amp, seed):
    """경로 법선 방향으로 부드러운 흔들림을 줘서 손그림 느낌을 낸다."""
    out = []
    n = len(pts)
    for i, (x, y) in enumerate(pts):
        t = i / max(n - 1, 1)
        d = amp * (math.sin(t * 7.0 + seed) * 0.6 + math.sin(t * 13.0 + seed * 2.1) * 0.4)
        j0, j1 = max(i - 1, 0), min(i + 1, n - 1)
        dx, dy = pts[j1][0] - pts[j0][0], pts[j1][1] - pts[j0][1]
        ln = math.hypot(dx, dy) or 1
        out.append((x - dy / ln * d, y + dx / ln * d))
    return out


def bezier(p0, p1, p2, n=80):
    return [((1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t * t * p2[0],
             (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t * t * p2[1])
            for t in (i / (n - 1) for i in range(n))]


def arrow_head(tip, prev, size=58, spread=28):
    ang = math.atan2(tip[1] - prev[1], tip[0] - prev[0])
    strokes = []
    for s in (spread, -spread):
        a = ang + math.radians(180 - s)
        strokes.append([tip, (tip[0] + size * math.cos(a), tip[1] + size * math.sin(a))])
    return strokes


# 각 도형: (가로, 세로, [(점 목록, 시작 비율, 끝 비율), ...])
def shapes():
    s = {}

    # 동그라미: 시작점을 살짝 지나치며 닫히는 손그림 타원
    w, h = 640, 380
    cx, cy, rx, ry = w / 2, h / 2, 285, 160
    pts = []
    for i in range(160):
        t = i / 159
        a = math.radians(-110 + t * 390)
        k = 0.95 + 0.11 * t  # 끝이 시작점보다 바깥으로 지나가게 (겹침 방지)
        pts.append((cx + rx * k * math.cos(a), cy + ry * k * math.sin(a)))
    s["circle"] = (w, h, [(wobble(pts, 4, 1.3), 0, 1)])

    # 원: 같은 손그림 방식의 정원
    w = h = 400
    c, r = w / 2, 165
    pts = []
    for i in range(160):
        t = i / 159
        a = math.radians(-110 + t * 390)
        k = 0.95 + 0.11 * t
        pts.append((c + r * k * math.cos(a), c + r * k * math.sin(a)))
    s["circle_round"] = (w, h, [(wobble(pts, 3.5, 2.4), 0, 1)])

    # 네모: 둥근 모서리 3개 + 왼쪽 위는 두 선이 교차하는 손그림 모서리
    w, h = 640, 360
    x0, y0, x1, y1, r = 40, 40, w - 40, h - 40, 26
    corners = [((x1 - r, y0 + r), -90), ((x1 - r, y1 - r), 0), ((x0 + r, y1 - r), 90)]
    pts = [(x0 - 16, y0 + 3)]  # 윗변은 왼쪽 모서리보다 조금 앞에서 시작
    for (ccx, ccy), start in corners:
        for k in range(12):
            a = math.radians(start + k * 90 / 11)
            pts.append((ccx + r * math.cos(a), ccy + r * math.sin(a)))
    pts.append((x0 + 3, y0 - 18))  # 왼쪽 변은 윗변을 지나쳐서 끝남
    dense = []
    for a, b in zip(pts, pts[1:]):
        steps = max(int(math.hypot(b[0] - a[0], b[1] - a[1]) / 6), 1)
        dense += [(a[0] + (b[0] - a[0]) * i / steps, a[1] + (b[1] - a[1]) * i / steps) for i in range(steps)]
    dense.append(pts[-1])
    s["rect"] = (w, h, [(wobble(dense, 2.5, 0.7), 0, 1)])

    # 밑줄: 살짝 처지는 곡선
    w, h = 640, 90
    s["underline"] = (w, h, [(wobble(bezier((24, 42), (w / 2, 58), (w - 24, 38)), 2, 2.2), 0, 1)])

    # 두 줄 밑줄: 윗줄이 먼저, 더 긴 아랫줄이 이어서 그려짐
    w, h = 640, 120
    top = wobble(bezier((90, 42), (w / 2, 52), (w - 90, 38)), 1.8, 0.9)
    bottom = wobble(bezier((24, 78), (w / 2, 92), (w - 24, 72)), 2, 2.6)
    s["underline_double"] = (w, h, [(top, 0, 0.42), (bottom, 0.5, 1)])

    # 직선 화살표 (오른쪽 방향, 편집에서 회전)
    w, h = 560, 220
    shaft = wobble(bezier((30, 140), (w / 2, 120), (w - 40, 96)), 2, 0.4)
    heads = arrow_head(shaft[-1], shaft[-6])
    s["arrow"] = (w, h, [(shaft, 0, 0.72), (heads[0], 0.72, 0.86), (heads[1], 0.86, 1)])

    # 휘어진 화살표 (아래에서 위로 올라가 오른쪽을 가리킴)
    w, h = 420, 420
    shaft = wobble(bezier((70, 370), (60, 90), (360, 80)), 2, 1.9)
    heads = arrow_head(shaft[-1], shaft[-6])
    s["arrow_curved"] = (w, h, [(shaft, 0, 0.72), (heads[0], 0.72, 0.86), (heads[1], 0.86, 1)])

    # 체크
    w, h = 320, 280
    pts = [(40, 150), (115, 225), (285, 45)]
    dense = []
    for a, b in zip(pts, pts[1:]):
        dense += [(a[0] + (b[0] - a[0]) * i / 30, a[1] + (b[1] - a[1]) * i / 30) for i in range(30)]
    dense.append(pts[-1])
    s["check"] = (w, h, [(dense, 0, 1)])

    # 엑스
    w, h = 280, 280
    s["cross"] = (w, h, [([(50, 50), (230, 230)], 0, 0.5), ([(230, 50), (50, 230)], 0.5, 1)])
    return s


def partial(pts, frac):
    """경로의 앞쪽 frac(0~1) 길이만큼만 잘라 돌려준다."""
    if frac <= 0:
        return []
    if frac >= 1:
        return pts
    seg = [math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(pts, pts[1:])]
    target = sum(seg) * frac
    out, acc = [pts[0]], 0
    for (a, b), l in zip(zip(pts, pts[1:]), seg):
        if acc + l >= target:
            r = (target - acc) / l if l else 0
            out.append((a[0] + (b[0] - a[0]) * r, a[1] + (b[1] - a[1]) * r))
            return out
        out.append(b)
        acc += l
    return out


def ease_out(t):
    return 1 - (1 - t) ** 3


def render(w, h, strokes, progress, color):
    W, H = w * SS, h * SS
    mask = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(mask)
    lw = STROKE * SS
    for pts, a, b in strokes:
        f = (progress - a) / (b - a) if b > a else 1
        seg = partial(pts, max(0.0, min(1.0, f)))
        if len(seg) < 2:
            continue
        sp = [(x * SS, y * SS) for x, y in seg]
        d.line(sp, fill=255, width=lw, joint="curve")
        for x, y in (sp[0], sp[-1]):
            d.ellipse((x - lw / 2, y - lw / 2, x + lw / 2, y + lw / 2), fill=255)
    mask = mask.resize((w, h), Image.LANCZOS)
    # 배경과 상관없이 보이도록 옅은 그림자 (검은 선은 어두운 배경용으로 흰 테두리)
    dark = sum(color) < 150
    shadow = mask.filter(ImageFilter.GaussianBlur(4)).point(lambda v: v * (0.5 if dark else 0.35))
    img = Image.new("RGBA", (w, h), (255, 255, 255, 0) if dark else (0, 0, 0, 0))
    img.putalpha(shadow)
    fg = Image.new("RGBA", (w, h), color + (0,))
    fg.putalpha(mask)
    img.alpha_composite(fg)
    return img


# 검지로 가리키는 손 (Fluent Emoji 3D, MIT) — 가리키는 방향으로 콕콕 찌르는 움직임
# 위를 가리키는 손 하나만 쓰고, 다른 방향은 편집기에서 회전한다
HANDS = {"up": (0, -1)}
HAND_URL = ("https://raw.githubusercontent.com/microsoft/fluentui-emoji/main/assets/"
            "Backhand%20index%20pointing%20{d}/Default/3D/backhand_index_pointing_{d}_3d_default.png")
HAND_SIZE = 220
POKE = 26  # 찌르는 거리(px)


def hand_frames(direction):
    src_dir = os.path.join(HERE, "_src")
    os.makedirs(src_dir, exist_ok=True)
    src = os.path.join(src_dir, f"hand_{direction}.png")
    if not os.path.exists(src):
        urllib.request.urlretrieve(HAND_URL.format(d=direction), src)
    hand = Image.open(src).convert("RGBA").resize((HAND_SIZE, HAND_SIZE), Image.LANCZOS)
    dx, dy = HANDS[direction]
    size = HAND_SIZE + POKE + 40
    frames = []
    total = DRAW_FRAMES + HOLD_FRAMES + 1
    for f in range(total):
        if f <= 6:  # 톡 튀어나오며 등장
            t = f / 6
            scale = 0.3 + 0.7 * (1 + 2.2 * (t - 1) ** 3 + 1.2 * (t - 1) ** 2)
            off = 0
        else:
            scale = 1
            c = (f - 7) / 16  # 16프레임에 한 번씩 콕, 두 번
            off = POKE * (0.5 - 0.5 * math.cos(2 * math.pi * c)) if c < 2 else 0
        img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        s = max(int(HAND_SIZE * scale), 1)
        hs = hand.resize((s, s), Image.LANCZOS)
        # 손가락 반대쪽으로 POKE/2 만큼 물러나 있다가 가리키는 방향으로 찌름
        x = (size - s) // 2 + int(dx * (off - POKE / 2))
        y = (size - s) // 2 + int(dy * (off - POKE / 2))
        img.alpha_composite(hs, (x, y))
        frames.append(img)
    return frames


# 숫자 1~9 (Fluent Emoji 3D 키캡, MIT) — 톡 튀어나오며 등장 후 유지
NUMBER_URL = ("https://raw.githubusercontent.com/microsoft/fluentui-emoji/main/assets/"
              "Keycap%20{n}/3D/keycap_{n}_3d.png")
NUMBER_SIZE = 220


def pop_scale(f, n=8):
    """0→살짝 크게(오버슈트)→1로 튀어나오는 크기 변화. n프레임 동안."""
    if f >= n:
        return 1.0
    t = f / n
    c = 1.70158 * 1.4
    return max(0.0, 1 + (c + 1) * (t - 1) ** 3 + c * (t - 1) ** 2)


def number_frames(n):
    src_dir = os.path.join(HERE, "_src")
    os.makedirs(src_dir, exist_ok=True)
    src = os.path.join(src_dir, f"number_{n}.png")
    if not os.path.exists(src):
        urllib.request.urlretrieve(NUMBER_URL.format(n=n), src)
    base = Image.open(src).convert("RGBA").resize((NUMBER_SIZE, NUMBER_SIZE), Image.LANCZOS)
    size = NUMBER_SIZE + 40  # 오버슈트 여유
    frames = []
    for f in range(DRAW_FRAMES + HOLD_FRAMES + 1):
        img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        s = int(NUMBER_SIZE * pop_scale(f))
        if s > 0:
            img.alpha_composite(base.resize((s, s), Image.LANCZOS), ((size - s) // 2, (size - s) // 2))
        frames.append(img)
    return frames


def write(frames, base):
    w, h = frames[0].size
    frames[-1].save(os.path.join(HERE, "png", base + ".png"))
    encode(frames, w, h, os.path.join(HERE, "mov", base + ".mov"),
           ["-c:v", "prores_ks", "-profile:v", "4", "-pix_fmt", "yuva444p10le", "-vendor", "apl0"])
    encode(frames, w, h, os.path.join(HERE, "_preview", base + ".webm"),
           ["-c:v", "libvpx-vp9", "-pix_fmt", "yuva420p", "-b:v", "0", "-crf", "30", "-auto-alt-ref", "0"])
    print("done", base)


def encode(frames, w, h, path, args):
    cmd = [FFMPEG, "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgba",
           "-s", f"{w}x{h}", "-r", str(FPS), "-i", "-"] + args + [path]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for fr in frames:
        p.stdin.write(fr.tobytes())
    p.stdin.close()
    if p.wait() != 0:
        raise RuntimeError(path)


def main():
    only = set(sys.argv[1:]) or {"lines", "hands", "numbers"}
    for sub in ("png", "mov", "_preview"):
        os.makedirs(os.path.join(HERE, sub), exist_ok=True)
    if "hands" in only:
        for d in HANDS:
            write(hand_frames(d), f"hand_{d}")
    if "numbers" in only:
        for n in range(1, 10):
            write(number_frames(n), f"number_{n}")
    if "lines" in only:
        for name, (w, h, strokes) in shapes().items():
            for cname, rgb in COLORS.items():
                frames = [render(w, h, strokes, ease_out(i / DRAW_FRAMES), rgb) for i in range(DRAW_FRAMES + 1)]
                frames += [frames[-1]] * HOLD_FRAMES
                write(frames, f"{name}_{cname}")


if __name__ == "__main__":
    main()
