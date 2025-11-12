<h1 align="center">
<img src="https://raw.githubusercontent.com/xixu-me/tzst/refs/heads/main/docs/_static/tzst-logo.png" width="300">
</h1><br>

[![codecov](https://codecov.io/gh/xixu-me/tzst/graph/badge.svg?token=2AIN1559WU)](https://codecov.io/gh/xixu-me/tzst)
[![CodeQL](https://github.com/xixu-me/tzst/actions/workflows/github-code-scanning/codeql/badge.svg)](https://github.com/xixu-me/tzst/actions/workflows/github-code-scanning/codeql)
[![CI/CD](https://github.com/xixu-me/tzst/actions/workflows/ci.yml/badge.svg)](https://github.com/xixu-me/tzst/actions/workflows/ci.yml)
[![PyPI - Version](https://img.shields.io/pypi/v/tzst)](https://pypi.org/project/tzst/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/tzst)](https://pypistats.org/packages/tzst)
[![GitHub License](https://img.shields.io/github/license/xixu-me/tzst)](LICENSE)
[![Sponsor](https://img.shields.io/badge/Sponsor-violet)](https://xi-xu.me/#sponsorships)
[![Documentation](https://img.shields.io/badge/Documentation-blue)](https://tzst.xi-xu.me)

[🇺🇸 English](./README.md) | **🇨🇳 汉语** | [🇪🇸 español](./README.es.md) | [🇯🇵 日本語](./README.ja.md) | [🇦🇪 العربية](./README.ar.md) | [🇷🇺 русский](./README.ru.md) | [🇩🇪 Deutsch](./README.de.md) | [🇫🇷 français](./README.fr.md) | [🇰🇷 한국어](./README.ko.md) | [🇧🇷 português](./README.pt.md)

**tzst** 是一个面向现代归档管理的新一代 Python 库，利用前沿的 Zstandard 压缩技术，提供卓越的性能、安全性和可靠性。专为 Python 3.12+ 打造，这个企业级解决方案结合原子操作、流式处理效率和精心设计的 API，重新定义了开发者在生产环境中处理 `.tzst`/`.tar.zst` 归档文件的方式。🚀

技术深度解析文章已发布：**[《深入解析 tzst：一个基于 Zstandard 的现代 Python 归档库》](https://blog.xi-xu.me/2025/11/01/deep-dive-into-tzst.html)**。

## ✨ 功能特性

- **🗜️ 高效压缩**：采用 Zstandard 压缩算法，实现优异的压缩率和速度
- **📁 Tar 兼容性**：创建符合标准的 tar 归档并使用 Zstandard 压缩
- **💻 命令行界面**：直观的 CLI，支持流式处理和全面选项
- **🐍 Python API**：简洁、符合 Python 风格的编程接口
- **🌍 跨平台支持**：兼容 Windows、macOS 和 Linux
- **📂 多扩展名支持**：同时支持 `.tzst` 和 `.tar.zst` 扩展名
- **💾 内存高效**：流模式可高效处理大型归档文件
- **⚡ 原子操作**：安全的文件操作，中断时自动清理
- **🔒 默认安全**：提取时使用 'data' 过滤器确保最高安全性
- **🚨 增强的错误处理**：清晰的错误信息和实用建议

## 📥 安装指南

### 从 GitHub Releases 安装

下载无需 Python 环境的独立可执行文件：

#### 支持平台

| 平台 | 架构 | 文件 |
|------|------|------|
| **🐧 Linux** | x86_64 | `tzst-{版本}-linux-amd64.zip` |
| **🐧 Linux** | ARM64 | `tzst-{版本}-linux-arm64.zip` |
| **🪟 Windows** | x64 | `tzst-{版本}-windows-amd64.zip` |
| **🪟 Windows** | ARM64 | `tzst-{版本}-windows-arm64.zip` |
| **🍎 macOS** | Intel | `tzst-{版本}-darwin-amd64.zip` |
| **🍎 macOS** | Apple Silicon | `tzst-{版本}-darwin-arm64.zip` |

#### 🛠️ 安装步骤

1. **📥 下载**：从[最新发布页面](https://github.com/xixu-me/tzst/releases/latest)下载适合您平台的压缩包
2. **📦 解压**：解压获取 `tzst` 可执行文件（Windows 为 `tzst.exe`）
3. **📂 移动**：将可执行文件添加到 PATH 环境变量：
   - **🐧 Linux/macOS**：`sudo mv tzst /usr/local/bin/`
   - **🪟 Windows**：将包含 `tzst.exe` 的目录添加到 PATH
4. **✅ 验证**：运行 `tzst --help` 确认安装成功

#### 🎯 二进制安装优势

- ✅ **无需 Python** - 独立可执行文件
- ✅ **启动更快** - 无 Python 解释器开销
- ✅ **易于部署** - 单文件分发
- ✅ **行为一致** - 依赖项已打包

### 📦 通过 PyPI 安装

使用 pip：

```bash
pip install tzst
```

或使用 uv（推荐）：

```bash
uv tool install tzst
```

### 🔧 从源码安装

```bash
git clone https://github.com/xixu-me/tzst.git
cd tzst
pip install .
```

### 🚀 开发环境安装

```bash
git clone https://github.com/xixu-me/tzst.git
cd tzst
pip install -e .[dev]
```

## 🚀 快速开始

### 💻 命令行使用

```bash
# 📁 创建归档
tzst a archive.tzst file1.txt file2.txt directory/

# 📤 提取归档
tzst x archive.tzst

# 📋 列出归档内容
tzst l archive.tzst

# 🧪 测试归档完整性
tzst t archive.tzst
```

### 🐍 Python API 使用

```python
from tzst import create_archive, extract_archive, list_archive

# 创建归档
create_archive("archive.tzst", ["file1.txt", "file2.txt", "directory/"])

# 提取归档
extract_archive("archive.tzst", "output_dir/")

# 列出归档内容
contents = list_archive("archive.tzst", verbose=True)
for item in contents:
    print(f"{item['name']}: {item['size']} bytes")
```

## 💻 命令行接口

### 📁 归档操作

#### ➕ 创建归档

```bash
# 基本用法
tzst a archive.tzst file1.txt file2.txt

# 指定压缩级别 (1-22, 默认: 3)
tzst a archive.tzst files/ -l 15

# 等效命令
tzst add archive.tzst files/
tzst create archive.tzst files/
```

#### 📤 提取归档

```bash
# 完整目录结构提取
tzst x archive.tzst

# 提取到指定目录
tzst x archive.tzst -o output_dir/

# 提取特定文件
tzst x archive.tzst file1.txt dir/file2.txt

# 扁平化提取（无目录结构）
tzst e archive.tzst -o output_dir/

# 大文件使用流模式
tzst x archive.tzst --streaming -o output_dir/
```

#### 📋 列出内容

```bash
# 简单列表
tzst l archive.tzst

# 详细列表
tzst l archive.tzst -v

# 大文件使用流模式
tzst l archive.tzst --streaming -v
```

#### 🧪 测试完整性

```bash
# 测试归档完整性
tzst t archive.tzst

# 流模式测试
tzst t archive.tzst --streaming
```

### 📊 命令参考

| 命令 | 等效命令 | 描述 | 是否支持流模式 |
|------|----------|------|----------------|
| `a` | `add`, `create` | 创建或添加文件到归档 | 不支持 |
| `x` | `extract` | 完整路径提取 | ✓ `--streaming` |
| `e` | `extract-flat` | 扁平化提取 | ✓ `--streaming` |
| `l` | `list` | 列出归档内容 | ✓ `--streaming` |
| `t` | `test` | 测试归档完整性 | ✓ `--streaming` |

### ⚙️ CLI 选项

- `-v, --verbose`：启用详细输出
- `-o, --output DIR`：指定输出目录（提取命令）
- `-l, --level LEVEL`：设置压缩级别 1-22（创建命令）
- `--streaming`：启用流模式实现内存高效处理
- `--filter FILTER`：提取安全过滤器（data/tar/fully_trusted）
- `--no-atomic`：禁用原子文件操作（不推荐）

### 🔒 安全过滤器

```bash
# 最高安全性提取（默认）
tzst x archive.tzst --filter data

# 标准tar兼容性提取
tzst x archive.tzst --filter tar

# 完全信任模式（危险 - 仅适用于可信归档）
tzst x archive.tzst --filter fully_trusted
```

**🔐 安全过滤器选项：**

- `data` (默认)：最安全。阻止危险文件、绝对路径和提取目录外路径
- `tar`：标准 tar 兼容性。阻止绝对路径和目录遍历
- `fully_trusted`：无安全限制。仅适用于完全可信的归档

## 🐍 Python API

### 📦 TzstArchive 类

```python
from tzst import TzstArchive

# 创建新归档
with TzstArchive("archive.tzst", "w", compression_level=5) as archive:
    archive.add("file.txt")
    archive.add("directory/", recursive=True)

# 读取现有归档
with TzstArchive("archive.tzst", "r") as archive:
    # 列出内容
    contents = archive.list(verbose=True)
    
    # 安全提取
    archive.extract("file.txt", "output/", filter="data")
    
    # 测试完整性
    is_valid = archive.test()

# 大文件使用流模式
with TzstArchive("large_archive.tzst", "r", streaming=True) as archive:
    archive.extract(path="output/")
```

**⚠️ 重要限制：**

- **❌ 不支持追加模式**：需创建新归档或重建整个归档

### 🎯 便捷函数

#### 📁 create_archive()

```python
from tzst import create_archive

# 原子操作创建（默认）
create_archive(
    archive_path="backup.tzst",
    files=["documents/", "photos/", "config.txt"],
    compression_level=10
)
```

#### 📤 extract_archive()

```python
from tzst import extract_archive

# 安全提取（默认：'data'过滤器）
extract_archive("backup.tzst", "restore_dir/")

# 提取特定文件
extract_archive("backup.tzst", "restore_dir/", members=["config.txt"])

# 扁平化提取
extract_archive("backup.tzst", "restore_dir/", flatten=True)

# 大文件使用流模式
extract_archive("large_backup.tzst", "restore_dir/", streaming=True)
```

#### 📋 list_archive()

```python
from tzst import list_archive

# 简单列表
file_list = list_archive("backup.tzst")

# 详细列表
file_details = list_archive("backup.tzst", verbose=True)

# 大文件使用流模式
large_list = list_archive("large_backup.tzst", streaming=True)
```

#### 🧪 test_archive()

```python
from tzst import test_archive

# 基本完整性测试
if test_archive("backup.tzst"):
    print("Archive is valid")

# 流模式测试
if test_archive("large_backup.tzst", streaming=True):
    print("Large archive is valid")
```

## 🔧 高级功能

### 📂 文件扩展名

库自动处理文件扩展名并智能标准化：

- `.tzst` - tar + zstandard 归档主扩展名
- `.tar.zst` - 替代标准扩展名
- 打开现有归档时自动检测
- 创建归档时自动添加扩展名

```python
# 以下创建方式均有效
create_archive("backup.tzst", files)      # 创建 backup.tzst
create_archive("backup.tar.zst", files)  # 创建 backup.tar.zst  
create_archive("backup", files)          # 创建 backup.tzst
create_archive("backup.txt", files)      # 创建 backup.tzst (标准化)
```

### 🗜️ 压缩级别

Zstandard 压缩级别范围从 1（最快）到 22（最佳压缩）：

- **级别 1-3**：快速压缩，文件较大
- **级别 3**（默认）：速度与压缩率的良好平衡
- **级别 10-15**：更好的压缩率，速度较慢
- **级别 20-22**：最高压缩率，速度显著变慢

### 🌊 流模式

使用流模式实现大归档文件的内存高效处理：

**✅ 优势：**

- 显著降低内存使用
- 对内存无法容纳的大文件性能更好
- 资源自动清理

**🎯 适用场景：**

- 大于 100MB 的归档文件
- 内存有限的环境
- 处理包含多个大文件的归档

```python
# 示例：处理大型备份归档
from tzst import extract_archive, list_archive, test_archive

large_archive = "backup_500gb.tzst"

# 内存高效操作
is_valid = test_archive(large_archive, streaming=True)
contents = list_archive(large_archive, streaming=True, verbose=True)
extract_archive(large_archive, "restore_dir/", streaming=True)
```

### ⚡ 原子操作

所有文件创建操作默认使用原子操作：

- 归档先在临时文件创建，然后原子移动
- 进程中断时自动清理
- 无损坏或不完整归档风险
- 跨平台兼容

```python
# 默认启用原子操作
create_archive("important.tzst", files)  # 中断时安全

# 可禁用（不推荐）
create_archive("test.tzst", files, use_temp_file=False)
```

### 🚨 错误处理

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
    print("Failed to decompress archive")
except TzstFileNotFoundError:
    print("Archive file not found")
except KeyboardInterrupt:
    print("Operation interrupted by user")
    # Cleanup handled automatically
```

## 🚀 性能与对比

### 💡 性能优化建议

1. **🗜️ 压缩级别**：级别 3 适用于大多数场景
2. **🌊 流模式**：归档大于 100MB 时使用
3. **📦 批量操作**：单次会话添加多个文件
4. **📄 文件类型**：已压缩文件不会进一步压缩

### 🆚 与其他工具对比

**对比 tar + gzip：**

- ✅ 更好的压缩率
- ⚡ 更快的解压速度
- 🔄 现代算法

**对比 tar + xz：**

- 🚀 显著更快的压缩速度
- 📊 相似的压缩率
- ⚖️ 更好的速度/压缩率平衡

**对比 zip：**

- 🗜️ 更好的压缩率
- 🔐 保留 Unix 权限和元数据
- 🌊 更好的流处理支持

## 📋 系统要求

- 🐍 Python 3.12 或更高版本
- 📦 zstandard >= 0.19.0

## 🛠️ 开发指南

### 🚀 设置开发环境

```bash
git clone https://github.com/xixu-me/tzst.git
cd tzst
pip install -e .[dev]
```

### 🧪 运行测试

```bash
# 带覆盖率的测试
pytest --cov=tzst --cov-report=html

# 简化命令 (覆盖配置在 pyproject.toml)
pytest
```

### ✨ 代码质量

```bash
# 代码检查
ruff check src tests

# 代码格式化
ruff format src tests
```

## 🤝 贡献指南

欢迎贡献！请阅读[贡献指南](CONTRIBUTING.md)了解：

- 开发设置和项目结构
- 代码风格指南和最佳实践
- 测试要求和编写测试
- PR流程和审核规范

### 🚀 贡献者快速入门

```bash
git clone https://github.com/xixu-me/tzst.git
cd tzst
pip install -e .[dev]
python -m pytest tests/
```

### 🎯 欢迎贡献类型

- 🐛 **缺陷修复** - 修复现有功能问题
- ✨ **新功能** - 扩展库的功能
- 📚 **文档** - 改进或新增文档
- 🧪 **测试** - 增加或改进测试覆盖
- ⚡ **性能** - 优化现有代码
- 🔒 **安全** - 修复安全漏洞

## 🙏 致谢

- [Meta Zstandard](https://github.com/facebook/zstd) 提供的优秀压缩算法
- [python-zstandard](https://github.com/indygreg/python-zstandard) 的 Python 绑定
- Python 社区的宝贵反馈和启发

## 📄 许可证

版权所有 &copy; 2025 [Xi Xu](https://xi-xu.me)。保留所有权利。

采用 [BSD 3-Clause](LICENSE) 许可证授权。
