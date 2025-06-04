[🇬🇧 English](./README.md) | [🇨🇳 汉语](./README.zh.md) | [🇪🇸 español](./README.es.md) | **🇯🇵 日本語** | [🇦🇪 العربية](./README.ar.md) | [🇷🇺 русский](./README.ru.md) | [🇩🇪 Deutsch](./README.de.md) | [🇫🇷 français](./README.fr.md) | [🇰🇷 한국어](./README.ko.md) | [🇧🇷 português](./README.pt.md)

# tzst

[![codecov](https://codecov.io/gh/xixu-me/tzst/graph/badge.svg?token=2AIN1559WU)](https://codecov.io/gh/xixu-me/tzst)
[![CodeQL](https://github.com/xixu-me/tzst/actions/workflows/github-code-scanning/codeql/badge.svg)](https://github.com/xixu-me/tzst/actions/workflows/github-code-scanning/codeql)
[![CI/CD](https://github.com/xixu-me/tzst/actions/workflows/ci.yml/badge.svg)](https://github.com/xixu-me/tzst/actions/workflows/ci.yml)
[![PyPI - Version](https://img.shields.io/pypi/v/tzst)](https://pypi.org/project/tzst/)
[![GitHub License](https://img.shields.io/github/license/xixu-me/tzst)](LICENSE)
[![Sponsor](https://img.shields.io/badge/Sponsor-violet)](https://xi-xu.me/#sponsorships)

**tzst** は、最新の Zstandard 圧縮技術を活用した次世代 Python ライブラリで、優れたパフォーマンス、セキュリティ、信頼性を提供するモダンなアーカイブ管理を実現します。 Python 3.12+ 専用に構築されたこのエンタープライズグレードのソリューションは、アトミック操作、ストリーミング効率、厳密に設計された API を組み合わせ、本番環境における `.tzst` / `.tar.zst` アーカイブの扱い方を再定義します。 🚀

## ✨ 特徴

- **🗜️ 高圧縮率**: Zstandard 圧縮による優れた圧縮率と速度
- **📁 Tar 互換性**: Zstandard で圧縮された標準 tar アーカイブを作成
- **💻 コマンドラインインターフェース**: ストリーミング対応の直感的な CLI と包括的なオプション
- **🐍 Python API**: プログラム利用のためのクリーンで Pythonic な API
- **🌍 クロスプラットフォーム**: Windows 、 macOS 、 Linux で動作
- **📂 複数拡張子対応**: `.tzst` と `.tar.zst` の両方の拡張子をサポート
- **💾 メモリ効率**: 大容量アーカイブを最小メモリ使用量で処理するストリーミングモード
- **⚡ アトミック操作**: 中断時にも安全な自動クリーンアップ付きファイル操作
- **🔒 デフォルトで安全**: 展開時の最大セキュリティのために「data」フィルタを使用
- **🚨 強化されたエラーハンドリング**: 代替案を示す明確なエラーメッセージ

## 📥 インストール

### GitHub リリースから

Python インストール不要のスタンドアロン実行ファイルをダウンロード:

#### サポート対象プラットフォーム

| プラットフォーム | アーキテクチャ | ファイル |
|----------|-------------|------|
| **🐧 Linux** | x86_64 | `tzst-v{version}-linux-x86_64.zip` |
| **🐧 Linux** | ARM64 | `tzst-v{version}-linux-aarch64.zip` |
| **🪟 Windows** | x64 | `tzst-v{version}-windows-amd64.zip` |
| **🪟 Windows** | ARM64 | `tzst-v{version}-windows-arm64.zip` |
| **🍎 macOS** | Intel | `tzst-v{version}-macos-x86_64.zip` |
| **🍎 macOS** | Apple Silicon | `tzst-v{version}-macos-arm64.zip` |

#### 🛠️ インストール手順

1. **📥 ダウンロード**: [最新リリースページ](https://github.com/xixu-me/tzst/releases/latest)からお使いのプラットフォームに合ったアーカイブをダウンロード
2. **📦 展開**: アーカイブを展開し、 `tzst` 実行ファイル（Windows の場合は `tzst.exe` ）を取得
3. **📂 移動**: 実行ファイルを PATH が通ったディレクトリに移動:
   - **🐧 Linux/macOS**: `sudo mv tzst /usr/local/bin/`
   - **🪟 Windows**: `tzst.exe` を含むディレクトリを PATH 環境変数に追加
4. **✅ 確認**: インストールを検証: `tzst --help`

#### 🎯 バイナリインストールの利点

- ✅ **Python 不要** - スタンドアロン実行ファイル
- ✅ **高速起動** - Python インタプリタのオーバーヘッドなし
- ✅ **簡単なデプロイ** - 単一ファイル配布
- ✅ **一貫した動作** - 依存関係をバンドル

### 📦 PyPI から

```bash
pip install tzst
```

### 🔧 ソースから

```bash
git clone https://github.com/xixu-me/tzst.git
cd tzst
pip install .
```

### 🚀 開発用インストール

このプロジェクトはモダンな Python パッケージング標準を使用します:

```bash
git clone https://github.com/xixu-me/tzst.git
cd tzst
pip install -e .[dev]
```

## 🚀 クイックスタート

### 💻 コマンドラインの使い方

> **注**: 最高のパフォーマンスと Python 依存なしを実現するには[スタンドアロンバイナリ](#github-リリースから)をダウンロードしてください。または、インストールなしで実行するには `uvx tzst` を使用します。詳細は [uv ドキュメント](https://docs.astral.sh/uv/)を参照。

```bash
# 📁 アーカイブ作成
tzst a archive.tzst file1.txt file2.txt directory/

# 📤 アーカイブ展開
tzst x archive.tzst

# 📋 アーカイブ内容一覧
tzst l archive.tzst

# 🧪 アーカイブ整合性テスト
tzst t archive.tzst
```

### 🐍 Python API の使い方

```python
from tzst import create_archive, extract_archive, list_archive

# アーカイブ作成
create_archive("archive.tzst", ["file1.txt", "file2.txt", "directory/"])

# アーカイブ展開
extract_archive("archive.tzst", "output_directory/")

# アーカイブ内容一覧
contents = list_archive("archive.tzst", verbose=True)
for item in contents:
    print(f"{item['name']}: {item['size']} bytes")
```

## 💻 コマンドラインインターフェース

### 📁 アーカイブ操作

#### ➕ アーカイブ作成

```bash
# 基本使用法
tzst a archive.tzst file1.txt file2.txt

# 圧縮レベル指定 (1-22, デフォルト: 3)
tzst a archive.tzst files/ -l 15

# 代替コマンド
tzst add archive.tzst files/
tzst create archive.tzst files/
```

#### 📤 アーカイブ展開

```bash
# 完全なディレクトリ構造で展開
tzst x archive.tzst

# 特定ディレクトリに展開
tzst x archive.tzst -o output/

# 特定ファイルのみ展開
tzst x archive.tzst file1.txt dir/file2.txt

# ディレクトリ構造なしで展開 (フラット)
tzst e archive.tzst -o output/

# 大容量アーカイブ用ストリーミングモード
tzst x archive.tzst --streaming -o output/
```

#### 📋 内容一覧

```bash
# シンプルな一覧表示
tzst l archive.tzst

# 詳細情報付き一覧表示
tzst l archive.tzst -v

# 大容量アーカイブ用ストリーミングモード
tzst l archive.tzst --streaming -v
```

#### 🧪 整合性テスト

```bash
# アーカイブ整合性テスト
tzst t archive.tzst

# ストリーミングモードでテスト
tzst t archive.tzst --streaming
```

### 📊 コマンドリファレンス

| コマンド | エイリアス | 説明 | ストリーミングサポート |
|---------|---------|-------------|-------------------|
| `a` | `add`, `create` | アーカイブ作成または追加 | N/A |
| `x` | `extract` | 完全パスで展開 | ✓ `--streaming` |
| `e` | `extract-flat` | ディレクトリ構造なしで展開 | ✓ `--streaming` |
| `l` | `list` | アーカイブ内容一覧 | ✓ `--streaming` |
| `t` | `test` | アーカイブ整合性テスト | ✓ `--streaming` |

### ⚙️ CLI オプション

- `-v, --verbose`: 詳細出力を有効化
- `-o, --output DIR`: 出力ディレクトリ指定 (展開コマンド)
- `-l, --level LEVEL`: 圧縮レベル設定 1-22 (作成コマンド)
- `--streaming`: メモリ効率処理のためのストリーミングモードを有効化
- `--filter FILTER`: 展開用セキュリティフィルタ (data/tar/fully_trusted)
- `--no-atomic`: アトミックファイル操作を無効化 (非推奨)

### 🔒 セキュリティフィルタ

```bash
# 最大セキュリティで展開 (デフォルト)
tzst x archive.tzst --filter data

# 標準 tar 互換で展開
tzst x archive.tzst --filter tar

# 完全信頼で展開 (危険 - 信頼済みアーカイブ専用)
tzst x archive.tzst --filter fully_trusted
```

**🔐 セキュリティフィルタオプション:**

- `data` (デフォルト): 最強のセキュリティ。危険なファイル、絶対パス、展開ディレクトリ外のパスをブロック
- `tar`: 標準 tar 互換。絶対パスとディレクトリトラバーサルをブロック
- `fully_trusted`: セキュリティ制限なし。完全に信頼できるアーカイブ専用

## 🐍 Python API

### 📦 TzstArchive クラス

```python
from tzst import TzstArchive

# 新規アーカイブ作成
with TzstArchive("archive.tzst", "w", compression_level=5) as archive:
    archive.add("file.txt")
    archive.add("directory/", recursive=True)

# 既存アーカイブ読み込み
with TzstArchive("archive.tzst", "r") as archive:
    # 内容一覧
    contents = archive.list(verbose=True)
    
    # セキュリティフィルタ付き展開
    archive.extract("file.txt", "output/", filter="data")
    
    # 整合性テスト
    is_valid = archive.test()

# 大容量アーカイブ用ストリーミングモード
with TzstArchive("large_archive.tzst", "r", streaming=True) as archive:
    archive.extract(path="output/")
```

**⚠️ 重要な制限事項:**

- **❌ 追加モード非対応**: 複数アーカイブを作成するか、アーカイブ全体を再作成してください

### 🎯 便利関数

#### 📁 create_archive()

```python
from tzst import create_archive

# アトミック操作で作成 (デフォルト)
create_archive(
    archive_path="backup.tzst",
    files=["documents/", "photos/", "config.txt"],
    compression_level=10
)
```

#### 📤 extract_archive()

```python
from tzst import extract_archive

# セキュリティ付き展開 (デフォルト: 'data' フィルタ)
extract_archive("backup.tzst", "restore/")

# 特定ファイルのみ展開
extract_archive("backup.tzst", "restore/", members=["config.txt"])

# ディレクトリ構造をフラット化
extract_archive("backup.tzst", "restore/", flatten=True)

# 大容量アーカイブ用ストリーミングモード
extract_archive("large_backup.tzst", "restore/", streaming=True)
```

#### 📋 list_archive()

```python
from tzst import list_archive

# シンプルな一覧
files = list_archive("backup.tzst")

# 詳細一覧
files = list_archive("backup.tzst", verbose=True)

# 大容量アーカイブ用ストリーミングモード
files = list_archive("large_backup.tzst", streaming=True)
```

#### 🧪 test_archive()

```python
from tzst import test_archive

# 基本的な整合性テスト
if test_archive("backup.tzst"):
    print("アーカイブは有効です")

# ストリーミングでテスト
if test_archive("large_backup.tzst", streaming=True):
    print("大容量アーカイブは有効です")
```

## 🔧 高度な機能

### 📂 ファイル拡張子

ライブラリはインテリジェントな正規化でファイル拡張子を自動処理:

- `.tzst` - tar + zstandard アーカイブの主要拡張子
- `.tar.zst` - 代替標準拡張子
- 既存アーカイブを開く際の自動検出
- アーカイブ作成時の自動拡張子追加

```python
# すべて有効なアーカイブを作成
create_archive("backup.tzst", files)      # backup.tzst を作成
create_archive("backup.tar.zst", files)  # backup.tar.zst を作成  
create_archive("backup", files)          # backup.tzst を作成
create_archive("backup.txt", files)      # backup.tzst を作成 (正規化)
```

### 🗜️ 圧縮レベル

Zstandard 圧縮レベルは 1 (最速) から 22 (最高圧縮) の範囲:

- **レベル 1-3**: 高速圧縮、ファイルサイズ大
- **レベル 3** (デフォルト): 速度と圧縮率の良いバランス
- **レベル 10-15**: 高圧縮、低速
- **レベル 20-22**: 最高圧縮、大幅に低速

### 🌊 ストリーミングモード

大容量アーカイブのメモリ効率処理にストリーミングモードを使用:

**✅ 利点:**

- メモリ使用量の大幅削減
- メモリに収まらないアーカイブのパフォーマンス向上
- リソースの自動クリーンアップ

**🎯 使用推奨ケース:**

- 100 MB を超えるアーカイブ
- メモリ制限環境
- 多数の大容量ファイルを含むアーカイブ処理

```python
# 例: 大容量バックアップアーカイブ処理
from tzst import extract_archive, list_archive, test_archive

large_archive = "backup_500gb.tzst"

# メモリ効率の良い操作
is_valid = test_archive(large_archive, streaming=True)
contents = list_archive(large_archive, streaming=True, verbose=True)
extract_archive(large_archive, "restore/", streaming=True)
```

### ⚡ アトミック操作

すべてのファイル作成操作はデフォルトでアトミックファイル操作を使用:

- 一時ファイルでアーカイブ作成後、アトミック移動
- プロセス中断時の自動クリーンアップ
- 破損/不完全なアーカイブのリスクなし
- クロスプラットフォーム互換性

```python
# デフォルトでアトミック操作有効
create_archive("important.tzst", files)  # 中断から安全

# 必要時に無効化可能 (非推奨)
create_archive("test.tzst", files, use_temp_file=False)
```

### 🚨 エラーハンドリング

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
    print("アーカイブの解凍に失敗しました")
except TzstFileNotFoundError:
    print("アーカイブファイルが見つかりません")
except KeyboardInterrupt:
    print("ユーザーにより操作中断")
    # クリーンアップは自動処理
```

## 🚀 パフォーマンスと比較

### 💡 パフォーマンスのヒント

1. **🗜️ 圧縮レベル**: ほとんどのユースケースでレベル 3 が最適
2. **🌊 ストリーミング**: 100 MB を超えるアーカイブで使用
3. **📦 バッチ操作**: 単一セッションで複数ファイル追加
4. **📄 ファイルタイプ**: 既に圧縮されたファイルはそれ以上圧縮されない

### 🆚 他のツールとの比較

**vs tar + gzip:**

- ✅ より高い圧縮率
- ⚡ 高速な解凍
- 🔄 モダンなアルゴリズム

**vs tar + xz:**

- 🚀 大幅に高速な圧縮
- 📊 同等の圧縮率
- ⚖️ 速度/圧縮率のトレードオフが優れる

**vs zip:**

- 🗜️ より高い圧縮率
- 🔐 Unix 権限とメタデータを保持
- 🌊 優れたストリーミングサポート

## 📋 要件

- 🐍 Python 3.12 以上
- 📦 zstandard >= 0.19.0

## 🛠️ 開発

### 🚀 開発環境セットアップ

このプロジェクトはモダンな Python パッケージング標準を使用:

```bash
git clone https://github.com/xixu-me/tzst.git
cd tzst
pip install -e .[dev]
```

### 🧪 テスト実行

```bash
# カバレッジ付きテスト実行
pytest --cov=tzst --cov-report=html

# またはシンプルなコマンド (カバレッジ設定は pyproject.toml 内)
pytest
```

### ✨ コード品質

```bash
# コード品質チェック
ruff check src tests

# コードフォーマット
ruff format src tests
```

## 🤝 貢献

貢献を歓迎します！以下の内容については[貢献ガイド](CONTRIBUTING.md)をお読みください:

- 開発セットアップとプロジェクト構造
- コードスタイルガイドラインとベストプラクティス  
- テスト要件とテスト作成
- プルリクエストプロセスとレビューワークフロー

### 🚀 貢献者向けクイックスタート

```bash
git clone https://github.com/xixu-me/tzst.git
cd tzst
pip install -e .[dev]
python -m pytest tests/
```

### 🎯 歓迎する貢献の種類

- 🐛 **バグ修正** - 既存機能の問題修正
- ✨ **機能** - ライブラリへの新機能追加
- 📚 **ドキュメント** - ドキュメントの改善・追加
- 🧪 **テスト** - テストカバレッジの追加・改善
- ⚡ **パフォーマンス** - 既存コードの最適化
- 🔒 **セキュリティ** - セキュリティ脆弱性への対応

## 🙏 謝辞

- [Meta Zstandard](https://github.com/facebook/zstd) - 優れた圧縮アルゴリズム
- [python-zstandard](https://github.com/indygreg/python-zstandard) - Python バインディング
- インスピレーションとフィードバックを提供した Python コミュニティ

## 📄 ライセンス

著作権 &copy; 2025 [Xi Xu](https://xi-xu.me)。全著作権を保留します。

[BSD 3-Clause](LICENSE) ライセンスのもとで公開されています。
