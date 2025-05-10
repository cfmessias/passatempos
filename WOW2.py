import streamlit as st
import itertools

st.set_page_config(page_title="Gerador de Combinações e Permutações", layout="centered")

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
