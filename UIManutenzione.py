from tkinter.ttk import Treeview
import pandas
from datetime import datetime
from UIChecklist import *

global count
count = 0

class Manutenzioni:

    def __init__(self,codice):


        self.manut_window = Toplevel()
        self.manut_window.title("Manutenzioni attrezzature")
        self.manut_window.config(width=2500, height=1000)
        self.codice_iniziale = codice

        #treeview per manutenzioni
        self.manut_tree = Treeview(self.manut_window, columns=("id","Codice","Matricola", "Tipologia", "Descrizione",
                                                                "Commessa","Tipo intervento","Data programmata","Data intervento","Note"))

        self.manut_tree.column("#0", width=0,minwidth=0)
        self.manut_tree.column("id",width=0,minwidth=0)
        self.manut_tree.column("Codice", width=20)
        self.manut_tree.column("Matricola", width=120)
        self.manut_tree.column("Tipologia", width=120)
        self.manut_tree.column("Descrizione", width=120)
        self.manut_tree.column("Commessa", width=120)
        self.manut_tree.column("Tipo intervento", width=120)
        self.manut_tree.column("Data programmata", width=120)
        self.manut_tree.column("Data intervento", width=120)
        self.manut_tree.column("Note", width=120)

        self.manut_tree.heading("id", text="id")
        self.manut_tree.heading("Codice", text="Codice")
        self.manut_tree.heading("Matricola", text="Matricola")
        self.manut_tree.heading("Tipologia", text="Tipologia")
        self.manut_tree.heading("Descrizione", text="Descrizione")
        self.manut_tree.heading("Commessa", text="Commessa")
        self.manut_tree.heading("Tipo intervento", text="Tipo intervento")
        self.manut_tree.heading("Data programmata", text="Data programmata")
        self.manut_tree.heading("Data intervento", text="Data intervento")
        self.manut_tree.heading("Note", text="Note")

        self.checklist_button= Button(self.manut_window, text="Gestisci", command=self.checklist_start)

        self.tipo_vista_button = Button(self.manut_window,text="Vedi da effettuare", command=self.change_view)

        self.filtro_data_lbl = Label(self.manut_window, text="Filtro date",width=20)
        self.data_da_lbl = Label(self.manut_window, text="Dal", width=20)
        self.data_da_entry = Entry(self.manut_window,width=20)
        self.data_a_lbl = Label(self.manut_window, text="al", width=20)
        self.data_a_entry = Entry(self.manut_window,width=20)
        self.data_button = Button(self.manut_window,width=20,text="Filtra",command=self.date_filter)



        #Posizione
        self.tipo_vista_button.grid(row=0,column=0,pady=10,padx=10,sticky="w")

        self.filtro_data_lbl.grid(row=1, column=0, sticky="w")
        self.data_da_lbl.grid(row=1, column=1, sticky="w")
        self.data_da_entry.grid(row=1, column=2, sticky="w")
        self.data_a_lbl.grid(row=1, column=3, sticky="w")
        self.data_a_entry.grid(row=1, column=4, sticky="w")
        self.data_button.grid(row=1, column=5, sticky="w")

        self.manut_tree.grid(row=2,column=0,pady=10,padx=10,columnspan=5)

        self.checklist_button.grid(row=3,column=0,pady=10,padx=10)



        self.populate_tree(codice=self.codice_iniziale, date=" ")

        self.manut_window.mainloop()

    def checklist_start(self):
        """Start new chacklist based on the treeview selection"""
        tipo_attr = self.manut_tree.item(self.manut_tree.selection())['values'][4]
        matr= self.manut_tree.item(self.manut_tree.selection())['values'][2]
        tipo = self.manut_tree.item(self.manut_tree.selection())['values'][3]
        comm = self.manut_tree.item(self.manut_tree.selection())['values'][5]
        riga = self.manut_tree.item(self.manut_tree.selection())['values'][0]
        print (f"Lavori sulla riga {riga}, {tipo}{comm}{matr}")
        if tipo_attr =="Aspiratore":
            checklist_window = Aspiratore(matr,tipo,comm,riga)
        elif tipo_attr =="Lavasciuga":
            checklist_window = Lavasciuga(matr,tipo,comm,riga)



    def tree_values(self,starting_df):
        """Insert rows in treeview starting from an existing DataFrame. Starting_df:Pandas.Dataframe"""
        global count
        df_dict_man = starting_df.to_dict(orient="records")
        tot_rows = len(starting_df)
        count=0
        self.manut_tree.delete(*self.manut_tree.get_children())

        for r in range(0,tot_rows):
            cod_attr =df_dict_man[r]["Codice"]
            df_dict_ana = self.search_attr(cod_attr)
            cod_dict = list(df_dict_ana["Codice"])[0]

            self.manut_tree.insert(parent='',index=END,iid=count,values=[df_dict_man[r]["id"],
                                                                         df_dict_man[r]["Codice"],
                                                                         df_dict_ana["Matricola"][cod_dict],
                                                                         df_dict_ana["Tipologia"][cod_dict],
                                                                         df_dict_ana["Descrizione"][cod_dict],
                                                                         df_dict_ana["Commessa"][cod_dict],
                                                                          df_dict_man[r]["Tipo intervento"],
                                                                          df_dict_man[r]["Data programmata"],
                                                                          df_dict_man[r]["Data intervento"],
                                                                         df_dict_man[r]["Note"]])

            count+=1

    def populate_tree(self,codice,date):
        """fill the Treeview with all values from manutenzioni.csv"""
        file = pandas.read_csv("anagrafica/manutenzioni.csv")
        df_file_start = pandas.DataFrame(file)

        codice = self.codice_iniziale
        if codice == "all" and date =="all":
            df_file_man = df_file_start
        elif codice != "all"and date == "all":
            df_file_man=df_file_start[df_file_start["Codice"]==codice]
        elif date==" ":
            df_file_man = df_file_start[df_file_start["Data intervento"] == date]
        #elif codice =="all" and isinstance(date,datetime):
        else:
            df_file_man=df_file_start[df_file_start["Data intervento"]>=date]
        self.tree_values(df_file_man)


    def search_attr(self,codice):
        """return dictionary of the values corresponding to codice in anagrafica.csv"""
        file = pandas.read_csv("anagrafica/anagrafica.csv")
        df_file_ana = pandas.DataFrame(file)

        df_newfile = df_file_ana[(df_file_ana["Codice"]==codice)]
        df_newfile_dict = df_newfile.to_dict()

        return df_newfile_dict

    def change_view(self):
        """Changes data shown in treeview"""
        data_zero = datetime(1900,1,1)
        data_zero_format = data_zero.strftime("%d/%m/%Y")
        actual_view= self.manut_tree.item(0)["values"][8]

        if actual_view ==" ":
            self.tipo_vista_button.config(text="Vedi da effettuare")
            self.populate_tree(codice="all",date=data_zero_format)
        else:
            self.tipo_vista_button.config(text="Vedi effettuate")
            self.populate_tree(codice="all",date=" ")

    def date_filter(self):
        """Filter the data shown by the treeview beetweeen the data given in the form"""
        from_date = self.data_da_entry.get()
        to_date = self.data_a_entry.get()
        date_format = '%d/%m/%Y'
        newdate_from = datetime.strptime(from_date, date_format)
        newdate_to = datetime.strptime(to_date, date_format)
        da_data = newdate_from.strftime("%Y-%m-%d")
        a_data = newdate_to.strftime("%Y-%m-%d")

        self.populate_tree2(date_from=da_data,date_to=a_data)


    def populate_tree2(self,codice="all",date="all",date_to="0",date_from="0"):
        """fill the Treeview with all values from manutenzioni.csv"""
        file = pandas.read_csv("anagrafica/manutenzioni.csv")
        df_file_start = pandas.DataFrame(file)

        codice = self.codice_iniziale
        if date_to =="0" or date_from=="0":
            if codice == "all" and date =="all":
                df_file_man = df_file_start
            elif codice != "all"and date == "all":
                df_file_man=df_file_start[df_file_start["Codice"]==codice]
            elif date==" ":
                df_file_man = df_file_start[df_file_start["Data intervento"] == date]
            else:
                df_file_man=df_file_start[df_file_start["Data intervento"]>=date]
        else:
            view_type = self.tipo_vista_button["text"]
            data_zero = datetime(1990,1,1)
            data_zero_format = data_zero.strftime("%d/%m/%Y")
            if view_type == "Vedi effettuate":
                df_1 = df_file_start[df_file_start["Data intervento"]==" "]
                #df_1 = df_file_start[df_file_start["Data intervento"]>=date_zero]
            else:
                df_1 = df_file_start[df_file_start["Data intervento"] >= data_zero_format]
                #df_1 = df_file_start[df_file_start["Data intervento"]==" "]
            df_conv =pandas.to_datetime(df_1["Data programmata"],dayfirst=True,format="%d/%m/%Y")
            mask = (df_conv>=date_from)&(df_conv<=date_to)
            df_file_man = df_1.loc[mask]
        self.tree_values(df_file_man)