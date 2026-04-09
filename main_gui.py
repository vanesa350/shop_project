'''Licensed to the Apache Software Foundation (ASF) under one
or more contributor license agreements.  See the NOTICE file
distributed with this work for additional information
regarding copyright ownership.  The ASF licenses this file
to you under the Apache License, Version 2.0 (the
"License"); you may not use this file except in compliance
with the License.  You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing,
software distributed under the License is distributed on an
"AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
KIND, either express or implied.  See the License for the
specific language governing permissions and limitations
under the License. '''
import tkinter as tk #tkinter bibl ar saisinajumu tk
from tkinter import messagebox #imp messagebox prieks kludu pazinojumiem
from models import Store, Cart #imp store un cart klases no models.py
from storage import StorageHandler #imp storagehandler klasi no storage.py
import os #!!!!imp os moduli failu celiem un operaciju veiksanai!!!!
from login_widget import show_login

DATA_DIR = os.path.normpath(os.path.join(os.path.dirname(__file__), 'data')) #nosaka celu uz direktoriju 
ENC_FILE = os.path.join(DATA_DIR, 'products.json.enc') #cels uz sifreto failu direktorija
KEY_FILE = os.path.join(DATA_DIR, 'key.key') #cels uz key.key(palaizot data.py izveidojas)

class GUI: #klase 
    def __init__(self, root): #inicialize gui un sanem tkinter rootu
        self.root = root #saglaba ka atributu instancem
        self.root.title("Maza interneta veikala simulācija") #virsraksts
        self.storage = StorageHandler(KEY_FILE) #atslegas parvaldibai
        try: #meginajums ieladet vekala datus
            self.store = Store.load_from_file(ENC_FILE, self.storage) #ielade Store obj no sifreta
        except FileNotFoundError: #nav atrsts fails
            messagebox.showerror("kluda", "vispirms data.py un tad sis") #parada kludu
            raise #partrauc darbu
        except Exception as e: #atrod citu darbibu
            messagebox.showerror("kluda", f"neieladejas dati {e}") #kludas zinojums
            raise #partrauc darbu

        self.cart = Cart() #jauna Cart ins
        self.build_ui() #lietotajs var lietot
        self.update_list() #atjauno datus
        show_login(on_success=self.on_login_success, master=self.root)

    # PIEVIENOTS: Klases metode, kas izpildās pēc veiksmīgas pieteikšanās
    def on_login_success(self, username):
        print("Logged in as", username)
        self.status_label.config(text=f"Sistēmā pieslēdzies: {username}")

    def build_ui(self): #metode ka lietotajs var lietot
        frame = tk.Frame(self.root, padx=10, pady=10) #ramis
        frame.pack() #pievieno rami

        self.listbox = tk.Listbox(frame, width=70, height=12) #produktu saraksta attelosanai
        self.listbox.grid(row=0, column=0, columnspan=3, pady=(0,10)) #ieliek rami ka tabula

        tk.Label(frame, text="Daudzums:").grid(row=1, column=0, sticky='e') #pieliek daudzumu otraja rinda pirmaja kolonna un izlidzina pa labi
        self.qty_entry = tk.Entry(frame, width=8) #daudzuma ievadei
        self.qty_entry.grid(row=1, column=1, sticky='w') #novieto kur bus ta daudzuma ievade
        self.qty_entry.insert(0, "1") #noklusejuma vertiba 1

        tk.Button(frame, text="Pievienot grozam", command=self.add_to_cart, width=18).grid(row=2, column=0, pady=6) #poga
        tk.Button(frame, text="Apskatīt grozu", command=self.view_cart, width=18).grid(row=2, column=1, pady=6) #poga
        tk.Button(frame, text="Noformēt pirkumu", command=self.checkout, width=18).grid(row=2, column=2, pady=6) #poga

        self.status_label = tk.Label(self.root, text="", anchor='w') #stat etikete root loga
        self.status_label.pack(fill='x', padx=10, pady=(6,0)) #stat etikete ko paplasina horiziontali ar atkapi

    def update_list(self): #atjauno sarakstu
        self.listbox.delete(0, tk.END) #notira visu saturu
        for p in self.store.list_products(): #parbauda un atgriez visu kas iznaca
            self.listbox.insert(tk.END, f"{p.id} | {p.name} | Cena: {p.price:.2f}€ | Noliktavā: {p.stock}") #ievieto jauno info

    def add_to_cart(self): #def pievienosanai groza
        sel = self.listbox.curselection() #izveleta sanemsana
        if not sel: #ja nav izvelets
            messagebox.showwarning("Brīdinājums", "Izvēlieties produktu") #bridinajums
            return #partrauc izpildi
        idx = sel[0] #sanem izveleto indexu
        line = self.listbox.get(idx) #iegust ierakstito
        product_id = line.split('|')[0].strip() #sadala ar | lai izveletos id
        try: 
            qty = int(self.qty_entry.get()) #megina parverst par veselu skaitli
        except ValueError: #nepareiza vertiba
            messagebox.showerror("Kļūda", "Ievadiet skaitlisku daudzumu") #nebija ievadits teksts
            return #partrauc izpildi
        prod = self.store.get_product(product_id) #iegust produktu id
        if not prod: #ja neatrod
            messagebox.showerror("Kļūda", "Produkts nav atrasts") #parada kludu
            return #partrauc darbu
        if qty > prod.stock: #ja ievaditais lielaks par pieejamo
            messagebox.showerror("Kļūda", "Nepietiek noliktavā") #kluda
            return #partrauc darbu
        try: 
            self.cart.add(product_id, qty) #pievieno id un daudzumu
            self.status_label.config(text=f"Pievienots: {prod.name} x{qty}") #parada ka pievienots un daudzums
        except ValueError as e: #ja nav pareizais ievadits
            messagebox.showerror("Kļūda", str(e)) #kluda

    def view_cart(self): #def skatit cart
        if not self.cart.items: #ja nav neka
            messagebox.showinfo("Grozs", "Grozs ir tukšs") #kluda
            return #partrauc darbu
        lines = [] #saraksts
        for pid, qty in self.cart.items.items(): #iet cauri sarakstam prieks id un daudzuma
            p = self.store.get_product(pid) #produkta obj no store pec id
            if p: #ja produkts eksiste
                lines.append(f"{p.name} x{qty} = {p.price * qty:.2f}€") #pievieno rindu ar nosauk, daudz, summu
        lines.append(f"Kopā: {self.cart.total(self.store.products):.2f}€") #rinda ar kop summu
        messagebox.showinfo("Grozs", "\n".join(lines)) #info logs 
    
    def checkout(self): #pirkuma noform
        if not self.cart.items: #ja tukss grozs
            messagebox.showwarning("Brīdinājums", "Grozs ir tukšs") #zina/kluda
            return #partrauc darbu
        try:
            for pid, qty in list(self.cart.items.items()): #mekle groza saraksta
                self.store.reduce_stock(pid, qty) #samazina noliktavas skaitu
            self.store.save_file(ENC_FILE) #saglaba datus
            self.cart.clear() #tukss grozs pec noformesanas
            self.update_list() #atjauno gui
            self.status_label.config(text="Pirkums veiksmīgi noformēts") #viss labi
            messagebox.showinfo("Veiksmīgi", "Pirkums noformēts un dati saglabāti") #apstiprina ka viss labi
        except ValueError as e: #kluda
            messagebox.showerror("Kļūda", str(e)) #kludas zinojums
        except Exception as e: #atrod parejas kludas ja ir
            messagebox.showerror("Kļūda", f"Nezināma kļūda: {e}") #atzime nezinamu ja ieprieksejie nenokera

if __name__ == "__main__": #parbauda skriptu
    root = tk.Tk() #galv root no tkiter
    app = GUI(root) #inic gui class
    root.mainloop() #ciklam