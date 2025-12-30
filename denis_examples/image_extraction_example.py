from docling.document_converter import DocumentConverter

# Image URL - Swiss QR-Bill example
source = "https://upload.wikimedia.org/wikipedia/commons/9/9f/Swiss_QR-Bill_example.jpg"

# Initialize the document converter
converter = DocumentConverter()

# Convert the image
print(f"Extracting content from image: {source}")
result = converter.convert(source)

# Export to markdown
markdown_content = result.document.export_to_markdown()

# Save to file
output_file = "output_test/extracted_image.md"

with open(output_file, "w", encoding="utf-8") as f:
    f.write(markdown_content)

print(f"Image content extracted and saved to: {output_file}")
#print(f"\nExtracted content preview:")
#print("=" * 50)
#print(markdown_content[:500] + "..." if len(markdown_content) > 500 else markdown_content)

