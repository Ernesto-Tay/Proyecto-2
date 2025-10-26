import customtkinter as ctk
from main import get_conn
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import calendar

DB_NAME = "bawiz.db"

class AdminUI(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="white")
        self.master = master
        self.pack(expand=True, fill="both")
        self.create_header()

    def create_header(self):
        header = ctk.CTkFrame(self, fg_color="#e0e0e0", height=60, corner_radius=0)
        header.pack(side="top", fill="x")

        # frame izquierdo
        left = ctk.CTkFrame(header, fg_color="transparent")
        left.pack(side="left", padx=15, pady=10)

        btn_colab = ctk.CTkButton(left, text="Colaboradores", width=130, height=36, corner_radius=18, fg_color="white",hover_color="#f2f2f2", text_color="black", font=("Open Sans", 13, "bold"))
        btn_colab.pack(side="left", padx=6)

        btn_sales = ctk.CTkButton(left, text="Ventas", width=130, height=36, corner_radius=18, fg_color="white",hover_color="#f2f2f2", text_color="black", font=("Open Sans", 13, "bold"))
        btn_sales.pack(side="left", padx=6)

        btn_products = ctk.CTkButton(left, text="Productos", width=130, height=36, corner_radius=18, fg_color="white",hover_color="#f2f2f2", text_color="black", font=("Open Sans", 13, "bold"))
        btn_products.pack(side="left", padx=6)

        btn_clients = ctk.CTkButton(left, text="Clientes", width=130, height=36, corner_radius=18, fg_color="white",hover_color="#f2f2f2", text_color="black", font=("Open Sans", 13, "bold"))
        btn_clients.pack(side="left", padx=6)

        # frame derecho
        right = ctk.CTkFrame(header, fg_color="transparent")
        right.pack(side="right", padx=15, pady=10)

        btn_logout = ctk.CTkButton(right, text="Cerrar Sesión", width=130, height=36, corner_radius=18, fg_color="white",hover_color="#f2f2f2", text_color="black", font=("Open Sans", 13, "bold"))
        btn_logout.pack(side="right", padx=6)

    def db_extract(self, kind):
        with get_conn as c:
            cur = c.cursor()
            cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=? LIMIT 1;", (kind,))
            if not cur.fetchone():
                return None



    def menu_visualizer(self, root, kind):
        """
        Toma en cuenta lo siguiente:
        1. crea instancias de clase del tipo de objeto que estás manejando para acceder bien fácil a sus datos, y luego actualizarlos en caso aplique
        2. Crea la función de cada botoncito para que jale bien y se muestren las cosas como tal
        3.
        """
        with get_conn() as c:

            #extrae la información de una tabla en la base de datos, buscándola con el nombre "kind" (argumento ingresado)
            cur = c.cursor()
            cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name= ? LIMIT = 1;", (kind,))
            if not cur.fetchone():
                return None

            # Inicializadores: "cols" es para las referencias en la tabla, "titles_dict" es para los títulos de las columnas
            cols = {"sales": ["sale_id", "time", "client", "products", "total"], "products": ["product_id", "name", "type", "description", "sale_price", "stock"], "clients": ["client_id", "name", "phone", "sale_price", "stock"], "collaborators": ["collab_id", "name", "phone", "position"], "providers":["provider_id", "name", "phone", "products"]}
            titles_dict = {"sales": ["ID", "hora", "cliente asociado", "productos", "total"], "products": ["ID", "Nombre", "Tipo", "Descripción", "Precio", "Stock"], "clients": ["ID", "Nombre", "Teléfono", "precio venta", "Stock"], "collaborators": ["ID", "Nombre", "Teléfono", "Posición"], "providers":["ID", "Nombre", "Teléfono", "Productos asociados"]}
            headers = cols[kind]
            titles = titles_dict[kind]

            # Aquí se guarda la info de los meses, años y días para los filtros de fecha si se miran las "ventas"
            months = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
            years = [str(y) for y in range (2025, 2030)]
            date_pop = False

            #Creación de la tablita visualizadora de opciones
            tree = ttk.Treeview(root, show="headings")
            tree.pack(fill = "both", expand = True)
            tree["columns"] = headers
            for col in headers:
                tree.heading(col, text=col)
                tree.column(col, width= 800 // len(headers))

            # toma todas las instancias de la tabla
            cur.execute(f"SELECT * FROM {kind}")
            for row in cur.fetchall():
                tree.insert("", "end", values=row)

            # crea el frame y el espacio para los botoncitos
            frame = ctk.CTkFrame(root, relief="ridge", corner_radius=12)
            frame.pack(fill="both", expand=True, padx=8, pady=8)

            controls = ctk.CTkFrame(frame, relief="ridge", fg_color="transparent")
            controls.pack(fill="x", padx=8, pady=(4,8))

            # inicializa los botoncitos para evitar error de llamada
            filter_btn = False
            date_btn = False
            search_btn = False
            back_btn = False

            if kind == "sales":
                # Organiza los botoncitos específicamente para las ventas
                filter_btn = ctk.CTkButton(controls, text = "Filtrar", width = 100, height = 36,  corner_radius=18, fg_color="white",hover_color="#f2f2f2", text_color="black", font=("Open Sans", 13, "bold"))
                filter_btn.pack(side="left", padx=6)
                date_btn = ctk.CTkButton(controls, text = "Fecha", width = 100, height = 36, corner_radius=18, fg_color="white",hover_color="#f2f2f2", text_color="black", font=("Open Sans", 13, "bold"))
                date_btn.pack(side="left", padx=6)
                search_btn = ctk.CTkEntry(controls, text = "Buscar...", width = 400, height = 36, corner_radius = 18, fg_color = "white", text_color = "grey", font=("Open Sans", 13, "bold"))
                search_btn.pack(side="left", padx=6)
                back_btn = ctk.CTkButton(controls, text = "Volver", width = 100, height = 36 , corner_radius=18, fg_color="white",hover_color="#f2f2f2", text_color="black", font=("Open Sans", 13, "bold"))
                back_btn.pack(side="right", padx=6)
            else:
                # si es otro modo (proveedores, productos...), pone la configuración normal
                filter_btn = ctk.CTkButton(controls, text="Filtrar", width=200, height=36, corner_radius=18, fg_color="white", hover_color="#f2f2f2", text_color="black", font=("Open Sans", 13, "bold"))
                filter_btn.pack(side="left", padx=6)
                search_btn = ctk.CTkEntry(controls, text="Buscar...", width=400, height=36, corner_radius=18, fg_color="white", text_color="grey", font=("Open Sans", 13, "bold"))
                search_btn.pack(side="left", padx=6)
                back_btn = ctk.CTkButton(controls, text="Volver", width=100, height=36, corner_radius=18,fg_color="white", hover_color="#f2f2f2", text_color="black", font=("Open Sans", 13, "bold"))
                back_btn.pack(side="right", padx=6)

            # esta es la configuración del filtro de fecha
            def date_cb(date_button, callback = None, first_values = None):
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
                date_pop = tk.Toplevel(root)
                root.date_pop = date_pop
                date_pop.wm_overrideredirect(True)
                date_pop.transient(root)
                date_pop.attributes("-topmost", True)

                # colocarlo debajo del botoncito de acción
                ax = date_button.winfo_rootx()
                ay = date_button.winfo_rooty() + date_button.winfo_height()
                date_pop.geometry(f"+{ax}+{ay}")

                # configuramos el contenedor interno para que quede chulo
                popup_frame = ctk.CTkFrame(date_pop, relief="ridge", corner_radius=12, fg_color = "white")
                popup_frame.pack(padx=4, pady=4)

                # le colocamos título
                title = ctk.CTkLabel(popup_frame, relief="ridge", fg_color="white")
                title.pack(anchor = "w", pady = (0, 4))

                selects = ctk.CTkFrame(popup_frame, relief="ridge", fg_color="transparent")
                selects.pack(anchor = "w", pady = (0, 4))

                # combobox año
                cb_year = ctk.CTkComboBox(selects, values=years, width=100, height=18, fg_color="white")
                cb_year.pack(anchor = "left", pady = (0, 4))
                # combobox mes
                cb_month = ctk.CTkComboBox(selects, values=months, width=100, height=18, fg_color="white")
                cb_month.pack(anchor = "left", pady = (0, 4))
                # combobox día (varía con el mes, por eso empieza vacío)
                cb_day = ctk.CTkComboBox(selects, values = [], width=100, height=18, fg_color="white")
                cb_day.pack(anchor = "left", pady = (0, 4))

                # Si hay valore iniciales (first_values), los establecemos
                if first_values:
                    if first_values.get("month") in months:
                        cb_month.set(first_values.get("month"))
                    if first_values.get("year") in years:
                        cb_year.set(first_values.get("year"))
                    if first_values.get("day"):
                        cb_day.set(first_values.get("day"))

                # Actualizador de días según mes y año (considerando biciestos)
                def day_upd(event = None):
                    s_month= cb_month.get()
                    if s_month not in months:
                        cb_day.configure(values = [])
                        cb_day.set("día")
                        return

                    # Obtener año
                    try:
                        s_year = int(cb_year.get())
                    except Exception:
                        s_year = 2025
                    month_n = months.index(s_month) + 1
                    n_days = calendar.monthrange(s_year, month_n)[1]
                    days =[f"{d:02d}" for d in range(n_days+1)]
                    cb_day.configure(values = days)
                    cur_day = cb_day.get()
                    if cur_day not in days:
                        cb_day.set(days[0])
                cb_month.bind("<<ComboboxSelected>>", day_upd)
                cb_year.bind("<<ComboboxSelected>>", day_upd)

                #botones para aplicar o cancelar
                btns =ctk.CTkFrame(popup_frame, relief="ridge", fg_color="transparent")
                btns.pack(fill ="x", pady = (4, 0))

                def on_apply():
                    vals = {"year": cb_year.get(), "month": cb_month.get(), "day": cb_day.get()}
                    # convertir mes a número para consultas y filtrado con datetime
                    if vals["month"] in months:
                        vals["month_num"] = f"{months.index(vals['month'])+1:02d}"
                    else:
                        vals["month_num"] = ""

                    if callback:
                        try:
                            callback(vals)
                        except Exception as e:
                            print(f"Error en callback: {e}")

                    # destruir el popup y eliminar la referencia
                    try:
                        date_pop.destroy()
                    except Exception:
                        pass
                    try:
                        delattr(root, "date_pop")
                    except Exception:
                        pass

                def on_cancel():
                    try:
                        date_pop.destroy()
                    except Exception:
                        pass
                    try:
                        delattr(root, "date_pop")
                    except Exception:
                        pass

                ct_apply = ctk.CTkButton(btns, relief="ridge", fg_color="transparent")
                ct_cancel = ctk.CTkButton(btns, relief="ridge", fg_color="white")
                ct_apply.pack(side="right", padx=(0, 6))
                ct_cancel.pack(side="right", padx=(6, 0))

                # cerrar la barrita de opciones cuando se clickee afuera
                def outside_click(event):
                    x, y = event.x_root, event.y_root
                    px = date_pop.winfo_rootx()
                    py = date_pop.winfo_rooty()
                    pw = date_pop.winfo_width()
                    ph = date_pop.winfo_height()
                    if not (px <= x <=px + pw and py <= y <=py + ph):
                        on_cancel()
                        root.unbind_all("<Button-1>")

                root.bind_all("<Button-1>", outside_click, add ="+")
                date_pop.focus_force()
                day_upd()

            return