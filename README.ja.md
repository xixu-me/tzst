[🇬🇧 English](./README.md) | [🇨🇳 汉语](./README.zh.md) | [🇪🇸 español](./README.es.md) | **🇯🇵 日本語** | [🇦🇪 العربية](./README.ar.md) | [🇷🇺 русский](./README.ru.md) | [🇩🇪 Deutsch](./README.de.md) | [🇫🇷 français](./README.fr.md) | [🇰🇷 한국어](./README.ko.md) | [🇧🇷 português](./README.pt.md)

# tzst

[![codecov](https://codecov.io/gh/xixu-me/tzst/graph/badge.svg?token=2AIN1559WU)](https://codecov.io/gh/xixu-me/tzst)
[![CodeQL](https://github.com/xixu-me/tzst/actions/workflows/github-code-scanning/codeql/badge.svg)](https://github.com/xixu-me/tzst/actions/workflows/github-code-scanning/codeql)
[![CI/CD](https://github.com/xixu-me/tzst/actions/workflows/ci.yml/badge.svg)](https://github.com/xixu-me/tzst/actions/workflows/ci.yml)
[![PyPI - Version](https://img.shields.io/pypi/v/tzst)](https://pypi.org/project/tzst/)
[![GitHub License](https://img.shields.io/github/license/xixu-me/tzst)](LICENSE)
[![Sponsor](https://img.shields.io/badge/Sponsor-violet)](https://xi-xu.me/#sponsorships)

**tzst** は、最新のアーカイブ管理のために設計された次世代の Python ライブラリであり、最先端の Zstandard 圧縮を利用して、優れたパフォーマンス、セキュリティ、信頼性を提供します。Python 3.12 以降専用に構築されたこのエンタープライズグレードのソリューションは、アトミック操作、ストリーミング効率、および綿密に作成された API を組み合わせることで、開発者が本番環境で `.tzst` / `.tar.zst` アーカイブを処理する方法を再定義します。🚀

## ✨ 特徴

- **🗜️ 高圧縮**: 優れた圧縮率と速度を実現する Zstandard 圧縮
- **📁 Tar 互換性**: Zstandard で圧縮された標準の tar アーカイブを作成
- **💻 コマンドラインインターフェース**: ストリーミングサポートと包括的なオプションを備えた直感的な CLI
- **🐍 Python API**: プログラムで使用するためのクリーンな Pythonic API
- **🌍 クロスプラットフォーム**: Windows、macOS、Linux で動作
- **📂 複数の拡張子**: `.tzst` と `.tar.zst` の両方の拡張子をサポート
- **💾 メモリ効率**: 最小限のメモリ使用量で大規模なアーカイブを処理するためのストリーミングモード
- **⚡ アトミック操作**: 中断時の自動クリーンアップによる安全なファイル操作
- **🔒 デフォルトで安全**: 抽出中に最大限のセキュリティを確保するために「data」フィルターを使用
- **🚨 強化されたエラー処理**: 役立つ代替案を備えた明確なエラーメッセージ

## 📥 インストール

### GitHub リリースから

Python のインストールを必要としないスタンドアロンの実行可能ファイルをダウンロードします。

#### サポートされているプラットフォーム

| プラットフォーム | アーキテクチャ | ファイル                               |
|----------|-------------|------|
| **🐧 Linux** | x86_64 | `tzst-v{version}-linux-x86_64.zip` |
| **🐧 Linux** | ARM64 | `tzst-v{version}-linux-aarch64.zip` |
| **🪟 Windows** | x64 | `tzst-v{version}-windows-amd64.zip` |
| **🪟 Windows** | ARM64 | `tzst-v{version}-windows-arm64.zip` |
| **🍎 macOS** | Intel | `tzst-v{version}-macos-x86_64.zip` |
| **🍎 macOS** | Apple Silicon | `tzst-v{version}-macos-arm64.zip` |

#### 🛠️ インストール手順

1. **📥 ダウンロード**: [最新のリリース ページ](https://github.com/xixu-me/tzst/releases/latest) から、お使いのプラットフォームに適したアーカイブをダウンロードします。
2. **📦 抽出**: アーカイブを**抽出**して、`tzst` 実行可能ファイル (Windows の場合は `tzst.exe`) を取得します。
3. **📂 移動**: 実行可能ファイルを PATH 内のディレクトリに**移動**します。
   - **🐧 Linux/macOS**: `sudo mv tzst /usr/local/bin/`
   - **🪟 Windows**: `tzst.exe` を含むディレクトリを PATH 環境変数に追加します。
4. **✅ 検証**: インストールを**検証**します: `tzst --help`

#### 🎯 バイナリインストールの利点

- ✅ **Python は不要** - スタンドアロンの実行可能ファイル
- ✅ **起動が高速** - Python インタープリターのオーバーヘッドがない
- ✅ **簡単なデプロイ** - 単一ファイル配布
- ✅ **一貫した動作** - バンドルされた依存関係

### 📦 PyPI から

```
pip install tzst
```

### 🔧 ソースから

```
git clone https://github.com/xixu-me/tzst.git
cd tzst
pip install .
```

### 🚀 開発インストール

このプロジェクトでは、最新の Python パッケージング標準を使用しています。

```
git clone https://github.com/xixu-me/tzst.git
cd tzst
pip install -e .[dev]
```

## 🚀 クイックスタート

### 💻 コマンドラインの使用

> **注**: 最高のパフォーマンスと Python への依存関係がないように、[スタンドアロンバイナリ](#github-リリースから)をダウンロードしてください。あるいは、インストールせずに実行するには `uvx tzst` を使用してください。詳細については、[uv ドキュメント](https://docs.astral.sh/uv/) を参照してください。

```
# 📁 アーカイブを作成
tzst a archive.tzst file1.txt file2.txt directory/

# 📤 アーカイブを抽出
tzst x archive.tzst

# 📋 アーカイブの内容をリスト
tzst l archive.tzst

# 🧪 アーカイブの整合性をテスト
tzst t archive.tzst
```

### 🐍 Python API の使用

```
from tzst import create_archive, extract_archive, list_archive

# アーカイブを作成
create_archive("archive.tzst", ["file1.txt", "file2.txt", "directory/"])

# アーカイブを抽出
extract_archive("archive.tzst", "output_directory/")

# アーカイブの内容をリスト
contents = list_archive("archive.tzst", verbose=True)
for item in contents:
    print(f"{item['name']}: {item['size']} bytes")
```

## 💻 コマンドラインインターフェース

### 📁 アーカイブ操作

#### ➕ アーカイブを作成

```
# 基本的な使用法
tzst a archive.tzst file1.txt file2.txt

# 圧縮レベルを指定 (1-22, デフォルト: 3)
tzst a archive.tzst files/ -l 15

# 代替コマンド
tzst add archive.tzst files/
tzst create archive.tzst files/
```

#### 📤 アーカイブを抽出

```
# ディレクトリ構造全体を抽出
tzst x archive.tzst

# 特定のディレクトリに抽出
tzst x archive.tzst -o output/

# 特定のファイルを抽出
tzst x archive.tzst file1.txt dir/file2.txt

# ディレクトリ構造なしで抽出 (フラット)
tzst e archive.tzst -o output/

# 大規模アーカイブにストリーミングモードを使用
tzst x archive.tzst --streaming -o output/
```

#### 📋 内容をリスト

```
# 簡単なリスト
tzst l archive.tzst

# 詳細を含む詳細リスト
tzst l archive.tzst -v

# 大規模アーカイブにストリーミングモードを使用
tzst l archive.tzst --streaming -v
```

#### 🧪 整合性をテスト

```
# アーカイブの整合性をテスト
tzst t archive.tzst

# ストリーミングモードでテスト
tzst t archive.tzst --streaming
```

### 📊 コマンドリファレンス

| コマンド | エイリアス | 説明 | ストリーミングサポート |
|---------|---------|-------------|-------------------|
| `a` | `add`, `create` | アーカイブを作成または追加 | N/A |
| `x` | `extract` | フルパスで抽出 | ✓ `--streaming` |
| `e` | `extract-flat` | ディレクトリ構造なしで抽出 | ✓ `--streaming` |
| `l` | `list` | アーカイブの内容をリスト | ✓ `--streaming` |
| `t` | `test` | アーカイブの整合性をテスト | ✓ `--streaming` |

### ⚙️ CLI オプション

- `-v, --verbose`: 詳細出力を有効にする
- `-o, --output DIR`: 出力ディレクトリを指定 (抽出コマンド)
- `-l, --level LEVEL`: 圧縮レベルを 1-22 に設定 (作成コマンド)
- `--streaming`: メモリ効率の高い処理のためにストリーミングモードを有効にする
- `--filter FILTER`: 抽出のセキュリティフィルター (data/tar/fully_trusted)
- `--no-atomic`: アトミックファイル操作を無効にする (推奨されません)

### 🔒 セキュリティフィルター

```
# 最大セキュリティで抽出 (デフォルト)
tzst x archive.tzst --filter data

# 標準の tar 互換性で抽出
tzst x archive.tzst --filter tar

# 完全な信頼で抽出 (危険 - 信頼できるアーカイブのみ)
tzst x archive.tzst --filter fully_trusted
```

**🔐 セキュリティフィルターオプション:**

- `data` (デフォルト): 最も安全。危険なファイル、絶対パス、および抽出ディレクトリ外のパスをブロックします
- `tar`: 標準の tar 互換性。絶対パスとディレクトリトラバーサルをブロックします
- `fully_trusted`: セキュリティ制限なし。完全に信頼できるアーカイブでのみ使用してください

## 🐍 Python API

### 📦 TzstArchive クラス

```
from tzst import TzstArchive

# 新しいアーカイブを作成
with TzstArchive("archive.tzst", "w", compression_level=5) as archive:
    archive.add("file.txt")
    archive.add("directory/", recursive=True)

# 既存のアーカイブを読み取り
with TzstArchive("archive.tzst", "r") as archive:
    # 内容をリスト
    contents = archive.list(verbose=True)
    
    # セキュリティフィルターで抽出
    archive.extract("file.txt", "output/", filter="data")
    
    # 整合性をテスト
    is_valid = archive.test()

# 大規模アーカイブの場合は、ストリーミングモードを使用
with TzstArchive("large_archive.tzst", "r", streaming=True) as archive:
    archive.extract(path="output/")
```

**⚠️ 重要な制限事項:**

- **❌ 追加モードはサポートされていません**: 複数のアーカイブを作成するか、代わりにアーカイブ全体を再作成してください

### 🎯 便利な関数

#### 📁 create_archive()

```
from tzst import create_archive

# アトミック操作で作成 (デフォルト)
create_archive(
    archive_path="backup.tzst",
    files=["documents/", "photos/", "config.txt"],
    compression_level=10
)
```

#### 📤 extract_archive()

```
from tzst import extract_archive

# セキュリティで抽出 (デフォルト: 'data' フィルター)
extract_archive("backup.tzst", "restore/")

# 特定のファイルを抽出
extract_archive("backup.tzst", "restore/", members=["config.txt"])

# ディレクトリ構造をフラット化
extract_archive("backup.tzst", "restore/", flatten=True)

# 大規模アーカイブにストリーミングを使用
extract_archive("large_backup.tzst", "restore/", streaming=True)
```

#### 📋 list_archive()

```
from tzst import list_archive

# 簡単なリスト
files = list_archive("backup.tzst")

# 詳細なリスト
files = list_archive("backup.tzst", verbose=True)

# 大規模アーカイブのストリーミング
files = list_archive("large_backup.tzst", streaming=True)
```

#### 🧪 test_archive()

```
from tzst import test_archive

# 基本的な整合性テスト
if test_archive("backup.tzst"):
    print("アーカイブは有効です")

# ストリーミングでテスト
if test_archive("large_backup.tzst", streaming=True):
    print("大規模アーカイブは有効です")
```

## 🔧 高度な機能

### 📂 ファイル拡張子

ライブラリは、インテリジェントな正規化によりファイル拡張子を自動的に処理します。

- `.tzst` - tar+zstandard アーカイブのプライマリ拡張子
- `.tar.zst` - 代替の標準拡張子
- 既存のアーカイブを開くときの自動検出
- アーカイブを作成するときの自動拡張子追加

```
# これらはすべて有効なアーカイブを作成します
create_archive("backup.tzst", files)      # backup.tzst を作成
create_archive("backup.tar.zst", files)  # backup.tar.zst を作成  
create_archive("backup", files)          # backup.tzst を作成
create_archive("backup.txt", files)      # backup.tzst を作成 (正規化)
```

### 🗜️ 圧縮レベル

Zstandard 圧縮レベルの範囲は、1 (最速) から 22 (最高の圧縮) です。

- **レベル 1-3**: 高速圧縮、より大きなファイル
- **レベル 3** (デフォルト): 速度と圧縮の良好なバランス
- **レベル 10-15**: より良い圧縮、より遅い
- **レベル 20-22**: 最大圧縮、はるかに遅い

### 🌊 ストリーミングモード

大規模アーカイブのメモリ効率の高い処理には、ストリーミングモードを使用します。

**✅ 利点:**

- メモリ使用量を大幅に削減
- メモリに収まらないアーカイブのパフォーマンスを向上
- リソースの自動クリーンアップ

**🎯 使用するタイミング:**

- 100MB を超えるアーカイブ
- 制限されたメモリ環境
- 多数の大きなファイルを含むアーカイブの処理

```
# 例: 大規模バックアップアーカイブの処理
from tzst import extract_archive, list_archive, test_archive

large_archive = "backup_500gb.tzst"

# メモリ効率の高い操作
is_valid = test_archive(large_archive, streaming=True)
contents = list_archive(large_archive, streaming=True, verbose=True)
extract_archive(large_archive, "restore/", streaming=True)
```

### ⚡ アトミック操作

すべてのファイル作成操作は、デフォルトでアトミックファイル操作を使用します。

- アーカイブは最初に一時ファイルに作成され、その後アトミックに移動されます
- プロセスが中断された場合の自動クリーンアップ
- 破損したアーカイブまたは不完全なアーカイブのリスクはありません
- クロスプラットフォーム互換性

```
# アトミック操作はデフォルトで有効になっています
create_archive("important.tzst", files)  # 中断から安全

# 必要に応じて無効にすることができます (推奨されません)
create_archive("test.tzst", files, use_temp_file=False)
```

### 🚨 エラー処理

```
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
    print("アーカイブの解凍に失敗しました")
except TzstFileNotFoundError:
    print("アーカイブファイルが見つかりません")
except KeyboardInterrupt:
    print("ユーザーによって操作が中断されました")
    # クリーンアップは自動的に処理されます
```

## 🚀 パフォーマンスと比較

### 💡 パフォーマンスのヒント

1. **🗜️ 圧縮レベル**: レベル 3 はほとんどのユースケースに最適です
2. **🌊 ストリーミング**: 100MB を超えるアーカイブに使用します
3. **📦 バッチ操作**: 単一セッションで複数のファイルを追加します
4. **📄 ファイルタイプ**: 既に圧縮されているファイルはそれ以上圧縮されません

### 🆚 他のツールとの比較

**vs tar + gzip:**

- ✅ より良い圧縮率
- ⚡ より高速な解凍
- 🔄 最新のアルゴリズム

**vs tar + xz:**

- 🚀 非常に高速な圧縮
- 📊 同様の圧縮率
- ⚖️ より良い速度/圧縮のトレードオフ

**vs zip:**

- 🗜️ より良い圧縮
- 🔐 Unix の権限とメタデータを保持します
- 🌊 より良いストリーミングサポート

## 📋 要件

- 🐍 Python 3.12 以降
- 📦 zstandard >= 0.19.0

## 🛠️ 開発

### 🚀 開発環境のセットアップ

このプロジェクトでは、最新の Python パッケージング標準を使用しています。

```
git clone https://github.com/xixu-me/tzst.git
cd tzst
pip install -e .[dev]
```

### 🧪 テストの実行

```
# カバレッジ付きでテストを実行
pytest --cov=tzst --cov-report=html

# または、より簡単なコマンドを使用します (カバレッジ設定は pyproject.toml にあります)
pytest
```

### ✨ コード品質

```
# コード品質を確認
ruff check src tests

# コードをフォーマット
ruff format src tests
```

## 🤝 貢献

貢献を歓迎します！以下について、[貢献ガイド](CONTRIBUTING.md)をお読みください。

- 開発のセットアップとプロジェクト構造
- コーディングスタイルのガイドラインとベストプラクティス
- テスト要件とテストの作成
- プルリクエストプロセスとレビューワークフロー

### 🚀 コントリビューター向けのクイックスタート

```
git clone https://github.com/xixu-me/tzst.git
cd tzst
pip install -e .[dev]
python -m pytest tests/
```

### 🎯 歓迎する貢献の種類

- 🐛 **バグ修正** - 既存の機能の問題を修正します
- ✨ **機能** - ライブラリに新しい機能を追加します
- 📚 **ドキュメント** - ドキュメントを改善または追加します
- 🧪 **テスト** - テストカバレッジを追加または改善します
- ⚡ **パフォーマンス** - 既存のコードを最適化します
- 🔒 **セキュリティ** - セキュリティ脆弱性に対処します

## 🙏 謝辞

- 優れた圧縮アルゴリズムを提供する[Meta Zstandard](https://github.com/facebook/zstd)
- Python バインディングを提供する[python-zstandard](https://github.com/indygreg/python-zstandard)
- インスピレーションとフィードバックを提供する Python コミュニティ

## 📄 ライセンス

Copyright &copy; 2025 [Xi Xu](https://xi-xu.me). All rights reserved.

[BSD 3-Clause](LICENSE)ライセンスの下でライセンスされています。
