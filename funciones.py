# !/usr/bin/python3

import heapq
import math
import grafo as g
import vertice as v
import operator

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

def prim(grafo, aeropuerto_origen, modo):

    visitados = []
    visitados.append(aeropuerto_origen)
    heap = []
    arbol = g.Grafo()
    peso_total = 0

    for adyacente in grafo.obtener_vertice_valor(aeropuerto_origen).obtener_adyacentes_claves():
        vertice_adyacente = grafo.obtener_vertice_valor(adyacente)
        if modo == "barato":
            peso = vertice_adyacente.obtener_precio(aeropuerto_origen)
        else:
            peso = vertice_adyacente.obtener_tiempo(aeropuerto_origen)
        heapq.heappush(heap, (peso, adyacente, aeropuerto_origen))

    for v in grafo.obtener_todas_aristas():
        arbol.agregar_vertice(v.obtener_ciudad(), v.obtener_codigo(), 0, 0)

    while heap:
        v = heapq.heappop(heap)
        vertice_actual = grafo.obtener_vertice_valor(v[1])
        ciudad_actual = vertice_actual.obtener_ciudad()
        if ciudad_actual in visitados:
            continue

        if modo == "barato":
            arbol.agregar_arista(v[1], v[2], 0, v[0], 0)
        else:
            arbol.agregar_arista(v[1], v[2], v[0], 0, 0)

        visitados.append(ciudad_actual)

        for key in grafo.obtener_adyacentes(v[1]):
            vertice_adyacente = grafo.obtener_vertice_valor(key)
            ciudad_adyacente = vertice_adyacente.obtener_ciudad()

            if ciudad_adyacente not in visitados:

                if modo == "barato":
                    a_guardar = vertice_adyacente.obtener_precio(v[1])
                else:
                    a_guardar = vertice_adyacente.obtener_tiempo(v[1])
                peso_total += int(a_guardar)
                heapq.heappush(heap, (a_guardar, key, v[1]))
    return arbol, peso_total


def recorrido_vacaciones(grafo, origen, v, contador, n, visitados):

    visitados.append(v)

    if contador == n:
        return True

    for adyacente in grafo.obtener_vertice_valor(v).obtener_adyacentes():
        if adyacente not in visitados:
            if adyacente not in visitados:
                if contador == n-1:
                    if origen not in grafo.obtener_vertice_valor(adyacente).obtener_adyacentes_claves():
                        break
                contador += 1
                if recorrido_vacaciones(grafo, origen, adyacente, contador, n, visitados):
                    return True
    visitados.remove(v)
    return False


def recorrer_lugares(grafo, lugares, actual, costo, visitados):
    if len(lugares) == 0:
        return True

    mejor_tiempo = float('inf')
    ciudad_prox = None
    mejor_aeropuerto = None


    for adyacente in grafo.obtener_vertice_valor(actual).obtener_adyacentes_claves():

        vertice_adyacente = grafo.obtener_vertice_valor(adyacente)
        if vertice_adyacente.obtener_ciudad() not in lugares:
            continue

        tiempo_actual = vertice_adyacente.obtener_tiempo(actual)
        if float(tiempo_actual) < float(mejor_tiempo):
            mejor_tiempo = tiempo_actual
            mejor_aeropuerto = adyacente
            ciudad_prox = vertice_adyacente.obtener_ciudad()

    costo += float(mejor_tiempo)
    print(ciudad_prox)
    lugares.remove(ciudad_prox)
    visitados.append(mejor_aeropuerto)

    return recorrer_lugares(grafo, lugares, mejor_aeropuerto, costo, visitados)



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

        for w in grafo.obtener_todos_vertices().keys():
            if w == key1:
                continue
            cent[w] += cent_aux[w]

    return cent
