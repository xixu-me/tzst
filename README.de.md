[us English](./README.md) | [🇨🇳 汉语](./README.zh.md) | [🇪🇸 español](./README.es.md) | [🇯🇵 日本語](./README.ja.md) | [🇦🇪 العربية](./README.ar.md) | [🇷🇺 русский](./README.ru.md) | **🇩🇪 Deutsch** | [🇫🇷 français](./README.fr.md) | [🇰🇷 한국어](./README.ko.md) | [🇧🇷 português](./README.pt.md)

# tzst

[![codecov](https://codecov.io/gh/xixu-me/tzst/graph/badge.svg?token=2AIN1559WU)](https://codecov.io/gh/xixu-me/tzst)
[![CodeQL](https://github.com/xixu-me/tzst/actions/workflows/github-code-scanning/codeql/badge.svg)](https://github.com/xixu-me/tzst/actions/workflows/github-code-scanning/codeql)
[![CI/CD](https://github.com/xixu-me/tzst/actions/workflows/ci.yml/badge.svg)](https://github.com/xixu-me/tzst/actions/workflows/ci.yml)
[![PyPI - Version](https://img.shields.io/pypi/v/tzst)](https://pypi.org/project/tzst/)
[![GitHub License](https://img.shields.io/github/license/xixu-me/tzst)](LICENSE)
[![Sponsor](https://img.shields.io/badge/Sponsor-violet)](https://xi-xu.me/#sponsorships)

**tzst** ist eine Python-Bibliothek der nächsten Generation, die für modernes Archivmanagement entwickelt wurde und hochmoderne Zstandard-Komprimierung nutzt, um überlegene Leistung, Sicherheit und Zuverlässigkeit zu bieten. Ausschließlich für Python 3.12+ entwickelt, kombiniert diese Unternehmenslösung atomare Operationen, Streaming-Effizienz und eine sorgfältig erstellte API, um die Art und Weise neu zu definieren, wie Entwickler mit `.tzst`/`.tar.zst`-Archiven in Produktionsumgebungen umgehen. 🚀

## ✨ Funktionen

- **🗜️ Hohe Komprimierung**: Zstandard-Komprimierung für ausgezeichnete Komprimierungsraten und Geschwindigkeit
- **📁 Tar-Kompatibilität**: Erstellt Standard-Tar-Archive, komprimiert mit Zstandard
- **💻 Kommandozeilenschnittstelle**: Intuitive CLI mit Streaming-Unterstützung und umfassenden Optionen
- **🐍 Python API**: Saubere, pythonische API für programmatische Nutzung
- **🌍 Plattformübergreifend**: Funktioniert auf Windows, macOS und Linux
- **📂 Mehrere Erweiterungen**: Unterstützt sowohl `.tzst` als auch `.tar.zst` Erweiterungen
- **💾 Speichereffizient**: Streaming-Modus für die Behandlung großer Archive mit minimalem Speicherverbrauch
- **⚡ Atomare Operationen**: Sichere Dateioperationen mit automatischer Bereinigung bei Unterbrechung
- **🔒 Standardmäßig sicher**: Verwendet den 'data' Filter für maximale Sicherheit beim Extrahieren
- **🚨 Verbesserte Fehlerbehandlung**: Klare Fehlermeldungen mit hilfreichen Alternativen

## 📥 Installation

### Von GitHub Releases

Lade eigenständige ausführbare Dateien herunter, die keine Python-Installation erfordern:

#### Unterstützte Plattformen

| Plattform | Architektur | Datei |
|----------|-------------|------|
| **🐧 Linux** | x86_64 | `tzst-v{Version}-linux-x86_64.zip` |
| **🐧 Linux** | ARM64 | `tzst-v{Version}-linux-aarch64.zip` |
| **🪟 Windows** | x64 | `tzst-v{Version}-windows-amd64.zip` |
| **🪟 Windows** | ARM64 | `tzst-v{Version}-windows-arm64.zip` |
| **🍎 macOS** | Intel | `tzst-v{Version}-macos-x86_64.zip` |
| **🍎 macOS** | Apple Silicon | `tzst-v{Version}-macos-arm64.zip` |

#### 🛠️ Installationsschritte

1. **📥 Lade** das entsprechende Archiv für deine Plattform von der [Seite der neuesten Releases](https://github.com/xixu-me/tzst/releases/latest) herunter
2. **📦 Extrahiere** das Archiv, um die ausführbare Datei `tzst` (oder `tzst.exe` unter Windows) zu erhalten
3. **📂 Verschiebe** die ausführbare Datei in ein Verzeichnis in deinem PATH:
   - **🐧 Linux/macOS**: `sudo mv tzst /usr/local/bin/`
   - **🪟 Windows**: Füge das Verzeichnis mit `tzst.exe` zu deiner PATH-Umgebungsvariable hinzu
4. **✅ Überprüfe** die Installation: `tzst --help`

#### 🎯 Vorteile der Binärinstallation

- ✅ **Kein Python erforderlich** - Eigenständige ausführbare Datei
- ✅ **Schnellerer Start** - Kein Python-Interpreter-Overhead
- ✅ **Einfache Bereitstellung** - Einzeldatei-Distribution
- ✅ **Konsistentes Verhalten** - Gebündelte Abhängigkeiten

### 📦 Von PyPI

```bash
pip install tzst
```

### 🔧 Aus dem Quellcode

```bash
git clone https://github.com/xixu-me/tzst.git
cd tzst
pip install .
```

### 🚀 Entwicklungsinstallation

Dieses Projekt verwendet moderne Python-Packaging-Standards:

```bash
git clone https://github.com/xixu-me/tzst.git
cd tzst
pip install -e .[dev]
```

## 🚀 Schnellstart

### 💻 Kommandozeilennutzung

> **Hinweis**: Lade die [eigenständige Binärdatei](#von-github-releases) für beste Leistung und keine Python-Abhängigkeit herunter. Alternativ verwende `uvx tzst` für die Ausführung ohne Installation. Siehe [uv-Dokumentation](https://docs.astral.sh/uv/) für Details.

```bash
# 📁 Archiv erstellen
tzst a archive.tzst file1.txt file2.txt directory/

# 📤 Archiv extrahieren
tzst x archive.tzst

# 📋 Archivinhalt auflisten
tzst l archive.tzst

# 🧪 Archivintegrität testen
tzst t archive.tzst
```

### 🐍 Python API Nutzung

```python
from tzst import create_archive, extract_archive, list_archive

# Archiv erstellen
create_archive("archive.tzst", ["file1.txt", "file2.txt", "directory/"])

# Archiv extrahieren
extract_archive("archive.tzst", "output_directory/")

# Archivinhalt auflisten
contents = list_archive("archive.tzst", verbose=True)
for item in contents:
    print(f"{item['name']}: {item['size']} bytes")
```

## 💻 Kommandozeilenschnittstelle

### 📁 Archivoperationen

#### ➕ Archiv erstellen

```bash
# Grundlegende Nutzung
tzst a archive.tzst file1.txt file2.txt

# Mit Komprimierungsstufe (1-22, Standard: 3)
tzst a archive.tzst files/ -l 15

# Alternative Befehle
tzst add archive.tzst files/
tzst create archive.tzst files/
```

#### 📤 Archiv extrahieren

```bash
# Mit vollständiger Verzeichnisstruktur extrahieren
tzst x archive.tzst

# In spezifisches Verzeichnis extrahieren
tzst x archive.tzst -o output/

# Spezifische Dateien extrahieren
tzst x archive.tzst file1.txt dir/file2.txt

# Ohne Verzeichnisstruktur extrahieren (flach)
tzst e archive.tzst -o output/

# Streaming-Modus für große Archive verwenden
tzst x archive.tzst --streaming -o output/
```

#### 📋 Inhalt auflisten

```bash
# Einfache Auflistung
tzst l archive.tzst

# Ausführliche Auflistung mit Details
tzst l archive.tzst -v

# Streaming-Modus für große Archive verwenden
tzst l archive.tzst --streaming -v
```

#### 🧪 Integrität testen

```bash
# Archivintegrität testen
tzst t archive.tzst

# Mit Streaming-Modus testen
tzst t archive.tzst --streaming
```

### 📊 Befehlsreferenz

| Befehl | Aliase | Beschreibung | Streaming-Unterstützung |
|---------|---------|-------------|-------------------|
| `a` | `add`, `create` | Archiv erstellen oder hinzufügen | N/A |
| `x` | `extract` | Mit vollständigen Pfaden extrahieren | ✓ `--streaming` |
| `e` | `extract-flat` | Ohne Verzeichnisstruktur extrahieren | ✓ `--streaming` |
| `l` | `list` | Archivinhalt auflisten | ✓ `--streaming` |
| `t` | `test` | Archivintegrität testen | ✓ `--streaming` |

### ⚙️ CLI-Optionen

- `-v, --verbose`: Ausführliche Ausgabe aktivieren
- `-o, --output DIR`: Ausgabeverzeichnis spezifizieren (Extraktionsbefehle)
- `-l, --level LEVEL`: Komprimierungsstufe 1-22 setzen (Erstellungsbefehl)
- `--streaming`: Streaming-Modus für speichereffiziente Verarbeitung aktivieren
- `--filter FILTER`: Sicherheitsfilter für Extraktion (data/tar/fully_trusted)
- `--no-atomic`: Atomare Dateioperationen deaktivieren (nicht empfohlen)

### 🔒 Sicherheitsfilter

```bash
# Mit maximaler Sicherheit extrahieren (Standard)
tzst x archive.tzst --filter data

# Mit Standard-Tar-Kompatibilität extrahieren
tzst x archive.tzst --filter tar

# Mit vollem Vertrauen extrahieren (gefährlich - nur für vertrauenswürdige Archive)
tzst x archive.tzst --filter fully_trusted
```

**🔐 Sicherheitsfilter-Optionen:**

- `data` (Standard): Am sichersten. Blockiert gefährliche Dateien, absolute Pfade und Pfade außerhalb des Extraktionsverzeichnisses
- `tar`: Standard-Tar-Kompatibilität. Blockiert absolute Pfade und Verzeichnisdurchquerung
- `fully_trusted`: Keine Sicherheitsbeschränkungen. Nur bei vollständig vertrauenswürdigen Archiven verwenden

## 🐍 Python API

### 📦 TzstArchive Klasse

```python
from tzst import TzstArchive

# Neues Archiv erstellen
with TzstArchive("archive.tzst", "w", compression_level=5) as archive:
    archive.add("file.txt")
    archive.add("directory/", recursive=True)

# Vorhandenes Archiv lesen
with TzstArchive("archive.tzst", "r") as archive:
    # Inhalt auflisten
    contents = archive.list(verbose=True)
    
    # Mit Sicherheitsfilter extrahieren
    archive.extract("file.txt", "output/", filter="data")
    
    # Integrität testen
    is_valid = archive.test()

# Für große Archive, Streaming-Modus verwenden
with TzstArchive("large_archive.tzst", "r", streaming=True) as archive:
    archive.extract(path="output/")
```

**⚠️ Wichtige Einschränkungen:**

- **❌ Anhängemodus nicht unterstützt**: Erstelle mehrere Archive oder erstelle das gesamte Archiv neu

### 🎯 Convenience-Funktionen

#### 📁 create_archive()

```python
from tzst import create_archive

# Mit atomaren Operationen erstellen (Standard)
create_archive(
    archive_path="backup.tzst",
    files=["documents/", "photos/", "config.txt"],
    compression_level=10
)
```

#### 📤 extract_archive()

```python
from tzst import extract_archive

# Mit Sicherheit extrahieren (Standard: 'data' Filter)
extract_archive("backup.tzst", "restore/")

# Spezifische Dateien extrahieren
extract_archive("backup.tzst", "restore/", members=["config.txt"])

# Verzeichnisstruktur abflachen
extract_archive("backup.tzst", "restore/", flatten=True)

# Streaming für große Archive verwenden
extract_archive("large_backup.tzst", "restore/", streaming=True)
```

#### 📋 list_archive()

```python
from tzst import list_archive

# Einfache Auflistung
files = list_archive("backup.tzst")

# Detaillierte Auflistung
files = list_archive("backup.tzst", verbose=True)

# Streaming für große Archive
files = list_archive("large_backup.tzst", streaming=True)
```

#### 🧪 test_archive()

```python
from tzst import test_archive

# Grundlegende Integritätsprüfung
if test_archive("backup.tzst"):
    print("Archiv ist gültig")

# Mit Streaming testen
if test_archive("large_backup.tzst", streaming=True):
    print("Großes Archiv ist gültig")
```

## 🔧 Erweiterte Funktionen

### 📂 Dateierweiterungen

Die Bibliothek behandelt Dateierweiterungen automatisch mit intelligenter Normalisierung:

- `.tzst` - Primäre Erweiterung für tar+zstandard Archive
- `.tar.zst` - Alternative Standarderweiterung
- Automatische Erkennung beim Öffnen vorhandener Archive
- Automatisches Hinzufügen von Erweiterungen beim Erstellen von Archiven

```python
# Diese erstellen alle gültige Archive
create_archive("backup.tzst", files)      # Erstellt backup.tzst
create_archive("backup.tar.zst", files)  # Erstellt backup.tar.zst  
create_archive("backup", files)          # Erstellt backup.tzst
create_archive("backup.txt", files)      # Erstellt backup.tzst (normalisiert)
```

### 🗜️ Komprimierungsstufen

Zstandard-Komprimierungsstufen reichen von 1 (schnellste) bis 22 (beste Komprimierung):

- **Stufe 1-3**: Schnelle Komprimierung, größere Dateien
- **Stufe 3** (Standard): Guter Kompromiss zwischen Geschwindigkeit und Komprimierung
- **Stufe 10-15**: Bessere Komprimierung, langsamer
- **Stufe 20-22**: Maximale Komprimierung, viel langsamer

### 🌊 Streaming-Modus

Verwende den Streaming-Modus für speichereffiziente Verarbeitung großer Archive:

**✅ Vorteile:**

- Deutlich reduzierter Speicherverbrauch
- Bessere Leistung für Archive, die nicht in den Speicher passen
- Automatische Bereinigung von Ressourcen

**🎯 Wann verwenden:**

- Archive größer als 100MB
- Umgebungen mit begrenztem Speicher
- Verarbeitung von Archiven mit vielen großen Dateien

```python
# Beispiel: Verarbeitung eines großen Backup-Archivs
from tzst import extract_archive, list_archive, test_archive

large_archive = "backup_500gb.tzst"

# Speichereffiziente Operationen
is_valid = test_archive(large_archive, streaming=True)
contents = list_archive(large_archive, streaming=True, verbose=True)
extract_archive(large_archive, "restore/", streaming=True)
```

### ⚡ Atomare Operationen

Alle Dateierstellungsoperationen verwenden standardmäßig atomare Dateioperationen:

- Archive werden zuerst in temporären Dateien erstellt, dann atomisch verschoben
- Automatische Bereinigung bei Prozessunterbrechung
- Kein Risiko von beschädigten oder unvollständigen Archiven
- Plattformübergreifende Kompatibilität

```python
# Atomare Operationen standardmäßig aktiviert
create_archive("important.tzst", files)  # Sicher vor Unterbrechung

# Kann bei Bedarf deaktiviert werden (nicht empfohlen)
create_archive("test.tzst", files, use_temp_file=False)
```

### 🚨 Fehlerbehandlung

```python
from tzst import TzstArchive
from tzst.exceptions import (
    TzstError,
    TzstArchiveError,
    TzstCompressionError,
    TzstDecompressionError,
    TzstFileNotFoundError
)

try:
    with TzstArchive("archive.tzst", "r") as archive:
        archive.extract()
except TzstDecompressionError:
    print("Fehler beim Dekomprimieren des Archivs")
except TzstFileNotFoundError:
    print("Archivdatei nicht gefunden")
except KeyboardInterrupt:
    print("Operation vom Benutzer unterbrochen")
    # Bereinigung wird automatisch durchgeführt
```

## 🚀 Leistung und Vergleich

### 💡 Leistungstipps

1. **🗜️ Komprimierungsstufen**: Stufe 3 ist optimal für die meisten Anwendungsfälle
2. **🌊 Streaming**: Verwende für Archive größer als 100MB
3. **📦 Batch-Operationen**: Füge mehrere Dateien in einer Sitzung hinzu
4. **📄 Dateitypen**: Bereits komprimierte Dateien werden nicht viel weiter komprimiert

### 🆚 vs Andere Tools

**vs tar + gzip:**

- ✅ Bessere Komprimierungsraten
- ⚡ Schnellere Dekomprimierung
- 🔄 Moderner Algorithmus

**vs tar + xz:**

- 🚀 Deutlich schnellere Komprimierung
- 📊 Ähnliche Komprimierungsraten
- ⚖️ Besserer Geschwindigkeit/Komprimierung-Kompromiss

**vs zip:**

- 🗜️ Bessere Komprimierung
- 🔐 Bewahrt Unix-Berechtigungen und Metadaten
- 🌊 Bessere Streaming-Unterstützung

## 📋 Anforderungen

- 🐍 Python 3.12 oder höher
- 📦 zstandard >= 0.19.0

## 🛠️ Entwicklung

### 🚀 Entwicklungsumgebung einrichten

Dieses Projekt verwendet moderne Python-Packaging-Standards:

```bash
git clone https://github.com/xixu-me/tzst.git
cd tzst
pip install -e .[dev]
```

### 🧪 Tests ausführen

```bash
# Tests mit Coverage ausführen
pytest --cov=tzst --cov-report=html

# Oder den einfacheren Befehl verwenden (Coverage-Einstellungen sind in pyproject.toml)
pytest
```

### ✨ Code-Qualität

```bash
# Code-Qualität prüfen
ruff check src tests

# Code formatieren
ruff format src tests
```

## 🤝 Beitragen

Wir begrüßen Beiträge! Bitte lies unseren [Beitragsleitfaden](CONTRIBUTING.md) für:

- Entwicklungssetup und Projektstruktur
- Code-Stil-Richtlinien und bewährte Praktiken  
- Testanforderungen und Schreibtests
- Pull-Request-Prozess und Review-Workflow

### 🚀 Schnellstart für Mitwirkende

```bash
git clone https://github.com/xixu-me/tzst.git
cd tzst
pip install -e .[dev]
python -m pytest tests/
```

### 🎯 Arten willkommener Beiträge

- 🐛 **Fehlerbehebungen** - Probleme in vorhandener Funktionalität beheben
- ✨ **Funktionen** - Neue Fähigkeiten zur Bibliothek hinzufügen
- 📚 **Dokumentation** - Dokumentation verbessern oder hinzufügen
- 🧪 **Tests** - Testabdeckung hinzufügen oder verbessern
- ⚡ **Leistung** - Vorhandenen Code optimieren
- 🔒 **Sicherheit** - Sicherheitsschwachstellen beheben

## 🙏 Danksagungen

- [Meta Zstandard](https://github.com/facebook/zstd) für den exzellenten Komprimierungsalgorithmus
- [python-zstandard](https://github.com/indygreg/python-zstandard) für Python-Bindings
- Der Python-Community für Inspiration und Feedback

## 📄 Lizenz

Urheberrecht &copy; 2025 [Xi Xu](https://xi-xu.me). Alle Rechte vorbehalten.

Lizenziert unter der [BSD 3-Clause](LICENSE) Lizenz.
