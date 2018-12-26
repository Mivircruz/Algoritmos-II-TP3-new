#!/usr/bin/python3

import funciones
import operator

ultima_ruta = []

def camino_mas(grafo, linea):

    #Validación

    parametros = funciones.obtener_parametros(linea)
    if len(parametros) != 3:
        return False

    #Vacía la última ruta para reemplazarla

    if len(ultima_ruta) != 0:
        del ultima_ruta[:]

    #Comienzo de la función

    modo = parametros[0]
    origen = parametros[1]
    destino = parametros[2]
    aeropuertos = grafo.obtener_aeropuertos(origen)
    peso_min = float('inf')
    padres_final = {}
    destino_final = None
    indice = 0

    for i in range(0, len(aeropuertos)):
        padres, dist, peso, destino = funciones.camino_minimo(grafo, aeropuertos[i], destino, modo)
        if peso < peso_min:
            padres_final = padres
            peso_min = peso
            destino_final = destino
            indice = i

    lista = []
    lista.append(destino_final)
    v = lista[0]

    while v != aeropuertos[indice]:
        v = padres_final[v]
        lista.append(v)

    while lista:
        if len(lista) != 1:
            aeropuerto = lista.pop()
            ultima_ruta.append(aeropuerto)
            print(aeropuerto, end=" ")
            print("->", end=" ")

        else:
            aeropuerto = lista.pop()
            print(aeropuerto)
            ultima_ruta.append(aeropuerto)

    return True


def camino_escalas(grafo, linea):

    # Validación

    parametros = funciones.obtener_parametros(linea)
    if len(parametros) != 2:
        return False

    #Vacía la última ruta para reemplazarla

    if len(ultima_ruta) != 0:
        del ultima_ruta[:]

    #Comienzo de la función

    origen = parametros[0]
    destino = parametros[1]
    aeropuertos_origen = grafo.obtener_aeropuertos(origen)
    aeropuertos_destino = grafo.obtener_aeropuertos(destino)
    padres_final = {}
    indice = 0
    mejor_orden = float('inf')
    destino_final = None

    for i in range(0, len(aeropuertos_origen)):
        padres, orden = funciones.bfs(grafo, aeropuertos_origen[i])
        for k in range(0, len(aeropuertos_destino)):
            if orden[aeropuertos_destino[k]] < mejor_orden:
                padres_final = padres
                indice = i
                destino_final = aeropuertos_destino[k]

    lista = []
    lista.append(destino_final)
    v = lista[0]

    while v != aeropuertos_origen[indice]:
        v = padres_final[v]
        lista.append(v)

    while lista:
        if len(lista) != 1:
            aeropuerto = lista.pop()
            print(aeropuerto, end=" ")
            ultima_ruta.append(aeropuerto)
            print("->", end=" ")

        else:
            aeropuerto = lista.pop()
            print(aeropuerto)
            ultima_ruta.append(aeropuerto)

    return True


def centralidad_aprox(grafo, linea):

    #Validación

    parametros = funciones.obtener_parametros(linea)
    if len(parametros) != 1:
        return False

    #Comienzo de la función

    cent = funciones.centralidad(grafo)
    vertices = sorted(cent.items(), key=operator.itemgetter(1))

    for i in range(0, int(parametros[0])):
        if i != int(parametros[0]) - 1:
            print(vertices.pop()[0] + ",", end=" ")
        else:
            print(vertices.pop()[0])

    return True


def recorrer_mundo_aprox(grafo, linea):

    #Validación

    parametros = funciones.obtener_parametros(linea)
    if len(parametros) != 1:
        return False

    #Vacía la última ruta para reemplazarla

    if len(ultima_ruta) != 0:
        del ultima_ruta[:]

    #Comienzo de la función

    parametros = funciones.obtener_parametros(linea)
    origen = parametros[0]
    lugares = []
    for vertice in grafo.obtener_todos_vertices_valores():
        lugares.append(vertice.obtener_ciudad())
    visitados = []
    costo = 0

    for aeropuerto in grafo.obtener_aeropuertos(origen):
        if funciones.recorrer_lugares(grafo, lugares, aeropuerto, costo, visitados):
            break

    for i in range(0, len(visitados)):
        if i < len(visitados) - 1:
            print(visitados[i], end=" ")
            print(" -> ", end=" ")
        else:
            print(visitados[i])
    print("Costo: ", costo)

    return True


def vacaciones(grafo, linea):

    #Validación

    parametros = funciones.obtener_parametros(linea)
    if len(parametros) != 2:
        return False

    # Vacía la última ruta para reemplazarla

    if len(ultima_ruta) != 0:
        del ultima_ruta[:]

    #Comienzo de la función

    origen = parametros[0]
    aeropuerto_origen = None
    visitados = []
    n = parametros[1]
    contador = 0

    for aeropuerto in grafo.obtener_aeropuertos(origen):
        if funciones.recorrido_vacaciones(grafo, aeropuerto, aeropuerto, contador, int(n), visitados):
            aeropuerto_origen = aeropuerto
            break

    if len(visitados) == 0:
        print("No se encontro recorrido")
    else:
        for i in range(0, len(visitados)):
            print(visitados[i], end=" ")
            print("->", end=" ")
            ultima_ruta.append(visitados[i])
        print(aeropuerto_origen)
        ultima_ruta.append(aeropuerto_origen)

    return True


def nueva_aerolinea(grafo, linea):

    #Validación

    if len(ultima_ruta) != 0:
        del ultima_ruta[:]

    #Comienzo de la función

    parametros = funciones.obtener_parametros(linea)
    if len(parametros) != 1:
        return False

    archivo = open(parametros[0], 'w')
    origen_aleatorio = grafo.obtener_vertice_random()

    arbol, peso_total = funciones.prim(grafo, origen_aleatorio, "barato")

    for aeropuerto in arbol.obtener_todos_vertices_claves():
        ultima_ruta.append(aeropuerto)
        archivo.write(aeropuerto + ',')

    archivo.close()
    print("OK")
    return True


def exportar_kml(grafo, linea):

    #Validación

    parametros = funciones.obtener_parametros(linea)
    if len(parametros) != 1 or len(ultima_ruta) == 0:
        return False

    #Comienzo de la función

    archivo = open(parametros[0], "w")

    # Encabezado
    archivo.write('<?xml version="1.0" encoding="UTF-8"?>\n')

    # Declaración de KML
    archivo.write('<kml xmlns="http://www.opengis.net/kml/2.2">\n')
    archivo.write('\t<Document>\n\t')

    for i in range(0, len(ultima_ruta)):
        # Contenido geográfico

        ciudad = ultima_ruta[i]
        latitud = grafo.obtener_latitud(ultima_ruta[i])
        longitud = grafo.obtener_longitud(ultima_ruta[i])

        archivo.write('\n\t\t<Placemark>\n\t')
        archivo.write('\t\t<name>' + ciudad + '</name>\n\t')
        archivo.write('\t\t<Point>\n\t')
        archivo.write('\t\t\t<coordinates>' + longitud.rstrip('\n') + ', ' + latitud + '</coordinates>\n\t')
        archivo.write('\t\t</Point>\n\t')
        archivo.write('\t</Placemark>\n')

    for i in range(1, len(ultima_ruta) - 1):
        lat_prim = grafo.obtener_latitud(ultima_ruta[i - 1])
        long_prim = grafo.obtener_longitud(ultima_ruta[i - 1])
        lat_seg = grafo.obtener_latitud(ultima_ruta[i])
        long_seg = grafo.obtener_longitud(ultima_ruta[i])

        archivo.write('\n\t\t<Placemark>\n\t')
        archivo.write('\t\t<LineString>\n\t')
        archivo.write(
            '\t\t\t<coordinates>' + long_prim.rstrip('\n') + ', ' + lat_prim.rstrip('\n') + ' ' + long_seg.rstrip(
                '\n') + ', ' + lat_seg + '</coordinates>\n\t')
        archivo.write('\t\t</LineString>\n\t')
        archivo.write('\t</Placemark>\n')

    # Fin de Documento

    archivo.write('\n\t</Document>')
    archivo.write('\n</kml>')

    archivo.close()
    return True


comandos = {
    "camino_mas": camino_mas,
    "camino_escalas": camino_escalas,
    "centralidad_aprox": centralidad_aprox,
    "recorrer_mundo_aprox": recorrer_mundo_aprox,
    "vacaciones": vacaciones,
    "nueva_aerolinea": nueva_aerolinea,
    "exportar_kml": exportar_kml
}
