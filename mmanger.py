from tkinter import *

root=Tk()

root.title('MoneyManager')
root.geometry("800x600")
def addMoneyEmFund():
    addScreen = Toplevel()
    addScreen.geometry("450x500")
    addMoneyPromptMessage = Label(addScreen,text='How much money would you like to add to your Emergency Fund?').grid(row=0, column=0)
    addMoneyField= Entry(addScreen)
    addMoneyField.grid(row=1, column=0, ipadx=130)
    finishAddingButton = Button(addScreen, text='Add money to your emergency fund',width=50, command=lambda: confirmAddingEmFundMoney(addMoneyField.get())).grid(row=2,column=0)

def confirmAddingEmFundMoney(amount):
    currAmount = amount
    formerAmount = emFundBox.get()
    emFundBox.delete(0,END)
    emFundBox.insert(0,float(int(currAmount))+float(int(formerAmount)))
#BUTTON LABEL - EMERGENCY FUND

emergencyFundLabel = Label(root, text='Emergency Fund:').grid(row=0, column=0)

#TEXTBOX - EMERGENCY FUND

emFundBox = Entry(root, state='normal')
emFundBox.grid(row=0, column=1)

#WITHDRAW FROM EMERGENCY FUND -> OPEN A NEW SCREEN ASKING HOW MUCH TO WITHDRAW

emFundWithdrawButton = Button(root, text='Withdraw money').grid(row=1, column=0)

#ADD TO EMERGENCY FUND -> OPEN A NEW SCREEN ASKING HOW MUCH TO ADD

emFundAddButton = Button(root, text='Add money', command=addMoneyEmFund).grid(row=1, column=1)






#BUTTON LABEL - THINGS
#TEXTBOX - THINGS FUND
#WITHDRAW FROM THINGS FUNDS -> OPEN A NEW SCREEN ASKING HOW MUCH TO WITHDRAW
#ADD TO THINGS FUND -> OPEN A NEW SCREEN ASKING HOW MUCH TO ADD

#CREATE NEW FUND BUTTON
#DELETE FUND BUTTON

#SHOW HISTORY OF WITHDRAWALS AND INSERTIONS 
root.mainloop()