import sys
import time
import operator
import subprocess
from functools import lru_cache


print("[{}] INICIO".format(time.asctime()[11:19]))

@lru_cache(maxsize=524288)
def pesquisar(termos, numero_itens):
    pacotes = {}
    linhas_relacionadas = []
    try:
        with open('./../cache/pacotes.rank.dat', encoding='utf8') as cache:
            linhas = cache.readlines()
            # percorre todas as linhas e forma uma nova lista
            # com os pacotes que tem alguma relação com a pesquisa
            for linha in linhas:
                linha = linha[0:-1] if linha[-1] == '\n' else linha # dropa o \n
                set_termos = set(termos.split(' '))
                set_linha = set(linha.split(';'))


                # testa se há alguma relação entre os termpos pesquisados
                # e a linha em questão
                existe_relacao = False
                for termo in set_termos:
                    if len(linha.split(';')) >= 2:
                        if termo in linha.split(';')[0] or termo in linha.split(';')[1]:
                            existe_relacao = True

                if existe_relacao:
                    linhas_relacionadas.append(linha)

            for linha in linhas_relacionadas:
                linha_split = linha.split(';')

                if len(linha_split) >= 4:
                    nome = linha_split[0]
                    lista_pal_chave = linha_split[1]
                    if len(linha_split) > 4:
                        descricao = ' '.join(linha_split[2:-1])
                        rank = int(linha_split[-1]) if linha_split[-1].isdecimal() else 0
                    else:
                        descricao = linha_split[2]
                        rank = int(linha_split[3]) if linha_split[3].isdecimal() else 0


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

                    pacotes.update({nome: rank})
                else:
                    pass

        pacotes_ordenados = sorted(pacotes.items(), key=operator.itemgetter(1), reverse=True)
        return pacotes_ordenados[0:numero_itens]
    except FileNotFoundError as e:
        print("[{}] CACHE NÃO ENCONTRADO".format(time.asctime()[11:19]))
        print("[{}] EXECUTANDO O PROCESSO DE CRIAÇÃO DE CACHE".format(time.asctime()[11:19]))
        subprocess.run(['python', 'criar-grafo.py'])
        pesquisar(termos)

def main():
    pesq = ' '.join(sys.argv[1:])

    print("[{}] PESQUISANDO POR: '{}'".format(time.asctime()[11:19], pesq))

    print("[{}] PROCESSANDO PESQUISA".format(time.asctime()[11:19]))

    resultado = pesquisar(pesq, 10)

    print("[{}] RESULTADOS DA PESQUISA".format(time.asctime()[11:19]))
    for pacote in resultado:
        print('[ {} ]'.format(pacote))

    print("[{}] FIM".format(time.asctime()[11:19]))

if __name__ == '__main__':
    main()