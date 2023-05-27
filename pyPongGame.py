# pyPong v. 0.1
# technologia - python3.10
# aplikacja pyPong demonstruje działanie biblioteki pygames

import pygame
import sys
from pygame.locals import *

# uruchomienie biblioteki pygame
pygame.init()

# ustawienie rozmiarów pola gry
POLEGRY_SZER = 800
POLEGRY_WYS = 450
KOLOR_POLA = (0, 144, 0)  # oraz jego barwy, składowe RGB

# inicjalizcja pola gry
polegry = pygame.display.set_mode((POLEGRY_SZER, POLEGRY_WYS), 0, 32)
pygame.display.set_caption('Prosty Pong')  # tytuł pola gry na pasku nagłówka

# ELEMENTY POLA GRY ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# wymiary paletek -----------------------------------------------------
PALETKA_SZER = 100  # szerokość
PALETKA_WYS = 20    # wysokość
# paletka gracza ------------------------------------------------------
PALETKA_G_KOLOR = (0, 90, 250)  # kolor wypełnienia - NIEBIESKI
PALETKA_G_POZ = (350, 400)  # początkowa pozycja paletki
# utworzenie powierzchni paletki, wypełnienie jej kolorem,
paletka1 = pygame.Surface([PALETKA_SZER, PALETKA_WYS])
paletka1.fill(PALETKA_G_KOLOR)
# ustawienie prostokąta zawierającego paletkę w początkowej pozycji
paletka1_prost = paletka1.get_rect()
paletka1_prost.x = PALETKA_G_POZ[0]
paletka1_prost.y = PALETKA_G_POZ[1]
# paletka koniec -------------------------------------------------------

# powtarzalność klawiszy po wciśnięciu (delay, interval)
pygame.key.set_repeat(50, 25)

# paletka ai -----------------------------------------------------------
PALETKA_AI_KOLOR = (226, 34, 12)  # kolor wypełnienia - CZERWONY
PALETKA_AI_POZ = (350, 20)  # początkowa pozycja paletki
# utworzenie powierzchni paletki, wypełnienie jej kolorem,
paletkaAI = pygame.Surface([PALETKA_SZER, PALETKA_WYS])
paletkaAI.fill(PALETKA_AI_KOLOR)
# ustawienie prostokąta zawierającego paletkę w początkowej pozycji
paletkaAI_prost = paletkaAI.get_rect()
paletkaAI_prost.x = PALETKA_AI_POZ[0]
paletkaAI_prost.y = PALETKA_AI_POZ[1]
# szybkość paletki AI
PREDKOSC_AI = 6.5
# paletka ai koniec ----------------------------------------------------

# piłka ----------------------------------------------------------------
P_SZER = 20  # szerokość
P_WYS = 20  # wysokość
P_PREDKOSC_X = 7  # prędkość pozioma x
P_PREDKOSC_Y = 7  # prędkość pionowa y
P_KOLOR = (250, 250, 0)  # kolor piłki
# utworzenie powierzchni piłki, narysowanie piłki i wypełnienie kolorem
pilka = pygame.Surface([P_SZER, P_WYS], pygame.SRCALPHA, 32).convert_alpha()
pygame.draw.ellipse(pilka, P_KOLOR, [0, 0, P_SZER, P_WYS])
# ustawienie prostokąta zawierającego piłkę w początkowej pozycji
pilka_prost = pilka.get_rect()
pilka_prost.x = POLEGRY_SZER / 2
pilka_prost.y = POLEGRY_WYS / 2
# piłka koniec ----------------------------------------------------------

# ustawienia animacji ###################################################
FPS = 30  # liczba klatek na sekundę
fpsClock = pygame.time.Clock()  # zegar śledzący czas

# WYNIKI GRY ###################################################
# zmienne przechowujące punkty i funkcje wyświetlające punkty
PKT_1 = '0'
PKT_AI = '0'
fontObj = pygame.font.Font('freesansbold.ttf', 56)  # czcionka napisów


def drukuj_punkty_g():
    tekst1 = fontObj.render(PKT_1, True, (16, 226, 226))
    tekst_prost1 = tekst1.get_rect()
    tekst_prost1.center = (POLEGRY_SZER / 2, POLEGRY_WYS * 0.75)
    polegry.blit(tekst1, tekst_prost1)


def drukuj_punkty_ai():
    tekst_ai = fontObj.render(PKT_AI, True, (16, 226, 226))
    tekst_prost_ai = tekst_ai.get_rect()
    tekst_prost_ai.center = (POLEGRY_SZER / 2, POLEGRY_WYS / 4)
    polegry.blit(tekst_ai, tekst_prost_ai)


# pętla główna programu *********************************************************
while True:
    # obsługa zdarzeń generowanych przez gracza
    for event in pygame.event.get():
        # przechwyć zamknięcie okna
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        # przechwyć ruch myszy
        if event.type == MOUSEMOTION:
            myszaX, myszaY = event.pos  # współrzędne x, y kursora myszy

            # oblicz przesunięcie paletki gracza
            przesuniecie = myszaX - (PALETKA_SZER / 2)

            # jeżeli wykraczamy poza okno gry w prawo
            if przesuniecie > POLEGRY_SZER - PALETKA_SZER:
                przesuniecie = POLEGRY_SZER - PALETKA_SZER

            # jeżeli wykraczamy poza okno gry w lewo
            if przesuniecie < 0:
                przesuniecie = 0

            # zaktualizuj położenie paletki w poziomie
            paletka1_prost.x = przesuniecie

        # przechwyć naciśnięcia klawiszy kursora
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                paletka1_prost.x -= 5
                if paletka1_prost.x < 0:
                    paletka1_prost.x = 0
            if event.key == pygame.K_RIGHT:
                paletka1_prost.x += 5
                if paletka1_prost.x > POLEGRY_SZER - PALETKA_SZER:
                    paletka1_prost.x = POLEGRY_SZER - PALETKA_SZER

    # ruch piłki ########################################################
    # przesuń piłkę po obsłużeniu zdarzeń
    pilka_prost.move_ip(P_PREDKOSC_X, P_PREDKOSC_Y)

    # jeżeli piłka wykracza poza pole gry
    # z lewej/prawej – odwracamy kierunek ruchu poziomego piłki
    if pilka_prost.right >= POLEGRY_SZER:
        P_PREDKOSC_X *= -1
    if pilka_prost.left <= 0:
        P_PREDKOSC_X *= -1

    if pilka_prost.top <= 0:  # piłka uciekła górą
        # P_PREDKOSC_Y *= -1  # odwracamy kierunek ruchu pionowego piłki
        pilka_prost.x = POLEGRY_SZER / 2  # więc startuję ze środka
        pilka_prost.y = POLEGRY_WYS / 2
        PKT_1 = str(int(PKT_1) + 1)

    if pilka_prost.bottom >= POLEGRY_WYS:  # piłka uciekła dołem
        pilka_prost.x = POLEGRY_SZER / 2  # więc startuję ze środka
        pilka_prost.y = POLEGRY_WYS / 2
        PKT_AI = str(int(PKT_AI) + 1)

    # jeżeli piłka dotknie paletki gracza, skieruj ją w przeciwną stronę
    if pilka_prost.colliderect(paletka1_prost):
        P_PREDKOSC_Y *= -1
        # zapobiegaj przysłanianiu paletki przez piłkę
        pilka_prost.bottom = paletka1_prost.top

    # AI (jak gra komputer) #############################################
    # jeżeli piłka ucieka na prawo, przesuń za nią paletkę
    if pilka_prost.centerx > paletkaAI_prost.centerx:
        paletkaAI_prost.x += PREDKOSC_AI
    # w przeciwnym wypadku przesuń w lewo
    elif pilka_prost.centerx < paletkaAI_prost.centerx:
        paletkaAI_prost.x -= PREDKOSC_AI

    # jeżeli piłka dotknie paletki AI, skieruj ją w przeciwną stronę
    if pilka_prost.colliderect(paletkaAI_prost):
        P_PREDKOSC_Y *= -1
        # uwzględnij nachodzenie paletki na piłkę (przysłonięcie)
        pilka_prost.top = paletkaAI_prost.bottom

    # rysowanie obiektów na polu gry
    polegry.fill(KOLOR_POLA)  # kolor pola gry
    drukuj_punkty_g()  # wyświetl punkty gracza
    drukuj_punkty_ai()   # wyświetl punkty AI

    # narysuj w oknie gry paletki
    polegry.blit(paletka1, paletka1_prost)
    polegry.blit(paletkaAI, paletkaAI_prost)
    # narysuj w oknie piłkę
    polegry.blit(pilka, pilka_prost)
    # aktualizacja pola gry
    pygame.display.update()

    # zaktualizuj zegar po narysowaniu obiektów
    fpsClock.tick(FPS)

# KONIEC
