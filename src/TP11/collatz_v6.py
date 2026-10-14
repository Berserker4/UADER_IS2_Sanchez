#Calculando el número de iteraciones del algoritmo de Collatz
def collatz(num):
  if num < 1 or num > 1999:
    raise ValueError("el número debe estar entre 1 y 1999")
  iteraciones = 0
  while num != 1:
    if num % 2 == 0:
      num = num // 2
    else:
      num = 3*num + 1
    iteraciones += 1
  return iteraciones
#Comprobando los resultados
i=20
print("El número de iteraciones para %d es %d\n" % (i,collatz(i)))
