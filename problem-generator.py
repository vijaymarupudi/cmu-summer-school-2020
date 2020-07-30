#!/usr/bin/python3

import random
import io
import csv


rows = []

for operator in ('AND', 'OR', 'XOR'):


    for _ in range(20):
        number1 = random.randint(0, 31)
        number2 = random.randint(0, 31)

        if operator == 'AND':
            answer = number1 & number2
        if operator == 'OR':
            answer = number1 | number2
        if operator == 'XOR':
            answer = number1 ^ number2

        rows.append(dict(operator=operator, number1=number1, number2=number2, answer=answer))


stringf = io.StringIO(newline='')
writer = csv.DictWriter(stringf, rows[0].keys())
writer.writeheader()
writer.writerows(rows)
stringf.seek(0)
print(stringf.read())
