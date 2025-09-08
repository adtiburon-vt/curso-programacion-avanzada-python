def contador(f):
    llamadas = 0
    def wrapper(*args, **kwargs):
        nonlocal llamadas
        llamadas +=1
        print(f'Se ha llamado {llamadas} veces')
        return f(*args, **kwargs)
    
    return wrapper

@contador
def f():
    return 

f()
f()
f()