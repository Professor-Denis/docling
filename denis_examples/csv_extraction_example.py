import logging
from pathlib import Path

from docling.datamodel.base_models import InputFormat
from docling.document_converter import DocumentConverter

_log = logging.getLogger(__name__)


def main():
    input_path = Path("tests/data/csv/csv-pipe.csv")  # z.B. die Datei, die du gerade offen hast
    output_path = Path("output_test/extracted_csv.md")

    converter = DocumentConverter(allowed_formats=[InputFormat.CSV])
    res = converter.convert(input_path)

    md = res.document.export_to_markdown()
    output_path.write_text(md, encoding="utf-8")

    print(f"Wrote: {output_path}")


if __name__ == "__main__":
    main()