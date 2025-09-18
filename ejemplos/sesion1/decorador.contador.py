def contador(func):
    llamadas = 0

    def wrapper(*args,**kwargs):
        nonlocal llamadas
        llamadas += 1
        print(f"La funcion {func.__name__}" se ha llamado {llamadas} veces")
        return func(*args, **kwargs)
    return wrapper