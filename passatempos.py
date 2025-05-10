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
        
        st.title("🔠 Gerador de Combinações e Permutações de Letras")

        letras_input = st.text_input("Digite as letras que deseja usar:", max_chars=20)
        tipo_operacao = st.radio("Tipo de operação:", ["Combinações (ordem não importa)", "Permutações (ordem importa)"])

        usar_tamanho_especifico = st.checkbox("Usar tamanho específico")
        if usar_tamanho_especifico:
            tamanho = st.number_input("Tamanho das combinações/permuntações:", min_value=1, max_value=len(letras_input), step=1)
        else:
            tamanho = None

        def gerar_combinacoes_letras(letras, tamanho=None):
            todas_combinacoes = []
            if tamanho is not None:
                combinacoes = itertools.combinations(letras, tamanho)
                todas_combinacoes = [''.join(c) for c in combinacoes]
            else:
                for i in range(1, len(letras) + 1):
                    combinacoes = itertools.combinations(letras, i)
                    todas_combinacoes.extend(''.join(c) for c in combinacoes)
            return todas_combinacoes

        def gerar_permutacoes_letras(letras, tamanho=None):
            todas_permutacoes = []
            if tamanho is not None:
                permutacoes = itertools.permutations(letras, tamanho)
                todas_permutacoes = [''.join(p) for p in permutacoes]
            else:
                for i in range(1, len(letras) + 1):
                    permutacoes = itertools.permutations(letras, i)
                    todas_permutacoes.extend(''.join(p) for p in permutacoes)
            return todas_permutacoes

        if letras_input:
            letras = ''.join(dict.fromkeys(letras_input.replace(" ", "")))
            st.markdown(f"**Letras únicas consideradas:** {letras}")

            if tipo_operacao.startswith("Combina"):
                resultado = gerar_combinacoes_letras(letras, tamanho)
                st.success(f"Foram geradas {len(resultado)} combinações.")
            else:
                resultado = gerar_permutacoes_letras(letras, tamanho)
                st.success(f"Foram geradas {len(resultado)} permutações.")

            st.write("### Resultados:")
            for i, item in enumerate(resultado, 1):
                st.write(f"{i}. {item}")
