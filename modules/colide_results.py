import os
import re
import pandas as pd

def make_reads_unique(all_reads):
    unique_reads = [[], []]
    output = []
    for read in all_reads:
        if 0 == unique_reads[0].count(read):
            copy_num = all_reads.count(read)
            unique_reads[0].append(read)
            unique_reads[1].append(copy_num)

    for i in range(len(unique_reads[0])):
        output.append([unique_reads[0][i], unique_reads[1][i]])

    return output


def gap_shift(refseq_fragment, read_fragment):
    gap_indexes = []
    index_addition = int(0)
    for i in range(len(refseq_fragment)):
        if read_fragment[i - index_addition] != refseq_fragment[i]:
            gap_indexes.append(i + 1)
            index_addition += 1

    print(refseq_fragment, len(refseq_fragment))
    print((read_fragment[:gap_indexes[0]] + '-' * len(gap_indexes) + read_fragment[gap_indexes[-1] - 1:]),
          len(read_fragment))

    return [gap_indexes[0] + 1, gap_indexes[-1] + 1]


def locate_deletion(refseq, reg_exp, del_length, unique_reads):
    reg_exp_arms = re.split(r'..ATGCN..0,\d+..', reg_exp)
    mask_length = int(re.search(r'..ATGCN..0,(\d+)..', reg_exp).group(1))

    reg_exp_for_refseq = str(reg_exp_arms[0] + '([ATGCN]{0,' + str(mask_length + del_length) + '})' + reg_exp_arms[1])
    masked_seq_on_refseq = re.search(reg_exp_for_refseq, refseq).group(0)
    mask_start = refseq.find(masked_seq_on_refseq)
    mask_end = mask_start + len(masked_seq_on_refseq)

    if refseq[mask_start:mask_end] == masked_seq_on_refseq:
        print('УСПЕШНО НАШЛИ МЕСТО НА РЕФСЕКЕ')
    else:
        print('проблема с индексами')

    list_masked_seq_on_read = []
    for read in unique_reads:
        masked_seq_on_read = re.search(reg_exp, read[0]).group(0)
        if list_masked_seq_on_read.count(masked_seq_on_read) == 0:
            list_masked_seq_on_read.append(masked_seq_on_read)
        else:
            print('уже есть такая маска рида')

    if len(list_masked_seq_on_read) >> 1:
        print('у уникальных ридов разные маскированные последовательности')
    else:
        print('у уникальных ридов ОДНА И ТАЖЕ маскированная последовательность')

    shift = gap_shift(masked_seq_on_refseq, list_masked_seq_on_read[0])
    del_actual_start = mask_start + shift[0]
    del_actual_end = del_actual_start + del_length

    #           маска до дел на рефеке                    # маска до дел на риде
    if refseq[mask_start:del_actual_start] == list_masked_seq_on_read[0][:shift[0]] \
            and refseq[del_actual_end:mask_end] == list_masked_seq_on_read[shift[1]:]:
        #       от дел до конца маски на рефсеке     # от дел до конца маски на риде
    else:
        print('ошибка с индексами')

    if del_actual_start != del_actual_end:
        return '{0}:{1}'.format(del_actual_start, del_actual_end)
    else:
        return del_actual_start

cwd = os.getcwd()
results = open(cwd + '\\REsults_multip_2.txt', mode='r')

ref_seq_file = open(cwd + '\\refseq\\sequence.fasta')
refseq = str()
x = int(0)  # счетчик для пропуска первой строки
for s in ref_seq_file:
    if x == 0:  # пропускаем первую строку
        x = + 1
    else:
        refseq = str(refseq + str(s[:-1]))

re_counter = 0
arr = []
call_info = []

for s in results:
    if s.count('Regular expression:') >> 0:
        if re_counter != 0:
            arr.append(call_info)
            call_info = []
        re_counter += 1
        reg_exp = re.split(':', s)[1][1:-2]
        call_info.append(reg_exp)  # reg_exp
    elif s.count('Info:') >> 0:
        del_start = int(re.findall(r'del_start (\d+)', s)[0])
        del_end = int(re.findall(r'del_end (\d+)', s)[0])
        direction_s = re.findall(r'([+-])', s)[0]

        call_info.append(del_start)  # del_start
        call_info.append(del_end)  # del_end
        if direction_s == '+':  # direction
            direction = 'forward'
            call_info.append(direction)
        elif direction_s == '-':
            direction = 'reverse'
            call_info.append(direction)


    elif s.count('Deletion length:') >> 0:
        del_length = int(re.split(':', s)[1][1:-2])
        call_info.append(del_length)  # del_length

    elif s.count('Amount of calls:') >> 0:
        amount_calls = int(re.split(':', s)[1][1:-2])
        call_info.append(amount_calls)  # amount_calls

    elif s.count('Reads with deletion:') >> 0:
        amount_reads = int(re.findall(r'Reads with deletion:\s(\d+)', s)[0])
        reads_list = re.findall(r'Reads with deletion:\s\d+\s(.*)', s)[0]
        call_info.append(amount_reads)  # amount_reads
        unique_reads = make_reads_unique(re.findall(r'\W([ATGCN]+)\W', reads_list))
        call_info.append(len(unique_reads))  # unique_reads_amount
        call_info.append(unique_reads)  # unique_reads
    else:
        pass
#new_arr = []
#for row in arr:
#    new_row = row[:3]
#    new_row.append(locate_deletion(refseq, row[0], row[4], row[8]))
#    new_row.extend(row[3:])
#    new_arr.append(new_row)


df = pd.DataFrame(arr, columns=['reg_exp', 'approx_start', 'approx_end',  # 'calculated_del_loc',
                                'direction', 'del_length', 'amount_calls',
                                'amount_reads', 'unique_reads_amount',
                                'unic_reads_list'])
print(df.axes)
df.to_excel('results.xlsx')
