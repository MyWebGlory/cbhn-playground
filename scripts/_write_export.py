import pathlib

content = '''\
"""
Export the HR1 Event Flyer as a PDF via headless Chromium + Playwright.
Strategy: screenshot at 3x DPR -> convert to A4 PDF with Pillow.
This bypasses Chromium\'s PDF compositor which drops text in complex stacking contexts.

Run from the repo root:  .venv/bin/python scripts/export_hr1_flyer.py
Output:  CBHN_HR1_Forum_Flyer.pdf  (repo root)
"""

import asyncio, os, http.server, threading, time, pathlib, io
from playwright.async_api import async_playwright
from PIL import Image

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
            .info-cell {
                backdrop-filter: none !important;
                -webkit-backdrop-filter: none !important;
                background: rgba(255, 255, 255, 0.20) !important;
                border: 1.5px solid rgba(255, 255, 255, 0.40) !important;
                box-shadow: none !important;
            }
            .info-cell-value { color: #ffffff !important; }
            .info-cell-label { color: rgba(255,255,255,0.70) !important; }
            .info-cell-sub   { color: rgba(255,255,255,0.55) !important; }
            .hero-bg-img {
                -webkit-mask-image: none !important;
                mask-image: none !important;
                background:
                    linear-gradient(to right,
                        rgba(7,9,26,0.76) 0%, rgba(7,9,26,0.76) 35%,
                        rgba(7,9,26,0.18) 65%, rgba(7,9,26,0.00) 100%
                    ),
                    url(\'../../images/hr1-forum-main-image.png\') center 20% / cover no-repeat !important;
                opacity: 1 !important;
            }
            .hero-title .t-line-3 {
                background: none !important;
                -webkit-background-clip: unset !important;
                background-clip: unset !important;
                -webkit-text-fill-color: #36c98a !important;
                color: #36c98a !important;
            }
            .cta-btn { box-shadow: none !important; }
        """)

        await page.wait_for_timeout(500)

        png_bytes = await page.screenshot(
            clip={"x": 0, "y": 0, "width": 794, "height": 1123},
            full_page=False,
        )
        await browser.close()

    server.shutdown()

    img = Image.open(io.BytesIO(png_bytes)).convert("RGB")
    img = img.resize((A4_W, A4_H), Image.LANCZOS)

    if OUT_PDF.exists():
        OUT_PDF.unlink()

    img.save(str(OUT_PDF), "PDF", resolution=300, quality=98)
    print(f"  PDF saved -> {OUT_PDF}")


if __name__ == "__main__":
    os.chdir(PUBLIC)
    asyncio.run(export())
'''

out = pathlib.Path(__file__).parent / "export_hr1_flyer.py"
out.write_text(content)
print(f"Written {out}")
