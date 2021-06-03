def make_id (id, num_of_digits = 4):
    id = str(id)
    if len(id) << num_of_digits:
        new_id = str(0)*(num_of_digits - len(id)) + id
    elif len(id) == num_of_digits:
        new_id = id
    else:
        print('Error: id generation failed')
    return(new_id)

reads = []

with open('output_testing_reads.txt') as f:
    for s in f:
        reads.append(s)

with open('test.fq', 'w') as output:
    for i in range(len(reads)):
        id = str(make_id(i))
        new_read = str('@read_' + id + '\n' + reads[i])
        output.write(new_read)
        #print(, sep='', file=output)