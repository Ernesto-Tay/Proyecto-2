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

    def menu_visualizer(self, root, kind):
        with get_conn() as c:
            cur = c.cursor()
            cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name= ? LIMIT = 1;", (kind,))
            if not cur.fetchone():
                return None

            cols = {"sales": ["sale_id", "time", "client", "products", "total"], "products": ["product_id", "name", "type", "description", "sale_price", "stock"], "clients": ["client_id", "name", "phone", "sale_price", "stock"], "collaborators": ["collab_id", "name", "phone", "position"], "providers":["provider_id", "name", "phone", "products"]}
            titles_dict = {"sales": ["ID", "hora", "cliente asociado", "productos", "total"], "products": ["ID", "Nombre", "Tipo", "Descripción", "Precio", "Stock"], "clients": ["ID", "Nombre", "Teléfono", "precio venta", "Stock"], "collaborators": ["ID", "Nombre", "Teléfono", "Posición"], "providers":["ID", "Nombre", "Teléfono", "Productos asociados"]}
            headers = cols[kind]
            titles = titles_dict[kind]

            months = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
            years = [str(y) for y in range (2025, 2030)]
            date_pop = False

            tree = ttk.Treeview(root, show="headings")
            tree.pack(fill = "both", expand = True)
            tree["columns"] = headers
            for col in headers:
                tree.heading(col, text=col)
                tree.column(col, width= 800 // len(headers))

            cur.execute(f"SELECT * FROM {kind}")
            for row in cur.fetchall():
                tree.insert("", "end", values=row)

            frame = ctk.CTkFrame(root, relief="ridge", corner_radius=12)
            frame.pack(fill="both", expand=True, padx=8, pady=8)

            controls = ctk.CTkFrame(frame, relief="ridge", fg_color="transparent")
            controls.pack(fill="x", padx=8, pady=(4,8))

            filter_btn = False
            date_btn = False
            search_btn = False
            back_btn = False

            if kind == "sales":
                filter_btn = ctk.CTkButton(controls, text = "Filtrar", width = 100, height = 36,  corner_radius=18, fg_color="white",hover_color="#f2f2f2", text_color="black", font=("Open Sans", 13, "bold"))
                filter_btn.pack(side="left", padx=6)

                date_btn = ctk.CTkButton(controls, text = "Fecha", width = 100, height = 36, corner_radius=18, fg_color="white",hover_color="#f2f2f2", text_color="black", font=("Open Sans", 13, "bold"))
                date_btn.pack(side="left", padx=6)

                search_btn = ctk.CTkEntry(controls, text = "Buscar...", width = 400, height = 36, corner_radius = 18, fg_color = "white", text_color = "grey", font=("Open Sans", 13, "bold"))
                search_btn.pack(side="left", padx=6)

                back_btn = ctk.CTkButton(controls, text = "Volver", width = 100, height = 36 , corner_radius=18, fg_color="white",hover_color="#f2f2f2", text_color="black", font=("Open Sans", 13, "bold"))
                back_btn.pack(side="right", padx=6)

            else:
                filter_btn = ctk.CTkButton(controls, text="Filtrar", width=200, height=36, corner_radius=18,
                                           fg_color="white", hover_color="#f2f2f2", text_color="black",
                                           font=("Open Sans", 13, "bold"))
                filter_btn.pack(side="left", padx=6)

                search_btn = ctk.CTkEntry(controls, text="Buscar...", width=400, height=36, corner_radius=18,
                                          fg_color="white", text_color="grey", font=("Open Sans", 13, "bold"))
                search_btn.pack(side="left", padx=6)

                back_btn = ctk.CTkButton(controls, text="Volver", width=100, height=36, corner_radius=18,
                                         fg_color="white", hover_color="#f2f2f2", text_color="black",
                                         font=("Open Sans", 13, "bold"))
                back_btn.pack(side="right", padx=6)

            def date_cb(date_button, callback = None, first_values = None):
                col_cb = ctk.CTkComboBox(controls,values = titles, fg_color="transparent", width=100, button_color=("white","#f2f2f2"), text_color="black", font=("Open Sans", 12))
                col_cb.set(headers[0])
                col_cb.pack(side="left", padx=10, pady=10)

                if date_pop and tk.Toplevel.winfo_exists(date_pop):
                    try:
                        date_pop.lift()
                        return
                    except Exception:
                        pass

                date_pop = tk.Toplevel(root)
                date_pop.wm_overrideredirect(True)
                date_pop.transient(root)
                date_pop.attributes("-topmost", True)





            return