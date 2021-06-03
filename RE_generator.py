from datetime import datetime
import os

cwd = os.getcwd()
input_path = str(cwd + '\\refseq\\modified_refseq.fasta')
input_file = open(input_path)


full_seq = str()  # записываем референс в одну строку
for s in input_file:
    full_seq = str(full_seq + str(s))
print('Длина полной последовательности: ' + str(len(full_seq)))

# Settings
fragment_start = int(0)
fragment_end = int(0)

circle = str(input('Полная последовательность mtDNA (введите: "full") или отрезок (введите: "segment")? '))
if circle == 'full':
    seq = full_seq
elif circle == 'segment':
    fragment_start = int(input('Начало исследуемой области: '))  # -1 от человеческой нумерации -50
    fragment_end = int(input('Конец исследуемой области: '))  # [: этот индекс не входит в отрезок] +50
    seq = full_seq[fragment_start - 1:fragment_end]

print('Последовательность в работе: ' + seq)
print('Длина исследуемой области: ' + str(len(seq)))

arm_length = int(input('Длина "боков": '))
mask_length = int(input('Длина маскирования нуклеотидов (ноль -> выкл. -> шаг в 1 нукл): '))
del_length_min = int(input('Минимальная длина делеции: '))
del_length_max = int(input('Максимальная длина делеции: '))
both_strands = str(input('генерировать для одной цепи (+) или для двух (+-)? '))

output_filename = 'RE_{0}_{1}_{2}_({3}).txt'.format(circle, str(arm_length), str(mask_length), both_strands)
f = open(output_filename, 'w')  # ('RE.txt', 'w')
f.write('')  # clean output

if mask_length == 0:  # шаг по делециям != 0
    step_length = int(1)
else:
    step_length = int(mask_length)

start_time = datetime.now()  # запуск таймера


def letter_replacer(line, list_of_replacements):
    new_line = str('')
    for letter in line:
        for a in list_of_replacements:
            if letter == a[0]:
                new_line += a[1]
                break
    return new_line


def reg_exp_generator(sequence, deletion_length, arm_length, masking):
    if masking == 0:
        step = int(1)
    else:
        step = masking
    for i in range(0, len(sequence) - int(deletion_length + 2 * arm_length), step):
        deletion_start = int(i + arm_length)
        deletion_end = int(deletion_start + deletion_length)
        reg_exp_start = int(i)
        reg_exp_end = int(deletion_end + arm_length)
        left_arm = str(sequence[reg_exp_start:deletion_start - masking])
        right_arm = str(sequence[deletion_end + masking:reg_exp_end])

        complementary_list = [['A', 'T'], ['T', 'A'], ['G', 'C'], ['C', 'G'],
                              ['M', 'K'], ['K', 'M'], ['R', 'Y'], ['Y', 'R'], ['W', 'W'], ['S', 'S'],
                              ['B', 'V'], ['V', 'B'], ['H', 'D'], ['D', 'H'], ['N', 'N']]

        IUPAC_to_RE_list = [['A', '[AN]'], ['T', '[TN]'], ['G', '[GN]'], ['C', '[CN]'],
                            ['W', '[ATN]'], ['M', '[ACN]'], ['R', '[AGN]'], ['K', '[GTN]'], ['S', '[GCN]'],
                            ['Y', '[CTN]'], ['B', '[CGTN]'], ['D', '[AGTN]'], ['H', '[ACTN]'], ['V', '[ACGN]'],
                            ['N', '[ATGCN]']]

        for direction in ['+', '-']:
            if both_strands == '+' and direction == '-':
                break
            elif both_strands == '+-' and direction == '-':
                larm = left_arm
                left_arm = letter_replacer(right_arm[::-1], complementary_list)
                right_arm = letter_replacer(larm[::-1], complementary_list)

            del_info = str('del_start {0}; del_end {1}; {2} {3} re:'.format(str(deletion_start - masking +
                                                                                fragment_start),
                                                                            str(deletion_end + masking +
                                                                                fragment_start),
                                                                            str(direction),
                                                                            str(deletion_length + 2 * masking)))

            new_left_arm = letter_replacer(left_arm, IUPAC_to_RE_list)
            new_right_arm = letter_replacer(right_arm, IUPAC_to_RE_list)

            reg_exp_seq = str(new_left_arm + '([ATGCN]{0,' + str(masking * 2) + '})' + new_right_arm + '\n')

            with open(output_filename, 'a') as output:
                output.write(str(del_info + reg_exp_seq))
    return


for dl in range(del_length_min, del_length_max + 1, step_length):  # тут у нас скачок по делециям
    extended_seq = seq
    if circle == 'full':
        extended_seq = str(seq + seq[:dl + 2 * arm_length])  # закольцовываем удлинняя в конце
    reg_exp_generator(extended_seq, dl, arm_length, mask_length)
    print('Время выполнения по делециям длинны ' + str(dl) + ' : ', (datetime.now() - start_time))
print('Полное время: ' + str(datetime.now() - start_time))
