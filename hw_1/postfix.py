import sys
lines = sys.stdin.readlines()
expression = ''
stack = []
currentSum = None
for c in lines:
    expression += c
    expression += ' '
entries = expression.split()
for entry in entries:
    if entry.isnumeric() or entry[1:].isnumeric():
        stack.append(entry)
    else:
        # if currentSum is not None:
        #     num = int(stack.pop())
        # else:

        currentSum = int(stack.pop())
        num = int(stack.pop())
        if entry == '+':
            currentSum += num
        elif entry == '-':
            currentSum = num - currentSum
        elif entry == '*':
            currentSum *= num
        else:
            currentSum = num // currentSum
        stack.append(currentSum)
sys.stdout.write(str(currentSum))
sys.stdout.write('\n')





