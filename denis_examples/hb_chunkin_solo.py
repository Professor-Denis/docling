"""
Hybrid Chunking - Einzeldatei-Verarbeitung
==========================================
Dieses Skript zeigt, wie man ein Dokument mit Doclings HybridChunker in Chunks aufteilt.
Die Chunks werden in eine TXT-Datei im Ordner 'output_chunks' gespeichert.

Autor: Basierend auf hybrid_chunking_d_test.ipynb
"""

# =============================================================================
# SCHRITT 1: Bibliotheken importieren
# =============================================================================
# Path: Hilft uns, Dateipfade einfach zu handhaben (z.B. "../ordner/datei.pdf")
# os: Wird benötigt um Ordner zu erstellen
from pathlib import Path
import os

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

# Pfad zur Eingabedatei - ändere diesen Pfad zu deiner eigenen Datei
DOC_SOURCE = Path("/Users/denisnorthe/Desktop/Cursor/docling/tests/data/pdf/2206.01062.pdf")

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
# SCHRITT 4: Dokument konvertieren
# =============================================================================
# Der DocumentConverter liest das PDF und wandelt es in ein strukturiertes Format um
# Dieses Format enthält Informationen über Überschriften, Absätze, Tabellen etc.
print(f"\n📄 Konvertiere Dokument: {DOC_SOURCE}")
converter = DocumentConverter()
result = converter.convert(source=DOC_SOURCE)
doc = result.document
print(f"✓ Dokument erfolgreich konvertiert")


# =============================================================================
# SCHRITT 5: Tokenizer konfigurieren
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
# SCHRITT 6: HybridChunker erstellen und Dokument chunken
# =============================================================================
# Der HybridChunker verbindet hierarchisches Chunking (nach Dokumentstruktur)
# mit Token-basiertem Chunking (Größenbeschränkung)
print(f"\n✂️ Teile Dokument in Chunks auf...")
chunker = HybridChunker(
    tokenizer=tokenizer,
    # merge_peers=True: Benachbarte kleine Chunks werden zusammengefasst
    merge_peers=True,
)

# chunk() gibt einen Iterator zurück - mit list() wandeln wir ihn in eine Liste um
chunk_iter = chunker.chunk(dl_doc=doc)
chunks = list(chunk_iter)
print(f"✓ {len(chunks)} Chunks erstellt")


# =============================================================================
# SCHRITT 7: Chunks verarbeiten und in Datei speichern
# =============================================================================
# Wir erstellen einen Dateinamen basierend auf dem Originaldokument
input_filename = DOC_SOURCE.stem  # Dateiname ohne Endung (z.B. "2206.01062")
output_file = OUTPUT_DIR / f"{input_filename}_chunks.txt"

print(f"\n💾 Speichere Chunks in: {output_file}")

# Öffne die Datei zum Schreiben (encoding utf-8 für Sonderzeichen)
with open(output_file, "w", encoding="utf-8") as f:
    # Schreibe einen Header in die Datei
    f.write(f"Hybrid Chunking Ergebnis\n")
    f.write(f"========================\n")
    f.write(f"Quelldokument: {DOC_SOURCE}\n")
    f.write(f"Anzahl Chunks: {len(chunks)}\n")
    f.write(f"Max. Tokens pro Chunk: {MAX_TOKENS}\n")
    f.write(f"Embedding-Modell: {EMBED_MODEL_ID}\n")
    f.write(f"\n{'='*60}\n\n")
    
    # Gehe durch jeden Chunk
    for i, chunk in enumerate(chunks):
        # Zähle die Tokens im Original-Text
        txt_tokens = tokenizer.count_tokens(chunk.text)
        
        # contextualize() fügt Kontext hinzu (z.B. Überschriften)
        # Dieser Text ist ideal für Embeddings/RAG-Anwendungen
        enriched_text = chunker.contextualize(chunk=chunk)
        enriched_tokens = tokenizer.count_tokens(enriched_text)
        
        # Ausgabe auf der Konsole
        print(f"  Chunk {i}: {txt_tokens} Tokens (mit Kontext: {enriched_tokens} Tokens)")
        
        # In die Datei schreiben
        f.write(f"=== CHUNK {i} ===\n")
        f.write(f"Tokens (Original): {txt_tokens}\n")
        f.write(f"Tokens (mit Kontext): {enriched_tokens}\n\n")
        
        f.write(f"--- Original-Text ---\n")
        f.write(f"{chunk.text}\n\n")
        
        f.write(f"--- Kontextualisierter Text (für Embedding) ---\n")
        f.write(f"{enriched_text}\n\n")
        
        f.write(f"{'-'*60}\n\n")


# =============================================================================
# SCHRITT 8: Zusammenfassung ausgeben
# =============================================================================
print(f"\n{'='*60}")
print(f"✅ FERTIG!")
print(f"   • {len(chunks)} Chunks erstellt")
print(f"   • Gespeichert in: {output_file}")
print(f"{'='*60}")
