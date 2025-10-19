import customtkinter as ctk
from tkinter import messagebox
from main import get_conn, DataBase

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

DataBase.create_tables()

root = ctk.CTk()
root.title("BAWIZ SYSTEM")
root.geometry("600x400")
root.resizable(False, False)

title = ctk.CTkLabel(root,text="INICIAR SESIÓN",font=("Open Sans", 32, "bold"),text_color="#111111")
title.pack(pady=25)
# frame nombre
# espacio gris
frame_nombre = ctk.CTkFrame(root, fg_color="#e0e0e0", corner_radius=20)
frame_nombre.pack(pady=10, ipadx=15, ipady=10)

frame_nombre.grid_columnconfigure(0, minsize=150)
frame_nombre.grid_columnconfigure(1, minsize=300)

label_nombre = ctk.CTkLabel(frame_nombre, text="Nombre", font=("Open Sans", 14))
label_nombre.grid(row=0, column=0, padx=(10, 5), pady=10, sticky="e")

entry_nombre = ctk.CTkEntry(frame_nombre,width=280,height=35,corner_radius=10,fg_color="white",border_color="#cfcfcf",text_color="black",font=("Open Sans", 12))
entry_nombre.grid(row=0, column=1, padx=(5, 10), pady=10, sticky="w")

# frame id
# espacio gris
frame_id = ctk.CTkFrame(root, fg_color="#e0e0e0", corner_radius=20)
frame_id.pack(pady=10, ipadx=15, ipady=10)

frame_id.grid_columnconfigure(0, minsize=150)
frame_id.grid_columnconfigure(1, minsize=300)

label_id = ctk.CTkLabel(frame_id, text="ID", font=("Open Sans", 14))
label_id.grid(row=0, column=0, padx=(10, 5), pady=10, sticky="e")

entry_id = ctk.CTkEntry(frame_id,width=280,height=35,corner_radius=10,fg_color="white",border_color="#cfcfcf",text_color="black",font=("Open Sans", 12))
entry_id.grid(row=0, column=1, padx=(5, 10), pady=10, sticky="w")

def validate_user(table, campo_id, id_usuario, name):
    try:
        with get_conn() as conn:
            query = f"""
                SELECT 1
                FROM {table} t
                JOIN users u ON t.user_id = u.user_id
                WHERE t.{campo_id} = ? AND u.name = ?
            """
            result = conn.execute(query, (id_usuario, name)).fetchone()
            return result is not None
    except Exception as e:
        messagebox.showerror("Error de BD", str(e))
        return False

def login_admin():
    name = entry_nombre.get().strip()
    user_id = entry_id.get().strip()

    if not user_id or not name:
        messagebox.showerror("Error", "Debe llenar todos los campos.")
        return

    if not user_id.startswith("ADM"):
        messagebox.showerror("Error", "El ID de administrador debe iniciar con 'ADM'.")
        return

    if validate_user("admins", "admin_id", user_id, name):
        messagebox.showinfo("Éxito", f"Bienvenido administrador {name}")
    else:
        messagebox.showerror("Error", "Credenciales incorrectas o usuario no registrado.")

def login_collab():
    name = entry_nombre.get().strip()
    user_id = entry_id.get().strip()

    if not user_id or not name:
        messagebox.showerror("Error", "Debe llenar todos los campos.")
        return

    if not user_id.startswith("COL"):
        messagebox.showerror("Error", "El ID del colaborador debe iniciar con 'COL'.")
        return

    if validate_user("collaborators", "collab_id", user_id, name):
        messagebox.showinfo("Éxito", f"Bienvenido colaborador {name}")
    else:
        messagebox.showerror("Error", "Credenciales incorrectas o usuario no registrado.")


# general botones
frame_botones = ctk.CTkFrame(root, fg_color="transparent")
frame_botones.pack(pady=25)

# boton admin
btn_admin = ctk.CTkButton(frame_botones,text="Ingresar (Admin)",width=150,height=45,corner_radius=25,fg_color="#bfbfbf",hover_color="#a9a9a9",text_color="black",font=("Open Sans", 12, "underline"),command=login_admin)
btn_admin.grid(row=0, column=0, padx=15)

# boton collab
btn_collab = ctk.CTkButton(frame_botones,text="Ingresar (Colab)",width=150,height=45,corner_radius=25,fg_color="#bfbfbf",hover_color="#a9a9a9",text_color="black",font=("Open Sans", 12, "underline"),command=login_collab)
btn_collab.grid(row=0, column=1, padx=15)

root.mainloop()