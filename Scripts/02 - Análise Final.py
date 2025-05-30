import subprocess
import sys
import os

def install_and_import(package, import_name=None):
    if import_name is None:
        import_name = package
    
    try:
        __import__(import_name)
    except ImportError:
        print(f"Instalando o pacote {package}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        try:
            __import__(import_name)
        except ImportError:
            print(f"Não foi possível importar {import_name} mesmo após a instalação.")
            return None
    
    return __import__(import_name)

# Lista de pacotes necessários
packages = [
    ('pandas', 'pandas'),
    ('numpy', 'numpy'),
    ('matplotlib', 'matplotlib')
]

# Importar pacotes
for package, import_name in packages:
    module = install_and_import(package, import_name)
    if module:
        globals()[import_name] = module

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

print("=" * 60)
print("ANÁLISE FINAL - METEORITOS")
print("=" * 60)

# Definir caminhos automaticamente
script_dir = os.path.dirname(os.path.abspath(__file__))
# Subir um nível para chegar à pasta raiz do projeto (analise_meteoritos)
project_dir = os.path.dirname(script_dir)
data_dir = os.path.join(project_dir, 'Data')
outputs_dir = os.path.join(project_dir, 'Outputs')
input_file = os.path.join(data_dir, 'base_final.csv')


# Criar pasta Outputs se não existir
os.makedirs(outputs_dir, exist_ok=True)

# Verificar se o arquivo existe
if not os.path.exists(input_file):
        print("Arquivo não localizado! Certifique-se de executar o script '01 - Análise Exploratória, Limpeza e Geração da Amostra', para gerar a base tratada.")
        sys.exit(1)

# Carregar a base final
try:
    df = pd.read_csv(input_file)
    print(f"Total de registros carregados: {len(df)}")
    
    if df.empty:
        print("ERRO: O arquivo CSV está vazio!")
        sys.exit(1)
        
except Exception as e:
    print(f"ERRO ao carregar o arquivo: {e}")
    sys.exit(1)

# Configurações de visualização
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 12

# 1. LOCAIS DE QUEDAS DOS METEORITOS (NÚMERO DE METEORITOS POR PAÍS)
print("\n" + "=" * 60)
print("1. LOCAIS DE QUEDAS DOS METEORITOS")
print("=" * 60)

if 'country' not in df.columns:
    print("ERRO: Coluna 'country' não encontrada no DataFrame!")
    print(f"Colunas disponíveis: {list(df.columns)}")
else:
    country_counts = df['country'].value_counts()
    top_countries = country_counts.head(20)
    
    print(f"Total de países com meteoritos: {len(country_counts)}")
    print("\nTop 10 países com mais meteoritos:")
    for i, (country, count) in enumerate(top_countries.head(10).items(), 1):
        print(f"{i:2d}. {country}: {count:,} meteoritos")
    
    # Criar o gráfico
    plt.figure(figsize=(14, 8))
    bars = plt.bar(range(len(top_countries)), top_countries.values, 
                   color='skyblue', edgecolor='navy', alpha=0.7)
    plt.title('Número de Meteoritos por País', fontsize=16, fontweight='bold')
    plt.xlabel('País', fontsize=14)
    plt.ylabel('Número de Meteoritos', fontsize=14)
    plt.xticks(range(len(top_countries)), top_countries.index, rotation=45, ha='right')
    
    # Adicionar valores nas barras
    for i, bar in enumerate(bars):
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + height*0.01,
                f'{int(height):,}',
                ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    plt.tight_layout()
    output_path = os.path.join(outputs_dir, 'meteoritos_por_pais.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Gráfico salvo em: {output_path}")
    plt.show()

# 3. MÉDIA DE MASSA DE METEORITOS POR PAÍS
print("\n" + "=" * 60)
print("3. MÉDIA DE MASSA DE METEORITOS POR PAÍS")
print("=" * 60)

if 'mass' not in df.columns:
    print("ERRO: Coluna 'mass' não encontrada no DataFrame!")
else:
    # Calcular a média de massa por país (excluindo valores nulos)
    mass_by_country = df.groupby('country')['mass'].mean().reset_index()
    mass_by_country = mass_by_country.sort_values('mass', ascending=False)
    
    # Selecionar os 20 principais países para melhor visualização
    top_countries_by_mass = mass_by_country.head(20)
    
    print("Top 10 países com maior massa média de meteoritos:")
    for i, row in enumerate(top_countries_by_mass.head(10).itertuples(), 1):
        print(f"{i:2d}. {row.country}: {row.mass:,.2f} g")
    
    # Criar o gráfico de média de massa por país
    plt.figure(figsize=(14, 8))
    bars = plt.bar(range(len(top_countries_by_mass)), top_countries_by_mass['mass'], 
                   color='lightcoral', edgecolor='darkred', alpha=0.7)
    plt.title('Média de Massa de Meteoritos por País (em gramas)', fontsize=16, fontweight='bold')
    plt.xlabel('País', fontsize=14)
    plt.ylabel('Massa Média (g)', fontsize=14)
    plt.xticks(range(len(top_countries_by_mass)), top_countries_by_mass['country'], 
               rotation=45, ha='right')
    
    # Adicionar valores nas barras
    for i, bar in enumerate(bars):
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + height*0.01,
                f'{int(height):,}g',
                ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    plt.tight_layout()
    output_path = os.path.join(outputs_dir, 'media_massa_por_pais.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Gráfico salvo em: {output_path}")
    plt.show()

# 4. DISTRIBUIÇÃO DE METEORITOS POR ANO
print("\n" + "=" * 60)
print("4. DISTRIBUIÇÃO DE METEORITOS POR ANO")
print("=" * 60)

if 'year' not in df.columns:
    print("ERRO: Coluna 'year' não encontrada no DataFrame!")
else:
    # Remover valores nulos de ano e converter para int
    df_year = df.dropna(subset=['year'])
    year_counts = df_year['year'].astype(int).value_counts().sort_index()
    
    print(f"Período analisado: {int(df_year['year'].min())} a {int(df_year['year'].max())}")
    print("\nAnos com mais meteoritos registrados:")
    for i, (year, count) in enumerate(year_counts.nlargest(5).items(), 1):
        print(f"{i}. {year}: {count} meteoritos")
    
    plt.figure(figsize=(14, 8))
    plt.plot(year_counts.index, year_counts.values, marker='o', 
             markersize=6, linewidth=2, color='darkblue', alpha=0.7)
    plt.title('Número de Meteoritos por Ano', fontsize=16, fontweight='bold')
    plt.xlabel('Ano', fontsize=14)
    plt.ylabel('Número de Meteoritos', fontsize=14)
    plt.grid(True, alpha=0.3)
    
    # Adicionar anotações para os picos
    top_years = year_counts.nlargest(3)
    for year, count in top_years.items():
        plt.annotate(f'{count} meteoritos',
                    xy=(year, count),
                    xytext=(0, 15),
                    textcoords='offset points',
                    ha='center',
                    va='bottom',
                    fontweight='bold',
                    bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.7),
                    arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0.2'))
    
    plt.tight_layout()
    output_path = os.path.join(outputs_dir, 'meteoritos_por_ano.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Gráfico salvo em: {output_path}")
    plt.show()

# Resumo final
print("\n" + "=" * 60)
print("RESUMO DA ANÁLISE")
print("=" * 60)
print(f"Total de meteoritos analisados: {len(df):,}")

if 'year' in df.columns:
    df_year = df.dropna(subset=['year'])
    print(f"Período analisado: {int(df_year['year'].min())} a {int(df_year['year'].max())}")

if 'country' in df.columns:
    print(f"Países com meteoritos: {df['country'].nunique()}")
    print(f"País com mais meteoritos: {df['country'].value_counts().index[0]} ({df['country'].value_counts().iloc[0]:,} meteoritos)")

if 'mass_category' in df.columns:
    print(f"Categoria de massa mais comum: {df['mass_category'].value_counts().index[0]}")

if 'mass' in df.columns:
    print(f"Massa média dos meteoritos: {df['mass'].mean():.2f} gramas")
    print(f"Massa total de todos os meteoritos: {df['mass'].sum():,.2f} gramas")

print(f"\nTodos os gráficos foram salvos na pasta: {outputs_dir}")
print("Análise concluída com sucesso!")
