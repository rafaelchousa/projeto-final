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
