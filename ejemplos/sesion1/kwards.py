def crear_alumno(**kwargs):
    for clave, valor in kwargs.items():
        print(f"{clave}: {valor}")

crear_alumno(no)
# nombre: Ana
# edad: 30
# ciudad: Madrid




def ejecutar(func, *args, **kwargs):
    otel.trace()
    func(*args,**kwargs)
    otel.trace()