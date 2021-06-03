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

read =   'CTCCATGCATTTGGTATTTTCGTCTGGGGG  TG TGCACGCGATAGCATTGCGAGACGCTGG'
refseq = 'CTCCATGCATTTGGTATTTTCGTCTGGGGG GTA TGCACGCGATAGCATTGCGAGACGCTGG'

a = gap_shift(refseq, read)

