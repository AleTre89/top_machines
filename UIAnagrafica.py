"""
TkInter interface to visualize alla the machines from anagrafica.csv and:
- Button "Aggiungi": add new machines to anagrafica.csv by filling all the text and checkbox widgets
- Button "Cerca": search through anagrafica.csv by filling even partially only the necessary widgets
- Button "Manutenzioni": allows to see the next maintenance for the selected machine
- Button "Crea prima manutenzione": active only for new machines, creates the first manteinance 90 days later
"""


from datetime import datetime,timedelta
from tkinter import *
import csv
import pandas
from tkinter.ttk import Treeview, Combobox
from UIManutenzione import Manutenzioni

class Anagrafica:

    def __init__(self):
        self.anagr_window = Toplevel()
        self.anagr_window.title("Anagrafica")
        self.anagr_window.config(width=1000,height=600)

        #Labels, textbox, checkboxe positioning
        self.matr_label = Label(self.anagr_window,text="Matricola")
        self.matr_text = Entry(self.anagr_window,width=20)
        self.matr_label.grid(row=0,column=0,pady=10, padx=10)
        self.matr_text.grid(row=0,column=1, pady=10, padx=10)

        self.tipo_label = Label(self.anagr_window,text="Tipologia")
        self.tipo_text =Entry(self.anagr_window,width=20)
        self.tipo_label.grid(row=1,column=0,pady=10, padx=10)
        self.tipo_text.grid(row=1,column=1,pady=10, padx=10)

        self.descrizione_label = Label(self.anagr_window, text="Descrizione")
        self.descrizione_text = Combobox(self.anagr_window, values= ["Aspiratore","Lavasciuga"],width=15)
        self.descrizione_label.grid(row=2,column=0,pady=10, padx=10)
        self.descrizione_text.grid(row=2,column=1,pady=10, padx=10)

        #retrieves customer list for combobox
        file = pandas.read_csv("anagrafica/commesse.csv")
        df_commesse = pandas.DataFrame(file)
        elenco_comm = df_commesse["nomecomm"].to_list()

        self.commessa_label = Label(self.anagr_window,text="Commessa")
        self.commessa_label.grid(row=3,column=0,pady=10, padx=10)
        self.commessa_cbx = Combobox(self.anagr_window, values=elenco_comm,width=15)
        self.commessa_cbx.grid(row=3, column=1, pady=10, padx=10)


        self.attivo_label = Label(self.anagr_window,text="Attivo")
        self.attivo_text = Entry(self.anagr_window,width=20)
        self.attivo_label.grid(row=4,column=0,pady=10, padx=10)
        self.attivo_text.grid(row=4,column=1,pady=10, padx=10)

        self.data_dismiss_lbl = Label(self.anagr_window, text="Data dismissione")
        self.data_dismiss_txt = Entry(self.anagr_window,width=20)
        self.data_dismiss_lbl.grid(row=5, column=0, pady=10, padx=10)
        self.data_dismiss_txt.grid(row=5, column=1, pady=10, padx=10)

        self.aggiungi = Button(self.anagr_window, text="Aggiungi", command=self.add_attrezzatura)
        self.aggiungi.grid(row=6,column=0,pady=10, padx=10)

        self.cerca = Button(self.anagr_window, text="Cerca", command=self.search_attrezzatura)
        self.cerca.grid(row=6,column=1,pady=10, padx=10)

        self.vedi_man = Button(self.anagr_window, text="Manutenzioni", command=self.search_man)
        self.vedi_man.grid(row=6,column=2,pady=10, padx=10,sticky="w")

        #TREEVIEW
        self.elenco_tree= Treeview(self.anagr_window,columns=("Codice","Matricola","Tipologia", "Descrizione",
                                                                "Commessa","Attivo","Dismissione"))


        self.elenco_tree.column("#0",width=15)
        self.elenco_tree.column("Codice",width=50)
        self.elenco_tree.column("Matricola", width=120)
        self.elenco_tree.column("Tipologia", width=120)
        self.elenco_tree.column("Descrizione", width=120)
        self.elenco_tree.column("Commessa", width=120)
        self.elenco_tree.column("Attivo", width=120)
        self.elenco_tree.column("Dismissione", width=120)

        self.elenco_tree.heading("#0",text="")
        self.elenco_tree.heading("Codice", text="Codice")
        self.elenco_tree.heading("Matricola", text="Matricola")
        self.elenco_tree.heading("Tipologia", text="Tipologia")
        self.elenco_tree.heading("Descrizione", text="Descrizione")
        self.elenco_tree.heading("Commessa", text="Commessa")
        self.elenco_tree.heading("Attivo", text="Attivo")
        self.elenco_tree.heading("Dismissione", text="Dismesso il")


        self.elenco_tree.grid(row=0,column=2, padx=10,rowspan=6,columnspan=2)

        #Firts maintenance Button and positioning
        self.prima_man = Button(self.anagr_window, text="Crea prima manutenzione", command=self.first_man,
                                state="disabled")
        self.prima_man.grid(row=6, column=3, pady=10, padx=10, sticky="w")


        def activate_first_man(event):
            """Searches if selected machine has scheduled maintenance.
            If positive, first manteinance button will be disabled"""
            self.elenco_tree = event.widget
            codice = self.elenco_tree.item(self.elenco_tree.selection())['values'][0]
            base = pandas.read_csv("anagrafica/manutenzioni.csv")
            df = pandas.DataFrame(base)
            lista_codici = df["Codice"].to_list()
            if codice in lista_codici:
                self.prima_man.config(state="disabled")
            else:
                self.prima_man.config(state="normal")

        self.elenco_tree.bind("<<TreeviewSelect>>", activate_first_man)

        global count
        count=0
        self.populate_tree()

        file = pandas.read_csv("anagrafica/anagrafica.csv")
        df_file = pandas.DataFrame(file)
        self.last_code= df_file["Codice"].max()


        self.anagr_window.mainloop()

    def tree_values(self,starting_df):
        """Insert rows in treeview starting from an existing DataFrame. Starting_df:Pandas.Dataframe"""
        global count
        df_dict = starting_df.to_dict(orient="records")
        tot_rows = len(starting_df)

        self.elenco_tree.delete(*self.elenco_tree.get_children())

        for r in range(0,tot_rows):
            self.elenco_tree.insert(parent='',index=END,iid=count,values=[df_dict[r]["Codice"],
                                                                          df_dict[r]["Matricola"],
                                                                          df_dict[r]["Tipologia"],
                                                                          df_dict[r]["Descrizione"],
                                                                          df_dict[r]["Commessa"],
                                                                          df_dict[r]["Attivo"],
                                                                          df_dict[r]["Data dismissione"]])

            count+=1

    def populate_tree(self):
        """fill the Treeview with all values from anagrafica.csv"""
        file = pandas.read_csv("anagrafica/anagrafica.csv")
        df_file = pandas.DataFrame(file)

        self.tree_values(df_file)


    def add_attrezzatura(self):
        """Add new line in anagrafica.csv getting Text widgets values. New line will be shown automatically"""

        cod= self.last_code+1
        matr=self.matr_text.get()
        tipo=self.tipo_text.get()
        descr=self.descrizione_text.get()
        comm=self.commessa_cbx.get()
        attivo=self.attivo_text.get()
        datadism=self.data_dismiss_txt.get()

        with open("anagrafica/anagrafica.csv",mode="a",newline="") as file:
            writer=csv.writer(file)
            writer.writerow([cod,matr,tipo,descr,comm,attivo,datadism])
        self.populate_tree()

        self.matr_text.delete(0,END)
        self.descrizione_text.delete(0,END)
        self.tipo_text.delete(0,END)
        self.commessa_cbx.delete(0,END)
        self.attivo_text.delete(0,END)
        self.data_dismiss_txt.delete(0,END)

    def search_attrezzatura(self):
        """Filter Treeview using values from Text widgets"""
        matr=self.matr_text.get()
        tipo=self.tipo_text.get()
        desc=self.descrizione_text.get()
        comm=self.commessa_cbx.get()
        att=self.attivo_text.get()
        dism=self.data_dismiss_txt.get()


        file = pandas.read_csv("anagrafica/anagrafica.csv")
        df_file = pandas.DataFrame(file)
        df_newfile_final = df_file[(df_file["Matricola"].str.contains(matr)) &
                                   (df_file["Descrizione"].str.contains(desc)) &
                                   (df_file["Tipologia"].str.contains(tipo)) &
                                   (df_file["Commessa"].str.contains(comm)) &
                                   (df_file["Attivo"].str.contains(att))]
                                   #(df_file["Data dismissione"] == (dism))]
        print(df_newfile_final)

        self.tree_values(df_newfile_final)

    def search_man(self):
        codice = self.elenco_tree.item(self.elenco_tree.selection())['values'][0]
        print(codice)
        manutenzioni_window = Manutenzioni(codice=codice)

    def first_man(self):
        """Creates the first row in manutenzioni.csv if no maintenance has already been scheduled """
        base = pandas.read_csv("anagrafica/manutenzioni.csv")
        df = pandas.DataFrame(base)
        df_dict = df.to_dict(orient="records")
        totrows = len(df_dict)
        print(totrows)

        df_updated = pandas.DataFrame.from_dict(df_dict)

        # Creazione nuova riga
        # inserimento dati base
        codice = self.elenco_tree.item(self.elenco_tree.selection())['values'][0]
        tipo_int = "ordinario"
        # spostamento data avanti di 90gg
        date_today = datetime.today()
        next_date = date_today + timedelta(days=90)
        next_date_format = next_date.strftime("%d/%m/%Y")

        # inserimento nuova riga, trasposizione e concatenazione
        new_row = pandas.Series({"id": totrows,
                                 "Codice": codice,
                                 "Tipo intervento": tipo_int,
                                 "Data programmata": next_date_format})
        df3 = pandas.concat([df_updated, new_row.to_frame().T], ignore_index=True)
        df_clean = df3.fillna(" ")
        manutenzione = df_clean.to_csv(path_or_buf="anagrafica/manutenzioni.csv", index=False)
