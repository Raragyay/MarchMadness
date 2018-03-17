import tkinter as tk
from collections import deque

calc = tk.Tk()
calc.title('Taken from Moonie. <3')

buttons = [
    ['7', '8', '9', '*', 'CA', '('],
    ['4', '5', '6', '/', 'C', ')'],
    ['1', '2', '3', '-', 'SHOW', 'WASTE'],
    ['+/-', '0', '.', '+', '=', 'WASTE']
]
button_style = 'raised'
for fake_row_num, row in enumerate(buttons):
    actual_row_num = fake_row_num + 1
    for button_location, button in enumerate(row):
        action = lambda x=button: click_event(x)
        tk.Button(calc, text=button, width=6, height=2, relief=button_style, command=action) \
            .grid(row=actual_row_num, column=button_location, padx=5, pady=5)

display = tk.Entry(calc, width=40, bg='white', state='readonly', justify='right')
display.grid(row=0, column=0, columnspan=5)
stack = deque()
operators = {'*', '/', '-', '+'}
precedences = {'+': 2, '-': 2, '*': 3, '/': 3}
operations = {
    '+': lambda x, y: x + y,
    '-': lambda x, y: x - y,
    '*': lambda x, y: x * y,
    '/': lambda x, y: x / y
}


def calc_expr():
    expression = stack.copy()
    operands = []
    operators = []
    while expression:
        token = expression.popleft()
        if type(token) == float:
            operands.append(token)
        elif token == '(':
            operators.append(token)
        elif token == ')':  # TODO: Add parentheses
            while operators[-1] != '(':
                operator = operators.pop()
                operand_2 = operands.pop()
                operand_1 = operands.pop()
                operands.append(operations[operator](operand_1, operand_2))
            operators.pop()
        else:
            while operators and precedences[operators[-1]] >= precedences[token]:
                operator = operators.pop()
                operand_2 = operands.pop()
                operand_1 = operands.pop()
                operands.append(operations[operator](operand_1, operand_2))
            operators.append(token)
    while operators:
        operator = operators.pop()
        operand_2 = operands.pop()
        operand_1 = operands.pop()
        operands.append(operations[operator](operand_1, operand_2))
    result = sum(operands)  # By this point there should only be one operand: the result.
    if int(result) == result:
        return int(result)
    else:
        return result


def click_event(button):
    global stack
    display.configure(state='normal')
    try:
        number = int(button)
        print(number)
        display.insert(tk.END, number)
        display.configure(state='readonly')
        return
    except ValueError:
        pass
    if button == '.':
        if '.' not in display.get():
            display.insert(tk.END, '.')
    elif button in operators or button in {'(', ')'}:
        num = float(display.get())
        stack.append(num)
        stack.append(button)
        display.delete(0, tk.END)
    elif button == '+/-':
        if '-' in display.get():
            display.delete(0)
        else:
            display.insert(0, '-')
    elif button == 'CA':
        stack = []
        display.delete(0, tk.END)
    elif button == 'C':
        display.delete(0, tk.END)
    elif button == '=':
        num = float(display.get())
        stack.append(num)
        print(stack)
        display.delete(0, tk.END)
        result = calc_expr()
        display.insert(0, result)
        stack = deque()
    display.configure(state='readonly')
    print(stack)


if __name__ == '__main__':
    calc.mainloop()
