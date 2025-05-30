# Análise de Quedas de Meteoritos na Terra: Aquisição e Preparação de Dados

Este repositório contém uma análise abrangente de dados sobre meteoritos que caíram na Terra no período de 1963 a 2013, desenvolvido como parte da disciplina de Aquisição e Preparação de Dados do curso de Ciência de Dados. O projeto aplica técnicas avançadas de limpeza, transformação e análise de dados geoespaciais para compreender padrões de distribuição global de meteoritos.

## 🌍 Visão Geral

Os meteoritos representam uma das poucas oportunidades de estudar material extraterrestre sem missões espaciais. Este projeto aborda:

- **Análise exploratória** dos dados históricos de quedas de meteoritos da NASA
- **Pipeline robusto** de limpeza e preparação de dados geoespaciais
- **Geocodificação reversa** para identificação de países por coordenadas
- **Visualizações interativas** da distribuição geográfica e temporal
- **Insights científicos** sobre padrões de quedas de meteoritos

## 🎯 Objetivos e Metas

Nosso objetivo é aplicar técnicas de aquisição e preparação de dados para analisar padrões de quedas de meteoritos na Terra. As metas específicas incluem:

1. **Limpeza de Dados:** Tratamento de valores ausentes, duplicatas e inconsistências
2. **Geocodificação:** Conversão de coordenadas geográficas em países identificáveis
3. **Análise Temporal:** Identificação de padrões e tendências ao longo de 50 anos
4. **Distribuição Geográfica:** Mapeamento de concentrações regionais de meteoritos
5. **Feature Engineering:** Criação de categorias de massa e novas variáveis analíticas

## 📊 Principais Descobertas

A análise revelou insights fascinantes sobre o comportamento das quedas de meteoritos:

- **Concentração Antártica:** 22.094 meteoritos (61% do total) registrados na Antártida
- **Distribuição Desigual:** Top 3 países concentram 86% de todos os registros
- **Variação de Massa:** Distribuição altamente assimétrica, de miligramas a toneladas
- **Picos Temporais:** Anos de 1979, 1988 e 1998 apresentaram maior número de registros
- **Tendência Crescente:** Aumento na frequência de registros a partir da década de 1970

## 🔧 Pipeline de Preparação

O pipeline desenvolvido transformou dados brutos em uma base analítica de qualidade:

```
Dados Brutos (45.716 registros)
    ↓ Remoção de Valores Ausentes
Base Limpa (38.116 registros)
    ↓ Remoção de Duplicatas
Base Única (38.116 registros)
    ↓ Filtragem Temporal (1963-2013)
Base Temporal (36.188 registros)
    ↓ Geocodificação Reversa
Base Geolocalizada (36.188 registros)
    ↓ Categorização de Massa
Base Final (36.188 registros)
```

## 📁 Estrutura do Projeto

```
meteorite-analysis/
├── data/
│   ├── meteorite-landings.csv      # Dataset original da NASA
│   └── base_final.csv              # Dataset processado
├── scripts/
│   ├── 01_analise_exploratoria.py  # Limpeza e preparação
│   └── 02_analise_final.py         # Visualizações e análises
├── outputs/
│   ├── meteoritos_por_pais.png     # Gráfico de distribuição por país
│   ├── media_massa_por_pais.png    # Gráfico de massa média
│   └── meteoritos_por_ano.png      # Gráfico de distribuição temporal
├── docs/
│   └── relatorio_final.pdf         # Relatório científico completo
└── requirements.txt                # Dependências do projeto
```

## 🐍 Scripts

### 1. 01_analise_exploratoria.py

**Localização:** `scripts/01_analise_exploratoria.py`

Este script realiza a limpeza e preparação completa dos dados de meteoritos.

#### Funcionalidades:
- Carrega dados originais da NASA (45.716 registros)
- Remove valores ausentes em colunas essenciais (lat, lon, year, mass)
- Elimina registros duplicados
- Filtra coordenadas geográficas válidas (-90°≤lat≤90°, -180°≤lon≤180°)
- Aplica filtro temporal para período 1963-2013
- Implementa geocodificação reversa robusta com tratamento especial para:
  - Antártida (latitudes < -60°)
  - Oceano Ártico (latitudes > 75°)
  - Mapeamento de 150+ códigos de países
- Cria categorização de massa (Pequeno/Médio/Grande/Muito Grande)
- Salva base final processada

#### Principais Inovações:
- **Geocodificação Inteligente:** Função customizada para regiões polares
- **Validação Geográfica:** Verificação rigorosa de coordenadas
- **Tratamento de Outliers:** Manutenção científica de valores extremos naturais

### 2. 02_analise_final.py

**Localização:** `scripts/02_analise_final.py`

Este script gera visualizações e análises estatísticas da base processada.

#### Funcionalidades:
- Instala dependências automaticamente
- Carrega base final com validações de integridade
- Gera três visualizações principais:
  1. **Distribuição por País:** Top 20 países com mais meteoritos
  2. **Massa Média por País:** Análise de tamanhos regionais
  3. **Distribuição Temporal:** Evolução anual com picos destacados
- Calcula estatísticas descritivas abrangentes
- Salva gráficos em alta resolução (300 DPI)
- Produz relatório final consolidado

#### Principais Visualizações:
- Gráficos de barras com anotações de valores
- Série temporal com identificação de picos
- Configurações profissionais de matplotlib

## 📋 Requisitos e Instalação

### Dependências Principais:
```
pandas>=1.3.0
numpy>=1.21.0
matplotlib>=3.4.0
reverse-geocoder>=1.5.1
```

### Instalação:
```bash
# Clone o repositório
git clone https://github.com/seu-usuario/meteorite-analysis.git
cd meteorite-analysis

# Instale as dependências
pip install -r requirements.txt

# Execute os scripts
python scripts/01_analise_exploratoria.py
python scripts/02_analise_final.py
```

## 🚀 Como Executar

1. **Preparação dos Dados:**
   ```bash
   python scripts/01_analise_exploratoria.py
   ```
   - Processa dados brutos
   - Gera `base_final.csv`

2. **Análise e Visualização:**
   ```bash
   python scripts/02_analise_final.py
   ```
   - Cria gráficos e estatísticas
   - Salva visualizações em `outputs/`

## 📈 Resultados e Insights

### Distribuição Geográfica:
- **Antártida domina:** 61% de todos os meteoritos registrados
- **Fatores de concentração:** Preservação no gelo, expedições científicas
- **Top 5 países:** Antártida, Gana, Omã, Líbia, Estados Unidos

### Análise Temporal:
- **Período analisado:** 1963-2013 (50 anos)
- **Picos identificados:** 1979 (3.045), 1988 (2.295), 1998 (2.147)
- **Tendência:** Crescimento na detecção a partir dos anos 1970

### Características de Massa:
- **Distribuição natural:** Assimétrica com valores extremos preservados
- **Variação regional:** China e Turcomenistão com maiores massas médias
- **Categorização:** 4 faixas de tamanho para análise intuitiva

## 🔬 Metodologia Científica

### Tratamento de Outliers:
Diferentemente de análises convencionais, **mantivemos valores extremos** por representarem variação natural dos meteoritos (de miligramas a toneladas), seguindo princípios científicos adequados ao domínio.

### Geocodificação Robusta:
Implementamos tratamento especial para regiões polares e oceânicas, garantindo precisão na identificação geográfica.

### Validação de Dados:
Aplicamos múltiplas camadas de validação para garantir qualidade e consistência dos dados finais.

## 👥 Contribuições

**Desenvolvido por:** Wesley Rodrigo dos Santos  
**RA:** 10433408  
**Disciplina:** Aquisição e Preparação de Dados  
**Curso:** Ciência de Dados

## 🔗 Links e Recursos

- **Dataset Original:** [NASA Meteorite Landings (Kaggle)](https://www.kaggle.com/datasets/nasa/meteorite-landings)
- **Documentação Técnica:** `docs/relatorio_final.pdf`
- **Biblioteca Geocoding:** [reverse-geocoder](https://pypi.org/project/reverse-geocoder/)

## 📚 Referências

- NASA - Meteorite Landings Database
- Kaggle - NASA Meteorite Landings Dataset
- Python Software Foundation - Pandas, NumPy, Matplotlib
- Ajay Thampi - reverse-geocoder library
- Universidade Presbiteriana Mackenzie - Curso de Ciência de Dados

## 📄 Licença

Este projeto é desenvolvido para fins educacionais como parte do curso de Ciência de Dados. Os dados utilizados são de domínio público da NASA.

---

**⭐ Se este projeto foi útil, considere dar uma estrela no repositório!**
"""
