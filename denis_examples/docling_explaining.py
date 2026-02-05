"""
Docling Document Struktur - Erklärungs-Skript
==============================================
Dieses Skript zeigt, wie ein PDF nach der Konvertierung aussieht.
"""

from pathlib import Path
from docling.document_converter import DocumentConverter
import json

# =============================================================================
# Konfiguration - HIER KANNST DU DEN PFAD ÄNDERN
# =============================================================================
# Große PDF (DocLayNet Paper) - Konvertierung dauert ca. 2-5 Minuten!
PDF_PATH = Path("/Users/denisnorthe/Desktop/Cursor /docling/tests/data/pdf/2206.01062.pdf")

# Alternative: Kleinere PDF für schnellen Test (nur 1 Seite, ~15 Sekunden)
# PDF_PATH = Path("/Users/denisnorthe/Desktop/Cursor /docling/tests/data/pdf/2305.03393v1-pg9.pdf")

OUTPUT_FILE = Path("/Users/denisnorthe/Desktop/Cursor /docling/denis_examples/docling_explaining_output_big.txt")

# =============================================================================
# Konvertieren
# =============================================================================
print("🔄 Konvertiere PDF...")
result = DocumentConverter().convert(source=PDF_PATH)
doc = result.document
print("✅ Konvertierung abgeschlossen!\n")

# =============================================================================
# Output-Datei öffnen
# =============================================================================
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    
    # =========================================================================
    # 1. Übersicht / Metadaten
    # =========================================================================
    f.write("=" * 80 + "\n")
    f.write("DOCLING DOCUMENT - STRUKTUR ERKLÄRT\n")
    f.write("=" * 80 + "\n\n")
    
    f.write(f"Quelldatei: {PDF_PATH}\n")
    f.write(f"Dokumentname: {doc.name}\n\n")
    
    f.write("-" * 40 + "\n")
    f.write("STATISTIK\n")
    f.write("-" * 40 + "\n")
    f.write(f"Anzahl Textelemente: {len(doc.texts)}\n")
    f.write(f"Anzahl Tabellen: {len(doc.tables)}\n")
    f.write(f"Anzahl Bilder: {len(doc.pictures)}\n")
    f.write(f"Anzahl Gruppen: {len(doc.groups)}\n\n")
    
    # =========================================================================
    # 2. Element-Baum (Hierarchie)
    # =========================================================================
    f.write("=" * 80 + "\n")
    f.write("ELEMENT-BAUM (Dokumentstruktur / Hierarchie)\n")
    f.write("=" * 80 + "\n")
    f.write("Zeigt wie die Elemente verschachtelt sind:\n\n")
    
    for item, level in doc.iterate_items():
        indent = "  " * level
        label = item.label if hasattr(item, 'label') else 'unknown'
        text_preview = ""
        if hasattr(item, 'text') and item.text:
            text_preview = f' → "{item.text[:60]}..."' if len(item.text) > 60 else f' → "{item.text}"'
        f.write(f"{indent}[{label}]{text_preview}\n")
    
    f.write("\n")
    
    # =========================================================================
    # 3. Alle Textelemente im Detail
    # =========================================================================
    f.write("=" * 80 + "\n")
    f.write("ALLE TEXTELEMENTE IM DETAIL\n")
    f.write("=" * 80 + "\n\n")
    
    for i, text_item in enumerate(doc.texts[:50]):  # Erste 50 zur Übersicht (bei großen PDFs)
        f.write(f"--- texts[{i}] ---\n")
        f.write(f"  self_ref: {text_item.self_ref}\n")
        f.write(f"  label: {text_item.label}\n")
        f.write(f"  text: {text_item.text[:200] if text_item.text else '(leer)'}{'...' if text_item.text and len(text_item.text) > 200 else ''}\n")
        if hasattr(text_item, 'prov') and text_item.prov:
            for prov in text_item.prov:
                f.write(f"  prov: Seite {prov.page_no}, BBox: {prov.bbox}\n")
        f.write("\n")
    
    if len(doc.texts) > 50:
        f.write(f"... und {len(doc.texts) - 50} weitere Textelemente\n\n")
    
    # =========================================================================
    # 4. Tabellen (falls vorhanden)
    # =========================================================================
    if doc.tables:
        f.write("=" * 80 + "\n")
        f.write("TABELLEN\n")
        f.write("=" * 80 + "\n\n")
        
        for i, table in enumerate(doc.tables[:5]):  # Max 5 Tabellen
            f.write(f"--- tables[{i}] ---\n")
            f.write(f"  self_ref: {table.self_ref}\n")
            if hasattr(table, 'data') and table.data:
                f.write(f"  Zeilen: {table.data.num_rows}\n")
                f.write(f"  Spalten: {table.data.num_cols}\n")
            f.write("\n")
    
    # =========================================================================
    # 5. Als Markdown (Lesereihenfolge)
    # =========================================================================
    f.write("=" * 80 + "\n")
    f.write("MARKDOWN EXPORT (so würde das Dokument als Text aussehen)\n")
    f.write("=" * 80 + "\n\n")
    
    markdown_output = doc.export_to_markdown()
    # Erste 8000 Zeichen für bessere Übersicht bei großen Dokumenten
    f.write(markdown_output[:8000])
    if len(markdown_output) > 8000:
        f.write(f"\n\n... [GEKÜRZT - Vollständiger Markdown hat {len(markdown_output)} Zeichen] ...\n")
    
    f.write("\n\n")
    
    # =========================================================================
    # 6. JSON-Struktur (Auszug)
    # =========================================================================
    f.write("=" * 80 + "\n")
    f.write("JSON-STRUKTUR (Auszug - zeigt die komplette Datenstruktur)\n")
    f.write("=" * 80 + "\n\n")
    
    doc_dict = doc.export_to_dict()
    
    # Zeige nur ausgewählte Felder für Übersichtlichkeit
    json_preview = {
        "schema_name": doc_dict.get("schema_name"),
        "version": doc_dict.get("version"),
        "name": doc_dict.get("name"),
        "origin": doc_dict.get("origin"),
        "body": {
            "self_ref": doc_dict.get("body", {}).get("self_ref"),
            "children": doc_dict.get("body", {}).get("children", [])[:5],
            "_hinweis": f"... und {len(doc_dict.get('body', {}).get('children', [])) - 5} weitere children" if len(doc_dict.get('body', {}).get('children', [])) > 5 else None
        },
        "texts_auszug": doc_dict.get("texts", [])[:3],
        "_hinweis": f"Vollständiges JSON hat {len(json.dumps(doc_dict))} Zeichen"
    }
    
    f.write(json.dumps(json_preview, indent=2, ensure_ascii=False))
    f.write("\n")

print(f"✅ Output gespeichert in: {OUTPUT_FILE}")