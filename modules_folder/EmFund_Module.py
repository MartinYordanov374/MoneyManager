from tkinter import *
import GUI_Module
import Data_Module
from Database_Module import mydb
class EmFund():
    def addMoneyEmFund():
        addScreen = Toplevel()
        addScreen.title('Deposit Money - Emergency Fund')
        addScreen.geometry("460x500")
        addMoneyPromptMessage = Label(addScreen,text='How much money would you like to deposit to your Emergency Fund?')
        addMoneyPromptMessage.grid(row=0, column=0)
        addMoneyField= Entry(addScreen)
        addMoneyField.grid(row=1, column=0, ipadx=130)
        finishAddingButton = Button(addScreen, text='Deposit money to your emergency fund',width=50, 
        command=lambda: EmFund.confirmAddingEmFundMoney(addMoneyField.get())).grid(row=2,column=0)
    
    def confirmAddingEmFundMoney(amount):
        if(len(amount)>0):
            currAmount = float(amount)
            formerAmount = float(GUI_Module.GUI.emFundBox.get())
            GUI_Module.GUI.emFundBox.delete(0,END)
            GUI_Module.GUI.emFundBox.insert(0,currAmount+formerAmount)
            Data_Module.DataOperations.saveData()

            val=('deposit', amount)
            mydb.execute('INSERT INTO TransactionHistory (type, amount) VALUES (?,?)', val)
            mydb.commit()

        else:
            errorScreen = Toplevel()
            errorMessage = Label(errorScreen, text='ERROR - INVALID VALUE')
            errorMessage.pack()

    def withdrawMoneyEmFund():
        withdrawScreen = Toplevel()
        withdrawScreen.title('Withdraw Money - Emergency Fund')
        withdrawScreen.geometry('460x500')
        #ask message -> How muhc would you like to withdraw?
        withdrawPromptMessage = Label(withdrawScreen,text='How much money would you like to withdraw?')
        withdrawPromptMessage.grid(row=0, column=0)
        #input field
        withdrawInputField = Entry(withdrawScreen)
        withdrawInputField.grid(row=1, column =0, ipadx=130)
        #withdraw input button -> How much would you like to withdraw?
        withdrawButton = Button(withdrawScreen,text='Withdraw money from your emergency fund', width=50, 
        command=lambda: EmFund.confirmWithdrawEmFundMoney(withdrawInputField.get()))
        withdrawButton.grid(row=2, column=0)

    def confirmWithdrawEmFundMoney(amount):
            currentEmFundMoney = float(GUI_Module.GUI.emFundBox.get())
            moneyToWithdraw = float(amount)
            if(len(amount)>=0 and moneyToWithdraw<=currentEmFundMoney):
                GUI_Module.GUI.emFundBox.delete(0,END)
                GUI_Module.GUI.emFundBox.insert(0,currentEmFundMoney-moneyToWithdraw)
                Data_Module.DataOperations.saveData()
                val=('withdraw', amount)
                mydb.execute('INSERT INTO TransactionHistory (type, amount) VALUES (?,?)', val)
                mydb.commit()

            else:
                errorScreen = Toplevel()
                errorMessage = Label(errorScreen, text='ERROR - INVALID VALUE')
                errorMessage.pack()
