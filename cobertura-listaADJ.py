import random
from collections import defaultdict, deque

def adjacentes(u, listaADJ):
    adj = []
    for v in listaADJ[u]:
        adj.append(v)
    return adj

def swap(solucao, porcentagem = 0.1):
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

def solucao_one_max(solucao, graus):
    while not all(i == -1 for i in graus):
        indice = graus.index(max(graus))
        solucao.append(indice)
        graus[indice] = -1

def solucao_one_min(solucao, graus, limite):
    while not all(i == limite for i in graus): 
        indice = graus.index(min(graus)) 
        solucao.append(indice) 
        graus[indice] = limite

def solucao_n_max(solucao, graus, listaADJ):
    conjunto = []
    while not all(i == -1 for i in graus):
        indice = graus.index(max(graus))
        solucao.append(indice)
        graus[indice] = -1

        if not listaADJ:
            break
        else:
            adj = adjacentes(indice, listaADJ)
            if len(adj) > 0:
                for v in adj:
                    listaADJ[indice].remove(v)
                    listaADJ[v].remove(indice)
                conjunto.append(indice)
        
        for g in range(0, len(graus)):
            if graus[g] != -1:
                graus[g] = descobreGrau(g, listaADJ)

    print(f"Resultado: {conjunto} | Número de vertices: {len(conjunto)}\n")

def solucao_n_min(solucao, graus, listaADJ, limite):
    conjunto = []
    while not all(i == limite for i in graus):
        indice = graus.index(min(graus))
        solucao.append(indice)
        graus[indice] = limite

        if not listaADJ:
            break
        else:
            adj = adjacentes(indice, listaADJ)
            if len(adj) > 0:
                for v in adj:
                    listaADJ[indice].remove(v)
                    listaADJ[v].remove(indice)
                conjunto.append(indice)
        
        for g in range(0, len(graus)):
            if graus[g] != limite:
                graus[g] = descobreGrau(g, listaADJ)

    print(f"Resultado: {conjunto} | Número de vertices: {len(conjunto)}\n")

if __name__ == '__main__':
    arquivo1 = './datasets/bio-diseasome/bio-diseasome.mtx'
    arquivo2 = './datasets/email-Enron/Email-Enron.txt'
    arquivo3 = './datasets/inf-power/inf-power.mtx'
    arquivo4 = './datasets/road-netherlands-osm/road-netherlands-osm.mtx'
    arquivo5 = './datasets/wiki-Vote/Wiki-Vote.txt'
    arquivo6 = './datasets/p2p-Gnutella31.txt'

    with open(arquivo1, 'r') as f:
        firstLine = f.readline()
        dados = firstLine.split()
        vertices = int(dados[0])
        listaVertices = list(range(0, vertices + 1))
        arestas = int(dados[1])

        listaADJ = defaultdict(set)
        linhas = f.readlines()
        for line in linhas:
            line = line.split()
            addADJ(listaADJ, int(line[0]), int(line[1]))
            addADJ(listaADJ, int(line[1]), int(line[0]))
    
    graus = []
    for v in listaVertices:
        graus.append(descobreGrau(v, listaADJ))
    
    solucao = []
    # solucao_one_max(solucao, graus)
    # solucao_one_min(solucao, graus, vertices)

    # conjunto = []
    # for s in solucao:
    #     if not listaADJ:
    #         break
    #     else:
    #         adj = adjacentes(s, listaADJ)
    #         if len(adj) > 0:
    #             for v in adj:
    #                 listaADJ[s].remove(v)
    #                 listaADJ[v].remove(s)
    #             conjunto.append(s)

    # print(f"Resultado: {conjunto} | Número de vertices: {len(conjunto)}\n")

    # solucao_n_max(solucao, graus, listaADJ)
    solucao_n_min(solucao, graus, listaADJ, vertices)