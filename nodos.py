# -*- coding: utf-8 -*-
import copy
from tkinter import *


class Nodo(object):
    def __init__(self, padre, estado):
        self.padre = padre
        self.estado = estado
        if self.padre is None:
            self.profundidad = 0
        else:
            self.profundidad = padre.profundidad + 1

    def test_objetivo(self):
        pass

    def crear_sucesores(self):
        pass

    def calcular_costo(self):
        pass

    def calcular_heuristica(self):
        pass

    def calcular_f(self):
        self.calcular_costo()
        self.calcular_heuristica()
        self.f = self.costo + self.heuristica

    def crear_frame(self, contenedor):
        pass


class NodoReina(Nodo):
    def __init__(self, padre, estado, dimension):
        super().__init__(padre, estado)
        self.dimension = dimension

    def test_objetivo(self):
        if len(self.estado) < self.dimension:
            return False
        else:
            return True

    def crear_sucesores(self):
        sucesores = []
        for columna in range(0, self.dimension):
            for fila in range(0, self.dimension):
                if not self.amenazada([columna, fila]):
                    estadoaux = copy.deepcopy(self.estado)
                    estadoaux.append([columna, fila])
                    nodoaux = NodoReina(self, estadoaux, self.dimension)
                    sucesores.append(nodoaux)
        return sucesores

    def amenazada(self, nuevareina):
        result = False
        if self.estado:
            for reina in self.estado:
                if (reina[0] == nuevareina[0] or reina[1] == nuevareina[1]) or (
                abs(reina[0] - nuevareina[0]) == abs(reina[1] - nuevareina[1])):
                    result = True
                    break
        return result

    def calcular_costo(self):
        if self.padre is None:
            self.costo = 0
        else:
            self.costo = self.padre.costo + 1

    def calcular_heuristica(self):
        #"""
        # Primer heurística: Rápida, pero recorre más nodos en pi y bf.
        self.heuristica = self.dimension - len(self.estado)
        """
        # Segunda heurística: Poco mas lenta, pero recorre menos nodos
        # (malo para a*).
        posLibres = 0
        for columna in range(0, self.dimension):
            for fila in range(0, self.dimension):
                if not self.amenazada([columna, fila]):
                    posLibres += 1
        faltan = self.dimension - len(self.estado)
        self.heuristica = faltan + faltan / (faltan + posLibres + 1)
        #"""

    def crear_frame(self, contenedor):
        frame = Frame(contenedor)
        for columna in range(0, self.dimension):
            for fila in range(0, self.dimension):
                if [columna, fila] in self.estado:
                    Button(frame, text="R", width=2, height=1,
                        bg="white").grid(row=fila, column=columna)
                else:
                    Button(frame, text="", width=2, height=1,
                        bg="white").grid(row=fila, column=columna)
        Label(frame, text="Profundidad: " + str(self.profundidad)).grid(
            row=self.dimension, columnspan=self.dimension)
        return frame


class NodoCamino(Nodo):
    def __init__(self, padre, estado, operador):
        super().__init__(padre, estado)
        self.operador = operador

    def test_objetivo(self):
        if 'G' in self.estado:
            return False
        else:
            return True

    def crear_sucesores(self):
        posicion = None
        sucesores = []
        # Si se trata de la raiz, empiezo a moverme a partir de la ubicacion
        # de 'S'
        if self.profundidad is 0:
            posicion = self.estado.index('S')
        else:
            posicion = self.estado.index('U')
        # Operador para moverse hacia arriba
        if posicion - 8 >= 0 and (self.estado[posicion - 8] in [0, 'G']):
            estadoaux = copy.deepcopy(self.estado)
            estadoaux[posicion - 8] = 'U'
            if(self.estado[posicion]) != 'S':
                estadoaux[posicion] = 2
            nodoaux = NodoCamino(self, estadoaux, 0)
            sucesores.append(nodoaux)
        # Operador para moverse hacia la derecha
        if ((posicion + 1) % 8) != 0 and (self.estado[posicion + 1]
            in [0, 'G']):
            estadoaux = copy.deepcopy(self.estado)
            estadoaux[posicion + 1] = 'U'
            if(self.estado[posicion]) != 'S':
                estadoaux[posicion] = 2
            nodoaux = NodoCamino(self, estadoaux, 1)
            sucesores.append(nodoaux)
        # Operador para moverse hacia abajo
        if posicion + 8 <= 63 and (self.estado[posicion + 8] in [0, 'G']):
            estadoaux = copy.deepcopy(self.estado)
            estadoaux[posicion + 8] = 'U'
            if(self.estado[posicion]) != 'S':
                estadoaux[posicion] = 2
            nodoaux = NodoCamino(self, estadoaux, 2)
            sucesores.append(nodoaux)
        # Operador para moverse hacia la izquierda
        if ((posicion - 1) % 8) != 7 and (self.estado[posicion - 1]
            in [0, 'G']):
            estadoaux = copy.deepcopy(self.estado)
            estadoaux[posicion - 1] = 'U'
            if(self.estado[posicion]) != 'S':
                estadoaux[posicion] = 2
            nodoaux = NodoCamino(self, estadoaux, 3)
            sucesores.append(nodoaux)
        return sucesores

    def calcular_costo(self):
        if self.padre is None:
            self.costo = 0
        elif self.operador == self.padre.operador:
            self.costo = self.padre.costo + 1
        else:
            self.costo = self.padre.costo + 2

    def calcular_heuristica(self):
        if 'G' in self.estado and 'U' in self.estado:
            self.heuristica = (abs(self.get_X('G') - self.get_X('U')) +
                    abs(self.get_Y('G') - self.get_Y('U')))
        elif 'G' in self.estado:
            self.heuristica = (abs(self.get_X('G') - self.get_X('S')) +
                    abs(self.get_Y('G') - self.get_Y('S')))
        else:
            self.heuristica = 0

    def get_X(self, letra):
        return (self.estado.index(letra) // 8) + 1

    def get_Y(self, letra):
        return (self.estado.index(letra) % 8) + 1

    def crear_frame(self, contenedor):
        operadores = ['↑', '→', '↓', '←']
        frame = Frame(contenedor, width="350", height="244")
        for fila in range(0, 8):
            for columna in range(0, 8):
                pos = columna + (8 * fila)
                if self.estado[pos] is 0:
                    Button(frame, text="", width=2, height=1,
                        bg="white").grid(row=fila, column=columna)
                elif self.estado[pos] is 1:
                    Button(frame, text="", width=2, height=1,
                        bg="black").grid(row=fila, column=columna)
                elif self.estado[pos] is 2:
                    padres = self.padre
                    while padres.estado[pos] != 'U':
                        padres = padres.padre
                    Button(frame, text=operadores[padres.operador], width=2,
                        height=1, bg="white").grid(row=fila, column=columna)
                elif self.estado[pos] is 'S':
                    Button(frame, text="S", width=2, height=1,
                        bg="white").grid(row=fila, column=columna)
                elif self.estado[pos] is 'G':
                    Button(frame, text="G", width=2, height=1,
                        bg="white").grid(row=fila, column=columna)
                else:
                    Button(frame, text="U", width=2, height=1,
                        bg="white").grid(row=fila, column=columna)
        Label(frame, text="Profundidad: " + str(self.profundidad)).grid(row=9,
            column=0, columnspan=8)
        frame.grid_propagate(False)
        return frame

    def crear_estado_inicial(self, contenedor):
        self.estado = [0, 0, 0, 0, 0, 0, 0, 0,
                      0, 0, 0, 0, 0, 0, 0, 0,
                      0, 0, 0, 0, 0, 0, 0, 0,
                      0, 0, 0, 0, 0, 0, 0, 0,
                      0, 0, 0, 0, 0, 0, 0, 0,
                      0, 0, 0, 0, 0, 0, 0, 0,
                      0, 0, 0, 0, 0, 0, 0, 0,
                      0, 0, 0, 0, 0, 0, 0, 0]
        self.botones = []
        self.opcion_seleccionada = 3
        frame = Frame(contenedor)
        for fila in range(0, 8):
            for columna in range(0, 8):
                self.botones.append(Button(frame, text="", width=2,
                    height=1, bg="white"))
                self.botones[-1].grid(row=fila, column=columna)
        Label(frame, text="Opciones:").grid(row=8, columnspan=8)
        self.botones.append(Button(frame, text="", width=2,
            height=1, bg="black"))
        self.botones[-1].grid(row=9, column=2)
        self.botones.append(Button(frame, text="S", width=2,
            height=1, bg="white"))
        self.botones[-1].grid(row=9, column=3)
        self.botones.append(Button(frame, text="G", width=2,
            height=1, bg="white"))
        self.botones[-1].grid(row=9, column=4)
        self.botones.append(Button(frame, text="", width=2,
            height=1, bg="white"))
        self.botones[-1].grid(row=9, column=5)
        for boton in range(0, 68):
            # Con el boton=boton guarda el valor de la iteracion en el momento
            # que definimos el lambda =D. Es el truco magico!
            self.botones[boton].config(
                command=lambda boton=boton: self.pulsar(boton))
        return frame

    def pulsar(self, posicion):
        if posicion < 64:
            if self.opcion_seleccionada == 0:
                self.botones[posicion].config(text="", bg="black")
                self.estado[posicion] = 1
            elif self.opcion_seleccionada == 1 and not 'S' in self.estado:
                self.botones[posicion].config(text="S", bg="white")
                self.estado[posicion] = 'S'
            elif self.opcion_seleccionada == 2 and not 'G' in self.estado:
                self.botones[posicion].config(text="G", bg="white")
                self.estado[posicion] = 'G'
            elif self.opcion_seleccionada == 3:
                self.botones[posicion].config(text="", bg="white")
                self.estado[posicion] = 0
        elif posicion == 64:
            self.opcion_seleccionada = 0
        elif posicion == 65:
            self.opcion_seleccionada = 1
        elif posicion == 66:
            self.opcion_seleccionada = 2
        elif posicion == 67:
            self.opcion_seleccionada = 3