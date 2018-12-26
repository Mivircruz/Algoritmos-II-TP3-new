#!/usr/bin/python3

import random

class Vertice(object):

    def __init__(self, ciudad, latitud, longitud):
        self.ciudad = ciudad
        self.latitud = latitud
        self.longitud = longitud
        self.adyacentes = {}

    def obtener_latitud(self):
        return self.latitud

    def obtener_longitud(self):
        return self.longitud

    def obtener_ciudad(self):
        return self.ciudad

    def obtener_adyacente_random(self):
        return random.choice(list(self.adyacentes))

    def obtener_adyacentes_claves(self):
        return list(self.adyacentes.keys())

    def obtener_tiempo(self, codigo):
        if codigo not in self.adyacentes:
            return None
        datos_conexion = self.adyacentes.get(codigo)
        return datos_conexion[0]

    def obtener_precio(self, codigo):
        if codigo not in self.adyacentes:
            return None
        datos_conexion = self.adyacentes.get(codigo)
        return datos_conexion[1]

    def obtener_cant_vuelos(self, codigo):
        if codigo not in self.adyacentes:
            return None
        datos_conexion = self.adyacentes.get(codigo)
        return datos_conexion[2]

    def agregar_adyacente(self, codigo, tiempo, precio, cant_vuelos):
        self.adyacentes[codigo] = [tiempo, precio, cant_vuelos]

    def son_adyacentes(self, codigo_ady):
        if codigo_ady in self.adyacentes:
            return True
        return False

    def obtener_aeropuertos_claves(self):
        return self.adyacentes.keys()


