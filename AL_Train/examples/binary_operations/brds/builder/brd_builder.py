def dec2bin(dec):
    quotient = [0, 0, 0, 0, 0]
    remainder = [0, 0, 0, 0, 0]
    present_value = dec
    for i in range(5):
        remainder[- 1 - i] = present_value % 2
        present_value = quotient[- 1 - i] = present_value // 2
    return remainder, quotient


a, b = dec2bin(2)
print(a)
print(b)
a, b = dec2bin(10)
print(a)
print(b)
