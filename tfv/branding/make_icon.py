"""Builds the Tampa FL VoIP Remote icon: company shield + remote-connection badge."""
from PIL import Image, ImageDraw

S = 1024  # master size; everything is drawn at 4x and downsampled for smooth edges
X = 4
W = S * X

shield = Image.open("logo-shield.png").convert("RGBA").resize((W, W), Image.LANCZOS)
canvas = Image.new("RGBA", (W, W), (0, 0, 0, 0))
canvas.alpha_composite(shield)

d = ImageDraw.Draw(canvas)

# Badge: circle bottom-right with white ring
cx, cy, r = int(W * 0.74), int(W * 0.74), int(W * 0.235)
ring = int(W * 0.022)
d.ellipse((cx - r - ring, cy - r - ring, cx + r + ring, cy + r + ring), fill=(255, 255, 255, 255))
d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(0, 168, 120, 255))  # green = connected

# Monitor
mw, mh = int(r * 1.15), int(r * 0.78)
mx0, my0 = cx - mw // 2, cy - int(r * 0.62)
lw = int(r * 0.09)
d.rounded_rectangle((mx0, my0, mx0 + mw, my0 + mh), radius=int(r * 0.08), outline="white", width=lw)
# stand
d.rectangle((cx - int(r * 0.07), my0 + mh, cx + int(r * 0.07), my0 + mh + int(r * 0.16)), fill="white")
d.rounded_rectangle((cx - int(r * 0.3), my0 + mh + int(r * 0.14), cx + int(r * 0.3), my0 + mh + int(r * 0.24)),
                    radius=int(r * 0.04), fill="white")

# Two-way arrows inside the screen
ay1, ay2 = my0 + int(mh * 0.36), my0 + int(mh * 0.66)
ax0, ax1 = mx0 + int(mw * 0.2), mx0 + int(mw * 0.8)
aw = int(r * 0.07)
h = int(r * 0.13)
d.line((ax0, ay1, ax1 - h // 2, ay1), fill="white", width=aw)
d.polygon([(ax1, ay1), (ax1 - h, ay1 - h), (ax1 - h, ay1 + h)], fill="white")
d.line((ax0 + h // 2, ay2, ax1, ay2), fill="white", width=aw)
d.polygon([(ax0, ay2), (ax0 + h, ay2 - h), (ax0 + h, ay2 + h)], fill="white")

master = canvas.resize((S, S), Image.LANCZOS)
master.save("tfv-remote-icon-1024.png")
for size in (512, 256, 192, 128, 64, 48, 32, 16):
    master.resize((size, size), Image.LANCZOS).save(f"tfv-remote-icon-{size}.png")
master.save("tfv-remote.ico", sizes=[(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)])
# iOS/Android need an opaque square: white background
opaque = Image.new("RGBA", (S, S), (255, 255, 255, 255))
opaque.alpha_composite(master)
opaque.convert("RGB").save("tfv-remote-icon-1024-opaque.png")
print("ok")
