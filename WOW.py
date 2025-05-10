import itertools

def gerar_combinacoes_letras(letras, tamanho=None):
    """
    Gera todas as combinações possíveis de letras.
    
    Args:
        letras (str): String contendo as letras a serem combinadas
        tamanho (int, optional): Tamanho específico das combinações. 
                                Se None, gera combinações de todos os tamanhos possíveis.
    
    Returns:
        list: Lista com todas as combinações possíveis
    """
    todas_combinacoes = []
    
    if tamanho is not None:
        # Gerar combinações de um tamanho específico
        combinacoes = itertools.combinations(letras, tamanho)
        for combo in combinacoes:
            todas_combinacoes.append(''.join(combo))
    else:
        # Gerar combinações de todos os tamanhos possíveis (de 1 até o número total de letras)
        for i in range(1, len(letras) + 1):
            combinacoes = itertools.combinations(letras, i)
            for combo in combinacoes:
                todas_combinacoes.append(''.join(combo))
    
    return todas_combinacoes

def gerar_permutacoes_letras(letras, tamanho=None):
    """
    Gera todas as permutações possíveis de letras.
    
    Args:
        letras (str): String contendo as letras a serem permutadas
        tamanho (int, optional): Tamanho específico das permutações.
                               Se None, gera permutações de todos os tamanhos possíveis.
    
    Returns:
        list: Lista com todas as permutações possíveis
    """
    todas_permutacoes = []
    
    if tamanho is not None:
        # Gerar permutações de um tamanho específico
        permutacoes = itertools.permutations(letras, tamanho)
        for perm in permutacoes:
            todas_permutacoes.append(''.join(perm))
    else:
        # Gerar permutações de todos os tamanhos possíveis (de 1 até o número total de letras)
        for i in range(1, len(letras) + 1):
            permutacoes = itertools.permutations(letras, i)
            for perm in permutacoes:
                todas_permutacoes.append(''.join(perm))
    
    return todas_permutacoes

# Exemplo de uso
if __name__ == "__main__":
    # Input do usuário
    letras_input = input("Digite as letras que deseja combinar: ")
    tipo_operacao = input("Deseja gerar [1] Combinações (ordem não importa) ou [2] Permutações (ordem importa)? ")
    
    tamanho_especifico = input("Deseja gerar combinações de um tamanho específico? (S/N): ")
    if tamanho_especifico.upper() == "S":
        tamanho = int(input("Digite o tamanho desejado: "))
    else:
        tamanho = None
    
    # Remove espaços e caracteres duplicados
    letras = ''.join(dict.fromkeys(letras_input.replace(" ", "")))
    
    print(f"\nUsando letras: {letras}")
    
    if tipo_operacao == "1":
        resultado = gerar_combinacoes_letras(letras, tamanho)
        print(f"\nGeradas {len(resultado)} combinações:")
    else:
        resultado = gerar_permutacoes_letras(letras, tamanho)
        print(f"\nGeradas {len(resultado)} permutações:")
    
    # Exibir resultados
    for i, item in enumerate(resultado, 1):
        print(f"{i}. {item}")
    
    print(f"\nTotal de resultados: {len(resultado)}")