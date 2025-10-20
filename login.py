import customtkinter as ctk
from tkinter import messagebox
from main import get_conn, DataBase
from ui_admin import AdminUI
from ui_collaborator import CollabUI

class LoginUI(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.pack(expand=True, fill="both")

        DataBase.create_tables()

        title = ctk.CTkLabel(self,text="INICIAR\nSESIÓN",font=("Open Sans", 62, "bold"),text_color="#111111")
        title.pack(pady=25)

        # Frame Nombre
        frame_nombre = ctk.CTkFrame(self, fg_color="#e0e0e0", corner_radius=20)
        frame_nombre.pack(pady=5, ipadx=10, ipady=4)

        frame_nombre.grid_columnconfigure(0, minsize=150)
        frame_nombre.grid_columnconfigure(1, minsize=300)

        label_nombre = ctk.CTkLabel(frame_nombre, text="Nombre", font=("Open Sans", 18, "bold"))
        label_nombre.grid(row=0, column=0, padx=(10, 5), pady=10, sticky="e")

        self.entry_nombre = ctk.CTkEntry(frame_nombre,width=280,height=35,corner_radius=10,fg_color="white",border_color="#cfcfcf",text_color="black",font=("Open Sans", 12))
        self.entry_nombre.grid(row=0, column=1, padx=(5, 10), pady=10, sticky="w")

        # frame ID
        frame_id = ctk.CTkFrame(self, fg_color="#e0e0e0", corner_radius=20)
        frame_id.pack(pady=5, ipadx=10, ipady=4)

        frame_id.grid_columnconfigure(0, minsize=150)
        frame_id.grid_columnconfigure(1, minsize=300)

        label_id = ctk.CTkLabel(frame_id, text="ID", font=("Open Sans", 18, "bold"))
        label_id.grid(row=0, column=0, padx=(10, 5), pady=10, sticky="e")

        self.entry_id = ctk.CTkEntry(frame_id,width=280,height=35,corner_radius=10,fg_color="white",border_color="#cfcfcf",text_color="black",font=("Open Sans", 12))
        self.entry_id.grid(row=0, column=1, padx=(5, 10), pady=10, sticky="w")

        # botón
        btn_login = ctk.CTkButton(self,text="Iniciar sesión",width=200,height=50,corner_radius=30,fg_color="#e0e0e0",hover_color="#a9a9a9",text_color="black",font=("Open Sans", 18, "bold", "underline"),command=self.login)
        btn_login.pack(pady=35)

    def validate_user(self, table, campo_id, id_usuario, nombre):
        try:
            with get_conn() as conn:
                query = f"""
                    SELECT 1
                    FROM {table} t
                    JOIN users u ON t.user_id = u.user_id
                    WHERE t.{campo_id} = ? AND u.name = ?
                """
                result = conn.execute(query, (id_usuario, nombre)).fetchone()
                return result is not None
        except Exception as e:
            messagebox.showerror("Error de BD", str(e))
            return False
    # login
    def login(self):
        name = self.entry_nombre.get().strip()
        user_id = self.entry_id.get().strip()

        if not user_id or not name:
            messagebox.showerror("Error", "Debe llenar todos los campos.")
            return

        if user_id.startswith("ADM"):
            if self.validate_user("admins", "admin_id", user_id, name):
                messagebox.showinfo("Éxito", f"Bienvenido administrador {name}")
                self.change_to_admin()

            else:
                messagebox.showerror("Error", "Credenciales de administrador incorrectas o no registradas.")

        elif user_id.startswith("COL"):
            if self.validate_user("collaborators", "collab_id", user_id, name):
                messagebox.showinfo("Éxito", f"Bienvenido colaborador {name}")
                self.change_to_collab()

            else:
                messagebox.showerror("Error", "Credenciales de colaborador incorrectas o no registradas.")

        else:
            messagebox.showerror("Error", "El ID debe iniciar con 'ADM' o 'COL' según su tipo de usuario.")

    def change_to_admin(self):
        self.pack_forget()
        AdminUI(self.master)

    def change_to_collab(self):
        self.pack_forget()
        CollabUI(self.master)