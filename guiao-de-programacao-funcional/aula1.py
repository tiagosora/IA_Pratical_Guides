#Exercicio 1.1
from unittest import result
from xml.dom.minidom import Element


def comprimento(lista):
	if lista == []: return 0
	return(1 + comprimento(lista[:-1])) 

#Exercicio 1.2
def soma(lista):
    if lista == []:	return 0
    return(lista[0] + soma(lista[1:]))

#Exercicio 1.3
def existe(lista, elem):
	if lista == []: return False
	
	if lista[0] == elem: return True
	else: return(existe(lista[1:], elem))

#Exercicio 1.4
def concat(l1, l2):
	if l2 == []: return []
	return l1 + [l2[0]] + concat([], l2[1:])

#Exercicio 1.5
def inverte(lista):
	if lista == []: return []
	return [lista[-1]] + inverte(lista[:-1])

#Exercicio 1.6
def capicua(lista):
	if lista == []: return True
	if lista[0] == lista[-1]: return capicua(lista[1:-1])
	return False

#Exercicio 1.7
def concat_listas(lista):
	if lista == []: return []

	return [x for x in lista[0]] + concat_listas(lista[1:])

#Exercicio 1.8
def substitui(lista, original, novo):
	if lista == []: return []
	
	if lista[0] == original: 
		return [novo] + substitui(lista[1:], original, novo)
	else: 
		return [lista[0]] + substitui(lista[1:], original, novo)

#Exercicio 1.9
def fusao_ordenada(lista1, lista2):
	if lista1 == []: return lista2
	if lista2 == []: return lista1

	if (lista1[0] < lista2[0]): return [lista1[0]] + fusao_ordenada(lista1[1:], lista2)
	else: return [lista2[0]] + fusao_ordenada(lista1, lista2[1:])
		

#Exercicio 1.10
def lista_subconjuntos(lista):
	if lista == []:
		return [[]]
	
	ll = lista_subconjuntos(lista[1:])

	return [[lista[0]] + l for l in ll] + ll
# print(lista_subconjuntos([1,2,3]))

#Exercicio 2.1
def separar(lista):
	if lista == []: return ([],[])

	par = separar(lista[1:])
	return ([lista[0][0]]+par[0], [lista[0][1]]+par[1])

#Exercicio 2.2
def remove_e_conta(lista, elem):
	if lista == []: return ([], 0)

	novalista, ocorrencias = remove_e_conta(lista[1:], elem)

	if lista[0] == elem: 
		return novalista, ocorrencias + 1
	return [lista[0]] + novalista, ocorrencias

#Exercicio 3.1
def cabeca(lista):
	if lista == []: return None
	return lista[0]

#Exercicio 3.2
def cauda(lista):
	if len(lista) < 2: return None
	return lista[-1]

#Exercicio 3.3
def juntar(l1, l2):
	if len(l1) != len(l2): return None
	if l1 == []: return None

	result = juntar(l1[1:],l2[1:])
	if result:
		return [(l1[0], l2[0])] + [x for x in result]
	else:
		return [(l1[0], l2[0])]
    		
#Exercicio 3.4
def menor(lista):
	if lista == [] : return None
	result = menor(lista[1:])
	if result != None and result < lista[0]:
		return result
	return lista[0]

#Exercicio 3.6
def max_min(lista):
	pass
