import json
import GUI_Module
from GUI_Module import Toplevel, Listbox, END
from Database_Module import mydb

class DataOperations():
    def saveData():
        data={
        'EmFund': GUI_Module.GUI.emFundBox.get(),
        'MiscFund': GUI_Module.GUI.thingsInputBox.get()
        }
        data_file = open('fundsData.json','w')
        json.dump(data, data_file, indent=6)

    savedEmFundMoney=0
    savedMiscMoney=0
    
    def readData():
        savedMoney=[]
        data_file=open('fundsData.json')
        loaded_data = json.load(data_file)
        pairs = loaded_data.items()
        for key,value in pairs:
            savedMoney.append(value)
        global savedEmFundMoney, savedMiscMoney
        savedEmFundMoney = savedMoney[0]
        savedMiscMoney = savedMoney[1]
        
    def readTransactionHistory():
        transactionHistoryScreen = Toplevel()
        transactionHistoryScreen.geometry('460x550')
        transactionHistoryTextBox = Listbox(transactionHistoryScreen, width=100, height=100)
        transactionHistoryTextBox.pack()
        
        queryCursor = mydb.cursor()
        sqlCommand ='SELECT type,amount FROM TransactionHistory'
        queryCursor.execute(sqlCommand)
        result = queryCursor.fetchall()
        mydb.commit()
        for i in result:
            transactionHistoryTextBox.insert(END,"--", i)
