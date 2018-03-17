import tkinter as tk
from collections import deque

calc = tk.Tk()
calc.title('Many Thanks to Moonie for telling me how to create buttons. <3')

buttons = [
    ['7', '8', '9', '*', '<-', '('],
    ['4', '5', '6', '/', 'MOD', ')'],
    ['1', '2', '3', '-', '^', 'CA'],
    ['+/-', '0', '.', '+', '=', 'C']
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
precedences = {'+': 2, '-': 2, '*': 3, '/': 3}
clear_next = False
operations = {
    '+'  : lambda x, y: x + y,
    '-'  : lambda x, y: x - y,
    '*'  : lambda x, y: x * y,
    '/'  : lambda x, y: x / y,
    '^'  : lambda x, y: x ** y,
    'MOD': lambda x, y: x % y
}


def calc_expr():
    expression = stack.copy()
    operand_stack = []
    operator_stack = []
    while expression:
        token = expression.popleft()
        if type(token) == float:
            operand_stack.append(token)
        elif token == '(':
            operator_stack.append(token)
        elif token == ')':
            while operator_stack[-1] != '(':
                operator = operator_stack.pop()
                operand_2 = operand_stack.pop()
                operand_1 = operand_stack.pop()
                operand_stack.append(operations[operator](operand_1, operand_2))
            operator_stack.pop()
        else:
            while operator_stack and precedences[operator_stack[-1]] >= precedences[token]:
                operator = operator_stack.pop()
                operand_2 = operand_stack.pop()
                operand_1 = operand_stack.pop()
                operand_stack.append(operations[operator](operand_1, operand_2))
            operator_stack.append(token)
    while operator_stack:
        operator = operator_stack.pop()
        operand_2 = operand_stack.pop()
        operand_1 = operand_stack.pop()
        operand_stack.append(operations[operator](operand_1, operand_2))
    result = sum(operand_stack)  # By this point there should only be one operand: the result.
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
    elif button in operations or button in {'(', ')'}:
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
        stack = deque()
        display.delete(0, tk.END)
    elif button == 'C':
        display.delete(0, tk.END)
    elif button == '<-':
        display.delete(len(display.get()) - 1)
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
