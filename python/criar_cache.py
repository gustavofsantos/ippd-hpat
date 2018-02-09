import os
import json
import time
from functools import lru_cache

class Pacote:
    def __init__(self, nome, descricao, palavras_chave, dependencias):
        self.nome = nome
        self.descricao = descricao
        self.palavras_chave = palavras_chave
        self.dependencias = dependencias

    def str_palavras_chave(self):
        if self.palavras_chave:
            return ','.join(self.palavras_chave)
        else:
            return ''


print("[{}] INICIO".format(time.asctime()[11:19]))

print("[{}] LISTANDO DIRETORIO".format(time.asctime()[11:19]))
nome_arquivos = os.listdir('pacotes')

print("[{}] CRIANDO GRAFO".format(time.asctime()[11:19]))
pacotes = {}

# carregar todos os arquivos para a memória
@lru_cache(maxsize=2048)
def ler_arquivos():
    global nome_arquivos
    global pacotes
    for i, arquivo in enumerate(nome_arquivos):
        print("[{}] - {} - Processando {}...".format(time.asctime()[11:19], str(i).ljust(6, ' '), arquivo), end='\r')
        try:
            with open('./../pacotes/{}'.format(arquivo), encoding='utf8') as arq_json:
                obj_json = json.loads(arq_json.read())
                nome = obj_json.get("name", None)
                descricao = obj_json.get("description", None)

                dependencias = obj_json.get("dependencies", None)
                dependencias = list(dependencias.keys()) if dependencias != None else None

                dependencias_dev = obj_json.get("devDependencies", None)
                dependencias_dev = list(dependencias_dev.keys()) if dependencias_dev != None else None

                if dependencias != None:
                    if dependencias_dev != None:
                        dependencias += dependencias_dev


                palavras_chave = obj_json.get("keywords", None)

                # cria o objeto pacote
                pacote = Pacote(nome, descricao, palavras_chave, dependencias)

                # cria uma entrada para o pacote na relação de pacotes
                pacotes[nome] = pacote

        except FileNotFoundError as e:
            print('\n[{}] - {} NÃO ENCONTRADO PELO SISTEMA OPERACIONAL.'.format(time.asctime()[11:19], arquivo))
        except Exception as e:
            print('\n[{}] - {} ERRO NO PROCESSAMENTO.'.format(time.asctime()[11:19], arquivo))

ler_arquivos()

print("[{}] FIM DO PROCESSAMENTO DOS ARQUIVOS.".format(time.asctime()[11:19]))

#----------------------------------------------------------------------------#

rank = {}
chaves = pacotes.keys()

@lru_cache(maxsize=2048)
def calc_rank():
    global chaves
    global rank 
    for chave in chaves:
        print("{} -> {}".format(chave, pacotes[chave].dependencias))
        entradas_rank = rank.keys()
        if not chave in entradas_rank:
            # se a chave ainda não está no rank, cria a entrada para ela
            rank[chave] = 0

        # checa as dependencias do pacote e analisa de quem este pacote depende
        dependencias = pacotes[chave].dependencias
        if dependencias:
            for dependencia in pacotes[chave].dependencias:
                # checa se a dependencia já está no rank, se estiver incrementa o seu rank
                # pois o pacote depende dela
                if dependencia in entradas_rank:
                    rank[dependencia] += 1 # incrementa o rank da dependencia
                else:
                    # senão cria a entrada no rank
                    rank[dependencia] = 1
                    # analisa os outros quesitos do ranqueamento
                    # todo: implementar outros quesitos de ranqueamento


print("[{}] INICIO DO PROCESSAMENTO DO RANK.".format(time.asctime()[11:19]))

calc_rank()

print("[{}] FIM DO PROCESSAMENTO DO RANK.".format(time.asctime()[11:19]))

#----------------------------------------------------------------------------#

print("[{}] INICIO DO PROCESSO DE SALVAR O CACHE DE PESQUISA.".format(time.asctime()[11:19]))

# salva da seguinte forma:
# nome do pacote; palavras chaves referente a este pacote; descrição deste pacote; rank deste pacote
entradas = pacotes.keys()
with open('./../cache/pacotes.rank.dat', 'w') as arq_cache:
    for pacote in entradas:
        arq_cache.write("{};{};{};{}\n".format(pacotes[pacote].nome, 
            pacotes[pacote].str_palavras_chave(),
            pacotes[pacote].descricao,
            rank[pacote]))

print("[{}] FIM DO PROCESSO DE SALVAR O CACHE DE PESQUISA.".format(time.asctime()[11:19]))
