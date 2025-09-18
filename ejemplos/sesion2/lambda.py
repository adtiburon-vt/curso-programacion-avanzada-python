



nums = [1,2,3,4,5]


cuadrados = list(map(lambda x: x * x,nums))   #  [1,3,9,16,25]


#  [ expresionlogica for elemento in iterable if condicion ]

cuadrados = [x*x for x in nums]  #  [1,3,9,16,25]





matriz = [[1,2,3],[4,5,6],[7,8,9]]


plana = []
for fila in matriz:
    for num in fila:
        plana.append(num)


plana # [1,2,3,4,5,6,7,8,9]


plana = [num for fila in matriz for num in fila]


aplanar = lambda matriz: [num for fila in matriz for num in fila]




A = [1,2,3]
B = ['a','b','c']


pares = [(x,y) for x in A for y in B]


[(1,'a'),(1,'b'),(2,'a'),(2,'b'),(3,'a'),(3,'b')]



