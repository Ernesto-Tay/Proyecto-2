import customtkinter as ctk
import tkinter.messagebox as mbox

class CollabUI(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="white")
        self.master = master
        self.pack(expand=True, fill="both")

        # elementos principales
        self.header = None
        self.body = None
        self.fullscreen_frame = None  # frame para vistas completas

        # submenús
        self.active_submenu = None
        self.last_opened = None  # guarda cuál botón se abrió

        # inicialización
        self.create_header()
        self.body = ctk.CTkFrame(self, fg_color="white")
        self.body.pack(expand=True, fill="both")

    def _open_fullscreen_view(self):
        self.header.pack_forget()
        self.body.pack_forget()
        self.fullscreen_frame = ctk.CTkFrame(self, fg_color="#fafafa")
        self.fullscreen_frame.pack(expand=True, fill="both")
        self.fullscreen_frame.lift()
        self.update_idletasks()  # refresca el diseño
        return self.fullscreen_frame

    def _close_fullscreen_view(self):
        if self.fullscreen_frame:
            self.fullscreen_frame.destroy()
            self.fullscreen_frame = None

        self.header.pack(side="top", fill="x")  # restaura el header
        self.body.pack(expand=True, fill="both")  # restaura el body

    def create_header(self):
        self.header = ctk.CTkFrame(self, fg_color="#e0e0e0", height=60, corner_radius=0)
        self.header.pack(side="top", fill="x")

        # frame izquierdo
        left = ctk.CTkFrame(self.header, fg_color="transparent")
        left.pack(side="left", padx=15, pady=10)
        # botones principales
        btn_sales = ctk.CTkButton(left, text="Ventas", width=130, height=36,corner_radius=18, fg_color="white", hover_color="#f2f2f2",text_color="black", font=("Open Sans", 13, "bold"),command=lambda: self.toggle_submenu("sales", btn_sales))
        btn_sales.pack(side="left", padx=6)

        btn_clients = ctk.CTkButton(left, text="Clientes", width=130, height=36,corner_radius=18, fg_color="white", hover_color="#f2f2f2",text_color="black", font=("Open Sans", 13, "bold"),command=lambda: self.toggle_submenu("clients", btn_clients))
        btn_clients.pack(side="left", padx=6)

        # frame derecho
        right = ctk.CTkFrame(self.header, fg_color="transparent")
        right.pack(side="right", padx=15, pady=10)

        btn_logout = ctk.CTkButton(right, text="Cerrar Sesión", width=130, height=36,corner_radius=18, fg_color="white", hover_color="#f2f2f2",text_color="black", font=("Open Sans", 13, "bold"),command=self.logout)
        btn_logout.pack(side="right", padx=6)

    def toggle_submenu(self, name, parent_button):  # configuración submenús
        if self.active_submenu:  # si ya hay uno abierto, se destruye
            if self.active_submenu.winfo_exists():
                self.active_submenu.destroy()
            self.active_submenu = None

            if self.last_opened == name:  # si se presiona el mismo botón, no se vuelve a abrir
                self.last_opened = None
                return

        # submenu flotante (CTkToplevel)
        submenu = ctk.CTkToplevel(self)
        submenu.overrideredirect(True)
        submenu.configure(fg_color="#f8f8f8")
        submenu.attributes("-topmost", True)  # siempre al frente

        # posición justo debajo del botón
        ax = parent_button.winfo_rootx()
        ay = parent_button.winfo_rooty() + parent_button.winfo_height()
        submenu.geometry(f"+{ax}+{ay}")

        # frame interno del submenú
        frame = ctk.CTkFrame(submenu, fg_color="#ffffff", corner_radius=12,border_width=1, border_color="#d0d0d0")
        frame.pack(padx=4, pady=4)

        # opciones según el botón presionado
        if name == "sales":
            self.add_submenu_button(frame, "Agregar venta", lambda: self.action("Agregar venta"))
            self.add_submenu_button(frame, "Ver ventas", lambda: self.action("Ver ventas"))
        elif name == "clients":
            self.add_submenu_button(frame, "Agregar cliente", lambda: self.action("Agregar cliente"))
            self.add_submenu_button(frame, "Ver clientes", lambda: self.action("Ver clientes"))

        # guarda referencia del submenú
        self.active_submenu = submenu
        self.last_opened = name

        # cierra automáticamente al perder el foco
        submenu.bind("<FocusOut>", lambda e: submenu.destroy())
        submenu.focus_force()

    def add_submenu_button(self, parent, text, command):
        btn = ctk.CTkButton(parent, text=text, width=180, height=30,fg_color="#ffffff", hover_color="#e6e6e6",text_color="black", font=("Open Sans", 12),command=command)
        btn.pack(padx=8, pady=4)

    # formulario agregar cliente
    def view_create_client(self):
        frame = self._open_fullscreen_view()  # abre pantalla completa

        title = ctk.CTkLabel(frame, text="Crear cliente",font=("Open Sans", 50, "bold"), text_color="#111111")
        title.pack(pady=(60, 40))

        # nombre
        row_name = ctk.CTkFrame(frame, fg_color="#e0e0e0", corner_radius=20)
        row_name.pack(pady=10, ipadx=10, ipady=6)
        row_name.grid_columnconfigure(0, minsize=160)
        row_name.grid_columnconfigure(1, minsize=320)
        ctk.CTkLabel(row_name, text="Nombre", font=("Open Sans", 18)).grid(row=0, column=0, padx=(14, 8), pady=8, sticky="nsew")
        self.ent_nombre = ctk.CTkEntry(row_name, width=300, height=36,corner_radius=14, fg_color="white",text_color="black", border_color="#cfcfcf")
        self.ent_nombre.grid(row=0, column=1, padx=(8, 14), pady=8, sticky="w")

        # teléfono
        row_tel = ctk.CTkFrame(frame, fg_color="#e0e0e0", corner_radius=20)
        row_tel.pack(pady=10, ipadx=10, ipady=6)
        row_tel.grid_columnconfigure(0, minsize=160)
        row_tel.grid_columnconfigure(1, minsize=320)
        ctk.CTkLabel(row_tel, text="Teléfono", font=("Open Sans", 18)).grid(row=0, column=0, padx=(14, 8), pady=8, sticky="nsew")
        self.ent_tel = ctk.CTkEntry(row_tel, width=300, height=36,corner_radius=14, fg_color="white",text_color="black", border_color="#cfcfcf")
        self.ent_tel.grid(row=0, column=1, padx=(8, 14), pady=8, sticky="w")

        # botones
        btns = ctk.CTkFrame(frame, fg_color="transparent", corner_radius=20)
        btns.pack(pady=25)

        # botón crear cliente
        btn_crclient = ctk.CTkButton(btns, text="Crear cliente", width=240, height=45,corner_radius=22, fg_color="#e0e0e0",hover_color="#9e9e9e", text_color="black",font=("Open Sans", 15, "bold", "underline"))
        btn_crclient.pack(pady=(0, 12))

        # botón volver
        btn_back = ctk.CTkButton(btns, text="Volver", width=240, height=45,corner_radius=22, fg_color="#e0e0e0",hover_color="#9e9e9e", text_color="black",font=("Open Sans", 15, "bold", "underline"),command=self._close_fullscreen_view)
        btn_back.pack()

    def action(self, msg):
        if self.active_submenu:
            self.active_submenu.destroy()
            self.active_submenu = None

        if msg == "Agregar cliente":
            self.view_create_client()

    def logout(self):
        confirm = mbox.askyesno("Cerrar sesión", "¿Deseas cerrar tu sesión actual?")
        if confirm:
            from login import LoginUI
            self.pack_forget()
            LoginUI(self.master)