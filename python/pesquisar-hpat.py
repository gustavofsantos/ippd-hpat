import hpat
import numba
import sys
import time
import operator
import subprocess

from functools import lru_cache


"""
Suporte de strings:
    ==, !=, split, concatenação e acesso a posicao (i.é. str[i])
-----------------
Suporte de operações paralelas:
    hpat.prange
-----------------
Otimização automática:
    - hpat.jit (sujeito as restrições de implementação)


Operações fora do suporte do hpat utilizam as construções do
próprio Python sem otimizações.
"""


print("[{}] INICIO".format(time.asctime()[11:19]))

@lru_cache(maxsize=4096)
def ler_cache():
    """
    Carrega o arquivo de cache na memória e retorna uma lista
    de entradas no cache.
    """
    with open('./../cache/pacotes.rank.dat', 'r', encoding='utf8') as cache:
        lcache = cache.readlines()
        fcache = []
        for i in hpat.prange(len(lcache)):
            linha = lcache[i][0:-1] if lcache[i][-1] == '\n' else lcache[i] # dropa o \n
            fcache.append(linha)
        
        return fcache
    return []


@hpat.jit(nopython=False)
def existe_relacao(termos, linha):
    """
    Checa se uma linha têm alguma relação com os termos de pesquisa
    --------
    Retorna True se existir alguma correspondência dos termos de pesquisa
    no nome ou nas palavras chave do pacote. Retorna False caso contrário.
    """
    linha_split = linha.split(';')
    termo_split = termos.split(' ')
    for termo in termo_split:
        if len(linha_split) >= 2:
            if termo in linha_split[0] or termo in linha_split[1]:
                return True
    return False

@hpat.jit(nopython=False)
def extrair_info_linha(linha_split):
    nome = linha_split[0]
    lista_pal_chave = linha_split[1]
    if len(linha_split) > 4:
        descricao = ' '.join(linha_split[2:-1]) # sem a flag nopython=False não funciona
                                                # numba não implementa o str.join
        rank = int(linha_split[-1]) if len(linha_split[-1]) > 0 else 0
    else:
        descricao = linha_split[2]
        rank = int(linha_split[3]) if len(linha_split[3]) > 0 else 0

    return [nome, lista_pal_chave, descricao, rank]

@hpat.jit(nopython=False)
def calc_rank(termos, linha):
    """
    Calcula o ranqueamento de um pacote baseado nos termos de pesquisa.

    Retorna o nome do pacote e o rank do pacote.
    """
    linha_split = linha.split(';')

    nome = ''
    rank = 0.0
    if len(linha_split) >= 4:
        nome, lista_pal_chave, descricao, rank = extrair_info_linha(linha_split)

        # ranqueamento
        for termo in termos.split(' '):
            if termo in nome:
                rank = rank + rank*0.9
            else:
                rank = rank - rank*0.9
            if termo in lista_pal_chave:
                rank = rank + rank*0.6
            else:
                rank = rank - rank*0.1
            if termo in descricao:
                rank = rank + rank*0.4
            else:
                rank = rank - rank*0.1
        
    return (nome, rank)

#@hpat.jit(nopython=False)
def pesquisar(termos, numero_itens, linhas):
    pacotes = {}

    linhas_relacionadas = [ linhas[i] 
        for i in hpat.prange(len(linhas)) 
            if existe_relacao(termos, linhas[i]) ]

    for i in hpat.prange(len(linhas_relacionadas)):
        res = calc_rank(termos, linhas_relacionadas[i])
        if res:
            nome, rank = res
            pacotes.update({nome: rank})


    if len(pacotes) > 0:
        pacotes_ordenados = sorted(pacotes.items(), key=operator.itemgetter(1), reverse=True)
        pacotes_ordenados = pacotes_ordenados[0:numero_itens]
        return pacotes_ordenados
    else:
        pacotes_ordenados = []
        return pacotes_ordenados


def main():
    print("[{}] PROCESSANDO PESQUISA".format(time.asctime()[11:19]))

    pesq = ' '.join(sys.argv[1:])

    cache = ler_cache()
    if len(cache) > 0:
        resultado = pesquisar(pesq, 10, cache)

        print("[{}] RESULTADOS DA PESQUISA".format(time.asctime()[11:19]))
        if resultado:
            for pacote in resultado:
                print('[ {} ]'.format(pacote))
        else:
            print('Nenhum resultado encontrado.')

        print("[{}] FIM".format(time.asctime()[11:19]))
    else:
        print('cache não encontrado.')


if __name__ == '__main__':
    main()
