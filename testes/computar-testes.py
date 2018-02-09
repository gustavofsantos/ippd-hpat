import time
import subprocess
import os
import resource
import sys
from timeit import timeit


sys.path.insert(0, './../python')
from pesquisar import pesquisar

pesquisas = ['browserify', 'grunt-cli', 'bower', 'gulp', 'grunt', 'express', 'npm', 'cordova', 'forever']


def memory_usage_resource():
    rusage_denom = 1024.
    mem = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / rusage_denom
    return mem

def criar_csv_medidas_tempo_mem(num_medidas_por_vez):
    global pesquisas

    medidas = {}
    medidas_mem = {}
    
    for medida in range(num_medidas_por_vez):
        print(medida)
        tempos_exec = []
        mems_exec = []
        for pesquisa in pesquisas:

            t_a = time.time()
            resultados = pesquisar(pesquisa, 10)
            t_d = time.time()
            dif_t = t_d - t_a
            mem = memory_usage_resource()

            if medida == 0:
                medidas[pesquisa] = [dif_t]
                medidas_mem[pesquisa] = [mem]
            else:
                medidas[pesquisa].append(dif_t)
                medidas_mem[pesquisa].append(mem)
            
            print(resultados)

    with open('criar_csv_medidas_tempo.csv', 'w') as saida:
        saida.write('Termo')
        for i in range(num_medidas_por_vez):
            saida.write(',Exec {}'.format(i+1))
        saida.write('\n')

        for pesquisa in medidas.keys():
            saida.write(pesquisa)
            tempos = medidas[pesquisa]
            for tempo in tempos:
                saida.write(',{0:.2f}'.format(tempo))
            saida.write('\n')

    with open('criar_csv_medidas_memoria.csv', 'w') as saida:
        saida.write('Termo')
        for i in range(num_medidas_por_vez):
            saida.write(',Exec {}'.format(i+1))
        saida.write('\n')

        for pesquisa in medidas.keys():
            saida.write(pesquisa)
            mems = medidas_mem[pesquisa]
            for mem in mems:
                saida.write(',{0:.2f}'.format(mem))
            saida.write('\n')

if __name__ == '__main__':
    criar_csv_medidas_tempo_mem(6)
