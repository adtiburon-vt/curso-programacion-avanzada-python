from abc import ABC, abstractmethod

class Vehiculo(ABC):
    @abstractmethod
    def mover(self):
        pass

class Coche(Vehiculo):
    contador = 0

    def __init__(self, marca, modelo):
        self.marca: str = marca
        self.modelo: str = modelo
        self.aumentar_contador()

    def descripcion(self):
        return f'{self.marca} {self.modelo}'
    
    @classmethod
    def aumentar_contador(cls):
        cls.contador += 1

    def mover(self):
        print('Brum bruuum')


class Moto(Vehiculo):
    def mover(self):
        return super().mover()


i1 = Coche("", "")
i1.contador = 0
i2 = Coche("", "")
print(i1.contador, i2.contador, Coche.contador)
i2.mover()

class Producto:
    def __init__(self, nombre, precio):
        self._precio = precio
        self.nombre = nombre

    @property
    def precio(self):
        return self._precio

    @precio.setter
    def precio(self, nuevo_precio):
        if nuevo_precio < 0:
            raise ValueError("El precio no puede ser negativo")
        self._precio = nuevo_precio

p = Producto('', 0)
print(p.precio)
p.precio = -1