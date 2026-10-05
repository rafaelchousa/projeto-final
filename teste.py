import mysql.connector

# ==========================================
# FUNÇÃO DE CONEXÃO E CONSULTA 
# ==========================================
def obter_dados_do_banco(query):
    try:
        conexao = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="spotify"
        )
        cursor = conexao.cursor()
        cursor.execute(query)
        resultados = cursor.fetchall()
        return resultados
    except mysql.connector.Error as erro:
        print(f"Erro ao conectar ao MySQL: {erro}")
        return None
    finally:
        if 'conexao' in locals() and conexao.is_connected():
            cursor.close()
            conexao.close()


# ==========================================
# CONSULTA 1 - Top 10 artistas por popularidade média
# ==========================================
print("\n=== CONSULTA 1: Top 10 artistas por popularidade média ===")
q1 = """
SELECT artist_name, ROUND(AVG(popularity), 2) AS media_popularidade
FROM tracks
GROUP BY artist_name
ORDER BY media_popularidade DESC
LIMIT 10;
"""
resultado = obter_dados_do_banco(q1)
if resultado:
    for linha in resultado:
        print(linha)


# ==========================================
# CONSULTA 2 - Top 5 gêneros por total de streams
# ==========================================

print("\n=== CONSULTA 2: Top 5 gêneros por total de streams ===")
q2 = """
SELECT genre, SUM(stream_count) AS total_streams
FROM tracks
GROUP BY genre
ORDER BY total_streams DESC
LIMIT 5;
"""
resultado = obter_dados_do_banco(q2)
if resultado:
    for linha in resultado:
        print(linha)


# ==========================================
# CONSULTA 3 - Danceability média por gênero
# ==========================================
print("\n=== CONSULTA 3: Danceability média por gênero ===")
q3a = """
SELECT genre, ROUND(AVG(danceability), 3) AS media_danceability
FROM tracks
GROUP BY genre
ORDER BY media_danceability DESC;
"""
resultado = obter_dados_do_banco(q3a)
if resultado:
    for linha in resultado:
        print(linha)


# ==========================================
# CONSULTA 4 - Energy média por gênero
# ==========================================
print("\n=== CONSULTA 4: Energy média por gênero ===")
q3b = """
SELECT genre, ROUND(AVG(energy), 3) AS media_energy
FROM tracks
GROUP BY genre
ORDER BY media_energy DESC;
"""
resultado = obter_dados_do_banco(q3b)
if resultado:
    for linha in resultado:
        print(linha)
# ==========================================
# CONSULTA 5 - Top 10 músicas mais tocadas 
# ==========================================
print("\n=== CONSULTA 5: Top 10 músicas mais tocadas ===")
q5 = """
SELECT track_name, artist_name, stream_count
FROM tracks
ORDER BY stream_count DESC
LIMIT 10;
"""
resultado = obter_dados_do_banco(q5)
if resultado:
    for linha in resultado:
        print(linha)
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Configuração visual dos gráficos
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)

# -------------------------------------------------------------------------
# 1. CARREGAMENTO DOS DADOS
# -------------------------------------------------------------------------
try:
    df = pd.read_csv('spotify_2015_2025_85k.csv')
    print("Dados carregados com sucesso!")
except FileNotFoundError:
    print("Erro: Verifique o caminho do arquivo 'spotify_2015_2025_85k.csv'.")
    exit()

# Selecionando a variável quantitativa para a análise
dados_streams = df['stream_count']

# =========================================================================
# 2. MEDIDAS DE TENDÊNCIA CENTRAL
# =========================================================================
media_streams = np.mean(dados_streams)
mediana_streams = np.median(dados_streams)

# Distância entre a média e a mediana
distancia_media_mediana = (media_streams - mediana_streams) / mediana_streams

print("\n" + "="*60)
print("ANÁLISE DE TENDÊNCIA CENTRAL - STREAMS")
print("="*60)
print(f"Média: {media_streams:.2f}")
print(f"Mediana: {mediana_streams:.2f}")
print(f"Distância entre Média e Mediana: {distancia_media_mediana * 100:.2f}%")

if abs(distancia_media_mediana) <= 0.10:
    print("-> A média tende a ser uma medida de tendência central confiável.")
elif abs(distancia_media_mediana) < 0.25:
    print("-> A média pode estar sofrendo influência moderada de valores extremos.")
else:
    print("-> A média tende a NÃO ser uma medida de tendência central confiável.")

if media_streams > mediana_streams:
    print("-> A influência é dos valores mais altos da distribuição.")
elif media_streams < mediana_streams:
    print("-> A influência é dos valores mais baixos da distribuição.")

# =========================================================================
# 3. MEDIDAS DE DISPERSÃO
# =========================================================================
variancia_streams = np.var(dados_streams, ddof=0)
desvio_padrao_streams = np.std(dados_streams, ddof=0)
cv_streams = (desvio_padrao_streams / media_streams) * 100
distancia_variancia_media = variancia_streams / (media_streams ** 2)

print("\n" + "="*60)
print("ANÁLISE DE DISPERSÃO - STREAMS")
print("="*60)
print(f"Variância: {variancia_streams:.2f}")
print(f"Desvio Padrão: {desvio_padrao_streams:.2f}")
print(f"Coeficiente de Variação (CV): {cv_streams:.2f}%")
print(f"Distância da Variância / Média²: {distancia_variancia_media:.2f}")

if distancia_variancia_media <= 0.10:
    print("-> Baixa dispersão dos dados em relação à média.")
elif distancia_variancia_media < 0.25:
    print("-> Dispersão moderada dos dados em relação à média.")
else:
    print("-> Alta dispersão dos dados em relação à média.")

# =========================================================================
# 4. FORMATO DA DISTRIBUIÇÃO (ASSIMETRIA E CURTOSE)
# =========================================================================
assimetria_streams = dados_streams.skew()
curtose_excesso_streams = dados_streams.kurtosis()
curtose_real_streams = curtose_excesso_streams + 3

print("\n" + "="*60)
print("ANÁLISE DE ASSIMETRIA E CURTOSE - STREAMS")
print("="*60)
print(f"Assimetria: {assimetria_streams:.4f}")

if -0.5 <= assimetria_streams <= 0.5:
    print("-> Simétrica (ou Quase Simétrica). Média e Mediana são próximas.")
elif assimetria_streams > 0.5:
    print("-> Assimétrica Positiva (à Direita). Média > Mediana. Cauda se estende para valores maiores.")
else:
    print("-> Assimétrica Negativa (à Esquerda). Média < Mediana. Cauda se estende para valores menores.")

print(f"Curtose (Real, Ref. 3.0): {curtose_real_streams:.4f}")

if 2.5 <= curtose_real_streams <= 3.5:
    print("-> Mesocúrtica. Distribuição próxima da normal.")
elif curtose_real_streams < 2.5:
    print("-> Platicúrtica. Dados mais dispersos, caudas finas e outliers comuns.")
else:
    print("-> Leptocúrtica. Dados extremamente concentrados no centro e caudas pesadas. Outliers muito comuns.")

# =========================================================================
# 5. IDENTIFICAÇÃO DE OUTLIERS (IQR)
# =========================================================================
Q1 = np.percentile(dados_streams, 25)
Q3 = np.percentile(dados_streams, 75)
IQR = Q3 - Q1

limite_superior = Q3 + (1.5 * IQR)
limite_inferior = Q1 - (1.5 * IQR)

print("\n" + "="*60)
print("IDENTIFICAÇÃO DE OUTLIERS - STREAMS")
print("="*60)
print(f"Q1 (25%): {Q1:.2f}")
print(f"Q3 (75%): {Q3:.2f}")
print(f"IQR: {IQR:.2f}")
print(f"Limite Superior (LS): {limite_superior:.2f}")
print(f"Limite Inferior (LI): {limite_inferior:.2f}")

outliers_superiores = df[df['stream_count'] > limite_superior]
outliers_inferiores = df[df['stream_count'] < abs(limite_inferior)]

print(f"\nTotal de Outliers Superiores: {len(outliers_superiores)} músicas")
print(outliers_superiores[['track_name', 'artist_name', 'stream_count']].sort_values(by='stream_count', ascending=False).head(5))

print(f"\nTotal de Outliers Inferiores: {len(outliers_inferiores)} músicas")
if len(outliers_inferiores) > 0:
    print(outliers_inferiores[['track_name', 'stream_count']].sort_values(by='stream_count', ascending=True).head(5))
else:
    print("Não houve outliers inferiores (comportamento esperado para contagem de streams).")

# =========================================================================
# 6. VISUALIZAÇÕES
# =========================================================================

# 6.1 Boxplot
plt.figure(figsize=(10, 4))
sns.boxplot(x=dados_streams, color='skyblue')
plt.title('Boxplot da Distribuição de Streams')
plt.xlabel('Streams')
plt.tight_layout()
plt.show()

# 6.2 Top 10 Outliers Superiores
top_10_outliers = outliers_superiores.sort_values(by='stream_count', ascending=False).head(10)

if not top_10_outliers.empty:
    plt.figure(figsize=(12, 5))
    sns.barplot(x='track_name', y='stream_count', data=top_10_outliers, palette='Reds_r')
    plt.title('Top 10 Músicas com Mais Streams (Outliers Superiores)')
    plt.xlabel('Música')
    plt.ylabel('Streams')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

# 6.3 Histograma com KDE
plt.figure(figsize=(12, 6))
sns.histplot(dados_streams, kde=True, bins=50, color='skyblue', edgecolor='black', stat='density')

plt.axvline(media_streams, color='red', linestyle='--', label=f'Média: {media_streams:.2f}')
plt.axvline(mediana_streams, color='green', linestyle=':', label=f'Mediana: {mediana_streams:.2f}')

plt.text(0.95, 0.95, f'Assimetria: {assimetria_streams:.2f}', transform=plt.gca().transAxes,
         fontsize=10, verticalalignment='top', horizontalalignment='right',
         bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.5))
plt.text(0.95, 0.88, f'Curtose (Real): {curtose_real_streams:.2f}', transform=plt.gca().transAxes,
         fontsize=10, verticalalignment='top', horizontalalignment='right',
         bbox=dict(boxstyle='round,pad=0.5', fc='lightgreen', alpha=0.5))

plt.title('Distribuição dos Streams (Histograma com KDE)', fontsize=14)
plt.xlabel('Streams', fontsize=12)
plt.ylabel('Densidade', fontsize=12)
plt.legend()
plt.grid(axis='y', alpha=0.75)
plt.tight_layout()
plt.show()