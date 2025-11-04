import customtkinter as ctk
from customtkinter import CTkImage
from tkinter import messagebox
from main import get_conn, DataBase
from ui_admin import AdminUI
from ui_collaborator import CollabUI
from PIL import Image

class LoginUI(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="white")
        self.master = master
        self.pack(expand=True, fill="both")
        self.active_submenu = None

        DataBase.create_tables()

        img_frame = ctk.CTkFrame(self, width=280,height=35,fg_color="#004857",border_color="#cfcfcf")
        img_frame.pack(side = "left", expand=True, fill="both")

        try:
            logo_path = "logo_bawiz.png"

            # Carga la imagen sin deformar
            logo_img = CTkImage(light_image=Image.open(logo_path), size=(230, 230))

            # Muestra la imagen centrada
            logo_label = ctk.CTkLabel(img_frame, image=logo_img, text="")
            logo_label.place(relx=0.5, rely=0.4, anchor="center")

            # Texto debajo del logo (opcional)
            ctk.CTkLabel(img_frame,text="BaWiz System",font=("Open Sans", 24, "bold"),text_color="white").place(relx=0.5, rely=0.60, anchor="center")

        except Exception as e:
            print(f"No se pudo cargar la imagen: {e}")

        form_frame = ctk.CTkFrame(self, width=230,height=35,fg_color="#f4f1ec",border_color="#cfcfcf")
        form_frame.pack(side = "left", expand=True, fill="both")

        title = ctk.CTkLabel(form_frame,text="INICIAR\nSESIÓN",font=("Open Sans", 48, "bold"),text_color="#004857")
        title.pack(pady=(100, 25))

        # Frame Nombre
        frame_nombre = ctk.CTkFrame(form_frame, fg_color="#f86a20", corner_radius=20)
        frame_nombre.pack(pady=5, ipadx=10, ipady=4)

        frame_nombre.grid_columnconfigure(0, minsize=150)
        frame_nombre.grid_columnconfigure(1, minsize=250)

        label_nombre = ctk.CTkLabel(frame_nombre, text="Nombre", font=("Open Sans", 20,"bold"),text_color="#004857")
        label_nombre.grid(row=0, column=0, padx=(10, 5), pady=10, sticky="nsew")

        self.entry_nombre = ctk.CTkEntry(frame_nombre,width=280,height=35,corner_radius=10,fg_color="white",border_color="#cfcfcf",text_color="black",font=("Open Sans", 12))
        self.entry_nombre.grid(row=0, column=1, padx=(5, 10), pady=10, sticky="w")

        # frame ID
        frame_id = ctk.CTkFrame(form_frame, fg_color="#f86a20", corner_radius=20)
        frame_id.pack(pady=5, ipadx=10, ipady=4)

        frame_id.grid_columnconfigure(0, minsize=150)
        frame_id.grid_columnconfigure(1, minsize=300)

        label_id = ctk.CTkLabel(frame_id, text="ID", font=("Open Sans", 20,"bold"),text_color="#004857")
        label_id.grid(row=0, column=0, padx=(10, 5), pady=10, sticky="nsew")

        self.entry_id = ctk.CTkEntry(frame_id,width=280,height=35,corner_radius=10,fg_color="white",border_color="#cfcfcf",text_color="black",font=("Open Sans", 12), show = "●")
        self.entry_id.grid(row=0, column=1, padx=(5, 10), pady=10, sticky="w")

        # botón
        btn_login = ctk.CTkButton(form_frame,text="Iniciar sesión",width=200,height=50,corner_radius=30,fg_color="#f86a20",hover_color="#cd5618",text_color="#004857",font=("Open Sans", 20, "bold", "underline"),command=self.login)
        btn_login.pack(pady=35)

    def validate_user(self, table, campo_id, id_usuario, nombre):
        try:
            with get_conn() as conn:
                query = f"""SELECT u.user_id, u.name, u.phone FROM {table} t JOIN users u ON t.user_id = u.user_id WHERE t.{campo_id} = ? AND u.name = ?"""
                result = conn.execute(query, (id_usuario, nombre)).fetchone()
                return result
        except Exception as e:
            messagebox.showerror("Error de BD", str(e))
            return None
    # login
    def login(self):
        name = self.entry_nombre.get().strip()
        user_id = self.entry_id.get().strip()

        if not user_id or not name:
            messagebox.showerror("Error", "Debe llenar todos los campos.")
            return

        user_data = None
        if user_id.startswith("ADM"):
            user_data = self.validate_user("admins", "admin_id", user_id, name)
            if user_data:
                self.pack_forget()
                AdminUI(self.master,current_user={"name": user_data["name"], "phone": user_data["phone"], "id": user_id})
                return
            else:
                messagebox.showerror("Error", "Credenciales de administrador incorrectas o no registradas.")

        elif user_id.startswith("COL"):
            user_data = self.validate_user("collaborators", "collab_id", user_id, name)

            if user_data:
                self.pack_forget()
                CollabUI(self.master,current_user={"name": user_data["name"], "phone": user_data["phone"], "id": user_id})
                return

            messagebox.showerror("Error", "Credenciales de colaborador incorrectas o no registradas.")
        else:
            messagebox.showerror("Error", "ID incorrecto.")

    def change_to_admin(self):
        self.pack_forget()
        AdminUI(self.master,current_user={"name": self.entry_nombre.get(), "phone": "Desconocido"})

    def change_to_collab(self):
        self.pack_forget()
        CollabUI(self.master,current_user={"name": self.entry_nombre.get(), "phone": "Desconocido"})