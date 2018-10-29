#converts binary number to its two's compliment
def twos_compliment(binary_num):
    compliment = ""
    binary_list = [int(x) for x in list(binary_num)]
    for i in range(len(binary_list)):
        if binary_list[i] == 1:
            binary_list[i] = 0
        else:
            binary_list[i] = 1
    binary_list[len(binary_list)-1] += 1
    i = len(binary_list)-1
    while binary_list[i] == 2:
        if i == 1:
            binary_list[1] = 0
            break
        binary_list[i-1] += 1
        binary_list[i] = 0
        i -= 1
    for binary_num in binary_list:
        compliment += str(binary_num)
    return compliment
print(twos_compliment("00000001"))
print(twos_compliment("10000001"))
print(twos_compliment("00000100"))