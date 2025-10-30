import json
import sqlite3
import random
import datetime
from datetime import datetime, date
from typing import Optional, Dict, Any, List

DB_NAME = "bawiz.db"


def id_generate(id_type):
    val1 = str(random.randint(1, 999))
    val2 = str(random.randint(1, 999))
    new_id = False
    if id_type.lower() == "usr":
        new_id = "USR" + val1 + val2
    elif id_type.lower() == "adm":
        new_id = "ADM" + val1 + val2
    elif id_type.lower() == "col":
        new_id = "COL" + val1 + val2
    elif id_type.lower() == "prv":
        new_id = "PRV" + val1 + val2
    elif id_type.lower() == "clt":
        new_id = "CLT" + val1 + val2
    elif id_type.lower() == "prd":
        new_id = "PRD" + val1 + val2
    elif id_type.lower() == "vnt":
        new_id = "VNT" + val1 + val2
    return new_id


def get_conn():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


class DataBase:

    @staticmethod
    def create_tables():
        with get_conn() as conn:
            conn.executescript("""
            CREATE TABLE IF NOT EXISTS users (
                user_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                phone REAL NOT NULL
            );

            CREATE TABLE IF NOT EXISTS admins (
                admin_id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                position TEXT NOT NULL,
                type TEXT DEFAULT 'admin',
                FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS collaborators (
                collab_id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                position TEXT NOT NULL,
                type TEXT DEFAULT 'collaborator',
                FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS clients (
                client_id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                sales TEXT NOT NULL,
                type TEXT DEFAULT 'client',
                FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS products (
                product_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                type TEXT DEFAULT 'product',
                providers TEXT NOT NULL,
                description TEXT NOT NULL,
                raw_price REAL NOT NULL,
                sale_price REAL NOT NULL,
                stock INTEGER NOT NULL
            );
            
            CREATE TABLE IF NOT EXISTS providers (
                provider_id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                products TEXT NOT NULL,
                type TEXT DEFAULT 'provider',
                FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
            );
            
            CREATE TABLE IF NOT EXISTS sales (
                sale_id TEXT PRIMARY KEY,
                client_id TEXT NOT NULL,
                date TEXT NOT NULL,
                time TEXT NOT NULL, 
                products TEXT NOT NULL,
                total REAL NOT NULL,
                FOREIGN KEY (client_id) REFERENCES clients(client_id)
            );
            
            """)

class User:
    def __init__(self, name: str, phone: int, user_id=None):
        self.__user_id = user_id or id_generate("usr")
        self._name = name
        self._phone = phone

    @property
    def user_id(self):
        return self.__user_id

    @user_id.setter
    def user_id(self, new_id):
        pass

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        if len(name) == 0 or not name.isalpha():
            raise ValueError("El nombre debe ser solo letras")
        self._name = name

    @property
    def phone(self):
        return self._phone
    @phone.setter
    def phone(self,phone):
        if len(phone) != 8:
            raise ValueError("El número telefónico es inválido")
        self._phone = phone

    def mostrar_datos(self):
        pass

    def save(self):
        with get_conn() as c:
            existing = c.execute("SELECT user_id FROM users WHERE user_id = ?", (self.user_id,)).fetchone()
            if existing:
                c.execute("UPDATE users SET name=?, phone=? WHERE user_id=?", (self.name, self.phone, self.user_id))
            else:
                c.execute("INSERT INTO users (user_id, name, phone) VALUES (?, ?, ?)",
                          (self.user_id, self.name, self.phone))
            c.commit()

    @staticmethod
    def load(user_id: str) -> Optional["User"]:
        with get_conn() as c:
            r = c.execute("SELECT * FROM users WHERE user_id = ?", (user_id,)).fetchone()
            if r:
                return User(r["name"], r["phone"], user_id=r["user_id"])
            return None


class Admin(User):
    def __init__(self, name: str, phone: int, position: str, user_id=None, admin_id: str = None):
        self.__admin_id = admin_id or id_generate("adm")
        self.__position = position
        self.type = "admin"
        User.__init__(self, name, phone, user_id)

    @property
    def admin_id(self):
        return self.__admin_id

    @admin_id.setter
    def admin_id(self, new_id):
        pass

    @property
    def position(self):
        return self.__position

    @position.setter
    def position(self, new_position):
        pass

    def products(self, root):
        pass
    def sales(self, root):
        pass
    def clients(self, root):
        pass
    def collaborators(self, root):
        pass
    def providers(self, root):
        pass
    def show_sales(self, root):
        pass

    def save(self):
        with get_conn() as c:
            super().save()
            existing = c.execute("SELECT admin_id FROM admins WHERE admin_id = ?", (self.admin_id,)).fetchone()
            if existing:
                c.execute("UPDATE admins SET user_id = ?, position = ?, type = ? WHERE admin_id = ?",
                          (self.user_id, self.position, self.type))
            else:
                c.execute("INSERT INTO admins (admin_id, user_id, position, type) VALUES (?,? , ?, ?)",
                          (self.admin_id,self.user_id, self.position, self.type))
            c.commit()

    @staticmethod
    def load(admin_id: str) -> Optional["Admin"]:
        with get_conn() as c:
            r = c.execute("SELECT * FROM admins WHERE admin_id = ?", (admin_id,)).fetchone()
            if r:
                user = User.load(r["user_id"])
                return Admin(name=user.name, phone=user.phone, position=r["position"], user_id=user.user_id)
            return None


class Collaborator(User):
    def __init__(self, name: str, phone: int, position: str, user_id: str = None, collab_id: str = None):
        self.__collab_id = collab_id or id_generate("col")
        self.position = position
        self.type = "collaborator"
        User.__init__(self, name, phone, user_id)
    @property
    def collab_id(self):
        return self.__collab_id
    @collab_id.setter
    def collab_id(self,new_id):
        pass
    def mostrar_datos(self):
        pass

    def sales(self, root):
        pass
    def clients(self, root):
        pass
    def show_sales(self, root):
        pass

    def save(self):
        with get_conn() as c:
            super().save()
            existing = c.execute("SELECT collab_id FROM collaborators WHERE collab_id = ?", (self.collab_id,)).fetchone()
            if existing:
                c.execute("UPDATE collaborators SET user_id = ?, position = ?, type = ? WHERE collab_id = ?",(self.user_id, self.position, self.type, self.collab_id))
            else:
                c.execute("INSERT INTO collaborators (collab_id, user_id, position, type) VALUES (?,?,?,?)",(self.collab_id, self.user_id, self.position, self.type))
            c.commit()
    @staticmethod
    def load(collab_id:str) ->Optional["Collaborator"]:
        with get_conn() as c:
            r = c.execute("SELECT * FROM collaborators WHERE collab_id = ?", (collab_id,)).fetchone()
            if r:
                user = User.load(r["user_id"])
                return Collaborator(name = user.name, phone = user.phone, user_id = user.user_id, position = r["position"])
            return None
    def delete(self):
        with get_conn() as c:
            c.execute("DELETE FROM sales WHERE sales_id = ?",(self.collab_id,))
            c.commit()

class Provider(User):
    def __init__(self, name:str, phone:int,products : List[str] = None,user_id:str = None, provider_id:str = None):
        self.__provider_id = provider_id or id_generate("prd")
        self.products : List[str] = products or []
        self.type = "provider"
        User.__init__(self, name, phone, user_id)
    @property
    def provider_id(self):
        return self.__provider_id
    @provider_id.setter
    def provider_id(self,new_id):
        pass
    def mostrar_datos(self):
        pass

    def add_product(self, product):
        if product not in self.products:
            self.products.append(product)
        else:
            raise ValueError("El producto ya está en la lista")

    def del_product(self, product):
        if product in self.products:
            self.products.remove(product)
        else:
            raise ValueError("El producto no fué encontrado")

    def save(self):
        products = "|".join(self.products)
        with get_conn() as c:
            exists = c.execute("SELECT provider_id FROM providers WHERE provider_id = ?", (self.provider_id,)).fetchone()
            if exists:
                c.execute("UPDATE providers SET products = ? WHERE provider_id = ?",(products,self.provider_id))
            else:
                c.execute("INSERT INTO providers (provider_id, products) VALUES (?,?)",(self.provider_id,products))
            c.commit()

    @staticmethod
    def load(provider_id:str) ->Optional["Provider"]:
        with get_conn() as c:
            r = c.execute("SELECT * FROM providers WHERE provider_id = ?", (provider_id,)).fetchone()
            if r:
                user = User.load(r["provider_id"])
                products = r["products"].split("|")
                return Provider(name = user.name, phone = user.phone, user_id = user.user_id, provider_id = provider_id, products = products)
            return None
    def delete(self):
        with get_conn() as c:
            c.execute("DELETE FROM sales WHERE sales_id = ?",(self.provider_id,))
            c.commit()

class Client(User):
    def __init__(self, name:str, phone:int,user_id:str = None, client_id:str = None, sales: List[str] = None):
        self.__client_id = client_id or id_generate("clt")
        self.sales : List[str] = sales or []
        self.type = "client"
        User.__init__(self, name, phone, user_id)
    @property
    def client_id(self):
        return self.__client_id
    @client_id.setter
    def client_id(self,new_id):
        pass
    def mostrar_datos(self):
        pass
    def add_sale(self, sale):
        if sale not in self.sales:
            self.sales.append(sale)
        else:
            raise ValueError("La venta ya está en la lista")
    def del_sale(self, sale):
        if sale in self.sales:
            self.sales.remove(sale)
        else:
            raise ValueError("La venta no está en la lista")
    def save(self):
        super().save() # guarda el usuario en la tabla users primero
        new_sales = "|".join(self.sales)
        with get_conn() as c:
            exists = c.execute("SELECT client_id FROM clients WHERE client_id = ?", (self.client_id,)).fetchone()
            if exists:
                c.execute("UPDATE clients SET sales = ?, type = ? WHERE client_id = ?", (new_sales, self.type, self.client_id))
            else:
                c.execute("INSERT INTO clients (client_id, user_id, sales, type) VALUES (?,?,?,?)",(self.client_id,self.user_id, new_sales, self.type))
            c.commit()

    @staticmethod
    def load(client_id:str) -> Optional["Client"]:
        with get_conn() as c:
            r = c.execute("SELECT * FROM clients WHERE client_id = ?", (client_id,)).fetchone()
            if r:
                user = User.load(r["client_id"])
                sales = r["sales"].split("|")
                return Client(name = user.name, phone = user.phone, client_id = r["client_id"], sales = sales)
            return None
    def delete(self):
        with get_conn() as c:
            c.execute("DELETE FROM sales WHERE sales_id = ?",(self.client_id,))
            c.commit()


class Product:
    def __init__(self, name:str, types:str,  desc:str, raw_p:float, sale_p:float,stock:int,providers: Optional[List[str]] = None,prod_id:str = None):
        self.__product_id = prod_id or id_generate("prd")
        self.__name = name
        self._type = types
        self.providers : List[str] = providers or []
        self.description = desc
        self._raw_p = raw_p
        self._sale_p = sale_p
        self.stock = stock

    @property
    def product_id(self):
        return self.__product_id
    @product_id.setter
    def product_id(self,new_id):
        pass
    @property
    def name(self):
        return self.__name
    @name.setter
    def name(self,new_name):
        pass
    @property
    def type(self):
        return self._type
    @type.setter
    def type(self,new_type):
        if len(new_type) == 0:
            raise ValueError("El tipo debe ser solo letras")
        self._type = new_type

    @property
    def raw_p(self):
        return self._raw_p
    @raw_p.setter
    def raw_p(self,new_p):
        if not new_p.isdigit():
            raise ValueError("Debe ingresar un número")
        if new_p < 0 or new_p > self._sale_p:
            raise ValueError("El valor debe ser mayor a 0 y menor al precio de venta")
        self._raw_p = new_p
    @property
    def sale_p(self):
        return self._sale_p
    @sale_p.setter
    def sale_p(self,new_p):
        if not new_p.isdigit():
            raise ValueError("Debe ingresar un número")
        if new_p < 0 or new_p < self._raw_p:
            raise ValueError("El valor debe ser mayor a 0 y al precio de compra")
        self._sale_p = new_p
    def add_provider(self,provider):
        if provider not in self.providers:
            self.providers.append(provider)
        else:
            raise ValueError("El proveedor ya está en la lista")

    def del_provider(self,provider):
        if provider in self.providers:
            self.providers.remove(provider)
        else:
            raise ValueError("Este producto no tiene a ese proveedor")
    def save(self):
        providers = "|".join(self.providers)
        with get_conn() as c:
            exists = c.execute("SELECT product_id FROM products WHERE product_id = ?", (self.product_id,)).fetchone()
            if exists:
                c.execute("UPDATE products SET name = ?, type = ?, providers = ?, description = ?, raw_price = ?, sale_price = ?, stock = ?", (self.name, self.type, providers, self.description, self.raw_p, self.sale_p, self.stock))
            else:
                c.execute("INSERT INTO products (name, type, providers, description, raw_price, sale_price, stock) VALUES (?,?,?,?,?,?,?)",(self.name, self.type, providers, self.description, self.raw_p, self.sale_p, self.stock))
            c.commit()

    @staticmethod
    def load(product_id:str) -> Optional["Product"]:
        with get_conn() as c:
            r = c.execute("SELECT * FROM products WHERE product_id = ?", (product_id,)).fetchone()
            if r:
                providers = r["providers"].split("|")
                return Product(name = r["name"], types = r["type"], desc = r["description"], raw_p = r["raw_price"], sale_p = r["sale_price"], stock = r["stock"],providers = providers)
            return None

    def delete(self):
        with get_conn() as c:
            c.execute("DELETE FROM sales WHERE sales_id = ?",(self.product_id,))
            c.commit()


class Sales:
    def __init__(self,client_id:str, products: Optional[Dict[str, Dict[str, Any]]] = None, sale_id = None, total:int = None, date_:str = None, time_:str = None):
        self.__sale_id = sale_id or id_generate("sal")
        self.__date = datetime.strptime(date_, "%d/%m/%Y").date() or date.today().strftime("%d/%m/%Y")
        self.__time = datetime.strptime(time_, "%H:%M").time() or datetime.now().strftime("%H:%M")
        self._client_id = client_id
        self.products : Dict[str, Dict[str, Any]] = products or {}
        self.total = total
    @property
    def sale_id(self):
        return self.__sale_id
    @sale_id.setter
    def sale_id(self,new_id):
        pass
    @property
    def date(self):
        return self.__date
    @date.setter
    def date(self,new_date):
        pass
    @property
    def time(self):
        return self.__time
    @time.setter
    def time(self,new_time):
        pass

    def save(self):
        with get_conn() as c:
            prod_json = json.dumps(self.products, ensure_ascii=False)
            exists = c.execute("SELECT 1 FROM sales WHERE sale_id = ?", self.sale_id).fetchone()
            if exists:
                c.execute("UPDATE sales SET client_id = ?,date = ?, time = ?, products = ?, total = ? WHERE sale_id = ?",(self._client_id, self.date, self.time, prod_json, self.total, self.sale_id))
            else:
                c.execute("INSERT INTO sales (sale_id, date, time, client_id, products, total) VALUES(?, ?, ?, ?, ?, ?)",(self.sale_id,self.date, self.time, self._client_id, prod_json, self.total))
            c.commit()
    @staticmethod
    def load(sale_id:str) -> Optional["Sales"]:
        with get_conn() as c:
            r = c.execute("SELECT * FROM sales WHERE sale_id = ?", sale_id).fetchone()
            if r:
                prods = {}
                if r["products"]:
                    try:
                        prods = json.loads(r["products"])
                    except json.JSONDecodeError:
                        prods = {}
                return Sales(client_id=r["client_id"], products=prods, sale_id=r["sale_id"], total = r["total"], date_ = r["date"], time_ = r["time"])
            else:
                return None

    def delete(self):
        with get_conn() as c:
            c.execute("DELETE FROM sales WHERE sales_id = ?",(self.sale_id,))
            c.commit()