from docling.document_converter import DocumentConverter
from pathlib import Path

source = Path("/Users/denisnorthe/Desktop/Cursor /docling/tests/data/pdf/Fluginfos.pdf")
#source = "https://arxiv.org/pdf/2408.09869"  # document per local path or URL
converter = DocumentConverter()
result = converter.convert(source)

# Save the markdown to a file
markdown_content = result.document.export_to_markdown()
#output_file = "output_test/extracted_document.md"

#with open(output_file, "w", encoding="utf-8") as f:
#    f.write(markdown_content)

#print(f"Markdown extraction saved to: {output_file}")

print(markdown_content)