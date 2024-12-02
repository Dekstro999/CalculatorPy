# https://github.com/Dekstro999/LPPYTHON

import customtkinter as ctk

root = ctk.CTk()
root.title("Calculadora Simple")
root.geometry("600x150")
root.resizable(False, False)
root.iconbitmap("calculator.ico")
root.config(bg="black")

# Variables
operator = ctk.StringVar(value="+")

def select_operator(op):
    operator.set(op)
    calculate()

def calculate(*args):
    try:
        num1 = float(entry1.get()) if entry1.get() else 0
        num2 = float(entry2.get()) if entry2.get() else 0
        op = operator.get()
        if op == "+":
            result = num1 + num2
        elif op == "-":
            result = num1 - num2
        elif op == "x":
            result = num1 * num2
        elif op == "/":
            result = num1 / num2
        entry_result.configure(state='normal')
        entry_result.delete(0, ctk.END)
        entry_result.insert(0, str(result))
        entry_result.configure(state='readonly')
    except Exception as e:
        entry_result.configure(state='normal')
        entry_result.delete(0, ctk.END)
        entry_result.insert(0, "Error")
        entry_result.configure(state='readonly')

entry1 = ctk.CTkEntry(root, width=150, height=50, font=("Arial", 24), justify='center')
entry1.grid(row=0, column=0, padx=10, pady=10)
entry1.bind("<KeyRelease>", calculate)

entry_operator = ctk.CTkLabel(root, textvariable=operator, width=50, height=50, font=("Arial", 24), fg_color="black", text_color="white")
entry_operator.grid(row=0, column=1, padx=10, pady=10)

entry2 = ctk.CTkEntry(root, width=150, height=50, font=("Arial", 24), justify='center')
entry2.grid(row=0, column=2, padx=10, pady=10)
entry2.bind("<KeyRelease>", calculate)

entry_result = ctk.CTkEntry(root, width=150, height=50, font=("Arial", 24), justify='center', state='readonly')
entry_result.grid(row=0, column=3, padx=10, pady=10)

# Botones de operadores
btn_add = ctk.CTkButton(root, text="+", width=50, height=50, command=lambda: select_operator("+"), font=("Arial", 24, "bold"))
btn_add.grid(row=1, column=0, padx=5, pady=5)

btn_subtract = ctk.CTkButton(root, text="-", width=50, height=50, command=lambda: select_operator("-"), font=("Arial", 24, "bold"))
btn_subtract.grid(row=1, column=1, padx=5, pady=5)

btn_multiply = ctk.CTkButton(root, text="x", width=50, height=50, command=lambda: select_operator("x"), font=("Arial", 24, "bold"))
btn_multiply.grid(row=1, column=2, padx=5, pady=5)

btn_divide = ctk.CTkButton(root, text="/", width=50, height=50, command=lambda: select_operator("/"), font=("Arial", 24, "bold"))
btn_divide.grid(row=1, column=3, padx=5, pady=5)

root.mainloop()