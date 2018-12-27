# !/usr/bin/python3

import heapq
import math
import grafo as g
import vertice as v
import operator
import random

def obtener_parametros(linea):

    parametros = linea.split(" ")
    sep = " "
    aux1 = []
    parametros_final = []

    for i in range(1, len(parametros)):
        aux1.append(parametros[i])

    cadena = sep.join(aux1)
    aux2 = cadena.split(",")

    for i in range(0, len(aux2)):
        parametros_final.append(aux2[i])

    return parametros_final


def recorrido_dfs(grafo, v, visitados, padres, orden):
    visitados.add(v)
    for w in grafo.obtener_vertice_valor(v).obtener_adyacentes_claves():
        if w not in visitados:
            padres[w] = v
            orden[w] = orden[v] + 1
            recorrido_dfs(grafo, w, visitados, padres, orden)


def dfs(grafo, origen):
    visitados = set()
    padres = {}
    orden = {}
    padres[origen] = None
    orden[origen] = 0
    recorrido_dfs(grafo, origen, visitados, padres, orden)
    return padres, orden


def bfs(grafo, origen):
    visitados = set()
    padres = {}
    orden = {}
    cola = []
    visitados.add(origen)
    padres[origen] = None
    orden[origen] = 0
    cola.append(origen)

    while len(cola) != 0:
        v = cola.pop(0)
        for w in grafo.obtener_vertice_valor(v).obtener_adyacentes_claves():
            if w not in visitados:
                visitados.add(w)
                padres[w] = v
                orden[w] = orden[v] + 1
                cola.append(w)

    return padres, orden

def camino_minimo(grafo, aeropuerto_origen, destino, modo):

    distancia = {}
    padres = {}
    visitados = set()
    heap = []
    peso_total = 0

    for key in grafo.obtener_todos_vertices_claves():
        distancia[key] = float('inf')

    distancia[aeropuerto_origen] = 0
    padres[aeropuerto_origen] = None
    vertice_actual = grafo.obtener_vertice_valor(aeropuerto_origen)
    visitados.add(vertice_actual.obtener_ciudad())
    heapq.heappush(heap, (distancia[aeropuerto_origen], aeropuerto_origen))

    while heap:

        aeropuerto_actual = heapq.heappop(heap)
        vertice_actual = grafo.obtener_vertice_valor(aeropuerto_actual[1])
        ciudad_actual = vertice_actual.obtener_ciudad()
        visitados.add(ciudad_actual)

        if ciudad_actual == destino:
            return padres, distancia, peso_total, aeropuerto_actual[1]

        for adyacente in grafo.obtener_vertice_valor(aeropuerto_actual[1]).obtener_adyacentes_claves():
            vertice_adyacente = grafo.obtener_vertice_valor(adyacente)
            ciudad_adyacente = vertice_adyacente.obtener_ciudad()
            if ciudad_adyacente not in visitados:
                if modo == "barato":
                    peso = int(vertice_adyacente.obtener_precio(aeropuerto_actual[1]))
                else:
                    peso = int(vertice_adyacente.obtener_tiempo(aeropuerto_actual[1]))

                if aeropuerto_actual[0] + peso < distancia[adyacente]:
                    distancia[adyacente] = aeropuerto_actual[0] + peso
                    peso_total += peso
                    padres[adyacente] = aeropuerto_actual[1]
                    heapq.heappush(heap, (distancia[adyacente], adyacente))

    return padres, distancia, peso_total, aeropuerto_actual[1]

def prim(grafo, aeropuerto_origen):

    visitados = []
    visitados.append(aeropuerto_origen)
    heap = []
    arbol = g.Grafo()

    for adyacente in grafo.obtener_vertice_valor(aeropuerto_origen).obtener_adyacentes_claves():
        vertice_adyacente = grafo.obtener_vertice_valor(adyacente)
        peso = vertice_adyacente.obtener_precio(aeropuerto_origen)
        heapq.heappush(heap, (int(peso), adyacente, aeropuerto_origen))

    for key in grafo.obtener_todos_vertices_claves():
        v = grafo.obtener_vertice_valor(key)
        arbol.agregar_vertice(key, (v.obtener_ciudad(), 0, 0))

    while heap:
        v = heapq.heappop(heap)

        if v[1] in visitados:
            continue

        arbol.agregar_arista(v[1], v[2], (0, v[0], 0))

        visitados.append(v[1])

        for key in grafo.obtener_vertice_valor(v[1]).obtener_adyacentes_claves():
            vertice_adyacente = grafo.obtener_vertice_valor(key)

            if key in visitados:
                continue
            a_guardar = vertice_adyacente.obtener_precio(v[1])
            heapq.heappush(heap, (int(a_guardar), key, v[1]))
    return arbol


def recorrido_vacaciones(grafo, origen, v, contador, n, visitados):

    visitados.append(v)

    if contador == n:
        return True

    for adyacente in grafo.obtener_vertice_valor(v).obtener_adyacentes_claves():
        if adyacente not in visitados:
            if contador == n-1:
                if origen not in grafo.obtener_vertice_valor(adyacente).obtener_adyacentes_claves():
                    break
            if recorrido_vacaciones(grafo, origen, adyacente, contador+1, n, visitados):
                return True
    visitados.remove(v)
    return False


def reconstruir_camino(origen, destino, padres, visitados, lugares, grafo):
    v = destino
    camino = []

    while v != origen:
        camino.append(v)
        if grafo.obtener_vertice_valor(v).obtener_ciudad() in lugares:
            lugares.remove(grafo.obtener_vertice_valor(v).obtener_ciudad())
        v = padres[v]

    if grafo.obtener_vertice_valor(origen).obtener_ciudad() in lugares:
        lugares.remove(grafo.obtener_vertice_valor(origen).obtener_ciudad())
    camino.append(origen)
    camino.reverse()

    while camino:
        aeropuerto = camino.pop(0)
        if visitados:
            if aeropuerto == visitados[len(visitados)-1]:
                continue
        visitados.append(aeropuerto)

    return

def recorrer_lugares(grafo, lugares, actual, costo, visitados):
    if len(lugares) == 0:
        return costo

    ciudad_aleatoria = random.choice(lugares)
    while ciudad_aleatoria not in lugares:
        ciudad_aleatoria = random.choice(lugares)

    padres, distancia, peso_total, aeropuerto_destino = camino_minimo(grafo, actual, ciudad_aleatoria, "rapido")

    reconstruir_camino(actual, aeropuerto_destino, padres, visitados, lugares, grafo)
    costo += peso_total

    return recorrer_lugares(grafo, lugares, aeropuerto_destino, costo, visitados)


def centralidad(grafo):
    cent = {}

    for key in grafo.obtener_todos_vertices_claves():
        cent[key] = 0

    for key1 in grafo.obtener_todos_vertices_claves():
        padres, dist = bfs(grafo, key1)
        cent_aux = {}
        for key2 in grafo.obtener_todos_vertices_claves():
            cent_aux[key2] = 0

        # Filtra infinitos
        for a in dist:
            if type(dist) is float:
                if math.isinf(a):
                    dist.pop(a)

        vertices_ordenados = sorted(dist.items(), key=operator.itemgetter(1))

        for w in vertices_ordenados:
            if w[0] == key1:
                continue

            cent_aux[padres[w[0]]] += 1
            cent_aux[padres[w[0]]] += cent_aux[w[0]]

        for w in grafo.obtener_todos_vertices_claves():
            if w == key1:
                continue
            cent[w] += cent_aux[w]

    return cent
