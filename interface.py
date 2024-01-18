import datetime

from dbController import DbController
from tkinter import *
from tkinter import ttk
import threading

dbManager = DbController()

# Arayüz kodları
root = Tk()
root.title("Car Parking")
root.state("zoomed")

fontStyleGroupC = ("Impact", int(root.winfo_screenheight() * 0.06), "bold")
parkingTitle = Label(root, text="FFS101 OTOPARK", foreground="black", font=fontStyleGroupC)
parkingTitle.place(relx=0.03, rely=0.1, relheight=0.1)

fontStyleGroupA = ("Impact", int(root.winfo_screenheight() * 0.02), "bold")
fontStyleGroupB = ("Impact", int(root.winfo_screenheight() * 0.02))
fontStyleButton = ("Impact", int(root.winfo_screenheight() * 0.017))
"""##############################################################"""

# Veri tabanı liste
carList = ttk.Treeview(root, show="headings")
carList["columns"] = ("column1", "column2", "column3", "column4", "column5")
carList.column("column1", width=5)
carList.column("column2", width=50)
carList.column("column3", width=50)
carList.column("column4", width=50)
carList.column("column5", width=50)

carList.heading("column1", text="Id")
carList.heading("column2", text="Marka")
carList.heading("column3", text="Model")
carList.heading("column4", text="Plaka")
carList.heading("column5", text="Zaman")

carList.place(relx=0.6, rely=0.05, relwidth=0.3, relheight=0.6)


# işlem ve hata listesi
processList = Listbox(root)
processList.place(relx=0.6, rely=0.7, relwidth=0.3, relheight=0.25)
dbManager.set_car_listbox(processList)


""""""
# sunucu bilgisi al
serverLbl = Label(root, text="Server İsmi:", font=("Impact", int(root.winfo_screenheight() * 0.02), "bold"))
serverLbl.place(relx=0.02, rely=0.3)
serverEntr = Entry(root, font=fontStyleGroupB)
serverEntr.place(relx=0.12, rely=0.3, relheight=0.04, relwidth=0.08)
# server bağlan
def ServerConnectThreading():
    serverConnectThread = threading.Thread(target=ServerConnect)
    serverConnectThread.start()
def ServerConnect():
    serverName = serverEntr.get()
    dbManager.connectWA(serverName)


serverCntBtn = Button(root, text="Server Bağlan", font=fontStyleButton, foreground="green",
                      command=ServerConnectThreading)
serverCntBtn.place(relx=0.22, rely=0.3, relheight=0.04, relwidth=0.1)

""""""
# veritabanı bilgisi al
databaseLbl = Label(root, text="Database İsmi:", font=fontStyleGroupA)
databaseLbl.place(relx=0.02, rely=0.35)
databaseEntr = Entry(root, font=fontStyleGroupB)
databaseEntr.place(relx=0.12, rely=0.35, relheight=0.04, relwidth=0.08)
# veritabanı oluştur
def DatabaseCreateThreading():
    databaseCreateThread = threading.Thread(target=DatabaseCreate)
    databaseCreateThread.start()
def DatabaseCreate():
    databaseName = databaseEntr.get()
    dbManager.CreateDatabase(databaseName)


databaseCrtBtn = Button(root, text="Veritabanı Oluştur", font=fontStyleButton, foreground="blue",
                        command=DatabaseCreateThreading)
databaseCrtBtn.place(relx=0.22, rely=0.35, relheight=0.04, relwidth=0.1)

""""""
# veritabanı bağlan
def DatabaseConnectThreading():
    databaseConnectThread = threading.Thread(target=DatabaseConnect)
    databaseConnectThread.start()
def DatabaseConnect():
    databaseName = databaseEntr.get()
    dbManager.ConnectDatabase(databaseName)
databaseCntBtn = Button(root, text="Veritabanı Bağlan", font=fontStyleButton, foreground="blue",
                        command=DatabaseConnectThreading)
databaseCntBtn.place(relx=0.322, rely=0.35, relheight=0.04, relwidth=0.1)

""""""
# tablo oluştur
tableLbl = Label(root, text="Tablo Adı:", font=fontStyleGroupA)
tableLbl.place(relx=0.02, rely=0.4)
tableEntr = Entry(root, font=fontStyleGroupB)
tableEntr.place(relx=0.12, rely=0.4, relheight=0.04, relwidth=0.08)
def TableCreateThreading():
    tableCreateThread = threading.Thread(target=TableCreate)
    tableCreateThread.start()
def TableCreate():
    tableName = tableEntr.get()
    dbManager.CreateTable(tableName)
tableCrtBtn = Button(root, text="Tablo Oluştur", font=fontStyleButton, foreground="purple",
                     command=TableCreateThreading)
tableCrtBtn.place(relx=0.22, rely=0.4, relheight=0.04, relwidth=0.1)


def TableConnectThreading():
    tableConnectThread = threading.Thread(target=TableConnect)
    tableConnectThread.start()
def TableConnect():
    tableName = tableEntr.get()
    dbManager.ConnectTable(tableName)
    dbManager.SetCarListTreeview(carList)

    serverEntr.delete(0, END)
    databaseEntr.delete(0, END)
    tableEntr.delete(0, END)

tableCntBtn = Button(root, text="Tablo Bağlan", font=fontStyleButton, foreground="purple",
                     command=TableConnectThreading)
tableCntBtn.place(relx=0.322, rely=0.4, relheight=0.04, relwidth=0.1)

"""##############################################################"""

# marka bilgisi al
brandLbl = Label(root, text="Araç Markası:", font=fontStyleGroupA)
brandLbl.place(relx=0.02, rely=0.6)
brandEntr = Entry(root, font=fontStyleGroupB)
brandEntr.place(relx=0.12, rely=0.6, relheight=0.04, relwidth=0.08)

# model bilgisi al
modelLbl = Label(root, text="Araç modeli:", font=fontStyleGroupA)
modelLbl.place(relx=0.02, rely=0.65)
modelEntr = Entry(root, font=fontStyleGroupB)
modelEntr.place(relx=0.12, rely=0.65, relheight=0.04, relwidth=0.08)

# plaka bilgisi al
plateLbl = Label(root, text="Araç Plakası:", font=fontStyleGroupA)
plateLbl.place(relx=0.02, rely=0.7)
plateEntr = Entry(root, font=fontStyleGroupB)
plateEntr.place(relx=0.12, rely=0.7, relheight=0.04, relwidth=0.08)

""""""
def VehicleSaveThreading():
    vehicleSaveThread = threading.Thread(target=VehicleSave)
    vehicleSaveThread.start()
def VehicleSave():
    brand = brandEntr.get()
    model = modelEntr.get()
    plate = plateEntr.get()

    if brand == "" or model == "" or plate == "":
        dbManager.update_car_listbox("Araç bilgileri eksik")
        return
    else:
        dbManager.SendToSQL(brand, model, plate, datetime.datetime.utcnow())
        dbManager.SetCarListTreeview(carList)

        brandEntr.delete(0, END)
        modelEntr.delete(0, END)
        plateEntr.delete(0, END)

vehicleSvBtn = Button(root, text="Araç Kayıt", font=fontStyleButton, foreground="orange", command=VehicleSaveThreading)
vehicleSvBtn.place(relx=0.22, rely=0.6, relheight=0.04, relwidth=0.1)

def VehicleDeleteThreading():
    vehicleDeleteThread = threading.Thread(target=VehicleDelete)
    vehicleDeleteThread.start()
def VehicleDelete():
    selected_item = carList.selection()
    if not selected_item:
        return

    values = carList.item(selected_item)['values']
    id = values[0]

    dbManager.DeleteCarList(id)

    carList.delete(selected_item)

vehicleDlBtn = Button(root, text="Araç Sil", font=fontStyleButton, foreground="red", command=VehicleDeleteThreading)
vehicleDlBtn.place(relx=0.22, rely=0.65, relheight=0.04, relwidth=0.1)

def RefreshTableThreading():
    refreshTableThread = threading.Thread(target=RefreshTable)
    refreshTableThread.start()
def RefreshTable():
    dbManager.SetCarListTreeview(carList)
RefrashTableBtn = Button(root, text="Tablo Yenile", font=fontStyleButton, foreground="turquoise", command=RefreshTableThreading)
RefrashTableBtn.place(relx=0.22, rely=0.7, relheight=0.04, relwidth=0.1)


root.mainloop()