from tkinter import *
from busqueda import *
from nodos import *

class Sistema(object):
    def __init__(self):
        self.ventana = Tk()
        self.ventana.title("Sistemas Inteligentes")
        self.ventana.geometry("550x400")
        self.frame1 = Frame(self.ventana)
        self.frame1.pack(side=TOP)
        (Label(self.frame1, text="Seleccione un juego").
            grid(row=1, column=1, columnspan=2))
        Button(self.frame1, text="Camino", width=15, height=1,
            command=lambda: self.pulsar(1)).grid(row=2, column=1)
        Button(self.frame1, text="N Reinas", width=15, height=1,
            command=lambda: self.pulsar(2)).grid(row=2, column=2)
        self.frame2 = Frame(self.ventana)
        self.frame2.pack(side=LEFT)
        Label(self.frame2, text="Seleccione una Búsqueda").pack()
        Button(self.frame2, text="Profundidad", width=15, height=1,
            command=lambda: self.pulsar(3)).pack()
        Button(self.frame2, text="Anchura", width=15, height=1,
            command=lambda: self.pulsar(4)).pack()
        Button(self.frame2, text="Costo", width=15, height=1,
            command=lambda: self.pulsar(5)).pack()
        Button(self.frame2, text="Prof. Informada", width=15, height=1,
            command=lambda: self.pulsar(6)).pack()
        Button(self.frame2, text="Best First", width=15, height=1,
            command=lambda: self.pulsar(7)).pack()
        Button(self.frame2, text="A*", width=15, height=1,
            command=lambda: self.pulsar(8)).pack()
        self.frame3 = Frame(self.ventana)
        self.frame3.pack(side=RIGHT)
        self.imput = None
        self.inicial = None
        self.juego_seleccionado = None
        self.ventana.mainloop()

    def pulsar(self, boton):
        if boton is 1:
            self.inicial = None
            self.juego_seleccionado = 1
            self.inicial = NodoCamino(None, [], None)
            self.frame3.destroy()
            self.frame3 = self.inicial.crear_estado_inicial(self.ventana)
            self.frame3.pack(side=RIGHT)
        elif boton is 2:
            self.inicial = None
            self.juego_seleccionado = 2
            self.frame3.destroy()
            self.frame3 = Frame(self.ventana)
            self.frame3.pack(side=RIGHT)
            Label(self.frame3, text="Ingrese la cantidad de Reinas").pack()
            self.imput = Entry(self.frame3)
            self.imput.pack()
            Button(self.frame3, text="OK", width=5, height=1,
                command=lambda: self.pulsar(9)).pack()
        elif boton is 9 and not self.imput.get() is '':
            self.inicial = NodoReina(None, [], int(self.imput.get()))
            self.frame3.destroy()
            self.frame3 = Frame(self.ventana)
            self.frame3.pack(side=RIGHT)
        elif (boton > 2 and ((self.juego_seleccionado is 1
            and 'G' in self.inicial.estado and 'S' in self.inicial.estado)
            or (self.juego_seleccionado is 2 and not self.inicial is None))):
                if boton is 3:
                    busqueda = Profundidad(self.inicial)
                elif boton is 4:
                    busqueda = Anchura(self.inicial)
                elif boton is 5:
                    busqueda = CostoUniforme(self.inicial)
                elif boton is 6:
                    busqueda = ProfundidadInformada(self.inicial)
                elif boton is 7:
                    busqueda = BestFirst(self.inicial)
                elif boton is 8:
                    busqueda = AEstrella(self.inicial)
                busqueda.cronometro(busqueda.buscar)
                self.frame3.destroy()
                self.frame3 = busqueda.crear_frame(self.ventana)
                self.frame3.pack(side=RIGHT)


if __name__ == "__main__":
    sist = Sistema()