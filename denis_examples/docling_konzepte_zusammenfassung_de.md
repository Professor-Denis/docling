# Docling – einfache Zusammenfassung (Deutsch)

Diese Notiz fasst zwei Docling-Konzeptseiten in **einfacher Sprache** zusammen:

- `DoclingDocument` (Dokument-„Bauplan“)
- `Chunking` (Dokument in handliche Text-Abschnitte teilen)

---

## 1) `DoclingDocument`: Ein einheitlicher „Bauplan“ für Dokumente

Docling kann unterschiedliche Dateien (z. B. PDF oder Word) in eine **einheitliche interne Darstellung** umwandeln. Diese heißt **`DoclingDocument`**.

Stell dir das wie einen **standardisierten Bauplan** vor, der beschreibt:

- **Was** im Dokument drin ist (Text, Tabellen, Bilder …)
- **Wie** es zusammenhängt (Struktur / Lesereihenfolge)
- **Wo** etwas auf der Seite steht (optional: Layout/Positionen)
- **Woher** Inhalte stammen (optional: Herkunft/Provenienz)

### Inhalte („was es gibt“)
Im `DoclingDocument` werden Inhalte in Listen gesammelt, z. B.:

- **`texts`**: alle Text-Bestandteile (Absätze, Überschriften, Formeln …)
- **`tables`**: Tabellen
- **`pictures`**: Bilder
- **`key_value_items`**: „Schlüssel: Wert“-Paare (z. B. „Datum: …“)

### Struktur („wie man es liest“)
Zusätzlich speichert Docling die **Struktur** wie einen Baum (Eltern/Kind – ähnlich wie Kapitel mit Unterpunkten).

- **`body`**: der Hauptinhalt
- **`furniture`**: Kopf-/Fußzeilen und ähnliche Randbereiche (nicht „Haupttext“)
- **`groups`**: Gruppierungen/Container (z. B. Listen, Kapitel, Abschnitte)

**Wichtig:** Die **Lesereihenfolge** ergibt sich aus dieser Struktur (und der Reihenfolge der „Kinder“ in jedem Abschnitt).

---

## 2) Chunking: Ein Dokument in „Chunks“ (Abschnitte) zerlegen

**Chunking** bedeutet: Ein langes Dokument wird in **kleinere Text-Abschnitte** („Chunks“) geteilt.
Das ist praktisch, damit man Inhalte leichter:

- suchen / wiederfinden kann
- an KI-Modelle geben kann (die oft Längen-Limits haben)
- weiterverarbeiten kann

### Zwei grundsätzliche Wege
Ausgehend von einem `DoclingDocument` gibt es zwei typische Ansätze:

1. **Über Markdown**: Dokument nach Markdown exportieren und danach selbst zerlegen.
2. **Nativ in Docling**: Direkt auf dem `DoclingDocument` arbeiten (darum geht es hier).

### Was ist ein „Chunker“?
Ein **Chunker** ist eine Komponente, die:

- ein `DoclingDocument` nimmt
- daraus eine Folge von **Chunks** erzeugt
- jeder Chunk besteht aus:
  - **Text** (als String)
  - **Metadaten** (Kontext wie Überschriften, Herkunft, Bildunterschriften etc.)

### `BaseChunker`: die gemeinsame Grundlage
Docling definiert eine Standard-Schnittstelle, damit unterschiedliche Chunker gleich benutzt werden können (auch in Tools wie LlamaIndex).

Ein Chunker bietet typischerweise:

- **`chunk(...)`**: erzeugt die Chunks für ein Dokument
- **`contextualize(...)`**: gibt einen Chunk als Text aus – oft inkl. hilfreichem Kontext/Metadaten (z. B. für Embeddings/KI)

---

## 3) Zwei wichtige Chunker in Docling

### A) `HierarchicalChunker` (nach Dokument-Struktur)
Dieser Chunker nutzt die **Struktur** des Dokuments:

- meist **ein Chunk pro erkanntem Dokument-Element**
- Listenpunkte werden standardmäßig **zusammengeführt** (optional abschaltbar)
- relevante Metadaten wie **Überschriften** und **Bildunterschriften** werden angehängt

### B) `HybridChunker` (Struktur + Token-Limits)
Der `HybridChunker` baut auf der strukturbasierten Zerlegung auf und verbessert das Ergebnis zusätzlich so, dass es besser zu **Token-Limits** von KI-Modellen passt:

- **Splitten**, wenn ein Chunk zu lang ist (zu viele Tokens)
- **Zusammenführen**, wenn mehrere kleine Chunks gut zusammenpassen (standardmäßig aktiv; optional abschaltbar)

---

## Kurz-Merksätze

- **`DoclingDocument`**: ein einheitlicher Bauplan, der Inhalt + Struktur (Lesereihenfolge) speichert.
- **Chunking**: macht aus einem Dokument viele kleine Textstücke (Chunks) mit Kontext.
- **HierarchicalChunker**: teilt nach Struktur.
- **HybridChunker**: teilt nach Struktur und optimiert zusätzlich für Token-Limits.


