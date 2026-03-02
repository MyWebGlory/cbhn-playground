"""
Export the HR1 Event Flyer as a PDF via headless Chromium + Playwright.
Strategy: screenshot at 3x DPR -> convert to A4 PDF with Pillow.
This bypasses Chromium's PDF compositor which drops text in complex stacking contexts.

Run from the repo root:  .venv/bin/python scripts/export_hr1_flyer.py
Output:  CBHN_HR1_Forum_Flyer.pdf  (repo root)
"""

import asyncio, os, http.server, threading, time, pathlib, io
from playwright.async_api import async_playwright
from PIL import Image
from pypdf import PdfWriter, PdfReader
from pypdf.generic import (
    ArrayObject, DictionaryObject, FloatObject,
    NameObject, NumberObject, TextStringObject
)

ROOT    = pathlib.Path(__file__).resolve().parent.parent
PUBLIC  = ROOT / "public"
OUT_PDF = ROOT / "CBHN_HR1_Forum_Flyer.pdf"
PORT    = 8765

# A4 at 300 DPI
A4_W, A4_H = 2480, 3508


def start_server():
    handler = http.server.SimpleHTTPRequestHandler
    handler.log_message = lambda *a: None
    server = http.server.HTTPServer(("127.0.0.1", PORT), handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server


async def export():
    server = start_server()
    time.sleep(0.4)

    url = f"http://127.0.0.1:{PORT}/projects/hr1-event-flyer/index.html"

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(
            viewport={"width": 794, "height": 1123},
            device_scale_factor=3,
        )

        print(f"  Loading {url} ...")
        await page.goto(url, wait_until="networkidle")
        await page.evaluate("document.fonts.ready")
        await page.wait_for_timeout(1500)

        await page.add_style_tag(content="""
            body { padding: 0 !important; margin: 0 !important; }

            /* backdrop-filter causes a blank compositing layer in headless — strip it */
            .info-cell {
                backdrop-filter: none !important;
                -webkit-backdrop-filter: none !important;
                background: rgba(160, 170, 200, 0.52) !important;
                border: 1.5px solid rgba(200, 210, 240, 0.65) !important;
                box-shadow: none !important;
            }
            .info-cell-value { color: #ffffff !important; }
            .info-cell-label { color: rgba(255,255,255,0.70) !important; }
            .info-cell-sub   { color: rgba(255,255,255,0.55) !important; }

            /* box-shadow renders as solid rect in headless — remove it */
            .cta-btn { box-shadow: none !important; }
        """)

        await page.wait_for_timeout(500)

        # Capture button bounding box before screenshotting
        btn_bbox = await page.locator(".cta-btn").bounding_box()

        png_bytes = await page.screenshot(
            clip={"x": 0, "y": 0, "width": 794, "height": 1123},
            full_page=False,
        )

        # Save raw debug PNG so we can verify the screenshot before PDF conversion
        debug_png = ROOT / "debug_screenshot.png"
        debug_png.write_bytes(png_bytes)
        print(f"  Debug PNG saved -> {debug_png}")

        await browser.close()

    server.shutdown()

    img = Image.open(io.BytesIO(png_bytes)).convert("RGB")
    img = img.resize((A4_W, A4_H), Image.LANCZOS)

    if OUT_PDF.exists():
        OUT_PDF.unlink()

    img.save(str(OUT_PDF), "PDF", resolution=300, quality=98)

    # Add clickable URI annotation over the CTA button
    # Scale from viewport (794x1123) to A4 PDF points (595.28x841.89)
    # PDF y-axis starts at bottom, so we flip
    A4_PTS_W, A4_PTS_H = 595.28, 841.89
    sx = A4_PTS_W / 794
    sy = A4_PTS_H / 1123

    x0 = btn_bbox["x"] * sx
    y0 = A4_PTS_H - (btn_bbox["y"] + btn_bbox["height"]) * sy
    x1 = (btn_bbox["x"] + btn_bbox["width"]) * sx
    y1 = A4_PTS_H - btn_bbox["y"] * sy

    reader = PdfReader(str(OUT_PDF))
    writer = PdfWriter()
    page_obj = reader.pages[0]
    writer.add_page(page_obj)

    # Build a /URI link annotation
    annot = DictionaryObject({
        NameObject("/Type"):    NameObject("/Annot"),
        NameObject("/Subtype"): NameObject("/Link"),
        NameObject("/Rect"):    ArrayObject([
            FloatObject(x0), FloatObject(y0),
            FloatObject(x1), FloatObject(y1),
        ]),
        NameObject("/Border"):  ArrayObject([NumberObject(0), NumberObject(0), NumberObject(0)]),
        NameObject("/A"):       DictionaryObject({
            NameObject("/Type"): NameObject("/Action"),
            NameObject("/S"):    NameObject("/URI"),
            NameObject("/URI"):  TextStringObject(
                "https://us06web.zoom.us/webinar/register/WN_Zh6EMM_TRfqyPZIKiPHO6g"
            ),
        }),
    })

    if "/Annots" not in writer.pages[0]:
        writer.pages[0][NameObject("/Annots")] = ArrayObject()
    writer.pages[0]["/Annots"].append(writer._add_object(annot))

    with open(str(OUT_PDF), "wb") as f:
        writer.write(f)

    print(f"  PDF saved -> {OUT_PDF}")


if __name__ == "__main__":
    os.chdir(PUBLIC)
    asyncio.run(export())
