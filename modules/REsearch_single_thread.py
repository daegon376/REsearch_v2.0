from datetime import datetime
import re
import os

cwd = os.getcwd()
reg_exp_file = open('RE.txt')
reads_file = open(cwd + '\\control\\test_reads.txt')

reads = str()  # все риды записываем в одну строку
for s in reads_file:
    reads = str(reads + s)
# print(reads)

f = open('REsults.txt', 'w')
f.write('')  # clean output


def re_search(reg_exp, info):
    pattern = re.compile(reg_exp)
    deletions = pattern.findall(reads)
    if len(deletions) != 0:  # если что-то нашли
        new_reg_exp = str('.*' + str(re.split(r'\W\WATGCN\W\W0.\d{1,3}\W\W', reg_exp)[0]) + deletions[0] +
                          str(re.split(r'\W\WATGCN\W\W0.\d{1,3}\W\W', reg_exp)[1]) + '.*')  # регулярка для поиска ридов с делецией
        reads_with_del = re.findall(new_reg_exp, reads)
        amount_of_finded_reads = str(len(reads_with_del))
        deletion_length = str(int(re.search(r'\d*$', info).group(0)) - len(deletions[0]))  # вычисляем длину делеции
        with open('REsults.txt', 'a') as output:  # пишем в аутпут
            print('\n Regular expression:', reg_exp,
                  '\n               Info:', info,
                  '\n    Deletion length:', deletion_length,
                  '\n    Amount of calls:', len(deletions),
                  '\nReads with deletion:', amount_of_finded_reads, reads_with_del, file=output)


start_time = datetime.now()  # запуск таймера

for s in reg_exp_file:
    info = str(re.split(r're:', s)[0])[:-1]  # парсим регулярки и сопровождающую инфу
    reg_exp = re.split(r're:', s)[1]
    reg_exp = reg_exp[:-1]
    # print(info)
    # print(reg_exp)
    re_search(reg_exp, info)

print('Полное время: ' + str(datetime.now() - start_time))
