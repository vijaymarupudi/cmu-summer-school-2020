# cmu-summer-school-2020

This repository will hold my project for the [Simon Initiative LearnLab Summer School], 2020, held online due to the COVID-19 pandemic.

This project involves a binary operator learner. Given one base 10 number, the binary operator and the output, the [Apprentice Learner] will have to determine was the missing number is.

[Apprentice Learner]: https://www.educationaldatamining.org/EDM2016/proceedings/paper_118.pdf
[Simon Initiative LearnLab Summer School]: https://learnlab.org/index.php/simon-initiative-summer-school/

## Operators

* `//` 
* `% 2`
* `&`
* `|`
* `^`
* `2 ** x * y`
* `+ (a1, a2, a3, a4, a5)`
* `(number1, number2, op)`

```
31 AND 2 = ___

First step

  Convert 31 -> binary
    Interface for this
  Convert 2 -> binary
    Interface for this

Conversion to binary


current_number = 31
binary_digit = []
quotients = []
remainders = []


for i in range(5):
  quotient = current_number // 2
  remainder = current_number % 2
  remainders.append(remainder)
  quotients.append(quotient)
  current_number = quotient

for remainder in reverse(remainders):
  input(remainder) 

# two times for each number

# two aligned boxes with the binary representations of the number

for numbers in column:
  input(binary_op(numbers))

# reverse conversion

1 0 0 1 0

_ _ _ _ _
# 16 0 0 2 0

18
```

## Progress

* `x // 2` done, `BOIntDiv2` 
* `x % 2` done, `BOMod2`
* `2 ** x * y`, done, `BOPowerOfTwoTimesNumber`
* `+ (a1, a2, a3, a4, a5)` done, `BOAdd5`
* `(number1, number2, op)` done, `BOBinaryOp`
  * `&`, `ADD` argument
  * `|`, `OR` argument
  * `^`, `XOR` argument
