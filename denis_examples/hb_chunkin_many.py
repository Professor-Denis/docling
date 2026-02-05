"""
Hybrid Chunking - Mehrfachdatei-Verarbeitung
============================================
Dieses Skript verarbeitet mehrere Dokumente nacheinander mit Doclings HybridChunker.
Für jede Datei wird eine separate TXT-Datei mit den Chunks im Ordner 'output_chunks' erstellt.

Autor: Basierend auf hybrid_chunking_d_test.ipynb
"""

# =============================================================================
# SCHRITT 1: Bibliotheken importieren
# =============================================================================
# Path: Hilft uns, Dateipfade einfach zu handhaben (z.B. "../ordner/datei.pdf")
from pathlib import Path

# DocumentConverter: Das Herzstück von Docling - wandelt PDFs/Dokumente in ein strukturiertes Format um
from docling.document_converter import DocumentConverter

# HybridChunker: Teilt das konvertierte Dokument in sinnvolle Textabschnitte (Chunks) auf
from docling.chunking import HybridChunker

# HuggingFaceTokenizer: Zählt Tokens (Wörter/Wortteile) passend zum Embedding-Modell
from docling_core.transforms.chunker.tokenizer.huggingface import HuggingFaceTokenizer

# AutoTokenizer: Lädt automatisch den richtigen Tokenizer für ein HuggingFace-Modell
from transformers import AutoTokenizer


# =============================================================================
# SCHRITT 2: Konfiguration - Hier kannst du deine Einstellungen anpassen
# =============================================================================

# Liste der zu verarbeitenden Dateien - füge hier deine eigenen Dateipfade hinzu
DOC_SOURCES = [
    Path("/Users/denisnorthe/Desktop/Cursor /docling/tests/data/pdf/2206.01062.pdf"),
    # Weitere Dateien hinzufügen:
    # Path("../documents/mein_dokument.pdf"),
    # Path("../documents/anderes_dokument.docx"),
    # Path("/absoluter/pfad/zu/datei.pdf"),
]

# Name des Embedding-Modells (bestimmt wie Tokens gezählt werden)
# Dieses Modell wird oft für Textähnlichkeitssuche verwendet
EMBED_MODEL_ID = "sentence-transformers/all-MiniLM-L6-v2"

# Maximale Anzahl an Tokens pro Chunk
# Kleinere Werte = mehr, kürzere Chunks | Größere Werte = weniger, längere Chunks
MAX_TOKENS = 64  # Hier klein gewählt zur Demonstration

# Ausgabeordner für die Chunk-Dateien
OUTPUT_DIR = Path("/Users/denisnorthe/Desktop/Cursor /docling/denis_examples/output_chunks")


# =============================================================================
# SCHRITT 3: Ausgabeordner erstellen (falls nicht vorhanden)
# =============================================================================
# exist_ok=True bedeutet: Keinen Fehler werfen, wenn der Ordner schon existiert
OUTPUT_DIR.mkdir(exist_ok=True)
print(f"✓ Ausgabeordner '{OUTPUT_DIR}' ist bereit")


# =============================================================================
# SCHRITT 4: Tokenizer konfigurieren (einmalig für alle Dokumente)
# =============================================================================
# Der Tokenizer teilt Text in Tokens (Wörter/Wortteile) auf
# WICHTIG: Der gleiche Tokenizer sollte später auch für das Embedding verwendet werden!
print(f"\n🔧 Konfiguriere Tokenizer: {EMBED_MODEL_ID}")
tokenizer = HuggingFaceTokenizer(
    # Lädt den Tokenizer automatisch von HuggingFace
    tokenizer=AutoTokenizer.from_pretrained(EMBED_MODEL_ID),
    # Maximale Token-Anzahl pro Chunk (optional - wird sonst vom Modell abgeleitet)
    max_tokens=MAX_TOKENS,
)
print(f"✓ Tokenizer konfiguriert mit max. {MAX_TOKENS} Tokens pro Chunk")


# =============================================================================
# SCHRITT 5: HybridChunker erstellen (einmalig für alle Dokumente)
# =============================================================================
# Der HybridChunker verbindet hierarchisches Chunking (nach Dokumentstruktur)
# mit Token-basiertem Chunking (Größenbeschränkung)
chunker = HybridChunker(
    tokenizer=tokenizer,
    # merge_peers=True: Benachbarte kleine Chunks werden zusammengefasst
    merge_peers=True,
)
print(f"✓ HybridChunker ist bereit")


# =============================================================================
# SCHRITT 6: DocumentConverter erstellen (einmalig für alle Dokumente)
# =============================================================================
# Der DocumentConverter liest Dokumente und wandelt sie in ein strukturiertes Format um
converter = DocumentConverter()
print(f"✓ DocumentConverter ist bereit")


# =============================================================================
# SCHRITT 7: Funktion zum Verarbeiten einer einzelnen Datei
# =============================================================================
def process_single_document(doc_path: Path) -> dict:
    """
    Verarbeitet ein einzelnes Dokument und speichert die Chunks in einer TXT-Datei.
    
    Parameter:
        doc_path: Pfad zur Eingabedatei
        
    Rückgabe:
        Ein Dictionary mit Statistiken zur Verarbeitung
    """
    # Prüfen ob die Datei existiert
    if not doc_path.exists():
        print(f"  ⚠️ Datei nicht gefunden: {doc_path}")
        return {"status": "error", "message": "Datei nicht gefunden"}
    
    print(f"\n  📄 Konvertiere: {doc_path.name}")
    
    # Dokument konvertieren
    try:
        result = converter.convert(source=doc_path)
        doc = result.document
    except Exception as e:
        print(f"  ❌ Fehler bei Konvertierung: {e}")
        return {"status": "error", "message": str(e)}
    
    # Dokument in Chunks aufteilen
    print(f"  ✂️ Erstelle Chunks...")
    chunk_iter = chunker.chunk(dl_doc=doc)
    chunks = list(chunk_iter)
    print(f"  ✓ {len(chunks)} Chunks erstellt")
    
    # Ausgabedatei erstellen
    input_filename = doc_path.stem  # Dateiname ohne Endung
    output_file = OUTPUT_DIR / f"{input_filename}_chunks.txt"
    
    # Chunks in Datei schreiben
    print(f"  💾 Speichere in: {output_file}")
    with open(output_file, "w", encoding="utf-8") as f:
        # Header schreiben
        f.write(f"Hybrid Chunking Ergebnis\n")
        f.write(f"========================\n")
        f.write(f"Quelldokument: {doc_path}\n")
        f.write(f"Anzahl Chunks: {len(chunks)}\n")
        f.write(f"Max. Tokens pro Chunk: {MAX_TOKENS}\n")
        f.write(f"Embedding-Modell: {EMBED_MODEL_ID}\n")
        f.write(f"\n{'='*60}\n\n")
        
        # Jeden Chunk schreiben
        for i, chunk in enumerate(chunks):
            # Tokens zählen
            txt_tokens = tokenizer.count_tokens(chunk.text)
            
            # contextualize() fügt Kontext hinzu (z.B. Überschriften)
            enriched_text = chunker.contextualize(chunk=chunk)
            enriched_tokens = tokenizer.count_tokens(enriched_text)
            
            # In die Datei schreiben
            f.write(f"=== CHUNK {i} ===\n")
            f.write(f"Tokens (Original): {txt_tokens}\n")
            f.write(f"Tokens (mit Kontext): {enriched_tokens}\n\n")
            
            f.write(f"--- Original-Text ---\n")
            f.write(f"{chunk.text}\n\n")
            
            f.write(f"--- Kontextualisierter Text (für Embedding) ---\n")
            f.write(f"{enriched_text}\n\n")
            
            f.write(f"{'-'*60}\n\n")
    
    print(f"  ✓ Fertig!")
    
    return {
        "status": "success",
        "chunks": len(chunks),
        "output_file": str(output_file)
    }


# =============================================================================
# SCHRITT 8: Alle Dokumente verarbeiten
# =============================================================================
print(f"\n{'='*60}")
print(f"🚀 STARTE VERARBEITUNG VON {len(DOC_SOURCES)} DOKUMENT(EN)")
print(f"{'='*60}")

# Statistiken sammeln
results = []

# Jedes Dokument nacheinander verarbeiten
for i, doc_path in enumerate(DOC_SOURCES, start=1):
    print(f"\n[{i}/{len(DOC_SOURCES)}] Verarbeite Dokument...")
    result = process_single_document(doc_path)
    result["source"] = str(doc_path)
    results.append(result)


# =============================================================================
# SCHRITT 9: Zusammenfassung ausgeben
# =============================================================================
print(f"\n{'='*60}")
print(f"📊 ZUSAMMENFASSUNG")
print(f"{'='*60}")

# Erfolgreiche Verarbeitungen zählen
successful = [r for r in results if r["status"] == "success"]
failed = [r for r in results if r["status"] == "error"]

print(f"\n✅ Erfolgreich verarbeitet: {len(successful)} von {len(DOC_SOURCES)}")

if successful:
    total_chunks = sum(r["chunks"] for r in successful)
    print(f"   • Gesamt Chunks erstellt: {total_chunks}")
    print(f"   • Ausgabedateien in: {OUTPUT_DIR}/")
    
    print(f"\n   Erstellte Dateien:")
    for r in successful:
        print(f"   - {r['output_file']} ({r['chunks']} Chunks)")

if failed:
    print(f"\n❌ Fehlgeschlagen: {len(failed)}")
    for r in failed:
        print(f"   - {r['source']}: {r['message']}")

print(f"\n{'='*60}")
print(f"✅ VERARBEITUNG ABGESCHLOSSEN")
print(f"{'='*60}")
