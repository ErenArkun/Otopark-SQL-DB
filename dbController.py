import pyodbc
import tkinter as tk
import datetime
from tkinter import *
from tkinter import ttk
import tkinter
class DbController:
    def __init__(self):
        self.server = None
        self.database = None
        self.connection = None
        self.cursor = None
        self.table = None
        self.listbox_car = None
        self.listbox_table = None
        self.carList = None

    def set_car_listbox(self, listbox_car):
        self.listbox_car = listbox_car

    def update_car_listbox(self, message):
        if self.listbox_car:
            #self.listbox_car.delete(0, tk.END)
            self.listbox_car.insert(tk.END, message)
            self.listbox_car.yview(tk.END)
        else:
            print("Listbox bulunamadı. Lütfen set_listbox metoduyla bir Listbox ekleyin.")

    # Connect Windows Authentication
    def connectWA(self, serverName):
        self.server = serverName
        connection_string = f'DRIVER={{SQL Server}};' \
                            f'SERVER={serverName};' \
                            f'Trusted_Connection=yes'
        self.connection = pyodbc.connect(connection_string, autocommit=True)
        self.cursor = self.connection.cursor()
        print(f'{serverName} adli server baglandi.')
        self.update_car_listbox(f'{serverName} adli server baglandi.')

    # veritabanı oluştur
    def CreateDatabase(self, databaseName):
        if not self.connection:
            self.update_car_listbox("SSMS bağlantısı yok! Connect metodunu kullanın.")
            raise ValueError("SSMS bağlantısı yok! Connect metodunu kullanın.")

        self.database = databaseName
        self.cursor.execute("SELECT name FROM sys.databases WHERE name = ?", databaseName)
        result = self.cursor.fetchone()

        if result is None:
            # Veritabanı yoksa oluştur
            self.cursor.execute(f"CREATE DATABASE {databaseName}")
            print(f"Veritabanı {databaseName} oluşturuldu.")
            self.update_car_listbox(f"Veritabanı {databaseName} oluşturuldu.")
        else:
            print(f"Veritabanı {databaseName} zaten mevcut.")
            self.update_car_listbox(f"Veritabanı {databaseName} zaten mevcut.")

    def ConnectDatabase(self, databaseName):
        if not self.connection:
            self.update_car_listbox("SSMS bağlantısı yok! Connect metodunu kullanın.")
            raise ValueError("SSMS bağlantısı yok! Connect metodunu kullanın.")

        # Yeni bir bağlantı dizesi oluştur
        Connection_String = f'DRIVER={{SQL Server}};' \
                            f'SERVER={self.server};' \
                            f'DATABASE={databaseName};' \
                            f'Trusted_Connection=yes'

        try:
            # Veritabanına bağlan
            self.Connection = pyodbc.connect(Connection_String, autocommit=True)
            self.cursor = self.Connection.cursor()  # self.cursor'u yeni bağlantıya güncelle

            # Yeni bağlantının olup olmadığını kontrol et
            if not self.Connection:
                self.update_car_listbox("SSMS bağlantısı yok! Connect metodunu kullanın.")
                raise ValueError("SSMS bağlantısı yok! Connect metodunu kullanın.")

            # Veritabanı bağlantısı başarılı olursa
            self.database = databaseName
            print(f"Bağlantı başarılı. Şu an {databaseName} veritabanına bağlısınız.")
            self.update_car_listbox(f"Bağlantı başarılı. Şu an {databaseName} veritabanına bağlısınız.")
        except pyodbc.Error as e:
            print(f"Hata oluştu: {str(e)}")
            # Veritabanına bağlanırken hata olursa
            self.update_car_listbox(
                f"{databaseName} adında bir veritabanı bulunamadı. Lütfen geçerli bir veritabanı adı girin.")
            raise ValueError(
                f"{databaseName} adında bir veritabanı bulunamadı. Lütfen geçerli bir veritabanı adı girin.")

    def CreateTable(self, table_name):
        if not self.connection:
            self.update_car_listbox("SSMS bağlantısı yok! Connect metodunu kullanın.")
            raise ValueError("SSMS bağlantısı yok! Connect metodunu kullanın.")

        self.table = table_name

        # Yeni bir bağlantı dizesi oluştur
        newConnection_String = f'DRIVER={{SQL Server}};' \
                               f'SERVER={self.server};' \
                               f'DATABASE={self.database};' \
                               f'Trusted_Connection=yes'

        # Yeni bağlantıyı oluştur ve ona ait bir imleç oluştur
        self.newConnection = pyodbc.connect(newConnection_String, autocommit=True)
        self.cursor = self.newConnection.cursor()  # self.cursor'u yeni bağlantıya güncelle

        # Yeni bağlantının olup olmadığını kontrol et
        if not self.newConnection:
            self.update_car_listbox("SSMS bağlantısı yok! Connect metodunu kullanın.")
            raise ValueError("SSMS bağlantısı yok! Veritabanına bağlanın.")

        # Tablonun veritabanındaki varlığını kontrol et
        self.cursor.execute("SELECT name FROM sys.tables WHERE name = ?", table_name)
        result = self.cursor.fetchone()

        # Tablo zaten varsa işlemi sonlandır
        if result is not None:
            self.update_car_listbox("Tablo zaten mevcut.")
            print("Tablo zaten mevcut.")
            return  # tablo varsa metodu bitir

        # Tablo oluşturma sorgusunu oluştur
        create_table_query = f'''
            CREATE TABLE {table_name} (
                ID INT PRIMARY KEY IDENTITY(1,1),
                Marka NVARCHAR(50),
                Model NVARCHAR(50),
                Plaka NVARCHAR(50),
                GirisZaman datetimeoffset
            )
        '''

        # Tablo oluşturma sorgusunu çalıştır
        self.cursor.execute(create_table_query)

        # Yapılan değişiklikleri kaydet
        self.newConnection.commit()

        # Kullanıcıya mesaj ver
        self.update_car_listbox(f"{table_name} adında 5 sütunlu tablo oluşturuldu.")
        print(f"{table_name} adında 5 sütunlu tablo oluşturuldu.")

    def ConnectTable(self, table_name):
        if not self.connection:
            self.update_car_listbox("SSMS database bağlantısı yok! Connect metodunu kullanın.")
            raise ValueError("SSMS bağlantısı yok! Connect metodunu kullanın.")

        if not self.database:
            self.update_car_listbox("Veritabanına bağlanmadınız! ConnectDatabase metodu kullanın.")
            raise ValueError("Veritabanına bağlanmadınız! ConnectDatabase metodu kullanın.")

        """ 
        if not self.table:
            self.update_car_listbox("Tablo belirlenmemiş! CreateTable metodu kullanın.")
            raise ValueError("Tablo belirlenmemiş! CreateTable metodu kullanın.")
        """

        # Yeni bir bağlantı dizesi oluştur
        Connection_String = f'DRIVER={{SQL Server}};' \
                            f'SERVER={self.server};' \
                            f'DATABASE={self.database};' \
                            f'Trusted_Connection=yes'

        try:
            # Veritabanına bağlan
            self.connection = pyodbc.connect(Connection_String, autocommit=True)
            self.cursor = self.connection.cursor()  # self.cursor'u yeni bağlantıya güncelle

            # Yeni bağlantının olup olmadığını kontrol et
            if not self.connection:
                self.update_car_listbox("SSMS bağlantısı yok! Connect metodunu kullanın.")
                raise ValueError("SSMS bağlantısı yok! Connect metodunu kullanın.")

            # Bağlanmak istenilen tablonun veritabanındaki varlığını kontrol et
            self.cursor.execute("SELECT name FROM sys.tables WHERE name = ?", table_name)
            result = self.cursor.fetchone()

            # Tablo varsa bağlantı başarılı olursa
            if result is not None:
                self.table = table_name
                print(f"Tablo bağlantısı başarılı. Şu an {table_name} tablosuna bağlısınız.")
                self.update_car_listbox(f"Tablo bağlantısı başarılı. Şu an {table_name} tablosuna bağlısınız.")
            else:
                print(f"Tablo {table_name} bulunamadı. Lütfen geçerli bir tablo adı girin.")
                self.update_car_listbox(f"Tablo {table_name} bulunamadı. Lütfen geçerli bir tablo adı girin.")

        except pyodbc.Error as e:
            print(f"Hata oluştu: {str(e)}")
            # Veritabanına bağlanırken hata olursa
            self.update_car_listbox(f"{table_name} adında bir tablo bulunamadı. Lütfen geçerli bir tablo adı girin.")
            raise ValueError(f"{table_name} adında bir tablo bulunamadı. Lütfen geçerli bir tablo adı girin.")

    def SendToSQL(self, marka, model, plaka, giriszaman):
        if not self.connection:
            self.update_car_listbox("SSMS database bağlantısı yok! Connect metodunu kullanın.")
            raise ValueError("SSMS bağlantısı yok! Connect metodunu kullanın.")

        if not self.table:
            self.update_car_listbox("Tablo belirlenmemiş! create_table metodu kullanın.")
            raise ValueError("Tablo belirlenmemiş! create_table metodu kullanın.")

        # Veri ekleme sorgusunu oluştur
        insert_query = f"INSERT INTO {self.table} (Marka, Model, Plaka, GirisZaman) VALUES (?, ?, ?, ?)"

        # Eklemek istediğiniz değerlere göre bu listeyi güncelleyin
        values_to_insert = (marka, model, plaka, giriszaman)

        try:
            # Sorguyu çalıştır
            self.cursor.execute(insert_query, values_to_insert)

            # Değişiklikleri kaydet
            self.connection.commit()

            # Kullanıcıya mesaj ver
            self.update_car_listbox(f"Veri başarıyla eklendi: {values_to_insert}")
            print(f"Veri başarıyla eklendi: {values_to_insert}")

        except pyodbc.Error as e:
            print(f"Hata oluştu: {str(e)}")
            self.update_car_listbox("Veri eklenirken bir hata oluştu.")

    def SetCarListTreeview(self, carlist):
        self.carList = carlist

        current_table = self.table

        if not self.connection:
            self.update_car_listbox("SSMS database bağlantısı yok! Connect metodunu kullanın.")
            raise ValueError("SSMS bağlantısı yok! Connect metodunu kullanın.")

        if not current_table:
            self.update_car_listbox("Tablo belirlenmemiş! CreateTable metodu kullanın.")
            raise ValueError("Tablo belirlenmemiş! CreateTable metodu kullanın.")

        # Tablodaki verileri al
        select_query = f"SELECT * FROM {current_table}"
        self.cursor.execute(select_query)
        rows = self.cursor.fetchall()

        # Sadece satırları temizle
        self.carList.delete(*self.carList.get_children())

        # Sütunları oluştur (eğer henüz oluşturulmamışsa)
        if not self.carList["columns"]:
            columns = [description[0] for description in self.cursor.description]
            self.carList["columns"] = columns
            for col in columns:
                self.carList.heading(col, text=col)
                self.carList.column(col, anchor="center",
                                    width=100)  # Sütun genişliğini ayarlayın (gerektiğinde değiştirin)

        # Verileri ttk.Treeview içine ekle
        for row in rows:
            self.carList.insert("", "end", values=(row[0], row[1], row[2], row[3], row[4]))

    def DeleteCarList(self, selectedCar):
        if not self.connection:
            self.update_car_listbox("SSMS database bağlantısı yok! Connect metodunu kullanın.")
            raise ValueError("SSMS bağlantısı yok! Connect metodunu kullanın.")

        if not self.table:
            self.update_car_listbox("Tablo belirlenmemiş! CreateTable metodu kullanın.")
            raise ValueError("Tablo belirlenmemiş! CreateTable metodu kullanın.")

        if not selectedCar:
            self.update_car_listbox("Silinecek araç seçilmedi!")
            return

        # Silme işlemi için SQL sorgusunu oluştur ve uygula
        #delete_query = f"DELETE FROM {self.table} WHERE ID = {selectedCar}"
        self.cursor.execute(f"DELETE FROM {self.table} WHERE ID = {selectedCar} ")
        self.update_car_listbox("Araç başarıyla silindi.")


    # Kullanım
    # Önce bir araç seçin, ardından DeleteCarList metodunu çağırın:
    # selectedCar = self.carList.selection()
    # self.DeleteCarList(selectedCar)

    def disconnect(self):
        if self.connection:
            self.connection.close()
            self.update_car_listbox("Bağlantı kapatıldı.")
            print("Bağlantı kapatıldı.")