<h1 align="center">
<img src="https://raw.githubusercontent.com/xixu-me/tzst/refs/heads/main/docs/_static/tzst-logo.png" width="300">
</h1><br>

[![codecov](https://codecov.io/gh/xixu-me/tzst/graph/badge.svg?token=2AIN1559WU)](https://codecov.io/gh/xixu-me/tzst)
[![CodeQL](https://github.com/xixu-me/tzst/actions/workflows/github-code-scanning/codeql/badge.svg)](https://github.com/xixu-me/tzst/actions/workflows/github-code-scanning/codeql)
[![CI/CD](https://github.com/xixu-me/tzst/actions/workflows/ci.yml/badge.svg)](https://github.com/xixu-me/tzst/actions/workflows/ci.yml)
[![PyPI - Version](https://img.shields.io/pypi/v/tzst)](https://pypi.org/project/tzst/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/tzst)](https://pypi.org/project/tzst/)
[![GitHub License](https://img.shields.io/github/license/xixu-me/tzst)](LICENSE)
[![Sponsor](https://img.shields.io/badge/Sponsor-violet)](https://xi-xu.me/#sponsorships)
[![Documentation](https://img.shields.io/badge/Documentation-blue)](https://tzst.xi-xu.me)

[🇺🇸 English](./README.md) | [🇨🇳 汉语](./README.zh.md) | [🇪🇸 español](./README.es.md) | [🇯🇵 日本語](./README.ja.md) | [🇦🇪 العربية](./README.ar.md) | [🇷🇺 русский](./README.ru.md) | [🇩🇪 Deutsch](./README.de.md) | **🇫🇷 français** | [🇰🇷 한국어](./README.ko.md) | [🇧🇷 português](./README.pt.md)

**tzst** est une bibliothèque Python de nouvelle génération conçue pour la gestion moderne d'archives, exploitant la compression Zstandard de pointe pour offrir des performances, une sécurité et une fiabilité supérieures. Construite exclusivement pour Python 3.12+, cette solution de niveau entreprise combine des opérations atomiques, l'efficacité du streaming et une API méticuleusement conçue pour redéfinir la façon dont les développeurs gèrent les archives `.tzst`/`.tar.zst` dans les environnements de production. 🚀

## ✨ Fonctionnalités

- **🗜️ Compression élevée** : Compression Zstandard pour d'excellents taux de compression et une vitesse remarquable
- **📁 Compatibilité Tar** : Crée des archives tar standard compressées avec Zstandard
- **💻 Interface en ligne de commande** : CLI intuitive avec support de streaming et options complètes
- **🐍 API Python** : API propre et pythonique pour un usage programmatique
- **🌍 Multi-plateforme** : Fonctionne sur Windows, macOS et Linux
- **📂 Extensions multiples** : Supporte les extensions `.tzst` et `.tar.zst`
- **💾 Efficace en mémoire** : Mode streaming pour gérer de grandes archives avec une utilisation mémoire minimale
- **⚡ Opérations atomiques** : Opérations de fichiers sécurisées avec nettoyage automatique en cas d'interruption
- **🔒 Sécurisé par défaut** : Utilise le filtre 'data' pour une sécurité maximale lors de l'extraction
- **🚨 Gestion d'erreurs améliorée** : Messages d'erreur clairs avec des alternatives utiles

## 📥 Installation

### Depuis les Releases GitHub

Téléchargez des exécutables autonomes qui ne nécessitent pas d'installation Python :

#### Plateformes supportées

| Plateforme | Architecture | Fichier |
|----------|-------------|------|
| **🐧 Linux** | x86_64 | `tzst-{version}-linux-amd64.zip` |
| **🐧 Linux** | ARM64 | `tzst-{version}-linux-arm64.zip` |
| **🪟 Windows** | x64 | `tzst-{version}-windows-amd64.zip` |
| **🪟 Windows** | ARM64 | `tzst-{version}-windows-arm64.zip` |
| **🍎 macOS** | Intel | `tzst-{version}-darwin-amd64.zip` |
| **🍎 macOS** | Apple Silicon | `tzst-{version}-darwin-arm64.zip` |

#### 🛠️ Étapes d'installation

1. **📥 Téléchargez** l'archive appropriée pour votre plateforme depuis la [page des dernières versions](https://github.com/xixu-me/tzst/releases/latest)
2. **📦 Extrayez** l'archive pour obtenir l'exécutable `tzst` (ou `tzst.exe` sous Windows)
3. **📂 Déplacez** l'exécutable vers un répertoire dans votre PATH :
   - **🐧 Linux/macOS** : `sudo mv tzst /usr/local/bin/`
   - **🪟 Windows** : Ajoutez le répertoire contenant `tzst.exe` à votre variable d'environnement PATH
4. **✅ Vérifiez** l'installation : `tzst --help`

#### 🎯 Avantages de l'installation binaire

- ✅ **Aucun Python requis** - Exécutable autonome
- ✅ **Démarrage plus rapide** - Aucune surcharge d'interpréteur Python
- ✅ **Déploiement facile** - Distribution en fichier unique
- ✅ **Comportement cohérent** - Dépendances intégrées

### 📦 Depuis PyPI

```bash
pip install tzst
```

### 🔧 Depuis le code source

```bash
git clone https://github.com/xixu-me/tzst.git
cd tzst
pip install .
```

### 🚀 Installation de développement

Ce projet utilise les standards modernes d'empaquetage Python :

```bash
git clone https://github.com/xixu-me/tzst.git
cd tzst
pip install -e .[dev]
```

## 🚀 Démarrage rapide

### 💻 Utilisation en ligne de commande

> **Note** : Téléchargez le [binaire autonome](#depuis-les-releases-github) pour les meilleures performances et aucune dépendance Python. Alternativement, utilisez `uvx tzst` pour exécuter sans installation. Voir la [documentation uv](https://docs.astral.sh/uv/) pour les détails.

```bash
# 📁 Créer une archive
tzst a archive.tzst file1.txt file2.txt directory/

# 📤 Extraire une archive
tzst x archive.tzst

# 📋 Lister le contenu d'une archive
tzst l archive.tzst

# 🧪 Tester l'intégrité d'une archive
tzst t archive.tzst
```

### 🐍 Utilisation de l'API Python

```python
from tzst import create_archive, extract_archive, list_archive

# Créer une archive
create_archive("archive.tzst", ["file1.txt", "file2.txt", "directory/"])

# Extraire une archive
extract_archive("archive.tzst", "output_directory/")

# Lister le contenu d'une archive
contents = list_archive("archive.tzst", verbose=True)
for item in contents:
    print(f"{item['name']}: {item['size']} bytes")
```

## 💻 Interface en ligne de commande

### 📁 Opérations d'archives

#### ➕ Créer une archive

```bash
# Utilisation de base
tzst a archive.tzst file1.txt file2.txt

# Avec niveau de compression (1-22, défaut : 3)
tzst a archive.tzst files/ -l 15

# Commandes alternatives
tzst add archive.tzst files/
tzst create archive.tzst files/
```

#### 📤 Extraire une archive

```bash
# Extraire avec structure complète des répertoires
tzst x archive.tzst

# Extraire vers un répertoire spécifique
tzst x archive.tzst -o output/

# Extraire des fichiers spécifiques
tzst x archive.tzst file1.txt dir/file2.txt

# Extraire sans structure de répertoires (à plat)
tzst e archive.tzst -o output/

# Utiliser le mode streaming pour de grandes archives
tzst x archive.tzst --streaming -o output/
```

#### 📋 Lister le contenu

```bash
# Liste simple
tzst l archive.tzst

# Liste détaillée avec informations
tzst l archive.tzst -v

# Utiliser le mode streaming pour de grandes archives
tzst l archive.tzst --streaming -v
```

#### 🧪 Tester l'intégrité

```bash
# Tester l'intégrité de l'archive
tzst t archive.tzst

# Tester avec le mode streaming
tzst t archive.tzst --streaming
```

### 📊 Référence des commandes

| Commande | Alias | Description | Support streaming |
|---------|---------|-------------|-------------------|
| `a` | `add`, `create` | Créer ou ajouter à une archive | N/A |
| `x` | `extract` | Extraire avec chemins complets | ✓ `--streaming` |
| `e` | `extract-flat` | Extraire sans structure de répertoires | ✓ `--streaming` |
| `l` | `list` | Lister le contenu de l'archive | ✓ `--streaming` |
| `t` | `test` | Tester l'intégrité de l'archive | ✓ `--streaming` |

### ⚙️ Options CLI

- `-v, --verbose` : Activer la sortie détaillée
- `-o, --output DIR` : Spécifier le répertoire de sortie (commandes d'extraction)
- `-l, --level LEVEL` : Définir le niveau de compression 1-22 (commande de création)
- `--streaming` : Activer le mode streaming pour un traitement efficace en mémoire
- `--filter FILTER` : Filtre de sécurité pour l'extraction (data/tar/fully_trusted)
- `--no-atomic` : Désactiver les opérations de fichiers atomiques (non recommandé)

### 🔒 Filtres de sécurité

```bash
# Extraire avec sécurité maximale (défaut)
tzst x archive.tzst --filter data

# Extraire avec compatibilité tar standard
tzst x archive.tzst --filter tar

# Extraire avec confiance totale (dangereux - uniquement pour les archives de confiance)
tzst x archive.tzst --filter fully_trusted
```

**🔐 Options de filtre de sécurité :**

- `data` (défaut) : Le plus sécurisé. Bloque les fichiers dangereux, les chemins absolus et les chemins en dehors du répertoire d'extraction
- `tar` : Compatibilité tar standard. Bloque les chemins absolus et la traversée de répertoires
- `fully_trusted` : Aucune restriction de sécurité. À utiliser uniquement avec des archives entièrement fiables

## 🐍 API Python

### 📦 Classe TzstArchive

```python
from tzst import TzstArchive

# Créer une nouvelle archive
with TzstArchive("archive.tzst", "w", compression_level=5) as archive:
    archive.add("file.txt")
    archive.add("directory/", recursive=True)

# Lire une archive existante
with TzstArchive("archive.tzst", "r") as archive:
    # Lister le contenu
    contents = archive.list(verbose=True)
    
    # Extraire avec filtre de sécurité
    archive.extract("file.txt", "output/", filter="data")
    
    # Tester l'intégrité
    is_valid = archive.test()

# Pour de grandes archives, utiliser le mode streaming
with TzstArchive("large_archive.tzst", "r", streaming=True) as archive:
    archive.extract(path="output/")
```

**⚠️ Limitations importantes :**

- **❌ Mode d'ajout non supporté** : Créez plusieurs archives ou recréez l'archive entière à la place

### 🎯 Fonctions de convenance

#### 📁 create_archive()

```python
from tzst import create_archive

# Créer avec opérations atomiques (défaut)
create_archive(
    archive_path="backup.tzst",
    files=["documents/", "photos/", "config.txt"],
    compression_level=10
)
```

#### 📤 extract_archive()

```python
from tzst import extract_archive

# Extraire avec sécurité (défaut : filtre 'data')
extract_archive("backup.tzst", "restore/")

# Extraire des fichiers spécifiques
extract_archive("backup.tzst", "restore/", members=["config.txt"])

# Aplatir la structure des répertoires
extract_archive("backup.tzst", "restore/", flatten=True)

# Utiliser le streaming pour de grandes archives
extract_archive("large_backup.tzst", "restore/", streaming=True)
```

#### 📋 list_archive()

```python
from tzst import list_archive

# Liste simple
files = list_archive("backup.tzst")

# Liste détaillée
files = list_archive("backup.tzst", verbose=True)

# Streaming pour de grandes archives
files = list_archive("large_backup.tzst", streaming=True)
```

#### 🧪 test_archive()

```python
from tzst import test_archive

# Test d'intégrité de base
if test_archive("backup.tzst"):
    print("L'archive est valide")

# Tester avec streaming
if test_archive("large_backup.tzst", streaming=True):
    print("La grande archive est valide")
```

## 🔧 Fonctionnalités avancées

### 📂 Extensions de fichiers

La bibliothèque gère automatiquement les extensions de fichiers avec normalisation intelligente :

- `.tzst` - Extension principale pour les archives tar+zstandard
- `.tar.zst` - Extension standard alternative
- Détection automatique lors de l'ouverture d'archives existantes
- Ajout automatique d'extension lors de la création d'archives

```python
# Toutes ces créent des archives valides
create_archive("backup.tzst", files)      # Crée backup.tzst
create_archive("backup.tar.zst", files)  # Crée backup.tar.zst  
create_archive("backup", files)          # Crée backup.tzst
create_archive("backup.txt", files)      # Crée backup.tzst (normalisé)
```

### 🗜️ Niveaux de compression

Les niveaux de compression Zstandard vont de 1 (le plus rapide) à 22 (meilleure compression) :

- **Niveau 1-3** : Compression rapide, fichiers plus volumineux
- **Niveau 3** (défaut) : Bon équilibre entre vitesse et compression
- **Niveau 10-15** : Meilleure compression, plus lent
- **Niveau 20-22** : Compression maximale, beaucoup plus lent

### 🌊 Mode streaming

Utilisez le mode streaming pour un traitement efficace en mémoire de grandes archives :

**✅ Avantages :**

- Utilisation mémoire considérablement réduite
- Meilleures performances pour les archives qui ne tiennent pas en mémoire
- Nettoyage automatique des ressources

**🎯 Quand utiliser :**

- Archives supérieures à 100MB
- Environnements à mémoire limitée
- Traitement d'archives avec de nombreux gros fichiers

```python
# Exemple : Traitement d'une grande archive de sauvegarde
from tzst import extract_archive, list_archive, test_archive

large_archive = "backup_500gb.tzst"

# Opérations efficaces en mémoire
is_valid = test_archive(large_archive, streaming=True)
contents = list_archive(large_archive, streaming=True, verbose=True)
extract_archive(large_archive, "restore/", streaming=True)
```

### ⚡ Opérations atomiques

Toutes les opérations de création de fichiers utilisent des opérations de fichiers atomiques par défaut :

- Archives créées dans des fichiers temporaires d'abord, puis déplacées atomiquement
- Nettoyage automatique si le processus est interrompu
- Aucun risque d'archives corrompues ou incomplètes
- Compatibilité multi-plateforme

```python
# Opérations atomiques activées par défaut
create_archive("important.tzst", files)  # Sûr contre les interruptions

# Peut être désactivé si nécessaire (non recommandé)
create_archive("test.tzst", files, use_temp_file=False)
```

### 🚨 Gestion des erreurs

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
    print("Échec de la décompression de l'archive")
except TzstFileNotFoundError:
    print("Fichier d'archive non trouvé")
except KeyboardInterrupt:
    print("Opération interrompue par l'utilisateur")
    # Le nettoyage est géré automatiquement
```

## 🚀 Performance et comparaison

### 💡 Conseils de performance

1. **🗜️ Niveaux de compression** : Le niveau 3 est optimal pour la plupart des cas d'usage
2. **🌊 Streaming** : Utilisez pour les archives supérieures à 100MB
3. **📦 Opérations par lots** : Ajoutez plusieurs fichiers en une seule session
4. **📄 Types de fichiers** : Les fichiers déjà compressés ne se compresseront pas beaucoup plus

### 🆚 vs Autres outils

**vs tar + gzip :**

- ✅ Meilleurs taux de compression
- ⚡ Décompression plus rapide
- 🔄 Algorithme moderne

**vs tar + xz :**

- 🚀 Compression significativement plus rapide
- 📊 Taux de compression similaires
- ⚖️ Meilleur compromis vitesse/compression

**vs zip :**

- 🗜️ Meilleure compression
- 🔐 Préserve les permissions Unix et métadonnées
- 🌊 Meilleur support de streaming

## 📋 Exigences

- 🐍 Python 3.12 ou supérieur
- 📦 zstandard >= 0.19.0

## 🛠️ Développement

### 🚀 Configuration de l'environnement de développement

Ce projet utilise les standards modernes d'empaquetage Python :

```bash
git clone https://github.com/xixu-me/tzst.git
cd tzst
pip install -e .[dev]
```

### 🧪 Exécution des tests

```bash
# Exécuter les tests avec couverture
pytest --cov=tzst --cov-report=html

# Ou utiliser la commande plus simple (paramètres de couverture dans pyproject.toml)
pytest
```

### ✨ Qualité du code

```bash
# Vérifier la qualité du code
ruff check src tests

# Formater le code
ruff format src tests
```

## 🤝 Contribution

Nous accueillons les contributions ! Veuillez lire notre [Guide de contribution](CONTRIBUTING.md) pour :

- Configuration de développement et structure du projet
- Directives de style de code et meilleures pratiques  
- Exigences de test et écriture de tests
- Processus de pull request et workflow de révision

### 🚀 Démarrage rapide pour les contributeurs

```bash
git clone https://github.com/xixu-me/tzst.git
cd tzst
pip install -e .[dev]
python -m pytest tests/
```

### 🎯 Types de contributions bienvenues

- 🐛 **Corrections de bugs** - Corriger les problèmes dans la fonctionnalité existante
- ✨ **Fonctionnalités** - Ajouter de nouvelles capacités à la bibliothèque
- 📚 **Documentation** - Améliorer ou ajouter de la documentation
- 🧪 **Tests** - Ajouter ou améliorer la couverture de tests
- ⚡ **Performance** - Optimiser le code existant
- 🔒 **Sécurité** - Traiter les vulnérabilités de sécurité

## 🙏 Remerciements

- [Meta Zstandard](https://github.com/facebook/zstd) pour l'excellent algorithme de compression
- [python-zstandard](https://github.com/indygreg/python-zstandard) pour les liaisons Python
- La communauté Python pour l'inspiration et les retours

## 📄 Licence

Droits d'auteur &copy; 2025 [Xi Xu](https://xi-xu.me). Tous droits réservés.

Sous licence [BSD 3-Clause](LICENSE).
