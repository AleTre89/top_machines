"""
TkInter interface with "anagrafica" and "Manutenzione" buttons that opens respectively
the objects Anagrafica() and Manutenzioni and allow the access to their functions
"""

import tkinter
from tkinter import *
from UIAnagrafica import Anagrafica
from UIManutenzione import Manutenzioni


def anagrafica_start():
    anagrafica_window = Anagrafica()

def manutenzioni_start():
    manutenzioni_window= Manutenzioni(codice="all")

master_window = Tk()
master_window.title("Gestione attrezzature")

#Buttons and position
anagrafica_button = Button(width=15, text= "Anagrafica", highlightthickness=0, command=anagrafica_start)
manutenzione_button = Button(width=15, text= "Manutenzione", highlightthickness=0,command=manutenzioni_start)
anagrafica_button.grid(row=0,column=0, padx=20,pady=20)
manutenzione_button.grid(row=0,column=1,padx=20,pady=20)


tkinter.mainloop()
