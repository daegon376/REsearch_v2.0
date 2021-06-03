import random
from datetime import datetime


def letter_replacer(line, list_of_replacements):
    """Эта функция переписывает строку, заменяя в ней символы соответственно списку замен. """

    new_line = str('')
    for letter in line:
        for a in list_of_replacements:
            if letter == a[0]:
                new_line += a[1]
                break
    return new_line


def read_generator(seq, read_type, r_length):
    """Эта функция генерирует рид на данной последовательности. У рида случайное начало, заданная длина.
    Два режима генерации рида 'ref' - для референсного генома и 'del' - для последовательности с делецией,
    коордната '0' которой находится в брейкпоинте"""

    if read_type == 'ref':
        seq += seq[:r_length]
    elif read_type == 'del':
        seq = seq[-(r_length - 1):] + seq[:r_length - 1]

    read_start = random.randint(0, len(seq) - r_length)
    read_end = read_start + r_length
    read = seq[read_start:read_end]
    return read


if __name__ == '__main__':
    start_time = datetime.now()  # запуск таймера

    # НАСТРОЙКИ
    read_length = int(150)  # длина генерируемых ридов
    del_length = random.randint(1, 16000)  # длина делеции

    total_amount = int(100)  # сумма всех ридов
    del_reads_percentage = int(15)  # процентная доля ридов с делецией

    refseq = str('')

    with open('sequence.fasta', 'r') as f:
        for s in f:
            refseq = s[:-1]  # загружаем референсную последовательность в переменную строки

    max_seq_index = int(len(refseq) - 1)  # индекс последнего нуклеотида на линейной последовательности
    del_start = int(random.randint(0, max_seq_index))  # случайно определяем точку начала делеции - брейкпоинт
    del_end = int(del_start + del_length) % len(refseq)  # координаты конца делеции на кольцевой молекуле

    circular_seq = str()  # кольцевая молекула с вырезанной делецией
    deletion = str()  # собственно делеция
    if del_end > del_start:  # делеция не затрагивает нулевую координату (OriH)
        circular_seq = refseq[del_end:] + refseq[:del_start]
        deletion = refseq[del_start:del_end]
    elif del_end < del_start:  # делеция затрагивает нулевую координату, при этом удаляя OriH
        circular_seq = refseq[del_end:del_start]
        deletion = refseq[del_start:] + refseq[:del_end]
    else:  # случай без делеции нас пока не интересует
        print('Error: Deletion length = 0')

    if len(circular_seq) != len(refseq) - del_length and len(deletion) != del_length:
        input('Error: circular molecule length is wrong!')  # проверка на соответсвие длин фрагметов заданым величинам

    with open('deletion_info.txt', 'w') as f:  # очищаем файлы для вывода результатов
        f.write('')
    with open('test_reads.txt', 'w') as f:
        f.write('')

    reads_ready = int()  # счетчик сгенерированных ридов всего
    del_reads_amount = 0  # счетчик сгенерированных ридов c делецией
    while reads_ready < total_amount:  # пока не нагенерируем нужное количество ридов
        reads_ready += 1
        with open('test_reads.txt', 'a') as output:
            read = str()
            if random.randint(1, 100) > del_reads_percentage:  # определяем какой рид генерировать с делецией или без
                read = read_generator(refseq, str('ref'), read_length)
            else:
                del_reads_amount += 1
                read = read_generator(circular_seq, str('del'), read_length)

            if random.randint(0, 1) == 1:
                # с условной вероятностью 50% переписываем рид комплиментарно и в обратном направлении.
                # Получаем распределение ридов по + и - strands ~1/1
                complementary_list = [['A', 'T'], ['T', 'A'], ['G', 'C'], ['C', 'G'],
                                      ['M', 'K'], ['K', 'M'], ['R', 'Y'], ['Y', 'R'], ['W', 'W'], ['S', 'S'],
                                      ['B', 'V'], ['V', 'B'], ['H', 'D'], ['D', 'H'], ['N', 'N']]
                read = str(letter_replacer(read, complementary_list))[::-1]

            output.write(read + '\n')  # записываем рид

    with open('deletion_info.txt', 'a') as f:
        f.write('\nDeletion length = {2} between {0} and {1}.'.format(str(del_start + 1), str(del_end + 1),
                                                                      str(del_length)))
        f.write('\nnucleotides before BP:{0}'
                '\n             deletion:{1}'
                '\n nucleotides after BP:{2}'
                '\n{3} reads with deletion in total {4} reads'.format(circular_seq[-read_length:],
                                                                      deletion, circular_seq[:read_length],
                                                                      str(del_reads_amount), str(total_amount)))

    print('Полное время: ' + str(datetime.now() - start_time))
