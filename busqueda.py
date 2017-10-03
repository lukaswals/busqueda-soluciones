# -*- coding: utf-8 -*-
import time
from tkinter import *


class Busqueda(object):
    def __init__(self, inicio):
        self.abiertos = []
        self.cerrados = []
        self.tiempo_total = 0
        self.inicio = inicio

    def buscar(self):
        encontro = False
        self.abiertos.append(self.inicio)
        while self.abiertos and not encontro:
            # Extraemos el primer elemento de Abiertos y lo insertamos en la
            # lista de Cerrados. Actual es el nodo que comprobaremos si posee
            # el estado objetivo, o "expanderemos" para generar otros estados.
            actual = self.abiertos.pop(0)
            self.cerrados.append(actual)
            # Aqui verificamos si "actual" es el nodo objetivo
            if actual.test_objetivo():
                encontro = True
            else:
                # Como no es el destino, debemos generar los sucesores y
                # ordenar la lista de abiertos
                self.aplicar_estrategia(actual.crear_sucesores())

    def crear_frame(self, contenedor):
        frame = Frame(contenedor, width="500", height="400")
        Label(frame, text="Resultado:").pack()
        if not self.abiertos:
            Label(frame, text="No se encontro solución").pack()
        else:
            self.cerrados[-1].crear_frame(frame).pack()
            (Label(frame, text="Nodos Totales: " + str(len(self.abiertos) +
                len(self.cerrados))).pack())
            (Label(frame, text="Nodos Abiertos: " + str(len(self.abiertos))).
                pack())
            (Label(frame, text="Nodos Cerrados: " + str(len(self.cerrados))).
                pack())
            Label(frame, text="Tiempo: " + str(self.tiempo_total)).pack()
        frame.pack_propagate(False)
        return frame

    def cronometro(self, funcion, *argumentos):
        # Tiempo de inicio de ejecución.
        inicio = time.time()
        # Aca ejecutamos la funcion.
        funcion(*argumentos)
        # Tiempo de fin de ejecución.
        fin = time.time()
        # Tiempo de ejecución total.
        self.tiempo_total = fin - inicio

    def ordenar(self, sucesores):
        pass


class Profundidad(Busqueda):
    def __init__(self, inicial):
        super().__init__(inicial)

    def aplicar_estrategia(self, sucesores):
        while sucesores:
            self.abiertos.insert(0, sucesores.pop())


class Anchura(Busqueda):
    def __init__(self, inicial):
        super().__init__(inicial)

    def aplicar_estrategia(self, sucesores):
        self.abiertos.extend(sucesores)


class CostoUniforme(Busqueda):
    def __init__(self, inicial):
        super().__init__(inicial)
        self.inicio.calcular_costo()

    def aplicar_estrategia(self, sucesores):
        for sucesor in sucesores:
            sucesor.calcular_costo()
            j = len(self.abiertos)
            while j > 0 and self.abiertos[j - 1].costo > sucesor.costo:
                j -= 1
            self.abiertos.insert(j, sucesor)


class ProfundidadInformada(Busqueda):
    def __init__(self, inicial):
        super().__init__(inicial)

    def aplicar_estrategia(self, sucesores):
        lim = 0
        for sucesor in sucesores:
            sucesor.calcular_heuristica()
            j = 0
            while j < lim and self.abiertos[j].heuristica < sucesor.heuristica:
                j += 1
            self.abiertos.insert(j, sucesor)
            lim += 1


class BestFirst(Busqueda):
    def __init__(self, inicial):
        super().__init__(inicial)

    def aplicar_estrategia(self, sucesores):
        for sucesor in sucesores:
            sucesor.calcular_heuristica()
            j = 0
            while (j < len(self.abiertos) and
                self.abiertos[j].heuristica < sucesor.heuristica):
                j += 1
            self.abiertos.insert(j, sucesor)


class AEstrella(Busqueda):
    def __init__(self, inicial):
        super().__init__(inicial)
        self.inicio.calcular_f()

    def aplicar_estrategia(self, sucesores):
        for sucesor in sucesores:
            sucesor.calcular_f()
            j = 0
            while j < len(self.abiertos) and self.abiertos[j].f < sucesor.f:
                j += 1
            while (j < len(self.abiertos) and self.abiertos[j].f == sucesor.f
                   and self.abiertos[j].heuristica < sucesor.heuristica):
                j += 1
            self.abiertos.insert(j, sucesor)