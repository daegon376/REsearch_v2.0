
def complementary_conversion(line):
    new_line = str('')
    complementary_list = [['A', 'T'], ['T', 'A'], ['G', 'C'], ['C', 'G'],
                          ['M', 'K'], ['K', 'M'], ['R', 'Y'], ['Y', 'R'], ['W', 'W'], ['S', 'S'],
                          ['B', 'V'], ['V', 'B'], ['H', 'D'], ['D', 'H'], ['N', 'N']]
    for letter in line:
        for a in complementary_list:
            if letter == a[0]:
                new_line += a[1]
                break

    return new_line

new_line = str()
with open('test_mt.txt', 'r') as file:
    for s in file:
        new_line = str(complementary_conversion(s))[::-1]

with open('test_mt.txt', 'a') as file:
    file.write('\n' + new_line)