class A:
    def accion(self):
        print("A empieza")
        super().accion()
        print("A termina")

class B(A):
    def accion(self):
        print("B empieza")
        super().accion()
        print("B termina")

class C(A):
    def accion(self):
        print("C empieza")
        super().accion()
        print("C termina")

class D(B, C):
    def accion(self):
        print("D empieza")
        super().accion()
        print("D termina")

# ---- Ejecutamos ----
d = D()
d.accion()

print("MRO:", D.mro())
