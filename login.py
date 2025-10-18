import tkinter as tk
from tkinter import ttk, messagebox
from main import get_conn, DataBase

DataBase.create_tables()

root = tk.Tk()
root.title("BAWIZ SYSTEM - Login")
root.geometry("600x400")
root.resizable(False, False)

frame = ttk.Frame(root, padding=20)
frame.pack(expand=True)

ttk.Label(frame, text="INICIAR SESIÓN", font=("Open Sans", 24, "bold")).grid(row=0, column=0, columnspan=2, pady=20)

ttk.Label(frame, text="Nombre:").grid(row=1, column=0, sticky="e", padx=10, pady=10)
entry_name = ttk.Entry(frame, width=30)
entry_name.grid(row=2, column=1, padx=10, pady=10)

ttk.Label(frame, text="ID de usuario:").grid(row=2, column=0, sticky="e", padx=10, pady=10)
entry_id = ttk.Entry(frame, width=30)
entry_id.grid(row=1, column=1, padx=10, pady=10)

def validar_usuario(tabla, campo_id, id_usuario, nombre):
    try:
        with get_conn() as conn:
            query = f"""
                SELECT 1
                FROM {tabla} t
                JOIN users u ON t.user_id = u.user_id
                WHERE t.{campo_id} = ? AND u.name = ?
            """
            result = conn.execute(query, (id_usuario, nombre)).fetchone()
            return result is not None
    except Exception as e:
        messagebox.showerror("Error de BD", str(e))
        return False

# botones
def login_admin():
    name = entry_name.get().strip()
    user_id = entry_id.get().strip()

    if not user_id or not name:
        messagebox.showerror("Error", "Debe llenar todos los campos.")
        return

    if not user_id.startswith("ADM"):
        messagebox.showerror("Error", "El ID de administrador debe iniciar con 'ADM'.")
        return

    if validar_usuario("admins", "admin_id", user_id, name):
        messagebox.showinfo("Éxito", f"Bienvenido administrador {name}")
    else:
        messagebox.showerror("Error", "Credenciales incorrectas o usuario no registrado.")

def login_collab():
    name = entry_name.get().strip()
    user_id = entry_id.get().strip()

    if not user_id or not name:
        messagebox.showerror("Error", "Debe llenar todos los campos.")
        return

    if not user_id.startswith("COL"):
        messagebox.showerror("Error", "El ID del colaborador debe iniciar con 'COL'.")
        return

    if validar_usuario("collaborators", "collab_id", user_id, name):
        messagebox.showinfo("Éxito", f"Bienvenido colaborador {name}")
    else:
        messagebox.showerror("Error", "Credenciales incorrectas o usuario no registrado.")

# Estilo de botones
style = ttk.Style()
style.configure("GrayButton.TButton",background="#9b9b9b",foreground="#000000",font=("Open Sans", 11, "underline"),padding=10,borderwidth=0,relief="flat")

# Visualización
style.map("GrayButton.TButton",background=[("active", "#c0c0c0"),("pressed", "#a9a9a9")])
buttons = ttk.Frame(frame)
buttons.grid(row=3, column=0, columnspan=2, pady=30)

ttk.Button(buttons, text="Ingresar (admin)", style="GrayButton.TButton",command=login_admin).grid(row=0, column=0, padx=10)
ttk.Button(buttons, text="Ingresar (collab)", style="GrayButton.TButton",command=login_collab).grid(row=0, column=1, padx=10)

root.mainloop()