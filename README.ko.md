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

[🇺🇸 English](./README.md) | [🇨🇳 汉语](./README.zh.md) | [🇪🇸 español](./README.es.md) | [🇯🇵 日本語](./README.ja.md) | [🇦🇪 العربية](./README.ar.md) | [🇷🇺 русский](./README.ru.md) | [🇩🇪 Deutsch](./README.de.md) | [🇫🇷 français](./README.fr.md) | **🇰🇷 한국어** | [🇧🇷 português](./README.pt.md)

**tzst**는 최신 Zstandard 압축 기술을 활용하여 우수한 성능, 보안 및 신뢰성을 제공하는 차세대 Python 라이브러리입니다. Python 3.12+ 전용으로 제작된 이 엔터프라이즈급 솔루션은 원자적 작업, 스트리밍 효율성 및 정교하게 설계된 API를 결합하여 `.tzst`/`.tar.zst` 아카이브를 프로덕션 환경에서 처리하는 방식을 재정의합니다. 🚀

심층 기술 분석 기사가 게시되었습니다: **[Deep Dive into tzst: A Modern Python Archiving Library Based on Zstandard](https://blog.xi-xu.me/2025/11/01/deep-dive-into-tzst-en.html)**.

## ✨ 기능

- **🗜️ 고압축률**: 우수한 압축률과 속도를 위한 Zstandard 압축
- **📁 Tar 호환성**: Zstandard로 압축된 표준 tar 아카이브 생성
- **💻 명령줄 인터페이스**: 스트리밍 지원과 포괄적인 옵션을 갖춘 직관적인 CLI
- **🐍 Python API**: 프로그램적 사용을 위한 깔끔하고 Python 스타일의 API
- **🌍 크로스 플랫폼**: Windows, macOS, Linux에서 작동
- **📂 다중 확장자**: `.tzst` 및 `.tar.zst` 확장자 모두 지원
- **💾 메모리 효율적**: 최소 메모리 사용으로 대용량 아카이브 처리 가능한 스트리밍 모드
- **⚡ 원자적 작업**: 중단 시 자동 정리 기능을 통한 안전한 파일 작업
- **🔒 기본 보안**: 추출 시 최대 보안을 위해 'data' 필터 사용
- **🚨 향상된 오류 처리**: 유용한 대안 제시와 함께 명확한 오류 메시지

## 📥 설치

### GitHub 릴리스에서

Python 설치가 필요 없는 독립형 실행 파일 다운로드:

#### 지원 플랫폼

| 플랫폼 | 아키텍처 | 파일 |
|----------|-------------|------|
| **🐧 Linux** | x86_64 | `tzst-{버전}-linux-amd64.zip` |
| **🐧 Linux** | ARM64 | `tzst-{버전}-linux-arm64.zip` |
| **🪟 Windows** | x64 | `tzst-{버전}-windows-amd64.zip` |
| **🪟 Windows** | ARM64 | `tzst-{버전}-windows-arm64.zip` |
| **🍎 macOS** | Intel | `tzst-{버전}-darwin-amd64.zip` |
| **🍎 macOS** | Apple Silicon | `tzst-{버전}-darwin-arm64.zip` |

#### 🛠️ 설치 단계

1. [최신 릴리스 페이지](https://github.com/xixu-me/tzst/releases/latest)에서 플랫폼에 맞는 아카이브 **📥 다운로드**
2. 아카이브를 **📦 추출**하여 `tzst` 실행 파일 획득 (Windows는 `tzst.exe`)
3. 실행 파일을 PATH 환경 변수 디렉터리로 **📂 이동**:
   - **🐧 Linux/macOS**: `sudo mv tzst /usr/local/bin/`
   - **🪟 Windows**: `tzst.exe`가 포함된 디렉터리를 PATH 환경 변수에 추가
4. 설치 **✅ 확인**: `tzst --help`

#### 🎯 바이너리 설치의 장점

- ✅ **Python 불필요** - 독립형 실행 파일
- ✅ **빠른 시작** - Python 인터프리터 오버헤드 없음
- ✅ **쉬운 배포** - 단일 파일 배포
- ✅ **일관된 동작** - 번들링된 의존성

### 📦 PyPI에서

pip 사용:

```bash
pip install tzst
```

또는 uv 사용 (권장):

```bash
uv tool install tzst
```

### 🔧 소스에서

```bash
git clone https://github.com/xixu-me/tzst.git
cd tzst
pip install .
```

### 🚀 개발 설치

최신 Python 패키징 표준 사용:

```bash
git clone https://github.com/xixu-me/tzst.git
cd tzst
pip install -e .[dev]
```

## 🚀 빠른 시작

### 💻 명령줄 사용법

```bash
# 📁 아카이브 생성
tzst a archive.tzst file1.txt file2.txt directory/

# 📤 아카이브 추출
tzst x archive.tzst

# 📋 아카이브 내용 목록
tzst l archive.tzst

# 🧪 아카이브 무결성 테스트
tzst t archive.tzst
```

### 🐍 Python API 사용법

```python
from tzst import create_archive, extract_archive, list_archive

# 아카이브 생성
create_archive("archive.tzst", ["file1.txt", "file2.txt", "directory/"])

# 아카이브 추출
extract_archive("archive.tzst", "output_directory/")

# 아카이브 내용 목록
contents = list_archive("archive.tzst", verbose=True)
for item in contents:
    print(f"{item['name']}: {item['size']} bytes")
```

## 💻 명령줄 인터페이스

### 📁 아카이브 작업

#### ➕ 아카이브 생성

```bash
# 기본 사용법
tzst a archive.tzst file1.txt file2.txt

# 압축 레벨 지정 (1-22, 기본값: 3)
tzst a archive.tzst files/ -l 15

# 대체 명령어
tzst add archive.tzst files/
tzst create archive.tzst files/
```

#### 📤 아카이브 추출

```bash
# 전체 디렉터리 구조 유지하며 추출
tzst x archive.tzst

# 특정 디렉터리로 추출
tzst x archive.tzst -o output/

# 특정 파일 추출
tzst x archive.tzst file1.txt dir/file2.txt

# 디렉터리 구조 없이 추출 (플랫)
tzst e archive.tzst -o output/

# 대용량 아카이브에 스트리밍 모드 사용
tzst x archive.tzst --streaming -o output/
```

#### 📋 내용 목록

```bash
# 간단한 목록
tzst l archive.tzst

# 상세 정보 포함 목록
tzst l archive.tzst -v

# 대용량 아카이브에 스트리밍 모드 사용
tzst l archive.tzst --streaming -v
```

#### 🧪 무결성 테스트

```bash
# 아카이브 무결성 테스트
tzst t archive.tzst

# 스트리밍 모드로 테스트
tzst t archive.tzst --streaming
```

### 📊 명령어 참조

| 명령어 | 별칭 | 설명 | 스트리밍 지원 |
|---------|---------|-------------|-------------------|
| `a` | `add`, `create` | 아카이브 생성 또는 추가 | N/A |
| `x` | `extract` | 전체 경로로 추출 | ✓ `--streaming` |
| `e` | `extract-flat` | 디렉터리 구조 없이 추출 | ✓ `--streaming` |
| `l` | `list` | 아카이브 내용 목록 | ✓ `--streaming` |
| `t` | `test` | 아카이브 무결성 테스트 | ✓ `--streaming` |

### ⚙️ CLI 옵션

- `-v, --verbose`: 상세 출력 활성화
- `-o, --output DIR`: 출력 디렉터리 지정 (추출 명령어)
- `-l, --level LEVEL`: 압축 레벨 1-22 설정 (생성 명령어)
- `--streaming`: 메모리 효율적 처리를 위한 스트리밍 모드 활성화
- `--filter FILTER`: 추출을 위한 보안 필터 (data/tar/fully_trusted)
- `--no-atomic`: 원자적 파일 작업 비활성화 (권장하지 않음)

### 🔒 보안 필터

```bash
# 최대 보안으로 추출 (기본값)
tzst x archive.tzst --filter data

# 표준 tar 호환성으로 추출
tzst x archive.tzst --filter tar

# 완전 신뢰 모드로 추출 (위험 - 신뢰할 수 있는 아카이브 전용)
tzst x archive.tzst --filter fully_trusted
```

**🔐 보안 필터 옵션:**

- `data` (기본값): 가장 안전. 위험한 파일, 절대 경로, 추출 디렉터리 외부 경로 차단
- `tar`: 표준 tar 호환성. 절대 경로 및 디렉터리 순회 차단
- `fully_trusted`: 보안 제한 없음. 완전히 신뢰할 수 있는 아카이브에서만 사용

## 🐍 Python API

### 📦 TzstArchive 클래스

```python
from tzst import TzstArchive

# 새 아카이브 생성
with TzstArchive("archive.tzst", "w", compression_level=5) as archive:
    archive.add("file.txt")
    archive.add("directory/", recursive=True)

# 기존 아카이브 읽기
with TzstArchive("archive.tzst", "r") as archive:
    # 내용 목록
    contents = archive.list(verbose=True)
    
    # 보안 필터 적용 추출
    archive.extract("file.txt", "output/", filter="data")
    
    # 무결성 테스트
    is_valid = archive.test()

# 대용량 아카이브에 스트리밍 모드 사용
with TzstArchive("large_archive.tzst", "r", streaming=True) as archive:
    archive.extract(path="output/")
```

**⚠️ 중요한 제한 사항:**

- **❌ 추가 모드 미지원**: 여러 아카이브 생성 또는 전체 아카이브 재생성 필요

### 🎯 편의 함수

#### 📁 create_archive()

```python
from tzst import create_archive

# 원자적 작업으로 생성 (기본값)
create_archive(
    archive_path="backup.tzst",
    files=["documents/", "photos/", "config.txt"],
    compression_level=10
)
```

#### 📤 extract_archive()

```python
from tzst import extract_archive

# 보안 추출 (기본값: 'data' 필터)
extract_archive("backup.tzst", "restore/")

# 특정 파일 추출
extract_archive("backup.tzst", "restore/", members=["config.txt"])

# 디렉터리 구조 평탄화
extract_archive("backup.tzst", "restore/", flatten=True)

# 대용량 아카이브에 스트리밍 사용
extract_archive("large_backup.tzst", "restore/", streaming=True)
```

#### 📋 list_archive()

```python
from tzst import list_archive

# 간단한 목록
files = list_archive("backup.tzst")

# 상세 목록
files = list_archive("backup.tzst", verbose=True)

# 대용량 아카이브에 스트리밍 사용
files = list_archive("large_backup.tzst", streaming=True)
```

#### 🧪 test_archive()

```python
from tzst import test_archive

# 기본 무결성 테스트
if test_archive("backup.tzst"):
    print("아카이브가 유효합니다")

# 스트리밍으로 테스트
if test_archive("large_backup.tzst", streaming=True):
    print("대용량 아카이브가 유효합니다")
```

## 🔧 고급 기능

### 📂 파일 확장자

라이브러리는 지능적인 정규화로 파일 확장자를 자동 처리합니다:

- `.tzst` - tar+zstandard 아카이브의 기본 확장자
- `.tar.zst` - 대체 표준 확장자
- 기존 아카이브 열 때 자동 감지
- 아카이브 생성 시 자동 확장자 추가

```python
# 모두 유효한 아카이브 생성
create_archive("backup.tzst", files)      # backup.tzst 생성
create_archive("backup.tar.zst", files)  # backup.tar.zst 생성  
create_archive("backup", files)          # backup.tzst 생성
create_archive("backup.txt", files)      # backup.tzst 생성 (정규화됨)
```

### 🗜️ 압축 레벨

Zstandard 압축 레벨 범위: 1 (가장 빠름) ~ 22 (최대 압축):

- **레벨 1-3**: 빠른 압축, 파일 크기 큼
- **레벨 3** (기본값): 속도와 압축률의 균형
- **레벨 10-15**: 더 나은 압축, 느림
- **레벨 20-22**: 최대 압축, 매우 느림

### 🌊 스트리밍 모드

대용량 아카이브의 메모리 효율적 처리를 위해 스트리밍 모드 사용:

**✅ 장점:**

- 메모리 사용량 현저히 감소
- 메모리에 맞지 않는 대용량 아카이브 처리 성능 향상
- 리소스 자동 정리

**🎯 사용 시기:**

- 100MB 이상의 아카이브
- 메모리가 제한된 환경
- 대용량 파일이 많은 아카이브 처리

```python
# 예제: 대용량 백업 아카이브 처리
from tzst import extract_archive, list_archive, test_archive

large_archive = "backup_500gb.tzst"

# 메모리 효율적 작업
is_valid = test_archive(large_archive, streaming=True)
contents = list_archive(large_archive, streaming=True, verbose=True)
extract_archive(large_archive, "restore/", streaming=True)
```

### ⚡ 원자적 작업

모든 파일 생성 작업은 기본적으로 원자적 파일 작업을 사용합니다:

- 임시 파일에 먼저 생성 후 원자적 이동
- 프로세스 중단 시 자동 정리
- 손상되거나 불완전한 아카이브 위험 없음
- 크로스 플랫폼 호환성

```python
# 기본적으로 원자적 작업 활성화
create_archive("important.tzst", files)  # 중단으로부터 안전

# 필요한 경우 비활성화 가능 (권장하지 않음)
create_archive("test.tzst", files, use_temp_file=False)
```

### 🚨 오류 처리

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
    print("아카이브 압축 해제 실패")
except TzstFileNotFoundError:
    print("아카이브 파일을 찾을 수 없음")
except KeyboardInterrupt:
    print("사용자에 의해 작업 중단됨")
    # 자동으로 정리됨
```

## 🚀 성능 및 비교

### 💡 성능 팁

1. **🗜️ 압축 레벨**: 대부분의 경우 레벨 3이 최적
2. **🌊 스트리밍**: 100MB 이상 아카이브에 사용
3. **📦 일괄 작업**: 단일 세션에서 여러 파일 추가
4. **📄 파일 유형**: 이미 압축된 파일은 추가 압축이 거의 안됨

### 🆚 다른 도구와 비교

**vs tar + gzip:**

- ✅ 더 나은 압축률
- ⚡ 더 빠른 압축 해제
- 🔄 현대적인 알고리즘

**vs tar + xz:**

- 🚀 현저히 빠른 압축
- 📊 유사한 압축률
- ⚖️ 더 나은 속도/압축률 균형

**vs zip:**

- 🗜️ 더 나은 압축
- 🔐 Unix 권한 및 메타데이터 보존
- 🌊 더 나은 스트리밍 지원

## 📋 요구 사항

- 🐍 Python 3.12 이상
- 📦 zstandard >= 0.19.0

## 🛠️ 개발

### 🚀 개발 환경 설정

최신 Python 패키징 표준 사용:

```bash
git clone https://github.com/xixu-me/tzst.git
cd tzst
pip install -e .[dev]
```

### 🧪 테스트 실행

```bash
# 커버리지 포함 테스트 실행
pytest --cov=tzst --cov-report=html

# 또는 간단한 명령어 사용 (커버리지 설정은 pyproject.toml에 있음)
pytest
```

### ✨ 코드 품질

```bash
# 코드 품질 확인
ruff check src tests

# 코드 포맷팅
ruff format src tests
```

## 🤝 기여

기여를 환영합니다! 다음 사항을 위해 [기여 가이드](CONTRIBUTING.md)를 읽어주세요:

- 개발 설정 및 프로젝트 구조
- 코드 스타일 가이드라인 및 모범 사례  
- 테스트 요구 사항 및 테스트 작성 방법
- 풀 리퀘스트 프로세스 및 리뷰 워크플로

### 🚀 기여자 빠른 시작

```bash
git clone https://github.com/xixu-me/tzst.git
cd tzst
pip install -e .[dev]
python -m pytest tests/
```

### 🎯 환영하는 기여 유형

- 🐛 **버그 수정** - 기존 기능의 문제 해결
- ✨ **기능** - 라이브러리에 새로운 기능 추가
- 📚 **문서** - 문서 개선 또는 추가
- 🧪 **테스트** - 테스트 커버리지 추가 또는 개선
- ⚡ **성능** - 기존 코드 최적화
- 🔒 **보안** - 보안 취약점 해결

## 🙏 감사의 말

- 우수한 압축 알고리즘을 제공한 [Meta Zstandard](https://github.com/facebook/zstd)
- Python 바인딩을 제공한 [python-zstandard](https://github.com/indygreg/python-zstandard)
- 영감과 피드백을 준 Python 커뮤니티

## 📄 라이선스

저작권 &copy; [시 쉬](https://xi-xu.me). 모든 권리 보유.

[BSD 3-Clause](LICENSE) 라이선스로 사용이 허가되었습니다.
