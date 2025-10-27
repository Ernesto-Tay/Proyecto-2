import customtkinter as ctk
import tkinter.messagebox as mbox

class AdminUI(ctk.CTkFrame):
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
        self.fullscreen_frame = ctk.CTkFrame(self, fg_color="#fafafa")  # color de fondo
        self.fullscreen_frame.pack(expand=True, fill="both")
        return self.fullscreen_frame

    def _close_fullscreen_view(self):
        if self.fullscreen_frame:    # Cierra la vista completa y regresa al diseño original
            self.fullscreen_frame.destroy()
            self.fullscreen_frame = None

        self.header.pack(side="top", fill="x") # Restaura header y body
        self.body.pack(expand=True, fill="both")

    def create_header(self):
        self.header = ctk.CTkFrame(self, fg_color="#e0e0e0", height=60, corner_radius=0)
        self.header.pack(side="top", fill="x")

        # frame izquierdo
        left = ctk.CTkFrame(self.header, fg_color="transparent")
        left.pack(side="left", padx=15, pady=10)

        # botones principales
        btn_colab = ctk.CTkButton(left, text="Colaboradores", width=130, height=36,corner_radius=18, fg_color="white", hover_color="#f2f2f2",text_color="black", font=("Open Sans", 13, "bold"),command=lambda: self.toggle_submenu("colab", btn_colab))
        btn_colab.pack(side="left", padx=6)

        btn_provider = ctk.CTkButton(left, text="Proveedores", width=130, height=36,corner_radius=18, fg_color="white", hover_color="#f2f2f2",text_color="black", font=("Open Sans", 13, "bold"),command=lambda: self.toggle_submenu("provider", btn_provider))
        btn_provider.pack(side="left", padx=6)

        btn_sales = ctk.CTkButton(left, text="Ventas", width=130, height=36,corner_radius=18, fg_color="white", hover_color="#f2f2f2",text_color="black", font=("Open Sans", 13, "bold"),command=lambda: self.toggle_submenu("sales", btn_sales))
        btn_sales.pack(side="left", padx=6)

        btn_products = ctk.CTkButton(left, text="Productos", width=130, height=36,corner_radius=18, fg_color="white", hover_color="#f2f2f2",text_color="black", font=("Open Sans", 13, "bold"),command=lambda: self.toggle_submenu("products", btn_products))
        btn_products.pack(side="left", padx=6)

        btn_clients = ctk.CTkButton(left, text="Clientes", width=130, height=36,corner_radius=18, fg_color="white", hover_color="#f2f2f2",text_color="black", font=("Open Sans", 13, "bold"),command=lambda: self.toggle_submenu("clients", btn_clients))
        btn_clients.pack(side="left", padx=6)

        # frame derecho
        right = ctk.CTkFrame(self.header, fg_color="transparent")
        right.pack(side="right", padx=15, pady=10)

        btn_logout = ctk.CTkButton(right, text="Cerrar Sesión", width=130, height=36,corner_radius=18, fg_color="white", hover_color="#f2f2f2",text_color="black", font=("Open Sans", 13, "bold"),command=self.logout)
        btn_logout.pack(side="right", padx=6)

    def toggle_submenu(self, name, parent_button): # configuracion submenus
        if self.active_submenu: # Guarda el submenú, si ya hay uno, se desaperece o se destruye antes de abrir otro.
            self.active_submenu.destroy()
            self.active_submenu = None

            if self.last_opened == name:
                self.last_opened = None
                return

        # frame submenu
        submenu = ctk.CTkFrame(self, fg_color="#f8f8f8", corner_radius=12,border_width=1, border_color="#d0d0d0")
        submenu.place(x=parent_button.winfo_rootx() - self.master.winfo_rootx(),y=parent_button.winfo_rooty() - self.master.winfo_rooty() + 50)

        if name == "colab":
            self.add_submenu_button(submenu, "Agregar colaborador",lambda: self.action("Agregar colaborador"))
            self.add_submenu_button(submenu, "Ver colaboradores",lambda: self.action("Ver colaboradores"))

        elif name == "provider":
            self.add_submenu_button(submenu, "Agregar proveedor",lambda: self.action("Agregar proveedor"))
            self.add_submenu_button(submenu, "Ver proveedores",lambda: self.action("Ver proveedores"))

        elif name == "sales":
            self.add_submenu_button(submenu, "Agregar ventas",lambda: self.action("Agregar ventas"))
            self.add_submenu_button(submenu, "Ver ventas",lambda: self.action("Ver ventas"))

        elif name == "products":
            self.add_submenu_button(submenu, "Agregar productos",lambda: self.action("Agregar productos"))
            self.add_submenu_button(submenu, "Ver productos",lambda: self.action("Ver productos"))

        elif name == "clients":
            self.add_submenu_button(submenu, "Agregar cliente", lambda: self.action("Agregar cliente"))
            self.add_submenu_button(submenu, "Ver clientes", lambda: self.action("Ver clientes"))

        self.active_submenu = submenu # Guarda la referencia en submenu
        self.last_opened = name

    def add_submenu_button(self, parent, text, command):
        btn = ctk.CTkButton(parent, text=text, width=180, height=30,fg_color="#ffffff", hover_color="#e6e6e6",text_color="black", font=("Open Sans", 12),command=command)
        btn.pack(padx=8, pady=4)

    def action(self, msg):
        """Determina qué vista abrir según el botón seleccionado."""
        # 🔹 cerrar submenú si está abierto
        if self.active_submenu:
            self.active_submenu.destroy()
            self.active_submenu = None

        if msg == "Agregar colaborador":
            self.view_create_collab()
        elif msg == "Ver colaboradores":
            self.view_list_collab()
        elif msg == "Agregar proveedor":
            self.view_create_provider()
        elif msg == "Ver proveedores":
            self.view_list_provider()
        else:
            mbox.showinfo("Acción", f"Seleccionaste: {msg}")

    # =====================================================
    # 🔹 5. FORMULARIO: CREAR COLABORADOR
    # =====================================================
    def view_create_collab(self):
        frame = self._open_fullscreen_view()

        title = ctk.CTkLabel(frame, text="Crear colaborador",
                             font=("Open Sans", 50, "bold"), text_color="#111111")
        title.pack(pady=(60, 40))

        # --- Fila: Nombre ---
        row_nombre = ctk.CTkFrame(frame, fg_color="#e0e0e0", corner_radius=20)
        row_nombre.pack(pady=10, ipadx=10, ipady=6)
        row_nombre.grid_columnconfigure(0, minsize=160)
        row_nombre.grid_columnconfigure(1, minsize=320)

        ctk.CTkLabel(row_nombre, text="Nombre", font=("Open Sans", 18)).grid(
            row=0, column=0, padx=(14, 8), pady=8, sticky="w")
        self.ent_nombre = ctk.CTkEntry(row_nombre, width=300, height=36,
                                       corner_radius=14, fg_color="white",
                                       text_color="black", border_color="#cfcfcf",
                                       placeholder_text="String")
        self.ent_nombre.grid(row=0, column=1, padx=(8, 14), pady=8, sticky="w")

        # --- Fila: Teléfono ---
        row_tel = ctk.CTkFrame(frame, fg_color="#e0e0e0", corner_radius=20)
        row_tel.pack(pady=10, ipadx=10, ipady=6)
        row_tel.grid_columnconfigure(0, minsize=160)
        row_tel.grid_columnconfigure(1, minsize=320)

        ctk.CTkLabel(row_tel, text="Teléfono", font=("Open Sans", 18)).grid(
            row=0, column=0, padx=(14, 8), pady=8, sticky="w")
        self.ent_tel = ctk.CTkEntry(row_tel, width=300, height=36,
                                    corner_radius=14, fg_color="white",
                                    text_color="black", border_color="#cfcfcf",
                                    placeholder_text="Int")
        self.ent_tel.grid(row=0, column=1, padx=(8, 14), pady=8, sticky="w")

        # --- Fila: Posición ---
        row_pos = ctk.CTkFrame(frame, fg_color="#e0e0e0", corner_radius=20)
        row_pos.pack(pady=10, ipadx=10, ipady=6)
        row_pos.grid_columnconfigure(0, minsize=160)
        row_pos.grid_columnconfigure(1, minsize=320)

        ctk.CTkLabel(row_pos, text="Posición", font=("Open Sans", 18)).grid(
            row=0, column=0, padx=(14, 8), pady=8, sticky="w")
        self.ent_pos = ctk.CTkEntry(row_pos, width=300, height=36,
                                    corner_radius=14, fg_color="white",
                                    text_color="black", border_color="#cfcfcf",
                                    placeholder_text="String")
        self.ent_pos.grid(row=0, column=1, padx=(8, 14), pady=8, sticky="w")

        # --- Botones ---
        btns = ctk.CTkFrame(frame, fg_color="white")
        btns.pack(pady=25)

        btn_create = ctk.CTkButton(btns, text="Crear uno", width=240, height=46,
                                   corner_radius=24, fg_color="#e0e0e0",
                                   hover_color="#a9a9a9", text_color="black",
                                   font=("Open Sans", 18, "bold", "underline"),
                                   command=self._submit_collab)
        btn_create.pack(pady=(0, 10))

        btn_back = ctk.CTkButton(btns, text="Volver", width=240, height=40,
                                 corner_radius=22, fg_color="white",
                                 hover_color="#f2f2f2", text_color="black",
                                 command=self._close_fullscreen_view)
        btn_back.pack()

    def _submit_collab(self):
        nombre = self.ent_nombre.get().strip()
        tel = self.ent_tel.get().strip()
        pos = self.ent_pos.get().strip()

        if not nombre or not tel or not pos:
            mbox.showerror("Error", "Debe llenar todos los campos.")
            return
        if not tel.isdigit():
            mbox.showerror("Error", "El teléfono debe ser numérico.")
            return

        # Aquí podrías guardar en base de datos
        mbox.showinfo("Éxito", "Colaborador creado correctamente.")
        self._close_fullscreen_view()

    def view_list_collab(self):
        frame = self._open_fullscreen_view()
        ctk.CTkLabel(frame, text="(Aquí irá la lista de colaboradores)",
                     font=("Open Sans", 22, "bold")).pack(pady=80)
        ctk.CTkButton(frame, text="Volver",
                      command=self._close_fullscreen_view).pack(pady=20)

    def logout(self):
        confirm = mbox.askyesno("Cerrar sesión", "¿Deseas cerrar tu sesión actual?")
        if confirm:
            from login import LoginUI
            self.pack_forget()
            LoginUI(self.master)