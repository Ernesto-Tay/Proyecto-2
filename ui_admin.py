import customtkinter as ctk
import tkinter.messagebox as mbox
from main import get_conn, User, Admin, Collaborator, Provider, Client , Product, Sales, id_generate
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import calendar

DB_NAME = "bawiz.db"
classes = {"users": User, "admins": Admin, "collaborators": Collaborator, "providers": Provider, "clients": Client, "sales": Sales, "products": Product}

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
        self.searchbar_frame = None
        # inicialización
        self.create_header()
        self.db_info = self.db_extract(classes)
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

        match msg:
            case "Agregar colaborador":
                self.view_create_collab()
            case "Agregar cliente":
                self.view_create_client()
            case "Agregar productos":
                self.view_create_product()
            case "Ver colaboradores":
                self.menu_visualizer(self.master, "collaborators", self.searchbar_frame)
            case "Ver clientes":
                self.menu_visualizer(self.master, "clients",self.searchbar_frame)
            case "Ver productos":
                self.menu_visualizer(self.master, "products",self.searchbar_frame)


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
            mbox.showerror("Error numerico","Deben de ingresar numeros")
            return

        try:
            product = Product(name=name,types=type_,desc=desc,raw_p=raw_price,sale_p=sale_price,stock=stock)
            product.save()
            mbox.showinfo(f"Producto", f"Producto '{name}' creado")
            self._close_fullscreen_view()
        except Exception as e:
            mbox.showerror("Error", f"Error inesperado: {e}")

    def logout(self):
        confirm = mbox.askyesno("Cerrar sesión", "¿Deseas cerrar tu sesión actual?")
        if confirm:
            from login import LoginUI
            self.searchbar_frame.destroy() if self.searchbar_frame else None
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

                # Obtener filas
                cur.execute(f"SELECT * FROM {table}")
                rows = cur.fetchall()

                # crear objetos con las filas para usar sus funciones y no complicarnos la vida
                the_class = ref_classes.get(table)
                objects = []
                for row in rows:
                    # Revisar como extrae la info, no creo que esté bien
                    row_dict = dict(zip(cols, row))
                    kind_id = row_dict[cols[0]]
                    obj = the_class.load(kind_id)
                    if obj is not None:
                        objects.append(obj)
                out[table] = objects
            return out

    def entry_upd(self, entry_var, *args):
        return entry_var.get()

    def menu_visualizer(self, root, kind, frame):
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
            cols = {"sales": ["sale_id", "time", "client", "products", "total"], "products": ["product_id", "name", "type", "description", "sale_price", "stock"], "clients": ["client_id", "name", "phone", "sale_price", "stock"], "collaborators": ["collab_id", "name", "phone", "position"], "providers":["provider_id", "name", "phone", "products"]}
            titles_dict = {"sales": ["ID", "hora", "cliente asociado", "productos", "total"], "products": ["ID", "Nombre", "Tipo", "Descripción", "Precio", "Stock"], "clients": ["ID", "Nombre", "Teléfono", "precio venta", "Stock"], "collaborators": ["ID", "Nombre", "Teléfono", "Posición"], "providers":["ID", "Nombre", "Teléfono", "Productos"]}
            headers = cols[kind]
            titles = titles_dict[kind]
            #Los junta en un dict que funcione como "ID": "sale_id", "hora":"time"... para que, al momento de mostrar filtros, se mire en español y afecte los filtros en inglés (como están en la db)
            main_headers = dict(zip(titles, headers))
            #extrae los datos de la db_info
            table_data = self.db_info[kind]
            #copia los datos para alterar la lista copiada
            upd_db = table_data.copy()

            # Aquí se guarda la info de los meses, años y días para los filtros de fecha si se miran las "ventas"
            months = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
            years = [str(y) for y in range (2025, 2030)]
            date_pop = False

            item_map = {}
            def apply_filters(tree):

                base = upd_db
                result = base[:]

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
                        result = [obj for obj in result if s in str(getattr(obj, header_attr, "").lower())]
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
                if date_vals and date_vals.get("year") and date_vals.get("month_num") and date_vals.get("day"):
                    try:
                        fy, fm, fd = int(date_vals["year"]), int(date_vals["month_num"]), int(date_vals["day"])
                        filtered = []
                        for obj in result:
                            r=getattr(obj, "date", None)
                            if r and r.year == fy and r.month == fm and r.day == fd:
                                filtered.append(obj)
                        result = filtered
                    except Exception:
                        pass

                # reiniciar el treeview con los datos filtrados
                for chld in tree.get_children():
                    tree.delete(chld)
                item_map.clear()
                for idx, item in enumerate(result):
                    all_vals = [getattr(item, t, "") for t in headers]

                    #revisar si es "sales" o "providers" para poner la sección de "vista"
                    try:
                        title_idx = headers.index("products")
                        if kind in ("sales", "providers"):
                            all_vals[title_idx] = "Ver ▾"
                    except ValueError:
                        prod_idx = None

                    # Añadir al tree_insert y al trace_map
                    iid = f"r{idx}"
                    tree.insert("", "end", iid=iid, values=all_vals)
                    item_map[iid] = item

            # crea el frame y el espacio para los botoncitos
            if frame is not None:
                frame.destroy()
            frame_2 = ctk.CTkFrame(frame, corner_radius=12)
            frame_2.pack(fill="both", expand=True, padx=8, pady=8)

            controls = ctk.CTkFrame(frame_2,  fg_color="transparent")
            controls.pack(fill="x", padx=8, pady=(4,8))

            # inicializa los botoncitos para evitar error de llamada
            filter_btn = False
            date_btn = False
            search_btn = False
            back_btn = False

            if kind == "sales":
                # Organiza los botoncitos específicamente para las ventas
                filter_btn = ctk.CTkLabel(controls, text="Filtrar", width = 150, height = 10, corner_radius=18, fg_color="transparent", text_color="black", font=("Open Sans", 13, "bold"))
                filter_btn.pack(side="left", padx=6)
                date_btn = ctk.CTkLabel(controls, text = "Fecha", width = 150, height = 10, corner_radius=18, fg_color="transparent", text_color="black", font=("Open Sans", 13, "bold"))
                date_btn.pack(side="left", padx=6)
                search_var = ctk.StringVar()
                search_btn = ctk.CTkEntry(controls, placeholder_text = "Buscar...",textvariable = search_var, width = 400, height = 36, corner_radius = 18, fg_color = "white", placeholder_text_color = "grey", font=("Open Sans", 13, "bold"))
                search_btn.pack(side="left", padx=6)
                back_btn = ctk.CTkButton(controls, text = "Cerrar",command = frame_2.destroy, width = 100, height = 36 , corner_radius=18, fg_color="white",hover_color="#f2f2f2", text_color="black", font=("Open Sans", 13, "bold"))
                back_btn.pack(side="right", padx=6)
            else:
                # si es otro modo (proveedores, productos...), pone la configuración normal
                filter_btn = ctk.CTkLabel(controls, width = 150, text = "Filtrar", height = 10, corner_radius=18, fg_color="transparent", text_color="black", font=("Open Sans", 13, "bold"))
                filter_btn.pack(side="left", padx=6)
                search_var = ctk.StringVar()
                search_btn = ctk.CTkEntry(controls, placeholder_text="Buscar...",textvariable = search_var, width=400, height=36, corner_radius=18, fg_color="white", placeholder_text_color="grey", font=("Open Sans", 13, "bold"))
                search_btn.pack(side="left", padx=6)
                back_btn = ctk.CTkButton(controls, text="Cerrar",command = frame_2.destroy, width=100, height=10, corner_radius=18,fg_color="white", hover_color="#f2f2f2", text_color="black", font=("Open Sans", 13, "bold"))
                back_btn.pack(side="right", padx=6)


            def header_filter(filter_button, options,origin_tree, initial = None, width = 150):
                existing = getattr(filter_button, "options_popup", None)
                if existing is not None and existing.winfo_exists():
                    try: existing.lift()
                    except Exception:
                        try: existing.destroy()
                        except: pass

                # Configuración del topLevel pa que parezca un combobox
                popup = tk.Toplevel(filter_button.winfo_toplevel())
                popup.wm_overrideredirect(True)
                popup.transient(filter_button.winfo_toplevel())
                popup.attributes("-topmost", True)

                # poner debajo del botoncito
                ax = filter_button.winfo_rootx()
                ay = filter_button.winfo_rooty() + filter_button.winfo_height()
                popup.geometry(f"+{ax}+{ay}")

                # Contenedor
                bframe = ctk.CTkFrame(popup,corner_radius = 8, fg_color="transparent")
                bframe.pack(padx = 4, pady = 4)

                # Creación de la combobox y colocar su valor inicial
                cbox = ctk.CTkComboBox(frame_2, values = options, width = width, height=36, corner_radius=18, fg_color="white", text_color="black", font=("Open Sans", 13, "bold"))
                if initial and initial in options:
                    cbox.set(initial)
                elif options:
                    cbox.set(options[0])
                cbox.pack(anchor = "w", pady = (0, 4))

                # Aplica el filtro obtenido. Si no funciona,
                def apply():
                    val = cbox.get()
                    filter_button.filter_value = val
                    try:
                        popup.destroy()
                    except Exception as e:
                        print("error en la función: ",e)
                    apply_filters(origin_tree)

                cbox.bind("<Return>", apply)

                def offclick(event):
                    #obtener coordenadas del "evento"
                    x, y = event.x_root, event.y_root
                    #obtener coordenadas y dimensiones del toplevel del combobox
                    if popup.winfo_exists():
                        px, py = popup.winfo_rootx(), popup.winfo_rooty()
                        pw, ph = popup.winfo_width(), popup.winfo_height()
                        b_id = getattr(event, "click_bind_id", None)

                        if not (px <= x <= px + pw and py <= y <= py + ph):
                            try: popup.destroy()
                            except: pass
                            try:
                                delattr(filter_button, "options_popup")
                            except: pass
                            try: root.unbind_all("<Button-1>", b_id)
                            except Exception: pass

                root.bind_all("<Button-1>", offclick, add = "+")
                popup.focus_force()
                return

            # esta es la configuración del filtro de fecha
            def date_cb(date_button, origin_tree, first_values = None):
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
                date_pop = tk.Toplevel(date_button.winfo_toplevel())
                date_button.date_pop = date_pop
                date_pop.wm_overrideredirect(True)
                date_pop.transient(date_button.winfo_toplevel())
                date_pop.attributes("-topmost", True)

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
                cb_year.pack(anchor = "left", pady = (0, 4))
                # combobox mes
                cb_month = ctk.CTkComboBox(selects, values=months, width=100,  height=36, corner_radius=18, fg_color="white", text_color="black", font=("Open Sans", 13, "bold"))
                cb_month.pack(anchor = "left", pady = (0, 4))
                # combobox día (varía con el mes, por eso empieza vacío)
                cb_day = ctk.CTkComboBox(selects, values = [], width=100,  height=36, corner_radius=18, fg_color="white", text_color="black", font=("Open Sans", 13, "bold"))
                cb_day.pack(anchor = "left", pady = (0, 4))

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
                    if s_month in months and s_year:
                        n_month = months.index(s_month) + 1
                        n_days = calendar.monthrange(s_year, n_month)[1]
                        days = [f"{d:02d}" for d in range(n_days)]
                        cb_day.configure(values = days)
                        cur_day = cb_day.get()
                        if cur_day not in days:
                            cb_day.set(days[0])
                    # si no, los días quedan vacíos
                    else:
                        cb_day.configure(values=[])
                        cb_day.set("")
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
                    date_apply()

                cb_year.configure(command= lambda _: date_change("year"))
                cb_month.configure(command = lambda _: date_change("month"))
                cb_day.configure(command = lambda _: date_change("day"))

                # cierra el toplevel si se hace click afuera del toplevel
                def click_outside(event):
                    x, y= event.x_root, event.y_root
                    if popup_frame.winfo_exists():
                        px, py =popup_frame.winfo_rootx(), popup_frame.winfo_rooty()
                        pw, ph = popup_frame.winfo_width(), popup_frame.winfo_height()
                        e_id = getattr(event, "click_bind_id", None)
                        if not (px <= x <= px + pw and py <= y <= py + ph):
                            try: popup_frame.destroy()
                            except Exception: pass
                            try:delattr(date_button, "options_popup")
                            except Exception: pass
                            try: root.unbind_all("<Button-1>", e_id)
                            except Exception: pass

                root.bind_all("<Button-1>", click_outside, add = "+")
                popup_frame.focus_force()
                upd_date()
                return
            try:
                p_col_index = f'#{titles.index('productos')+1}'
            except:
                p_col_index = None

            # Creación de la tablita visualizadora de opciones
            tree = ttk.Treeview(frame_2, show="headings")

            #instanciamos JUSTO después del tree para que se vean bien las cosas
            header_filter(filter_btn, titles, tree)
            if kind == "sales":
                date_cb(date_btn, tree)
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

            def tree_click(event):
                x, y = event.x, event.y
                e_row = tree.identify_row(y)
                e_col=tree.identify_column(x)
                r_line = item_map.get(e_row, None)
                if not e_row:
                    return
                inst = item_map.get(e_row, None)
                if not r_line:
                    return

                if kind== "sales" or kind == "providers":
                    if e_col == p_col_index:
                        return  show_list(root, r_line)
                return  row_menu(tree, event, r_line, e_row)
            tree.bind("<Button-1>", tree_click)

            def row_menu(origin, event, line, row):
                menu = tk.Menu(tree, tearoff=0)
                menu.add_command(label="editar") #command = lambda l=line: edit_event(l) -> comando para mostrar la ventana de "editar"
                menu.add_command(label="eliminar") #command = lambda l=line, iid=row: del_event(l) -> comando para el popup de eliminación
                menu.post(event.x_root, event.y_root)

            def show_list(origin, r_line):
                top = tk.Toplevel(origin)
                top.geometry("300x220")
                list_frame = ttk.Frame(top)
                list_frame.pack(side="top", expand = True, padx = 5, pady = 5)
                scrollbar = ttk.Scrollbar(list_frame, orient = "vertical")
                lbox = tk.Listbox(list_frame, yscrollcommand=scrollbar.set, activestyle = "none", exportselection = False)
                scrollbar.config(command=lbox.yview)
                scrollbar.pack(side="right", fill="y")
                lbox.pack(side="left", fill="x", expand=True)

                if kind == "sales":
                    p_in = getattr(r_line, "products", False)
                    if p_in is not False:
                        for key, p in p_in:
                            entrance = {
                                "v1" : key,
                                "v2" : p["subtotal"],
                            }
                            lbox.insert("end", " | ".join(entrance.values()))

                if kind == "providers":
                    p_in = getattr(r_line, "products", False)
                    if p_in is not False:
                        for val in p_in:
                            lbox.insert("end", val)
                ctk.CTkButton(top, text = "Cerrar", command = top.destroy(), width=100,  height=36, corner_radius=18, fg_color="white", text_color="black", font=("Open Sans", 13, "bold"))