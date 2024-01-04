import tkinter as tk
from tkinter import ttk


from xmlHelper import clientHandler,productHandler
from web3Interpreter import ClientInterface

############statics################
tokenContract="0x0A92f94579B117427c1416968d3288C995015255"
shopContract="0x7564D0ABB9c9AAAdff18259D1bA18F8827B2f0Ec"
######################################

class GUI():
    def __init__(self):
        #instantiem clientHandler-ul pentru a avea o interfata cu baza de date a utilizatorului
        self.cH=clientHandler("clientDatabase.xml")
        self._privateKey=self.cH.getPrivateKey()
        (self._name,self._surname,self._address,self._phone,self._email)=self.cH.getDetails()
        self._details=self._name+" "+self._surname+" "+self._address+" "+self._phone+" "+self._email

        #instantiem un handler pentru a avea o interfata cu blockchain-ul... il vom initializa din nou dupa ce vom face adaugarea datelor initiale
        self.web3cH=ClientInterface(self._privateKey,self._details,tokenContract,shopContract)

        #instantiem un handler pentru produse
        self.pH=productHandler("productDatabase.xml")



    def show_private_key_window(self):
        root = tk.Tk()  # Hidden root window
        root.withdraw()  # Hide the root window
        private_key_window = tk.Toplevel(root)
        private_key_window.title("Introducere Cheie Privată")
        private_key_window.geometry("270x350")

        #Adaugare stil (pentru buton)
        style = ttk.Style()
        style.configure("TButton", font=("Helvetica", 13))

        #Adaugare text
        textintr=ttk.Label(private_key_window,text="Momentan nu aveți configurată o cheie privată.\nPentru a face asta vă rugăm să o introduceți în căsuța de mai jos:",wraplength=230,justify="left",font=("Helvetica",13))
        textintr.pack(pady=10)
        # Adaugare buton lipire

        # Adaugare Entry widget pentru introducerea cheii private
        entry = ttk.Entry(private_key_window,font=("Helvetica",12))
        entry.pack(pady=10)
        paste_button = ttk.Button(private_key_window, text="Lipește", command=lambda: self.paste_from_clipboard(entry))
        paste_button.pack( pady=10)

        # Adaugare buton pentru a obține cheia privată
        button = ttk.Button(private_key_window, text="Confirmă cheia privată", command=lambda: self.get_private_key(entry.get(), root))
        button.pack(pady=10)
        tk.mainloop()

    def show_details_windows(self):
        root = tk.Tk()  # Hidden root window
        root.withdraw()  # Hide the root window
        private_key_window = tk.Toplevel(root)
        private_key_window.title("Introducere Cheie Privată")
        private_key_window.geometry("270x350")

        #Adaugare stil (pentru buton)
        style = ttk.Style()
        style.configure("TButton", font=("Helvetica", 13))

        #Adaugare text
        textintr=ttk.Label(private_key_window,text="Introduceți detaliile personale:",wraplength=230,justify="left",font=("Helvetica",13))
        textintr.pack(pady=10)
        #Adaugare in pentru date
        name_entry = ttk.Entry(private_key_window, font=("Helvetica", 12))
        name_entry.pack(pady=10)
        self.add_default_text(name_entry,"Introduceti numele...")

        surname_entry = ttk.Entry(private_key_window, font=("Helvetica", 12))
        surname_entry.pack(pady=10)
        self.add_default_text(surname_entry, "Introduceti prenumele...")

        address_entry = ttk.Entry(private_key_window, font=("Helvetica", 12))
        address_entry.pack(pady=10)
        self.add_default_text(address_entry, "Introduceti adresa...")

        phone_entry = ttk.Entry(private_key_window, font=("Helvetica", 12))
        phone_entry.pack(pady=10)
        self.add_default_text(phone_entry, "Introduceti telefonul...")

        email_entry = ttk.Entry(private_key_window, font=("Helvetica", 12))
        email_entry.pack(pady=10)
        self.add_default_text(email_entry, "Introduceti email-ul...")

        button = ttk.Button(private_key_window, text="Confirmă detaliile",
                            command=lambda: self.get_details(name_entry.get(),surname_entry.get(), address_entry.get(),phone_entry.get(),email_entry.get(),root))
        button.pack(pady=10)

        tk.mainloop()


    def get_private_key(self,private_key, root):
        self._privateKey=private_key
        self.cH.setPrivateKey(self._privateKey) #dupa ce am instantiat, o vom seta
        root.destroy()  # Close the root window after obtaining the private key


    def get_details(self,name,surname,address,phone,email, root):
        self._name=name
        self._surname=surname
        self._address=address
        self._phone=phone
        self._email=email
        self.cH.setDetails(self._name,self._surname,self._address,self._phone,self._email) #dupa ce le instantiem, le vom seta in baza de date
        root.destroy()  # Close the root window after obtaining the private key


    def paste_from_clipboard(self,entry):
        clipboard_text = entry.clipboard_get()
        entry.insert(tk.END, clipboard_text)

    def add_default_text(self,entry, default_text):
        entry.insert(0, default_text)
        entry.bind("<FocusIn>", lambda event: self.clear_default_text(entry, default_text))
        entry.bind("<FocusOut>", lambda event: self.restore_default_text(entry, default_text))

    def clear_default_text(self,entry, default_text):
        if entry.get() == default_text:
            entry.delete(0, tk.END)

    def restore_default_text(self,entry, default_text):
        if not entry.get():
            entry.insert(0, default_text)

    def isOutdated(self):
        if sorted(self.web3cH.getProductList())==sorted(self.pH.getProductListIDS()):
            return False
        return True


    def run(self):
        #daca nu avem cheie privata, vom face una(se trateaza exceptiile in interior)
        if self._privateKey==None:
            self.show_private_key_window()
        #daca nu avem detaliile setate, le vom seta
        if self._name==None or self._surname==None or self._email==None or self._address==None or self._phone==None:
            self.show_details_windows()
        #daca nu coincid bazele de date inseamna ca trebuie sa le sincronizam
        if self.isOutdated():
            print("Aplicatia necesita o sincronizare a bazelor de date")
            return 42


        return 0


gui=GUI()
code=gui.run()
print("Aplicatia a intors codul "+str(code))
