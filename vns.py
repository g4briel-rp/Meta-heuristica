import cProfile, pstats, io
from pstats import SortKey
import random
import numpy as np
from copy import deepcopy
from collections import defaultdict, deque

contador_instancias = 1

def adjacentes(u, listaADJ):
    return listaADJ[u]

def swap(solucao, porcentagem = 0.0005):
    qtd = round(porcentagem * len(solucao))
    contador = 0
    while contador < qtd:
        index1 = random.randint(0, len(solucao) - 1)
        index2 = random.randint(0, len(solucao) - 1)
        if index1 != index2:
            solucao[index1], solucao[index2] = solucao[index2], solucao[index1]
            contador += 1
    return solucao

def shift(solucao, n):
    solucao = deque(solucao)
    solucao.rotate(n)
    return list(solucao)

def descobreGrau(u, listaADJ):
    return len(adjacentes(u, listaADJ))

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

def solucao_one_max(numVertices, solucao, graus):
    analisados = 0
    while analisados <= numVertices:
        indice = graus.index(max(graus))
        solucao.append(indice)
        graus[indice] = -1
        analisados += 1

def solucao_n_max(numVertices, solucao, graus, listaADJ):
    conjunto = []
    lenGraus = range(0, len(graus))
    analisados = 0
    while analisados <= numVertices:
        indice = graus.index(max(graus))
        solucao.append(indice)
        graus[indice] = -1
        analisados += 1

        if not listaADJ:
            break
        else:
            adj = adjacentes(indice, listaADJ)
            if adj:
                adj = list(adj)
                for v in adj:
                    listaADJ[indice].remove(v)
                    listaADJ[v].remove(indice)
                conjunto.append(indice)
        
        for g in lenGraus:
            if graus[g] != -1:
                graus[g] = descobreGrau(g, listaADJ)
                if graus[g] == 0:
                    graus[g] = -1
                    analisados += 1

    # print(f"Resultado: {conjunto} | Número de vertices: {len(conjunto)}\n")

def localSearch(solucao_inicial, temp_inicial, temp_final, alpha, reaquecimentos, qtd_vizinhos, estrutura_vizinhanca, annealing, listaADJ):
    melhor_solucao = solucao_inicial
    solucao_atual = solucao_inicial

    while reaquecimentos > 0:
        reaquecimentos -= 1
        temp_atual = temp_inicial

        while temp_atual > temp_final:
            temp_atual *= alpha

            i = 0
            while i < qtd_vizinhos:
                i += 1
                if estrutura_vizinhanca == shift:
                    nova_solucao = estrutura_vizinhanca(solucao_atual.copy(), int(len(solucao_atual) * 0.05))
                elif estrutura_vizinhanca == swap:
                    nova_solucao = estrutura_vizinhanca(solucao_atual.copy())

                # chamar o avalia e analisar o retorno dele
                _, tamanho_obj_solucao_atual = avalia_solucao(solucao_atual, deepcopy(listaADJ))
                _, tamanho_obj_nova_solucao = avalia_solucao(nova_solucao, deepcopy(listaADJ))

                delta = tamanho_obj_solucao_atual - tamanho_obj_nova_solucao

                if delta > 0:
                    solucao_atual = nova_solucao

                    # chamar o avalia e analisar o retorno dele
                    melhor_conjunto, tamanho_obj_melhor_solucao = avalia_solucao(melhor_solucao, deepcopy(listaADJ))

                    delta2 = tamanho_obj_melhor_solucao - tamanho_obj_nova_solucao

                    if delta2 > 0:
                        melhor_solucao = solucao_atual
                        
                        with open('output-MH2-instancia-' + str(contador_instancias) + '.txt', 'w') as f:
                            f.write(f"Solucao busca local: {melhor_solucao}\n\n")
                            f.write(f"Conjunto busca local: {melhor_conjunto}\n\n")
                            f.write(f"Tamanho do conjunto busca local: {tamanho_obj_melhor_solucao}\n\n\n")
                            f.close()
                else:
                    if annealing:
                        r = random.uniform(0, 1)
                        if r <= np.exp(-delta / temp_atual):
                            solucao_atual = nova_solucao
    
    melhor_conjunto, tamanho_melhor_conjunto = avalia_solucao(melhor_solucao, deepcopy(listaADJ))
    return melhor_solucao, melhor_conjunto, tamanho_melhor_conjunto

def vns(solucao_inicial, kmax, tmax, listaADJ):
    t = 0

    solucao_atual = solucao_inicial

    while t < tmax:
        k = 1

        conjunto_atual, tam_solucao_atual = avalia_solucao(solucao_atual.copy(), deepcopy(listaADJ))

        while k < kmax:
            solucao_shake = swap(solucao_atual.copy(), 0.25)
            solucao, conjunto, tam_solucao = localSearch(solucao_shake.copy(), 100, 10, 0.9, 5, 20, swap, False, listaADJ)

            if tam_solucao < tam_solucao_atual:
                solucao_atual = solucao
                conjunto_atual = conjunto
                tam_solucao_atual = tam_solucao
                
                with open('output-MH2-instancia-' + str(contador_instancias) + '.txt', 'w') as f:
                    f.write(f"Solucao vns: {solucao_atual}\n\n")
                    f.write(f"Conjunto vns: {conjunto_atual}\n\n")
                    f.write(f"Tamanho do conjunto vns: {tam_solucao_atual}\n\n\n")
                    f.close()

                k = 1
            else:
                k += 1

        t += 1

    return solucao_atual, conjunto_atual, tam_solucao_atual

if __name__ == '__main__':
    pr = cProfile.Profile()
    pr.enable()
    
    instancia1 = 'instancias-MH/umk.txt'
    instancia2 = 'instancias-MH/cemk.txt'
    instancia3 = 'instancias-MH/umM.txt'

    instancias = [instancia1, instancia2, instancia3]
    
    for i in instancias:
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
        
        graus = []
        for v in listaVertices:
            graus.append(descobreGrau(v, listaADJ))
        
        # solucao = []
        # solucao_one_max(vertices, solucao, graus.copy(), deepcopy(listaADJ))

        # solucao = []
        # solucao_n_max(vertices, solucao, graus.copy(), deepcopy(listaADJ))

        solucao = []
        solucao = listaVertices
        solucao = random.sample(solucao, len(solucao))

        melhor_conjunto, tamanho_melhor_conjunto = avalia_solucao(solucao, deepcopy(listaADJ))

        # Variable Neighborhood Search
        solucao, conjunto, tam_conjunto = vns(solucao, 5, 10, deepcopy(listaADJ))

        pr.disable()
        s = io.StringIO()
        sortby = SortKey.CUMULATIVE
        ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
        ps.print_stats()
        print(s.getvalue())

        with open('output-MH2-instancia-' + str(contador_instancias) + '.txt', 'a') as f:
            f.write(s.getvalue())
            f.close()
            
        contador_instancias += 1