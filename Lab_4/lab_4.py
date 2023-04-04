import math

class MD4:

    def __init__(self, message):
        self.message = message

    # будем работать октетами - порциями из 8 битов
    # 128 = b'10000000'
    PADDING = [128, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
               0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
               0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
               0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    BLOCK_SIZE = 64

    def hash_code(self):

        # Этап 1 обработка входной строки

        # перевод символов сообщения в числа
        symbol_message = [ord(symbol) for symbol in self.message]

        # длина исходного сообщения
        message_len = len(symbol_message)

        # остаток от mod64 байтов (512 битов)
        index = message_len % 64

        # если остаток(index) меньше 56 байтов добавляем 1 бит + 56 - index
        if index < 56:
            symbol_message = symbol_message + self.PADDING[0:(56 - index)]

        else:
            symbol_message = symbol_message + self.PADDING[0:(120 - index)]

        # Этап 2 добавляем к нашему сообщению, к последнему блоку 64 бита (8 байтов)

        # добавляем байты от младшего к старшему
        symbol_message = symbol_message + list((message_len * 8).to_bytes(8, 'little'))

        # Этап 3 Инициализация MD-буфера

        # инициализация регистров
        word_A = 0x67452301
        word_B = 0xefcdab89
        word_C = 0x98badcfe
        word_D = 0x10325476

        # проходимся по раундам
        for i in range(math.ceil(len(symbol_message) / self.BLOCK_SIZE)):

            # делим слово на блоки
            block = MD4.decode_block(symbol_message[i * self.BLOCK_SIZE: (i + 1) * self.BLOCK_SIZE])

            AA = word_A
            BB = word_B
            CC = word_C
            DD = word_D

            # 0x100000000 - это 2^32 в 16-ричном формате

            # 1 - й раунд
            word_A = MD4.bit_shift((word_A + MD4.F(word_B, word_C, word_D) + block[0]) % 0x100000000, 3)
            word_D = MD4.bit_shift((word_D + MD4.F(word_A, word_B, word_C) + block[1]) % 0x100000000, 7)
            word_C = MD4.bit_shift((word_C + MD4.F(word_D, word_A, word_B) + block[2]) % 0x100000000, 11)
            word_B = MD4.bit_shift((word_B + MD4.F(word_C, word_D, word_A) + block[3]) % 0x100000000, 19)

            word_A = MD4.bit_shift((word_A + MD4.F(word_B, word_C, word_D) + block[4]) % 0x100000000, 3)
            word_D = MD4.bit_shift((word_D + MD4.F(word_A, word_B, word_C) + block[5]) % 0x100000000, 7)
            word_C = MD4.bit_shift((word_C + MD4.F(word_D, word_A, word_B) + block[6]) % 0x100000000, 11)
            word_B = MD4.bit_shift((word_B + MD4.F(word_C, word_D, word_A) + block[7]) % 0x100000000, 19)

            word_A = MD4.bit_shift((word_A + MD4.F(word_B, word_C, word_D) + block[8]) % 0x100000000, 3)
            word_D = MD4.bit_shift((word_D + MD4.F(word_A, word_B, word_C) + block[9]) % 0x100000000, 7)
            word_C = MD4.bit_shift((word_C + MD4.F(word_D, word_A, word_B) + block[10]) % 0x100000000, 11)
            word_B = MD4.bit_shift((word_B + MD4.F(word_C, word_D, word_A) + block[11]) % 0x100000000, 19)

            word_A = MD4.bit_shift((word_A + MD4.F(word_B, word_C, word_D) + block[12]) % 0x100000000, 3)
            word_D = MD4.bit_shift((word_D + MD4.F(word_A, word_B, word_C) + block[13]) % 0x100000000, 7)
            word_C = MD4.bit_shift((word_C + MD4.F(word_D, word_A, word_B) + block[14]) % 0x100000000, 11)
            word_B = MD4.bit_shift((word_B + MD4.F(word_C, word_D, word_A) + block[15]) % 0x100000000, 19)

            # 2 - й раунд
            word_A = MD4.bit_shift((word_A + MD4.G(word_B, word_C, word_D) + block[0] + 0x5A827999) % 0x100000000, 3)
            word_D = MD4.bit_shift((word_D + MD4.G(word_A, word_B, word_C) + block[4] + 0x5A827999) % 0x100000000, 5)
            word_C = MD4.bit_shift((word_C + MD4.G(word_D, word_A, word_B) + block[8] + 0x5A827999) % 0x100000000, 9)
            word_B = MD4.bit_shift((word_B + MD4.G(word_C, word_D, word_A) + block[12] + 0x5A827999) % 0x100000000, 13)

            word_A = MD4.bit_shift((word_A + MD4.G(word_B, word_C, word_D) + block[1] + 0x5A827999) % 0x100000000, 3)
            word_D = MD4.bit_shift((word_D + MD4.G(word_A, word_B, word_C) + block[5] + 0x5A827999) % 0x100000000, 5)
            word_C = MD4.bit_shift((word_C + MD4.G(word_D, word_A, word_B) + block[9] + 0x5A827999) % 0x100000000, 9)
            word_B = MD4.bit_shift((word_B + MD4.G(word_C, word_D, word_A) + block[13] + 0x5A827999) % 0x100000000, 13)

            word_A = MD4.bit_shift((word_A + MD4.G(word_B, word_C, word_D) + block[2] + 0x5A827999) % 0x100000000, 3)
            word_D = MD4.bit_shift((word_D + MD4.G(word_A, word_B, word_C) + block[6] + 0x5A827999) % 0x100000000, 5)
            word_C = MD4.bit_shift((word_C + MD4.G(word_D, word_A, word_B) + block[10] + 0x5A827999) % 0x100000000, 9)
            word_B = MD4.bit_shift((word_B + MD4.G(word_C, word_D, word_A) + block[14] + 0x5A827999) % 0x100000000, 13)

            word_A = MD4.bit_shift((word_A + MD4.G(word_B, word_C, word_D) + block[3] + 0x5A827999) % 0x100000000, 3)
            word_D = MD4.bit_shift((word_D + MD4.G(word_A, word_B, word_C) + block[7] + 0x5A827999) % 0x100000000, 5)
            word_C = MD4.bit_shift((word_C + MD4.G(word_D, word_A, word_B) + block[11] + 0x5A827999) % 0x100000000, 9)
            word_B = MD4.bit_shift((word_B + MD4.G(word_C, word_D, word_A) + block[15] + 0x5A827999) % 0x100000000, 13)

            # 3 - й раунд
            word_A = MD4.bit_shift((word_A + MD4.H(word_B, word_C, word_D) + block[0] + 0x6ED9EBA1) % 0x100000000, 3)
            word_D = MD4.bit_shift((word_D + MD4.H(word_A, word_B, word_C) + block[8] + 0x6ED9EBA1) % 0x100000000, 9)
            word_C = MD4.bit_shift((word_C + MD4.H(word_D, word_A, word_B) + block[4] + 0x6ED9EBA1) % 0x100000000, 11)
            word_B = MD4.bit_shift((word_B + MD4.H(word_C, word_D, word_A) + block[12] + 0x6ED9EBA1) % 0x100000000, 15)

            word_A = MD4.bit_shift((word_A + MD4.H(word_B, word_C, word_D) + block[2] + 0x6ED9EBA1) % 0x100000000, 3)
            word_D = MD4.bit_shift((word_D + MD4.H(word_A, word_B, word_C) + block[10] + 0x6ED9EBA1) % 0x100000000, 9)
            word_C = MD4.bit_shift((word_C + MD4.H(word_D, word_A, word_B) + block[6] + 0x6ED9EBA1) % 0x100000000, 11)
            word_B = MD4.bit_shift((word_B + MD4.H(word_C, word_D, word_A) + block[14] + 0x6ED9EBA1) % 0x100000000, 15)

            word_A = MD4.bit_shift((word_A + MD4.H(word_B, word_C, word_D) + block[1] + 0x6ED9EBA1) % 0x100000000, 3)
            word_D = MD4.bit_shift((word_D + MD4.H(word_A, word_B, word_C) + block[9] + 0x6ED9EBA1) % 0x100000000, 9)
            word_C = MD4.bit_shift((word_C + MD4.H(word_D, word_A, word_B) + block[5] + 0x6ED9EBA1) % 0x100000000, 11)
            word_B = MD4.bit_shift((word_B + MD4.H(word_C, word_D, word_A) + block[13] + 0x6ED9EBA1) % 0x100000000, 15)

            word_A = MD4.bit_shift((word_A + MD4.H(word_B, word_C, word_D) + block[3] + 0x6ED9EBA1) % 0x100000000, 3)
            word_D = MD4.bit_shift((word_D + MD4.H(word_A, word_B, word_C) + block[11] + 0x6ED9EBA1) % 0x100000000, 9)
            word_C = MD4.bit_shift((word_C + MD4.H(word_D, word_A, word_B) + block[7] + 0x6ED9EBA1) % 0x100000000, 11)
            word_B = MD4.bit_shift((word_B + MD4.H(word_C, word_D, word_A) + block[15] + 0x6ED9EBA1) % 0x100000000, 15)

            word_A = (word_A + AA) % 0x100000000
            word_B = (word_B + BB) % 0x100000000
            word_C = (word_C + CC) % 0x100000000
            word_D = (word_D + DD) % 0x100000000

        # здесь хранятся хэш-код в 16-ричном формате
        hash_code = word_A.to_bytes(8, 'little')
        hash_code += word_B.to_bytes(8, 'little')
        hash_code += word_C.to_bytes(8, 'little')
        hash_code += word_D.to_bytes(8, 'little')

        # выводим хэш-код сообщения в виде строки:
        # hex(x) - преобразует число в 16-ричную сроку
        # lstrip("0x") - удаляет приставку(основания)

        return "".join(map(lambda x: hex(x).lstrip("0x"), hash_code))



    @staticmethod
    def decode_block(word):
        # преобразуем каждый блок, составленный из 4 байтов, в целое число
        process_block = []

        for i in range(0, len(word), 4):
            process_block.append((word[i]) | ((word[i + 1]) << 8) | ((word[i + 2]) << 16) | ((word[i + 3]) << 24))

        return process_block

    @staticmethod
    def F(x, y, z):
        return (x & y) | (~x & z)

    @staticmethod
    def G(x, y, z):
        return (x & y) | (x & z) | (y & z)

    @staticmethod
    def H(x, y, z):
        return x ^ y ^ z

    @staticmethod
    def bit_shift(x, n):
        # циклический сдвиг битов
        return (x << n) | (x >> (32 - n))


messages = ['The quick brown fox jumps over the lazy dog',
            'The quick brown fox jumps over the lazy cog',
            '']

for i in messages:
    md4 = MD4(message=i).hash_code()
    print(f'Для строки "{i}" хэш-код: {md4}')



