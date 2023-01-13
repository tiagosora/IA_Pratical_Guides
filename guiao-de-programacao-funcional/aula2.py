#Exercicio 4.1
import math


def impartest(x):
    if int(x)%2 == 0:
        return False
    return True
impar = lambda x: impartest (x)
# impar = lambda x : x%2 == 1


#Exercicio 4.2
def positivotest(x):
    if x > 0:
        return True
    return False
positivo = lambda x: positivotest (x)
# positivo = lambda a:a >= 0

#Exercicio 4.3
def comparar(x, y):
    if abs(x) < abs(y):
        return True
    return False
comparar_modulo = lambda x, y: comparar (x, y)
# comparar_modulo = lambda x, y : abs(x) < abs(y)

#Exercicio 4.4
def tratar(x, y):
    r = math.sqrt(pow(x,2)+pow(y,2))
    o = math.atan2(y,x)
    return (r, o)
cart2pol = lambda x, y: tratar (x, y)

#Exercicio 4.5
ex5 = lambda f, g, h: lambda x, y, z: h(f(x, y), g(y, z))

#Exercicio 4.6
def quantificador_universal(lista, f):
    if lista == []:
        return True
    
    if f(lista[0]):
        return quantificador_universal(lista[1:], f)

#Exercicio 4.8
def subconjunto(lista1, lista2):
    if lista1 == []:
        return True
    
    if lista1[0] in lista2:
        return subconjunto(lista1[1:], lista2)

    return False

#Exercicio 4.9
def ordem(lista, f):
    if lista[1:] == []:
        return lista[0]
    
    menor = ordem(lista[1:], f)

    if f(lista[0], menor):
        return (lista[0])
    else:
        return (menor)

#Exercicio 4.10
def filtrar_ordem(lista, f):
    if lista[1:] == []:
        return lista[0], []
    
    menor, resto = filtrar_ordem(lista[1:], f)

    if f(lista[0], menor):
        return lista[0], resto + [menor]
    else:
        return menor, [lista[0]] + resto

#Exercicio 5.2
def ordenar_seleccao(lista, ordem):
    if lista == []:
        return []

    menor, resto = filtrar_ordem(lista, ordem)

    return [menor] + ordenar_seleccao(resto, ordem)