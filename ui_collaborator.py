import customtkinter as ctk
import tkinter.messagebox as mbox
from main import Client, get_conn, id_generate
from tkinter import messagebox as mbox
import tkinter as tk
import json
from datetime import datetime

class CollabUI(ctk.CTkFrame):
    def __init__(self, master, current_user=None):
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

        # Mensaje de bienvenida
        self.current_user = current_user
        if self.current_user:
            name = self.current_user.get("name", "Usuario")
            phone = self.current_user.get("phone", "Sin teléfono")
        else:
            name= "Usuario"
            phone ="Sin teléfono"

        msg = f"Bienvenido, {name}\nTeléfono: {phone}"
        welcome_label = ctk.CTkLabel(self.body,text=msg,font=("Open Sans", 28, "bold"),text_color="#111111",justify="center")
        welcome_label.pack(expand=True)

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
            mbox.showinfo(f"Colaborador creado", f"Cliente '{name}' creado y guardado")
            self._close_fullscreen_view() # cierra la ventana cuando se crea
        except Exception as e:
            mbox.showerror("Error", f"Error inesperado: {e}")

    def action(self, msg):
        if self.active_submenu:
            self.active_submenu.destroy()
            self.active_submenu = None

        match msg:
            case "Agregar cliente":
                self.view_create_client()
            case "Agregar venta":
                self.view_create_sale()

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

    def logout(self):
        confirm = mbox.askyesno("Cerrar sesión", "¿Deseas cerrar tu sesión actual?")
        if confirm:
            from login import LoginUI
            self.pack_forget()
            LoginUI(self.master)