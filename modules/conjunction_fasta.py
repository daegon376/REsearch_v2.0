from datetime import datetime

start_time = datetime.now()
genome = str()
x = 0
with open('sequence.fasta', 'r') as genome_file:
    for s in genome_file:
        if s.startswith('>'):  # пропускаем первую строку
            with open('test_mt.txt', 'a') as newfile:
                newfile.write('\n' + s.upper())
        else:
            with open('test_mt.txt', 'a') as newfile:
                newfile.write(s[:-1].upper())

print('Полное время: ' + str(datetime.now() - start_time))