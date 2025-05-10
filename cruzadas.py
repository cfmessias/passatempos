import streamlit as st
import requests

def obter_sinonimos(palavra):
    url = "https://api.datamuse.com/words"
    params = {"rel_syn": palavra, "max": 10}
    resposta = requests.get(url, params=params)
    if resposta.status_code == 200:
        return [item["word"] for item in resposta.json()]
    return []

def obter_relacionadas(palavra):
    url = "https://api.datamuse.com/words"
    params = {"ml": palavra, "max": 10}
    resposta = requests.get(url, params=params)
    if resposta.status_code == 200:
        return [item["word"] for item in resposta.json()]
    return []

def obter_definicoes(palavra):
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{palavra}"
    resposta = requests.get(url)
    if resposta.status_code == 200:
        try:
            dados = resposta.json()
            definicoes = []
            for sentido in dados[0]['meanings']:
                for definicao in sentido['definitions']:
                    definicoes.append(definicao['definition'])
            return definicoes[:3]
        except Exception:
            return []
    return []

# Interface do Streamlit
st.title("🔠 Ajuda para Palavras Cruzadas")
palavra = st.text_input("Insere uma palavra ou pista curta:")

if palavra:
    st.markdown(f"### 🔍 Resultados para: `{palavra}`")

    definicoes = obter_definicoes(palavra)
    if definicoes:
        st.subheader("📘 Definições")
        for d in definicoes:
            st.markdown(f"- {d}")

    sinonimos = obter_sinonimos(palavra)
    if sinonimos:
        st.subheader("🟢 Sinónimos")
        st.markdown(", ".join(sinonimos))

    relacionadas = obter_relacionadas(palavra)
    if relacionadas:
        st.subheader("🔵 Palavras relacionadas")
        st.markdown(", ".join(relacionadas))

    if not (definicoes or sinonimos or relacionadas):
        st.warning("⚠️ Nenhuma informação encontrada.")
