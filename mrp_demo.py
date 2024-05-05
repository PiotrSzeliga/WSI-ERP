import tkinter as tk
from webbrowser import open_new

root = tk.Tk()
root.geometry("910x500")
root.resizable(width=False, height=False)
root.title("MRP 235032")

def callback(input):
        if input.isdigit():
            return True
        elif input == "":
            return True
        else:
            return False

magazyn = {
    "blaty": 1,
    "nogi": 1,
    "siedziska": 1,
    "nóżki": 1
} 

tabelka_czysta = {
    "Tydzień":              [x for x in range(1,10)],  
    "Zamówione stoły":      [0 for x in range(1,10)],
    "Zamówione krzesła":    [0 for x in range(1,10)],
    "Wstępne blaty":        [magazyn["blaty"] for x in range(1,10)],
    "Potrzebne blaty":      [0 for x in range(1,10)],
    "Wstępne nogi":         [magazyn["nogi"] for x in range(1,10)],
    "Potrzebne nogi":       [0 for x in range(1,10)],
    "Wstępne siedziska":    [magazyn["siedziska"] for x in range(1,10)],
    "Potrzebne siedziska":  [0 for x in range(1,10)],
    "Wstępne nóżki":        [magazyn["nóżki"] for x in range(1,10)],
    "Potrzebne nóżki":      [0 for x in range(1,10)],
}

tabelka = tabelka_czysta

def rysuj():
    counter = 0
    for i in tabelka.keys():
        k = tk.Entry(tableframe,relief="groove",bg="snow3",font=("Cambria",14),width=15)
        k.grid(row=counter, column=0,sticky="NS")
        k.insert(0,i)
        counter +=1
        counter2 = 1
        for j in tabelka[i]:
            e = tk.Entry(tableframe,relief="groove",bg="white",font=('Arial', 14),width=5)
            e.grid(row=counter-1, column=counter2,sticky="NS")
            e.insert(0, j)
            counter2 += 1

def zlecenie(dane):
    try:
        tydzień = dane[0]  
        stoły = dane[1] 
        krzesła = dane[2]
        zestaw = dane[3]
    except TypeError:
        return 
    #combo
    stoły += zestaw
    krzesła += 2*zestaw
    #warunki do sprawdzenia
    if stoły < 0 or krzesła < 0 or zestaw < 0:
        print("Zła ilość")
        return 
    if tydzień <= 0:
        print("Zły tydzień")
        return
    if tydzień-1 <= 0:
        print("Nie można ukończyć zlecenia na czas")
        return
    kolumna = ["Zamówione stoły","Zamówione krzesła","Wstępne blaty","Potrzebne blaty","Wstępne nogi","Potrzebne nogi","Wstępne siedziska","Potrzebne siedziska","Wstępne nóżki","Potrzebne nóżki"]
    #powiększenie tabelki jeżeli za mała
    if tydzień-1 > len(tabelka["Tydzień"]):
        for b in range(tydzień - len(tabelka["Tydzień"])):
            tabelka["Tydzień"].append(tabelka["Tydzień"][-1]+1)
            for c in kolumna:
                if c == "Wstępne blaty":
                    tabelka["Wstępne blaty"].append(tabelka["Wstępne blaty"][-1])
                elif c == "Wstępne nogi":
                    tabelka["Wstępne nogi"].append(tabelka["Wstępne nogi"][-1])
                elif c == "Wstępne siedziska":
                    tabelka["Wstępne siedziska"].append(tabelka["Wstępne siedziska"][-1])
                elif c == "Wstępne nóżki":
                    tabelka["Wstępne nóżki"].append(tabelka["Wstępne nóżki"][-1])
                else:
                    tabelka[f"{c}"].append(0)
    #zamówione stoły
    tabelka["Zamówione stoły"][tydzień-1] += stoły
    #zamówione krzesła
    tabelka["Zamówione krzesła"][tydzień-1] += krzesła
    #blaty
    if tabelka["Zamówione stoły"][tydzień-1]-tabelka["Wstępne blaty"][tydzień-2] >= 0:
        tabelka["Potrzebne blaty"][tydzień-2] = tabelka["Zamówione stoły"][tydzień-1]-tabelka["Wstępne blaty"][tydzień-1]      
        for i in range(len(tabelka["Tydzień"])-tydzień+1):
            tabelka["Wstępne blaty"][tydzień+i-1] = 0
    else:
        for i in range(len(tabelka["Tydzień"])-tydzień+1):
            tabelka["Wstępne blaty"][tydzień+i-1] = tabelka["Wstępne blaty"][tydzień-2]-tabelka["Zamówione stoły"][tydzień-1]
    #nogi
    if tabelka["Zamówione krzesła"][tydzień-1]-tabelka["Wstępne nogi"][tydzień-2] >= 0:
        tabelka["Potrzebne nogi"][tydzień-2] = 4*tabelka["Zamówione krzesła"][tydzień-1]-tabelka["Wstępne nogi"][tydzień-1]      
        for i in range(len(tabelka["Tydzień"])-tydzień+1):
            tabelka["Wstępne nogi"][tydzień+i-1] = 0
    else:
        for i in range(len(tabelka["Tydzień"])-tydzień+1):
            tabelka["Wstępne nogi"][tydzień+i-1] = tabelka["Wstępne nogi"][tydzień-2]-4*tabelka["Zamówione stoły"][tydzień-1]
    #siedziska
    if tabelka["Zamówione krzesła"][tydzień-1]-tabelka["Wstępne siedziska"][tydzień-2] >= 0:
        tabelka["Potrzebne siedziska"][tydzień-2] = tabelka["Zamówione krzesła"][tydzień-1]-tabelka["Wstępne siedziska"][tydzień-1]      
        for i in range(len(tabelka["Tydzień"])-tydzień+1):
            tabelka["Wstępne siedziska"][tydzień+i-1] = 0
    else:
        for i in range(len(tabelka["Tydzień"])-tydzień+1):
            tabelka["Wstępne siedziska"][tydzień+i-1] = tabelka["Wstępne siedziska"][tydzień-2]-tabelka["Zamówione krzesła"][tydzień-1]
    #nóżki
    if tabelka["Zamówione krzesła"][tydzień-1]-tabelka["Wstępne nóżki"][tydzień-2] >= 0:
        tabelka["Potrzebne nóżki"][tydzień-2] = 3*tabelka["Zamówione krzesła"][tydzień-1]-tabelka["Wstępne nóżki"][tydzień-1]      
        for i in range(len(tabelka["Tydzień"])-tydzień+1):
            tabelka["Wstępne nóżki"][tydzień+i-1] = 0
    else:
        for i in range(len(tabelka["Tydzień"])-tydzień+1):
            tabelka["Wstępne nóżki"][tydzień+i-1] = tabelka["Wstępne nóżki"][tydzień-2]-3*tabelka["Zamówione krzesła"][tydzień-1]
    #ostateczny output
    rysuj()



def zlecenie_okno(): 
    
    okno = tk.Toplevel(root)
    reg = okno.register(callback) 
    tk.Label(master=okno, text="Napisz, na który tydzień jest zlecenie\n(Można więcej niż w jest tabeli)").pack()
    tydzień = tk.Entry(master=okno,validate ="key",validatecommand =(reg, '%P'))
    tydzień.pack()
    tk.Label(master=okno, text="Ile stołów jest w zamówieniu?\n(Stół = 1 blat + 4 nogi)").pack()
    stół = tk.Entry(master=okno,validatecommand =(reg, '%P'))
    stół.pack()
    tk.Label(master=okno, text="Ile krzeseł jest w zamówieniu?\n(Krzesło = 1 siedzisko + 3 nózki)").pack()
    krzesło = tk.Entry(master=okno,validate ="key",validatecommand =(reg, '%P'))
    krzesło.pack()
    tk.Label(master=okno, text="Ile zestawów jest w zamówieniu?\n(Zestaw to stół+2*krzesło)").pack()
    zestaw = tk.Entry(master=okno,validate ="key",validatecommand =(reg, '%P'))
    zestaw.pack()
    
    def okno_zniszcz():  
       okno.destroy()
    
    def bierz():
            try:
                return(int(tydzień.get()),int(stół.get()),int(krzesło.get()),int(zestaw.get()))
            except ValueError:
                return None

    
    button4 = tk.Button(master=okno,text="Zatwierdź",font=("Cambria",18),command=lambda:[zlecenie(bierz()),okno_zniszcz()]).pack()
    okno.grab_set()

def strona(url="https://github.com/PiotrSzeliga/WSI-MRP"):
    open_new(url)

def rysuj_czyste(tabelka=tabelka):
    counter = 0
    for i in tabelka.keys():
        k = tk.Entry(tableframe,relief="groove",bg="snow3",font=("Cambria",14),width=15)
        k.grid(row=counter, column=0,sticky="NS")
        k.insert(0,i)
        counter +=1
        counter2 = 1
        for j in tabelka[i]:
            e = tk.Entry(tableframe,relief="groove",bg="white",font=('Arial', 14),width=5)
            e.grid(row=counter-1, column=counter2,sticky="NS")
            if counter-1 == 0:
                e.insert(0,counter2)
            else:
                e.insert(0, list(tabelka_czysta[i])[0])
            counter2 += 1
    tabelka = tabelka_czysta

buttonframe = tk.Frame(root,bg="white")
buttonframe.rowconfigure(0,weight=1)
buttonframe.rowconfigure(1,weight=1)
buttonframe.rowconfigure(2,weight=1)
buttonframe.pack(side="left",fill="y")
canvas = tk.Canvas(root,confine="false",bg="green")
canvas.pack(side="left",fill="y")
tableframe = tk.Frame(canvas,bg="red")
tableframe.rowconfigure(0,weight=1)
tableframe.rowconfigure(1,weight=1)
tableframe.rowconfigure(2,weight=1)
tableframe.rowconfigure(3,weight=1)
tableframe.rowconfigure(4,weight=1)
tableframe.rowconfigure(5,weight=1)
tableframe.rowconfigure(6,weight=1)
tableframe.rowconfigure(7,weight=1)
tableframe.rowconfigure(8,weight=1)
tableframe.rowconfigure(9,weight=1)
tableframe.rowconfigure(10,weight=1)
tableframe.pack(side="left",fill="y")
button1 = tk.Button(buttonframe, text="Dodaj zamówienie",font=("Cambria",18),command=zlecenie_okno)
button1.pack(fill="x")
button2 = tk.Button(buttonframe, text="Wyczyść tabelkę",font=("Cambria",18),command=rysuj_czyste)
button2.pack(fill="x")
button3 = tk.Button(buttonframe, text="Przejdź do github",font=("Cambria",18),command=strona)
button3.pack(side="bottom",fill="x")

rysuj()
root.mainloop()