import re


# patron para obtener letras seguidas.
pat = re.compile(r"[A-Za-z]+")


m1 = pat.match("Hola Mundo")


print(m1.group())     #     Hola


m2 = pat.match("  Hola Mundo")

print()    # none 


email = re.compile()