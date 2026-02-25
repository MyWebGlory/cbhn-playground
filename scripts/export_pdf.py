
import asyncio
import os
from playwright.async_api import async_playwright
from PyPDF2 import PdfReader, PdfWriter
from PyPDF2.generic import (NameObject, DictionaryObject, NumberObject, FloatObject, TextStringObject, ArrayObject)

async def export_pdf():

    pdf_path = 'CBHN_Sponsorship_Package.pdf'
    # Delete old PDF if it exists
    if os.path.exists(pdf_path):
        os.remove(pdf_path)
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto('http://localhost:8000', wait_until='networkidle')
        await page.wait_for_timeout(3000)
        await page.pdf(
            path=pdf_path,
            format='A4',
            print_background=True,
            margin={'top': '0', 'right': '0', 'bottom': '0', 'left': '0'},
            prefer_css_page_size=True
        )
        await browser.close()
        print('✅ PDF exported: CBHN_Sponsorship_Package.pdf')

    # Add fillable fields to the last page using PyPDF2
    # add_fillable_fields(pdf_path)


def add_fillable_fields(pdf_path):
    # Coordinates are in points (1/72 inch). A4: 595 x 842 pts. Adjust as needed for your layout.
    # These are rough estimates and may need fine-tuning for your design.
    # Fields: Sponsorship Level (radio), Organization, Contact, Title, Email, Phone, Notes
    # All fields stacked vertically, with visible titles
    y_start = 700
    y_gap = 50
    field_defs = [
        ("tier", "radio_group", -1, 70, y_start, 12, 12, {"options": [
            ("Presenting Sponsor ($25,000)", "Presenting"),
            ("Gold Sponsor ($10,000)", "Gold"),
            ("Silver Sponsor ($5,000)", "Silver"),
            ("Bronze Sponsor ($2,500)", "Bronze")
        ]}),
        ("organization", "text", -1, 70, y_start - y_gap * 1, 350, 18, {"label": "Organization Name"}),
        ("contact", "text", -1, 70, y_start - y_gap * 2, 350, 18, {"label": "Contact Name"}),
        ("title", "text", -1, 70, y_start - y_gap * 3, 350, 18, {"label": "Title/Role"}),
        ("email", "text", -1, 70, y_start - y_gap * 4, 350, 18, {"label": "Email"}),
        ("phone", "text", -1, 70, y_start - y_gap * 5, 350, 18, {"label": "Phone"}),
        ("notes", "text", -1, 70, y_start - y_gap * 6, 350, 40, {"label": "Additional Notes"}),
    ]

    reader = PdfReader(pdf_path)
    writer = PdfWriter()
    for i, page in enumerate(reader.pages):
        writer.add_page(page)

    # Prepare AcroForm
    if "/AcroForm" not in writer._root_object:
        writer._root_object.update({NameObject("/AcroForm"): DictionaryObject()})
    writer._root_object[NameObject("/AcroForm")].update({NameObject("/Fields"): ArrayObject()})
    from PyPDF2.generic import BooleanObject
    acroform = writer._root_object[NameObject("/AcroForm")]
    acroform.update({NameObject("/NeedAppearances"): BooleanObject(True)})

    # Group radio buttons
    from PyPDF2.generic import DecodedStreamObject
    radio_widgets = []
    for field in field_defs:
        name, ftype, page_idx, x, y, w, h, opts = field
        page_num = page_idx if page_idx >= 0 else len(reader.pages) - 1
        page = writer.pages[page_num]
        # Draw field label (as text annotation)
        if ftype == "radio_group":
            # Draw group label
            label = "Sponsorship Level (select one):"
            _add_text_appearance(writer, page, label, x, y + 18, 12, pdf_path)
            radio_kids = []
            for idx, (option_label, option_value) in enumerate(opts["options"]):
                ry = y - idx * 22
                # Draw option label
                _add_text_appearance(writer, page, option_label, x + 20, ry + 2, 11, pdf_path)
                radio_dict = DictionaryObject()
                radio_dict.update({
                    NameObject("/FT"): NameObject("/Btn"),
                    NameObject("/T"): TextStringObject(name),
                    NameObject("/Ff"): NumberObject(32768),  # Radio button
                    NameObject("/V"): TextStringObject(option_value),
                    NameObject("/Rect"): ArrayObject([FloatObject(x), FloatObject(ry), FloatObject(x + w), FloatObject(ry + h)]),
                    NameObject("/Subtype"): NameObject("/Widget"),
                    NameObject("/P"): page,
                    NameObject("/AS"): NameObject("/Off"),
                    NameObject("/Opt"): ArrayObject([TextStringObject(option_value)]),
                })
                radio_ref = writer._add_object(radio_dict)
                radio_kids.append(radio_ref)
                if "/Annots" not in page:
                    page[NameObject("/Annots")] = ArrayObject()
                page[NameObject("/Annots")].append(radio_ref)
            # Add radio group parent
            parent_radio = DictionaryObject()
            parent_radio.update({
                NameObject("/FT"): NameObject("/Btn"),
                NameObject("/T"): TextStringObject(name),
                NameObject("/Ff"): NumberObject(32768),
                NameObject("/Kids"): ArrayObject(radio_kids),
            })
            parent_radio_ref = writer._add_object(parent_radio)
            writer._root_object[NameObject("/AcroForm")][NameObject("/Fields")].append(parent_radio_ref)
        elif ftype == "text":
            label = opts.get("label", name)
            _add_text_appearance(writer, page, label, x, y + 18, 12, pdf_path)
            field_dict = DictionaryObject()
            field_dict.update({
                NameObject("/FT"): NameObject("/Tx"),
                NameObject("/T"): TextStringObject(name),
                NameObject("/Ff"): NumberObject(0),
                NameObject("/V"): TextStringObject(""),
                NameObject("/Rect"): ArrayObject([FloatObject(x), FloatObject(y), FloatObject(x + w), FloatObject(y + h)]),
                NameObject("/Subtype"): NameObject("/Widget"),
                NameObject("/P"): page,
            })
            field_ref = writer._add_object(field_dict)
            writer._root_object[NameObject("/AcroForm")][NameObject("/Fields")].append(field_ref)
            if "/Annots" not in page:
                page[NameObject("/Annots")] = ArrayObject()
            page[NameObject("/Annots")].append(field_ref)


def _add_text_appearance(writer, page, text, x, y, font_size=12, pdf_path=None):
    # Add a simple text annotation for field labels (not selectable, just visible)
    from PyPDF2.generic import RectangleObject
    annot = DictionaryObject()
    annot.update({
        NameObject("/Type"): NameObject("/Annot"),
        NameObject("/Subtype"): NameObject("/FreeText"),
        NameObject("/Rect"): RectangleObject([x, y, x + 400, y + 20]),
        NameObject("/DA"): TextStringObject(f"/Helv {font_size} Tf 0 g"),
        NameObject("/Contents"): TextStringObject(text),
        NameObject("/F"): NumberObject(4),
    })
    annot_ref = writer._add_object(annot)
    if "/Annots" not in page:
        page[NameObject("/Annots")] = ArrayObject()
    page[NameObject("/Annots")].append(annot_ref)

    # Do NOT save the PDF here. The PDF is saved once at the end of add_fillable_fields.
    # Save new PDF (only once, after all fields and labels are added)
    if pdf_path is not None:
        with open(pdf_path, "wb") as f:
            writer.write(f)

asyncio.run(export_pdf())
