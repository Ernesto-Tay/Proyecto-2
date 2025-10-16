import tkinter as tk
from tkinter import ttk
import sqlite3
import random
from typing import Optional

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

class DataBase:
    @staticmethod
    def _conn():
        conn = sqlite3.connect(DB_NAME)
        conn.row_factory = sqlite3.Row
        return conn

    @staticmethod
    def create_tables():
        with DataBase._conn() as conn:
            conn.executescript(""""+
            CREATE TABLE IF NOT EXISTS users (
                id_user TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                phone REAL NOT NULL,
                type TEXT NOT NULL,
            );
            
            CREATE TABLE IF NOT EXISTS clients (
                id_client TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                phone REAL NOT NULL,
                sales TEXT NOT NULL,
                type TEXT DEFAULT 'client',
            );
            
            CREATE TABLE IF NOT EXISTS products (
                id_product TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                type TEXT DEFAULT 'product',
                description TEXT NOT NULL,
                raw_price REAL NOT NULL,
                sale_price REAL NOT NULL,
                stock INTEGER NOT NULL,
            );
            
            CREATE TABLE IF NOT EXISTS providers (
                id_provider TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                phone TEXT NOT NULL,
                products TEXT NOT NULL,
                type TEXT DEFAULT 'provider',
            );
            
            CREATE TABLE IF NOT EXISTS sales (
                id_sale TEXT PRIMARY KEY,
                id_client TEXT,
                total REAL,
                FOREIGN KEY (id_client) REFERENCES clients(id_client)
            );
            
            """)

class User:
    def __init__(self, name:str, phone:int ,user_id = None):
        self.__id = user_id or id_generate("usr")
        self._name = name
        self._phone = phone

    @property
    def id(self):
        return self.__id
    @id.setter
    def id(self,new_id):
        pass
    @property
    def name(self):
        return self._name
    @name.setter
    def name(self,name):
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
    def guardar(self):
        pass


class Admin(User):
    def __init__(self, name:str, phone:int, position:str,user_id=None, admin_id:str = None):
        self.__admin_id = admin_id or id_generate("adm")
        self.__position = position
        self.type = "admin"
        User.__init__(self, name, phone, user_id)
    @property
    def position(self):
        return self.__position
    @position.setter
    def position(self,new_position):
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
    def guardar(self):
        pass


class Collaborator(User):
    def __init__(self, name:str, phone:int, position:str,user_id:str = None, collab_id:str = None):
        self.__collab_id = collab_id or id_generate("col")
        self.position = position
        self.type = "collaborator"
        User.__init__(self, name, phone, user_id)

    def mostrar_datos(self):
        pass

    def sales(self, root):
        pass
    def clients(self, root):
        pass
    def show_sales(self, root):
        pass

    def guardar(self):
        pass


class Provider(User):
    def __init__(self, name:str, phone:int,user_id:str = None, provider_id:str = None):
        self.__provider_id = provider_id or id_generate("prd")
        self.products = []
        self.type = "provider"
        User.__init__(self, name, phone, user_id)

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

class Client(User):
    def __init__(self, name:str, phone:int,user_id:str = None, client_id:str = None):
        self.__client_id = client_id or id_generate("clt")
        self.sales = []
        self.type = "client"
        User.__init__(self, name, phone, user_id)

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

    def guardar(self):
        pass


class Product:
    def __init__(self, name:str, types:str,  desc:str, raw_p:float, sale_p:float,stock:int,providers: Optional[list[str]] = None,prod_id:str = None):
        self.__id = prod_id or id_generate("prd")
        self.__name = name
        self._type = types
        self._providers = providers
        self.description = desc
        self._raw_p = raw_p
        self._sale_p = sale_p
        self.stock = stock

    @property
    def id(self):
        return self.__id
    @id.setter
    def id(self,new_id):
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
        if provider not in self._providers:
            self._providers.append(provider)
        else:
            raise ValueError("El proveedor ya está en la lista")

    def del_provider(self,provider):
        if provider in self._providers:
            self._providers.remove(provider)
        else:
            raise ValueError("Este producto no tiene a ese proveedor")

    def guardar(self):
        pass

class Sales:
    def __init__(self,sale_id:str,id_client:str, products: Optional[list[str]] = None):
        self.__id = sale_id
        self._id_client = id_client
        self.products = products
        self.total = 0

    def guardar(self):
        pass