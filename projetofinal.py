import sqlite3
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


conn = sqlite3.connect("clientes.db")
cursor = conn.cursor()


cursor.execute("""
CREATE TABLE IF NOT EXISTS clientes (
    nome TEXT NOT NULL,
    email TEXT,
    telefone TEXT,
    endereco TEXT
)
""")
conn.commit()

# Funções
def cadastrar_cliente():
    nome = entry_nome.get()
    email = entry_email.get()
    telefone = entry_telefone.get()
    endereco = entry_endereco.get()

    if nome == "":
        messagebox.showwarning("Atenção", "O campo 'Nome' é obrigatório!")
        return

    cursor.execute("INSERT INTO clientes (nome, email, telefone, endereco) VALUES (?, ?, ?, ?)", 
                   (nome, email, telefone, endereco))
    conn.commit()
    mostrar_usuario()
    limpar_campos()

def mostrar_usuario():
    for row in tree.get_children():
        tree.delete(row)
    cursor.execute("SELECT * FROM clientes")
    for row in cursor.fetchall():
        tree.insert("", "end", values=(row[1], row[2], row[3], row[4]), tags=(row[0],))

def limpar_campos():
    entry_nome.delete(0, tk.END)
    entry_email.delete(0, tk.END)
    entry_telefone.delete(0, tk.END)
    entry_endereco.delete(0, tk.END)

def selecionar_item(event):
    selected = tree.focus()
    if not selected:
        return
    values = tree.item(selected, 'values')
    entry_nome.delete(0, tk.END)
    entry_email.delete(0, tk.END)
    entry_telefone.delete(0, tk.END)
    entry_endereco.delete(0, tk.END)

    entry_nome.insert(0, values[0])
    entry_email.insert(0, values[1])
    entry_telefone.insert(0, values[2])
    entry_endereco.insert(0, values[3])

def editar_cliente():
    selected = tree.focus()
    if not selected:
        messagebox.showwarning("Atenção", "Selecione um cliente para editar.")
        return
    id_cliente = tree.item(selected, 'tags')[0]

    novo_nome = entry_nome.get()
    novo_email = entry_email.get()
    novo_telefone = entry_telefone.get()
    novo_endereco = entry_endereco.get()

    cursor.execute("""
    UPDATE clientes SET nome=?, email=?, telefone=?, endereco=?
    WHERE id=?
    """, (novo_nome, novo_email, novo_telefone, novo_endereco, id_cliente))
    conn.commit()
    mostrar_usuario()
    limpar_campos()

def excluir_cliente():
    selected = tree.focus()
    if not selected:
        messagebox.showwarning("Atenção", "Selecione um cliente para excluir.")
        return
    id_cliente = tree.item(selected, 'tags')[0]

    cursor.execute("DELETE FROM clientes WHERE id=?", (id_cliente,))
    conn.commit()
    mostrar_usuario()
    limpar_campos()

janela = tk.Tk()
janela.configure(bg="#D3D3D3")
janela.title("CRUD - PROJETO FINAL")
janela.geometry('800x600')

TITULO = tk.Label(janela, text="CADASTRO DE CLIENTES - XYZ", fg="#808080", bg="#D3D3D3", font=("roboto", 20, "bold"))
TITULO.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

label_nome = tk.Label(janela, text="NOME: ", fg="black", bg="#808080", font=("arial", 10))
label_nome.grid(row=1, column=0, padx=10, pady=5)
entry_nome = tk.Entry(janela, font=("arial", 15))
entry_nome.grid(row=1, column=1, padx=10, pady=5)

label_email = tk.Label(janela, text="E-MAIL: ", fg="black", bg="#808080", font=("arial", 10))
label_email.grid(row=2, column=0, padx=10, pady=5)
entry_email = tk.Entry(janela, font=("arial", 15))
entry_email.grid(row=2, column=1, padx=10, pady=5)

label_telefone = tk.Label(janela, text="TELEFONE: ", fg="black", bg="#808080", font=("arial", 10))
label_telefone.grid(row=3, column=0, padx=10, pady=5)
entry_telefone = tk.Entry(janela, font=("arial", 15))
entry_telefone.grid(row=3, column=1, padx=10, pady=5)

label_endereco = tk.Label(janela, text="ENDEREÇO: ", fg="black", bg="#808080", font=("arial", 10))
label_endereco.grid(row=4, column=0, padx=10, pady=5)
entry_endereco = tk.Entry(janela, font=("arial", 15))
entry_endereco.grid(row=4, column=1, padx=10, pady=5)


tk.Button(janela, text="Cadastrar", fg= "black", bg= "green", command=cadastrar_cliente).grid(row=5, column=0)
tk.Button(janela, text="Editar", fg= "black", bg="blue", command=editar_cliente).grid(row=5, column=1)
tk.Button(janela, text="Excluir", fg="black", bg="red", command=excluir_cliente).grid(row=5, column=2)


tree = ttk.Treeview(janela, columns=("Nome", "Email", "Telefone", "Endereço"), show="headings")
tree.heading("Nome", text="Nome")
tree.heading("Email", text="Email")
tree.heading("Telefone", text="Telefone")
tree.heading("Endereço", text="Endereço")
tree.grid(row=6, column=0, columnspan=4)

tree.bind("<Double-1>", selecionar_item)
mostrar_usuario()
janela.mainloop()
