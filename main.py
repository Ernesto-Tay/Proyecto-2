import json
import sqlite3
import random
import datetime
from datetime import datetime, date
from typing import Optional, Dict, Any, List

DB_NAME = "bawiz.db"

# Se crea un generador de ID aleatorio (tipo de valor + número aleatorio del 0 al 999 999)
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

# Se inicia la conexión
def get_conn():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

# Se crea la base de datos
class DataBase:
    #*Todos los hijos de "User" tienen "ON DELETE CASCADE" para eliminar su instancia de user si se elimina la instancia principal
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
# Clase padre (de usuarios) User
class User:
    def __init__(self, name: str, phone: int, user_id=None):
        self.__user_id = user_id or id_generate("usr")
        self._name = name
        self._phone = phone

    #Getters y setters de cada sistema
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
        name = name.strip()
        if len(name) == 0 or not all(ch.isalpha() or ch.isspace() for ch in name): # Valida que no esté vacío y que solo tenga letras o espacios
            raise ValueError("El nombre solo puede contener letras y espacios")
        self._name = name

    @property
    def phone(self):
        return self._phone
    @phone.setter
    def phone(self,phone):
        if len(phone) != 8:
            raise ValueError("El número telefónico es inválido")
        self._phone = phone

    # Méthod de guardado
    def save(self):
        with get_conn() as c:
            existing = c.execute("SELECT user_id FROM users WHERE user_id = ?", (self.user_id,)).fetchone()
            if existing:
                c.execute("UPDATE users SET name=?, phone=? WHERE user_id=?", (self.name, self.phone, self.user_id))
            else:
                c.execute("INSERT INTO users (user_id, name, phone) VALUES (?, ?, ?)",
                          (self.user_id, self.name, self.phone))
            c.commit()

    # Méthod de carga (estático para que pueda llamarse desde el principio)
    @staticmethod
    def load(user_id: str) -> Optional["User"]:
        with get_conn() as c:
            r = c.execute("SELECT * FROM users WHERE user_id = ?", (user_id,)).fetchone()
            print("toy acá y r es: ",r)
            if r:
                return User(r["name"], r["phone"], user_id=r["user_id"])
            return None
    def delete(self):
        with get_conn() as c:
            cursor = c.cursor()
            cursor.execute("DELETE FROM users WHERE user_id = ?", (self.user_id,))
            c.commit()

# Clase tipo admin
class Admin(User):
    def __init__(self, name: str, phone: int, position: str, user_id=None, admin_id: str = None):
        self.__admin_id = admin_id or id_generate("adm")
        self.__position = position
        self.type = "admin"
        User.__init__(self, name, phone, user_id)

    #Getter y setter de los sistemas privados
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

    #Méthodo para guardar en la db
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

        #Méthodo estático de carga
    @staticmethod
    def load(admin_id: str) -> Optional["Admin"]:
        with get_conn() as c:
            #debe crear una instancia de User antes de crear una de Admin
            r = c.execute("SELECT * FROM admins WHERE admin_id = ?", (admin_id,)).fetchone()
            if r:
                user = User.load(r["user_id"])
                if user:
                    return Admin(name=user.name, phone=user.phone, position=r["position"], user_id=user.user_id)
            return None

# Clase de Colaboradores (subordinados de Admin)
class Collaborator(User):
    def __init__(self, name: str, phone: int, position: str, user_id: str = None, collab_id: str = None):
        self.__collab_id = collab_id or id_generate("col")
        self.position = position
        self.type = "collaborator"
        User.__init__(self, name, phone, user_id)

    #Getter y setter de la ID
    @property
    def collab_id(self):
        return self.__collab_id
    @collab_id.setter
    def collab_id(self,new_id):
        pass

    #methodo de guardado
    def save(self):
        with get_conn() as c:
            super().save()
            existing = c.execute("SELECT collab_id FROM collaborators WHERE collab_id = ?", (self.collab_id,)).fetchone()
            if existing:
                c.execute("UPDATE collaborators SET user_id = ?, position = ?, type = ? WHERE collab_id = ?",(self.user_id, self.position, self.type, self.collab_id))
            else:
                c.execute("INSERT INTO collaborators (collab_id, user_id, position, type) VALUES (?,?,?,?)",(self.collab_id, self.user_id, self.position, self.type))
            c.commit()
    #Méthodo de carga (llamable al momento de crear una instancia que está en la db)
    @staticmethod
    def load(collab_id:str) ->Optional["Collaborator"]:
        with get_conn() as c:
            r = c.execute("SELECT * FROM collaborators WHERE collab_id = ?", (collab_id,)).fetchone()
            if r:
                user = User.load(r["user_id"])
                if user:
                    return Collaborator(name = user.name, phone = user.phone, user_id = user.user_id, position = r["position"], collab_id=r["collab_id"])
            return None
    #Méthodo de eliminación
    def delete(self):
        with get_conn() as c:
            cursor = c.cursor()
            cursor.execute("DELETE FROM users WHERE user_id = ?", (self.user_id,))
            c.commit()

#Clase de proveedores
class Provider(User):
    def __init__(self, name:str, phone:int,products : List[str] = None,user_id:str = None, provider_id:str = None):
        self.__provider_id = provider_id or id_generate("prv")
        self.products : List[str] = products or []
        self.type = "provider"
        User.__init__(self, name, phone, user_id)
    @property
    def provider_id(self):
        return self.__provider_id
    @provider_id.setter
    def provider_id(self,new_id):
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

    #Méhod de ordenamiento de los productos (selection sort)
    def prod_ordering(self):
        for i in range(len(self.products)):
            min_index = i
            for j in range(i + 1, len(self.products)):
                if self.products[j] < self.products[min_index]:
                    min_index = j
            self.products[i], self.products[min_index] = self.products[min_index], self.products[i]

    # Méthodo de guardado en la db
    def save(self):
        super().save()
        products = ""
        if self.products:
            products = "|".join(self.products)
        if not self.__provider_id:
            self.__provider_id = id_generate("prv")

        with get_conn() as c:
            exists = c.execute("SELECT provider_id FROM providers WHERE provider_id = ?",(self.provider_id,)).fetchone()
            if exists:
                c.execute("UPDATE providers SET user_id = ?, products = ?, type = ? WHERE provider_id = ?",(self.user_id, products, self.type, self.provider_id))
            else:
                c.execute("INSERT INTO providers (provider_id, user_id, products, type) VALUES (?, ?, ?, ?)",(self.provider_id, self.user_id, products, self.type))

            c.commit()

    # Méthodo de carga
    @staticmethod
    def load(provider_id:str) ->Optional["Provider"]:
        with get_conn() as c:
            r = c.execute("SELECT * FROM providers WHERE provider_id = ?", (provider_id,)).fetchone()
            if r:
                user = User.load(r["user_id"])
                if user:
                    products = r["products"].split("|")
                    return Provider(name = user.name, phone = user.phone, user_id = user.user_id, provider_id = provider_id, products = products)
            return None
    # Méthodo de eliminación de la db
    def delete(self):
        with get_conn() as c:
            cursor = c.cursor()
            cursor.execute("DELETE FROM users WHERE user_id = ?",(self.user_id,))
            c.commit()

# Clase de clientes
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
    # Ordenar la lista por medio de bubble sort
    def sale_sorter(self):
        for i in range(len(self.sales) - 1):
            for j in range(len(self.sales) - 1 - i):
                if self.sales[j] > self.sales[j + 1]:
                    self.sales[j], self.sales[j + 1] = self.sales[j + 1], self.sales[j]

    #Méthodo de guardado
    def save(self):
        super().save() # guarda el usuario en la tabla users primero
        new_sales = ""
        if self.sales:
            new_sales = "|".join(self.sales)

        if not self.__client_id:
            self.__client_id = id_generate("clt")
        with get_conn() as c:
            exists = c.execute("SELECT client_id FROM clients WHERE client_id = ?", (self.client_id,)).fetchone()
            if exists:
                c.execute("UPDATE clients SET sales = ?, type = ? WHERE client_id = ?", (new_sales, self.type, self.client_id))
            else:
                c.execute("INSERT INTO clients (client_id, user_id, sales, type) VALUES (?,?,?,?)",(self.client_id,self.user_id, new_sales, self.type))
            c.commit()

    #Méthodo de carga
    @staticmethod
    def load(client_id:str) -> Optional["Client"]:
        with get_conn() as c:
            r = c.execute("SELECT * FROM clients WHERE client_id = ?", (client_id,)).fetchone()
            if r:
                user = User.load(r["user_id"])
                if user:
                    sales = r["sales"].split("|")
                    return Client(name = user.name, phone = user.phone, client_id = r["client_id"], sales = sales, user_id = user.user_id)
            return None
    #Méthodo de eliminación
    def delete(self):
        with get_conn() as c:
            cursor = c.cursor()
            cursor.execute("DELETE FROM users WHERE user_id = ?",(self.user_id,))
            c.commit()
    # Clase de productos
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

    #getters y setters de los productos
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

    #Sistemas para actualizar los precios
    @property
    def raw_p(self):
        return self._raw_p

    @raw_p.setter
    def raw_p(self, new_p):
        try:
            value = float(new_p)
        except (TypeError, ValueError):
            raise ValueError("Debe ingresar un número")
        if value <= 0:
            raise ValueError("El precio de costo debe ser mayor que 0")
        if hasattr(self, "_sale_p") and value > self._sale_p:
            raise ValueError("El costo no puede ser mayor que el precio de venta")
        self._raw_p = value

    @property
    def sale_p(self):
        return self._sale_p

    @sale_p.setter
    def sale_p(self, new_p):
        try:
            value = float(new_p)
        except (TypeError, ValueError):
            raise ValueError("Debe ingresar un número")
        if value <= 0:
            raise ValueError("El precio de venta debe ser mayor que 0")
        if hasattr(self, "_raw_p") and value < self._raw_p:
            raise ValueError("El precio de venta debe ser mayor que el costo")
        self._sale_p = value
    #Méthodo para añadir proveedores (si no están en la lista)
    def add_provider(self,provider):
        if provider not in self.providers:
            self.providers.append(provider)
        else:
            raise ValueError("El proveedor ya está en la lista")
    #Méthodo para eliminar proveedores (de estar en la lista)
    def del_provider(self,provider):
        if provider in self.providers:
            self.providers.remove(provider)
        else:
            raise ValueError("Este producto no tiene a ese proveedor")


    # Ordenamiento por bubble sort
    def sale_sorter(self):
        for i in range(len(self.providers) - 1):
            for j in range(len(self.providers) - 1 - i):
                if self.providers[j] > self.providers[j + 1]:
                    self.providers[j], self.providers[j + 1] = self.providers[j + 1], self.providers[j]

    #Búsqueda binaria para buscar proveedores
    def binary_search(self, prov):
        inicio = 0
        fin = len(self.providers) - 1
        while inicio <= fin:
            medio = (inicio + fin) // 2
            if self.providers[medio] == prov:
                return medio
            elif self.providers[medio] < prov:
                inicio = medio + 1
            else:
                fin = medio - 1
        return None


    #Guardado en la db
    def save(self):
        providers = "|".join(str(p) for p in self.providers if p)
        with get_conn() as c:
            exists = c.execute("SELECT product_id FROM products WHERE product_id = ?",(self.product_id,)).fetchone()
            if exists:
                c.execute("""UPDATE products SET name = ?, type = ?, providers = ?, description = ?, raw_price = ?, sale_price = ?, stock = ?WHERE product_id = ?""", (self.name,self.type,providers,self.description,self.raw_p,self.sale_p,self.stock,self.product_id))
            else:
                c.execute("""INSERT INTO products (product_id, name, type, providers, description, raw_price, sale_price, stock)VALUES (?, ?, ?, ?, ?, ?, ?, ?)""", (self.product_id,self.name,self.type,providers,self.description,self.raw_p,self.sale_p,self.stock))
            c.commit()

    #Carga de la DB
    @staticmethod
    def load(product_id:str) -> Optional["Product"]:
        with get_conn() as c:
            r = c.execute("SELECT * FROM products WHERE product_id = ?", (product_id,)).fetchone()
            if r:
                providers = r["providers"].split("|")
                return Product(prod_id = r["product_id"], name = r["name"], types = r["type"], desc = r["description"], raw_p = r["raw_price"], sale_p = r["sale_price"], stock = r["stock"],providers = providers)
            return None
    #Eliminación (si amerita)
    def delete(self):
        with get_conn() as c:
            cursor = c.cursor()
            cursor.execute("DELETE FROM products WHERE product_id = ?",(self.__product_id,))
            c.commit()

# Clase de ventas
class Sales:
    def __init__(self,client_id:str, products: Optional[Dict[str, Dict[str, Any]]] = None, sale_id = None, total:int = None, date_:str = None, time_:str = None):
        self.__sale_id = sale_id or id_generate("sal")
        self.__date = datetime.strptime(date_, "%d/%m/%Y").date() or date.today().strftime("%d/%m/%Y")
        self.__time = datetime.strptime(time_, "%H:%M:%S").time() if time_ else datetime.now().time()
        self._client_id = client_id
        self.products : Dict[str, Dict[str, Any]] = products or {}
        self.total = total

    #Getters y setters de los atributos privados
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

    # Convertir el diccionario a lista y pasarlo por quick_sort (funciona con valores dinámicos)
    def convert(self, order_val):
        if order_val not in ['cuantity','subtotal']:
            return
        p_list = list(self.products.items())
        new_list = self.sort(p_list, order_val)
        new_dict = dict(new_list)
        self.products = new_dict

    def sort(self,order_list, order_val):
        if len(order_list) <= 1:
            return order_list
        pivot = order_list[len(order_list)//2]
        bigger = [val for val in order_list if val[order_val] > pivot[order_val]]
        middle = [val for val in order_list if val[order_val] == pivot[order_val]]
        smaller = [val for val in order_list if val[order_val] < pivot[order_val]]
        return self.sort(smaller, order_val) + middle + self.sort(bigger, order_val)

    #Guardado en la DB
    def save(self):
        with get_conn() as c:
            prod_json = json.dumps(self.products, ensure_ascii=False)
            exists = c.execute("SELECT 1 FROM sales WHERE sale_id = ?", self.sale_id).fetchone()
            if exists:
                c.execute("UPDATE sales SET client_id = ?,date = ?, time = ?, products = ?, total = ? WHERE sale_id = ?",(self._client_id, self.date, self.time, prod_json, self.total, self.sale_id))
            else:
                c.execute("INSERT INTO sales (sale_id, date, time, client_id, products, total) VALUES(?, ?, ?, ?, ?, ?)",(self.sale_id,self.date, self.time, self._client_id, prod_json, self.total))
            c.commit()

    #Carga en la DB
    @staticmethod
    def load(sale_id:str) -> Optional["Sales"]:
        with get_conn() as c:
            r = c.execute("SELECT * FROM sales WHERE sale_id = ?", (sale_id,)).fetchone()
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

    #Eliminación en la DB
    def delete(self):
        with get_conn() as c:
            cursor = c.cursor()
            cursor.execute("DELETE FROM sales WHERE sale_id = ?",(self.__sale_id,))
            c.commit()