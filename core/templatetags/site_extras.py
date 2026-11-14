from django import template
from django.utils.html import escape, format_html, format_html_join, linebreaks
from django.utils.safestring import mark_safe

from core.images import WIDTHS, variant_name

register = template.Library()


@register.filter
def paragraphs(text):
    """Plain text -> <p> paragraphs (HTML-escaped)."""
    return mark_safe(linebreaks(escape(text or "")))


@register.filter
def bullets(text):
    """One bullet per line -> <ul>."""
    lines = [l.strip().lstrip("•-– ").strip() for l in (text or "").splitlines() if l.strip()]
    if not lines:
        return ""
    return format_html("<ul>{}</ul>", format_html_join("", "<li>{}</li>", ((l,) for l in lines)))


@register.filter
def csv(text):
    return [t.strip() for t in (text or "").split(",") if t.strip()]


@register.filter
def lines(text):
    return [t.strip() for t in (text or "").splitlines() if t.strip()]


@register.filter
def metrics(text):
    """'ROC-AUC: 0.79' lines -> [(label, value)]"""
    out = []
    for line in (text or "").splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            out.append((k.strip(), v.strip()))
    return out


@register.simple_tag
def picture(image, alt="", sizes="(max-width: 700px) 100vw, 700px", css="", eager=False):
    """Responsive <img> using the WebP variants made at upload time."""
    if not image:
        return ""
    storage = image.storage
    found = [(w, variant_name(image.name, w)) for w in WIDTHS if storage.exists(variant_name(image.name, w))]
    loading = "eager" if eager else "lazy"
    if not found:
        return format_html('<img src="{}" alt="{}" class="{}" loading="{}" decoding="async">',
                           image.url, alt, css, loading)
    srcset = ", ".join(f"{storage.url(n)} {w}w" for w, n in found)
    return format_html(
        '<img src="{}" srcset="{}" sizes="{}" alt="{}" class="{}" loading="{}" decoding="async">',
        storage.url(found[-1][1]), srcset, sizes, alt, css, loading,
    )
