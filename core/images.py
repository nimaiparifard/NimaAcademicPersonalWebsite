"""Image optimisation.

Every uploaded image is converted once, at upload time, into resized WebP
variants (480/960/1600 px wide). Templates then emit <img srcset=...> so each
visitor downloads the smallest file that looks sharp on their screen.
"""
import io
import os

from django.core.files.base import ContentFile
from PIL import Image, ImageOps

WIDTHS = (480, 960, 1600)


def variant_name(name: str, width: int) -> str:
    root, _ = os.path.splitext(name)
    return f"{root}_w{width}.webp"


def build_variants(field_file) -> None:
    """Create WebP variants for an ImageFieldFile (idempotent)."""
    if not field_file or not field_file.name:
        return
    storage = field_file.storage
    try:
        with storage.open(field_file.name) as fh:
            img = ImageOps.exif_transpose(Image.open(fh))
            img.load()
    except Exception:  # unreadable / not an image: leave it alone
        return
    if img.mode not in ("RGB", "RGBA"):
        img = img.convert("RGBA" if "transparency" in img.info else "RGB")
    prev = 0
    for w in WIDTHS:
        name = variant_name(field_file.name, w)
        # never upscale: the first slot at/above the original gets the native size, later slots are skipped
        if prev >= img.width or storage.exists(name):
            prev = w
            continue
        prev = w
        target_w = min(w, img.width)
        h = round(img.height * target_w / img.width)
        buf = io.BytesIO()
        img.resize((target_w, h), Image.LANCZOS).save(buf, "WEBP", quality=82, method=6)
        storage.save(name, ContentFile(buf.getvalue()))


def delete_variants(field_file) -> None:
    if not field_file or not field_file.name:
        return
    for w in WIDTHS:
        name = variant_name(field_file.name, w)
        if field_file.storage.exists(name):
            field_file.storage.delete(name)
