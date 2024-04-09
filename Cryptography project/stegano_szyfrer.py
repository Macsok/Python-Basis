from PIL import Image

def ustaw_parzystosc(parzystosc, krotka):
    """Ustawia pierwszy element z krotki na parzystosc zadana w argumencie 'parzystosc'"""
    # skupiamy sie tylko na pierwszym elemencie - w tym przypadku wartosc R z RGB pixela
    wartosc = int(krotka[0])

    # sprawdzamy parzystosc i zwracamy krotke bez zmian jesli sie zgadza z porzadana
    if wartosc % 2 == int(parzystosc):
        return krotka
    
    # zmienamy parzystosc, odejmujemy 1 od warotsci, jesli 0 to dodajemy
    if wartosc != 0:
        wartosc = wartosc - 1
    else:
        wartosc = wartosc + 1
    # zwracamy nowa krotke
    return (wartosc, krotka[1], krotka[2])
    
def parzystosc(krotka):
    """Zwraca parzysotsc pierwszego elementu w krotce"""
    if int(krotka[0]) % 2 == 0:
        return 0
    else:
        return 1

def szyfrowanie(sciezka_wejsciowa, zapisz_jako, tekst):
    """Szyfruje podany text w obrazie i zapisuje jako nowy obraz"""
    # otwarcie obrazu jako tablicy pixeli
    obraz = Image.open(sciezka_wejsciowa)
    pixel = obraz.load()

    # zamien tekst na reprezentacje bitowa
    tekst_binarnie = ''.join('{0:08b}'.format(ord(x), 'b') for x in tekst)

    # sprawdzenie dlugosci tekstu i zamienienie wartosci na binarna
    dlugosc = len(tekst_binarnie)
    dlugosc_binarnie = bin(dlugosc)[2:]
    # przeznaczamy 100 bitow na zapisanie dlugosci zaszyforwanego tekstu
    do_zapisu = '0' * (100 - len(dlugosc_binarnie)) + dlugosc_binarnie
    
    licznik = 0
    # dla kazdego pixela w obrazie
    for y in range(obraz.size[1]):
        for x in range(obraz.size[0]):
            if licznik < 100:
                # ustaw parzystosc
                pixel[x, y] = ustaw_parzystosc(do_zapisu[licznik], pixel[x, y])
            else:
                # odejmujemy 100 bo to indeks tablicy dlugosci tekstu
                pixel[x, y] = ustaw_parzystosc(tekst_binarnie[licznik - 100], pixel[x, y])
            # inkrementacja licznika
            licznik += 1
        # stop jesli skonczylismy pisanie
            if licznik >= dlugosc + 100:
                break
        if licznik >= dlugosc + 100:
            break
    # zapis nowego obrazu
    obraz.save(zapisz_jako, 'png')


def odszyfruj(image_path):
    """Odczytuje zaszyfrowany tekst z obrazu"""
    # wczytanie obrazu
    obraz = Image.open(image_path)
    pixel = obraz.load()

    # inicjalizacja zmiennych
    licznik = 0
    tekst = ''
    dlugosc_binarnie = ''
    czytaj_do = 1

    for y in range(obraz.size[1]):
        for x in range(obraz.size[0]):
            if licznik < 100:
                # dodajemy parzystosc odczytanego bita do tablicy
                dlugosc_binarnie += str(parzystosc(pixel[x, y]))

            # zamiana odczytanych wartosci na typ int
            if licznik == 100:
                czytaj_do = int(dlugosc_binarnie, 2)
                print(f'Dlugosc odczytanej wiadomosci w bitach: {czytaj_do}')

            # stop jesli wczystko przeczytane
            if czytaj_do <= 0:
                break

            if licznik >= 100:
                # dodanie wartosci binarnych do tablicy odszyfrowanej
                tekst += str(parzystosc(pixel[x, y]))
                # aktualizacja licznika odczytanych bitow
                czytaj_do -= 1
            
            # inkrementacja licznika
            licznik += 1
        # stop jesli wszystko przeczytane
        if czytaj_do <= 0:
            break

    # zamiana odczytanej wiadomosci binarnej na ANSI (symbole)
    czysty_tekst = ''
    for i in range(int(dlugosc_binarnie, 2) // 8):
        czysty_tekst += chr(int(tekst[i * 8 : (i + 1) * 8], 2))
    return czysty_tekst


def interfejs():
    inp = input('s - szyfrowanie, o - odczytanie, q - wyjscie: ')
    
    if inp == 's':
        plik_wejsciowy = input('Podaj plik wejsciowy: ')
        zapisz_jako = input('Zapisz jako [.png]: ')
        tekst = input('Tekst do zaszyfrowania: ')
        print('Szyfrowanie...')
        szyfrowanie(plik_wejsciowy, zapisz_jako, tekst)
        print('Zakonczono.')
    
    if inp == 'o':
        plik_wejsciowy = input('Plik do odczytu [.png]: ')
        print('Czytanie...')
        print('Odszyfrowany tekst:', odszyfruj(plik_wejsciowy))
    return 0

interfejs()