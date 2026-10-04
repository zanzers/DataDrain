import math
from PIL import Image, ImageDraw

S = 1024                      
GREEN, TRACK, BG, DOT = "#a6e3a1", "#313244", "#1e1e2e", "#cdd6f4"

img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
d = ImageDraw.Draw(img)


d.rounded_rectangle((0, 0, S - 1, S - 1), radius=220, fill=BG)

# gauge ring: gray track + green arc (70% left)
pad, w = 200, 110
box = (pad, pad, S - pad, S - pad)
d.arc(box, 0, 360, fill=TRACK, width=w)

start = -90                      # 12 o'clock
end = start + 360 * 0.70
d.arc(box, start, end, fill=GREEN, width=w)

# round caps on both ends of the green arc
cx = cy = S / 2
r = (S - 2 * pad) / 2 - w / 2
for angle in (start, end):
    x = cx + r * math.cos(math.radians(angle))
    y = cy + r * math.sin(math.radians(angle))
    d.ellipse((x - w / 2, y - w / 2, x + w / 2, y + w / 2), fill=GREEN)

# center dot
d.ellipse((cx - 70, cy - 70, cx + 70, cy + 70), fill=DOT)

img.save("icon.png")
img.save("icon.ico", sizes=[(16, 16), (24, 24), (32, 32), (48, 48),
                            (64, 64), (128, 128), (256, 256)])
print("Created icon.png and icon.ico")