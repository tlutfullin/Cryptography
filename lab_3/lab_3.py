import random
import time
from random import randrange
from matplotlib import pyplot as plt



# 50 простых чисел от 2
first_50_primes = [3, 5, 7, 11, 13, 17, 19, 23, 29, 31,
                   37, 41, 43, 47, 53, 59, 61, 67, 71, 73,
                   79, 83, 89, 97, 101, 103, 107, 109, 113, 127,
                   131, 137, 139, 149, 151, 157, 163, 167, 173, 179,
                   181, 191, 193, 197, 199, 211, 223, 227, 229, 233]

random.seed(17)
# генерация случайного целого числа [2 ** (n - 1) + 1, 2 ** n]
def generate_n_bit_odd(n: int):

    assert n > 1
    return randrange(2 ** (n - 1) + 1, 2 ** n, 2)


# слабый тест на проверку числа на простоту
def get_lowlevel_prime(n):

    while True:

        c = generate_n_bit_odd(n)

        # проверяем является ли число простым, путем деления простых чисел из first_50_primes
        for divisor in first_50_primes:
            if c % divisor == 0 and divisor ** 2 <= c:
                break
        else:

            return c

# тест Миллера - Рабина на проверку числа на простоту, по дефолту 20 итерации
def miller_rabin_primality_check(n, k=20):

    assert n > 3
    if n % 2 == 0:
        return False

    s, d = 0, n - 1
    while d % 2 == 0:
        d >>= 1
        s += 1

    for _ in range(k):
        a = randrange(2, n - 1)
        x = pow(a, d, n)

        if x == 1 or x == n - 1:
            continue

        for _ in range(s):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False

    return True

# простое число после всех тестов
def get_random_prime(num_bits):
    while True:
        pp = get_lowlevel_prime(num_bits)
        if miller_rabin_primality_check(pp):
            return pp


# Алгоритм Евклида
def gcd(a, b):

    while b:
        a, b = b, a % b
    return a

# Наибольший общий делитель
def lcm(a, b):
    return a // gcd(a, b) * b

# расширенный алгоритм Евклидова
def exgcd(a, b):

    old_s, s = 1, 0
    old_t, t = 0, 1
    while b:
        q = a // b
        s, old_s = old_s - q * s, s
        t, old_t = old_t - q * t, t
        a, b = b, a % b
    return a, old_s, old_t

# находит модульное обратное число
def invmod(e, m):
    g, x, y = exgcd(e, m)
    assert g == 1

    if x < 0:
        x += m
    return x

# переводит число в байты
def uint_to_bytes(x: int) -> bytes:
    if x == 0:
        return bytes(1)
    return x.to_bytes((x.bit_length() + 7) // 8, 'big')


# переводит байты в целые числа
def uint_from_bytes(xbytes: bytes) -> int:
    return int.from_bytes(xbytes, 'big')


RSA_DEFAULT_EXPONENT = 65537
RSA_DEFAULT_MODULUS_LEN = 2048


class RSA:

    def __init__(self, key_length=RSA_DEFAULT_MODULUS_LEN,
                 exponent=RSA_DEFAULT_EXPONENT):
        self.e = exponent
        self.key_length = key_length

        t = 0
        p = q = 2

        # генерируем два простых числа
        while gcd(self.e, t) != 1:
            p = get_random_prime(key_length // 2)
            q = get_random_prime(key_length // 2)
            t = lcm(p - 1, q - 1)

        # модуль шифрования
        self.n = p * q
        # находит модульное обратное число
        self.d = invmod(self.e, t)

    # метод для записи открытого и закрытого ключа
    def write_key(self):
        with open('public.txt', 'w', encoding='utf-8') as f:
            f.write(f'{self.e} {self.n}')

        with open('private.txt', 'w', encoding='utf-8') as f:
            f.write(f'{self.d} {self.n}')

    # метод для  перевода из бинарного в целое число
    def dec_to_bin(self, x):
        return int(bin(x)[2:])

    # метод шифрования текста
    def encrypt(self, binary_data):
        # длина ключа
        L = self.key_length

        # cчитывание ключа
        with open('public.txt', 'r') as f:
            public_text = f.read()

        tem = [int(s) for s in public_text.split() if s.isdigit()]
        e = int(tem[0])
        N = int(tem[1])

        # преобразование ascii в бинарный вид
        array_text_ascii = [ord(k) for k in binary_data]
        for i in range(len(array_text_ascii)):
            array_text_ascii[i] = self.dec_to_bin(array_text_ascii[i])

        # дополняем блоки до L/4
        i = 0
        if len(binary_data) % (L / 32) != 0:
            while i < (L / 32) - len(binary_data) % (L / 32):
                array_text_ascii.append(0)
                i += 1

        # преобразуем строку
        text_bin = ""
        for i in range(len(array_text_ascii)):
            if array_text_ascii[i] == 0:
                text_bin += "00000000"
            elif array_text_ascii[i] < self.dec_to_bin(64):
                text_bin += "00"
                text_bin += str(array_text_ascii[i])
            else:
                text_bin += "0"
                text_bin += str(array_text_ascii[i])

        l = len(array_text_ascii) * 8

        block_text = array_text_ascii
        block_text.clear()
        block = ""

        # делим файл на равные L/4 блока
        i = 0

        while i < l:
            block += text_bin[i]
            if len(block) == L / 4:
                block_text.append(int(block, 2))
                block = ""
            i += 1

        lenN = len(bin(N)[2:])

        encrypted_block = []
        len_block = len(block_text)
        i = 0

        # шифруем блоки и переводим в бинарный вид
        while i < len_block:
            encrypted_block.append(bin(pow(int(block_text.pop(0)), e, N))[2:])
            block = lenN - len(encrypted_block[i])
            encrypted_block[i] = "0" * block + encrypted_block[i]
            i += 1
        encrypted_write = ""

        i = 0
        while i < len_block:
            encrypted_write += str(encrypted_block.pop(0))
            i += 1

        # запись зашифрованного текста в файл
        with open('encrypted.txt', 'w') as f:
            f.write(encrypted_write)

        return encrypted_write

    # метод дешифрования текста
    def decrypt(self, encrypted_int_data: int):

        # cчитывание ключа
        with open('private.txt', 'r') as f:
            private_text = f.read()

        tem = [int(s) for s in private_text.split() if s.isdigit()]
        d = int(tem[0])
        N = int(tem[1])
        L = self.key_length

        with open('encrypted.txt', 'r') as f:
            encrypted_text = f.read()

        lenN = len(bin(N)[2:])
        i = 0
        decrypted_block = []
        temp = ""

        # расшифрования блока
        while i < len(encrypted_text):
            temp += encrypted_text[i]
            if len(temp) == lenN:
                decrypted_block.append(bin(pow(int(temp, 2), d, N))[2:])

                temp = ""
            i += 1

        i = 0
        temp_string = ""
        while i < len(decrypted_block):
            a = int(L / 4) - len(decrypted_block[i])
            decrypted_block[i] = "0" * a + decrypted_block[i]
            temp_string += decrypted_block[i]
            i += 1

        temp = ""
        i = 0
        array_ascii = []

        # преобразование бинарного вида в ascii
        while i < len(temp_string):
            temp += temp_string[i]
            if len(temp) == 8:
                array_ascii.append(int(temp, 2))
                temp = ""
            i += 1

        decrypted_text = ""
        k = 0
        while k < len(array_ascii):
            decrypted_text += chr(array_ascii[k])
            k += 1

        with open('decrypted.txt', 'w') as f:
            f.write(decrypted_text)

        return decrypted_text

    def attack(self):

        # считываем открытый ключ
        with open('public.txt', 'r') as f:
            public_key = f.read()

        temp = [int(s) for s in public_key.split() if s.isdigit()]
        N = int(temp[1])

        # разложение чисел на множители методом p эвристики Полларда
        x = 2
        y = 1;
        i = 0;
        st = 2

        # время выполнения кода
        start = time.time()
        while gcd(N, abs(x - y)) == 1:
            if i == st:
                y = x
                st = st * 2
            x = (x * x + 1) % N
            i += 1
        p = gcd(N, abs(x - y))

        end = time.time()

        q = int(N / p)

        print(f'Найденные числа p={p}, q={q} время поиска составило {(end - start) * 1000}ms')

    def graph_attack(self, L):
        time_factorization = []

        for i in L:
            p = get_random_prime(i // 2)
            q = get_random_prime(i // 2)
            N = p * q

            # разложение чисел на множители методом p эвристики Полларда
            x = 2
            y = 1
            i = 0
            st = 2

            # время выполнения кода
            start = time.time()
            while gcd(N, abs(x - y)) == 1:
                if i == st:
                    y = x
                    st = st * 2
                x = (x * x + 1) % N
                i += 1
            p = gcd(N, abs(x - y))

            end = time.time()
            time_func = end - start

            time_factorization.append(time_func)

        plt.figure(figsize=(15, 10))

        plt.title('График зависимости времени факторизации от длины ключа', fontsize=14, color='green',
                  loc='center')

        # названия меток к осям: x и y
        plt.ylabel('Time,ms', loc='center', color='blue', fontsize=14)
        plt.xlabel('L, bit', loc='center', fontsize=14)

        plt.plot(L, time_factorization, 'r')

        plt.show()

    def graph_factorization(self):
        len_max = 100
        # хранения простых чисел:
        p_array = []
        q_array = []
        time_factorization = []
        r = 0.25
        while r <= 0.5:
            p = get_random_prime(int(len_max * r / 2))
            q = get_random_prime(int(len_max * (1 - r) / 2))
            N = p * q

            # разложение чисел на множители методом p эвристики Полларда
            x = 2
            y = 1;
            i = 0;
            st = 2

            # время выполнения кода
            start = time.time()
            while gcd(N, abs(x - y)) == 1:
                if i == st:
                    y = x
                    st = st * 2
                x = (x * x + 1) % N
                i += 1
            p = gcd(N, abs(x - y))

            end = time.time()
            time_func = end - start
            time_factorization.append(time_func)
            r += 0.025

        list_r = [0.5 + 0.025 * i for i in range(10)]

        plt.figure(figsize=(15, 10))

        plt.title('График зависимости времени факторизации числа n = p⋅q от r', fontsize=14, color='green',
                  loc='center')

        # названия меток к осям: x и y
        plt.ylabel('Время,ms', loc='center', color='blue', fontsize=14)
        plt.xlabel('r', loc='center', fontsize=14)

        plt.plot(list_r, time_factorization, 'r')

        plt.show()



# экземпляр класса
rsa= RSA(512, 3)

# запись ключей в файл
#rsa.write_key()

rsa.attack()


# text = 'Since deep learning and machine learning tend to be used interchangeably, its worth noting the nuances between the two. Machine learning, deep learning, and neural networks are all sub-fields of artificial intelligence. However, neural networks is actually a sub-field of machine learning, and deep learning is a sub-field of neural networks. The way in which deep learning and machine learning differ is in how each algorithm learns. '
# print(f'Исходный текст: {text}')
# encrypt_text = rsa.encrypt(text)
# print(f'Зашифрованный текст: {encrypt_text[:1000]}')
#
# decrypt_text = rsa.decrypt(encrypt_text)
# print(f'Расшифрованный текст: {decrypt_text}')


