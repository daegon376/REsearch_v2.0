import csv
import re


def row_parser(row):
    replacement = []
    s = re.split(r':', row[0])
    coord = int(s[1])  # вытащили коордиаты
    replacement.append(coord)

    s = re.split(r',', row[1][1:-1])   # вытащили список вариантов на этой координате
    vars = []
    for i in s:
        if len(i[1:-1]) == 1:  # оставляем только SNV
            vars.append(i[1:-1])
        else:
            return None

    replacement.append(vars)
    return replacement


def locus_conductor(old_list):
    new_list = []
    last_coords = int()
    last_index = int(-1)

    for r in old_list:
        if r[0] == last_coords:  # если координата уже встречалась
            for var in r[1]:
                if new_list[last_index][1].count(var) == 0:  # если еще нет такого варианта на данной координате
                    new_list[last_index][1].append(var)  # добавляем новый вариант к имеющимся
        else:  # если координата новая
            new_list.append(r)
            last_index += 1
            last_coords = r[0]
    return new_list


def convert_to_IUPAC(old_list):
    iupac = []
    for s in old_list:
        replacement = []
        coord = s[0]
        replacement.append(coord)  # переписали коордиаты
        vars = s[1]
        fin_letter = str()
        if len(vars) == 2:
            if vars.count('A') == 1:
                if vars.count('C') == 1:
                    fin_letter = 'M'  # AC
                elif vars.count('G') == 1:
                    fin_letter = 'R'  # AG
                elif vars.count('T') == 1:
                    fin_letter = 'W'  # AT
            elif vars.count('G') == 1:
                if vars.count('C') == 1:
                    fin_letter = 'S'  # GC
                elif vars.count('T') == 1:
                    fin_letter = 'K'  # GT
            elif vars.count('T') == 1 and vars.count('C') == 1:
                fin_letter = 'Y'  # TC
        elif len(vars) == 3:
            if vars.count('C') == vars.count('T') == vars.count('G') == 1 and vars.count('A') == 0:
                fin_letter = 'B'  # не А
            if vars.count('A') == vars.count('T') == vars.count('G') == 1 and vars.count('C') == 0:
                fin_letter = 'D'  # не С
            if vars.count('A') == vars.count('C') == vars.count('G') == 1 and vars.count('T') == 0:
                fin_letter = 'V'  # не Т
            if vars.count('A') == vars.count('C') == vars.count('T') == 1 and vars.count('G') == 0:
                fin_letter = 'H'  # не G
        elif len(vars) == 4:
            if vars.count('A') == vars.count('C') == vars.count('T') == vars.count('G') == 1:
                fin_letter = 'N'  # любой нуклеотид
        replacement.append(fin_letter)
        iupac.append(replacement)
    return iupac


def replacer(seq, replacements):
    for r in replacements:
        coords = int(r[0]) - 1  # уменьшаем на 1, т.к. индексы питона
        letter = r[1]
        seq = str(seq[:coords] + letter + seq[coords + 1:])
    new_seq = seq

    return new_seq



if __name__ == '__main__':
    replacements_counter = int(0)
    replacements = []
    with open('polymorphisms_test_100.csv') as csvfile:
        pm_sheet = csv.reader(csvfile, delimiter=';')
        x = int(0)  # счетчик для пропуска головы таблицы
        for row in pm_sheet:
            if x == 0:  # пропускаем первую строку таблицы
                x = + 1
            else:
                if row_parser(row) is not None:
                    replacements.append(row_parser(row))

    with open('sequence.fasta') as seq_inp_file:
        sequence = str()
        x = int(0)  # счетчик для пропуска первой строки
        for s in seq_inp_file:
            if x == 0:  # пропускаем первую строку
                x = + 1
            else:
                sequence = str(sequence + str(s[:-1]))


    replacements_counter = int(0)
    old_len = len(replacements)
    replacements = locus_conductor(replacements)
    replacements = convert_to_IUPAC(replacements)
    print(replacements)
    print(len(replacements), old_len)

    with open('modified_refseq.fasta', 'w') as output_file:
        output_file.write(replacer(sequence, replacements))
    print('RefSeq is successfully modified!')


