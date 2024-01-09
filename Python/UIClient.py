import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk


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

    def show_product_window(self,products):
        root = tk.Tk()
        root.title("Lista de Produse")

        def update_details(event):
            selected_index = product_listbox.curselection()
            if selected_index:
                selected_index = selected_index[0]
                selected_product = products[selected_index]
                details_text.delete(1.0, tk.END)
                details_text.insert(tk.END, f"Detalii: {selected_product['details']}")
                details_text.insert(tk.END, f"\nPret: {selected_product['pret']} lei")

                # Afișează imaginea produsului
                load_and_display_image(selected_product["image_path"])

        def add_to_cart():
            selected_index = product_listbox.curselection()
            if selected_index:
                selected_index = selected_index[0]
                selected_product = products[selected_index]

                # Adaugă produsul în coș
                found = False
                for     item in cart:
                    if item["id"] == selected_product["id"]:
                        item["quantity"] += 1
                        found = True
                        break

                if not found:
                    cart.append({"id": selected_product["id"], "name": selected_product["name"],"pret":selected_product["pret"], "quantity": 1})
                update_cart_label()

        def update_cart_label():
            #update la suma totala
            sum = 0
            for item in cart:
                sum += item['pret'] * item['quantity']

            #partea de afisare
            cart_contents_text = "\n".join([f"{item['name']} - {item['quantity']} buc." for item in cart])
            cart_contents_text+="\nTotal: "+str(sum)+" lei"
            cart_contents.set(cart_contents_text)

            walletText = "Portofelul tau: " + str(self.web3cH.getPublicAddress()) + "\nBalanta contului: " + str(self.web3cH.getLeiBalance()) + " lei"
            wallet_info_var.set(walletText)
        def submit():
            #vom extrage informatiile sub forma pe care ne-o cere programul in solidity
            sum = 0
            for item in cart:
                sum += item['pret'] * item['quantity']
            itemList=[]
            quantityList=[]
            for item in cart:
                itemList.append(int(item['id']))
                quantityList.append(int(item['quantity']))
            cart.clear()
            update_cart_label()
            if sum>self.web3cH.getLeiBalance():
                print("Nu aveti destui bani pentru a cumpara produsele")
                return 50
            #vom face apelul functiei aici
            myList=itemList+quantityList
            self.web3cH.BuyWithLei(myList,self._details)
            print("Ati cumparat produsele cu succes")

        def clear_cart():
            cart.clear()
            update_cart_label()



        def resize_image(image_path, target_width, target_height):
            original_image = Image.open(image_path)
            resized_image = original_image.resize((target_width, target_height))
            return ImageTk.PhotoImage(resized_image)

        def load_and_display_image(image_path):

            target_width = 150
            target_height = 100
            resized_image = resize_image(image_path, target_width, target_height)

            image_label.configure(image=resized_image)
            image_label.image = resized_image  # păstrează o referință la imagine pentru a evita garbage collection

        product_frame = ttk.Frame(root, padding="10")
        product_frame.grid(row=0, column=0)

        wallet_info_var = tk.StringVar()
        wallet_info=tk.Label(product_frame,height=3,width=50,textvariable=wallet_info_var)
        wallet_info.pack()

        product_listbox = tk.Listbox(product_frame, height=10, width=50)
        product_listbox.pack(side="left", fill="y")
        product_listbox.bind("<<ListboxSelect>>", update_details)

        details_frame = ttk.Frame(root, padding="10")
        details_frame.grid(row=0, column=1)

        details_text = tk.Text(details_frame, height=10, width=50)
        details_text.pack()


        image_label = ttk.Label(details_frame)
        image_label.pack()

        cart_frame = ttk.Frame(root, padding="10")
        cart_frame.grid(row=1, column=0, columnspan=2)

        cart_label = ttk.Label(cart_frame, text="Coșul tău:")
        cart_label.grid(row=0, column=0, sticky=tk.W)
        cart_contents = tk.StringVar()
        cart_contents_label = ttk.Label(cart_frame, textvariable=cart_contents)
        cart_contents_label.grid(row=1, column=0, sticky=tk.W)

        add_to_cart_button = ttk.Button(product_frame, text="Adaugă în Coș", command=add_to_cart)
        add_to_cart_button.pack(pady=10)

        delete_cart_button = ttk.Button(product_frame, text="Golește coșul", command=clear_cart)
        delete_cart_button.pack(pady=10)

        submit_button = ttk.Button(product_frame, text="Pune comanda", command=submit)
        submit_button.pack(pady=10)

        cart = []
        update_cart_label()
        for product in products:
            product_listbox.insert(tk.END, f"{product['id']} - {product['name']}")

        root.mainloop()
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
        try:
            self.authRun()
        except:
            print("A aparut o eroare in rularea programului")


        return 0

    def appendPrice(self,productList,priceTuple):
        for pereche in priceTuple:
            id=pereche[0]
            pret=pereche[1]
            for x in productList:

                if str(x['id'])==str(id):
                    x['pret']=pret
        return productList

    def authRun(self):
        testList=[]
        prods=self.pH.getProductList()
        for prod in prods:
            testList.append(prod.getData())
        #print(testList)

        #print(self.web3cH.getRawProductList())
        testList=self.appendPrice(testList,self.web3cH.getRawProductList())
        self.show_product_window(testList)


gui=GUI()
code=gui.run()


##TODO:istoric comenzi, maybe better view :), testare
