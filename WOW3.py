import streamlit as st
import itertools
import requests

def validar_palavra(palavra):
    """Verifica se a palavra existe na língua (via API Datamuse)"""
    url = "https://api.datamuse.com/words"
    params = {"sp": palavra, "max": 1}
    resposta = requests.get(url, params=params)
    if resposta.status_code == 200:
        resultados = resposta.json()
        return any(item["word"] == palavra for item in resultados)
    return False

def palavra_respeita_molde(palavra, molde):
    """Verifica se a palavra cumpre o molde (letras nas posições corretas)"""
    return all(m == "_" or m == p for m, p in zip(molde, palavra))

def gerar_palavras_validas(letras, tamanho, molde=None):
    """Gera permutações e filtra por molde e por palavras reais"""
    letras = letras.lower()
    todas = set(''.join(p) for p in itertools.permutations(letras, tamanho))
    
    # Filtra por molde se fornecido
    if molde:
        molde = molde.lower()
        todas = [p for p in todas if palavra_respeita_molde(p, molde)]

    # Verifica se são palavras reais
    palavras_validas = [p for p in todas if validar_palavra(p)]
    return palavras_validas

# Interface Streamlit
st.title("🧩 Gerador de Palavras Válidas com Letras Repetidas")

letras_input = st.text_input("Insere letras (pode repetir):", value="rarroc")

if letras_input:
    tamanho = st.number_input("Tamanho da palavra:", min_value=1, max_value=len(letras_input), step=1)
    
    molde = st.text_input("Molde da palavra (usa '_' para desconhecidos):", value="_" * tamanho)
    
    if len(molde) != tamanho:
        st.warning("O molde deve ter o mesmo número de letras indicado no tamanho.")
    elif st.button("🔍 Gerar Palavras"):
        st.info("A procurar palavras válidas...")
        resultado = gerar_palavras_validas(letras_input, tamanho, molde)
        
        if resultado:
            st.success(f"Encontradas {len(resultado)} palavra(s):")
            st.markdown(", ".join(sorted(resultado)))
        else:
            st.warning("Nenhuma palavra real encontrada com essas letras e molde.")
