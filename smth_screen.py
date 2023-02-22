import pygame
import sys
from load_smth import load_image


pygame.init()
sector = 0
size = width, height = 1500, 800
screen = pygame.display.set_mode(size)


def terminate():  # выход из игры(егор)
    pygame.quit()
    sys.exit()


def start_screen(wid, heig):  # загрузка начального экрана(егор)
    intro_text = ["Master of dungeon", "",
                  "Правила игры",
                  "Собирайте очки чтобы победить монстров,",
                  "Чтобы перейти на следующий уровень войдите в красный портал",
                  'Чтобы начать игру заново нажмите кнопку SPACE']

    fon = pygame.transform.scale(load_image('fon.png'), (wid, heig))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, True, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return

        pygame.display.flip()


def death_screen(wid, heig):  # загрузка экрана смерти(ярик)
    pygame.mixer.music.load('data/death.mp3')
    pygame.mixer.music.play(0)
    intro_text = ["", "",
                  " ",
                  " ",
                  " "]

    fon = pygame.transform.scale(load_image('fon1.jpg'), (wid, heig))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 80)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, True, pygame.Color('RED'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                pygame.mixer.music.pause()
                pygame.mixer.music.load('data/game_music.mp3')
                pygame.mixer.music.play(-1)
                pygame.mixer.music.set_volume(0.2)
                return
        pygame.display.flip()
