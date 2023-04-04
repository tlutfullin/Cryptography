import random
import math

def initial_values(L):

    random.seed(17)
    rand_initial = []
    for i in range(L):
        rand_initial.append(random.randint(0,19)//10)

    with open('key_binary.txt', 'w', encoding='utf-8') as file:
        for item in rand_initial:
            file.write(str(item))

    return rand_initial

def LFSR(P, M, N, K):

    S = initial_values(23)
    def LFSR2():
        seq, st = [S[-1]], S
        for j in range(K ** len(S) - 2):
            st0 = sum([i * j for i, j in zip(st, P[1:])]) % K
            st = [st0] + st[:-1]
            seq += [st[-1]]
        return seq

    assert len(P) > 1 and len(P) - 1 == len(S)
    s = LFSR2()
    L = len(s)
    assert M <= L
    sequence_m = [s[i % L] if M == 1 else (s[i % L:] + s[:i % L])[:M] for i in range(N)]

    with open('key.txt', 'w') as file:
        for item in sequence_m:
            file.write(str(item))

    return sequence_m


def serial_test(m, k):

    #количество непересекающихся серий
    n_selial = len(m)/k
    # группы серий
    serial_group = [m[i:i + int(k)] for i in range(0, len(m), int(k))]
    #print(f'Серии длиной {k} последовательных бит: {serial_group}')

    #словарь для хранения эмпирических частот
    dict_frequency = dict()
    for i in serial_group:
        # ключ словаря - хэшируемый объект
        m1 = tuple(i)
        dict_frequency[m1] = serial_group.count(i)

    #print(f'Частота серии {dict_frequency}')

    # теоретические частота каждой комбинации
    theory_frequency = n_selial / pow(2.0, k)

    print(f'Теоретическая вероятность реализации: {theory_frequency:.4f}')

    # значения эмпирических частот
    empirical_frequency = list(dict_frequency.values())

    #заполнить нулями до
    while len(empirical_frequency) < pow(2, k):
        empirical_frequency.append(0)

    print(f'Эмпирические частоты серии: {empirical_frequency}')

    # подсчет статистики хи-2
    statistics_hi = 0
    for i in empirical_frequency:
        statistics_hi += pow((i - theory_frequency), 2.0) / theory_frequency
    print(f'Критерий хи-2 Пирсона: {statistics_hi:.4f}')

    # критические уровни статистика для а = 0.05
    dict_hi = {'k2':[0.584, 6.251 ], 'k3':[2.833, 12.017], 'k4':[8.547, 22.307 ]}

    #
    k_number = list(dict_hi.values())[k-2]

    if statistics_hi>= k_number[0] and statistics_hi<= k_number[1]:
        print(f'Для уровня значимости а=0,9 и a=0.1 при k={k}: {k_number[0]} < {statistics_hi:.3f} < {k_number[1]} - Тест пройден')

    else:
        print(f'Для уровня значимости а=0,9 и a=0.1 и k={k}: {k_number[0]} < {statistics_hi:.3f} < {k_number[1]} - Тест не пройден')


# корреляционный тест
def correlation_test(m, k):
    print(f'Корреляционный тест для k-{k}:')
    global N
    N = len(m)

    def moments(m, k):
        moment_0 = 0
        moment_k = 0

        for i in range(1, N-k):
            moment_0 += m[i]

        for j in range(k+1, N):
            moment_k += m[j]

        moment_0 = moment_0 /(N-k)
        moment_k = moment_k /(N-k)
        return moment_0, moment_k

    def variance(m, k):
        moment_0 = float(moments(m,k)[0])
        moment_k = float(moments(m, k)[1])

        variance_0 = 0
        variance_k = 0

        for i in range(1, N-k):
            variance_0 += (m[i]- moment_0 )**2

        for j in range(k+1, N):
            variance_k += (m[i] - moment_k)**2

        variance_0 = variance_0/(N-k-1)
        variance_k = variance_k/(N- k -1)

        return variance_0, variance_k

    moment_0 = float(moments(m, k)[0])
    moment_k = float(moments(m, k)[1])
    variance_0 = float(variance(m, k)[0])
    variance_k = float(variance(m, k)[1])

    autocorrelation  = 0

    for i, j in zip(range(1, N-k), range(k + 1, N)):
        autocorrelation  += ( (int(m[i]) - moment_0) * (int(m[j]) - moment_k) ) / (math.sqrt( variance_0 * variance_k))

    autocorrelation  = autocorrelation /(N-k)
    print(f'Коэффициент автокорреляции: {autocorrelation:.5f}')

    critical_r = 1/(N-1) + 2/(N-2)*math.sqrt((N*(N-3))/(N+1))
    print(f'Критический уровень статистики: {critical_r:.5f}')

    if math.fabs(autocorrelation) <= critical_r:
        print(f'Для уровня значимости а=0,05 и k={k} - корреляционный тест пройден')

    else:
        print(f'Для уровня значимости α=0,05 и k={k} - корреляционный тест не пройден')




def encryption_text():

    # считываем м-последовательность
    with open('key.txt', 'r') as f:
        key = f.read()

    # переводим ключ в итерируемый объект, состоящей из 0 и 1
    key = [int(i) for i in key]

    # считываем файл в бинарном виде
    with open('text.txt', 'rb') as f:
        binary_data = f.read()

    # шифрования файла
    encrypted_data = bytearray(len(binary_data))

    for i in range(len(binary_data)):
        encrypted_data[i] = binary_data[i] ^ key[i]

    # запись шифрованного файла в бинарный файл
    with open('text_encrypted.txt', 'wb') as f:
        f.write(encrypted_data)


    # преобразуем исходный файл в 0 и 1,
    binary_data_test = [bin(i)[2:] for i in encrypted_data ]
    str_binary_data = ''.join(binary_data_test)
    array_binary_data = [int(i)  for i in str_binary_data]

    array_binary_data = [i^j for  i,j in  zip(array_binary_data,key)]


    # проверяем зашифрованный  файл на тесты:

    # сериальный тест:
    for k in [2,3,4]:
        print(serial_test(m=array_binary_data, k=k))

    # # корреляционный тест:
    for k in [1, 2, 8, 9]:
        print(correlation_test(m=array_binary_data, k=k))



def decryption_text():
    # считываем м-последовательность
    with open('key.txt', 'r') as f:
        key = f.read()

    # переводим ключ в итерируемый объект, состоящей из 0 и 1
    key = [int(i) for i in key]

    # считываем файл в бинарном виде
    with open('text_encrypted.txt', 'rb') as f:
        binary_data = f.read()

    encrypted_data = bytearray(len(binary_data))

    for i in range(len(binary_data)):
        encrypted_data[i] = binary_data[i] ^ key[i]

    # запись расшифрованного файла в бинарник
    with open('text_dencrypted.txt', 'wb') as f:
        f.write(encrypted_data)




polinom = [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1]


m = LFSR(P=polinom, M=1, N=600000, K=2)



