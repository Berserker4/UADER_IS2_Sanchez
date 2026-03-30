#!/usr/bin/python3
# Programa: listado de números primos en el intervalo cerrado [lower, upper].

# Límite inferior e superior (inclusive) del rango a analizar.
lower = 1
upper = 500

print("Prime numbers between", lower, "and", upper, "are:")

# Se prueba cada entero del intervalo como posible primo.
for num in range(lower, upper + 1):
   # Los primos son mayores que 1.
   if num > 1:
       # Búsqueda de un divisor propio entre 2 y num-1.
       for i in range(2, num):
           if (num % i) == 0:
               break
       else:
           # El else del for solo corre si no hubo break: num es primo.
           print(num)
