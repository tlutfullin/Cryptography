import random
import re
from collections import Counter
import math

frequency_simbol = ' оеаитнсрвлкмдпуяызбгьчйхжюшцщэъф'
alphabet = 'абвгдежзийклмнопрстуфхцчшщъыьэюя '

bigramm_frequency = ['ов', 'ст', 'но', 'ко', 'ен', 'во', 'ро', 'то', 'го', 'по']

with open('text.txt', 'r', encoding='utf-8') as f:
    text = f.read()

#print(text)


# подсчет количества N - грамм в тексте:
def ngrams(text, n):
    # удаление знаков препинания и цифр, перевод в нижний регистр
    text = re.sub(r'[.,"\'-?:!;0-9]', '', text)
    text = text.lower()
    len_text = len(text)

    # список всех n - грамм
    list_ngrams = []
    for i in range(len_text-n +1):
        list_ngrams.append(text[i:i+n])

    # словарь: ключ - n-грамма, значение - частота
    ngrams_frequency = Counter(list_ngrams)
    # упорядочиваем словарь
    ngrams_frequency = dict(sorted(ngrams_frequency.items(), key=lambda item: item[1], reverse=True))

    return ngrams_frequency


# создания ключа шифрования
def key_encryption(alphabet):

    random.seed(17)
    list_alphabet = [i for i in alphabet]
    # перемешиваем алфавит
    list_alphabet_random = random.sample(list_alphabet, len(list_alphabet))

    # словарь замены
    dict_encryption = {list_alphabet[i]: list_alphabet_random[i]  for i in range(len(list_alphabet))}

    with open('key.txt', 'w', encoding='utf-8') as f:
        for key, value in dict_encryption.items():
            f.write(f'{key}-{value}\n')


key_encryption(alphabet)


# функция дешифрования текста:
def decryption_key(text,alphabet, ngrams):

    frequency_simbol_text = ngrams(text, 1)
    frequency_simbol = [i for i in alphabet]
    simbol_text = list(frequency_simbol_text.keys())
    dict_simbol = {simbol_text[i]:frequency_simbol[i] for i in range(len(simbol_text))}

    with open('key_1.txt', 'w', encoding='utf-8') as f:
        for key, value in dict_simbol.items():
            f.write(f'{key}-{value}\n')

    encrypted_text = ''
    for simbol in text:
        for i in simbol_text:
            if simbol == i:
                encrypted_text +=dict_simbol.get(i)

    return encrypted_text

text1 = decryption_key(text, frequency_simbol, ngrams)
alphabet_text = list( set(text1))

print('Исходный зашифрованный текст:', '\n', text, '\n')
print('Текст после частотной замены символов:', '\n', text1, '\n')

#with open('key_endcrypt.txt', 'w', encoding='utf-8') as f:
#    for i in alphabet_text:
#        f.write(f'{i}-{i}\n')


def decryption_text(decryption_key):

    text1 = decryption_key(text, frequency_simbol, ngrams)

    with open('key_endcrypt.txt', 'r', encoding='utf-8') as f:
        key_text = f.read()

    list_key = [i[0] for i in key_text.splitlines() if len(i) > 0]
    list_value = [i[2] for i in key_text.splitlines() if len(i) > 0]
    dict_key = {list_key[i]:list_value[i] for i in range(len(list_key))}


    encrypted_text1 = ''
    for simbol in text1:
        for i in range(len(list_key)):
            if simbol == list_key[i]:
                encrypted_text1 +=list_value[i]

    print('Текст после подборов букв:', '\n', encrypted_text1, '\n')

    #return encrypted_text1

decryption_text(decryption_key)


# информация о тексте
def info_text(text, ngrams):

    #частотная таблица зашифрованного текста
    frequency_table = ngrams(text, 1)
    list_key = list(frequency_table.keys())
    list_value = list(frequency_table.values())

    #длина текста
    len_text = len(text)

    print("Частотная таблица:")
    for key, value in frequency_table.items():
        print(f'{key}-{value/len_text:.4f}')

    #энтропия зашифрованного текста:
    entropy = 0
    for i in list_value:
        entropy += (i/len_text) * (math.log2(i/len_text))

    print(f'Энтропия зашифрованного текста: {-entropy:.4f}')


    print(f'Избыточность зашифрованного текста: {1 + entropy/5:.4f}')

    #количество пробелов в зашифрованном тексте
    count_ = frequency_table[' ']

    #Средняя длина слова
    print(f'Средняя длина слова в зашифрованном тексте: {round(len_text/count_ - 1)}')

info_text(text, ngrams)

