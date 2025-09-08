def crear_alumno(**kwargs):
    for clave, valor in kwargs.items():
        print(f'{clave}: {valor}')


crear_alumno(nombre='Alex', edad=25)

# Ej 1) Función para calcular la media
def suma(*args):
    return sum(args)

def media(*args):
    return suma(*args) / len(args)

print(media(1, 2, 6))