import customtkinter as ctk
from main import get_conn
from tkinter import ttk, messagebox, filedialog
from login import logout_login

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

            def get_hearders(table_name):
                cur.execute(f"PRAGMA table_info('{table_name}')")
                return [r[1] for r in cur.fetchall()]

            headers = get_hearders(kind)
            if headers is None:
                return None
            tree = ttk.Treeview(root, show="headings")
            tree.pack(fill = "both", expand = True)
            tree["columns"] = headers
            for col in headers:
                tree.heading(col, text=col)
                tree.column(col, width= 800 // len(headers))

            cur.execute(f"SELECT * FROM {kind}")
            for row in cur.fetchall():
                tree.insert("", "end", values=row)


            return