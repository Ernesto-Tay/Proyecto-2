import customtkinter as ctk
import tkinter.messagebox as mbox
from main import User, Admin, Collaborator, Provider, Client , Product, Sales, get_conn
import tkinter as tk
from tkinter import ttk
import calendar
import json
from datetime import datetime

DB_NAME = "bawiz.db"
classes = {"users": User, "admins": Admin, "collaborators": Collaborator, "providers": Provider, "clients": Client, "sales": Sales, "products": Product}

class AdminUI(ctk.CTkFrame):
    def __init__(self, master, current_user=None):
        super().__init__(master, fg_color="white")
        self.master = master
        self.pack(expand=True, fill="both")
        #Datos del usuario actual (para validaciones futuras)
        self.curr_id = None
        # elementos principales
        self.header = None
        self.body = None
        self.fullscreen_frame = None  # frame para vistas completas
        # submenús
        self.active_submenu = None
        self.last_opened = None  # guarda cuál botón se abrió
        self.searchbar_frame = None
        # inicialización
        self.create_header()
        self.db_info = self.db_extract(classes)
        self.body = ctk.CTkFrame(self, fg_color="white")
        self.body.pack(expand=True, fill="both")
        self.current_sale = None

        # Mensaje de bienvenida
        self.current_user = current_user
        if self.current_user:
            name = self.current_user.get("name", "Usuario")
            phone = self.current_user.get("phone", "Sin teléfono")
            self.curr_id = self.current_user.get("id", None)

        else:
            name = "Usuario"
            phone = "Sin teléfono"

        msg = f"Bienvenido, {name}"
        welcome_label = ctk.CTkLabel(self.body,text=msg,font=("Open Sans", 28, "bold"),text_color="#004857",justify="center")
        welcome_label.pack(expand=True)

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
        self.header = ctk.CTkFrame(self, fg_color="#004857", height=60, corner_radius=0)
        self.header.pack(side="top", fill="x")

        # frame izquierdo
        left = ctk.CTkFrame(self.header, fg_color="transparent")
        left.pack(side="left", padx=15, pady=10)

        # botones principales
        btn_colab = ctk.CTkButton(left, text="Colaboradores", width=130, height=36,corner_radius=18, fg_color="#f4f1ec", hover_color="#cd5618",text_color="black", font=("Open Sans", 13, "bold"),command=lambda: self.toggle_submenu("colab", btn_colab))
        btn_colab.pack(side="left", padx=6)

        btn_provider = ctk.CTkButton(left, text="Proveedores", width=130, height=36,corner_radius=18, fg_color="#f4f1ec", hover_color="#cd5618",text_color="black", font=("Open Sans", 13, "bold"),command=lambda: self.toggle_submenu("provider", btn_provider))
        btn_provider.pack(side="left", padx=6)

        btn_sales = ctk.CTkButton(left, text="Ventas", width=130, height=36,corner_radius=18, fg_color="#f4f1ec", hover_color="#cd5618",text_color="black", font=("Open Sans", 13, "bold"),command=lambda: self.toggle_submenu("sales", btn_sales))
        btn_sales.pack(side="left", padx=6)

        btn_products = ctk.CTkButton(left, text="Productos", width=130, height=36,corner_radius=18, fg_color="#f4f1ec", hover_color="#cd5618",text_color="black", font=("Open Sans", 13, "bold"),command=lambda: self.toggle_submenu("products", btn_products))
        btn_products.pack(side="left", padx=6)

        btn_clients = ctk.CTkButton(left, text="Clientes", width=130, height=36,corner_radius=18, fg_color="#f4f1ec", hover_color="#cd5618",text_color="black", font=("Open Sans", 13, "bold"),command=lambda: self.toggle_submenu("clients", btn_clients))
        btn_clients.pack(side="left", padx=6)

        # frame derecho
        right = ctk.CTkFrame(self.header, fg_color="transparent")
        right.pack(side="right", padx=15, pady=10)

        btn_logout = ctk.CTkButton(right, text="Cerrar Sesión", width=130, height=36,corner_radius=18, fg_color="#f86a20", hover_color="#da6a2a",text_color="white", font=("Open Sans", 13, "bold"),command=self.logout)
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
        submenu.configure(fg_color="#004857")
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
        btn = ctk.CTkButton(parent, text=text, width=180, height=30,fg_color="#ffffff", hover_color="#f86a20",text_color="black", font=("Open Sans", 12),command=command)
        btn.pack(padx=8, pady=4)

    def action(self, msg):
        # Cierra el submenú si está abierto
        if self.active_submenu:
            self.active_submenu.destroy()
            self.active_submenu = None

        match msg:
            case "Agregar colaborador":
                self.close_searchbar()
                self.view_create_collab()
            case "Agregar cliente":
                self.close_searchbar()
                self.view_create_client()
            case "Agregar productos":
                self.close_searchbar()
                self.view_create_product()
            case "Agregar proveedor":
                self.close_searchbar()
                self.view_create_provider()
            case "Agregar ventas":
                self.close_searchbar()
                self.view_create_sale()
            case "Ver colaboradores":
                self.menu_visualizer(self.master, "collaborators")
            case "Ver clientes":
                self.menu_visualizer(self.master, "clients")
            case "Ver productos":
                self.menu_visualizer(self.master, "products")
            case "Ver proveedores":
                self.menu_visualizer(self.master, "providers")
            case "Ver ventas":
                self.menu_visualizer(self.master, "sales")

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
        ctk.CTkLabel(row_nombre, text="Nombre", font=("Open Sans", 18, "bold")).grid(row=0, column=0, padx=(14, 8), pady=8, sticky="nsew")
        self.ent_nombre = ctk.CTkEntry(row_nombre, width=300, height=36,corner_radius=14, fg_color="white",text_color="black", border_color="#cfcfcf")
        self.ent_nombre.grid(row=0, column=1, padx=(8, 14), pady=8, sticky="w")

        # telefono
        row_tel = ctk.CTkFrame(frame, fg_color="#e0e0e0", corner_radius=20)
        row_tel.pack(pady=10, ipadx=10, ipady=6)
        row_tel.grid_columnconfigure(0, minsize=160)
        row_tel.grid_columnconfigure(1, minsize=320)
        ctk.CTkLabel(row_tel, text="Teléfono", font=("Open Sans", 18, "bold")).grid(row=0, column=0, padx=(14, 8), pady=8, sticky="nsew")
        self.ent_tel = ctk.CTkEntry(row_tel, width=300, height=36, corner_radius=14, fg_color="white",text_color="black", border_color="#cfcfcf")
        self.ent_tel.grid(row=0, column=1, padx=(8, 14), pady=8, sticky="w")

        # posición
        row_pos = ctk.CTkFrame(frame, fg_color="#e0e0e0", corner_radius=20)
        row_pos.pack(pady=10, ipadx=10, ipady=6)
        row_pos.grid_columnconfigure(0, minsize=160)
        row_pos.grid_columnconfigure(1, minsize=320)
        ctk.CTkLabel(row_pos, text="Posición", font=("Open Sans", 18, "bold")).grid(row=0, column=0, padx=(14, 8), pady=8, sticky="nsew")
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
        elif len(phone) != 8:
            mbox.showerror("Teléfono inválido", "El número telefónico debe tener 8 dígitos numéricos")
            return

        try:
            usr = User(name = name, phone = phone)
            usr.save()
            collab = Collaborator(name=name, phone=phone, position=position, user_id = usr.user_id) # crea al objeto
            collab.save() # metodo importado para guardar
            mbox.showinfo(f"Colaborador creado", f"Colaborador '{name}' creado y guardado")
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

        # telefono
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

    # lógica para crear cliente
    def create_client(self):
        name = self.ent_nombre.get().strip()
        phone = self.ent_tel.get().strip()

        if not name or not phone:
            mbox.showerror("Campos vacíos", "Se deben llenar todos los campos.")
            return
        elif len(phone) != 8:
            mbox.showerror("Teléfono inválido", "El número telefónico debe tener 8 dígitos numéricos")
            return

        try:
            usr = User(name,phone)
            usr.save()
            client = Client(name=name, phone=phone, user_id = usr.user_id) # crea al objeto
            client.save() # metodo importado para guardar
            mbox.showinfo(f"Cliente creado", f"Cliente '{name}' creado y guardado")
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
        btn_crclient = ctk.CTkButton(btns, text="Crear producto", width=240, height=45, corner_radius=22,fg_color="#e0e0e0", hover_color="#9e9e9e", text_color="black",font=("Open Sans", 15, "bold", "underline"),command=self.create_product)
        btn_crclient.pack(pady=(0, 12))

        # Botón "Volver"
        btn_back = ctk.CTkButton(btns, text="Volver", width=240, height=45, corner_radius=22, fg_color="#e0e0e0",hover_color="#9e9e9e", text_color="black", font=("Open Sans", 15, "bold", "underline"),command=self._close_fullscreen_view)
        btn_back.pack()

    def create_product(self):
        name = self.ent_nombre.get().strip()
        type_ = self.ent_tipo.get().strip()
        desc = self.ent_desc.get().strip()
        stock = self.ent_stock.get().strip()
        raw_price = self.ent_costo.get().strip()
        sale_price = self.ent_venta.get().strip()

        if not all([name, type_, desc, stock, raw_price, sale_price]):
            mbox.showerror("Campos Vacíos", "No puede dejar campos vacíos")
            return

        try:
            stock = int(stock)
            raw_price = float(raw_price)
            sale_price = float(sale_price)
        except ValueError:
            mbox.showerror("Error numérico", "Debe ingresar valores válidos para precios y stock.")
            return

        if stock <= 0:
            mbox.showerror("Error de stock", "El stock no puede ser negativo.")
            return

        if raw_price <= 0 or sale_price <= 0:
            mbox.showerror("Error de precios", "Los precios deben ser mayores que cero.")
            return

        if sale_price <= raw_price:
            mbox.showerror("Error de precios", "El precio de venta debe ser mayor que el precio costo.")
            return

        try:
            product = Product(name=name,types=type_,desc=desc,raw_p=raw_price,sale_p=sale_price,stock=stock)
            product.save()
            mbox.showinfo(f"Producto", f"Producto '{name}' creado")
            self._close_fullscreen_view()
        except Exception as e:
            mbox.showerror("Error", f"Error inesperado: {e}")

    # formulario para agregar proveedor
    def view_create_provider(self):
        container = self._open_fullscreen_view()
        frame = ctk.CTkScrollableFrame(container, fg_color="#fafafa")
        frame.pack(expand=True, fill="both")
        title = ctk.CTkLabel(frame,text="Crear proveedor",font=("Open Sans", 50, "bold"),text_color="#111111")
        title.pack(pady=(40, 20))

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

        # busqueda de productos
        ctk.CTkLabel(frame, text="Buscar productos:",font=("Open Sans", 18, "bold")).pack(anchor="w", padx=20, pady=(10, 0))

        self.ent_search = ctk.CTkEntry(frame, width=400, height=36,corner_radius=14, fg_color="white", text_color="black", border_color="#cfcfcf")
        self.ent_search.pack(padx=20, pady=(4, 10), anchor="w")
        self.ent_search.bind("<KeyRelease>", self.update_product_checklist)

        self.products_frame = ctk.CTkScrollableFrame(frame, fg_color="white", height=100)
        self.products_frame.pack(fill="x", padx=20, pady=5)

        self.product_checks = {}
        self.update_product_checklist()

        # botones
        btns = ctk.CTkFrame(frame, fg_color="transparent", corner_radius=20)
        btns.pack(pady=25)

        btn_create = ctk.CTkButton(btns, text="Crear proveedor", width=200, height=40,corner_radius=22, fg_color="#e0e0e0",hover_color="#9e9e9e", text_color="black",font=("Open Sans", 15, "bold", "underline"),command=self.create_provider)
        btn_create.pack(pady=(0, 12))

        btn_back = ctk.CTkButton(btns, text="Volver", width=200, height=40,corner_radius=22, fg_color="#e0e0e0",hover_color="#9e9e9e", text_color="black",font=("Open Sans", 15, "bold", "underline"),command=self._close_fullscreen_view)
        btn_back.pack()

    def update_product_checklist(self, *_): # reconstruye dinámicamente la lista de productos
        search_term = self.ent_search.get().lower().strip()
        for widget in self.products_frame.winfo_children(): # limpia frame antes de reconstruir
            widget.destroy()

        self.product_checks = {}

        with get_conn() as c: # consulta de productos desde la base de datos
            rows = c.execute("SELECT product_id, name, type, description FROM products").fetchall()

        for row in rows: # por cada producto, extrae sus datos para poder mostrarlos
            pid = row["product_id"]
            name = row["name"]
            type_ = row["type"]
            desc = row["description"]
            text = f"{name}  |  {type_}  |  {desc}"
            if not search_term or (search_term in name.lower()) or (search_term in type_.lower()) or (search_term in desc.lower()):
                var = tk.IntVar(value=0)  # guarda el estado del checkbox (1 si está marcado, 0 si no).
                chk = ctk.CTkCheckBox(self.products_frame,text=text,text_color="black",font=("Open Sans", 14),variable=var,onvalue=1,offvalue=0)
                chk.var = var
                chk.pack(anchor="w", padx=10, pady=4)

                self.product_checks[pid] = chk  #  se guarda una referencia en el diccionario self.product_checks, usando el product_id como clave.

    def create_provider(self):
        name = self.ent_nombre.get().strip()  #guarda el proveedor con los productos seleccionados
        phone = self.ent_tel.get().strip()
        selected_products = []
        for pid, chk in self.product_checks.items(): # recorre cada producto, donde mira si el checkbox está marcado (chk.var.get() == 1), lo añade a selected_products.
            if chk.var.get() == 1:  # obtiene el valor real
                selected_products.append(str(pid))

        if not name or not phone:
            mbox.showerror("Campos vacíos", "Debe llenar todos los campos.")
            return
        elif len(phone) != 8:
            mbox.showerror("Teléfono inválido", "El número telefónico debe tener 8 dígitos numéricos")
            return
        if not selected_products:
            mbox.showwarning("Sin productos", "Debe seleccionar al menos un producto.")
            return


        try:
            usr = User(name=name, phone=phone)
            usr.save()
            provider = Provider(products=selected_products, user_id=usr.user_id, name=name, phone=phone)
            provider.save()
            mbox.showinfo("Proveedor creado", f"Proveedor '{name}' guardado correctamente.")
            self._close_fullscreen_view()
        except Exception as e:
            mbox.showerror("Error", f"No se pudo crear el proveedor:\n{e}")

    def manage_sale(self, action=None, product_id=None, quantity=0, unit_price=0.0):
        """
        Función centralizada para manejar la lógica base del diccionario que guarda las ventas.
        Permite inicializar el carrito, agregar productos, eliminarlos,
        calcular el total y visualizar el estado actual.
        """

        if action == "init":  # Inicializa el diccionario
            self.current_sale = {
                "client": None,  # Guarda al cliente seleccionado (su ID)
                "products": {}  # {product_id: {"quantity": int, "subtotal": float}}
            }
            return

        if action == "add":
            if not hasattr(self, "current_sale"): # Si no existe el diccionario, lo inicializa automáticamente
                self.manage_sale("init")

            if product_id in self.current_sale["products"]: # Acá, si el producto ya existe, suma cantidades y recalcula subtotal
                self.current_sale["products"][product_id]["quantity"] += quantity
                self.current_sale["products"][product_id]["subtotal"] = round(
                    self.current_sale["products"][product_id]["quantity"] * unit_price, 2
                )
            else: # Si es un producto nuevo, se añade al diccionario
                self.current_sale["products"][product_id] = {
                    "quantity": quantity,
                    "subtotal": round(quantity * unit_price, 2)
                }
            return

        if action == "remove":
            if hasattr(self, "current_sale") and product_id in self.current_sale["products"]:
                del self.current_sale["products"][product_id]
            return

        if action == "total":
            if not hasattr(self, "current_sale"):
                return 0
            total = round(sum(item["subtotal"] for item in self.current_sale["products"].values()), 2)
            return total

        if action == "print": # Muestra lo que contiene el diccionario
            if not hasattr(self, "current_sale"):
                return
            # venta en el momento
            print(json.dumps(self.current_sale, indent=4, ensure_ascii=False))
            return

    def save_sale_to_db(self):
        """
        Guarda la venta actual (diccionario) en la base de datos y actualiza existencias.
        Verifica que haya stock suficiente antes de registrar la venta.
        """

        # Verifica que exista una venta activa
        if not hasattr(self, "current_sale") or not self.current_sale.get("products"):
            mbox.showerror("Venta vacía", "No hay productos agregados a la venta.")
            return

        if not self.current_sale.get("client"):
            mbox.showerror("Cliente no seleccionado", "Debe seleccionar un cliente antes de guardar la venta.")
            return

        # Conexión a la base de datos
        with get_conn() as conn:
            # Valida el stock disponible antes de confirmar la venta
            for product_id, data in self.current_sale["products"].items():
                prod = conn.execute("SELECT name, stock FROM products WHERE product_id = ?", (product_id,)).fetchone()
                if not prod:
                    mbox.showerror("Error", f"Producto con ID {product_id} no encontrado en la base de datos.")
                    return
                if prod["stock"] < data["quantity"]:
                    mbox.showerror("Stock insuficiente", f"No hay suficiente stock para '{prod['name']}'.\n Disponible: {prod['stock']} unidades.")
                    return

            # Si está correcto, calcula el total
            total = round(sum(item["subtotal"] for item in self.current_sale["products"].values()), 2)

            # Crea ID único para la venta
            sale_id = "SAL" + datetime.now().strftime("%d%m%H%M%S")

            # Fecha y hora actuales
            now = datetime.now()
            date_str = now.strftime("%d/%m/%Y")
            time_str = now.strftime("%H:%M:%S")

            # Guardar la venta
            conn.execute(
                """INSERT INTO sales (sale_id, client_id, date, time, products, total)
                   VALUES (?, ?, ?, ?, ?, ?)""",
                (sale_id,self.current_sale["client"],date_str,time_str,json.dumps(self.current_sale["products"], ensure_ascii=False),total))

            # Actualiza el stock de cada producto vendido
            for product_id, data in self.current_sale["products"].items():
                conn.execute("UPDATE products SET stock = stock - ? WHERE product_id = ?",(data["quantity"], product_id))
            conn.commit()

        # Reinicia la lista de productos después de guardar
        self.manage_sale("init")
        self.refresh_cart_view()
        mbox.showinfo("Venta registrada", f"La venta {sale_id} fue guardada correctamente.")

    def view_create_sale(self):
        container = self._open_fullscreen_view()
        frame = ctk.CTkScrollableFrame(container, fg_color="#fafafa")
        frame.pack(expand=True, fill="both")

        title = ctk.CTkLabel(frame, text="Registrar Venta", font=("Open Sans", 42, "bold"), text_color="#111111")
        title.pack(pady=(30, 20))

        # Inicializa el diccionario
        self.manage_sale("init")

        # cliente
        ctk.CTkLabel(frame, text="Buscar cliente:", font=("Open Sans", 18, "bold")).pack(anchor="w", padx=20, pady=(10, 0))
        self.ent_client_search = ctk.CTkEntry(frame, width=350, height=34, corner_radius=14,fg_color="white", text_color="black", border_color="#cfcfcf")
        self.ent_client_search.pack(padx=20, pady=(4, 10), anchor="w")
        self.ent_client_search.bind("<KeyRelease>", self.update_client_search)

        self.client_frame = ctk.CTkScrollableFrame(frame, fg_color="white", height=80)
        self.client_frame.pack(fill="x", padx=20, pady=5)

        self.selected_client = None

        # productos
        ctk.CTkLabel(frame, text="Buscar productos:", font=("Open Sans", 18, "bold")).pack(anchor="w", padx=20, pady=(15, 0))
        self.ent_prod_search = ctk.CTkEntry(frame, width=350, height=34, corner_radius=14,fg_color="white", text_color="black", border_color="#cfcfcf")
        self.ent_prod_search.pack(padx=20, pady=(4, 10), anchor="w")
        self.ent_prod_search.bind("<KeyRelease>", self.update_product_search)

        self.products_frame = ctk.CTkScrollableFrame(frame, fg_color="white", height=220)
        self.products_frame.pack(fill="x", padx=20, pady=5)

        # lista de productos
        ctk.CTkLabel(frame, text="Productos:", font=("Open Sans", 18, "bold")).pack(anchor="w", padx=20, pady=(20, 0))
        self.cart_frame = ctk.CTkScrollableFrame(frame, fg_color="white", height=200)
        self.cart_frame.pack(fill="x", padx=20, pady=5)

        # etiqueta de total
        self.lbl_total = ctk.CTkLabel(frame, text="Total: Q0.00", font=("Open Sans", 20, "bold"), text_color="#333333")
        self.lbl_total.pack(anchor="e", padx=30, pady=(10, 5))

        # botones
        btns = ctk.CTkFrame(frame, fg_color="transparent", corner_radius=20)
        btns.pack(pady=25)

        btn_save = ctk.CTkButton(btns, text="Guardar venta", width=200, height=40, corner_radius=20,fg_color="#e0e0e0", hover_color="#9e9e9e",text_color="black", font=("Open Sans", 15, "bold", "underline"),command=self.save_sale_to_db)
        btn_save.pack(pady=(0, 12))

        btn_back = ctk.CTkButton(btns, text="Volver", width=200, height=40, corner_radius=20,fg_color="#e0e0e0", hover_color="#9e9e9e",text_color="black", font=("Open Sans", 15, "bold", "underline"),command=self._close_fullscreen_view)
        btn_back.pack()

        # Inicia vista del carrito vacía
        self.refresh_cart_view()

    # Funciones para buscar
    def update_client_search(self, *_):
        """Filtra clientes mientras se escribe"""
        term = self.ent_client_search.get().lower().strip()
        for widget in self.client_frame.winfo_children():
            widget.destroy()

        with get_conn() as c:
            rows = c.execute("""
                SELECT c.client_id, u.name, u.phone
                FROM clients c
                JOIN users u ON c.user_id = u.user_id
            """).fetchall()

        for row in rows:
            if term in row["name"].lower():
                btn = ctk.CTkButton(self.client_frame,text=f"{row['name']}  |  {row['phone']}",fg_color="white", text_color="black", anchor="w", hover_color="#f2f2f2",command=lambda cid=row["client_id"], name=row["name"]: self.select_client(cid, name))
                btn.pack(fill="x", padx=10, pady=2)

    def select_client(self, client_id, name):
        """Guarda el cliente seleccionado"""
        self.selected_client = client_id
        self.current_sale["client"] = client_id
        mbox.showinfo("Cliente seleccionado", f"Cliente: {name}\nID: {client_id}")
        self.ent_client_search.delete(0, "end")
        self.ent_client_search.insert(0, name)

    def update_product_search(self, *_):
        """Muestra productos disponibles y permite agregarlos al carrito"""
        term = self.ent_prod_search.get().lower().strip()
        for widget in self.products_frame.winfo_children():
            widget.destroy()

        with get_conn() as c:
            rows = c.execute("SELECT product_id, name, sale_price, stock FROM products").fetchall()

        for row in rows:
            if term in row["name"].lower():
                prod_id = row["product_id"]
                name = row["name"]
                price = row["sale_price"]
                stock = row["stock"]

                frame = ctk.CTkFrame(self.products_frame, fg_color="#f8f8f8", corner_radius=8)
                frame.pack(fill="x", padx=10, pady=4)

                label = ctk.CTkLabel(frame, text=f"{name} (Q{price}) | Stock: {stock}", text_color="black",anchor="w", font=("Open Sans", 14))
                label.pack(side="left", padx=8)

                # Selector de cantidad
                qty_var = tk.IntVar(value=1)
                minus_btn = ctk.CTkButton(frame, text="-", width=30, height=30,command=lambda v=qty_var: v.set(max(1, v.get() - 1)))
                minus_btn.pack(side="right", padx=2)
                qty_entry = ctk.CTkEntry(frame, width=40, textvariable=qty_var, justify="center")
                qty_entry.pack(side="right", padx=2)
                plus_btn = ctk.CTkButton(frame, text="+", width=30, height=30,command=lambda v=qty_var: v.set(v.get() + 1))
                plus_btn.pack(side="right", padx=2)

                add_btn = ctk.CTkButton(frame, text="Agregar", width=100,command=lambda pid=prod_id, p=price, q=qty_var, n=name: self.add_product(pid, p, q, n))
                add_btn.pack(side="right", padx=8)

    def refresh_cart_view(self):
        """Actualiza la vista del carrito en la interfaz."""
        # Limpia el contenido previo
        for widget in self.cart_frame.winfo_children():
            widget.destroy()

        # Si no hay venta activa
        if not hasattr(self, "current_sale") or not self.current_sale["products"]:
            lbl = ctk.CTkLabel(self.cart_frame, text="No hay productos agregados.",text_color="gray", font=("Open Sans", 14, "italic"))
            lbl.pack(pady=10)
            self.lbl_total.configure(text="Total: Q0.00")
            return

        # Recorre los productos agregados
        for pid, info in self.current_sale["products"].items():
            row = ctk.CTkFrame(self.cart_frame, fg_color="#f4f4f4", corner_radius=10)
            row.pack(fill="x", padx=10, pady=4)

            # Nombre del producto
            with get_conn() as c:
                prod = c.execute("SELECT name FROM products WHERE product_id = ?", (pid,)).fetchone()
                prod_name = prod["name"] if prod else "Desconocido"

            ctk.CTkLabel(row, text=f"{prod_name}", anchor="w",font=("Open Sans", 14, "bold"), text_color="black").pack(side="left", padx=10)
            ctk.CTkLabel(row, text=f"Cantidad: {info['quantity']}", anchor="center",font=("Open Sans", 13), text_color="black").pack(side="left", padx=10)
            ctk.CTkLabel(row, text=f"Subtotal: Q{info['subtotal']:.2f}", anchor="center",font=("Open Sans", 13), text_color="black").pack(side="left", padx=10)

            # Botón eliminar producto
            del_btn = ctk.CTkButton(row, text="X", width=30, height=28, fg_color="#e57373",hover_color="#ef5350", text_color="white",command=lambda p=pid: self.remove_product_from_cart(p))
            del_btn.pack(side="right", padx=10)

        # Actualiza el total
        total = self.manage_sale("total")
        self.lbl_total.configure(text=f"Total: Q{total:.2f}")

    def remove_product_from_cart(self, product_id):
        """Elimina un producto del diccionario y refresca la vista."""
        self.manage_sale("remove", product_id)
        self.refresh_cart_view()

    def add_product(self, product_id, price, qty_var, name):
        """Agrega producto al diccionario y refresca vista"""
        cantidad = qty_var.get()
        subtotal = round(cantidad * price, 2)
        self.manage_sale("add", product_id, cantidad, price)
        self.refresh_cart_view()

    def view_edit_sale(self, sale_id):
        """formulario para editar una venta existente (edita al cliente, productos y cantidades)"""
        container = self._open_fullscreen_view()
        frame = ctk.CTkScrollableFrame(container, fg_color="#fafafa")
        frame.pack(expand=True, fill="both")

        title = ctk.CTkLabel(frame, text=f"Editar Venta {sale_id}", font=("Open Sans", 42, "bold"),
                             text_color="#111111")
        title.pack(pady=(30, 20))

        # obtiene los datos de la venta
        with get_conn() as c:
            sale = c.execute("SELECT * FROM sales WHERE sale_id = ?", (sale_id,)).fetchone()
            if not sale:
                mbox.showerror("Error", f"No se encontró la venta con ID {sale_id}")
                self._close_fullscreen_view()
                return
            products_dict = json.loads(sale["products"])
            client_id = sale["client_id"]
            total_actual = sale["total"]

        # inicializa el diccionario y la lista de productos existentes
        self.manage_sale("init")
        for pid, info in products_dict.items():
            with get_conn() as c:
                prod = c.execute("SELECT sale_price FROM products WHERE product_id = ?", (pid,)).fetchone()
            if prod:
                price = prod["sale_price"]
                self.manage_sale("add", product_id=pid, quantity=info["quantity"], unit_price=price)

        # se puede editar cliente
        ctk.CTkLabel(frame, text="Cliente asignado:", font=("Open Sans", 18, "bold")).pack(anchor="w", padx=20,pady=(10, 0))
        self.ent_client_search = ctk.CTkEntry(frame, width=350, height=34, corner_radius=14,fg_color="white", text_color="black", border_color="#cfcfcf")
        self.ent_client_search.pack(padx=20, pady=(4, 10), anchor="w")
        self.ent_client_search.bind("<KeyRelease>", self.update_client_search)

        self.client_frame = ctk.CTkScrollableFrame(frame, fg_color="white", height=80)
        self.client_frame.pack(fill="x", padx=20, pady=5)

        self.selected_client = client_id
        with get_conn() as c:
            client = c.execute("""
                SELECT u.name 
                FROM clients c
                JOIN users u ON c.user_id = u.user_id
                WHERE c.client_id = ?
            """, (client_id,)).fetchone()

        self.ent_client_search.insert(0, client["name"] if client else "Desconocido")

        # busca y agrega productos nuevos
        ctk.CTkLabel(frame, text="Agregar productos:", font=("Open Sans", 18, "bold")).pack(anchor="w", padx=20,
                                                                                            pady=(20, 0))
        self.ent_prod_search = ctk.CTkEntry(frame, width=350, height=34, corner_radius=14,fg_color="white", text_color="black", border_color="#cfcfcf")
        self.ent_prod_search.pack(padx=20, pady=(4, 10), anchor="w")
        self.ent_prod_search.bind("<KeyRelease>", self.update_product_search_edit)

        self.products_frame = ctk.CTkScrollableFrame(frame, fg_color="white", height=220)
        self.products_frame.pack(fill="x", padx=20, pady=5)

        # productos acutales
        ctk.CTkLabel(frame, text="Productos actuales:", font=("Open Sans", 18, "bold")).pack(anchor="w", padx=20,
                                                                                             pady=(20, 0))
        self.cart_frame = ctk.CTkScrollableFrame(frame, fg_color="white", height=240)
        self.cart_frame.pack(fill="x", padx=20, pady=5)

        # muestra el total
        self.lbl_total = ctk.CTkLabel(frame, text=f"Total actual: Q{total_actual:.2f}",font=("Open Sans", 20, "bold"), text_color="#333333")
        self.lbl_total.pack(anchor="e", padx=30, pady=(10, 5))

        # botones
        btns = ctk.CTkFrame(frame, fg_color="transparent", corner_radius=20)
        btns.pack(pady=25)
        ctk.CTkButton(btns, text="Guardar cambios", width=200, height=40, corner_radius=20,fg_color="#e0e0e0", hover_color="#9e9e9e", text_color="black",font=("Open Sans", 15, "bold", "underline"),command=lambda: self.save_sale_edit(sale_id)).pack(pady=(0, 12))
        ctk.CTkButton(btns, text="Volver", width=200, height=40, corner_radius=20,fg_color="#e0e0e0", hover_color="#9e9e9e", text_color="black",font=("Open Sans", 15, "bold", "underline"),command=self._close_fullscreen_view).pack()

        # muestra el diccionario actual
        self.refresh_cart_view_edit()

    def update_product_search_edit(self, *_):
        """muestra productos disponibles (para agregar nuevos durante la edición)"""
        term = self.ent_prod_search.get().lower().strip()
        for widget in self.products_frame.winfo_children():
            widget.destroy()

        with get_conn() as c:
            rows = c.execute("SELECT product_id, name, sale_price, stock FROM products").fetchall()

        for row in rows:
            if term in row["name"].lower():
                pid, name, price, stock = row["product_id"], row["name"], row["sale_price"], row["stock"]

                frame = ctk.CTkFrame(self.products_frame, fg_color="#f8f8f8", corner_radius=8)
                frame.pack(fill="x", padx=10, pady=4)

                ctk.CTkLabel(frame, text=f"{name} (Q{price}) | Stock: {stock}",text_color="black", anchor="w", font=("Open Sans", 14)).pack(side="left", padx=8)

                qty_var = tk.IntVar(value=1)
                ctk.CTkButton(frame, text="-", width=30, command=lambda v=qty_var: v.set(max(1, v.get() - 1))).pack(side="right", padx=2)
                ctk.CTkEntry(frame, width=40, textvariable=qty_var, justify="center").pack(side="right", padx=2)
                ctk.CTkButton(frame, text="+", width=30, command=lambda v=qty_var: v.set(v.get() + 1)).pack(side="right", padx=2)
                ctk.CTkButton(frame, text="Agregar", width=100,command=lambda pid=pid, p=price, q=qty_var, n=name, s=stock: self.add_product_to_edit(pid,p,q,n,s)).pack(side="right", padx=8)

    def add_product_to_edit(self, product_id, price, qty_var, name, stock):
        """agrega un producto nuevo a la lista de edición (validando stock)"""
        cantidad = qty_var.get()
        if cantidad > stock:
            mbox.showerror("Stock insuficiente", f"No hay suficiente stock para {name}.")
            return
        self.manage_sale("add", product_id, cantidad, price)
        self.refresh_cart_view_edit()

    def refresh_cart_view_edit(self):
        """actualiza la vista de productos dentro de la venta (editable)"""
        for widget in self.cart_frame.winfo_children():
            widget.destroy()

        if not hasattr(self, "current_sale") or not self.current_sale["products"]:
            ctk.CTkLabel(self.cart_frame, text="No hay productos agregados.",text_color="gray", font=("Open Sans", 14, "italic")).pack(pady=10)
            self.lbl_total.configure(text="Total actual: Q0.00")
            return

        for pid, info in self.current_sale["products"].items():
            row = ctk.CTkFrame(self.cart_frame, fg_color="#f4f4f4", corner_radius=10)
            row.pack(fill="x", padx=10, pady=4)

            with get_conn() as c:
                prod = c.execute("SELECT name, sale_price, stock FROM products WHERE product_id = ?", (pid,)).fetchone()
                if not prod: continue
                name, price, stock = prod["name"], prod["sale_price"], prod["stock"]

            ctk.CTkLabel(row, text=f"{name}", anchor="w", font=("Open Sans", 14, "bold"), text_color="black").pack(side="left", padx=10)
            qty_var = tk.IntVar(value=info["quantity"])

            # Botones para editar cantidad
            ctk.CTkButton(row,text="-",width=30, height=28,command=lambda v=qty_var: self.change_qty_edit(pid, v, price, -1)).pack(side="right", padx=2)
            ctk.CTkEntry(row,width=40,textvariable=qty_var,justify="center").pack(side="right", padx=2)
            ctk.CTkButton(row,text="+", width=30, height=28,command=lambda v=qty_var: self.change_qty_edit(pid, v, price, +1)).pack(side="right", padx=2)
            ctk.CTkLabel(row, text=f"Subtotal: Q{info['subtotal']:.2f}", anchor="center",font=("Open Sans", 13), text_color="black").pack(side="left", padx=10)

            # Botón eliminar
            ctk.CTkButton(row,text="X",width=30,height=28,fg_color="#e57373",hover_color="#ef5350", text_color="white",command=lambda p=pid: self.remove_product_from_cart_edit(p)).pack(side="right", padx=10)

        total = self.manage_sale("total")
        self.lbl_total.configure(text=f"Total actual: Q{total:.2f}")

    def change_qty_edit(self, product_id, qty_var, price, delta):
        """cambia cantidad y recalcula subtotal, lo actualiza."""
        new_qty = max(1, qty_var.get() + delta)
        qty_var.set(new_qty)
        self.manage_sale("add", product_id, 0, price)  # fuerza recalculo
        self.current_sale["products"][product_id]["quantity"] = new_qty
        self.current_sale["products"][product_id]["subtotal"] = round(new_qty * price, 2)
        self.refresh_cart_view_edit()

    def remove_product_from_cart_edit(self, product_id):
        """elimina un producto del carrito en edición"""
        self.manage_sale("remove", product_id)
        self.refresh_cart_view_edit()

    def save_sale_edit(self, sale_id):
        """guarda los cambios realizados en la venta (cliente, productos y total)"""
        try:
            if not hasattr(self, "current_sale") or not self.current_sale["products"]:
                mbox.showerror("Error", "No hay productos en la venta.")
                return
            new_client = self.selected_client
            new_products = self.current_sale["products"]
            new_total = round(sum(item["subtotal"] for item in new_products.values()), 2)

            with get_conn() as conn:
                conn.execute("""
                    UPDATE sales 
                    SET client_id = ?, products = ?, total = ?
                    WHERE sale_id = ?
                """, (new_client, json.dumps(new_products, ensure_ascii=False), new_total, sale_id))
                conn.commit()


            mbox.showinfo("Venta actualizada", f"Se actualizó la venta {sale_id} correctamente.")
            self._close_fullscreen_view()
        except Exception as e:
            mbox.showerror("Error", f"No se pudo actualizar la venta:\n{e}")

    def view_edit_provider(self, provider_id):
        """Formulario para editar un proveedor existente"""
        container = self._open_fullscreen_view()
        frame = ctk.CTkScrollableFrame(container, fg_color="#fafafa")
        frame.pack(expand=True, fill="both")

        title = ctk.CTkLabel(frame, text="Editar proveedor", font=("Open Sans", 50, "bold"), text_color="#111111")
        title.pack(pady=(40, 20))

        # Cargar datos del proveedor
        provider = Provider.load(provider_id)
        if not provider:
            mbox.showerror("Error", f"No se encontró el proveedor con ID {provider_id}")
            self._close_fullscreen_view()
            return

        # Muestra el ID del proveedor que no es editable, solo es lectura
        row_id = ctk.CTkFrame(frame, fg_color="#e0e0e0", corner_radius=20)
        row_id.pack(pady=10, ipadx=10, ipady=6)
        row_id.grid_columnconfigure(0, minsize=160)
        row_id.grid_columnconfigure(1, minsize=320)
        ctk.CTkLabel(row_id, text="ID Proveedor", font=("Open Sans", 18)).grid(row=0, column=0, padx=(14, 8), pady=8,sticky="nsew")
        ent_id = ctk.CTkEntry(row_id, width=300, height=36, corner_radius=14, fg_color="#f2f2f2", text_color="gray",border_color="#cfcfcf")
        ent_id.insert(0, provider.provider_id)
        ent_id.configure(state="disabled")
        ent_id.grid(row=0, column=1, padx=(8, 14), pady=8, sticky="w")

        # Nombre editable
        row_name = ctk.CTkFrame(frame, fg_color="#e0e0e0", corner_radius=20)
        row_name.pack(pady=10, ipadx=10, ipady=6)
        row_name.grid_columnconfigure(0, minsize=160)
        row_name.grid_columnconfigure(1, minsize=320)
        ctk.CTkLabel(row_name, text="Nombre", font=("Open Sans", 18)).grid(row=0, column=0, padx=(14, 8), pady=8,sticky="nsew")
        self.ent_nombre = ctk.CTkEntry(row_name, width=300, height=36, corner_radius=14, fg_color="white",text_color="black", border_color="#cfcfcf")
        self.ent_nombre.insert(0, provider.name)
        self.ent_nombre.grid(row=0, column=1, padx=(8, 14), pady=8, sticky="w")

        # Teléfono editable
        row_tel = ctk.CTkFrame(frame, fg_color="#e0e0e0", corner_radius=20)
        row_tel.pack(pady=10, ipadx=10, ipady=6)
        row_tel.grid_columnconfigure(0, minsize=160)
        row_tel.grid_columnconfigure(1, minsize=320)
        ctk.CTkLabel(row_tel, text="Teléfono", font=("Open Sans", 18)).grid(row=0, column=0, padx=(14, 8), pady=8,sticky="nsew")
        self.ent_tel = ctk.CTkEntry(row_tel, width=300, height=36, corner_radius=14, fg_color="white",text_color="black", border_color="#cfcfcf")
        self.ent_tel.insert(0, provider.phone)
        self.ent_tel.grid(row=0, column=1, padx=(8, 14), pady=8, sticky="w")

        # Lista de productos
        ctk.CTkLabel(frame, text="Productos asociados:", font=("Open Sans", 18, "bold")).pack(anchor="w", padx=20,pady=(10, 0))
        self.products_frame = ctk.CTkScrollableFrame(frame, fg_color="white", height=100)
        self.products_frame.pack(fill="x", padx=20, pady=5)

        # Diccionario donde se guardan los checkbox (para saber cuales se están seleccionado)
        self.product_checks = {}
        with get_conn() as c:  # consulta todos los productos de la base de datos
            rows = c.execute("SELECT product_id, name FROM products").fetchall()

        for row in rows:   # Recorre los productos y crea un checkbox para cada uno
            pid, name = row["product_id"], row["name"]
            var = tk.IntVar(value=1 if pid in provider.products else 0)
            chk = ctk.CTkCheckBox(self.products_frame, text=f"{name}", text_color="black", font=("Open Sans", 14),variable=var, onvalue=1, offvalue=0)
            chk.var = var  # Guarda la variable para consultar luego su estado
            chk.pack(anchor="w", padx=10, pady=4)
            self.product_checks[pid] = chk # se agrega al diccionario para tener acceso

        # Botones
        btns = ctk.CTkFrame(frame, fg_color="transparent", corner_radius=20)
        btns.pack(pady=25)

        ctk.CTkButton(btns, text="Guardar cambios", width=200, height=40, corner_radius=22,fg_color="#e0e0e0", hover_color="#9e9e9e", text_color="black",font=("Open Sans", 15, "bold", "underline"),command=lambda: self.save_provider_edit(provider)).pack(pady=(0, 12))
        ctk.CTkButton(btns, text="Volver", width=200, height=40, corner_radius=22,fg_color="#e0e0e0", hover_color="#9e9e9e", text_color="black",font=("Open Sans", 15, "bold", "underline"),command=self._close_fullscreen_view).pack()

    def save_provider_edit(self, provider):
        """Guarda los cambios realizados al proveedor."""
        new_name = self.ent_nombre.get().strip()
        new_phone = self.ent_tel.get().strip()

        # ciclo para recolectar los productos seleccionados
        selected_products = []
        for pid, chk in self.product_checks.items():
            if chk.var.get() == 1:
                selected_products.append(pid)

        if not new_name or not new_phone:
            mbox.showerror("Error", "Debe llenar todos los campos.")
            return

        try:
            provider.name = new_name
            provider.phone = new_phone
            provider.products = selected_products
            provider.save()
            mbox.showinfo("Proveedor actualizado", f"El proveedor '{new_name}' fue actualizado correctamente.")
            self._close_fullscreen_view()
        except Exception as e:
            mbox.showerror("Error", f"No se pudo actualizar el proveedor:\n{e}")

    def view_edit_collab(self, collab_id):
        """Formulario para editar un colaborador existente."""
        container = self._open_fullscreen_view()
        frame = ctk.CTkScrollableFrame(container, fg_color="#fafafa")
        frame.pack(expand=True, fill="both")

        title = ctk.CTkLabel(frame, text="Editar colaborador", font=("Open Sans", 50, "bold"), text_color="#111111")
        title.pack(pady=(40, 20))

        # Carga datos del colaborador
        collab = Collaborator.load(collab_id)

        # ID, solo lo muestra
        row_id = ctk.CTkFrame(frame, fg_color="#e0e0e0", corner_radius=20)
        row_id.pack(pady=10,ipadx=10,ipady=6)
        ctk.CTkLabel(row_id,text="ID Colaborador",font=("Open Sans", 18)).pack(side="left",padx=14,pady=8)
        ent_id = ctk.CTkEntry(row_id,width=300,height=36,corner_radius=14,fg_color="#f2f2f2",text_color="gray",border_color="#cfcfcf")
        ent_id.insert(0, collab.collab_id)
        ent_id.configure(state="disabled")
        ent_id.pack(side="left", padx=10, pady=8)

        # nombre
        row_name = ctk.CTkFrame(frame,fg_color="#e0e0e0",corner_radius=20)
        row_name.pack(pady=10,ipadx=10,ipady=6)
        ctk.CTkLabel(row_name, text="Nombre", font=("Open Sans", 18)).pack(side="left", padx=14, pady=8)
        self.ent_nombre = ctk.CTkEntry(row_name,width=300,height=36,corner_radius=14,fg_color="white",text_color="black",border_color="#cfcfcf")
        self.ent_nombre.insert(0, collab.name)
        self.ent_nombre.pack(side="left", padx=10, pady=8)

        # teléfono
        row_tel = ctk.CTkFrame(frame, fg_color="#e0e0e0", corner_radius=20)
        row_tel.pack(pady=10, ipadx=10, ipady=6)
        ctk.CTkLabel(row_tel, text="Teléfono", font=("Open Sans", 18)).pack(side="left", padx=14, pady=8)

        self.ent_tel = ctk.CTkEntry( row_tel,width=300,height=36,corner_radius=14,fg_color="white",text_color="black",border_color="#cfcfcf")
        self.ent_tel.insert(0, collab.phone)
        self.ent_tel.pack(side="left", padx=10, pady=8)

        # puesto
        row_pos = ctk.CTkFrame(frame, fg_color="#e0e0e0", corner_radius=20)
        row_pos.pack(pady=10, ipadx=10, ipady=6)
        ctk.CTkLabel(row_pos, text="Puesto", font=("Open Sans", 18)).pack(side="left", padx=14, pady=8)
        self.ent_pos = ctk.CTkEntry(row_pos, width=300, height=36, corner_radius=14,fg_color="white", text_color="black", border_color="#cfcfcf")
        self.ent_pos.insert(0, collab.position)
        self.ent_pos.pack(side="left", padx=10, pady=8)

        # botones
        btns = ctk.CTkFrame(frame, fg_color="transparent", corner_radius=20)
        btns.pack(pady=25)
        ctk.CTkButton(btns,text="Guardar cambios",width=200,height=40,corner_radius=22,fg_color="#e0e0e0",hover_color="#9e9e9e",text_color="black",font=("Open Sans", 15, "bold", "underline"),command=lambda: self.save_collaborator_edit(collab)).pack(pady=(0, 12))
        ctk.CTkButton(btns,text="Volver",width=200,height=40,corner_radius=22,fg_color="#e0e0e0",hover_color="#9e9e9e",text_color="black",font=("Open Sans", 15, "bold", "underline"),command=self._close_fullscreen_view).pack()

    def save_collaborator_edit(self, collab):
        """Guarda los cambios realizados al colaborador."""
        new_name = self.ent_nombre.get().strip()
        new_phone = self.ent_tel.get().strip()
        new_pos = self.ent_pos.get().strip()

        if not new_name or not new_phone or not new_pos:
            mbox.showerror("Error", "Debe llenar todos los campos.")
            return

        try:
            collab.name = new_name
            collab.phone = new_phone
            collab.position = new_pos
            collab.save()
            mbox.showinfo("Colaborador actualizado", f"El colaborador '{new_name}' fue actualizado correctamente.")
            self._close_fullscreen_view()
        except Exception as e:
            mbox.showerror("Error", f"No se pudo actualizar el colaborador:\n{e}")

    def view_edit_client(self, client_id):
        """Formulario para editar un cliente existente"""
        container = self._open_fullscreen_view()
        frame = ctk.CTkScrollableFrame(container, fg_color="#fafafa")
        frame.pack(expand=True, fill="both")

        title = ctk.CTkLabel(frame, text="Editar cliente", font=("Open Sans", 50, "bold"), text_color="#111111")
        title.pack(pady=(40, 20))

        # Carga datos del cliente
        client = Client.load(client_id)

        # ID, solo lectura
        row_id = ctk.CTkFrame(frame, fg_color="#e0e0e0", corner_radius=20)
        row_id.pack(pady=10, ipadx=10, ipady=6)
        ctk.CTkLabel(row_id, text="ID Cliente", font=("Open Sans", 18)).pack(side="left", padx=14, pady=8)
        ent_id = ctk.CTkEntry(row_id, width=300, height=36, corner_radius=14, fg_color="#f2f2f2",text_color="gray", border_color="#cfcfcf")
        ent_id.insert(0, client.client_id)
        ent_id.configure(state="disabled")
        ent_id.pack(side="left", padx=10, pady=8)

        # nombre
        row_name = ctk.CTkFrame(frame, fg_color="#e0e0e0", corner_radius=20)
        row_name.pack(pady=10, ipadx=10, ipady=6)
        ctk.CTkLabel(row_name, text="Nombre", font=("Open Sans", 18)).pack(side="left", padx=14, pady=8)
        self.ent_nombre = ctk.CTkEntry(row_name, width=300, height=36, corner_radius=14,fg_color="white", text_color="black", border_color="#cfcfcf")
        self.ent_nombre.insert(0, client.name)
        self.ent_nombre.pack(side="left", padx=10, pady=8)

        # teléfono
        row_tel = ctk.CTkFrame(frame, fg_color="#e0e0e0", corner_radius=20)
        row_tel.pack(pady=10, ipadx=10, ipady=6)
        ctk.CTkLabel(row_tel, text="Teléfono", font=("Open Sans", 18)).pack(side="left", padx=14, pady=8)
        self.ent_tel = ctk.CTkEntry(row_tel, width=300, height=36, corner_radius=14,fg_color="white", text_color="black", border_color="#cfcfcf")
        self.ent_tel.insert(0, client.phone)
        self.ent_tel.pack(side="left", padx=10, pady=8)

        # botones
        btns = ctk.CTkFrame(frame, fg_color="transparent", corner_radius=20)
        btns.pack(pady=25)
        ctk.CTkButton(btns, text="Guardar cambios", width=200, height=40, corner_radius=22,fg_color="#e0e0e0", hover_color="#9e9e9e", text_color="black",font=("Open Sans", 15, "bold", "underline"),command=lambda: self.save_client_edit(client)).pack(pady=(0, 12))
        ctk.CTkButton(btns, text="Volver", width=200, height=40, corner_radius=22,fg_color="#e0e0e0", hover_color="#9e9e9e", text_color="black",font=("Open Sans", 15, "bold", "underline"),command=self._close_fullscreen_view).pack()

    def save_client_edit(self, client):
        """Guarda los cambios realizados al cliente."""
        new_name = self.ent_nombre.get().strip()
        new_phone = self.ent_tel.get().strip()

        if not new_name or not new_phone:
            mbox.showerror("Error", "Debe llenar todos los campos.")
            return

        try:
            client.name = new_name
            client.phone = new_phone
            client.save()
            mbox.showinfo("Cliente actualizado", f"El cliente '{new_name}' fue actualizado correctamente.")
            self._close_fullscreen_view()
        except Exception as e:
            mbox.showerror("Error", f"Error inesperado: \n{e}")

    def view_edit_product(self, product_id):
        """Formulario para editar un producto existente (mismo estilo que 'Crear producto')."""
        frame = self._open_fullscreen_view()

        title = ctk.CTkLabel(frame, text="Editar producto", font=("Open Sans", 50, "bold"), text_color="#111111")
        title.pack(pady=(60, 40))

        container = ctk.CTkFrame(frame, fg_color="transparent")
        container.pack(pady=10)

        # Carga datos del producto
        product = Product.load(product_id)

        # ID, solo lectura
        row_id = ctk.CTkFrame(container, fg_color="#e0e0e0", corner_radius=20)
        row_id.pack(pady=10, ipadx=10, ipady=6)
        ctk.CTkLabel(row_id, text="ID Producto", font=("Open Sans", 18)).pack(side="left", padx=14, pady=8)
        ent_id = ctk.CTkEntry(row_id, width=300, height=36, corner_radius=14,fg_color="#f2f2f2", text_color="gray", border_color="#cfcfcf")
        ent_id.insert(0, product.product_id)
        ent_id.configure(state="disabled")
        ent_id.pack(side="left", padx=10, pady=8)
        # fila 1
        row1 = ctk.CTkFrame(container, fg_color="transparent")
        row1.pack(pady=6)

        # nombre
        row_nombre = ctk.CTkFrame(row1, fg_color="#e0e0e0", corner_radius=20)
        row_nombre.pack(side="left",ipadx=10, ipady=6)
        ctk.CTkLabel(row_nombre, text="Nombre", font=("Open Sans", 18)).pack(side="left", padx=14, pady=8)
        self.ent_nombre = ctk.CTkEntry(row_nombre, width=300, height=36, corner_radius=14,fg_color="white", text_color="black", border_color="#cfcfcf")
        self.ent_nombre.insert(0, product.name)
        self.ent_nombre.pack(side="left", padx=10, pady=8)

        # tipo
        row_tipo = ctk.CTkFrame(row1, fg_color="#e0e0e0", corner_radius=20)
        row_tipo.pack(side="right",ipadx=10, ipady=6)
        ctk.CTkLabel(row_tipo, text="Tipo", font=("Open Sans", 18)).pack(side="left", padx=14, pady=8)
        self.ent_tipo = ctk.CTkEntry(row_tipo, width=300, height=36, corner_radius=14,fg_color="white", text_color="black", border_color="#cfcfcf")
        self.ent_tipo.insert(0, product.type)
        self.ent_tipo.pack(side="left", padx=10, pady=8)
        # fila 2
        row2 = ctk.CTkFrame(container, fg_color="transparent")
        row2.pack(pady=6)

        # descripción
        row_desc = ctk.CTkFrame(row2, fg_color="#e0e0e0", corner_radius=20)
        row_desc.pack(side="left",ipadx=10, ipady=6)
        ctk.CTkLabel(row_desc, text="Descripción", font=("Open Sans", 18)).pack(side="left", padx=14, pady=8)
        self.ent_desc = ctk.CTkEntry(row_desc, width=400, height=36, corner_radius=14,fg_color="white", text_color="black", border_color="#cfcfcf")
        self.ent_desc.insert(0, product.description)
        self.ent_desc.pack(side="left", padx=10, pady=8)

        # stock
        row_stock = ctk.CTkFrame(row2, fg_color="#e0e0e0", corner_radius=20)
        row_stock.pack(side="right",ipadx=10, ipady=6)
        ctk.CTkLabel(row_stock, text="Stock", font=("Open Sans", 18)).pack(side="left", padx=14, pady=8)
        self.ent_stock = ctk.CTkEntry(row_stock, width=150, height=36, corner_radius=14,fg_color="white", text_color="black", border_color="#cfcfcf")
        self.ent_stock.insert(0, product.stock)
        self.ent_stock.pack(side="left", padx=10, pady=8)
        # fila 3
        row3 = ctk.CTkFrame(container, fg_color="transparent")
        row3.pack(pady=6)

        # precio costo
        row_costo = ctk.CTkFrame(row3, fg_color="#e0e0e0", corner_radius=20)
        row_costo.pack(side="left",ipadx=10, ipady=6)
        ctk.CTkLabel(row_costo, text="Precio costo", font=("Open Sans", 18)).pack(side="left", padx=14, pady=8)
        self.ent_costo = ctk.CTkEntry(row_costo, width=150, height=36, corner_radius=14,fg_color="white", text_color="black", border_color="#cfcfcf")
        self.ent_costo.insert(0, product.raw_p)
        self.ent_costo.pack(side="left", padx=10, pady=8)

        # precio venta
        row_venta = ctk.CTkFrame(row3, fg_color="#e0e0e0", corner_radius=20)
        row_venta.pack(side="right",ipadx=10, ipady=6)
        ctk.CTkLabel(row_venta, text="Precio venta", font=("Open Sans", 18)).pack(side="left", padx=14, pady=8)
        self.ent_venta = ctk.CTkEntry(row_venta, width=150, height=36, corner_radius=14,fg_color="white", text_color="black", border_color="#cfcfcf")
        self.ent_venta.insert(0, product.sale_p)
        self.ent_venta.pack(side="left", padx=10, pady=8)

        # botones
        btns = ctk.CTkFrame(frame, fg_color="transparent", corner_radius=20)
        btns.pack(pady=25)

        ctk.CTkButton(btns, text="Guardar cambios", width=240, height=45, corner_radius=22,fg_color="#e0e0e0", hover_color="#9e9e9e", text_color="black",font=("Open Sans", 15, "bold", "underline"),command=lambda: self.save_product_edit(product)).pack(pady=(0, 12))
        ctk.CTkButton(btns, text="Volver", width=240, height=45, corner_radius=22,fg_color="#e0e0e0", hover_color="#9e9e9e", text_color="black",font=("Open Sans", 15, "bold", "underline"),command=self._close_fullscreen_view).pack()

    def save_product_edit(self, product):
        """Guarda los cambios realizados al producto."""
        new_name = self.ent_nombre.get().strip()
        new_type = self.ent_tipo.get().strip()
        new_desc = self.ent_desc.get().strip()

        try:
            new_stock = int(self.ent_stock.get())
            new_raw = float(self.ent_costo.get())
            new_sale = float(self.ent_venta.get())
        except ValueError:
            mbox.showerror("Error numérico", "Debe ingresar valores válidos para precios y stock.")
            return

        if not new_name or not new_type or not new_desc:
            mbox.showerror("Campos vacíos", "Debe llenar todos los campos de texto.")
            return

        if new_stock < 0:
            mbox.showerror("Error de stock", "El stock no puede ser negativo.")
            return

        if new_raw <= 0 or new_sale <= 0:
            mbox.showerror("Error de precios", "Los precios deben ser mayores que cero.")
            return

        if new_sale <= new_raw:
            mbox.showerror("Error de precios", "El precio de venta debe ser mayor que el costo.")
            return

        try:
            product.name = new_name
            product.type = new_type
            product.description = new_desc
            product.stock = new_stock
            product.raw_p = str(new_raw)
            product.sale_p = str(new_sale)
            product.save()
            mbox.showinfo("Producto actualizado", f"El producto '{new_name}' fue actualizado correctamente.")
            self._close_fullscreen_view()
        except Exception as e:
            mbox.showerror("Error", f"Error inesperado:\n{e}")

    def logout(self):
        confirm = mbox.askyesno("Cerrar sesión", "¿Deseas cerrar tu sesión actual?")
        if confirm:
            from login import LoginUI
            self.close_searchbar()
            self.pack_forget()
            LoginUI(self.master)

    def db_extract(self, ref_classes):
        with get_conn() as c:
            out = {}
            cur = c.cursor()

            # Obtiene todas las tablas que NO sean de metadatos (creadas por SQL para operaciones internas)
            cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
            tables = [r[0] for r in cur.fetchall()]

            for table in tables:
                # Obtención de encabezados de tabla
                cur.execute(f"PRAGMA table_info('{table}')")
                info = cur.fetchall()
                cols = [col[1] for col in info]

                # obtiene filas
                cur.execute(f"SELECT * FROM {table}")
                rows = cur.fetchall()

                # crear objetos con las filas para usar sus funciones y no complicarnos la vida
                the_class = ref_classes.get(table)
                objects = []
                for row in rows:
                    # Revisa como extrae la info, no creo que este bien
                    row_dict = dict(zip(cols, row))
                    kind_id = row_dict[cols[0]]
                    obj = the_class.load(kind_id)
                    if obj is not None:
                        objects.append(obj)
                out[table] = objects
            return out

    def entry_upd(self, entry_var, *args):
        return entry_var.get()

        # función para cerrar la searchbar
    def close_searchbar(self):
        frm = getattr(self, "searchbar_frame", None)
        if frm and frm.winfo_exists():
            try:
                frm.destroy()
            except Exception:
                pass
        # cerrar popup abierto (si es que hay alguno)
        pop = getattr(self, "current_popup", None)
        if pop and pop.winfo_exists():
            try:
                pop.destroy()
            except Exception:
                pass

    def menu_visualizer(self, root, kind):
        """
        t e x t o
        """
        with get_conn() as c:

            #extrae la información de una tabla en la base de datos, buscándola con el nombre "kind" (argumento ingresado)
            cur = c.cursor()
            cur.execute("SELECT name FROM sqlite_master WHERE type ='table' AND name = ? LIMIT 1;", (kind,))
            if not cur.fetchone():
                return None

            # Inicializadores: "cols" es para las referencias en la tabla, "titles_dict" es para los títulos de las columnas
            cols = {"sales": ["sale_id", "time", "_client_id", "products", "total"], "products": ["product_id", "name", "type", "description", "sale_p", "stock"], "clients": ["client_id", "name", "phone", "sales"], "collaborators": ["collab_id", "name", "phone", "position"], "providers":["provider_id", "name", "phone", "products"]}
            titles_dict = {"sales": ["ID", "hora", "cliente asociado", "productos", "total"], "products": ["ID", "Nombre", "Tipo", "Descripción", "Precio", "Stock"], "clients": ["ID", "Nombre", "Teléfono", "compras"], "collaborators": ["ID", "Nombre", "Teléfono", "Posición"], "providers":["ID", "Nombre", "Teléfono", "productos"]}
            headers = cols[kind]
            titles = titles_dict[kind]
            #Los junta en un dict que funcione como "ID": "sale_id", "hora":"time"... para que, al momento de mostrar filtros, se mire en español y afecte los filtros en inglés (como están en la db)
            main_headers = dict(zip(titles, headers))
            #extrae los datos de la db_info
            self.db_info = self.db_extract(classes)
            table_data = self.db_info[kind]
            print(table_data)

            # Aquí se guarda la info de los meses, años y días para los filtros de fecha si se miran las "ventas"
            months = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
            years = [str(y) for y in range (2025, 2030)]

            item_map = {}
            def apply_filters(m_tree):
                base = table_data
                result = base[:]

                # reiniciar el treeview con los datos filtrados
                for chld in m_tree.get_children():
                    m_tree.delete(chld)
                item_map.clear()

                #filtro por encabezado seleccionado
                header_selected = getattr(filter_btn, "filter_value", None)
                header_attr = main_headers.get(header_selected, header_selected) if header_selected else None
                #texto ingresado en el buscador
                search_text = ""
                try:
                    search_text = search_var.get().strip()
                except Exception:
                    pass
                if search_text:
                    s=search_text.lower()
                    if header_attr:
                        result = [obj for obj in result if s in str(getattr(obj, header_attr, "")).lower()]
                    else:
                        tmp = []
                        for obj in result:
                            for h in headers:
                                if s in str(getattr(obj, h, "")).lower():
                                    tmp.append(obj)
                                    break
                        result = tmp
                # filtrar por fecha (si aplica)
                date_vals = getattr(date_btn, "date_value", None)
                if date_vals is not None:
                    #Intenta obtener los atributos de cada uno
                    fy = int(date_vals.get("year", "")) if date_vals.get("year") else None
                    fm = int(date_vals.get("month", "")) if date_vals.get("month") else None
                    fd = int(date_vals.get("day", "")) if date_vals.get("day") else None
                    if fy or fm or fd:  # Filtra si al menos uno está set
                        filtered = []
                        for obj in result:
                            r = getattr(obj, "date", None)
                            if r:
                                # Maneja si r es str (por seguridad)
                                if isinstance(r, str):
                                    try:
                                        r = datetime.strptime(r, "%d/%m/%Y").date()
                                    except ValueError:
                                        continue
                                # Extrae componentes
                                rd, rm, ry = r.day, r.month, r.year

                                # Filtrado progresivo: coincide lo que esté set
                                match = True
                                if fy is not None and ry != fy:
                                    match = False
                                if fm is not None and rm != fm:
                                    match = False
                                if fd is not None and rd != fd:
                                    match = False
                                if match:
                                    filtered.append(obj)
                        result = filtered
                    else:
                        pass
                for idx, item in enumerate(result):
                    all_vals = [str(getattr(item, t, "")) for t in headers]

                    #revisar si es "sales" o "providers" para poner la sección de "vista"
                    try:
                        title_idx = headers.index("products")
                        if kind in ("sales", "providers"):
                            all_vals[title_idx] = "Ver ▾"
                    except ValueError:
                        title_idx = None

                    # Añadir al tree_insert y al trace_map
                    iid = f"r{idx}"
                    m_tree.insert("", "end", iid=iid, values=all_vals)
                    item_map[iid] = item
                    search_btn.focus_set()

            # crea el frame y el espacio para los botoncitos
            if getattr(self, "searchbar_frame", None) and self.searchbar_frame.winfo_exists():
                try:
                    self.searchbar_frame.destroy()
                except Exception:
                    pass
            self.searchbar_frame = ctk.CTkFrame(root, corner_radius=12,fg_color="#004857")
            self.searchbar_frame.pack(fill="both", expand=True, padx=8, pady=8)

            controls = ctk.CTkFrame(self.searchbar_frame,  fg_color="transparent")
            controls.pack(fill="x", padx=8, pady=(4,8))

            # inicializa los botoncitos para evitar error de llamada
            filter_btn = False
            date_btn = False
            search_btn = False
            back_btn = False

            if kind == "sales":
                # Organiza los botoncitos específicamente para las ventas
                filter_btn = ctk.CTkButton(controls, text="Filtrar", width = 150, height = 10, corner_radius=18, fg_color="#f4f1ec", hover_color="#f86a20", text_color="#004857", font=("Open Sans", 13, "bold"))
                filter_btn.pack(side="left", padx=6)
                date_btn = ctk.CTkButton(controls, text = "Fecha", width = 150, height = 10, corner_radius=18, fg_color="#f4f1ec", hover_color="#f86a20", text_color="#004857", font=("Open Sans", 13, "bold"))
                date_btn.pack(side="left", padx=6)
                search_var = ctk.StringVar()
                search_btn = ctk.CTkEntry(controls, placeholder_text = "Buscar...",text_color="#004857",textvariable = search_var, width = 400, height = 36, corner_radius = 18, fg_color = "white", placeholder_text_color = "grey", font=("Open Sans", 13, "bold"))
                search_btn.pack(side="left", padx=6)
                back_btn = ctk.CTkButton(controls, text = "Cerrar",command =self.close_searchbar, width = 100, height = 10 , corner_radius=18, fg_color="#f86a20",hover_color="#cd5618", text_color="white", font=("Open Sans", 13, "bold"))
                back_btn.pack(side="right", padx=6)
            else:
                # si es otro modo (proveedores, productos...), pone la configuración normal
                filter_btn = ctk.CTkButton(controls, width = 150, text = "Filtrar", height = 10, corner_radius=18, fg_color="#f4f1ec", hover_color="#f86a20", text_color="black", font=("Open Sans", 13, "bold"))
                filter_btn.pack(side="left", padx=6)
                search_var = ctk.StringVar()
                search_btn = ctk.CTkEntry(controls, placeholder_text="Buscar...",text_color="#004857",textvariable = search_var, width=400, height=36, corner_radius=18, fg_color="white", placeholder_text_color="grey", font=("Open Sans", 13, "bold"))
                search_btn.pack(side="left", padx=6)
                back_btn = ctk.CTkButton(controls, text="Cerrar",command = self.close_searchbar, width=100, height=10, corner_radius=18,fg_color="#f86a20", hover_color="#cd5618", text_color="white", font=("Open Sans", 13, "bold"))
                back_btn.pack(side="right", padx=6)

            print("search_var initial:", repr(search_var.get()))
            def header_filter(filter_button, options,origin_tree, initial = None, width = 150):
                old = getattr(self, "_current_popup", None)
                if old is not None and old.winfo_exists():
                    try:
                        old.destroy()
                    except Exception:
                        pass

                # Configuración del topLevel pa que parezca un combobox
                popup = ctk.CTkToplevel(filter_button.winfo_toplevel())
                filter_button.options_popup = popup
                popup.wm_overrideredirect(True)
                popup.transient(filter_button.winfo_toplevel())
                popup.attributes("-topmost", True)
                popup.update_idletasks()
                popup.deiconify()
                popup.lift()

                # poner debajo del botoncito
                ax = filter_button.winfo_rootx()
                ay = filter_button.winfo_rooty() + filter_button.winfo_height()
                popup.geometry(f"+{ax}+{ay}")

                # Contenedor
                bframe = ctk.CTkFrame(popup,corner_radius = 8, fg_color="transparent")
                bframe.pack(padx = 4, pady = 4)

                # Creación de la combobox y colocar su valor inicial
                cbox = ctk.CTkComboBox(bframe, values = options, width = width, height=36, corner_radius=18, fg_color="white", text_color="black", font=("Open Sans", 13, "bold"))
                if initial and initial in options:
                    cbox.set(initial)
                elif options:
                    cbox.set(options[0])
                cbox.pack(anchor = "w", pady = (0, 4))

                # Aplica el filtro obtenido. Si no funciona,
                def apply(value = None):
                    val =  value if value else cbox.get()

                    filter_button.filter_value = val
                    try:
                        popup.destroy()
                    except Exception as e:
                        print("error en la función: ",e)
                    apply_filters(origin_tree)

                cbox.configure(command = apply)

                def offclick(event):
                    if not popup.winfo_exists():
                        return
                    #obtener coordenadas del "evento"
                    x, y = event.x_root, event.y_root
                    #obtener coordenadas y dimensiones del toplevel del combobox
                    if popup.winfo_exists():
                        px, py = popup.winfo_rootx(), popup.winfo_rooty()
                        pw, ph = popup.winfo_width(), popup.winfo_height()

                        if not (px <= x <= px + pw and py <= y <= py + ph):
                            try: popup.destroy()
                            except: pass
                            try:delattr(filter_button, "options_popup")
                            except: pass
                            try: root.unbind_all("<Button-1>", b_id)
                            except Exception: pass

                b_id = root.bind_all("<Button-1>", offclick, add = "+")
                popup.focus_force()
                popup.grab_set()
                popup.wait_window()
                return

            # esta es la configuración del filtro de fecha
            def date_cb(date_button, origin_tree, first_values = None):
                old = getattr(self, "_current_popup", None)
                if old is not None and old.winfo_exists():
                    try:
                        old.destroy()
                    except Exception:
                        pass
                date_exists = getattr(root, "date_pop", None)
                if date_exists is not None and date_exists.winfo_exists():
                    try:
                        date_exists.lift()
                        return
                    except Exception:
                        try:
                            date_exists.destroy()
                        except Exception:
                            pass

                # crear y configurar un top level para que funcione más como un combobox con pequeñas comboboxes... y no como un toplevel
                date_pop = ctk.CTkToplevel(date_button.winfo_toplevel())
                date_button.date_pop = date_pop
                date_pop.wm_overrideredirect(True)
                date_pop.transient(date_button.winfo_toplevel())
                date_pop.attributes("-topmost", True)
                date_pop.update_idletasks()
                date_pop.deiconify()
                date_pop.lift()

                # colocarlo debajo del botoncito de acción

                ax = date_button.winfo_rootx()
                ay = date_button.winfo_rooty() + date_button.winfo_height()
                date_pop.geometry(f"+{ax}+{ay}")

                # configuramos el contenedor interno para que quede chulo
                popup_frame = ctk.CTkFrame(date_pop, corner_radius=12, fg_color = "white")
                popup_frame.pack(padx=4, pady=4)

                # le colocamos título
                title = ctk.CTkLabel(popup_frame, text = "Seleccionar fecha", fg_color="white")
                title.pack(anchor = "w", pady = (0, 4))

                selects = ctk.CTkFrame(popup_frame, fg_color="transparent")
                selects.pack(anchor = "w", pady = (0, 4))

                # combobox año
                cb_year = ctk.CTkComboBox(selects, values=years, width=100,  height=36, corner_radius=18, fg_color="white", text_color="black", font=("Open Sans", 13, "bold"))
                cb_year.pack(anchor = "w", pady = (0, 4))
                # combobox mes
                cb_month = ctk.CTkComboBox(selects, values=months, width=100,  height=36, corner_radius=18, fg_color="white", text_color="black", font=("Open Sans", 13, "bold"))
                cb_month.pack(anchor = "w", pady = (0, 4))
                # combobox día (varía con el mes, por eso empieza vacío)
                cb_day = ctk.CTkComboBox(selects, values = [], width=100,  height=36, corner_radius=18, fg_color="white", text_color="black", font=("Open Sans", 13, "bold"))
                cb_day.pack(anchor = "w", pady = (0, 4))

                # Si hay valore iniciales (first_values), los establecemos
                if first_values:
                    if first_values.get("month") in months:
                        cb_month.set(first_values.get("month"))
                    if first_values.get("year") in years:
                        cb_year.set(first_values.get("year"))
                    if first_values.get("day"):
                        cb_day.set(first_values.get("day"))

                #actualizador de fecha
                def upd_date():
                    #revisa el mes e intenta obtener el año
                    s_month = cb_month.get()
                    try:s_year = int(cb_year.get())
                    except: s_year = None

                    #revisa si el mes es válido y si el año existe para establecer los días
                    if s_month in months and s_year is not None:
                        n_month = months.index(s_month) + 1
                        n_days = calendar.monthrange(s_year, n_month)[1]
                        days = [f"{d:02d}" for d in range(1,n_days+1)]
                        cb_day.configure(values = days)
                        cur_day = cb_day.get()
                        if cur_day not in days:
                            cb_day.set(days[0])                    # si no, los días quedan vacíos
                    else:
                        cb_day.configure(values=[])
                        cb_day.set("")
                        print("Dias inválidos")

                def date_apply():
                    # poner valores y guardarlos en el botoncito
                    vals ={
                        "year": cb_year.get() if cb_year.get() in years else "",
                        "month": (f"{months.index(cb_month.get())+1:02d}" if cb_month.get() in months else ""),
                        "day": cb_day.get() if cb_day.get() else ""
                    }
                    date_button.date_value = vals
                    try:date_pop.destroy()
                    except Exception:pass
                    apply_filters(origin_tree)

                def date_change(changed):
                    if changed in ("year","month"):
                        upd_date()

                cb_year.configure(command= lambda _: date_change("year"))
                cb_month.configure(command = lambda _: date_change("month"))
                cb_day.configure(command = lambda _: date_change("day"))

                btn_apply = ctk.CTkButton(popup_frame, text="Aplicar", width=100, height=36, corner_radius=18,fg_color="#e0e0e0", hover_color="#9e9e9e", text_color="black",font=("Open Sans", 13, "bold"), command=date_apply)
                btn_apply.pack(pady=(8, 0))

                # cierra el toplevel si se hace click afuera del toplevel
                def click_outside(event):
                    x, y= event.x_root, event.y_root
                    if date_pop.winfo_exists():
                        px, py =date_pop.winfo_rootx(), date_pop.winfo_rooty()
                        pw, ph = date_pop.winfo_width(), date_pop.winfo_height()
                        e_id = getattr(event, "click_bind_id", None)
                        if not (px <= x <= px + pw and py <= y <= py + ph):
                            try: date_pop.destroy()
                            except Exception: pass
                            try:delattr(date_button, "options_popup")
                            except Exception: pass
                            try: root.unbind_all("<Button-1>", e_id)
                            except Exception: pass

                root.bind_all("<Button-1>", click_outside, add = "+")
                popup_frame.focus_force()
                upd_date()
                popup_frame.grab_set()
                popup_frame.wait_window()
                return

            def del_event(line, origin_tree, iid = None):
                # Crear pop-up personalizado para confirmación con input de ID
                confirm_popup = ctk.CTkToplevel(root)
                confirm_popup.title("Confirmar Eliminación")
                confirm_popup.geometry("300x200")
                confirm_popup.transient(root)
                confirm_popup.grab_set()  # Bloquea interacciones con otras ventanas
                confirm_popup.lift()  # Trae al frente

                # Centrar el pop-up
                root_x = root.winfo_rootx()
                root_y = root.winfo_rooty()
                root_w = root.winfo_width()
                root_h = root.winfo_height()
                w, h = 300, 200
                x = root_x + (root_w // 2) - (w // 2)
                y = root_y + (root_h // 2) - (h // 2)
                confirm_popup.geometry(f"{w}x{h}+{x}+{y}")

                # Etiqueta con mensaje
                msg = f"Para eliminar esta instancia (ID: {getattr(line, 'provider_id', getattr(line, 'client_id', getattr(line, 'sale_id', 'N/A')))}), ingresa tu ID de admin:"
                ctk.CTkLabel(confirm_popup, text=msg, wraplength=280, font=("Open Sans", 14)).pack(pady=20)

                # Campo de entrada para ID
                ent_id = ctk.CTkEntry(confirm_popup, width=200, height=36, corner_radius=14, fg_color="white", text_color="black", border_color="#cfcfcf", placeholder_text="Ingresa tu ID...", show = "●")
                ent_id.pack(pady=10)

                # Frame para botones
                btn_frame = ctk.CTkFrame(confirm_popup, fg_color="transparent")
                btn_frame.pack(pady=10)
                print(self.curr_id)
                def confirm_action():
                    input_id = ent_id.get().strip()
                   # Verifica contra la ID actual
                    if input_id == self.curr_id:
                        try:
                            line.delete()  # Elimina la instancia
                            self.db_info = self.db_extract(classes) #Actualiza la DB
                            origin_tree.delete(iid)
                            mbox.showinfo("Éxito", "Instancia eliminada correctamente.")
                            confirm_popup.destroy()
                            apply_filters(origin_tree)  # Refresca el Treeview
                            import sqlite3
                        except Exception as e:
                            mbox.showerror("Error", f"No se pudo eliminar: {e}")
                    else:
                        mbox.showerror("Error", "ID incorrecta. Acción cancelada.")
                        confirm_popup.destroy()  # Cierra el pop-up sin eliminar

                # Botón Confirmar
                ctk.CTkButton(btn_frame, text="Confirmar", width=120, height=36, corner_radius=18, fg_color="#f86a20", hover_color="#cd5618", text_color="white", font=("Open Sans", 13, "bold"), command=confirm_action).pack(side="left", padx=10)

                # Botón Cancelar
                ctk.CTkButton(btn_frame, text="Cancelar", width=120, height=36, corner_radius=18, fg_color="#f86a20", hover_color="#cd5618", text_color="white", font=("Open Sans", 13, "bold"), command=confirm_popup.destroy).pack(side="right", padx=10)

            try:
                if kind == "sales" or kind == "providers":
                    p_col_index = f'#{titles.index('productos')+1}'
                elif kind == "clients":
                    p_col_index = f'#{titles.index('compras')+1}'
            except:
                p_col_index = None

            # Creación de la tablita visualizadora de opciones
            tree = ttk.Treeview(self.searchbar_frame, show="headings")

            #instanciamos JUSTO después del tree para que se vean bien las cosas
            filter_btn.configure(command = lambda:header_filter(filter_btn, titles, tree))
            if kind == "sales":
                date_btn.configure(command = lambda: date_cb(date_btn, tree))
            apply_filters(tree)
            # empaquetamos el tree
            tree.pack(fill="both", expand=True)
            tree["columns"] = titles
            for col in titles:
                tree.heading(col, text=col)
                tree.column(col, width=800 // len(titles), anchor="w")

            # actualizador al escribir
            def search_change(var_name=None, index=None, mode=None):
                apply_filters(tree)

            # se añade el actualizador cada vez que se escribe
            try:
                search_var.trace_add('write', search_change)
            except Exception:
                pass

            #se traza el click si está en el treeview
            def tree_click(event):
                x, y = event.x, event.y
                e_row = tree.identify_row(y)
                e_col = tree.identify_column(x)
                r_line = item_map.get(e_row, None)
                if not e_row:
                    return
                if not r_line:
                    return

                if kind== "sales" or kind == "providers" or kind == "clients":
                    if e_col == p_col_index:
                        return  show_list(root, r_line)
                return  row_menu(tree, event, r_line, e_row)
            tree.bind("<ButtonRelease-1>", tree_click)

            def edit_event(line):
                try:
                    if kind == "products":
                        prod_id = getattr(line, "product_id", None)
                        if prod_id:
                            self.close_searchbar()
                            self.view_edit_product(prod_id)
                        else:
                            mbox.showerror("Error", "No se encontró product_id en este registro.")
                    elif kind == "providers":
                        pid = getattr(line, "provider_id", None)
                        if pid:
                            self.close_searchbar()
                            self.view_edit_provider(pid)
                        else:
                            mbox.showerror("Error", "No se encontró provider_id en este registro.")
                    elif kind == "collaborators":
                        cid = getattr(line, "collab_id", None)
                        if cid:
                            self.close_searchbar()
                            self.view_edit_collab(cid)
                        else:
                            mbox.showerror("Error", "No se encontró collab_id en este registro.")
                    elif kind == "clients":
                        clid = getattr(line, "client_id", None)
                        if clid:
                            self.close_searchbar()
                            self.view_edit_client(clid)
                        else:
                            mbox.showerror("Error", "No se encontró client_id en este registro.")
                    elif kind == "sales":
                        sid = getattr(line, "sale_id", None)
                        if sid:
                            self.close_searchbar()
                            self.view_edit_sale(sid)
                        else:
                            mbox.showerror("Error", "No se encontró sale_id en este registro.")
                    else:
                        mbox.showwarning("Editar", f"No hay formulario de edición implementado para: {kind}")
                except Exception as e:
                    mbox.showerror("Error", f"No se pudo abrir el editor: {e}")

            #Menú adicional en caso sea venta, proveedor o producto
            def row_menu(origin, event, line, row):
                menu = tk.Menu(tree, tearoff=0)
                menu.add_command(label="editar", command = lambda l=line: edit_event(l))
                menu.add_command(label="eliminar", command = lambda l=line, iid=row: del_event(l, tree, iid))
                menu.post(event.x_root, event.y_root)

            def show_list(origin, r_line):
                # Creamos y configuramos el TopLevel
                top = tk.Toplevel(origin)
                top.geometry("300x220")
                top.transient(origin)
                top.grab_set()
                top.configure(bg = "white")
                top.title("Lista asociada")
                top.update_idletasks()

                #Configuramos las dimensiones del TopLevel y lo colocamos en medio de la pantallita
                w = 350
                h = 250
                root_x = origin.winfo_rootx()
                root_y = origin.winfo_rooty()
                root_w = origin.winfo_width()
                root_h = origin.winfo_height()
                x = root_x + (root_w // 2) - (w // 2)
                y = root_y + (root_h // 2) - (h // 2)
                top.geometry(f"{w}x{h}+{x}+{y}")

                #Creamos un frame y le añadimos tanto una scrollbar como una listbox
                list_frame = ttk.Frame(top)
                list_frame.pack(side="top", expand = True, fill = "both", padx = 5, pady = (10, 5))
                scrollbar = ttk.Scrollbar(list_frame, orient = "vertical")
                lbox = tk.Listbox(list_frame, yscrollcommand=scrollbar.set, activestyle = "none", exportselection = False, bg="white", font=("Open Sans", 12))
                scrollbar.config(command=lbox.yview)
                scrollbar.pack(side="right", fill="y")
                lbox.pack(side="left", fill="x", expand=True)

                # Si son Ventas, entonces se trabaja de la siguiente forma:
                if kind == "sales":
                    #Se obtiene el diccionario de productos en la venta
                    p_dict = getattr(r_line, "products", "{}")
                    if not p_dict:
                        lbox.insert("end", "Venta sin productos.")
                    else:
                        #Se obtiene info de los productos en el diccionario principal y se mapean como id: nombre
                        prod_list = self.db_info.get("products", [])
                        prod_look = {prod.product_id: prod.name for prod in prod_list}

                        for prod_id, sale_info in p_dict.items():
                            qty = sale_info.get("quantity", "?")
                            subtotal = sale_info.get("subtotal", 0.0)
                            #Se obtiene el nombre del producto del diccionario id:valor
                            prod_name = prod_look.get(prod_id, prod_id)

                            line_text = f"{prod_name} | Cant: {qty} | Subtotal: Q{subtotal:.2f}"
                            lbox.insert("end", line_text)

                #Si son proveedores, se trabajan de la siguiente manera:
                if kind == "providers":
                    # Ordena los productos relacionados con el proveedor
                    r_line.prod_ordering()
                    # Obtiene esos mismos productos
                    p_in = getattr(r_line, "products", [])
                    prod_list = self.db_info.get("products", [])  # Obtiene la lista de productos de la DB
                    prod_look = {prod.product_id: prod.name for prod in prod_list}  # Mapeo ID : nombre
                    if p_in:
                        for val in p_in:
                            prod_name = prod_look.get(val, val)  # Usa nombre si existe, sino el ID
                            lbox.insert("end", prod_name)
                    else:
                        lbox.insert("end", "No hay productos asociados.")

                #Si son clientes, lo trabajan así:
                if kind == "clients":
                    #Se ordenan las IDs relacionadas de las ventas
                    r_line.sale_sorter()
                    p_in = getattr(r_line, "sales", False)
                    if p_in and p_in is not False:
                        #Se obtienen todos los productos de la database si su ID está dentro de la lista de ventas relacionadas
                        r_prods = [prod for prod in self.db_info["sales"] if prod.sale_id in p_in]
                        s_list = []
                        for val in p_in:
                            for p in r_prods:
                                if p.sale_id == val:
                                    #Se generaN tuplas de dos valores (id de la venta y el total de esta)
                                    sale = [p.sale_id, p.total]
                                    s_list.append(sale)
                        for val in s_list:
                            #Se añaden toditas las ventas a la lista
                            lbox.insert("end", " | ".join(val))
                    else:
                        lbox.insert("end", "No hay compras asociadas")
                ctk.CTkButton(top, text = "Cerrar", command = top.destroy, width=100,  height=36, corner_radius=18, fg_color="white", text_color="black", font=("Open Sans", 13, "bold")).pack(pady = (5, 10))
                top.lift()
                top.focus_force()