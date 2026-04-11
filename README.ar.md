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

[🇺🇸 English](./README.md) | [🇨🇳 汉语](./README.zh.md) | [🇪🇸 español](./README.es.md) | [🇯🇵 日本語](./README.ja.md) | **🇦🇪 العربية** | [🇷🇺 русский](./README.ru.md) | [🇩🇪 Deutsch](./README.de.md) | [🇫🇷 français](./README.fr.md) | [🇰🇷 한국어](./README.ko.md) | [🇧🇷 português](./README.pt.md)

<div dir="rtl" lang="ar">

**tzst** هي مكتبة وأداة سطر أوامر لـ Python 3.12+ لإنشاء أرشيفات `.tzst` و`.tar.zst` واستخراجها وعرض محتوياتها والتحقق منها. تجمع بين توافق tar وضغط Zstandard ووضع التدفق والكتابة الذرية والاستخراج الآمن افتراضياً ضمن واجهة موجزة جاهزة للاستخدام الإنتاجي.

> [!NOTE]
> مقال تقني مفصل: **[Deep Dive into tzst: A Modern Python Archiving Library Based on Zstandard](https://blog.xi-xu.me/2025/11/01/deep-dive-into-tzst-en.html)**.

## الميزات

- **ضغط عالي**: ضغط Zstandard لنسب ضغط وسرعة ممتازة
- **توافق Tar**: ينشئ أرشيف tar قياسي مضغوط بـ Zstandard
- **واجهة سطر الأوامر**: واجهة CLI بديهية مع دعم التدفق وخيارات شاملة
- **Python API**: واجهة برمجة تطبيقات نظيفة وpythonic للاستخدام البرمجي
- **متعدد المنصات**: يعمل على Windows وmacOS وLinux
- **امتدادات متعددة**: يدعم كلاً من امتدادات `.tzst` و `.tar.zst`
- **فعال في الذاكرة**: وضع التدفق للتعامل مع الأرشيف الكبير باستخدام أقل للذاكرة
- **عمليات ذرية**: عمليات ملف آمنة مع تنظيف تلقائي عند المقاطعة
- **آمن افتراضياً**: يستخدم مرشح 'data' للحد الأقصى من الأمان أثناء الاستخراج
- **معالجة أخطاء محسنة**: رسائل خطأ واضحة مع بدائل مفيدة

## التثبيت

### من إصدارات GitHub

تحميل ملفات تنفيذية مستقلة لا تتطلب تثبيت Python:

#### المنصات المدعومة

| المنصة | المعمارية | الملف |
|----------|-------------|------|
| **Linux** | x86_64 | `tzst-{version}-linux-amd64.zip` |
| **Linux** | ARM64 | `tzst-{version}-linux-arm64.zip` |
| **Windows** | x64 | `tzst-{version}-windows-amd64.zip` |
| **Windows** | ARM64 | `tzst-{version}-windows-arm64.zip` |
| **macOS** | Intel | `tzst-{version}-darwin-amd64.zip` |
| **macOS** | Apple Silicon | `tzst-{version}-darwin-arm64.zip` |

#### خطوات التثبيت

1. **تحميل** الأرشيف المناسب لمنصتك من [صفحة الإصدارات الأحدث](https://github.com/xixu-me/tzst/releases/latest)
2. **استخراج** الأرشيف للحصول على الملف التنفيذي `tzst` (أو `tzst.exe` على Windows)
3. **نقل** الملف التنفيذي إلى مجلد في PATH الخاص بك:
   - **Linux/macOS**: `sudo mv tzst /usr/local/bin/`
   - **Windows**: أضف المجلد الذي يحتوي على `tzst.exe` إلى متغير البيئة PATH
4. **تحقق** من التثبيت: `tzst --help`

#### فوائد التثبيت الثنائي

- **لا يتطلب Python** - ملف تنفيذي مستقل
- **بدء تشغيل أسرع** - بدون إضافة مفسر Python
- **نشر سهل** - توزيع ملف واحد
- **سلوك متسق** - تبعيات مجمعة

### من PyPI

استخدام pip:

```bash
pip install tzst
```

أو استخدام uv (موصى به):

```bash
uv tool install tzst
```

### من المصدر

```bash
git clone https://github.com/xixu-me/tzst.git
cd tzst
pip install .
```

### تثبيت التطوير

يستخدم هذا المشروع معايير تعبئة Python الحديثة:

```bash
git clone https://github.com/xixu-me/tzst.git
cd tzst
pip install -e .[dev]
```

## البداية السريعة

### استخدام سطر الأوامر

```bash
# إنشاء أرشيف
tzst a archive.tzst file1.txt file2.txt directory/

# استخراج أرشيف
tzst x archive.tzst

# قائمة محتويات الأرشيف
tzst l archive.tzst

# اختبار سلامة الأرشيف
tzst t archive.tzst
```

### استخدام Python API

```python
from tzst import create_archive, extract_archive, list_archive

# إنشاء أرشيف
create_archive("archive.tzst", ["file1.txt", "file2.txt", "directory/"])

# استخراج أرشيف
extract_archive("archive.tzst", "output_directory/")

# قائمة محتويات الأرشيف
contents = list_archive("archive.tzst", verbose=True)
for item in contents:
    print(f"{item['name']}: {item['size']} bytes")
```

## واجهة سطر الأوامر

### عمليات الأرشيف

#### إنشاء أرشيف

```bash
# الاستخدام الأساسي
tzst a archive.tzst file1.txt file2.txt

# مع مستوى الضغط (1-22، افتراضي: 3)
tzst a archive.tzst files/ -l 15

# أوامر بديلة
tzst add archive.tzst files/
tzst create archive.tzst files/
```

#### استخراج أرشيف

```bash
# استخراج مع هيكل المجلد الكامل
tzst x archive.tzst

# استخراج إلى مجلد محدد
tzst x archive.tzst -o output/

# استخراج ملفات محددة
tzst x archive.tzst file1.txt dir/file2.txt

# استخراج بدون هيكل المجلد (مسطح)
tzst e archive.tzst -o output/

# استخدام وضع التدفق للأرشيف الكبير
tzst x archive.tzst --streaming -o output/
```

#### قائمة المحتويات

```bash
# قائمة بسيطة
tzst l archive.tzst

# قائمة مفصلة مع التفاصيل
tzst l archive.tzst -v

# استخدام وضع التدفق للأرشيف الكبير
tzst l archive.tzst --streaming -v
```

#### اختبار السلامة

```bash
# اختبار سلامة الأرشيف
tzst t archive.tzst

# اختبار مع وضع التدفق
tzst t archive.tzst --streaming
```

### مرجع الأوامر

| الأمر | البدائل | الوصف | دعم التدفق |
|---------|---------|-------------|-------------------|
| `a` | `add`, `create` | إنشاء أو إضافة إلى أرشيف | N/A |
| `x` | `extract` | استخراج مع المسارات الكاملة | ✓ `--streaming` |
| `e` | `extract-flat` | استخراج بدون هيكل المجلد | ✓ `--streaming` |
| `l` | `list` | قائمة محتويات الأرشيف | ✓ `--streaming` |
| `t` | `test` | اختبار سلامة الأرشيف | ✓ `--streaming` |

### خيارات CLI

- `-v, --verbose`: تمكين الإخراج المفصل
- `-o, --output DIR`: تحديد مجلد الإخراج (أوامر الاستخراج)
- `-l, --level LEVEL`: تحديد مستوى الضغط 1-22 (أمر الإنشاء)
- `--streaming`: تمكين وضع التدفق للمعالجة الفعالة في الذاكرة
- `--filter FILTER`: مرشح الأمان للاستخراج (data/tar/fully_trusted)
- `--no-atomic`: تعطيل العمليات الذرية للملفات (غير مستحسن)

### مرشحات الأمان

```bash
# استخراج مع أقصى أمان (افتراضي)
tzst x archive.tzst --filter data

# استخراج مع توافق tar قياسي
tzst x archive.tzst --filter tar

# استخراج مع ثقة كاملة (خطر - فقط للأرشيف الموثوق)
tzst x archive.tzst --filter fully_trusted
```

**خيارات مرشح الأمان:**

- `data` (افتراضي): الأكثر أماناً. يحجب الملفات الخطيرة والمسارات المطلقة والمسارات خارج مجلد الاستخراج
- `tar`: توافق tar قياسي. يحجب المسارات المطلقة واجتياز المجلد
- `fully_trusted`: لا قيود أمان. استخدم فقط مع الأرشيف الموثوق تماماً

## Python API

### فئة TzstArchive

```python
from tzst import TzstArchive

# إنشاء أرشيف جديد
with TzstArchive("archive.tzst", "w", compression_level=5) as archive:
    archive.add("file.txt")
    archive.add("directory/", recursive=True)

# قراءة أرشيف موجود
with TzstArchive("archive.tzst", "r") as archive:
    # قائمة المحتويات
    contents = archive.list(verbose=True)
    
    # استخراج مع مرشح الأمان
    archive.extract("file.txt", "output/", filter="data")
    
    # اختبار السلامة
    is_valid = archive.test()

# للأرشيف الكبير، استخدم وضع التدفق
with TzstArchive("large_archive.tzst", "r", streaming=True) as archive:
    archive.extract(path="output/")
```

**قيود مهمة:**

- **وضع الإلحاق غير مدعوم**: أنشئ أرشيف متعدد أو أعد إنشاء الأرشيف بالكامل بدلاً من ذلك

### دوال الراحة

#### create_archive()

```python
from tzst import create_archive

# إنشاء مع عمليات ذرية (افتراضي)
create_archive(
    archive_path="backup.tzst",
    files=["documents/", "photos/", "config.txt"],
    compression_level=10
)
```

#### extract_archive()

```python
from tzst import extract_archive

# استخراج مع الأمان (افتراضي: مرشح 'data')
extract_archive("backup.tzst", "restore/")

# استخراج ملفات محددة
extract_archive("backup.tzst", "restore/", members=["config.txt"])

# تسطيح هيكل المجلد
extract_archive("backup.tzst", "restore/", flatten=True)

# استخدام التدفق للأرشيف الكبير
extract_archive("large_backup.tzst", "restore/", streaming=True)
```

#### list_archive()

```python
from tzst import list_archive

# قائمة بسيطة
files = list_archive("backup.tzst")

# قائمة مفصلة
files = list_archive("backup.tzst", verbose=True)

# تدفق للأرشيف الكبير
files = list_archive("large_backup.tzst", streaming=True)
```

#### test_archive()

```python
from tzst import test_archive

# اختبار سلامة أساسي
if test_archive("backup.tzst"):
    print("الأرشيف صالح")

# اختبار مع التدفق
if test_archive("large_backup.tzst", streaming=True):
    print("الأرشيف الكبير صالح")
```

## الميزات المتقدمة

### امتدادات الملفات

تتعامل المكتبة تلقائياً مع امتدادات الملفات مع التطبيع الذكي:

- `.tzst` - الامتداد الأساسي لأرشيف tar+zstandard
- `.tar.zst` - امتداد قياسي بديل
- الكشف التلقائي عند فتح الأرشيف الموجود
- إضافة الامتداد التلقائي عند إنشاء الأرشيف

```python
# هذه كلها تنشئ أرشيف صالح
create_archive("backup.tzst", files)      # ينشئ backup.tzst
create_archive("backup.tar.zst", files)  # ينشئ backup.tar.zst  
create_archive("backup", files)          # ينشئ backup.tzst
create_archive("backup.txt", files)      # ينشئ backup.tzst (مُطبع)
```

### مستويات الضغط

تتراوح مستويات ضغط Zstandard من 1 (الأسرع) إلى 22 (أفضل ضغط):

- **المستوى 1-3**: ضغط سريع، ملفات أكبر
- **المستوى 3** (افتراضي): توازن جيد بين السرعة والضغط
- **المستوى 10-15**: ضغط أفضل، أبطأ
- **المستوى 20-22**: أقصى ضغط، أبطأ بكثير

### وضع التدفق

استخدم وضع التدفق للمعالجة الفعالة في الذاكرة للأرشيف الكبير:

**الفوائد:**

- انخفاض كبير في استخدام الذاكرة
- أداء أفضل للأرشيف الذي لا يناسب الذاكرة
- تنظيف تلقائي للموارد

**متى تستخدم:**

- أرشيف أكبر من 100 ميجابايت
- بيئات ذاكرة محدودة
- معالجة أرشيف بملفات كبيرة كثيرة

```python
# مثال: معالجة أرشيف نسخ احتياطي كبير
from tzst import extract_archive, list_archive, test_archive

large_archive = "backup_500gb.tzst"

# عمليات فعالة في الذاكرة
is_valid = test_archive(large_archive, streaming=True)
contents = list_archive(large_archive, streaming=True, verbose=True)
extract_archive(large_archive, "restore/", streaming=True)
```

### العمليات الذرية

جميع عمليات إنشاء الملفات تستخدم عمليات ملف ذرية افتراضياً:

- الأرشيف منشأ في ملفات مؤقتة أولاً، ثم نُقل ذرياً
- تنظيف تلقائي إذا تمت مقاطعة العملية
- لا خطر من أرشيف تالف أو غير مكتمل
- توافق متعدد المنصات

```python
# العمليات الذرية ممكنة افتراضياً
create_archive("important.tzst", files)  # آمن من المقاطعة

# يمكن تعطيلها إذا لزم الأمر (غير مستحسن)
create_archive("test.tzst", files, use_temp_file=False)
```

### معالجة الأخطاء

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
    print("فشل في إلغاء ضغط الأرشيف")
except TzstFileNotFoundError:
    print("ملف الأرشيف غير موجود")
except KeyboardInterrupt:
    print("العملية مقاطعة من قبل المستخدم")
    # التنظيف يتم تلقائياً
```

## الأداء والمقارنة

### نصائح الأداء

1. **مستويات الضغط**: المستوى 3 هو الأمثل لمعظم حالات الاستخدام
2. **التدفق**: استخدم للأرشيف أكبر من 100 ميجابايت
3. **عمليات الدفعات**: أضف ملفات متعددة في جلسة واحدة
4. **أنواع الملفات**: الملفات المضغوطة مسبقاً لن تنضغط كثيراً أكثر

### مقابل أدوات أخرى

**مقابل tar + gzip:**

- نسب ضغط أفضل
- إلغاء ضغط أسرع
- خوارزمية حديثة

**مقابل tar + xz:**

- ضغط أسرع بشكل كبير
- نسب ضغط مماثلة
- توازن سرعة/ضغط أفضل

**مقابل zip:**

- ضغط أفضل
- يحافظ على أذونات Unix والبيانات الوصفية
- دعم تدفق أفضل

## المتطلبات

- Python 3.12 أو أعلى
- zstandard >= 0.19.0

## التطوير

### إعداد بيئة التطوير

يستخدم هذا المشروع معايير تعبئة Python الحديثة:

```bash
git clone https://github.com/xixu-me/tzst.git
cd tzst
pip install -e .[dev]
```

### تشغيل الاختبارات

```bash
# تشغيل الاختبارات مع التغطية
pytest --cov=tzst --cov-report=html

# أو استخدم الأمر الأبسط (إعدادات التغطية في pyproject.toml)
pytest
```

### جودة الكود

```bash
# فحص جودة الكود
ruff check src tests

# تنسيق الكود
ruff format src tests
```

## المساهمة

نرحب بالمساهمات! يرجى قراءة [دليل المساهمة](CONTRIBUTING.md) لـ:

- إعداد التطوير وهيكل المشروع
- إرشادات أسلوب الكود وأفضل الممارسات
- متطلبات الاختبار وكتابة الاختبارات
- عملية طلب السحب وسير عمل المراجعة

### البداية السريعة للمساهمين

```bash
git clone https://github.com/xixu-me/tzst.git
cd tzst
pip install -e .[dev]
python -m pytest tests/
```

### أنواع المساهمات المرحب بها

- **إصلاح الأخطاء** - إصلاح مشاكل في الوظائف الموجودة
- **الميزات** - إضافة قدرات جديدة للمكتبة
- **التوثيق** - تحسين أو إضافة التوثيق
- **الاختبارات** - إضافة أو تحسين تغطية الاختبار
- **الأداء** - تحسين الكود الموجود
- **الأمان** - معالجة الثغرات الأمنية

## الشكر والتقدير

- [Meta Zstandard](https://github.com/facebook/zstd) لخوارزمية الضغط الممتازة
- [python-zstandard](https://github.com/indygreg/python-zstandard) لروابط Python
- مجتمع Python للإلهام والملاحظات

## الترخيص

حقوق النشر &copy; [شي شو](https://xi-xu.me). جميع الحقوق محفوظة.

مرخص تحت ترخيص [BSD 3-Clause](LICENSE).

</div>
