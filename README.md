# top_machines
Get to know your cleaning machines and how to keep them going 

ENG 🇬🇧

Equipment Management – Desktop App with Tkinter
This application is designed to help manage company equipment and its maintenance, with a simple yet complete structure developed entirely in Python using Tkinter for the graphical interface.

▶️ Launching the Program
The main entry point of the application is the Principale.py file.
Running it will open a main window with two buttons:

Anagrafica: to add, search, and view equipment records.

Manutenzione: to consult and update maintenance activities.

📁 Project Structure
UIAnagrafica.py
Handles the equipment registry. From here you can:
Add new equipment (serial number, type, description, project, active status, deactivation date).
Search and filter equipment using various criteria.
View all registered equipment in a Treeview.
Create the first scheduled maintenance (in 90 days).
Access the maintenance records for a specific piece of equipment.

UIManutenzione.py
Displays the list of maintenance activities recorded in the manutenzioni.csv file. It offers:
Full or filtered view by date or status (to do / completed).
Automatic link to the equipment registry for additional data.
Access to the maintenance checklist, based on machine type.

UIChecklist.py
Contains operational checklists for:
Vacuum Cleaners
Scrubber Dryers
Each checklist includes a set of checks to be ticked. Upon confirmation:
The data is saved in the existing row in the manutenzioni.csv file.
A new row is automatically created for the next maintenance (after 90 days).

📂 Data Structure
All data is handled in .csv format:
anagrafica/anagrafica.csv: equipment records
anagrafica/manutenzioni.csv: maintenance history
anagrafica/commesse.csv: list of available projects

🧰 Requirements
Python 3.13

Python libraries:
tkinter
pandas
csv
datetime

▶️ Starting the Application
Make sure all .csv files are in the anagrafica/ folder, then run:

bash
Copy
Edit
python Principale.py

ITA 🇮🇹
# Gestione Attrezzature – App Desktop con Tkinter

Questa applicazione è pensata per aiutare nella gestione delle attrezzature aziendali e delle relative manutenzioni, con una struttura semplice ma completa sviluppata interamente in Python usando `Tkinter` per l'interfaccia grafica.

## ▶️ Avvio del programma

Il punto d'ingresso dell'applicazione è il file `Principale.py`.  
Lanciandolo si apre una finestra principale con due pulsanti:

- **Anagrafica**: per inserire, cercare e visualizzare le attrezzature.
- **Manutenzione**: per consultare e aggiornare gli interventi di manutenzione.

## 📁 Struttura del progetto

### `UIAnagrafica.py`

Permette di gestire l'anagrafica delle attrezzature. Da qui si possono:

- Aggiungere nuove attrezzature (matricola, tipologia, descrizione, commessa, attivo, data dismissione).
- Cercare e filtrare attrezzature con diversi criteri.
- Visualizzare tutte le attrezzature registrate tramite una `Treeview`.
- Creare la **prima manutenzione programmata** (tra 90 giorni).
- Accedere alle manutenzioni specifiche di una singola attrezzatura.

---

### `UIManutenzione.py`

Mostra l'elenco degli interventi di manutenzione registrati nel file `manutenzioni.csv`. Offre:

- Visualizzazione completa o filtrata per date o stato (da fare / effettuate).
- Collegamento automatico all’anagrafica per mostrare dati aggiuntivi.
- Accesso alla **checklist di manutenzione**, distinta per tipo macchina.

---

### `UIChecklist.py`

Contiene le checklist operative per:

- **Aspiratori**
- **Lavasciuga**

Ogni checklist presenta una serie di controlli da spuntare. Alla conferma:

1. I dati vengono salvati nella riga esistente nel file `manutenzioni.csv`.
2. Viene creata **automaticamente** una nuova riga per la prossima manutenzione (dopo 90 giorni).

## 📂 Struttura dei dati

Tutti i dati sono gestiti in formato `.csv`:

- `anagrafica/anagrafica.csv`: dati delle attrezzature
- `anagrafica/manutenzioni.csv`: cronologia delle manutenzioni
- `anagrafica/commesse.csv`: elenco delle commesse selezionabili

## 🧰 Requisiti

- Python 3.13
- Librerie Python:
  - `tkinter`
  - `pandas`
  - `csv`
  - `datetime`

## ▶️ Avvio dell'applicazione

Assicurati di avere tutti i file `.csv` nella cartella `anagrafica/`, poi esegui:

```bash
python Principale.py

