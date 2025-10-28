import customtkinter as ctk
import tkinter.messagebox as mbox

class CollabUI(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="white")
        self.master = master
        self.pack(expand=True, fill="both")
        self.create_header()
        self.active_submenu = None
        self.last_opened

    def create_header(self):
        header = ctk.CTkFrame(self, fg_color="#e0e0e0", height=60, corner_radius=0)
        header.pack(side="top", fill="x")

        # frame izquierdo
        left = ctk.CTkFrame(header, fg_color="transparent")
        left.pack(side="left", padx=15, pady=10)

        # botones principales
        btn_sales = ctk.CTkButton(left, text="Ventas", width=130, height=36,corner_radius=18, fg_color="white", hover_color="#f2f2f2",text_color="black", font=("Open Sans", 13, "bold"),command=lambda: self.toggle_submenu("sales", btn_sales))
        btn_sales.pack(side="left", padx=6)

        btn_clients = ctk.CTkButton(left, text="Clientes", width=130, height=36,corner_radius=18, fg_color="white", hover_color="#f2f2f2",text_color="black", font=("Open Sans", 13, "bold"),command=lambda: self.toggle_submenu("clients", btn_clients))
        btn_clients.pack(side="left", padx=6)

        # frame derecho
        right = ctk.CTkFrame(header, fg_color="transparent")
        right.pack(side="right", padx=15, pady=10)

        btn_logout = ctk.CTkButton(right, text="Cerrar Sesión", width=130, height=36, corner_radius=18,fg_color="white", hover_color="#f2f2f2", text_color="black", font=("Open Sans", 13, "bold"), command = self.logout)
        btn_logout.pack(side="right", padx=6)

    def toggle_submenu(self, name, parent_button):
        # Cierra cualquier submenú abierto
        if self.active_submenu:
            if self.active_submenu.winfo_exists():
                self.active_submenu.destroy()
            self.active_submenu = None

            if self.last_opened == name:
                self.last_opened = None
                return

        # Se crea el submenú como ventana flotante (independiente)
        submenu = ctk.CTkToplevel(self)
        submenu.overrideredirect(True)
        submenu.configure(fg_color="#f8f8f8")
        submenu.attributes("-topmost", True)  # se mantiene al frente

        # Se coloca justo debajo del botón
        ax = parent_button.winfo_rootx()
        ay = parent_button.winfo_rooty() + parent_button.winfo_height()
        submenu.geometry(f"+{ax}+{ay}")

        # Cuerpo del submenú
        frame = ctk.CTkFrame(submenu, fg_color="#ffffff", corner_radius=12,border_width=1, border_color="#d0d0d0")
        frame.pack(padx=4, pady=4)

        if name == "sales":
            self.add_submenu_button(frame, "Agregar venta", lambda: self.action("Agregar venta"))
            self.add_submenu_button(frame, "Ver ventas", lambda: self.action("Ver ventas"))
        elif name == "clients":
            self.add_submenu_button(frame, "Agregar cliente", lambda: self.action("Agregar cliente"))
            self.add_submenu_button(frame, "Ver clientes", lambda: self.action("Ver clientes"))

        self.active_submenu = submenu
        self.last_opened = name # guarda la referencia para el __init__
        submenu.bind("<FocusOut>", lambda e: submenu.destroy()) # cierra automáticamente al perder el foco
        submenu.focus_force()

    def add_submenu_button(self, parent, text, command):
        btn = ctk.CTkButton(parent, text=text, width=180, height=30,fg_color="#ffffff", hover_color="#e6e6e6",text_color="black", font=("Open Sans", 12),command=command)
        btn.pack(padx=8, pady=4)

    def action(self, msg):
        pass

    def logout(self):
        confirm = mbox.askyesno("Cerrar sesión", "¿Deseas cerrar tu sesión actual?")
        if confirm:
            from login import LoginUI
            self.pack_forget()
            LoginUI(self.master)