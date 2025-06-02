"""
Checklist to compile. In this moment it works only for Aspiratore and Lavasciuga
"""

from tkinter import *
from datetime import datetime,timedelta
import pandas


ASP1 = "Controllo sistema aspirazione e filtri"
ASP2 = "Ruote e rotelle"
ASP3 = "Interuttori e spina di alimentazione"
ASP4 = "Controllo pulizia interna e esterna"
ASP5 = "Sostituzione spugne interne (ogni sei mesi o se è necessario)"


LAV1 = "Stato e ricarica batterie"
LAV2 = "Stato e pulizia ruote"
LAV3 = "Squeegee \"gomme e rotelle\""
LAV4 = "Pulizia interna ed esterna"
LAV5 = "Funzionamento aspiratore e tubazioni"
LAV6 = "Funzionamento generale e accessori"
NOTE = "Note ed eventuali"

class Aspiratore:


    def __init__(self,matr,tipo,comm,riga):

        self.check_aspiratore = Toplevel()
        self.check_aspiratore.title("Checklist aspiratori")
        self.check_aspiratore.config(width=500, height=500)
        self.work_row = riga


        global var1, var2, var3, var4, var5
        var1 = IntVar()
        var2 = IntVar()
        var3 = IntVar()
        var4 = IntVar()
        var5 = IntVar()



        self.matr_label = Label(self.check_aspiratore, text="Matricola")
        self.matr_text = Label(self.check_aspiratore, text=matr)
        self.matr_label.grid(row=0,column=0)
        self.matr_text.grid(row=1,column=0)

        self.tipo_label = Label(self.check_aspiratore,text="Tipologia")
        self.tipo_text =Label(self.check_aspiratore,text=tipo)
        self.tipo_label.grid(row=0,column=1)
        self.tipo_text.grid(row=1,column=1)

        self.commessa_label = Label(self.check_aspiratore,text="Commessa")
        self.commessa_text = Label(self.check_aspiratore,text=comm)
        self.commessa_label.grid(row=0,column=2)
        self.commessa_text.grid(row=1,column=2)

        self.asp_1_label = Label(self.check_aspiratore,width=50, anchor="w",text=ASP1)
        self.asp_1_label.grid(row=2,column=0, padx=10,columnspan=3)
        self.asp_1_chk = Checkbutton(self.check_aspiratore,variable=var1)
        self.asp_1_chk.grid(row=3,column=0)

        self.asp_2_label = Label(self.check_aspiratore,width=50, anchor="w" ,text=ASP2)
        self.asp_2_label.grid(row=4,column=0, padx=10,columnspan=3)
        self.asp_2_chk = Checkbutton(self.check_aspiratore,variable=var2)
        self.asp_2_chk.grid(row=5,column=0)

        self.asp_3_label = Label(self.check_aspiratore,width=50, anchor="w",text=ASP3)
        self.asp_3_label.grid(row=6,column=0, padx=10,columnspan=3)
        self.asp_3_chk = Checkbutton(self.check_aspiratore,variable=var3)
        self.asp_3_chk.grid(row=7,column=0)

        self.asp_4_label = Label(self.check_aspiratore,width=50, anchor="w",text=ASP4)
        self.asp_4_label.grid(row=8,column=0, padx=10,columnspan=3)
        self.asp_4_chk = Checkbutton(self.check_aspiratore,variable=var4)
        self.asp_4_chk.grid(row=9,column=0)

        self.asp_5_label = Label(self.check_aspiratore,width=50, anchor="w" ,text=ASP5)
        self.asp_5_label.grid(row=10,column=0, padx=10,columnspan=3)
        self.asp_5_chk = Checkbutton(self.check_aspiratore,variable=var5)
        self.asp_5_chk.grid(row=11,column=0)

        self.asp_6_label = Label(self.check_aspiratore,width=50, anchor="w" ,text=NOTE)
        self.asp_6_text = Entry(self.check_aspiratore,width=50)
        self.asp_6_label.grid(row=12,column=0, padx=10,columnspan=3)
        self.asp_6_text.grid(row=13,column=0, pady=10, padx=10,columnspan=3)


        self.invia_button= Button(self.check_aspiratore,text="Inserisci", command=self.insert_data)
        self.invia_button.grid(row=14,column=2,padx=10,pady=10)


        self.check_aspiratore.mainloop()

    def insert_data(self):
            base = pandas.read_csv("anagrafica/manutenzioni.csv")
            df = pandas.DataFrame(base)
            df_dict = df.to_dict(orient="records")
            print(df_dict)
            riga = self.work_row
            totrows=len(df_dict)
            print(totrows)

            #modifica riga attuale
            today = datetime.today().strftime("%d/%m/%Y")
            df_dict[riga]["Data intervento"] = today
            df_dict[riga]["ASP1-filtri"] = var1.get()
            df_dict[riga]["ASP2-ruote"] = int(var2.get())
            df_dict[riga]["ASP3-interruttori"] = int(var3.get())
            df_dict[riga]["ASP4-pulizia"] = int(var4.get())
            df_dict[riga]["ASP5-spugne"] = int(var5.get())
            df_dict[riga]["Note"] = self.asp_6_text.get()

            df_updated = pandas.DataFrame.from_dict(df_dict)


            #Creazione nuova riga
            #inserimento dati base
            codice = df_dict[riga]["Codice"]
            tipo_int = df_dict[riga]["Tipo intervento"]
            #spostamento data avanti di 90gg
            data_prog = df_dict[riga]["Data programmata"]
            date_format = '%d/%m/%Y'
            newdate = datetime.strptime(data_prog,date_format)
            next_date = newdate + timedelta(days=90)
            next_date_format = next_date.strftime("%d/%m/%Y")

            #inserimento nuova riga, trasposizione e concatenazione
            new_row = pandas.Series({"id":totrows,
                                    "Codice": codice,
                                     "Tipo intervento": tipo_int,
                                     "Data programmata":next_date_format})
            df3 = pandas.concat([df_updated,new_row.to_frame().T], ignore_index=True)
            df_clean = df3.fillna(" ")
            manutenzione = df_clean.to_csv(path_or_buf="anagrafica/manutenzioni.csv",index=False)



class Lavasciuga:

    def __init__(self, matr, tipo, comm, riga):
        self.check_lavasciuga = Toplevel()
        self.check_lavasciuga.title("Checklist aspiratori")
        self.check_lavasciuga.config(width=500, height=500)
        self.work_row = riga

        #answer = str.upper(attr[:3]+"1")
        #print(answer)

        global varl2, varl3, varl4, varl5, varl6
        self.varl1 = IntVar()
        varl2 = IntVar()
        varl3 = IntVar()
        varl4 = IntVar()
        varl5 = IntVar()
        varl6 = IntVar()

        self.matr_label = Label(self.check_lavasciuga, text="Matricola")
        self.matr_text = Label(self.check_lavasciuga, text=matr)
        self.matr_label.grid(row=0, column=0)
        self.matr_text.grid(row=1, column=0)

        self.tipo_label = Label(self.check_lavasciuga, text="Tipologia")
        self.tipo_text = Label(self.check_lavasciuga, text=tipo)
        self.tipo_label.grid(row=0, column=1)
        self.tipo_text.grid(row=1, column=1)

        self.commessa_label = Label(self.check_lavasciuga, text="Commessa")
        self.commessa_text = Label(self.check_lavasciuga, text=comm)
        self.commessa_label.grid(row=0, column=2)
        self.commessa_text.grid(row=1, column=2)

        self.lav_1_label= Label(self.check_lavasciuga, width=50, anchor="w", text=LAV1)
        self.lav_1_label.grid(row=2, column=0, padx=10, columnspan=3)
        self.lav_1_chk = Checkbutton(self.check_lavasciuga, variable=self.varl1)
        self.lav_1_chk.grid(row=3, column=0)

        self.lav_2_label = Label(self.check_lavasciuga, width=50, anchor="w", text=LAV2)
        self.lav_2_label.grid(row=4, column=0, padx=10, columnspan=3)
        self.lav_2_chk = Checkbutton(self.check_lavasciuga, variable=varl2)
        self.lav_2_chk.grid(row=5, column=0)

        self.lav_3_label = Label(self.check_lavasciuga, width=50, anchor="w", text=LAV3)
        self.lav_3_label.grid(row=6, column=0, padx=10, columnspan=3)
        self.lav_3_chk = Checkbutton(self.check_lavasciuga, variable=varl3)
        self.lav_3_chk.grid(row=7, column=0)

        self.lav_4_label = Label(self.check_lavasciuga, width=50, anchor="w", text=LAV4)
        self.lav_4_label.grid(row=8, column=0, padx=10, columnspan=3)
        self.lav_4_chk = Checkbutton(self.check_lavasciuga, variable=varl4)
        self.lav_4_chk.grid(row=9, column=0)

        self.lav_5_label = Label(self.check_lavasciuga, width=50, anchor="w", text=LAV5)
        self.lav_5_label.grid(row=10, column=0, padx=10, columnspan=3)
        self.lav_5_chk = Checkbutton(self.check_lavasciuga, variable=varl5)
        self.lav_5_chk.grid(row=11, column=0)

        self.lav_6_label = Label(self.check_lavasciuga, width=50, anchor="w", text=LAV6)
        self.lav_6_label.grid(row=10, column=0, padx=10, columnspan=3)
        self.lav_6_chk = Checkbutton(self.check_lavasciuga, variable=varl6)
        self.lav_6_chk.grid(row=11, column=0)

        self.lav_7_label = Label(self.check_lavasciuga, width=50, anchor="w", text=NOTE)
        self.lav_7_text = Entry(self.check_lavasciuga, width=50)
        self.lav_7_label.grid(row=12, column=0, padx=10, columnspan=3)
        self.lav_7_text.grid(row=13, column=0, pady=10, padx=10, columnspan=3)

        self.invia_button = Button(self.check_lavasciuga, text="Inserisci", command=self.insert_data)
        self.invia_button.grid(row=14, column=2, padx=10, pady=10)

        self.check_lavasciuga.mainloop()

    def insert_data(self):
            base = pandas.read_csv("anagrafica/manutenzioni.csv")
            df = pandas.DataFrame(base)
            df_dict = df.to_dict(orient="records")
            riga = self.work_row
            totrows=len(df_dict)
            print(totrows)

            #modifica riga attuale
            today = datetime.today().strftime("%d/%m/%Y")
            df_dict[riga]["Data intervento"] = today
            df_dict[riga]["LAV1-batt"] = self.varl1.get()
            df_dict[riga]["LAV2-ruote"] = int(varl2.get())
            df_dict[riga]["LAV3-gomme"] = int(varl3.get())
            df_dict[riga]["LAV4-pulizia"] = int(varl4.get())
            df_dict[riga]["LAV5-tubaz"] = int(varl5.get())
            df_dict[riga]["LAV6-gen"] = int(varl6.get())
            df_dict[riga]["Note"] = self.lav_7_text.get()

            df_updated = pandas.DataFrame.from_dict(df_dict)


            #Creazione nuova riga
            #inserimento dati base
            codice = df_dict[riga]["Codice"]
            tipo_int = df_dict[riga]["Tipo intervento"]
            #spostamento data avanti di 90gg
            data_prog = df_dict[riga]["Data programmata"]
            date_format = '%d/%m/%Y'
            newdate = datetime.strptime(data_prog,date_format)
            next_date = newdate + timedelta(days=90)
            next_date_format = next_date.strftime("%d/%m/%Y")

            #inserimento nuova riga, trasposizione e concatenazione
            new_row = pandas.Series({"id":totrows,
                                     "Codice": codice,
                                     "Tipo intervento": tipo_int,
                                     "Data programmata":next_date_format})
            df3 = pandas.concat([df_updated,new_row.to_frame().T],ignore_index = True)
            df_clean = df3.fillna(" ")
            manutenzione = df_clean.to_csv(path_or_buf="anagrafica/manutenzioni.csv",index=False)

#TODO: next step to use one and only object Checklist() to optimize code
