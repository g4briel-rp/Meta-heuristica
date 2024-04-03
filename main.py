import random


def adjacentes(u, solucao, arestas):
  return [v for v in arestas[u] if arestas[u][v] == 1]


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


if __name__ == "__main__":
  arestas = [[0, 1, 0, 1, 0, 1], [1, 0, 1, 1, 1, 1], [0, 1, 0, 0, 0, 0],
             [1, 1, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0], [1, 1, 0, 0, 0, 0]]
  solucao = [0, 1, 2, 3, 4, 5]
  conjunto = []
  for u in solucao:
    if isEmpty(arestas):
      break
    else:
      adj = adjacentes(u, solucao, arestas)
      if len(adj) >= 0:
        for v in adj:
          arestas[u][v] = 0
          arestas[v][u] = 0
        conjunto.append(u)
  print(f"Resultado: {conjunto} | Número de vertices: {len(conjunto)}")

  # solucao = swap(solucao)
  # print(solucao)
