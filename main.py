import tkinter as tk
from tkinter import ttk
import sqlite3

DB_NAME = "bawiz.db"

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
                phone TEXT NOT NULL,
                type TEXT NOT NULL,
            );
            
            CREATE TABLE IF NOT EXISTS clients (
                id_client TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                phone TEXT NOT NULL,
            );
            
            CREATE TABLE IF NOT EXISTS products (
                id_product TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                type TEXT NOT NULL,
                description TEXT NOT NULL,
                raw_price TEXT NOT NULL,
                sale_price TEXT NOT NULL,
            );
            
            CREATE TABLE IF NOT EXISTS providers (
                id_provider TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                phone TEXT NOT NULL,
            );
            
            CREATE TABLE IF NOT EXISTS sales (
                id_sale TEXT PRIMARY KEY,
                id_client TEXT,
                total REAL,
                FOREIGN KEY (id_client) REFERENCES clients(id_client)
            );
            
            """)

class User:
    def __init__(self,user_id, name, phone):
        self.__id = user_id
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


class Admin(User):
    def __init__(self,user_id, name, phone):
        User.__init__(self,user_id,name,phone)
        self.type = "admin"

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


class Collaborator(User):
    def __init__(self,user_id, name, phone, position):
        User.__init__(self,user_id,name,phone)
        self.position = position
        self.type = "collaborator"

    def mostrar_datos(self):
        pass

    def sales(self, root):
        pass
    def clients(self, root):
        pass
    def show_sales(self, root):
        pass


class provider(User):
    def __init__(self,user_id, name, phone):
        User.__init__(self,user_id,name,phone)
        self.products = []
        self.type = "provider"

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
    def __init__(self,user_id, name, phone):
        User.__init__(self,user_id,name,phone)
        self.sales = []
        self.type = "client"

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


class Product:
    def __init__(self,prod_id, name, type, desc, raw_p, sale_p):
        self.__id = prod_id
        self.__name = name
        self._type = type
        self._providers = []
        self.description = desc
        self._raw_p = raw_p
        self._sale_p = sale_p

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

class Sales:
    def __init__(self,sale_id,id_client):
        self.__id = sale_id
        self._id_client = id_client
        self.products = {} #ID_producto[cantidad_productos, subtotal (cantidad*precio_unitario)]
        self.total = 0