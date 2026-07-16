from pathlib import Path
from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parent
ICON_DIR = ROOT / "icons"
ICON_DIR.mkdir(exist_ok=True)


def make_icon(size: int, maskable: bool = False) -> Image.Image:
    # Render large, then downsample for smooth icon edges.
    render_size = max(1024, size * 3)
    unit = render_size / 512
    image = Image.new("RGBA", (render_size, render_size), (0, 0, 0, 0))

    # Soft vertical sky/water gradient clipped to an app-icon silhouette.
    backdrop = Image.new("RGBA", (render_size, render_size))
    backdrop_px = backdrop.load()
    for y in range(render_size):
        t = y / max(1, render_size - 1)
        if t < .45:
            local = t / .45
            top, bottom = (111, 211, 246), (38, 169, 224)
        else:
            local = (t - .45) / .55
            top, bottom = (3, 155, 229), (1, 64, 121)
        color = tuple(round(top[i] + (bottom[i] - top[i]) * local) for i in range(3)) + (255,)
        for x in range(render_size):
            backdrop_px[x, y] = color

    mask = Image.new("L", (render_size, render_size), 0)
    mask_draw = ImageDraw.Draw(mask)
    margin = 0 if maskable else int(12 * unit)
    radius = int((92 if maskable else 84) * unit)
    mask_draw.rounded_rectangle((margin, margin, render_size - margin, render_size - margin), radius=radius, fill=255)
    image.paste(backdrop, (0, 0), mask)
    draw = ImageDraw.Draw(image)

    # Sun and three clean wave bands.
    draw.ellipse((365 * unit, 48 * unit, 450 * unit, 133 * unit), fill="#FFE33D")
    for y, color, height in ((234, "#72D9FA", 34), (286, "#28B9ED", 39), (354, "#0277BD", 45)):
        points = []
        for x in range(-55, 570, 44):
            crest = y - height if (x // 44) % 2 == 0 else y
            points.append((x * unit, crest * unit))
        points.extend(((570 * unit, 520 * unit), (-55 * unit, 520 * unit)))
        draw.polygon(points, fill=color)

    # Friendly orange fish with fins and crisp outline.
    outline = max(5, int(9 * unit))
    draw.polygon(
        [(127 * unit, 315 * unit), (52 * unit, 251 * unit), (52 * unit, 378 * unit)],
        fill="#FFB347",
        outline="#B93A18"
    )
    draw.ellipse((105 * unit, 231 * unit, 366 * unit, 397 * unit), fill="#FF7043", outline="#B93A18", width=outline)
    draw.polygon(
        [(215 * unit, 246 * unit), (275 * unit, 187 * unit), (305 * unit, 255 * unit)],
        fill="#FFB347",
        outline="#B93A18"
    )
    draw.arc((135 * unit, 259 * unit, 338 * unit, 383 * unit), 20, 150, fill="#FFB596", width=max(3, int(7 * unit)))
    draw.ellipse((302 * unit, 271 * unit, 340 * unit, 309 * unit), fill="white")
    draw.ellipse((316 * unit, 283 * unit, 335 * unit, 302 * unit), fill="#16324A")
    draw.arc((330 * unit, 315 * unit, 370 * unit, 351 * unit), 90, 260, fill="#7A2711", width=max(3, int(6 * unit)))

    # Yellow multiplication badge, legible even at launcher size.
    draw.ellipse((342 * unit, 330 * unit, 477 * unit, 465 * unit), fill="#FFD740", outline="#7A4E00", width=max(4, int(8 * unit)))
    cross_width = max(7, int(17 * unit))
    draw.line((378 * unit, 369 * unit, 442 * unit, 427 * unit), fill="#17324D", width=cross_width)
    draw.line((442 * unit, 369 * unit, 378 * unit, 427 * unit), fill="#17324D", width=cross_width)

    # Small white ripples reinforce the fishing/water theme.
    for left, top, width in ((62, 432, 120), (205, 446, 92), (300, 477, 105)):
        draw.arc((left * unit, top * unit, (left + width) * unit, (top + 28) * unit), 190, 350, fill=(225, 247, 250, 220), width=max(2, int(4 * unit)))

    if maskable:
        draw.rounded_rectangle((8 * unit, 8 * unit, 504 * unit, 504 * unit), radius=88 * unit, outline=(255, 255, 255, 45), width=max(2, int(3 * unit)))

    return image.resize((size, size), Image.Resampling.LANCZOS)


make_icon(192).save(ICON_DIR / "icon-192.png", optimize=True)
make_icon(512).save(ICON_DIR / "icon-512.png", optimize=True)
make_icon(512, maskable=True).save(ICON_DIR / "icon-maskable-512.png", optimize=True)
