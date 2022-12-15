import mysql.connector
import PySimpleGUI as sg


'''ŁĄCZENIE SIE Z BAZA DANYCH'''
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="autobarman",
    database="barman"
)
mycursor = mydb.cursor()

class User:
    def __init__(self, nazwa):
        self.nazwa = nazwa

def logging_window():
    layout2 = [
        [sg.T("Podaj login:")],
        [sg.I(key="-LOGIN-")],
        [sg.B("ZALOGUJ")],
    ]
    window2 = sg.Window("Logowanie", layout2)
    while True:
        event, values = window2.read()
        if event in (sg.WINDOW_CLOSED,):
            window2.close()
            break
        if event == "ZALOGUJ":
            global Uzytkownik_barman
            uzytkownik=values["-LOGIN-"]
            '''LOGOWANIE'''
            users = []
            f = open("użytkownicy_barman.txt")
            for x in f:
                users.append(x)
            f.close()
            Uzytkownik = uzytkownik
            if Uzytkownik in users:
                Uzytkownik_barman = User(Uzytkownik)
            else:
                f = open("użytkownicy_barman.txt", "a")
                f.write("\n" + Uzytkownik)
                f.close()
                Uzytkownik_barman = User(Uzytkownik)
            window2.close()
            main_window()
            return Uzytkownik_barman
            break

class Operacje:
    def dodaj(self):
        nowy_drink = "INSERT INTO drinki (nazwa, wodka, tequila, rum, gin, cola, tonic, Uzytkownik) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        nowy_szczegoly = (
            self.nazwa, self.skladniki[0], self.skladniki[1], self.skladniki[2], self.skladniki[3],
            self.skladniki[4], self.skladniki[5], Uzytkownik_barman.nazwa)
        mycursor.execute(nowy_drink, nowy_szczegoly)
        mydb.commit()
        print("Drink dodany.")

    def zrob(self):
        zapytanie = "SELECT wodka, tequila, rum, gin, cola, tonic FROM drinki WHERE nazwa = (%s) AND Uzytkownik = (%s)"
        reszta = (self.nazwa, Uzytkownik_barman.nazwa)
        mycursor.execute(zapytanie, reszta)
        przygotowanie = mycursor.fetchone()
        return przygotowanie

    def usun(self):
        usuniecie = ("DELETE FROM drinki WHERE nazwa = (%s) AND Uzytkownik = (%s)")
        reszta = (self.nazwa, Uzytkownik_barman.nazwa)
        mycursor.execute(usuniecie, reszta)
        mydb.commit()
        print("Drink usunięty.")

    def wymiensklad(self):
        dane = self.zrob()
        x = 0
        wypelnienie = []
        for dana in dane:
            if dana != '0':
                wypelnienie = wypelnienie + [[sg.T(' ' + self.dostepne_skladniki[x] + ': ' + dana + 'ml')]]
            x = x + 1
        return wypelnienie


class Drink(Operacje):
    def __init__(self, nazwa, skladniki=[]):
        self.nazwa = nazwa
        self.skladniki = skladniki
        self.dostepne_skladniki = ['wódka', 'tequila', 'rum', 'gin', 'cola', 'tonic']


class DrinkAlk(Drink):
    def wymiensklad(self):
        dane = self.zrob()
        x = 0
        wypelnienie = [[sg.T("W TYM DRINKU JEST ALKOHOL")]]
        for dana in dane:
            if dana != '0':
                wypelnienie = wypelnienie + [[sg.T(' ' + self.dostepne_skladniki[x] + ': ' + dana + 'ml')]]
            x = x + 1
        return wypelnienie


class DrinkBezalk(Drink):
    def wymiensklad(self):
        dane = self.zrob()
        x = 0
        wypelnienie = [[sg.T("W TYM DRINKU NIE MA ALKOHOLU")]]
        for dana in dane:
            if dana != '0':
                wypelnienie = wypelnienie + [[sg.T(' ' + self.dostepne_skladniki[x] + ': ' + dana + 'ml')]]
            x = x + 1
        return wypelnienie

def add_window():
    layout3 = [
        [sg.T("Nazwa:")],
        [sg.I(key="-NOWANAZWA-")],
        [sg.T("Ilość wódki w ml:")],
        [sg.I(key="-WOD-")],
        [sg.T("Ilość tequili w ml:")],
        [sg.I(key="-TEQ-")],
        [sg.T("Ilość rumu w ml:")],
        [sg.I(key="-RUM-")],
        [sg.T("Ilość ginu w ml:")],
        [sg.I(key="-GIN-")],
        [sg.T("Ilość coli w ml:")],
        [sg.I(key="-COL-")],
        [sg.T("Ilość tonicu w ml:")],
        [sg.I(key="-TON-")],
        [sg.B("DODAJ")],
        [sg.B("POWRÓT")],
    ]
    window3 = sg.Window("Dodaj Drinka", layout3)
    while True:
        event, values = window3.read()
        if event in (sg.WINDOW_CLOSED,):
            window3.close()
            break
        if event == "POWRÓT":
            window3.close()
            main_window()
        if event == "DODAJ":
            wod = values["-WOD-"]
            teq = values["-TEQ-"]
            rum = values["-RUM-"]
            gin = values["-GIN-"]
            col = values["-COL-"]
            ton = values["-TON-"]
            nowa_nazwa = values["-NOWANAZWA-"]
            nowe_skladniki = [wod, teq, rum, gin, col, ton]
            if wod == '0' and teq == '0' and rum == '0' and gin == '0':
                nowydrink = DrinkBezalk(nowa_nazwa, nowe_skladniki)
            else:
                nowydrink = DrinkAlk(nowa_nazwa, nowe_skladniki)
            nowydrink.dodaj()
            window3.close()
            main_window()
            break

def remove_window():
    jeden = ("SELECT nazwa FROM drinki WHERE Uzytkownik = (%s)")
    dwa = (Uzytkownik_barman.nazwa,)
    mycursor.execute(jeden, dwa)
    lista_drinkow = mycursor.fetchall()
    if lista_drinkow == []:
        wypelnienie = [sg.T("Najpierw musisz coś dodać")], [sg.B("DODAJ DRINKA")]
        layout4 = [
            [sg.T("Dostępne Drinki:")],
            wypelnienie,
            [sg.B("POWRÓT")],
        ]
    else:
        layout4 = [[sg.T("Wybierz drinka, którego chcesz usunąć:")]]
        wypelnienie = [[sg.B(drink[0])] for drink in lista_drinkow]
        koniec = [[sg.B("POWRÓT")]]
        layout4 = layout4 + wypelnienie + koniec
    window4 = sg.Window("Usuń Drinka", layout4)
    while True:
        event, values = window4.read()
        if event in (sg.WINDOW_CLOSED,):
            window4.close()
            break
        if event == "POWRÓT":
            window4.close()
            main_window()
        for drink in lista_drinkow:
            if event == drink[0]:
                juz_nie_drineczek = Drink(drink[0])
                juz_nie_drineczek.usun()
                window4.close()
                main_window()
                break
        if event == "DODAJ DRINKA":
            window4.close()
            add_window()
            break

def make_window():
    jeden = ("SELECT nazwa FROM drinki WHERE Uzytkownik = (%s)")
    dwa = (Uzytkownik_barman.nazwa,)
    mycursor.execute(jeden, dwa)
    lista_drinkow = mycursor.fetchall()
    if lista_drinkow == []:
        wypelnienie = [sg.T("Najpierw musisz coś dodać")], [sg.B("DODAJ DRINKA")]
        layout5 = [
            [sg.T("Dostępne Drinki:")],
            wypelnienie,
            [sg.B("POWRÓT")],
        ]
    else:
        layout5 = [[sg.T("Wybierz drinka, którego chcesz zrobić:")]]
        wypelnienie = [[sg.B(drink[0])] for drink in lista_drinkow]
        koniec = [[sg.B("POWRÓT")]]
        layout5 = layout5 + wypelnienie + koniec
    window5 = sg.Window("Zrób Drinka", layout5)
    while True:
        event, values = window5.read()
        if event in (sg.WINDOW_CLOSED,):
            window5.close()
            break
        if event == "POWRÓT":
            window5.close()
            main_window()
        for drink in lista_drinkow:
            if event == drink[0]:
                drineczek = Drink(drink[0])
                przygotowanie = drineczek.zrob()
                global drineczek_wybrany
                if przygotowanie[0] == '0' and przygotowanie[1] == '0' and przygotowanie[2] == '0' and przygotowanie[3] == '0':
                    drineczek_wybrany = DrinkBezalk(drink[0])
                else:
                    drineczek_wybrany = DrinkAlk(drink[0])
                window5.close()
                ingredients_window()
                break
        if event == "DODAJ DRINKA":
            window5.close()
            add_window()
            break

def ingredients_window():
    layout6 = [[sg.T("Skład tego drinka to:")]]
    wypelnienie = drineczek_wybrany.wymiensklad()
    koniec = [[sg.T("Odpowiada ci to?")], [sg.B("TAK")], [sg.B("NIE")]]
    layout6 = layout6 + wypelnienie + koniec

    window6 = sg.Window("Skład", layout6)
    while True:
        event, values = window6.read()
        if event in (sg.WINDOW_CLOSED,):
            window6.close()
            break
        if event == "TAK":
            window6.close()
            cheers_window()
            break
        if event == "NIE":
            window6.close()
            make_window()
            break

def cheers_window():
    layout7 = [
        [sg.T("SMACZNEGO!")],
        [sg.B("POWRÓT")],
    ]
    window7 = sg.Window("Smacznego (Teraz wysyłają się dane do robota)", layout7)
    while True:
        event, values = window7.read()
        if event in (sg.WINDOW_CLOSED,):
            window7.close()
            break
        if event == "POWRÓT":
            window7.close()
            main_window()
            break

def main_window():
    layout1 = [
        [sg.B("DODAJ DRINKA")],
        [sg.B("USUŃ DRINKA")],
        [sg.B("ZRÓB DRINKA")],
        [sg.B("ZMIEŃ UŻYTKOWNIKA")],
    ]
    window1 = sg.Window("Menu główne", layout1)
    while True:
        event, values = window1.read()
        if event in (sg.WINDOW_CLOSED,):
            window1.close()
            break
        if event == "DODAJ DRINKA":
            window1.close()
            add_window()
            break
        if event == "USUŃ DRINKA":
            window1.close()
            remove_window()
            break
        if event == "ZRÓB DRINKA":
            window1.close()
            make_window()
            break
        if event == "ZMIEŃ UŻYTKOWNIKA":
            window1.close()
            logging_window()
            break

logging_window()








'''
class User:
    def __init__(self,nazwa):
        self.nazwa = nazwa

users=[]
f = open("użytkownicy_barman.txt")
for x in f:
  users.append(x)
f.close()
Uzytkownik = input("Podaj nazwę użytkownika:")
if Uzytkownik in users:
    Uzytkownik_barman = User(Uzytkownik)
else:
    f = open("użytkownicy_barman.txt","a")
    f.write("\n" + Uzytkownik)
    f.close()
    Uzytkownik_barman = User(Uzytkownik)

class Operacje:
    def dodaj(self):
        nowy_drink = "INSERT INTO drinki (nazwa, wodka, tequila, rum, gin, cola, tonic, Uzytkownik) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        nowy_szczegoly = (self.nazwa, self.skladniki[0], self.skladniki[1], self.skladniki[2], self.skladniki[3], self.skladniki[4], self.skladniki[5], Uzytkownik_barman.nazwa)
        mycursor.execute(nowy_drink, nowy_szczegoly)
        mydb.commit()
        print("Drink dodany.")
    def zrob(self):
        zapytanie = "SELECT wodka, tequila, rum, gin, cola, tonic FROM drinki WHERE nazwa = (%s) AND Uzytkownik = (%s)"
        reszta =  (self.nazwa, Uzytkownik_barman.nazwa)
        mycursor.execute(zapytanie, reszta)
        przygotowanie = mycursor.fetchone()
        return przygotowanie
    def usun(self):
        usuniecie = ("DELETE FROM drinki WHERE nazwa = (%s) AND Uzytkownik = (%s)")
        reszta =  (self.nazwa, Uzytkownik_barman.nazwa)
        mycursor.execute(usuniecie, reszta)
        mydb.commit()
        print("Drink usunięty.")
    def wymiensklad(self):
        print("\nSKŁADNIKI TEGO DRINKA TO:")
        dane = self.zrob()
        x = 0
        for dana in dane:
            if dana != '0':
                print(' ' + self.dostepne_skladniki[x] + ': ' + dana + 'ml')
            x = x + 1

class Drink(Operacje):
    def __init__(self, nazwa, skladniki=[]):
        self.nazwa = nazwa
        self.skladniki = skladniki
        self.dostepne_skladniki = ['wódka', 'tequila', 'rum', 'gin', 'cola', 'tonic']

class DrinkAlk(Drink):
    def wymiensklad(self):
        print("\nW TYM DRINKU JEST ALKOHOL")
        print("\nSKŁADNIKI TEGO DRINKA TO:")
        dane = self.zrob()
        x = 0
        for dana in dane:
            if dana != '0':
                print(' ' + self.dostepne_skladniki[x] + ': ' + dana + 'ml')
            x = x + 1

class DrinkBezalk(Drink):
    def wymiensklad(self):
        print("\nW TYM DRINKU NIE MA ALKOHOLU")
        print("\nSKŁADNIKI TEGO DRINKA TO:")
        dane = self.zrob()
        x = 0
        for dana in dane:
            if dana != '0':
                print(' ' + self.dostepne_skladniki[x] + ': ' + dana + 'ml')
            x = x + 1

print('\nWITAJ!')
temp=0
while temp==0:
    print('\nCO CHCESZ ZROBIĆ?')
    print(' 1.NAPIĆ SIE CZEGOŚ Z LISTY \n 2.DODAĆ DRINKA DO LISTY \n 3.USUNĄĆ DRINKA Z LISTY')
    opt = int(input('WYBIERZ NUMER OPCJI:'))

    if opt == 2:
        nowa_nazwa = input('WPISZ NAZWĘ SWOJEGO NOWEGO DRINKA: ')
        print("\nDOSTĘPNE SKŁADNIKI TO: WÓDKA, TEQUILA, RUM, GIN, COLA, TONIC")
        wod = input('\nWPISZ ILOŚĆ WÓDKI [ML]: ')
        teq = input('WPISZ ILOŚĆ TEQUILI [ML]: ')
        rum = input('WPISZ ILOŚĆ RUMU [ML]: ')
        gin = input('WPISZ ILOŚĆ GINU [ML]: ')
        col = input('WPISZ ILOŚĆ COLI [ML]: ')
        ton = input('WPISZ ILOŚĆ TONICU [ML]: ')
        nowe_skladniki = [wod, teq, rum, gin, col, ton]
        if wod == '0' and teq == '0' and rum == '0' and gin == '0':
            nowydrink = DrinkBezalk(nowa_nazwa, nowe_skladniki)
        else:
            nowydrink = DrinkAlk(nowa_nazwa, nowe_skladniki)
        nowydrink.dodaj()
    elif opt == 3:
        print("\nDOSTĘPNE DRINKI:")
        jeden=("SELECT nazwa FROM drinki WHERE Uzytkownik = (%s)")
        dwa=(Uzytkownik_barman.nazwa, )
        mycursor.execute(jeden, dwa)
        lista_drinkow = mycursor.fetchall()
        if lista_drinkow == []:
            print("\nNajpierw musisz coś dodać:)))")
            continue
        else:
            idx = 1
            lista = []
            for drink in lista_drinkow:
                print(' ' + str(idx) + '.' + drink[0])
                lista.append(drink[0])
                idx += 1
            nr1 = input('WYBIERZ NUMER DRINKA KTÓREGO CHCESZ USUNĄĆ: ')
            juz_nie_drineczek = Drink(lista[int(nr1) - 1])
            juz_nie_drineczek.usun()
    else:
        jeden = ("SELECT nazwa FROM drinki WHERE Uzytkownik = (%s)")
        dwa = (Uzytkownik_barman.nazwa, )
        mycursor.execute(jeden, dwa)
        print("\nDOSTĘPNE DRINKI:")
        lista_drinkow = mycursor.fetchall()
        idx=1
        lista=[]
        if lista_drinkow == []:
            print("\nNajpierw musisz coś dodać:)))")
            continue
        else:
            for drink in lista_drinkow:
                print(' ' + str(idx) + '.' + drink[0])
                lista.append(drink[0])
                idx += 1
            nr2 = input('WYBIERZ NUMER DRINKA KTÓREGO CHCESZ ZROBIĆ: ')
            drineczek = Drink(lista[int(nr2) - 1])
            przygotowanie = drineczek.zrob()
            if przygotowanie[0]=='0' and przygotowanie[1]=='0' and przygotowanie[2]=='0' and przygotowanie[3]=='0':
                drineczek = DrinkBezalk(lista[int(nr2) - 1])
                print("\nSKŁADNIKI TEGO DRINKA TO:")
                drineczek.wymiensklad()
            else:
                drineczek = DrinkAlk(lista[int(nr2) - 1])
                print("\nSKŁADNIKI TEGO DRINKA TO:")
                drineczek.wymiensklad()
            print("\nODPOWIADA CI TO?\n 1.NIE\n 2.TAK")
            decyzja = int(input("WYBIERZ NUMER ODPOWIEDZI:"))
            if decyzja == 1:
                continue
            elif decyzja == 2:
                print(przygotowanie)
                temp = 1
                print("\nSMACZNEGO!")
'''