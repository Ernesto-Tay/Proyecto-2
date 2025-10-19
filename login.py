import customtkinter as ctk
from tkinter import messagebox
from main import get_conn, DataBase

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

DataBase.create_tables()

root = ctk.CTk()
root.title("BAWIZ SYSTEM")
root.geometry("800x500")
root.resizable(False, False)

#titulo
title = ctk.CTkLabel(root,text="INICIAR\nSESIÓN",font=("Open Sans", 62, "bold"),text_color="#111111")
title.pack(pady=25)

# frame nombre
# espacio gris
frame_nombre = ctk.CTkFrame(root, fg_color="#e0e0e0", corner_radius=20)
frame_nombre.pack(pady=5, ipadx=10, ipady=4)

frame_nombre.grid_columnconfigure(0, minsize=150)
frame_nombre.grid_columnconfigure(1, minsize=300)

label_nombre = ctk.CTkLabel(frame_nombre, text="Nombre", font=("Open Sans", 18))
label_nombre.grid(row=0, column=0, padx=(10, 5), pady=10, sticky="nwes")

entry_nombre = ctk.CTkEntry(frame_nombre,width=280, height=35,corner_radius=10,fg_color="white",border_color="#cfcfcf",text_color="black",font=("Open Sans", 12))
entry_nombre.grid(row=0, column=1, padx=(5, 10), pady=10, sticky="w")

# frame id
# espacio gris
frame_id = ctk.CTkFrame(root, fg_color="#e0e0e0", corner_radius=20)
frame_id.pack(pady=5, ipadx=10, ipady=4)

frame_id.grid_columnconfigure(0, minsize=150)
frame_id.grid_columnconfigure(1, minsize=300)

label_id = ctk.CTkLabel(frame_id, text="ID", font=("Open Sans", 18))
label_id.grid(row=0, column=0, padx=(10, 5), pady=10, sticky="nwes")

entry_id = ctk.CTkEntry(frame_id,width=280,height=35,corner_radius=10,fg_color="white",border_color="#cfcfcf",text_color="black",font=("Open Sans", 12))
entry_id.grid(row=0, column=1, padx=(5, 10), pady=10, sticky="w")

def validate_user(tabla, campo_id, id_usuario, nombre):
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

def login():
    name = entry_nombre.get().strip()
    user_id = entry_id.get().strip()

    if not user_id or not name:
        messagebox.showerror("Error", "Debe llenar todos los campos.")
        return

    if user_id.startswith("ADM"):
        if validate_user("admins", "admin_id", user_id, name):
            messagebox.showinfo("Éxito", f"Bienvenido administrador {name}")
        else:
            messagebox.showerror("Error", "Credenciales de administrador incorrectas o no registradas.")

    elif user_id.startswith("COL"):
        if validate_user("collaborators", "collab_id", user_id, name):
            messagebox.showinfo("Éxito", f"Bienvenido colaborador {name}")
        else:
            messagebox.showerror("Error", "Credenciales de colaborador incorrectas o no registradas.")

    else:
        messagebox.showerror("Error", "El ID debe iniciar con 'ADM' o 'COL' según su tipo de usuario.")

# botón de inicio de sesión
btn_login = ctk.CTkButton(root,text="Iniciar sesión",width=200,height=50,corner_radius=30,fg_color="#e0e0e0",hover_color="#a9a9a9",text_color="black",font=("Open Sans", 18, "bold", "underline"),command=login)
btn_login.pack(pady=35)

root.mainloop()