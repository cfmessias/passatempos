import streamlit as st
import requests
import itertools

tabs = st.tabs(["Cruzadas", "Sinonimos","WOW"])

with tabs[0]:
    def obter_sinonimos(palavra, num_letras=None):
        url = "https://api.datamuse.com/words"
        params = {"rel_syn": palavra, "max": 50}
        resposta = requests.get(url, params=params)
        if resposta.status_code == 200:
            lista = [item["word"] for item in resposta.json()]
            if num_letras:
                lista = [w for w in lista if len(w) == num_letras]
            return lista
        return []

    def obter_relacionadas(palavra, num_letras=None):
        url = "https://api.datamuse.com/words"
        params = {"ml": palavra, "max": 50}
        resposta = requests.get(url, params=params)
        if resposta.status_code == 200:
            lista = [item["word"] for item in resposta.json()]
            if num_letras:
                lista = [w for w in lista if len(w) == num_letras]
            return lista
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
    num_letras = st.number_input("Número de letras esperado (opcional):", min_value=1, max_value=30, step=1, format="%d", value=None)

    if palavra:
        st.markdown(f"### 🔍 Resultados para: `{palavra}`")
        
        definicoes = obter_definicoes(palavra)
        if definicoes:
            st.subheader("📘 Definições")
            for d in definicoes:
                st.markdown(f"- {d}")

        sinonimos = obter_sinonimos(palavra, num_letras)
        if sinonimos:
            st.subheader("🟢 Sinónimos")
            st.markdown(", ".join(sinonimos))

        relacionadas = obter_relacionadas(palavra, num_letras)
        if relacionadas:
            st.subheader("🔵 Palavras relacionadas")
            st.markdown(", ".join(relacionadas))

        if not (definicoes or sinonimos or relacionadas):
            st.warning("⚠️ Nenhuma informação encontrada.")

        
with tabs[1]:
    def obter_sinonimos(palavra):
        url = "https://api.datamuse.com/words"
        params = {
            "rel_syn": palavra,
            "max": 10
        }
        resposta = requests.get(url, params=params)

        if resposta.status_code == 200:
            dados = resposta.json()
            return [item["word"] for item in dados]
        else:
            st.error(f"Erro ao aceder à API: {resposta.status_code}")
            return []

    # Interface Streamlit
    st.title("Descobre Sinónimos")
    st.write("Insere uma palavra para obter possíveis sinónimos (via Datamuse API).")

    palavra = st.text_input("Palavra:", "")

    if st.button("Procurar Sinónimos"):
        if palavra.strip() != "":
            sinonimos = obter_sinonimos(palavra.strip())
            if sinonimos:
                st.success(f"Sinónimos de '{palavra}':")
                st.write(", ".join(sinonimos))
            else:
                st.warning("Nenhum sinónimo encontrado.")
        else:
            st.warning("Por favor, insere uma palavra válida.")
        
    with tabs[2]:
        
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

        def gerar_palavras_validas(letras, tamanho):
            """Gera permutações com letras repetidas e filtra por palavras reais"""
            letras = letras.lower()
            todas = set(''.join(p) for p in itertools.permutations(letras, tamanho))
            palavras_validas = [p for p in todas if validar_palavra(p)]
            return palavras_validas

        # Interface Streamlit
        st.title("🧩 Gerador de Palavras Válidas com Letras Repetidas")
        letras_input = st.text_input("Insere letras (pode repetir):", value="rarroc")

        if letras_input:
            tamanho = st.number_input("Tamanho da palavra:", min_value=1, max_value=len(letras_input), step=1)

            if st.button("🔍 Gerar Palavras"):
                st.info("A procurar palavras válidas...")
                resultado = gerar_palavras_validas(letras_input, tamanho)
                
                if resultado:
                    st.success(f"Encontradas {len(resultado)} palavra(s):")
                    st.markdown(", ".join(sorted(resultado)))
                else:
                    st.warning("Nenhuma palavra real encontrada com essas letras.")

