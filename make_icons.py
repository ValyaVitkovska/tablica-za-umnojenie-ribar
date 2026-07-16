from pathlib import Path
from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parent
ICON_DIR = ROOT / "icons"
ICON_DIR.mkdir(exist_ok=True)


def make_icon(size: int, maskable: bool = False) -> Image.Image:
    image = Image.new("RGBA", (size, size), "#0288D1")
    draw = ImageDraw.Draw(image)
    unit = size / 512

    # Sky, sun and water.
    draw.rectangle((0, 0, size, size * 0.48), fill="#81D4FA")
    draw.ellipse((350 * unit, 45 * unit, 455 * unit, 150 * unit), fill="#FFEB3B")
    draw.rectangle((0, size * 0.45, size, size), fill="#0277BD")
    for y, color in ((245, "#4FC3F7"), (305, "#29B6F6"), (370, "#01579B")):
        points = []
        for x in range(-40, 553, 32):
            points.append((x * unit, (y + (14 if (x // 32) % 2 else -14)) * unit))
        points += [(size, size), (0, size)]
        draw.polygon(points, fill=color)

    # Fish.
    fish_box = (105 * unit, 225 * unit, 350 * unit, 390 * unit)
    draw.ellipse(fish_box, fill="#FF7043", outline="#BF360C", width=max(2, int(9 * unit)))
    draw.polygon(
        [(115 * unit, 305 * unit), (40 * unit, 245 * unit), (42 * unit, 365 * unit)],
        fill="#FFB74D",
        outline="#BF360C"
    )
    draw.ellipse((286 * unit, 265 * unit, 318 * unit, 297 * unit), fill="white")
    draw.ellipse((298 * unit, 274 * unit, 313 * unit, 289 * unit), fill="#263238")

    # Multiplication sign.
    line_width = max(6, int(20 * unit))
    draw.line((365 * unit, 230 * unit, 460 * unit, 365 * unit), fill="white", width=line_width)
    draw.line((460 * unit, 230 * unit, 365 * unit, 365 * unit), fill="white", width=line_width)

    if maskable:
        # Subtle safe-zone ring to keep the important artwork centered.
        draw.ellipse((52 * unit, 52 * unit, 460 * unit, 460 * unit), outline=(255, 255, 255, 55), width=max(2, int(3 * unit)))
    return image


make_icon(192).save(ICON_DIR / "icon-192.png", optimize=True)
make_icon(512).save(ICON_DIR / "icon-512.png", optimize=True)
make_icon(512, maskable=True).save(ICON_DIR / "icon-maskable-512.png", optimize=True)
