from pathlib import Path
from PIL import Image, ImageChops

source = Path(r"C:\Users\User\Downloads\CLIENT PICTURES\Your Phenomenal Builder")
target = Path(__file__).resolve().parents[1] / "assets"
target.mkdir(parents=True, exist_ok=True)

mapping = {
    "WhatsApp Image 2026-09-22 at 07.49.30 (2).jpeg": "project-feature.webp",
    "WhatsApp Image 2026-09-22 at 07.49.30 (3).jpeg": "construction-pour.webp",
    "WhatsApp Image 2026-09-22 at 07.49.31 (1).jpeg": "residences-courtyard.webp",
    "WhatsApp Image 2026-09-22 at 07.49.31 (2).jpeg": "residences-street.webp",
    "WhatsApp Image 2026-09-22 at 07.49.31 (3).jpeg": "construction-slab.webp",
    "WhatsApp Image 2026-09-22 at 07.49.31.jpeg": "interior-shower.webp",
    "WhatsApp Image 2026-09-22 at 07.49.32 (1).jpeg": "residences-gate.webp",
    "WhatsApp Image 2026-09-22 at 07.49.32.jpeg": "residences-courtyard-angle.webp",
}

for filename, output in mapping.items():
    image = Image.open(source / filename).convert("RGB")
    image.thumbnail((1800, 1800), Image.Resampling.LANCZOS)
    image.save(target / output, "WEBP", quality=86, method=6)

# Extract the supplied mark from the Facebook screenshot, then key out the white UI.
screenshot = Image.open(source / "WhatsApp Image 2026-09-22 at 07.49.30.jpeg").convert("RGBA")
logo = screenshot.crop((44, 202, 166, 313))
pixels = logo.load()
for y in range(logo.height):
    for x in range(logo.width):
        r, g, b, a = pixels[x, y]
        brightness = min(r, g, b)
        alpha = max(0, min(255, (245 - brightness) * 10))
        if max(r, g, b) - min(r, g, b) < 18 and brightness > 205:
            alpha = 0
        pixels[x, y] = (r, g, b, alpha)

# Remove the WhatsApp/Facebook presence dot overlaid on the lower-right of the mark.
for y in range(72, logo.height):
    for x in range(78, logo.width):
        r, g, b, a = pixels[x, y]
        if g > r * 1.15 and g > b * 1.15:
            pixels[x, y] = (r, g, b, 0)

# Keep only the dominant connected artwork, discarding screenshot chrome fragments.
opaque = {(x, y) for y in range(logo.height) for x in range(logo.width) if pixels[x, y][3] > 30}
components = []
while opaque:
    seed = opaque.pop()
    component = {seed}
    stack = [seed]
    while stack:
        x, y = stack.pop()
        for point in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
            if point in opaque:
                opaque.remove(point)
                component.add(point)
                stack.append(point)
    components.append(component)
keep = max(components, key=len)
for y in range(logo.height):
    for x in range(logo.width):
        if (x, y) not in keep:
            r, g, b, _ = pixels[x, y]
            pixels[x, y] = (r, g, b, 0)

logo = logo.crop(logo.getbbox())

bbox = logo.getbbox()
logo = logo.crop(bbox)
canvas = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
scale = min(430 / logo.width, 430 / logo.height)
logo = logo.resize((round(logo.width * scale), round(logo.height * scale)), Image.Resampling.LANCZOS)
canvas.alpha_composite(logo, ((512 - logo.width) // 2, (512 - logo.height) // 2))
canvas.save(target / "logo.png", optimize=True)
canvas.resize((64, 64), Image.Resampling.LANCZOS).save(target / "favicon.png", optimize=True)

print(f"Prepared {len(mapping)} project images plus logo and favicon in {target}")
