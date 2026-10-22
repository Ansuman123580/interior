import os
import re
import struct
import zlib

def make_png(filename, size=64):
    width, height = size, size
    raw = bytearray()
    for y in range(height):
        raw.append(0)
        for x in range(width):
            border = (x in (2, width-3) and 2 <= y <= height-3) or (y in (2, height-3) and 2 <= x <= width-3)
            # M shape
            is_m = False
            scale = size / 64.0
            x_norm = x / scale
            y_norm = y / scale
            if 14 <= y_norm <= 50:
                if 14 <= x_norm <= 21 or 43 <= x_norm <= 50:
                    is_m = True
                elif 21 <= x_norm <= 32 and abs((y_norm - 14) - (x_norm - 21) * 1.8) < 3.8:
                    is_m = True
                elif 32 <= x_norm <= 43 and abs((y_norm - 14) - (43 - x_norm) * 1.8) < 3.8:
                    is_m = True
            if is_m:
                raw.extend([230, 175, 46, 255])
            elif border:
                raw.extend([60, 60, 70, 255])
            else:
                raw.extend([14, 15, 19, 255])
    
    compressor = zlib.compressobj()
    idat = compressor.compress(bytes(raw)) + compressor.flush()
    def chunk(tag, data):
        return struct.pack(">I", len(data)) + tag + data + struct.pack(">I", zlib.crc32(tag + data) & 0xffffffff)
    
    png = b"\x89PNG\r\n\x1a\n"
    png += chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 6, 0, 0, 0))
    png += chunk(b"IDAT", idat)
    png += chunk(b"IEND", b"")
    with open(filename, "wb") as f:
        f.write(png)

# 1. Update Stanzza icons
make_png("stanzza.design/assets/images/69ee66fc20b6501ed7d5875a_Favicon_224b5b100a.png", 64)
make_png("stanzza.design/assets/images/69ee66f7321d78262d0cd10b_Webclip_1826940137.png", 180)

# 2. Update dsgninterior favicon SVG
modus_svg = """<svg width="48" height="48" viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg">
  <style>.c1{fill:#111111}.c2{fill:#F6F5F4}@media(prefers-color-scheme:dark){.c1{fill:#F6F5F4}.c2{fill:#111111}}</style>
  <rect class="c2" width="48" height="48" rx="10"/>
  <path class="c1" d="M10 36V14h4.5l9.5 13 9.5-13H38v22h-4.5V20.5L24 33.2 14.5 20.5V36H10z"/>
</svg>"""
with open("dsgninterior.se/assets/images/favicon_cd0abbdf4b.svg", "w") as f:
    f.write(modus_svg)

print("Icons created successfully.")

# SVG definitions for Atelier Modena
NEW_FULL_LOGO = """<svg xmlns="http://www.w3.org/2000/svg" width="100%" viewBox="0 0 643 120" fill="none" class="u-logo"><text x="50%" y="76" text-anchor="middle" fill="currentColor" font-family="'Space Grotesk', -apple-system, sans-serif" font-weight="700" font-size="46" letter-spacing="12">ATELIER MODENA</text></svg>"""
NEW_SYMBOL_LOGO = """<svg xmlns="http://www.w3.org/2000/svg" width="100%" viewBox="0 0 120 120" fill="none" class="u-logo"><path d="M22 100V20L60 62L98 20V100H84V44L60 70L36 44V100H22Z" fill="currentColor"/></svg>"""

NEW_PRELOADER_EMBED = """<div style="width:100%;height:100%;display:flex;align-items:center;justify-content:flex-end;"><span style="font-family:'Space Grotesk',sans-serif;font-weight:700;font-size:clamp(14px,1.8svw,22px);letter-spacing:0.25em;text-transform:uppercase;color:#ffffff;opacity:0.9;">ATELIER MODENA</span></div>"""

# Rebrand Stanzza HTML files
stanzza_count = 0
for root, _, files in os.walk("stanzza.design"):
    for file in files:
        if file.endswith(".html"):
            path = os.path.join(root, file)
            with open(path, "r", encoding="utf-8", errors="ignore") as fp:
                html = fp.read()
            
            orig = html
            
            # Replace SVGs with 643 120 viewBox
            html = re.sub(r'<svg[^>]*viewBox="0 0 643 120"[^>]*>.*?</svg>', NEW_FULL_LOGO, html, flags=re.DOTALL)
            # Replace SVGs with 120 120 viewBox (symbol monogram)
            html = re.sub(r'<svg[^>]*viewBox="0 0 120 120"[^>]*>.*?</svg>', NEW_SYMBOL_LOGO, html, flags=re.DOTALL)
            
            # Replace preloader video aside embed
            html = re.sub(
                r'<div class="preloader_logo-aside_video w-embed">\s*<video[^>]*>.*?</video>\s*</div>',
                f'<div class="preloader_logo-aside_video w-embed">{NEW_PRELOADER_EMBED}</div>',
                html,
                flags=re.DOTALL
            )
            
            # Brand string replacements
            html = html.replace("Stanzza Design Europe SL", "Atelier Modena Architecture SL")
            html = html.replace("Stanzza Design", "Atelier Modena")
            html = html.replace("STANZZA DESIGN", "ATELIER MODENA")
            html = html.replace("Stanzza", "Atelier Modena")
            html = html.replace("STANZZA", "ATELIER MODENA")
            html = html.replace("stanzza.design", "ateliermodena.com")
            html = html.replace("info@stanzza.design", "contact@ateliermodena.com")
            html = html.replace("stanzza_design", "ateliermodena")
            html = html.replace("https://www.facebook.com/Stanzza-Design-111487748009895", "#")
            html = html.replace("+34 654 496 780", "+34 932 201 840")
            html = html.replace("+34654496780", "+34932201840")
            html = html.replace("<!-- This site was created in Webflow. https://webflow.com -->", "<!-- Atelier Modena Architecture & Interiors -->")
            html = re.sub(r'<meta[^>]*content="Webflow"[^>]*name="generator"[^>]*>', '<meta content="Atelier Modena" name="author"/>', html)
            html = re.sub(r'<meta[^>]*name="facebook-domain-verification"[^>]*>', '', html)
            
            if html != orig:
                with open(path, "w", encoding="utf-8") as fp:
                    fp.write(html)
                stanzza_count += 1

print(f"Rebranded {stanzza_count} files in stanzza.design.")

# Rebrand dsgninterior HTML files
dsgn_count = 0
for root, _, files in os.walk("dsgninterior.se"):
    for file in files:
        if file.endswith(".html"):
            path = os.path.join(root, file)
            with open(path, "r", encoding="utf-8", errors="ignore") as fp:
                html = fp.read()
            
            orig = html
            
            # Logo replacements
            html = re.sub(r'<strong>\s*dsgn\s*</strong>\s*interior', '<strong>modus</strong> interior', html, flags=re.IGNORECASE)
            html = re.sub(r'<span>\s*dsgn\s+Archive\s*</span>', '<span>Modus Archive</span>', html, flags=re.IGNORECASE)
            html = re.sub(r'<span>\s*dsgn\s+Arkiv\s*</span>', '<span>Modus Arkiv</span>', html, flags=re.IGNORECASE)
            
            # Contact & copyright replacements
            html = html.replace("info@dsgninterior.se", "contact@modusinterior.se")
            html = html.replace("dsgninterior.se", "modusinterior.se")
            html = html.replace("+46 040 26 26 40", "+46 (0) 8 500 240 00")
            html = html.replace("+46040262640", "+46850024000")
            html = html.replace("dsgn+interior", "modus+interior")
            
            # Title & meta replacements
            html = re.sub(r'<title>\s*(.*?)\s*\|\s*dsgn\s+interior\s*</title>', r'<title>\1 | Modus Interior</title>', html, flags=re.IGNORECASE)
            html = re.sub(r'<title>\s*dsgn\s+interior\s*(.*?)\s*</title>', r'<title>Modus Interior \1</title>', html, flags=re.IGNORECASE)
            html = re.sub(r'content="dsgn interior"', 'content="Modus Interior"', html)
            html = re.sub(r'content="dsgn interior\s*-\s*([^"]*)"', r'content="Modus Interior - \1"', html)
            
            # General text
            html = html.replace("dsgn interior", "Modus Interior")
            html = html.replace("dsgn Interior", "Modus Interior")
            html = html.replace("DSGN INTERIOR", "MODUS INTERIOR")
            
            if html != orig:
                with open(path, "w", encoding="utf-8") as fp:
                    fp.write(html)
                dsgn_count += 1

print(f"Rebranded {dsgn_count} files in dsgninterior.se.")
