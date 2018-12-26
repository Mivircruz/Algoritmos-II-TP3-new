import vertice
import random

class Grafo(object):

	def __init__(self):
		self.vertices = {}

	def agregar_vertice(self, codigo, valor):
		self.vertices[codigo] = vertice.Vertice(valor[0], valor[1], valor[2])

	def agregar_arista(self, codigo1, codigo2, peso):
		self.vertices[codigo1].agregar_adyacente(codigo2, peso[0], peso[1], peso[2])
		self.vertices[codigo2].agregar_adyacente(codigo1, peso[0], peso[1], peso[2])

	def obtener_vertice_valor(self, codigo):
		return self.vertices[codigo]

	def obtener_peso(self, codigo1, codigo2):
		tiempo = self.vertices[codigo1].obtener_tiempo(codigo2)
		precio = self.vertices[codigo1].obtener_precio(codigo2)
		cant_vuelos = self.vertices[codigo1].obtener_cant_vuelos(codigo2)
		return (tiempo, precio, cant_vuelos)

	def obtener_aeropuertos(self, ciudad):
		lista_aeropuertos = []
		for key, value in self.vertices.items():
			if value.obtener_ciudad() == ciudad:
				lista_aeropuertos.append(key)

		return lista_aeropuertos

	def obtener_todos_vertices_valores(self):
		return list(self.vertices.values())

	def obtener_todos_vertices_claves(self):
		return list(self.vertices.keys())

	def estan_conectados(self, codigo1, codigo2):
		return self.vertices[codigo1].son_adyacentes(codigo2)

	def obtener_vertice_random(self):
		codigo_random = random.choice(list(self.vertices))
		return self.vertices.get(codigo_random)

	def obtener_largo(self):
		return len(self.vertices)

	def pertenece(self, codigo):
		if codigo not in self.vertices:
			return False
		return True

	def __iter__(self):
		return iter(self.vertices.values)
