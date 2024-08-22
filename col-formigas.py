import cProfile, pstats, io
from pstats import SortKey
import random
from copy import deepcopy
from collections import Counter, defaultdict, deque

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

def soma_feromonios(feromonios):
    soma = 0
    for f in feromonios:
        soma += feromonios[f]
    return soma

def colonia_formigas(k, numero_solucoes, numero_melhores_solucoes, feromonios, listaADJ):
    melhor = None
    while k > 0:
        individuos = []
        i = numero_solucoes

        while i > 0:
            individuo = []
            copia_lista_ADJ = deepcopy(listaADJ)
            while any(copia_lista_ADJ.values()):
                vertice_escolhido = random.randint(0, soma_feromonios(feromonios))
                if vertice_escolhido not in individuo:
                    adj = adjacentes(vertice_escolhido, copia_lista_ADJ)
                    if adj:
                        adj = list(adj)
                        for v in adj:
                            copia_lista_ADJ[vertice_escolhido].remove(v)
                            copia_lista_ADJ[v].remove(vertice_escolhido)
                        individuo.append(vertice_escolhido)

            if individuo not in individuos:
                individuos.append(individuo)
                i -= 1

        individuos.sort(key=len)
        melhores = individuos[: numero_melhores_solucoes]

        todos = [vertice for i in melhores for vertice in i]
        add_feromonios = Counter(todos)

        for item in add_feromonios:
            feromonios[item] += add_feromonios[item]

        if not melhor:
            melhor = melhores[0]
        else:
            if len(melhores[0]) < len(melhor):
                melhor = melhores[0]

        with open('output-MH3-instancia-' + str(contador_instancias) + '.txt', 'w') as f:
            f.write(f"Conjunto colonia de formigas: {melhor}\n\n")
            f.write(f"Tamanho do conjunto colonia de formigas: {len(melhor)}\n\n\n")
            f.close()

        k -= 1

    return melhor, len(melhor)


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

        # Colonias de Formigas
        feromonios = defaultdict(set)
        for i in listaVertices:
            feromonios[i] = 1

        conjunto, tam_conjunto = colonia_formigas(5, 20, 5, feromonios, deepcopy(listaADJ))

        pr.disable()
        s = io.StringIO()
        sortby = SortKey.CUMULATIVE
        ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
        ps.print_stats()
        print(s.getvalue())

        with open('output-MH3-instancia-' + str(contador_instancias) + '.txt', 'a') as f:
            f.write(s.getvalue())
            f.close()
            
        contador_instancias += 1