import requests

def obter_sinonimos(palavra):
    url = "https://api.datamuse.com/words"
    params = {
        "rel_syn": palavra,  # sinónimos
        "max": 10  # número máximo de resultados
    }
    resposta = requests.get(url, params=params)
    
    if resposta.status_code == 200:
        dados = resposta.json()
        return [item["word"] for item in dados]
    else:
        print(f"Erro ao aceder à API: {resposta.status_code}")
        return []

# Exemplo de uso
palavras = ["feliz", "rápido", "inteligente"]

for palavra in palavras:
    sinonimos = obter_sinonimos(palavra)
    print(f"Sinónimos de '{palavra}': {', '.join(sinonimos) if sinonimos else 'Nenhum encontrado.'}")
