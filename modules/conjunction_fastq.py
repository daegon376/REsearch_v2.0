from datetime import datetime
import os

start_time = datetime.now()
cwd = os.getcwd()
os.mkdir(cwd + '\\txt\\')
files_list = os.listdir(cwd)
fastq_files = []
for file in files_list:
    if file[-6:] == '.fastq':
        fastq_files.append([cwd + '\\' + file, cwd + '\\txt\\' + file])

for fastq_file in fastq_files:
    new_file = str(fastq_file[1]) + '.txt'
    with open(str(fastq_file[0])) as file:
        reads_list = []
        x = 1   #line counter
        for s in file:
            if x == 2 or (x-2)%4 == 0:
                reads_list.append(s)
                x += 1
            else:
                x += 1
        with open(new_file, 'w') as output:
            for i in reads_list:
                output.write(i)
            output_length = str(len(reads_list))
            print('File saved: ' + new_file + '\n it contain ' + output_length + ' lines')

print('Полное время: ' + str(datetime.now() - start_time))