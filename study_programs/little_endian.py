# evaluate  little endian integer with spaces between bytes
def eval_byte(byte):
    value = 0
    bit_list = [int(x) for x in list(byte)]
    for i in range(8):
        value += bit_list[len(bit_list)-i-1] * (2 ** i)
    return value


def int_value(integer):
    value = 0
    byte_list = integer.split()
    for i in range(len(byte_list)):
        value += (256 ** i) * eval_byte(byte_list[len(byte_list)-i-1])
    return value


print(int_value('01111100 01110011 11111010 00000001'),
      'expected 2087975425')
print(int_value('01000111 10101100 01010111 11110100'),
      'expected 1202477044')
