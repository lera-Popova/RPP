# Задание 1.1
a = int(input('Первое число'))
b = int(input('Второе число'))
c = int(input('Третье число'))
if b>= a <=c:
     print(a)
elif a >= b <= c:
     print(b)
elif a >= c <=b:
     print(c)


# Задание 1.2
a = int(input('Введите первое число'))
b = int(input('Введите второе число'))
c = int(input('Введите третье число'))
if a >= 1 and a <= 50:
   print(a)
if b >= 1 and b <= 50:
   print(b)
if c >= 1 and c <= 50:
   print(c)

# Задание 1.3
m = float(input('Введите вещественное число: '))
for x in range(1, 11):
   print(x*m)
# Задание 1.4
a = 0
b = 0
num = int(input('Введите число: '))
while num != 0:
   a += num
   b += 1
   num = int(input('Введите число: '))
print('Сумма: ', a)
print('Количество: ', b)


# Задание 2
phrase = input("Введите строку: ")
x = phrase.replace(":", "%")
print(x)
count = 0
for i in x:
   if i == '%':
      count += 1
print(count)

# Задание 3
masiv = [int(x) for x in input().split()]
print(masiv)
print(min(masiv))
resul = [i for i, j in enumerate(masiv) if j == min(masiv)]
print(resul)
print(lambda x : x > 0, masiv)
print(lambda x : x < 0, masiv)