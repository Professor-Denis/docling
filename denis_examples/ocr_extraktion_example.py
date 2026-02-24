"""
OCR-Extraktion mit Docling

Extrahiert PDF-Inhalt als Markdown mittels OCR (Optical Character Recognition).
Nützlich wenn die PDF-Textschicht fehlerhaft ist (z.B. überlagerte Template-Werte).

- force_full_page_ocr=True: Ersetzt den PDF-Text durch OCR-Erkennung


Voraussetzung: Tesseract mit deutschem Sprachpaket (z.B. brew install tesseract tesseract-lang)
"""

from pathlib import Path

from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import (
    PdfPipelineOptions,
    TesseractCliOcrOptions,
)
from docling.document_converter import DocumentConverter, PdfFormatOption

source = Path(
    "/Users/denisnorthe/Desktop/Cursor /docling/tests/data/pdf/Antwortschreiben.pdf"
)

pipeline_options = PdfPipelineOptions(
    do_ocr=True,
    do_table_structure=True,
    ocr_options=TesseractCliOcrOptions(
        force_full_page_ocr=True,
        lang=["eng"],  # Nur eng ist in der Basis-Installation enthalten
        # Für Deutsch: brew install tesseract-lang, dann lang=["deu"]
    ),
)

converter = DocumentConverter(
    format_options={
        InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options),
    }
)

result = converter.convert(source)
markdown_content = result.document.export_to_markdown()

print(markdown_content)
