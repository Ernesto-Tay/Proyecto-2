import customtkinter as ctk
import tkinter.messagebox as mbox
from main import Collaborator, Client


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
        self.fullscreen_frame = ctk.CTkFrame(self, fg_color="#fafafa")
        self.fullscreen_frame.pack(expand=True, fill="both")
        self.fullscreen_frame.lift()  # se sobrepone el frame sobre todos los demás
        self.update_idletasks()  # refresca el diseño (lo dibuja)
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

    def toggle_submenu(self, name, parent_button):
        # Cierra cualquier submenú abierto
        if self.active_submenu:
            try:
                self.active_submenu.destroy()
            except:
                pass
            self.active_submenu = None

            if self.last_opened == name:
                self.last_opened = None
                return

        submenu = ctk.CTkToplevel(self) # Se crea el submenú como ventana flotante (independiente)
        submenu.overrideredirect(True)
        submenu.configure(fg_color="#f8f8f8")
        submenu.attributes("-topmost", True)  # se mantiene al frente

        ax = parent_button.winfo_rootx()
        ay = parent_button.winfo_rooty() + parent_button.winfo_height()
        submenu.geometry(f"+{ax}+{ay}")  # coloca el menú justo debajo del botón

        frame = ctk.CTkFrame(submenu, fg_color="#ffffff", corner_radius=12, border_width=1, border_color="#d0d0d0")
        frame.pack(padx=4, pady=4)

        if name == "colab":
            self.add_submenu_button(frame, "Agregar colaborador", lambda: self.action("Agregar colaborador"))
            self.add_submenu_button(frame, "Ver colaboradores", lambda: self.action("Ver colaboradores"))
        elif name == "provider":
            self.add_submenu_button(frame, "Agregar proveedor", lambda: self.action("Agregar proveedor"))
            self.add_submenu_button(frame, "Ver proveedores", lambda: self.action("Ver proveedores"))
        elif name == "sales":
            self.add_submenu_button(frame, "Agregar ventas", lambda: self.action("Agregar ventas"))
            self.add_submenu_button(frame, "Ver ventas", lambda: self.action("Ver ventas"))
        elif name == "products":
            self.add_submenu_button(frame, "Agregar productos", lambda: self.action("Agregar productos"))
            self.add_submenu_button(frame, "Ver productos", lambda: self.action("Ver productos"))
        elif name == "clients":
            self.add_submenu_button(frame, "Agregar cliente", lambda: self.action("Agregar cliente"))
            self.add_submenu_button(frame, "Ver clientes", lambda: self.action("Ver clientes"))

        self.active_submenu = submenu
        self.last_opened = name

        submenu.bind("<FocusOut>", lambda e: submenu.destroy())
        submenu.focus_force()

    def add_submenu_button(self, parent, text, command):
        btn = ctk.CTkButton(parent, text=text, width=180, height=30,fg_color="#ffffff", hover_color="#e6e6e6",text_color="black", font=("Open Sans", 12),command=command)
        btn.pack(padx=8, pady=4)

    def action(self, msg):
        # Cierra el submenú si está abierto
        if self.active_submenu:
            self.active_submenu.destroy()
            self.active_submenu = None

        if msg == "Agregar colaborador":
            self.view_create_collab()

        elif msg == "Agregar cliente":
            self.view_create_client()

        elif msg == "Agregar productos":
            self.view_create_product()

    # formulario agregar colaborador
    def view_create_collab(self):
        frame = self._open_fullscreen_view()

        title = ctk.CTkLabel(frame, text="Crear colaborador",font=("Open Sans", 50, "bold"), text_color="#111111")
        title.pack(pady=(60, 40))

        #fila de nombre (posición tipo matriz) donde nombre, aún no funcional
        row_nombre = ctk.CTkFrame(frame, fg_color="#e0e0e0", corner_radius=20)
        row_nombre.pack(pady=10, ipadx=10, ipady=6)
        row_nombre.grid_columnconfigure(0, minsize=160)
        row_nombre.grid_columnconfigure(1, minsize=320)
        ctk.CTkLabel(row_nombre, text="Nombre", font=("Open Sans", 18)).grid(row=0, column=0, padx=(14, 8), pady=8, sticky="nsew")
        self.ent_nombre = ctk.CTkEntry(row_nombre, width=300, height=36,corner_radius=14, fg_color="white",text_color="black", border_color="#cfcfcf")
        self.ent_nombre.grid(row=0, column=1, padx=(8, 14), pady=8, sticky="w")

        # telefono
        row_tel = ctk.CTkFrame(frame, fg_color="#e0e0e0", corner_radius=20)
        row_tel.pack(pady=10, ipadx=10, ipady=6)
        row_tel.grid_columnconfigure(0, minsize=160)
        row_tel.grid_columnconfigure(1, minsize=320)
        ctk.CTkLabel(row_tel, text="Teléfono", font=("Open Sans", 18)).grid(row=0, column=0, padx=(14, 8), pady=8, sticky="nsew")
        self.ent_tel = ctk.CTkEntry(row_tel, width=300, height=36, corner_radius=14, fg_color="white",text_color="black", border_color="#cfcfcf")
        self.ent_tel.grid(row=0, column=1, padx=(8, 14), pady=8, sticky="w")

        # posición
        row_pos = ctk.CTkFrame(frame, fg_color="#e0e0e0", corner_radius=20)
        row_pos.pack(pady=10, ipadx=10, ipady=6)
        row_pos.grid_columnconfigure(0, minsize=160)
        row_pos.grid_columnconfigure(1, minsize=320)
        ctk.CTkLabel(row_pos, text="Posición", font=("Open Sans", 18)).grid(row=0, column=0, padx=(14, 8), pady=8, sticky="nsew")
        self.ent_pos = ctk.CTkEntry(row_pos, width=300, height=36, corner_radius=14, fg_color="white",text_color="black", border_color="#cfcfcf")
        self.ent_pos.grid(row=0, column=1, padx=(8, 14), pady=8, sticky="w")

        # frame de botones
        btns = ctk.CTkFrame(frame, fg_color="transparent", corner_radius=20)
        btns.pack(pady=25)

        # botón "Crear colaborador"
        btn_crcolla = ctk.CTkButton(btns,text="Crear colaborador",width=240,height=45,corner_radius=22,fg_color="#e0e0e0",hover_color="#9e9e9e", text_color="black",font=("Open Sans", 15, "bold", "underline"),command=self.create_collaborator)
        btn_crcolla.pack(pady=(0, 12))

        # botón "Volver"
        btn_back = ctk.CTkButton(btns,text="Volver",width=240,height=45,corner_radius=22,fg_color="#e0e0e0",hover_color="#9e9e9e",text_color="black",font=("Open Sans", 15, "bold", "underline"),command=self._close_fullscreen_view)
        btn_back.pack()

    # lógica para crear colaborador
    def create_collaborator(self):
        name = self.ent_nombre.get().strip()
        phone = self.ent_tel.get().strip()
        position = self.ent_pos.get().strip()

        if not name or not phone or not position:
            mbox.showerror("Campos vacíos", "Se deben llenar todos los campos.")
            return

        try:
            collab = Collaborator(name=name, phone=phone, position=position) # crea al objeto
            collab.save() # metodo importado para guardar
            mbox.showinfo(f"Colaborador creado", f"Colaborador {name} creado y guardado")
            self._close_fullscreen_view()
        except Exception as e:
            mbox.showerror("Error", f"Error inesperado: {e}")

    # formulario agregar cliente
    def view_create_client(self):
        frame = self._open_fullscreen_view()

        title = ctk.CTkLabel(frame,text="Crear cliente",font=("Open Sans", 50, "bold"),text_color="#111111")
        title.pack(pady=(60, 40))

        row_name = ctk.CTkFrame(frame, fg_color="#e0e0e0", corner_radius=20)
        row_name.pack(pady=10, ipadx=10, ipady=6)
        row_name.grid_columnconfigure(0, minsize=160)
        row_name.grid_columnconfigure(1, minsize=320)
        ctk.CTkLabel(row_name, text="Nombre", font=("Open Sans", 18)).grid(row=0, column=0, padx=(14, 8), pady=8,sticky="nsew")
        self.ent_nombre = ctk.CTkEntry(row_name, width=300, height=36, corner_radius=14, fg_color="white", text_color="black", border_color="#cfcfcf")
        self.ent_nombre.grid(row=0, column=1, padx=(8, 14), pady=8, sticky="w")

        # telefono, aún no funcional
        row_tel = ctk.CTkFrame(frame, fg_color="#e0e0e0", corner_radius=20)
        row_tel.pack(pady=10, ipadx=10, ipady=6)
        row_tel.grid_columnconfigure(0, minsize=160)
        row_tel.grid_columnconfigure(1, minsize=320)
        ctk.CTkLabel(row_tel, text="Teléfono", font=("Open Sans", 18)).grid(row=0, column=0, padx=(14, 8), pady=8,sticky="nsew")
        self.ent_tel = ctk.CTkEntry(row_tel, width=300, height=36, corner_radius=14, fg_color="white",text_color="black", border_color="#cfcfcf")
        self.ent_tel.grid(row=0, column=1, padx=(8, 14), pady=8, sticky="w")

        # frame de botones
        btns = ctk.CTkFrame(frame, fg_color="transparent", corner_radius=20)
        btns.pack(pady=25)

        # Botón "Crear cliente"
        btn_crclient = ctk.CTkButton(btns,text="Crear cliente",width=240,height=45,corner_radius=22,fg_color="#e0e0e0",hover_color="#9e9e9e",text_color="black",font=("Open Sans", 15, "bold", "underline"),command=self.create_client)
        btn_crclient.pack(pady=(0, 12))

        # Botón "Volver"
        btn_back = ctk.CTkButton(btns,text="Volver",width=240,height=45,corner_radius=22,fg_color="#e0e0e0",hover_color="#9e9e9e",text_color="black",font=("Open Sans", 15, "bold", "underline"),command=self._close_fullscreen_view)
        btn_back.pack()

    # lógica para crear colaborador
    def create_client(self):
        name = self.ent_nombre.get().strip()
        phone = self.ent_tel.get().strip()

        if not name or not phone:
            mbox.showerror("Campos vacíos", "Se deben llenar todos los campos.")
            return

        try:
            client = Client(name=name, phone=phone) # crea al objeto
            client.save() # metodo importado para guardar
            mbox.showinfo(f"Colaborador creado", f"Cliente {name} creado y guardado")
            self._close_fullscreen_view() # cierra la ventana cuando se crea
        except Exception as e:
            mbox.showerror("Error", f"Error inesperado: {e}")

    # formulario agregar producto
    def view_create_product(self):
        frame = self._open_fullscreen_view()

        title = ctk.CTkLabel(frame, text="Crear producto", font=("Open Sans", 50, "bold"), text_color="#111111")
        title.pack(pady=(60, 40))

        container = ctk.CTkFrame(frame, fg_color="transparent")
        container.pack(pady=10)

        row1 = ctk.CTkFrame(container, fg_color="transparent")
        row1.pack(pady=6)
        # nombre
        row_nombre = ctk.CTkFrame(row1, fg_color="#e0e0e0", corner_radius=20)
        row_nombre.pack(side= "left",padx= 20,pady=10, ipadx=10, ipady=6)
        row_nombre.grid_columnconfigure(0, minsize=130)
        row_nombre.grid_columnconfigure(1, minsize=250)
        ctk.CTkLabel(row_nombre, text="Nombre", font=("Open Sans", 18)).grid(row=0, column=0, padx=(14, 8), pady=8, sticky="nsew")
        self.ent_nombre = ctk.CTkEntry(row_nombre, width=300, height=36,corner_radius=14, fg_color="white",text_color="black", border_color="#cfcfcf")
        self.ent_nombre.grid(row=0, column=1, padx=(8, 14), pady=8, sticky="w")

        # Tipo
        row_tipo = ctk.CTkFrame(row1, fg_color="#e0e0e0", corner_radius=20)
        row_tipo.pack(side= "right",padx= 20,pady=10, ipadx=10, ipady=6)
        row_tipo.grid_columnconfigure(0, minsize=130)
        row_tipo.grid_columnconfigure(1, minsize=250)
        ctk.CTkLabel(row_tipo, text="Tipo", font=("Open Sans", 18)).grid(row=0, column=0, padx=(14, 8), pady=8, sticky="nsew")
        self.ent_tipo = ctk.CTkEntry(row_tipo, width=300, height=36,corner_radius=14, fg_color="white",text_color="black", border_color="#cfcfcf")
        self.ent_tipo.grid(row=0, column=1, padx=(8, 14), pady=8, sticky="w")

        row2 = ctk.CTkFrame(container, fg_color="transparent")
        row2.pack(pady=6)
        # Descripción
        row_desc = ctk.CTkFrame(row2, fg_color="#e0e0e0", corner_radius=20)
        row_desc.pack(side= "left",padx= 20,pady=10, ipadx=10, ipady=6)
        row_desc.grid_columnconfigure(0, minsize=130)
        row_desc.grid_columnconfigure(1, minsize=250)
        ctk.CTkLabel(row_desc, text="Descripción", font=("Open Sans", 18)).grid(row=0, column=0, padx=(14, 8), pady=8, sticky="nsew")
        self.ent_desc = ctk.CTkEntry(row_desc, width=300, height=36,corner_radius=14, fg_color="white",text_color="black", border_color="#cfcfcf")
        self.ent_desc.grid(row=0, column=1, padx=(8, 14), pady=8, sticky="w")

        # Stock
        row_stock = ctk.CTkFrame(row2, fg_color="#e0e0e0", corner_radius=20)
        row_stock.pack(side= "right",padx= 20,pady=10, ipadx=10, ipady=6)
        row_stock.grid_columnconfigure(0, minsize=130)
        row_stock.grid_columnconfigure(1, minsize=250)
        ctk.CTkLabel(row_stock, text="Stock", font=("Open Sans", 18)).grid(row=0, column=0, padx=(14, 8), pady=8, sticky="nsew")
        self.ent_stock = ctk.CTkEntry(row_stock, width=300, height=36,corner_radius=14, fg_color="white",text_color="black", border_color="#cfcfcf")
        self.ent_stock.grid(row=0, column=1, padx=(8, 14), pady=8, sticky="w")

        row3 = ctk.CTkFrame(container, fg_color="transparent")
        row3.pack(pady=6)
        # Precio costo
        row_costo = ctk.CTkFrame(row3, fg_color="#e0e0e0", corner_radius=20)
        row_costo.pack(side= "left",padx= 20,pady=10, ipadx=10, ipady=6)
        row_costo.grid_columnconfigure(0, minsize=130)
        row_costo.grid_columnconfigure(1, minsize=250)
        ctk.CTkLabel(row_costo, text="Precio costo", font=("Open Sans", 18)).grid( row=0, column=0, padx=(14, 8), pady=8, sticky="nsew")
        self.ent_costo = ctk.CTkEntry(row_costo, width=300, height=36,corner_radius=14, fg_color="white",text_color="black", border_color="#cfcfcf")
        self.ent_costo.grid(row=0, column=1, padx=(8, 14), pady=8, sticky="w")

        # Precio venta
        row_venta = ctk.CTkFrame(row3, fg_color="#e0e0e0", corner_radius=20)
        row_venta.pack(side= "right",padx= 20,pady=10, ipadx=10, ipady=6)
        row_venta.grid_columnconfigure(0, minsize=130)
        row_venta.grid_columnconfigure(1, minsize=250)
        ctk.CTkLabel(row_venta, text="Precio venta", font=("Open Sans", 18)).grid(row=0, column=0, padx=(14, 8), pady=8, sticky="nsew")
        self.ent_venta = ctk.CTkEntry(row_venta, width=300, height=36,corner_radius=14, fg_color="white",text_color="black", border_color="#cfcfcf")
        self.ent_venta.grid(row=0, column=1, padx=(8, 14), pady=8, sticky="w")

        # frame de botones
        btns = ctk.CTkFrame(frame, fg_color="transparent", corner_radius=20)
        btns.pack(pady=25)

        # Botón "Crear producto"
        btn_crclient = ctk.CTkButton(btns, text="Crear producto", width=240, height=45, corner_radius=22,fg_color="#e0e0e0", hover_color="#9e9e9e", text_color="black",font=("Open Sans", 15, "bold", "underline"))
        btn_crclient.pack(pady=(0, 12))

        # Botón "Volver"
        btn_back = ctk.CTkButton(btns, text="Volver", width=240, height=45, corner_radius=22, fg_color="#e0e0e0",hover_color="#9e9e9e", text_color="black", font=("Open Sans", 15, "bold", "underline"),command=self._close_fullscreen_view)
        btn_back.pack()

    def logout(self):
        confirm = mbox.askyesno("Cerrar sesión", "¿Deseas cerrar tu sesión actual?")
        if confirm:
            from login import LoginUI
            self.pack_forget()
            LoginUI(self.master)