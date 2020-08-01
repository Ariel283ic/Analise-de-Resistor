import sympy as sp
import tkinter as tk
from tkinter import messagebox as mbox

IEWidth = 0.08
IEHeight = 0.25
EWidth = 0.25
LWidth = 0.52
LHeight = 0.25
root = tk.Tk()
root.title('Analise de Resistor')
aviso = mbox.askyesno("AVISOS", "Mostrar avisos após apertar o botão?")
root.geometry('500x120')
root.resizable(0, 0)
frame = tk.Frame(root, bg='light gray')
frame.place(relwidth=1, relheight=1)
label1 = tk.Label(frame, text="Pot D =", bg='cyan')
label1.place(relx=0, rely=0, relwidth=IEWidth, relheight=IEHeight)
label2 = tk.Label(frame, text="U =", bg='cyan')
label2.place(relx=0, rely=IEHeight, relwidth=IEWidth, relheight=IEHeight)
label3 = tk.Label(frame, text="I =", bg='cyan')
label3.place(relx=0, rely=IEHeight * 2, relwidth=IEWidth, relheight=IEHeight)
label4 = tk.Label(frame, text="R =", bg='cyan')
label4.place(relx=0, rely=IEHeight * 3, relwidth=IEWidth, relheight=IEHeight)
entry = tk.Entry(frame, bg='green')
entry.place(relx=IEWidth, rely=0, relwidth=EWidth, relheight=IEHeight)
entry2 = tk.Entry(frame, bg='green')
entry2.place(relx=IEWidth, rely=+IEHeight, relwidth=EWidth, relheight=IEHeight)
entry3 = tk.Entry(frame, bg='green')
entry3.place(relx=IEWidth, rely=IEHeight * 2, relwidth=EWidth, relheight=IEHeight)
entry4 = tk.Entry(frame, bg='green')
entry4.place(relx=IEWidth, rely=IEHeight * 3, relwidth=EWidth, relheight=IEHeight)
button = tk.Button(frame, text="Calcular", bg='gray',
                   command=lambda: ligar(entry.get(), entry2.get(), entry3.get(), entry4.get()))
button.place(relx=0.33, rely=0, relwidth=0.15, relheight=IEHeight * 4)
label5 = tk.Label(frame, bg='light yellow', borderwidth=2, relief="groove")
label5.place(relx=0.48, rely=0, relwidth=LWidth, relheight=LHeight)
label6 = tk.Label(frame, bg='light yellow', borderwidth=2, relief="groove")
label6.place(relx=0.48, rely=LHeight, relwidth=LWidth, relheight=LHeight)
label7 = tk.Label(frame, bg='light yellow', borderwidth=2, relief="groove")
label7.place(relx=0.48, rely=LHeight * 2, relwidth=LWidth, relheight=LHeight)
label8 = tk.Label(frame, bg='light yellow', borderwidth=2, relief="groove")
label8.place(relx=0.48, rely=LHeight * 3, relwidth=LWidth, relheight=LHeight)



def check_input(list):
    dados = []
    for X in list:
        if X:
            dados.append(True)
        else:
            dados.append(False)
    return dados


def ligar(entry, entry2, entry3, entry4):
    R, U, I, PD = sp.symbols('R U I PD')
    dados_dados = []
    todos_simbolos = [R, U, I, PD]
    desconhecidos = []
    simbolos_passados = []
    error_count = 0

    if entry4:
        R = sp.S(entry4)
        dados_dados.append(entry4)
    if entry2:
        U = sp.S(entry2)
        dados_dados.append(entry2)
    if entry3:
        I = sp.S(entry3)
        dados_dados.append(entry3)
    if entry:
        PD = sp.S(entry)
        dados_dados.append(entry)

    data = check_input([entry4, entry2, entry3, entry])

    for i, j in zip(data, todos_simbolos):
        if i:
            simbolos_passados.append(j)
        else:
            desconhecidos.append(j)

    resposta = {}
    for i, j in zip(dados_dados, simbolos_passados):
        resposta[f'{j}'] = f'{i}'

    eq1 = U * I - PD
    eq2 = R * I - U
    for x, y in zip(resposta.keys(), resposta.values()):
        eq1.subs(x, y)
        eq2.subs(x, y)
    equations = [eq1, eq2]
    leng_desc = 0
    for x in desconhecidos:
        leng_desc += 1
    if leng_desc >= 2:
        resultado = sp.nonlinsolve(equations, desconhecidos)
        resultado = list(resultado).pop()
        for i, y in zip(resultado, desconhecidos):
            resposta[f'{y}'] = f'{i}'
    else:
        resultado = sp.solve(equations, desconhecidos)
        try:
            for x, y in list(resultado.items()):
                resposta[f'{x}'] = f'{y}'
        except AttributeError:
            mbox.showerror("Erro", f"Mais de um resultado para a mesma incógnita, {desconhecidos} = {resultado}.")
            error_count = 1
    if error_count == 0:
        try:
            label7['text'] = "I = " + resposta['I']
            label8['text'] = "R = " + resposta['R']
            label6['text'] = "U = " + resposta['U']
            label5['text'] = "Pot D = " + resposta['PD']
            if aviso == True:
                mbox.showinfo("Sucesso", "Calculado com sucesso, ou talvez não, se aparecer algo como 'FiniteSet' significa que o valor pode ser qualquer coisa (um conjunto infinito).")
        except KeyError:
            mbox.showerror("ERRO",
                           "Impossível calcular, provavelmente você digitou algum número errado e não foi possível calcular um resultado.")


root.mainloop()
