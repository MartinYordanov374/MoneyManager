from tkinter import *
import json
from dotenv.main import find_dotenv 
import os
from datetime import date
import GUI_Module
from GUI_Module import root
import Data_Module


Data_Module.DataOperations.checkFunds()

Data_Module.DataOperations.readData()


GUI_Module.GUI.emFundGUI()
GUI_Module.GUI.thingsFundGUI()
GUI_Module.GUI.optionsGUI()

root.mainloop()