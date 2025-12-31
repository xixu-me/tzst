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

[🇺🇸 English](./README.md) | [🇨🇳 汉语](./README.zh.md) | [🇪🇸 español](./README.es.md) | [🇯🇵 日本語](./README.ja.md) | [🇦🇪 العربية](./README.ar.md) | [🇷🇺 русский](./README.ru.md) | [🇩🇪 Deutsch](./README.de.md) | [🇫🇷 français](./README.fr.md) | [🇰🇷 한국어](./README.ko.md) | **🇧🇷 português**

**tzst** é uma biblioteca Python de próxima geração projetada para gerenciamento moderno de arquivos, aproveitando a compressão Zstandard de ponta para oferecer desempenho, segurança e confiabilidade superiores. Construída exclusivamente para Python 3.12+, esta solução corporativa combina operações atômicas, eficiência de streaming e uma API meticulosamente elaborada para redefinir como os desenvolvedores lidam com arquivos `.tzst`/`.tar.zst` em ambientes de produção. 🚀

Artigo de análise técnica aprofundada publicado: **[Deep Dive into tzst: A Modern Python Archiving Library Based on Zstandard](https://blog.xi-xu.me/2025/11/01/deep-dive-into-tzst-en.html)**.

## ✨ Recursos

- **🗜️ Alta Compressão**: Compressão Zstandard para excelentes taxas de compressão e velocidade
- **📁 Compatibilidade com Tar**: Cria arquivos tar padrão comprimidos com Zstandard
- **💻 Interface de Linha de Comando**: CLI intuitiva com suporte a streaming e opções abrangentes
- **🐍 API Python**: API limpa e pythônica para uso programático
- **🌍 Multiplataforma**: Funciona no Windows, macOS e Linux
- **📂 Múltiplas Extensões**: Suporta tanto extensões `.tzst` quanto `.tar.zst`
- **💾 Eficiente em Memória**: Modo streaming para lidar com grandes arquivos com uso mínimo de memória
- **⚡ Operações Atômicas**: Operações de arquivo seguras com limpeza automática em caso de interrupção
- **🔒 Seguro por Padrão**: Usa o filtro 'data' para máxima segurança durante a extração
- **🚨 Tratamento de Erros Aprimorado**: Mensagens de erro claras com alternativas úteis

## 📥 Instalação

### Dos Releases do GitHub

Baixe executáveis independentes que não requerem instalação do Python:

#### Plataformas Suportadas

| Plataforma | Arquitetura | Arquivo |
|----------|-------------|------|
| **🐧 Linux** | x86_64 | `tzst-{versão}-linux-amd64.zip` |
| **🐧 Linux** | ARM64 | `tzst-{versão}-linux-arm64.zip` |
| **🪟 Windows** | x64 | `tzst-{versão}-windows-amd64.zip` |
| **🪟 Windows** | ARM64 | `tzst-{versão}-windows-arm64.zip` |
| **🍎 macOS** | Intel | `tzst-{versão}-darwin-amd64.zip` |
| **🍎 macOS** | Apple Silicon | `tzst-{versão}-darwin-arm64.zip` |

#### 🛠️ Passos de Instalação

1. **📥 Baixe** o arquivo apropriado para sua plataforma da [página de releases mais recentes](https://github.com/xixu-me/tzst/releases/latest)
2. **📦 Extraia** o arquivo para obter o executável `tzst` (ou `tzst.exe` no Windows)
3. **📂 Mova** o executável para um diretório em seu PATH:
   - **🐧 Linux/macOS**: `sudo mv tzst /usr/local/bin/`
   - **🪟 Windows**: Adicione o diretório contendo `tzst.exe` à sua variável de ambiente PATH
4. **✅ Verifique** a instalação: `tzst --help`

#### 🎯 Benefícios da Instalação Binária

- ✅ **Python não é necessário** - Executável independente
- ✅ **Inicialização mais rápida** - Sem overhead do interpretador Python
- ✅ **Implantação fácil** - Distribuição de arquivo único
- ✅ **Comportamento consistente** - Dependências incluídas

### 📦 Do PyPI

Usando pip:

```bash
pip install tzst
```

Ou usando uv (recomendado):

```bash
uv tool install tzst
```

### 🔧 Do Código Fonte

```bash
git clone https://github.com/xixu-me/tzst.git
cd tzst
pip install .
```

### 🚀 Instalação para Desenvolvimento

Este projeto usa padrões modernos de empacotamento Python:

```bash
git clone https://github.com/xixu-me/tzst.git
cd tzst
pip install -e .[dev]
```

## 🚀 Início Rápido

### 💻 Uso da Linha de Comando

```bash
# 📁 Criar um arquivo
tzst a archive.tzst file1.txt file2.txt directory/

# 📤 Extrair um arquivo
tzst x archive.tzst

# 📋 Listar conteúdo do arquivo
tzst l archive.tzst

# 🧪 Testar integridade do arquivo
tzst t archive.tzst
```

### 🐍 Uso da API Python

```python
from tzst import create_archive, extract_archive, list_archive

# Criar um arquivo
create_archive("archive.tzst", ["file1.txt", "file2.txt", "directory/"])

# Extrair um arquivo
extract_archive("archive.tzst", "output_directory/")

# Listar conteúdo do arquivo
contents = list_archive("archive.tzst", verbose=True)
for item in contents:
    print(f"{item['name']}: {item['size']} bytes")
```

## 💻 Interface de Linha de Comando

### 📁 Operações de Arquivo

#### ➕ Criar Arquivo

```bash
# Uso básico
tzst a archive.tzst file1.txt file2.txt

# Com nível de compressão (1-22, padrão: 3)
tzst a archive.tzst files/ -l 15

# Comandos alternativos
tzst add archive.tzst files/
tzst create archive.tzst files/
```

#### 📤 Extrair Arquivo

```bash
# Extrair com estrutura completa de diretórios
tzst x archive.tzst

# Extrair para diretório específico
tzst x archive.tzst -o output/

# Extrair arquivos específicos
tzst x archive.tzst file1.txt dir/file2.txt

# Extrair sem estrutura de diretórios (plano)
tzst e archive.tzst -o output/

# Usar modo streaming para grandes arquivos
tzst x archive.tzst --streaming -o output/
```

#### 📋 Listar Conteúdo

```bash
# Listagem simples
tzst l archive.tzst

# Listagem detalhada com informações
tzst l archive.tzst -v

# Usar modo streaming para grandes arquivos
tzst l archive.tzst --streaming -v
```

#### 🧪 Testar Integridade

```bash
# Testar integridade do arquivo
tzst t archive.tzst

# Testar com modo streaming
tzst t archive.tzst --streaming
```

### 📊 Referência de Comandos

| Comando | Aliases | Descrição | Suporte a Streaming |
|---------|---------|-------------|-------------------|
| `a` | `add`, `create` | Criar ou adicionar ao arquivo | N/A |
| `x` | `extract` | Extrair com caminhos completos | ✓ `--streaming` |
| `e` | `extract-flat` | Extrair sem estrutura de diretórios | ✓ `--streaming` |
| `l` | `list` | Listar conteúdo do arquivo | ✓ `--streaming` |
| `t` | `test` | Testar integridade do arquivo | ✓ `--streaming` |

### ⚙️ Opções da CLI

- `-v, --verbose`: Ativar saída detalhada
- `-o, --output DIR`: Especificar diretório de saída (comandos de extração)
- `-l, --level LEVEL`: Definir nível de compressão 1-22 (comando de criação)
- `--streaming`: Ativar modo streaming para processamento eficiente em memória
- `--filter FILTER`: Filtro de segurança para extração (data/tar/fully_trusted)
- `--no-atomic`: Desativar operações de arquivo atômicas (não recomendado)

### 🔒 Filtros de Segurança

```bash
# Extrair com máxima segurança (padrão)
tzst x archive.tzst --filter data

# Extrair com compatibilidade tar padrão
tzst x archive.tzst --filter tar

# Extrair com confiança total (perigoso - apenas para arquivos confiáveis)
tzst x archive.tzst --filter fully_trusted
```

**🔐 Opções de Filtro de Segurança:**

- `data` (padrão): Mais seguro. Bloqueia arquivos perigosos, caminhos absolutos e caminhos fora do diretório de extração
- `tar`: Compatibilidade tar padrão. Bloqueia caminhos absolutos e travessia de diretórios
- `fully_trusted`: Sem restrições de segurança. Use apenas com arquivos completamente confiáveis

## 🐍 API Python

### 📦 Classe TzstArchive

```python
from tzst import TzstArchive

# Criar um novo arquivo
with TzstArchive("archive.tzst", "w", compression_level=5) as archive:
    archive.add("file.txt")
    archive.add("directory/", recursive=True)

# Ler um arquivo existente
with TzstArchive("archive.tzst", "r") as archive:
    # Listar conteúdo
    contents = archive.list(verbose=True)
    
    # Extrair com filtro de segurança
    archive.extract("file.txt", "output/", filter="data")
    
    # Testar integridade
    is_valid = archive.test()

# Para grandes arquivos, usar modo streaming
with TzstArchive("large_archive.tzst", "r", streaming=True) as archive:
    archive.extract(path="output/")
```

**⚠️ Limitações Importantes:**

- **❌ Modo de anexação não suportado**: Crie múltiplos arquivos ou recrie o arquivo inteiro em vez disso

### 🎯 Funções de Conveniência

#### 📁 create_archive()

```python
from tzst import create_archive

# Criar com operações atômicas (padrão)
create_archive(
    archive_path="backup.tzst",
    files=["documents/", "photos/", "config.txt"],
    compression_level=10
)
```

#### 📤 extract_archive()

```python
from tzst import extract_archive

# Extrair com segurança (padrão: filtro 'data')
extract_archive("backup.tzst", "restore/")

# Extrair arquivos específicos
extract_archive("backup.tzst", "restore/", members=["config.txt"])

# Achatar estrutura de diretórios
extract_archive("backup.tzst", "restore/", flatten=True)

# Usar streaming para grandes arquivos
extract_archive("large_backup.tzst", "restore/", streaming=True)
```

#### 📋 list_archive()

```python
from tzst import list_archive

# Listagem simples
files = list_archive("backup.tzst")

# Listagem detalhada
files = list_archive("backup.tzst", verbose=True)

# Streaming para grandes arquivos
files = list_archive("large_backup.tzst", streaming=True)
```

#### 🧪 test_archive()

```python
from tzst import test_archive

# Teste básico de integridade
if test_archive("backup.tzst"):
    print("Arquivo é válido")

# Testar com streaming
if test_archive("large_backup.tzst", streaming=True):
    print("Grande arquivo é válido")
```

## 🔧 Recursos Avançados

### 📂 Extensões de Arquivo

A biblioteca automaticamente lida com extensões de arquivo com normalização inteligente:

- `.tzst` - Extensão primária para arquivos tar+zstandard
- `.tar.zst` - Extensão padrão alternativa
- Detecção automática ao abrir arquivos existentes
- Adição automática de extensão ao criar arquivos

```python
# Todos estes criam arquivos válidos
create_archive("backup.tzst", files)      # Cria backup.tzst
create_archive("backup.tar.zst", files)  # Cria backup.tar.zst  
create_archive("backup", files)          # Cria backup.tzst
create_archive("backup.txt", files)      # Cria backup.tzst (normalizado)
```

### 🗜️ Níveis de Compressão

Os níveis de compressão Zstandard variam de 1 (mais rápido) a 22 (melhor compressão):

- **Nível 1-3**: Compressão rápida, arquivos maiores
- **Nível 3** (padrão): Bom equilíbrio entre velocidade e compressão
- **Nível 10-15**: Melhor compressão, mais lento
- **Nível 20-22**: Compressão máxima, muito mais lento

### 🌊 Modo Streaming

Use o modo streaming para processamento eficiente em memória de grandes arquivos:

**✅ Benefícios:**

- Uso de memória significativamente reduzido
- Melhor desempenho para arquivos que não cabem na memória
- Limpeza automática de recursos

**🎯 Quando usar:**

- Arquivos maiores que 100MB
- Ambientes com memória limitada
- Processamento de arquivos com muitos arquivos grandes

```python
# Exemplo: Processando um grande arquivo de backup
from tzst import extract_archive, list_archive, test_archive

large_archive = "backup_500gb.tzst"

# Operações eficientes em memória
is_valid = test_archive(large_archive, streaming=True)
contents = list_archive(large_archive, streaming=True, verbose=True)
extract_archive(large_archive, "restore/", streaming=True)
```

### ⚡ Operações Atômicas

Todas as operações de criação de arquivo usam operações de arquivo atômicas por padrão:

- Arquivos criados em arquivos temporários primeiro, depois movidos atomicamente
- Limpeza automática se o processo for interrompido
- Nenhum risco de arquivos corrompidos ou incompletos
- Compatibilidade multiplataforma

```python
# Operações atômicas habilitadas por padrão
create_archive("important.tzst", files)  # Seguro contra interrupção

# Pode ser desabilitado se necessário (não recomendado)
create_archive("test.tzst", files, use_temp_file=False)
```

### 🚨 Tratamento de Erros

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
    print("Falha ao descomprimir arquivo")
except TzstFileNotFoundError:
    print("Arquivo de arquivo não encontrado")
except KeyboardInterrupt:
    print("Operação interrompida pelo usuário")
    # Limpeza é tratada automaticamente
```

## 🚀 Desempenho e Comparação

### 💡 Dicas de Desempenho

1. **🗜️ Níveis de compressão**: Nível 3 é ótimo para a maioria dos casos de uso
2. **🌊 Streaming**: Use para arquivos maiores que 100MB
3. **📦 Operações em lote**: Adicione múltiplos arquivos em uma única sessão
4. **📄 Tipos de arquivo**: Arquivos já comprimidos não comprimirão muito mais

### 🆚 vs Outras Ferramentas

**vs tar + gzip:**

- ✅ Melhores taxas de compressão
- ⚡ Descompressão mais rápida
- 🔄 Algoritmo moderno

**vs tar + xz:**

- 🚀 Compressão significativamente mais rápida
- 📊 Taxas de compressão similares
- ⚖️ Melhor compromisso velocidade/compressão

**vs zip:**

- 🗜️ Melhor compressão
- 🔐 Preserva permissões Unix e metadados
- 🌊 Melhor suporte a streaming

## 📋 Requisitos

- 🐍 Python 3.12 ou superior
- 📦 zstandard >= 0.19.0

## 🛠️ Desenvolvimento

### 🚀 Configurando Ambiente de Desenvolvimento

Este projeto usa padrões modernos de empacotamento Python:

```bash
git clone https://github.com/xixu-me/tzst.git
cd tzst
pip install -e .[dev]
```

### 🧪 Executando Testes

```bash
# Executar testes com cobertura
pytest --cov=tzst --cov-report=html

# Ou usar o comando mais simples (configurações de cobertura estão em pyproject.toml)
pytest
```

### ✨ Qualidade do Código

```bash
# Verificar qualidade do código
ruff check src tests

# Formatar código
ruff format src tests
```

## 🤝 Contribuindo

Nós recebemos contribuições! Por favor, leia nosso [Guia de Contribuição](CONTRIBUTING.md) para:

- Configuração de desenvolvimento e estrutura do projeto
- Diretrizes de estilo de código e melhores práticas  
- Requisitos de teste e escrita de testes
- Processo de pull request e fluxo de revisão

### 🚀 Início Rápido para Colaboradores

```bash
git clone https://github.com/xixu-me/tzst.git
cd tzst
pip install -e .[dev]
python -m pytest tests/
```

### 🎯 Tipos de Contribuições Bem-vindas

- 🐛 **Correções de bugs** - Corrigir problemas na funcionalidade existente
- ✨ **Recursos** - Adicionar novas capacidades à biblioteca
- 📚 **Documentação** - Melhorar ou adicionar documentação
- 🧪 **Testes** - Adicionar ou melhorar cobertura de testes
- ⚡ **Desempenho** - Otimizar código existente
- 🔒 **Segurança** - Abordar vulnerabilidades de segurança

## 🙏 Agradecimentos

- [Meta Zstandard](https://github.com/facebook/zstd) pelo excelente algoritmo de compressão
- [python-zstandard](https://github.com/indygreg/python-zstandard) pelas ligações Python
- A comunidade Python pela inspiração e feedback

## 📄 Licença

Direitos autorais &copy; [Xi Xu](https://xi-xu.me). Todos os direitos reservados.

Licenciado sob a licença [BSD 3-Clause](LICENSE).
