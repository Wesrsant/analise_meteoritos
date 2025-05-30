import pandas as pd
import numpy as np
import sys
import subprocess
import os

# Verificar e instalar bibliotecas necessárias
try:
    import reverse_geocoder
except ImportError:
    print("Instalando a biblioteca reverse_geocoder...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "reverse_geocoder"])
    print("reverse_geocoder instalado com sucesso!")

import reverse_geocoder as rg

print("=" * 60)
print("ANÁLISE EXPLORATÓRIA E LIMPEZA DE DADOS - METEORITOS")
print("=" * 60)

# Definir caminhos automaticamente
script_dir = os.path.dirname(os.path.abspath(__file__))
# Subir um nível para chegar à pasta raiz do projeto (analise_meteoritos)
project_dir = os.path.dirname(script_dir)
data_dir = os.path.join(project_dir, 'Data')
input_file = os.path.join(data_dir, 'meteorite-landings.csv')
output_file = os.path.join(data_dir, 'base_final.csv')

print(f"Diretório do script: {script_dir}")
print(f"Diretório do projeto: {project_dir}")
print(f"Diretório de dados: {data_dir}")
print(f"Arquivo de entrada: {input_file}")

# Verificar se o arquivo de entrada existe
if not os.path.exists(input_file):
    print(f"Erro: Arquivo não encontrado em {input_file}")
    print("Verifique se o arquivo 'meteorite-landings.csv' está na pasta 'Data'")
    
    # Tentar localizar o arquivo em outros locais possíveis
    alternative_paths = [
        os.path.join(script_dir, 'meteorite-landings.csv'),  # Na mesma pasta do script
        os.path.join(script_dir, 'Data', 'meteorite-landings.csv'),  # Scripts/Data
        os.path.join(project_dir, 'meteorite-landings.csv'),  # Na raiz do projeto
        os.path.join(os.path.dirname(project_dir), 'Data', 'meteorite-landings.csv'),  # Um nível acima
    ]
    
    print("\nTentando localizar o arquivo em outros locais...")
    for alt_path in alternative_paths:
        print(f"Verificando: {alt_path}")
        if os.path.exists(alt_path):
            input_file = alt_path
            print(f"Arquivo encontrado em: {input_file}")
            break
    else:
        # Listar arquivos na pasta Data para debug
        print(f"\nListando arquivos na pasta Data ({data_dir}):")
        if os.path.exists(data_dir):
            files = os.listdir(data_dir)
            for file in files:
                print(f"  - {file}")
        else:
            print("  Pasta Data não existe!")
        
        print("\nListando arquivos na pasta do projeto:")
        if os.path.exists(project_dir):
            files = os.listdir(project_dir)
            for file in files:
                print(f"  - {file}")
        
        print("Arquivo não encontrado em nenhum local. Verifique o nome e localização do arquivo.")
        sys.exit(1)

# Criar pasta Data se não existir
os.makedirs(data_dir, exist_ok=True)

# Carregamento dos dados
df = pd.read_csv(input_file)
print(f"Arquivo carregado de: {input_file}")
print(f"Shape original: {df.shape}")

# Análise exploratória básica
print("\nPrimeiras linhas do dataset:")
print(df.head())

print("\nValores ausentes por coluna:")
print(df.isnull().sum())

print("\nEstatísticas descritivas:")
print(df.describe())

# Limpeza de dados
print("\n" + "=" * 60)
print("LIMPEZA DE DADOS")
print("=" * 60)

# 1. Remover registros com valores ausentes nas colunas essenciais
df_clean = df.dropna(subset=['reclat', 'reclong', 'year', 'mass'])
print(f"Shape após remover nulos: {df_clean.shape}")

# 2. Remover duplicatas
df_clean = df_clean.drop_duplicates()
print(f"Shape após remover duplicatas: {df_clean.shape}")

# 3. Filtrar coordenadas válidas (latitude: -90 a 90, longitude: -180 a 180)
df_clean = df_clean[
    (df_clean['reclat'] >= -90) & (df_clean['reclat'] <= 90) &
    (df_clean['reclong'] >= -180) & (df_clean['reclong'] <= 180)
]
print(f"Shape após filtrar coordenadas válidas: {df_clean.shape}")

# 4. Filtrar registros de 1963 a 2013 (50 anos até 2013)
min_year = 1963
max_year = 2013
df_clean = df_clean[(df_clean['year'] >= min_year) & (df_clean['year'] <= max_year)]
print(f"Shape após filtrar período de {min_year} a {max_year}: {df_clean.shape}")

# Função para determinar país baseado em coordenadas geográficas
def get_country_by_coordinates(lat, lon):
    """
    Determina o país baseado nas coordenadas, com validações geográficas
    """
    # Antártica (latitudes abaixo de -60°)
    if lat < -60:
        return 'Antarctica'
    
    # Ártico/Oceano Ártico (latitudes acima de 75°)
    if lat > 75:
        return 'Arctic Ocean'
    
    # Usar reverse geocoding para outras regiões
    try:
        result = rg.search([(lat, lon)], mode=1, verbose=False)[0]
        country_code = result.get('cc', '')
        
        # Dicionário para converter códigos de país em nomes completos
        country_codes = {
            'US': 'United States', 'CA': 'Canada', 'MX': 'Mexico', 'BR': 'Brazil',
            'AR': 'Argentina', 'CL': 'Chile', 'PE': 'Peru', 'CO': 'Colombia',
            'VE': 'Venezuela', 'UY': 'Uruguay', 'PY': 'Paraguay', 'BO': 'Bolivia',
            'EC': 'Ecuador', 'GY': 'Guyana', 'SR': 'Suriname', 'GF': 'French Guiana',
            'GB': 'United Kingdom', 'FR': 'France', 'DE': 'Germany', 'IT': 'Italy',
            'ES': 'Spain', 'PT': 'Portugal', 'NL': 'Netherlands', 'BE': 'Belgium',
            'CH': 'Switzerland', 'AT': 'Austria', 'SE': 'Sweden', 'NO': 'Norway',
            'DK': 'Denmark', 'FI': 'Finland', 'IS': 'Iceland', 'IE': 'Ireland',
            'PL': 'Poland', 'CZ': 'Czech Republic', 'SK': 'Slovakia', 'HU': 'Hungary',
            'RO': 'Romania', 'BG': 'Bulgaria', 'GR': 'Greece', 'HR': 'Croatia',
            'SI': 'Slovenia', 'RS': 'Serbia', 'BA': 'Bosnia and Herzegovina',
            'ME': 'Montenegro', 'MK': 'North Macedonia', 'AL': 'Albania',
            'RU': 'Russia', 'UA': 'Ukraine', 'BY': 'Belarus', 'LT': 'Lithuania',
            'LV': 'Latvia', 'EE': 'Estonia', 'MD': 'Moldova', 'GE': 'Georgia',
            'AM': 'Armenia', 'AZ': 'Azerbaijan', 'KZ': 'Kazakhstan', 'KG': 'Kyrgyzstan',
            'TJ': 'Tajikistan', 'TM': 'Turkmenistan', 'UZ': 'Uzbekistan',
            'CN': 'China', 'JP': 'Japan', 'KR': 'South Korea', 'KP': 'North Korea',
            'MN': 'Mongolia', 'IN': 'India', 'PK': 'Pakistan', 'BD': 'Bangladesh',
            'LK': 'Sri Lanka', 'NP': 'Nepal', 'BT': 'Bhutan', 'MM': 'Myanmar',
            'TH': 'Thailand', 'VN': 'Vietnam', 'LA': 'Laos', 'KH': 'Cambodia',
            'MY': 'Malaysia', 'SG': 'Singapore', 'ID': 'Indonesia', 'PH': 'Philippines',
            'BN': 'Brunei', 'TL': 'East Timor', 'AU': 'Australia', 'NZ': 'New Zealand',
            'PG': 'Papua New Guinea', 'FJ': 'Fiji', 'SB': 'Solomon Islands',
            'VU': 'Vanuatu', 'NC': 'New Caledonia', 'PF': 'French Polynesia',
            'EG': 'Egypt', 'LY': 'Libya', 'TN': 'Tunisia', 'DZ': 'Algeria',
            'MA': 'Morocco', 'SD': 'Sudan', 'SS': 'South Sudan', 'ET': 'Ethiopia',
            'ER': 'Eritrea', 'DJ': 'Djibouti', 'SO': 'Somalia', 'KE': 'Kenya',
            'UG': 'Uganda', 'TZ': 'Tanzania', 'RW': 'Rwanda', 'BI': 'Burundi',
            'CD': 'Democratic Republic of Congo', 'CG': 'Republic of Congo',
            'CF': 'Central African Republic', 'CM': 'Cameroon', 'TD': 'Chad',
            'NE': 'Niger', 'NG': 'Nigeria', 'BJ': 'Benin', 'TG': 'Togo',
            'GH': 'Ghana', 'CI': 'Ivory Coast', 'LR': 'Liberia', 'SL': 'Sierra Leone',
            'GN': 'Guinea', 'GW': 'Guinea-Bissau', 'SN': 'Senegal', 'GM': 'Gambia',
            'ML': 'Mali', 'BF': 'Burkina Faso', 'MR': 'Mauritania', 'ZA': 'South Africa',
            'NA': 'Namibia', 'BW': 'Botswana', 'ZW': 'Zimbabwe', 'ZM': 'Zambia',
            'MW': 'Malawi', 'MZ': 'Mozambique', 'SZ': 'Eswatini', 'LS': 'Lesotho',
            'MG': 'Madagascar', 'MU': 'Mauritius', 'SC': 'Seychelles', 'KM': 'Comoros',
            'AO': 'Angola', 'GA': 'Gabon', 'GQ': 'Equatorial Guinea', 'ST': 'São Tomé and Príncipe',
            'CV': 'Cape Verde', 'IR': 'Iran', 'IQ': 'Iraq', 'SY': 'Syria',
            'LB': 'Lebanon', 'JO': 'Jordan', 'IL': 'Israel', 'PS': 'Palestine',
            'SA': 'Saudi Arabia', 'YE': 'Yemen', 'OM': 'Oman', 'AE': 'United Arab Emirates',
            'QA': 'Qatar', 'BH': 'Bahrain', 'KW': 'Kuwait', 'TR': 'Turkey',
            'CY': 'Cyprus', 'AF': 'Afghanistan', 'AQ': 'Antarctica',
            'TF': 'French Southern Territories'
        }
        
        if country_code and country_code != '':
            return country_codes.get(country_code, country_code)
        else:
            return None
            
    except Exception as e:
        print(f"Erro na geocodificação para ({lat}, {lon}): {e}")
        return None

# Processar todos os registros limpos para obter países
print("\n" + "=" * 60)
print("PROCESSANDO GEOLOCALIZAÇÃO PARA TODOS OS REGISTROS")
print("=" * 60)

print(f"Processando {len(df_clean)} coordenadas...")

# Aplicar a função de geocodificação
countries = []
valid_indices = []

for idx, row in df_clean.iterrows():
    lat, lon = row['reclat'], row['reclong']
    country = get_country_by_coordinates(lat, lon)
    
    if country:
        countries.append(country)
        valid_indices.append(idx)

print(f"Total de registros com país identificado: {len(valid_indices)}")
print(f"Total de registros sem país identificado: {len(df_clean) - len(valid_indices)}")

# Filtrar apenas os registros com país identificado
df_final = df_clean.loc[valid_indices].copy()
df_final['country'] = countries

print(f"Tamanho da base final: {len(df_final)}")

# Mostrar alguns exemplos dos países identificados
print(f"\nExemplos de países identificados:")
print(df_final['country'].value_counts().head(15))

# Adicionar categorização de massa
def categorize_mass(mass):
    if mass < 10:
        return 'Pequeno'
    elif mass < 100:
        return 'Médio'
    elif mass < 1000:
        return 'Grande'
    else:
        return 'Muito Grande'

df_final['mass_category'] = df_final['mass'].apply(categorize_mass)

# Salvar a base final na pasta Data
df_final.to_csv(output_file, index=False)
print(f"\nBase final salva com sucesso em: {output_file}")
print(f"Total de registros na base final: {len(df_final)}")
print(f"Todos os {len(df_final)} registros têm país identificado.")
print(f"Período dos dados: {min_year} a {max_year}")
