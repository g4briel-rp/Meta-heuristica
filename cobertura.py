import random
import numpy as np

def imprime(list):
  for i in list:
    print(i)

def adjacentes(u, vertices, matrizArestas):
  return [v for v in vertices if matrizArestas[u][v] == 1]

def isEmpty(arestas):
  for i in range(len(arestas)):
    for j in range(len(arestas[i])):
      if arestas[i][j] == 1:
        return False
  return True

def swap(solucao):
  porcentagem = 0.1
  qtd = round(porcentagem * len(solucao))
  contador = 0
  while contador < qtd:
    index1 = random.randint(0, len(solucao) - 1)
    index2 = random.randint(0, len(solucao) - 1)
    if index1 != index2:
      solucao[index1], solucao[index2] = solucao[index2], solucao[index1]
      contador += 1
  return solucao

def descobreGrau(u, vertices, matrizArestas):
  return len(adjacentes(u, vertices, matrizArestas))

if __name__ == '__main__':
  arquivo = './datasets/bio-diseasome/bio-diseasome.mtx'

  with open(arquivo, 'r') as f:
    firstLine = f.readline()
    dados = firstLine.split()
    vertices = int(dados[0])
    listaVertices = list(range(0, vertices + 1))
    arestas = int(dados[1])

    matrizArestas = np.zeros((vertices + 1, vertices + 1))
    linhas = f.readlines()
    for line in linhas:
      line = line.split()
      matrizArestas[int(line[0])][int(line[1])] = 1
      matrizArestas[int(line[1])][int(line[0])] = 1
  
  graus = []
  for i in listaVertices:
    graus.append(descobreGrau(i, listaVertices, matrizArestas))
  
  solucao = []
  while not all(i == -1 for i in graus):
    indice = graus.index(max(graus))
    solucao.append(indice)
    graus[indice] = -1
  
  conjunto = []
  for k in range(0, 5):
    copia = matrizArestas.copy()
    for s in solucao:
      if isEmpty(copia):
        break
      else:
        adj = adjacentes(s, solucao, copia)
        if len(adj) > 0:
          for v in adj:
            copia[s][v] = 0
            copia[v][s] = 0
          conjunto.append(s)

    print(f"Resultado: {conjunto} | Número de vertices: {len(conjunto)}\n")
    solucao = swap(solucao)
    conjunto.clear()