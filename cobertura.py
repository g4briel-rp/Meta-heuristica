import random

def imprime(list):
    for i in list:
        print(i)

def adjacentes(u, vertices, matrizArestas):
   print(vertices)
#   return [v for v in vertices if matrizArestas[u-1][v-1] == 1]

def isEmpty(arestas):
  for i in range(len(arestas)):
    for j in range(len(arestas[i])):
      if arestas[i][j] == 1:
        return False
  return True

def swap(solucao):
  porcentagem = 0.1
  qtd = round(porcentagem * len(solucao))
  print(qtd)
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
    matrizArestas = []

    with open(arquivo, 'r') as f:
        firstLine = f.readline()
        dados = firstLine.split()
        vertices = int(dados[0])
        arestas = int(dados[1])

        linhas = f.readlines()
        for line in linhas:
            line = line.split()
            matrizArestas.append([int(line[0]), int(line[1]), 1])
            matrizArestas.append([int(line[1]), int(line[0]), 1])
    
    # graus = []
    # for i in range(1, vertices):
    #     graus.append(descobreGrau(i, list(range(1, vertices + 1)), matrizArestas))
    
    print(matrizArestas[0:11])

    # corrigir a criação da matriz de arestas