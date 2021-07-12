from types import new_class
import pygame
import sys
import random

from pygame.event import set_blocked

pygame.init()
tekst = pygame.font.SysFont('Comic Sans MS', 30)
wymiary = szerokosc, wysokosc = 840, 840
ekran = pygame.display.set_mode(wymiary)


class Plansza:
    def __init__(self, ilosc_x, ilosc_y, odstep_gora=60, odstep_boki=10):
        self.plansza_x = ilosc_x
        self.plansza_y = ilosc_y
        self.odstep_gora = odstep_gora
        self.odstep_boki = odstep_boki
        self.pola = []
        self.dodaj_pola()
        pass

    def dodaj_pola(self):
        for j in range(0, self.plansza_y):
            for i in range(0, self.plansza_x):
                self.pola.append(Pole(i+j*self.plansza_y, 40*i+self.odstep_boki,
                                 40*j+self.odstep_gora, ekran, j, [0, 0, 0]))

    def rysuj(self):
        for p in self.pola:
            p.rysuj()

    def wstaw_bomby(self):
        ilosc_bomb = int(self.plansza_x * self.plansza_y * 0.13)

        bomby = random.sample(
            range(self.plansza_x * self.plansza_y), ilosc_bomb)
        for i in bomby:
            self.pola[i].stan = [0, 1, 0, 0, 0]

        for j in bomby:
            self.pola[j].sprawdz_numer(
                self.plansza_x, self.plansza_y, self.pola)

    def zakoncz_gre(self):
        print('koniec')
        for pole in self.pola:
            if pole.stan[1]:
                pole.stan[2] = True
                pole.rysuj()

    def sprawdz_pole_klikniete(self, mysza):
        # self.pola
        # print(f'x {mysza[0]} i y {mysza[1]}')
        for pl in self.pola:
            if(pl.rect.collidepoint(mysza)):  # interakcja z polem klikniętym
                if pl.stan[1]:
                    self.zakoncz_gre()
                else:
                    pl.stan[2] = True
                    pl.sprawdz_numer(self.plansza_x, self.plansza_y, self.pola)
                    pl.odkryj(self.plansza_x, self.plansza_y, self.pola)
                # print(f'Nr kliknietego {pl.nr}')


class Pole:
    def __init__(self, nr, x, y, ekran, rzad, kolor=[0, 0, 0], wymiar_x=40, wymiar_y=40,):
        self.nr = nr
        self.x = x
        self.y = y
        self.wymiar_x = wymiar_x
        self.wymiar_y = wymiar_y
        self.ekran = ekran
        self.kolor = kolor
        self.stan = [1, 0, 0, 0, 0]  # [puste,bomba,klikniete,flaga,pytajnik]
        self.numer = 0
        self.rzad = rzad
        pass

    def sprawdz_numer(self, plansza_x, plansza_y, plansza_pola):
        if self.stan[1]:
            r = plansza_x
            n = self.nr
            maks = plansza_x * plansza_y - 1

            if(n-r >= 0):  # nad bezpośrednio
                plansza_pola[n-r].numer += 1
            if(n+r <= maks):  # pod bezpośrednio
                plansza_pola[n+r].numer += 1
            if(n-1 >= 0 and plansza_pola[n-1].rzad == self.rzad):  # lewo
                plansza_pola[n-1].numer += 1
            if(n+1 <= maks and plansza_pola[n+1].rzad == self.rzad):  # prawo
                plansza_pola[n+1].numer += 1
            if(n-r-1 >= 0 and plansza_pola[n-r-1].rzad == self.rzad-1):  # lewa góra
                plansza_pola[n-r-1].numer += 1
            # lewy dół
            if(n+r-1 <= maks and plansza_pola[n+r-1].rzad == self.rzad+1):
                plansza_pola[n+r-1].numer += 1
            # prawa góra
            if(n-r+1 >= 0 and plansza_pola[n-r+1].rzad == self.rzad-1):
                plansza_pola[n-r+1].numer += 1
            # prawy dół
            if(n+r+1 <= maks and plansza_pola[n+r+1].rzad == self.rzad+1):
                plansza_pola[n+r+1].numer += 1

    def rysuj(self):
        if self.stan[2]:  # klikniete
            if self.stan[1]:  # bomba
                self.kolor = [255, 0, 0]
                pygame.draw.rect(self.ekran, self.kolor, pygame.Rect(
                    self.x, self.y, self.wymiar_x, self.wymiar_y))
                self.ekran.blit(tekst.render("*", False, (0, 0, 0)),
                                dest=(self.x+self.wymiar_x/2-8, self.y))
            elif self.numer > 0:
                self.ekran.blit(tekst.render("{}".format(self.numer), False, (0, 0, 0)),
                                dest=(self.x+self.wymiar_x/2-8, self.y))
            elif self.numer == 0:
                self.kolor = [155, 78, 0]
                pygame.draw.rect(self.ekran, self.kolor, pygame.Rect(
                    self.x, self.y, self.wymiar_x, self.wymiar_y))

        self.rect = pygame.draw.rect(self.ekran, self.kolor, pygame.Rect(
            self.x, self.y, self.wymiar_x, self.wymiar_y), 1, 1)

    def odkryj(self, plansza_x, plansza_y, plansza_pola):
        if self.numer == 0:
            r = plansza_x
            n = self.nr
            maks = plansza_x * plansza_y - 1
            self.stan[2] = True

            # nad bezpośrednio
            if(n-r >= 0 and plansza_pola[n-r].numer == 0 and not plansza_pola[n-r].stan[2]):
                plansza_pola[n-r].odkryj(plansza_x, plansza_y, plansza_pola)
            if(n+r <= maks):  # pod bezpośrednio
                plansza_pola[n+r].odkryj(plansza_x, plansza_y, plansza_pola)
            # lewo
            if(n-1 >= 0 and plansza_pola[n-1].numer == 0 and not plansza_pola[n-1].stan[2] and plansza_pola[n-1].rzad == self.rzad):
                plansza_pola[n-1].odkryj(plansza_x, plansza_y, plansza_pola)
            # prawo
            if(n+1 <= maks and plansza_pola[n+1].numer == 0 and not plansza_pola[n+1].stan[2] and plansza_pola[n+1].rzad == self.rzad):
                plansza_pola[n+1].odkryj(plansza_x, plansza_y, plansza_pola)
            # lewa góra
            if(n-r-1 >= 0 and plansza_pola[n-r-1].numer == 0 and not plansza_pola[n-r-1].stan[2] and plansza_pola[n-r-1].rzad == self.rzad-1):
                plansza_pola[n-r-1].odkryj(plansza_x, plansza_y, plansza_pola)
            # lewy dół
            if(n+r-1 <= maks and plansza_pola[n+r-1].numer == 0 and not plansza_pola[n+r-1].stan[2] and plansza_pola[n+r-1].rzad == self.rzad+1):
                plansza_pola[n+r-1].odkryj(plansza_x, plansza_y, plansza_pola)
            # prawa góra
            if(n-r+1 >= 0 and plansza_pola[n-r+1].numer == 0 and not plansza_pola[n-r+1].stan[2] and plansza_pola[n-r+1].rzad == self.rzad-1):
                plansza_pola[n-r+1].odkryj(plansza_x, plansza_y, plansza_pola)
            # prawy dół
            if(n+r+1 <= maks and plansza_pola[n+r+1].numer == 0 and not plansza_pola[n+r+1].stan[2] and plansza_pola[n+r+1].rzad == self.rzad+1):
                plansza_pola[n+r+1].odkryj(plansza_x, plansza_y, plansza_pola)
            self.rysuj()


plansza = Plansza(10, 10)
plansza.wstaw_bomby()
# plansza.pola[60].sprawdz_numer(plansza.pola)
mysz = pygame.mouse
while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if mysz.get_pressed(num_buttons=3) == (1, 0, 0):
                # print("klik {}".format(mysz.get_pos()))
                plansza.sprawdz_pole_klikniete(mysz.get_pos())

    ekran.fill([255, 255, 255])
    plansza.rysuj()
    pygame.display.flip()
    pygame.time.delay(10)
