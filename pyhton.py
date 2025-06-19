import pygame
import random

pygame.init()
pygame.mixer.init()

genislik, yukseklik = 1920, 1080
ekran = pygame.display.set_mode((genislik, yukseklik))
pygame.display.set_caption("Coin Toplama Oyunu")

font = pygame.font.SysFont("Arial", 40)
coin_sesi = pygame.mixer.Sound("Coin.mp3")
pygame.mixer.music.load("muzik.mp3")
pygame.mixer.music.play(-1)

arka_plan = pygame.transform.scale(pygame.image.load("arka_plan.png"), (genislik, yukseklik))

karakter_duruyor = pygame.transform.scale(pygame.image.load("karakter_duruyor.png"), (70, 70))
karakter_yuruyor1 = pygame.transform.scale(pygame.image.load("karakter_yuruyor1.png"), (70, 70))
karakter_yuruyor2 = pygame.transform.scale(pygame.image.load("karakter_yuruyor2.png"), (70, 70))
karakter_ziplama = pygame.transform.scale(pygame.image.load("karakter_ziplama.png"), (70, 70))
karakter_resmi = karakter_duruyor
coin_resmi = pygame.transform.scale(pygame.image.load("coin.png"), (50, 50))

def menu():
    while True:
        ekran.fill((200, 200, 200))
        baslik = font.render("Coin Toplama Oyunu", True, (0, 0, 0))
        ekran.blit(baslik, (genislik//2 - baslik.get_width()//2, 200))
        ekran.blit(font.render("Başlamak için Enter e bas", True, (0, 0, 255)), (genislik//2 - 150, 300))
        ekran.blit(font.render("Çıkmak için Esc ye bas", True, (255, 0, 0)), (genislik//2 - 150, 360))
        pygame.display.update()

        for e in pygame.event.get():
            if e.type == pygame.QUIT: exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RETURN: return
                if e.key == pygame.K_ESCAPE: exit()

def seviye_gecisi(seviye):
    ekran.fill((255, 255, 255))
    mesaj = font.render(f"{seviye}. Seviye Başlıyor! Devam etmek için bir tuşa bas...", True, (0, 0, 0))
    ekran.blit(mesaj, (genislik//2 - mesaj.get_width()//2, yukseklik//2))
    pygame.display.update()

    bekle = True
    while bekle:
        for e in pygame.event.get():
            if e.type == pygame.QUIT: exit()
            if e.type == pygame.KEYDOWN:
                bekle = False

menu()

x, y = 300, 880
hiz = 5
ziplaniyor = False
ziplama_gucu = 10
yercekimi = 0.5
hiz_y = 0
yer = 950

coin_x = random.randint(50, genislik - 50)
coin_y = random.randint(50, yukseklik - 50)
puan = 0
seviye = 1
maks_puan = 30
saat = pygame.time.Clock()
calisiyor = True

seviye_gecisi(seviye)

while calisiyor:
    saat.tick(60)
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            calisiyor = False

    tuslar = pygame.key.get_pressed()
    if tuslar[pygame.K_a]: x -= hiz
    if tuslar[pygame.K_d]: x += hiz
    if tuslar[pygame.K_w]: y -= hiz
    if tuslar[pygame.K_s]: y += hiz
    if tuslar[pygame.K_SPACE] and not ziplaniyor:
        ziplaniyor = True
        hiz_y = -ziplama_gucu

    if ziplaniyor:
        y += hiz_y
        hiz_y += yercekimi
        if y >= yer:
            y = yer
            ziplaniyor = False

    karakter_merkez = (x + 25, y + 25)
    coin_merkez = (coin_x + 15, coin_y + 15)
    mesafe = ((karakter_merkez[0] - coin_merkez[0]) ** 2 + (karakter_merkez[1] - coin_merkez[1]) ** 2) ** 0.5
    if mesafe < 40:
        puan += 1
        coin_sesi.play()
        coin_x = random.randint(50, genislik - 50)
        coin_y = random.randint(50, yukseklik - 50)

        if puan in [10, 20]:
            seviye += 1
            seviye_gecisi(seviye)
        elif puan >= maks_puan:
            ekran.fill((255, 255, 255))
            kazandin = font.render("Kazandın! Oyunu bitirdin!", True, (0, 200, 0))
            ekran.blit(kazandin, (genislik//2 - kazandin.get_width()//2, yukseklik//2))
            pygame.display.update()
            pygame.time.delay(3000)
            calisiyor = False

    if ziplaniyor and hiz_y < 0:
        karakter_resmi = karakter_ziplama
    else:
        karakter_resmi = karakter_duruyor

    ekran.blit(arka_plan, (0, 0))
    ekran.blit(karakter_resmi, (x, y))
    ekran.blit(coin_resmi, (coin_x, coin_y))
    surum = font.render("Sürüm: 1.0 Beta", True, (0, 0, 0))
    ekran.blit(surum, (genislik - surum.get_width() - 10, 10))
    ekran.blit(font.render(f"Puan: {puan}", True, (0, 0, 0)), (10, 10))
    ekran.blit(font.render(f"Seviye: {seviye}", True, (0, 0, 0)), (10, 50))
    pygame.display.update()

pygame.quit()
