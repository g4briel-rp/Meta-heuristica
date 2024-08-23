import cProfile, pstats, io
from pstats import SortKey
import random
from copy import deepcopy
from collections import defaultdict 

# -------------------------------------------------------------------------------------------------------------------------------------
# HEURISTICA ALEATORIA
# -------------------------------------------------------------------------------------------------------------------------------------

def adjacentes(u, listaADJ):
    return listaADJ[u]

def addADJ(listaADJ, u, v):
    listaADJ[u].add(v)

def avalia_solucao(solucao, listaADJ):
    conjunto = []
    
    for s in solucao:
        if not listaADJ:
            break
        else:
            adj = adjacentes(s, listaADJ)
            if adj:
                adj = list(adj)
                for v in adj:
                    listaADJ[s].remove(v)
                    listaADJ[v].remove(s)
                conjunto.append(s)

    return conjunto, len(conjunto)

if __name__ == '__main__':
    pr = cProfile.Profile()

    instancia1 = 'instancias-MH/umk.txt'
    instancia2 = 'instancias-MH/cemk.txt'
    instancia3 = 'instancias-MH/umM.txt'
    instancia4 = 'instancias-MH/vqM.mtx'

    instancias = [instancia1, instancia2, instancia3, instancia4]
    contador_instancias = 1
    
    for i in instancias:
        pr.enable()

        with open(i, 'r') as f:
            firstLine = f.readline()
            dados = firstLine.split()
            vertices = int(dados[0])
            listaVertices = list(range(0, vertices + 1))
            arestas = int(dados[1])

            listaADJ = defaultdict(set)
            linhas = f.readlines()
            for line in linhas:
                line = line.split()
                if int(line[0]) != int(line[1]):
                    addADJ(listaADJ, int(line[0]), int(line[1]))
                    addADJ(listaADJ, int(line[1]), int(line[0]))

        solucao = []
        solucao = listaVertices
        solucao = random.sample(solucao, len(solucao))

        conjunto, tamanho_conjunto = avalia_solucao(solucao, deepcopy(listaADJ))

        pr.disable()
        s = io.StringIO()
        sortby = SortKey.CUMULATIVE
        ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
        ps.print_stats()
        
        with open('output-H1-instancia-' + str(contador_instancias) + '.txt', 'a') as f:
            f.write(f"Heurística aleatória para a instância {i} \n\n")
            f.write(f"Solucao: {solucao}\n\n")
            f.write(f"Conjunto: {conjunto}\n\n")
            f.write(f"Tamanho do conjunto: {tamanho_conjunto}\n\n\n")
            f.write(s.getvalue())
            f.close()
        
        contador_instancias += 1