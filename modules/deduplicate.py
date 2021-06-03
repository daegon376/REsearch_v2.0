import os

cwd = str(os.getcwd())
input_f = open(cwd + '\\AllUnmapped.fastq.txt', mode='r')

unique_reads = []
counter = int(0)
with open(cwd + '\\AllUnmapped-normalized.txt', mode='w') as output:
    for read in input_f:
        counter += 1
        if unique_reads.count(read) == 0:
            unique_reads.append(read)
            output.write(read)

print('{1} - {2} = {3}'.format(str(counter), str(len(unique_reads)), str(counter - len(unique_reads))))
