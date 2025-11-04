import customtkinter as ctk
import tkinter.messagebox as mbox
from tkinter import ttk
import tkinter as tk
from main import get_conn, User, Admin, Collaborator, Provider, Client , Product, Sales, id_generate
import datetime
from datetime import date
DB_NAME = "bawiz.db"
classes = {"users": User, "admins": Admin, "collaborators": Collaborator, "providers": Provider, "clients": Client, "sales": Sales, "products": Product}


class CollabUI(ctk.CTkFrame):
    def __init__(self, master, current_user=None):
        super().__init__(master, fg_color="white")
        self.master = master
        self.pack(expand=True, fill="both")
        self.db_info = self.db_extract(classes)
        self.searchbar_frame = None

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

    def logout(self):
        confirm = mbox.askyesno("Cerrar sesión", "¿Deseas cerrar tu sesión actual?")
        if confirm:
            from login import LoginUI
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
            cols = {"sales": ["sale_id", "time", "client", "products", "total"], "products": ["product_id", "name", "type", "description", "sale_price", "stock"], "clients": ["client_id", "name", "phone", "sale_price", "stock"], "collaborators": ["collab_id", "name", "phone", "position"], "providers":["provider_id", "name", "phone", "products"]}
            titles_dict = {"sales": ["ID", "hora", "cliente asociado", "productos", "total"], "products": ["ID", "Nombre", "Tipo", "Descripción", "Precio", "Stock"], "clients": ["ID", "Nombre", "Teléfono", "precio venta", "Stock"], "collaborators": ["ID", "Nombre", "Teléfono", "Posición"], "providers":["ID", "Nombre", "Teléfono", "Productos"]}
            headers = cols[kind]
            titles = titles_dict[kind]
            #Los junta en un dict que funcione como "ID": "sale_id", "hora":"time"... para que, al momento de mostrar filtros, se mire en español y afecte los filtros en inglés (como están en la db)
            main_headers = dict(zip(titles, headers))
            reverse_headers = dict(zip(headers, titles))
            #extrae los datos de la db_info
            table_data = self.db_info[kind]
            # define la fecha de hoy
            today = date.today()

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
                print("header_selected: ", header_selected)
                #texto ingresado en el buscador
                search_text = ""
                try:
                    search_text = search_var.get().strip()
                    print("search_text: ", search_text)
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
                    print("result: ", result)
                # filtrar por fecha (si aplica)
                date_vals = today
                if date_vals and date_vals.year and date_vals.month and date_vals.day:
                    try:
                        fy, fm, fd = int(date_vals.year), int(date_vals.month), int(date_vals.day)
                        filtered = []
                        for obj in result:
                            r=getattr(obj, "date", None)
                            if r and r.year == fy and r.month == fm and r.day == fd:
                                filtered.append(obj)
                        result = filtered
                    except Exception:
                        pass
                for idx, item in enumerate(result):
                    all_vals = [str(getattr(item, t, "")) for t in headers]

                    #revisar si es "sales" o "providers" para poner la sección de "vista"
                    try:
                        title_idx = headers.index("products")
                        if kind == "sales":
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
            self.searchbar_frame = ctk.CTkFrame(root, corner_radius=12)
            self.searchbar_frame.pack(fill="both", expand=True, padx=8, pady=8)

            controls = ctk.CTkFrame(self.searchbar_frame,  fg_color="transparent")
            controls.pack(fill="x", padx=8, pady=(4,8))

            filter_btn = ctk.CTkButton(controls, width = 150, text = "Filtrar", height = 10, corner_radius=18, fg_color="white", hover_color="#f2f2f2", text_color="black", font=("Open Sans", 13, "bold"))
            filter_btn.pack(side="left", padx=6)
            search_var = ctk.StringVar()
            search_btn = ctk.CTkEntry(controls, placeholder_text="Buscar...",textvariable = search_var, width=400, height=36, corner_radius=18, fg_color="white", placeholder_text_color="grey", font=("Open Sans", 13, "bold"))
            search_btn.pack(side="left", padx=6)
            back_btn = ctk.CTkButton(controls, text="Cerrar",command = self.searchbar_frame.destroy, width=100, height=10, corner_radius=18,fg_color="white", hover_color="#f2f2f2", text_color="black", font=("Open Sans", 13, "bold"))
            back_btn.pack(side="right", padx=6)

            print("search_var initial:", repr(search_var.get()))
            def header_filter(filter_button, options,origin_tree, initial = None, width = 150):
                old = getattr(self, "_current_popup", None)
                if old is not None and old.winfo_exists():
                    try:
                        old.destroy()
                    except Exception:
                        pass
                existing = getattr(filter_button, "options_popup", None)
                if existing is not None and existing.winfo_exists():
                    try: existing.lift()
                    except Exception:
                        try: existing.destroy()
                        except: pass

                # Configuración del topLevel pa que parezca un combobox
                popup = ctk.CTkToplevel(filter_button.winfo_toplevel())
                filter_button.options_popup = popup
                popup.wm_overrideredirect(True)
                popup.transient(filter_button.winfo_toplevel())
                popup.attributes("-topmost", True)
                popup.update_idletasks()
                popup.deiconify()
                popup.lift()

                print(getattr(filter_btn, "options_popup", None))

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
                print("cbox_var initial:", repr(getattr(cbox, 'get', lambda: None)()))

                # Aplica el filtro obtenido. Si no funciona,
                def apply(value = None):
                    val =  value if value else cbox.get()

                    filter_button.filter_value = val
                    print("val is: ",val)
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
            try:
                p_col_index = f'#{titles.index('productos')+1}'
            except:
                p_col_index = None
            # Creación de la tablita visualizadora de opciones
            tree = ttk.Treeview(self.searchbar_frame, show="headings")

            #instanciamos JUSTO después del tree para que se vean bien las cosas
            filter_btn.configure(command = lambda:header_filter(filter_btn, titles, tree))
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