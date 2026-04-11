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

[🇺🇸 English](./README.md) | [🇨🇳 汉语](./README.zh.md) | **🇪🇸 español** | [🇯🇵 日本語](./README.ja.md) | [🇦🇪 العربية](./README.ar.md) | [🇷🇺 русский](./README.ru.md) | [🇩🇪 Deutsch](./README.de.md) | [🇫🇷 français](./README.fr.md) | [🇰🇷 한국어](./README.ko.md) | [🇧🇷 português](./README.pt.md)

**tzst** es una biblioteca y CLI para Python 3.12+ orientada a crear, extraer, listar y validar archivos `.tzst` y `.tar.zst`. Reúne compatibilidad con tar, compresión Zstandard, modo streaming, escrituras atómicas y extracción segura por defecto en una interfaz compacta lista para producción.

> [!NOTE]
> Artículo técnico detallado: **[Deep Dive into tzst: A Modern Python Archiving Library Based on Zstandard](https://blog.xi-xu.me/2025/11/01/deep-dive-into-tzst-en.html)**.

## Características

- **Alta Compresión**: Compresión Zstandard para excelentes ratios de compresión y velocidad.
- **Compatibilidad con Tar**: Crea archivos tar estándar comprimidos con Zstandard.
- **Interfaz de Línea de Comandos**: CLI intuitiva con soporte para transmisión y opciones completas.
- **API de Python**: API limpia y pitónica para uso programático.
- **Multiplataforma**: Funciona en Windows, macOS y Linux.
- **Múltiples Extensiones**: Soporta las extensiones `.tzst` y `.tar.zst`.
- **Eficiente en Memoria**: Modo de transmisión para manejar archivos grandes con un uso mínimo de memoria.
- **Operaciones Atómicas**: Operaciones de archivo seguras con limpieza automática en caso de interrupción.
- **Seguro por Defecto**: Utiliza el filtro 'data' para máxima seguridad durante la extracción.
- **Manejo de Errores Mejorado**: Mensajes de error claros con alternativas útiles.

## Instalación

### Desde los Lanzamientos de GitHub

Descarga ejecutables independientes que no requieren instalación de Python:

#### Plataformas Soportadas

| Plataforma   | Arquitectura | Archivo                               |
|--------------|---------------|---------------------------------------|
| **Linux** | x86_64        | `tzst-{versión}-linux-amd64.zip`    |
| **Linux** | ARM64         | `tzst-{versión}-linux-arm64.zip`   |
| **Windows**| x64           | `tzst-{versión}-windows-amd64.zip`   |
| **Windows**| ARM64         | `tzst-{versión}-windows-arm64.zip`   |
| **macOS** | Intel         | `tzst-{versión}-darwin-amd64.zip`    |
| **macOS** | Apple Silicon | `tzst-{versión}-darwin-arm64.zip`     |

#### Pasos de Instalación

1. **Descarga** el archivo apropiado para tu plataforma desde la [página de lanzamientos más recientes](https://github.com/xixu-me/tzst/releases/latest).
2. **Extrae** el archivo para obtener el ejecutable `tzst` (o `tzst.exe` en Windows).
3. **Mueve** el ejecutable a un directorio en tu PATH:
    - **Linux/macOS**: `sudo mv tzst /usr/local/bin/`
    - **Windows**: Añade el directorio que contiene `tzst.exe` a tu variable de entorno PATH.
4. **Verifica** la instalación: `tzst --help`

#### Beneficios de la Instalación Binaria

- **No requiere Python** - Ejecutable independiente.
- **Inicio más rápido** - Sin la sobrecarga del intérprete de Python.
- **Despliegue fácil** - Distribución en un solo archivo.
- **Comportamiento consistente** - Dependencias incluidas.

### Desde PyPI

Usando pip:

```
pip install tzst
```

O usando uv (recomendado):

```
uv tool install tzst
```

### Desde el Código Fuente

```
git clone https://github.com/xixu-me/tzst.git
cd tzst
pip install .
```

### Instalación para Desarrollo

Este proyecto utiliza estándares modernos de empaquetado de Python:

```
git clone https://github.com/xixu-me/tzst.git
cd tzst
pip install -e .[dev]
```

## Inicio Rápido

### Uso desde la Línea de Comandos

```
# Crear un archivo
tzst a archivo.tzst archivo1.txt archivo2.txt directorio/

# Extraer un archivo
tzst x archivo.tzst

# Listar el contenido del archivo
tzst l archivo.tzst

# Probar la integridad del archivo
tzst t archivo.tzst
```

### Uso de la API de Python

```
from tzst import create_archive, extract_archive, list_archive

# Crear un archivo
create_archive("archivo.tzst", ["archivo1.txt", "archivo2.txt", "directorio/"])

# Extraer un archivo
extract_archive("archivo.tzst", "directorio_salida/")

# Listar el contenido del archivo
contents = list_archive("archivo.tzst", verbose=True)
for item in contents:
    print(f"{item['name']}: {item['size']} bytes")
```

## Interfaz de Línea de Comandos

### Operaciones con Archivos

#### Crear Archivo

```
# Uso básico
tzst a archivo.tzst archivo1.txt archivo2.txt

# Con nivel de compresión (1-22, por defecto: 3)
tzst a archivo.tzst archivos/ -l 15

# Comandos alternativos
tzst add archivo.tzst archivos/
tzst create archivo.tzst archivos/
```

#### Extraer Archivo

```
# Extraer con la estructura de directorios completa
tzst x archivo.tzst

# Extraer a un directorio específico
tzst x archivo.tzst -o salida/

# Extraer archivos específicos
tzst x archivo.tzst archivo1.txt dir/archivo2.txt

# Extraer sin estructura de directorios (plano)
tzst e archivo.tzst -o salida/

# Usar modo de transmisión para archivos grandes
tzst x archivo.tzst --streaming -o salida/
```

#### Listar Contenido

```
# Listado simple
tzst l archivo.tzst

# Listado detallado con detalles
tzst l archivo.tzst -v

# Usar modo de transmisión para archivos grandes
tzst l archivo.tzst --streaming -v
```

#### Probar Integridad

```
# Probar la integridad del archivo
tzst t archivo.tzst

# Probar con modo de transmisión
tzst t archivo.tzst --streaming
```

### Referencia de Comandos

| Comando | Alias              | Descripción                               | Soporte de Transmisión |
|---------|--------------------|-------------------------------------------|------------------------|
| `a`     | `add`, `create`    | Crear o añadir a un archivo               | N/A                    |
| `x`     | `extract`          | Extraer con rutas completas               | ✓ `--streaming`        |
| `e`     | `extract-flat`     | Extraer sin estructura de directorios     | ✓ `--streaming`        |
| `l`     | `list`             | Listar el contenido del archivo           | ✓ `--streaming`        |
| `t`     | `test`             | Probar la integridad del archivo          | ✓ `--streaming`        |

### Opciones de CLI

- `-v, --verbose`: Habilitar salida detallada.
- `-o, --output DIR`: Especificar directorio de salida (comandos de extracción).
- `-l, --level NIVEL`: Establecer nivel de compresión 1-22 (comando de creación).
- `--streaming`: Habilitar modo de transmisión para procesamiento eficiente en memoria.
- `--filter FILTRO`: Filtro de seguridad para extracción (data/tar/fully_trusted).
- `--no-atomic`: Deshabilitar operaciones de archivo atómicas (no recomendado).

### Filtros de Seguridad

```
# Extraer con máxima seguridad (por defecto)
tzst x archivo.tzst --filter data

# Extraer con compatibilidad estándar de tar
tzst x archivo.tzst --filter tar

# Extraer con confianza total (peligroso - solo para archivos de confianza)
tzst x archivo.tzst --filter fully_trusted
```

**Opciones de Filtro de Seguridad:**

- `data` (por defecto): El más seguro. Bloquea archivos peligrosos, rutas absolutas y rutas fuera del directorio de extracción.
- `tar`: Compatibilidad estándar con tar. Bloquea rutas absolutas y recorrido de directorios (directory traversal).
- `fully_trusted`: Sin restricciones de seguridad. Usar solo con archivos completamente confiables.

## API de Python

### Clase TzstArchive

```
from tzst import TzstArchive

# Crear un nuevo archivo
with TzstArchive("archivo.tzst", "w", compression_level=5) as archive:
    archive.add("archivo.txt")
    archive.add("directorio/", recursive=True)

# Leer un archivo existente
with TzstArchive("archivo.tzst", "r") as archive:
    # Listar contenido
    contents = archive.list(verbose=True)
    
    # Extraer con filtro de seguridad
    archive.extract("archivo.txt", "salida/", filter="data")
    
    # Probar integridad
    is_valid = archive.test()

# Para archivos grandes, usar modo de transmisión
with TzstArchive("archivo_grande.tzst", "r", streaming=True) as archive:
    archive.extract(path="salida/")
```

**Limitaciones Importantes:**

- **Modo de Añadir No Soportado**: Crea múltiples archivos o recrea el archivo completo en su lugar.

### Funciones de Conveniencia

#### create_archive()

```
from tzst import create_archive

# Crear con operaciones atómicas (por defecto)
create_archive(
    archive_path="backup.tzst",
    files=["documentos/", "fotos/", "config.txt"],
    compression_level=10
)
```

#### extract_archive()

```
from tzst import extract_archive

# Extraer con seguridad (por defecto: filtro 'data')
extract_archive("backup.tzst", "restaurar/")

# Extraer archivos específicos
extract_archive("backup.tzst", "restaurar/", members=["config.txt"])

# Aplanar estructura de directorios
extract_archive("backup.tzst", "restaurar/", flatten=True)

# Usar transmisión para archivos grandes
extract_archive("backup_grande.tzst", "restaurar/", streaming=True)
```

#### list_archive()

```
from tzst import list_archive

# Listado simple
files = list_archive("backup.tzst")

# Listado detallado
files = list_archive("backup.tzst", verbose=True)

# Transmisión para archivos grandes
files = list_archive("backup_grande.tzst", streaming=True)
```

#### test_archive()

```
from tzst import test_archive

# Prueba de integridad básica
if test_archive("backup.tzst"):
    print("El archivo es válido")

# Prueba con transmisión
if test_archive("backup_grande.tzst", streaming=True):
    print("El archivo grande es válido")
```

## Características Avanzadas

### Extensiones de Archivo

La biblioteca maneja automáticamente las extensiones de archivo con normalización inteligente:

- `.tzst` - Extensión principal para archivos tar+zstandard.
- `.tar.zst` - Extensión estándar alternativa.
- Autodetección al abrir archivos existentes.
- Adición automática de extensión al crear archivos.

```
# Todos estos crean archivos válidos
create_archive("backup.tzst", files)      # Crea backup.tzst
create_archive("backup.tar.zst", files)  # Crea backup.tar.zst  
create_archive("backup", files)          # Crea backup.tzst
create_archive("backup.txt", files)      # Crea backup.tzst (normalizado)
```

### Niveles de Compresión

Los niveles de compresión de Zstandard van de 1 (más rápido) a 22 (mejor compresión):

- **Nivel 1-3**: Compresión rápida, archivos más grandes.
- **Nivel 3** (por defecto): Buen equilibrio entre velocidad y compresión.
- **Nivel 10-15**: Mejor compresión, más lento.
- **Nivel 20-22**: Máxima compresión, mucho más lento.

### Modo de Transmisión (Streaming)

Usa el modo de transmisión para el procesamiento eficiente en memoria de archivos grandes:

**Beneficios:**

- Uso de memoria significativamente reducido.
- Mejor rendimiento para archivos que no caben en memoria.
- Limpieza automática de recursos.

**Cuándo Usar:**

- Archivos mayores de 100MB.
- Entornos con memoria limitada.
- Procesamiento de archivos con muchos archivos grandes.

```
# Ejemplo: Procesando un archivo de copia de seguridad grande
from tzst import extract_archive, list_archive, test_archive

large_archive = "backup_500gb.tzst"

# Operaciones eficientes en memoria
is_valid = test_archive(large_archive, streaming=True)
contents = list_archive(large_archive, streaming=True, verbose=True)
extract_archive(large_archive, "restore/", streaming=True)
```

### Operaciones Atómicas

Todas las operaciones de creación de archivos utilizan operaciones de archivo atómicas por defecto:

- Los archivos se crean primero en archivos temporales y luego se mueven atómicamente.
- Limpieza automática si el proceso se interrumpe.
- Sin riesgo de archivos corruptos o incompletos.
- Compatibilidad multiplataforma.

```
# Operaciones atómicas habilitadas por defecto
create_archive("importante.tzst", files)  # Seguro contra interrupciones

# Se pueden deshabilitar si es necesario (no recomendado)
create_archive("test.tzst", files, use_temp_file=False)
```

### Manejo de Errores

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
    with TzstArchive("archivo.tzst", "r") as archive:
        archive.extract()
except TzstDecompressionError:
    print("Falló la descompresión del archivo")
except TzstFileNotFoundError:
    print("Archivo no encontrado")
except KeyboardInterrupt:
    print("Operación interrumpida por el usuario")
    # La limpieza se maneja automáticamente
```

## Rendimiento y Comparación

### Consejos de Rendimiento

1. **Niveles de compresión**: El nivel 3 es óptimo para la mayoría de los casos de uso.
2. **Transmisión**: Usar para archivos mayores de 100MB.
3. **Operaciones por lotes**: Añadir múltiples archivos en una sola sesión.
4. **Tipos de archivo**: Los archivos ya comprimidos no se comprimirán mucho más.

### vs Otras Herramientas

**vs tar + gzip:**

- Mejores ratios de compresión.
- Descompresión más rápida.
- Algoritmo moderno.

**vs tar + xz:**

- Compresión significativamente más rápida.
- Ratios de compresión similares.
- Mejor equilibrio velocidad/compresión.

**vs zip:**

- Mejor compresión.
- Preserva permisos y metadatos de Unix.
- Mejor soporte para transmisión.

## Requisitos

- Python 3.12 o superior
- zstandard >= 0.19.0

## Desarrollo

### Configuración del Entorno de Desarrollo

Este proyecto utiliza estándares modernos de empaquetado de Python:

```
git clone https://github.com/xixu-me/tzst.git
cd tzst
pip install -e .[dev]
```

### Ejecución de Pruebas

```
# Ejecutar pruebas con cobertura
pytest --cov=tzst --cov-report=html

# O usar el comando más simple (la configuración de cobertura está en pyproject.toml)
pytest
```

### Calidad del Código

```
# Comprobar la calidad del código
ruff check src tests

# Formatear el código
ruff format src tests
```

## Contribuir

¡Aceptamos contribuciones! Por favor, lee nuestra [Guía de Contribución](CONTRIBUTING.md) para:

- Configuración del desarrollo y estructura del proyecto.
- Directrices de estilo de código y mejores prácticas.
- Requisitos de prueba y escritura de pruebas.
- Proceso de pull request y flujo de trabajo de revisión.

### Inicio Rápido para Colaboradores

```
git clone https://github.com/xixu-me/tzst.git
cd tzst
pip install -e .[dev]
python -m pytest tests/
```

### Tipos de Contribuciones Bienvenidas

- **Corrección de errores** - Soluciona problemas en la funcionalidad existente.
- **Características** - Añade nuevas capacidades a la biblioteca.
- **Documentación** - Mejora o añade documentación.
- **Pruebas** - Añade o mejora la cobertura de pruebas.
- **Rendimiento** - Optimiza el código existente.
- **Seguridad** - Aborda vulnerabilidades de seguridad.

## Agradecimientos

- [Meta Zstandard](https://github.com/facebook/zstd) por el excelente algoritmo de compresión.
- [python-zstandard](https://github.com/indygreg/python-zstandard) por los bindings de Python.
- La comunidad de Python por la inspiración y los comentarios.

## Licencia

Copyright &copy; [Xi Xu](https://xi-xu.me). Todos los derechos reservados.

Licenciado bajo la licencia [BSD 3-Clause](LICENSE).
