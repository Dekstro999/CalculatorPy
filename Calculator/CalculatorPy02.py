# https://github.com/Dekstro999/LPPYTHON


import customtkinter as ctk


# Configuración de la ventana principal
root = ctk.CTk()
root.title("Calculadora")
root.geometry("500x750")
root.resizable(False, False)
root.iconbitmap("calculator.ico")
root.config(bg="black")


# Función para manejar los eventos de los botones
def click(value):
    print(value)
    if entry.get() == "Error":
        clear()
        entry.insert(0, temp)
    current = entry.get()
    entry.delete(0, ctk.END)
    entry.insert(0, current + str(value))

def clear():
    entry.delete(0, ctk.END)

def calculate():
    try:
        result = eval(entry.get())
        clear()
        entry.insert(0, str(result))
    except Exception as e:
        global temp 
        temp= entry.get()
        entry.delete(0, ctk.END)
        entry.insert(0, "Error")

def change_sign():
    current = entry.get()
    if current:
        if current[0] == '-':
            entry.delete(0)
        else:
            entry.insert(0, '-')

def add_parentheses():
    current = entry.get()
    if current.count('(') > current.count(')'):
        entry.insert(ctk.END, ')')
    else:
        entry.insert(ctk.END, '(')

def add_percentage():
    current = entry.get()
    try:
        result = eval(current) / 100
        entry.delete(0, ctk.END)
        entry.insert(0, str(result))
    except Exception as e:
        entry.delete(0, ctk.END)
        entry.insert(0, "Error")

entry = ctk.CTkEntry(root, width=480, height=200, font=("Arial Narrow", 90),bg_color='black', fg_color="transparent", border_width=0, justify='right')
entry.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

TOP = 'lightgray'
OP = 'orange'
NUM = '#333333'
DG= 'gray'
DO= 'darkorange'
W= 'white'
D= 'black'

buttons = [
    ('AC', TOP, DG,D), ('+/-', TOP, DG,D), ('%',  TOP, DG,D), ('/', OP, DO,W),
    ('7', NUM, DG,W), ('8', NUM, DG,W), ('9', NUM, DG,W), ('x', OP, DO,W),
    ('4', NUM, DG,W), ('5', NUM, DG,W), ('6', NUM, DG,W), ('-', OP, DO,W),
    ('1', NUM, DG,W), ('2', NUM, DG,W), ('3', NUM, DG,W), ('+', OP, DO,W),
    ('()', NUM, DG,W), ('0', NUM, DG,W), ('.', NUM, DG,W), ('=', OP, DO,W)
]

row_val = 1
col_val = 0

for (text,color, hover_color, t_color) in buttons:
    
    if text == 'AC':
        command=clear
    elif text == '+/-':
        command=change_sign
    elif text == '%':
        command=add_percentage
    elif text == '()':
        command=add_parentheses
    elif text == '=':
        command=calculate
    elif text == 'x':
        command=lambda:click('*')
    else:
        command=lambda text=text:click(text)
    
    btn = ctk.CTkButton(root, text="", width=90, height=90, 
                        command=command,bg_color='black', fg_color=color, hover_color=hover_color, text_color=t_color, 
                        font=("Arial", 23, "bold"), corner_radius=45)
    lable = ctk.CTkLabel(btn, text=text, bg_color='transparent', fg_color='transparent', text_color=t_color, font=("Arial", 50, "bold"),  anchor='center')
    lable.place(relx=0.5, rely=0.5, anchor='center')
    btn.grid(row=row_val, column=col_val, padx=5, pady=5)
    col_val += 1
    if col_val > 3:
        col_val = 0
        row_val += 1

# Ejecutar la aplicación
root.mainloop()