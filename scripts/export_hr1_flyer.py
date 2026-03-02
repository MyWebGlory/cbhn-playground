"""
Export the HR1 Event Flyer as a PDF via headless Chromium + Playwright.
Run from the repo root:  .venv/bin/python scripts/export_hr1_flyer.py
Output:  CBHN_HR1_Forum_Flyer.pdf  (repo root)
"""

import asyncio, os, http.server, threading, time, pathlib
from playwright.async_api import async_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
PUBLIC = ROOT / "public"
OUT_PDF = ROOT / "CBHN_HR1_Forum_Flyer.pdf"
PORT = 8765


def start_server():
    """Serve the public/ directory on a local HTTP server."""
    handler = http.server.SimpleHTTPRequestHandler
    handler.log_message = lambda *a: None   # silence logs
    server = http.server.HTTPServer(("127.0.0.1", PORT), handler)
    t = threading.Thread(target=server.serve_forever, daemon=True)
    t.start()
    return server


async def export():
    server = start_server()
    time.sleep(0.4)   # let the server start

    url = f"http://127.0.0.1:{PORT}/projects/hr1-event-flyer/index.html"

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 794, "height": 1123})

        print(f"  Loading {url} ...")
        await page.goto(url, wait_until="networkidle")
        await page.wait_for_timeout(2500)   # let fonts/images render

        # Inject PDF-rendering fixes directly — more reliable than @media print
        # which Playwright's headless engine often ignores.
        await page.add_style_tag(content="""
            /* Remove body padding so flyer sits flush */
            body { padding: 0 !important; margin: 0 !important; }

            /* backdrop-filter:blur is not rendered in headless PDF */
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

            /* mask-image not rendered in headless: replicate the left-dark fade
               by layering a matching gradient on top of the image */
            .hero-bg-img {
                -webkit-mask-image: none !important;
                mask-image: none !important;
                background:
                    linear-gradient(
                        to right,
                        rgba(7,9,26,0.76) 0%,
                        rgba(7,9,26,0.76) 35%,
                        rgba(7,9,26,0.18) 65%,
                        rgba(7,9,26,0.00) 100%
                    ),
                    url('../../images/hr1-forum-main-image.png') center 20% / cover no-repeat !important;
                opacity: 1 !important;
            }

            /* -webkit-text-fill-color:transparent makes gradient-clip text
               completely invisible in PDF — fall back to a solid colour */
            .hero-title .t-line-3 {
                background: none !important;
                -webkit-background-clip: unset !important;
                background-clip: unset !important;
                -webkit-text-fill-color: #36c98a !important;
                color: #36c98a !important;
            }

            /* Reduce title font size so italic tail isn't clipped */
            .hero-title { font-size: 47px !important; }

            /* Large box-shadow blur renders as a solid rectangle in PDF */
            .cta-btn { box-shadow: none !important; }
        """)

        if OUT_PDF.exists():
            OUT_PDF.unlink()

        await page.pdf(
            path=str(OUT_PDF),
            format="A4",
            print_background=True,
            margin={"top": "0", "right": "0", "bottom": "0", "left": "0"},
            prefer_css_page_size=True,
        )

        await browser.close()

    server.shutdown()
    print(f"✅  PDF saved → {OUT_PDF}")


if __name__ == "__main__":
    os.chdir(PUBLIC)   # resolve relative paths in HTML correctly
    asyncio.run(export())
