import pygame
import sys
from load_smth import load_image, load_level, load_points, load_level_player
from save_smth import save_points, save_level_player
from smth_screen import death_screen, start_screen, terminate

# глобальные переменные
pygame.init()
sector = 0
size = width, height = 1500, 800
screen = pygame.display.set_mode(size)
cou = 0
cou2 = 0
max_point = 70
level_player = 0

# загрузка картинок
tile_images = {
    'grass': load_image('grass.png'),
    'tree': load_image('tree.png', 'white'),
    'wall': load_image('wall.png'),
    'empty': load_image('floor.png'),
    'door_next': load_image('door_next.png', 'white'),
    'door_prev': load_image('door_prev.png', 'white'),
    'gem': load_image('gem.png', 'white'),
    'spike': load_image('spike.png', 'white'),
    'checkpoint': load_image('checkpoint.png', 'white'),
    'enemy0': load_image('enemy0.png'),
    'enemy1': load_image('enemy1.png', 'white'),
    'enemy2': load_image('enemy2.png'),
    'enemy3': load_image('enemy3.png', 'white'),
    'enemy4': load_image('enemy4.png'),
    'dead': load_image('dead.png')
}
player_image = load_image('knight.png', 'white')
tile_width = tile_height = 50
# основной персонаж
player = None

# группы спрайтов
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()


def save_level(kind, x, y):  # сохранение положения игрока на уровне(егор)
    filename = "data/" + f'sector{sector}.txt'
    # читаем уровень, убирая символы перевода строки
    if kind == 'normal':
        map_of_level[7][12] = '@'
    elif kind == 'quit':
        map_of_level[y][x] = '@'
    with open(filename, 'w') as mapFile:
        for y in map_of_level:
            mapFile.writelines(''.join(y) + '\n')


def up_level(points):  # повышение уровня игрока зависимое от колличества очков(ярик)
    global level_player
    if points < 1:
        level_player = 0
    elif points < 10:
        level_player = 1
    elif points < 15:
        level_player = 2
    elif points < 20:
        level_player = 3
    elif points < 25:
        level_player = 4
    elif points >= 25:
        level_player = 5


def remote_out(all_point):  # выведение на экран колличество очков(ярик)
    font = pygame.font.Font(None, 30)
    text = font.render(f"Points: {all_point}", True, (250, 42, 42))
    screen.blit(text, (10, 770))


def remote_load(level_pl):  # загрузка уровня(ярик)
    font = pygame.font.Font(None, 30)
    text = font.render(f"Level: {level_pl}", True, (250, 42, 42))
    screen.blit(text, (10, 750))


def final_screen():  # загрузка финального экрана(ярик)
    global width
    global height
    global all_points
    global level_player
    pygame.mixer.music.load('data/win.mp3')
    pygame.mixer.music.play(0)
    word = f'Вы набрали: {all_points}'
    if all_points == max_point:
        word = 'Вы набрали максимальное колличество очков: 70'
    intro_text = ["Поздравляем, вы прошли игру", "",
                  f"Ваш уровень: {level_player}",
                  word]

    fon = pygame.transform.scale(load_image('fon2.png'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, True, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    while True:
        for event_in in pygame.event.get():
            if event_in.type == pygame.QUIT:
                restart('total')
                terminate()
            elif event_in.type == pygame.KEYDOWN or \
                    event_in.type == pygame.MOUSEBUTTONDOWN:
                terminate()
        pygame.display.flip()


def generate_level(level):  # генерирование уровня(вместе)
    new_player, x, y = None, None, None
    global cou
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == ')':
                Tile('grass', x, y)
            elif level[y][x] == '/':
                Tile('grass', x, y)
                Tile('tree', x, y)
            elif level[y][x] == '%':
                Tile('grass', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            if sector == 3:
                if level[y][x] == '!':
                    Tile('grass', x, y)
                    Tile('door_prev', x, y)
            if sector != 0:
                if level[y][x] == '@' and cou == 0:
                    cou += 1
                    Tile('empty', x, y)
                    new_player = Player(x, y)
                    level[y][x] = '.'
                elif level[y][x] == '@' and cou != 0:
                    cou += 1
                    Tile('empty', x, y)
                    level[y][x] = '.'
                elif level[y][x] == '*':
                    Tile('empty', x, y)
                    Tile('gem', x, y)
                elif level[y][x] == '?':
                    Tile('empty', x, y)
                    Tile('door_next', x, y)
                elif level[y][x] == '!':
                    Tile('empty', x, y)
                    Tile('door_prev', x, y)
            if sector == 0:
                if level[y][x] == '@' and cou == 0:
                    cou += 1
                    Tile('grass', x, y)
                    new_player = Player(x, y)
                    level[y][x] = '%'
                elif level[y][x] == '@' and cou != 0:
                    cou += 1
                    Tile('grass', x, y)
                    level[y][x] = '%'
                elif level[y][x] == '*':
                    Tile('grass', x, y)
                    Tile('gem', x, y)
                elif level[y][x] == '?':
                    Tile('grass', x, y)
                    Tile('door_next', x, y)
                elif level[y][x] == '!':
                    Tile('grass', x, y)
                    Tile('door_prev', x, y)
            if sector == 3:
                if level[y][x] == '!':
                    Tile('grass', x, y)
                    Tile('door_prev', x, y)
            elif level[y][x] == '^':
                Tile('empty', x, y)
                Tile('spike', x, y)
            elif level[y][x] == '&':
                Tile('empty', x, y)
                Tile('checkpoint', x, y)
            elif level[y][x] == '0':
                Tile('empty', x, y)
                Tile('enemy0', x, y)
            elif level[y][x] == '1':
                Tile('empty', x, y)
                Tile('enemy1', x, y)
            elif level[y][x] == '2':
                Tile('empty', x, y)
                Tile('enemy2', x, y)
            elif level[y][x] == '3':
                Tile('empty', x, y)
                Tile('enemy3', x, y)
            elif level[y][x] == '4':
                Tile('empty', x, y)
                Tile('enemy4', x, y)
            elif level[y][x] == 'x':
                Tile('empty', x, y)
                Tile('dead', x, y)

    # вернем игрока, а также размер поля в клетках
    return new_player, x, y


def restart(how):  # обновление данных(егор)
    global sector
    global cou
    if how == 'normal':
        player.move_player(9, 7)
    if how == 'total':
        save_points(0)
        for i in range(4):
            with open(f'data/sector{i}_orig.txt', 'r') as original:
                level_map = original.readlines()
                with open(f'data/sector{i}.txt', 'w') as to_save:
                    for line in level_map:
                        to_save.writelines(line)


def movement(charec, direction):  # передвижение(егор)
    x, y = charec.positions
    global sector
    global map_of_level
    global all_points
    global gem_get_is
    global attack_is_1
    global save_coord
    if direction == 'down':
        if sector != 0:
            if map_of_level[y + 1][x] == '*' and y < border_y - 1:
                all_points += 1
                Tile('empty', x, y + 1)
                map_of_level[y + 1][x] = '.'
                gem_get_is = True
        if sector == 0:
            if map_of_level[y + 1][x] == '*' and y < border_y - 1:
                all_points += 1
                Tile('grass', x, y + 1)
                map_of_level[y + 1][x] = '%'
                gem_get_is = True
        if map_of_level[y + 1][x] == '0':
            if all_points >= 1 and y < border_y - 1:
                all_points += 1
                Tile('empty', x, y + 1)
                Tile('dead', x, y + 1)
                map_of_level[y + 1][x] = 'x'
                attack_is_1 = True
                save_coord = player.positions[0], player.positions[1]
                player_group.empty()
            else:
                death_screen(width, height)
                restart('normal')
        if map_of_level[y + 1][x] == '1':
            if all_points >= 10 and y < border_y - 1:
                all_points += 2
                Tile('empty', x, y + 1)
                Tile('dead', x, y + 1)
                map_of_level[y + 1][x] = 'x'
                attack_is_1 = True
                save_coord = player.positions[0], player.positions[1]
                player_group.empty()
            else:
                death_screen(width, height)
                restart('normal')
        if map_of_level[y + 1][x] == '2':
            if all_points >= 15 and y < border_y - 1:
                all_points += 3
                Tile('empty', x, y + 1)
                Tile('dead', x, y + 1)
                map_of_level[y + 1][x] = 'x'
                attack_is_1 = True
                save_coord = player.positions[0], player.positions[1]
                player_group.empty()
            else:
                death_screen(width, height)
                restart('normal')
        if map_of_level[y + 1][x] == '3':
            if all_points >= 25 and y < border_y - 1:
                all_points += 4
                Tile('empty', x, y + 1)
                Tile('dead', x, y + 1)
                map_of_level[y + 1][x] = 'x'
                attack_is_1 = True
                save_coord = player.positions[0], player.positions[1]
                player_group.empty()
            else:
                death_screen(width, height)
                restart('normal')
        if map_of_level[y + 1][x] == '4':
            death_screen(width, height)
            restart('normal')
        if map_of_level[y + 1][x] == '^' and y < border_y - 1:
            death_screen(width, height)
            restart('normal')
        if map_of_level[y + 1][x] == '?' and y < border_y - 1:
            save_level('normal', x, y)
            sector += 1
            map_of_level = load_level(f'sector{sector}.txt')
            generate_level(map_of_level)
            player.move_player(9, 6)
        if map_of_level[y + 1][x] == '!' and y < border_y - 1:
            save_level('normal', x, y)
            sector -= 1
            map_of_level = load_level(f'sector{sector}.txt')
            generate_level(map_of_level)
            player.move_player(4, 4)
        if y < border_y - 1 and map_of_level[y + 1][x] == '.' or map_of_level[y + 1][x] == '*' or \
                map_of_level[y + 1][x] == 'x' or map_of_level[y + 1][x] == '@' or map_of_level[y + 1][x] == '%':
            charec.move_player(x, y + 1)
    if direction == 'up':
        if sector != 0:
            if map_of_level[y - 1][x] == '*' and y > 0:
                all_points += 1
                Tile('empty', x, y - 1)
                map_of_level[y - 1][x] = '.'
                gem_get_is = True
        if sector == 0:
            if map_of_level[y - 1][x] == '*' and y > 0:
                all_points += 1
                Tile('grass', x, y - 1)
                map_of_level[y - 1][x] = '%'
                gem_get_is = True
        if map_of_level[y - 1][x] == '0':
            if all_points >= 1 and y > 0:
                all_points += 1
                Tile('empty', x, y - 1)
                Tile('dead', x, y - 1)
                map_of_level[y - 1][x] = 'x'
                attack_is_1 = True
                save_coord = player.positions[0], player.positions[1]
                player_group.empty()
            else:
                death_screen(width, height)
                restart('normal')
        if map_of_level[y - 1][x] == '1':
            if all_points >= 10 and y > 0:
                all_points += 2
                Tile('empty', x, y - 1)
                Tile('dead', x, y - 1)
                map_of_level[y - 1][x] = 'x'
                attack_is_1 = True
                save_coord = player.positions[0], player.positions[1]
                player_group.empty()
            else:
                death_screen(width, height)
                restart('normal')
        if map_of_level[y - 1][x] == '2':
            if all_points >= 15 and y > 0:
                all_points += 3
                Tile('empty', x, y - 1)
                Tile('dead', x, y - 1)
                map_of_level[y - 1][x] = 'x'
                attack_is_1 = True
                save_coord = player.positions[0], player.positions[1]
                player_group.empty()
            else:
                death_screen(width, height)
                restart('normal')
        if map_of_level[y - 1][x] == '3':
            if all_points >= 25 and y > 0:
                all_points += 4
                Tile('empty', x, y - 1)
                Tile('dead', x, y - 1)
                map_of_level[y - 1][x] = 'x'
                attack_is_1 = True
                save_coord = player.positions[0], player.positions[1]
                player_group.empty()
            else:
                death_screen(width, height)
                restart('normal')
        if map_of_level[y - 1][x] == '4':
            death_screen(width, height)
            restart('normal')
        if map_of_level[y - 1][x] == '^' and y > 0:
            death_screen(width, height)
            restart('normal')
        if map_of_level[y - 1][x] == '?' and y > 0:
            save_level('normal', x, y)
            sector += 1
            map_of_level = load_level(f'sector{sector}.txt')
            generate_level(map_of_level)
            player.move_player(9, 6)
        if map_of_level[y - 1][x] == '!' and y > 0:
            save_level('normal', x, y)
            sector -= 1
            map_of_level = load_level(f'sector{sector}.txt')
            generate_level(map_of_level)
            player.move_player(4, 4)
        if y > 0 and map_of_level[y - 1][x] == '.' or map_of_level[y - 1][x] == '*' or \
                map_of_level[y - 1][x] == 'x' or map_of_level[y - 1][x] == '@' or map_of_level[y - 1][x] == '%':
            charec.move_player(x, y - 1)
    if direction == 'right':
        if map_of_level[y][x + 1] == '&' and x < border_x - 1:
            save_level('normal', x, y)
        if map_of_level[y][x + 1] == ')' and x < border_x - 1:
            final_screen()
            restart('total')
        if sector != 0:
            if map_of_level[y][x + 1] == '*' and x < border_x - 1:
                all_points += 1
                Tile('empty', x + 1, y)
                map_of_level[y][x + 1] = '.'
                gem_get_is = True
        if sector == 0:
            if map_of_level[y][x + 1] == '*' and x < border_x - 1:
                all_points += 1
                Tile('grass', x + 1, y)
                map_of_level[y][x + 1] = '%'
                gem_get_is = True
        if map_of_level[y][x + 1] == '0':
            if all_points >= 1 and x < border_x - 1:
                all_points += 1
                Tile('empty', x + 1, y)
                Tile('dead', x + 1, y)
                map_of_level[y][x + 1] = 'x'
                attack_is_1 = True
                save_coord = player.positions[0], player.positions[1]
                player_group.empty()
            else:
                death_screen(width, height)
                restart('normal')
        if map_of_level[y][x + 1] == '1':
            if all_points >= 10 and x < border_x - 1:
                all_points += 2
                Tile('empty', x + 1, y)
                Tile('dead', x + 1, y)
                map_of_level[y][x + 1] = 'x'
                attack_is_1 = True
                save_coord = player.positions[0], player.positions[1]
                player_group.empty()
            else:
                death_screen(width, height)
                restart('normal')
        if map_of_level[y][x + 1] == '2':
            if all_points >= 15 and x < border_x - 1:
                all_points += 3
                Tile('empty', x + 1, y)
                Tile('dead', x + 1, y)
                map_of_level[y][x + 1] = 'x'
                attack_is_1 = True
                save_coord = player.positions[0], player.positions[1]
                player_group.empty()
            else:
                death_screen(width, height)
                restart('normal')
        if map_of_level[y][x + 1] == '3':
            if all_points >= 25 and x < border_x - 1:
                all_points += 4
                Tile('empty', x + 1, y)
                Tile('dead', x + 1, y)
                map_of_level[y][x + 1] = 'x'
                attack_is_1 = True
                save_coord = player.positions[0], player.positions[1]
                player_group.empty()
            else:
                death_screen(width, height)
                restart('normal')
        if map_of_level[y][x + 1] == '4':
            death_screen(width, height)
            restart('normal')
        if map_of_level[y][x + 1] == '^' and x < border_x - 1:
            death_screen(width, height)
            restart('normal')
        if map_of_level[y][x + 1] == '?' and x < border_x - 1:
            save_level('normal', x, y)
            sector += 1
            map_of_level = load_level(f'sector{sector}.txt')
            generate_level(map_of_level)
            player.move_player(9, 6)
        if map_of_level[y][x + 1] == '!' and x < border_x - 1:
            save_level('normal', x, y)
            sector -= 1
            map_of_level = load_level(f'sector{sector}.txt')
            generate_level(map_of_level)
            player.move_player(4, 4)
        if x < border_x - 1 and map_of_level[y][x + 1] == '.' or map_of_level[y][x + 1] == '*' or map_of_level[y][
                x + 1] == 'x' or map_of_level[y][x + 1] == '@' or map_of_level[y][x + 1] == '%':
            charec.move_player(x + 1, y)
            charec.change_look('right')
    if direction == 'left':
        if map_of_level[y][x - 1] == '&' and x > 0:
            save_level('normal', x, y)
        if sector != 0:
            if map_of_level[y][x - 1] == '*' and x > 0:
                all_points += 1
                Tile('empty', x - 1, y)
                map_of_level[y][x - 1] = '.'
                gem_get_is = True
        if sector == 0:
            if map_of_level[y][x - 1] == '*' and x > 0:
                all_points += 1
                Tile('grass', x - 1, y)
                map_of_level[y][x - 1] = '%'
                gem_get_is = True
        if map_of_level[y][x - 1] == '0':
            if all_points >= 1 and x > 0:
                all_points += 1
                Tile('empty', x - 1, y)
                Tile('dead', x - 1, y)
                map_of_level[y][x - 1] = 'x'
                attack_is_1 = True
                save_coord = player.positions[0], player.positions[1]
                player_group.empty()
            else:
                death_screen(width, height)
                restart('normal')
        if map_of_level[y][x - 1] == '1':
            if all_points >= 10 and x > 0:
                all_points += 2
                Tile('empty', x - 1, y)
                Tile('dead', x - 1, y)
                map_of_level[y][x - 1] = 'x'
                attack_is_1 = True
                save_coord = player.positions[0], player.positions[1]
                player_group.empty()
            else:
                death_screen(width, height)
                restart('normal')
        if map_of_level[y][x - 1] == '2':
            if all_points >= 15 and x > 0:
                all_points += 3
                Tile('empty', x - 1, y)
                Tile('dead', x - 1, y)
                map_of_level[y][x - 1] = 'x'
                attack_is_1 = True
                save_coord = player.positions[0], player.positions[1]
                player_group.empty()
            else:
                death_screen(width, height)
                restart('normal')
        if map_of_level[y][x - 1] == '3':
            if all_points >= 25 and x > 0:
                all_points += 4
                Tile('empty', x - 1, y)
                Tile('dead', x - 1, y)
                map_of_level[y][x - 1] = 'x'
                attack_is_1 = True
                save_coord = player.positions[0], player.positions[1]
                player_group.empty()
            else:
                death_screen(width, height)
                restart('normal')
        if map_of_level[y][x - 1] == '4':
            death_screen(width, height)
            restart('normal')
        if map_of_level[y][x - 1] == '^' and x > 0:
            death_screen(width, height)
            restart('normal')
        if map_of_level[y][x - 1] == '?' and x > 0:
            save_level('normal', x, y)
            sector += 1
            map_of_level = load_level(f'sector{sector}.txt')
            generate_level(map_of_level)
            player.move_player(9, 6)
        if map_of_level[y][x - 1] == '!' and x > 0:
            save_level('normal', x, y)
            sector -= 1
            map_of_level = load_level(f'sector{sector}.txt')
            generate_level(map_of_level)
            player.move_player(4, 4)
        if x > 0 and map_of_level[y][x - 1] == '.' or map_of_level[y][x - 1] == '*' or \
                map_of_level[y][x - 1] == 'x' or map_of_level[y][x - 1] == '@' or map_of_level[y][x - 1] == '%':
            charec.move_player(x - 1, y)
            charec.change_look('left')


def shoot(x, y):
    global map_of_level
    if map_of_level[y][x] == '4':
        map_of_level[y][x] = 'x'
        Tile('empty', x, y)
        Tile('dead', x, y)


class Player(pygame.sprite.Sprite):  # класс игрока(егор)
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group)
        self.image = player_image
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)
        self.positions = (pos_x, pos_y)
        self.look = 'right'

    def move_player(self, x, y):
        self.positions = (x, y)
        self.rect = self.image.get_rect().move(tile_width * x, tile_height * y)

    def change_look(self, look):
        if look != self.look and look == 'right':
            self.image = pygame.transform.flip(self.image, True, False)
            self.look = 'right'
        elif look != self.look and look == 'left':
            self.image = pygame.transform.flip(self.image, True, False)
            self.look = 'left'


class Tile(pygame.sprite.Sprite):  # класс не двигающихся объектов(егор)
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


class AnimatedGemGet(pygame.sprite.Sprite):  # анимация разрушение кристаллов(егор)
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(gem_get_sprites)
        self.place_x = player.positions[0]
        self.place_y = player.positions[1]
        self.frames = []  # список кадров
        self.cut_sheet(sheet, columns, rows)  # разреанная на кадры
        self.cur_frame = 0  # номер кадра нынешнего
        self.image = self.frames[self.cur_frame]  # Кадр в нынешний момент
        self.rect = self.rect.move(self.place_x * x, self.place_y * y)  # место рисовки кадра

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,  # прямоугольник с размерами кадра
                                sheet.get_height() // rows)
        for j in range(rows):  # проходить по изначальной картинке и отделяем кадры
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)  # позиция кадра на изначльном изображении
                self.frames.append(sheet.subsurface(pygame.Rect(  # доюавляем в список кадров
                    frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)  # обновление номера кадра
        self.image = self.frames[self.cur_frame]  # обновление самого кадра


class AnimatedAttack1(pygame.sprite.Sprite):  # анимация атаки(егор)
    def __init__(self, sheet, columns, rows, x, y, look):
        super().__init__(attack1_sprites)
        self.place_x = player.positions[0]
        self.place_y = player.positions[1]
        self.look = look
        self.frames = []  # список кадров
        self.cut_sheet(sheet, columns, rows)  # разреанная на кадры
        self.cur_frame = 0  # номер кадра нынешнего
        self.image = self.frames[self.cur_frame]  # Кадр в нынешний момент
        self.rect = self.rect.move(self.place_x * x, self.place_y * y)  # место рисовки кадра

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,  # прямоугольник с размерами кадра
                                sheet.get_height() // rows)
        for j in range(rows):  # проходить по изначальной картинке и отделяем кадры
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)  # позиция кадра на изначльном изображении
                self.frames.append(sheet.subsurface(pygame.Rect(  # доюавляем в список кадров
                    frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)  # обновление номера кадра
        if self.look == 'left':
            self.image = self.frames[self.cur_frame]  # обновление самого кадра
            self.image = pygame.transform.flip(self.image, True, False)
        else:
            self.image = self.frames[self.cur_frame]


class AnimatedAttack2(pygame.sprite.Sprite):  # анимация атаки(егор)
    def __init__(self, sheet, columns, rows, x, y, look):
        super().__init__(attack2_sprites)
        self.place_x = player.positions[0]
        self.place_y = player.positions[1]
        self.look = look
        self.frames = []  # список кадров
        self.cut_sheet(sheet, columns, rows)  # разреанная на кадры
        self.cur_frame = 0  # номер кадра нынешнего
        self.image = self.frames[self.cur_frame]  # Кадр в нынешний момент
        self.rect = self.rect.move(self.place_x * x, self.place_y * y)  # место рисовки кадра

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,  # прямоугольник с размерами кадра
                                sheet.get_height() // rows)
        for j in range(rows):  # проходить по изначальной картинке и отделяем кадры
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)  # позиция кадра на изначльном изображении
                self.frames.append(sheet.subsurface(pygame.Rect(  # доюавляем в список кадров
                    frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)  # обновление номера кадра
        if self.look == 'left':
            self.image = self.frames[self.cur_frame]  # обновление самого кадра
            self.image = pygame.transform.flip(self.image, True, False)
        else:
            self.image = self.frames[self.cur_frame]


class AnimatedAttack3(pygame.sprite.Sprite):  # анимация атаки(егор)
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(attack3_sprites)
        self.place_x = shoot_at[0]
        self.place_y = shoot_at[1]
        self.frames = []  # список кадров
        self.cut_sheet(sheet, columns, rows)  # разреанная на кадры
        self.cur_frame = 0  # номер кадра нынешнего
        self.image = self.frames[self.cur_frame]  # Кадр в нынешний момент
        self.rect = self.rect.move(self.place_x * x, self.place_y * y)  # место рисовки кадра

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,  # прямоугольник с размерами кадра
                                sheet.get_height() // rows)
        for j in range(rows):  # проходить по изначальной картинке и отделяем кадры
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)  # позиция кадра на изначльном изображении
                self.frames.append(sheet.subsurface(pygame.Rect(  # доюавляем в список кадров
                    frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)  # обновление номера кадра
        self.image = self.frames[self.cur_frame]


class Board:  # создание доски(егор)
    # создание поля
    def __init__(self, width1, height1):
        self.width = width1
        self.height = height1
        self.board = [[0] * width for _ in range(height1)]
        # значения по умолчанию
        self.left = 0
        self.top = 0
        self.cell_size = 50

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def get_cell(self, mouse_pos):
        width1 = self.width * self.cell_size + self.left
        height1 = self.height * self.cell_size + self.top
        x, y = mouse_pos
        if self.left <= x <= width1 and self.top <= y <= height1:
            x1 = (x - self.left) // self.cell_size
            y1 = (y - self.top) // self.cell_size
            total = (x1, y1)
            return total
        else:
            return None

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        print(cell)


if __name__ == '__main__':
    level_player = int(load_level_player())
    all_points = int(load_points())
    pygame.display.set_caption('Master of dungeon')
    pygame.mixer.music.load('data/game_music.mp3')
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.2)

    FPS = 24
    running = True
    clock = pygame.time.Clock()
    map_of_level = load_level(f'sector{sector}.txt')
    player, border_x, border_y = generate_level(map_of_level)

    save_coord = (1, 1)
    gem_get_sprites = pygame.sprite.Group()
    gem_get_is = False
    cou_gem_get = 1

    attack1_sprites = pygame.sprite.Group()
    attack_is_1 = False
    cou_attack_1 = 1

    attack2_sprites = pygame.sprite.Group()
    attack_is_2 = False
    cou_attack_2 = 1

    attack3_sprites = pygame.sprite.Group()
    attack_is_3 = False
    cou_attack_3 = 1

    board = Board(30, 17)
    start_screen(width, height)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_points(all_points)
                save_level_player(level_player)
                save_level('quit', player.positions[0], player.positions[1])
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                attack_is_2 = True
                attack_is_3 = True
                shoot_at = board.get_cell(event.pos)
                save_coord = player.positions[0], player.positions[1]
                shoot(shoot_at[0], shoot_at[1])
                player_group.empty()
            key = pygame.key.get_pressed()
            if key[pygame.K_DOWN] or key[pygame.K_s]:
                movement(player, 'down')
            elif key[pygame.K_UP] or key[pygame.K_w]:
                movement(player, 'up')
            if key[pygame.K_LEFT] or key[pygame.K_a]:
                movement(player, 'left')
            elif key[pygame.K_RIGHT] or key[pygame.K_d]:
                movement(player, 'right')
            if key[pygame.K_SPACE]:
                restart('total')
                sys.exit()
        save_coord = player.positions[0], player.positions[1]
        screen.fill((0, 0, 0))
        tiles_group.draw(screen)
        player_group.draw(screen)
        tiles_group.update()
        player_group.update()
        if cou_gem_get < 8 and gem_get_is:
            if cou_gem_get == 1:
                gem_get = AnimatedGemGet(load_image("anim1.png", 'white'), 4, 2, 50, 50)
            gem_get_sprites.update()
            gem_get_sprites.draw(screen)
            cou_gem_get += 1
        if cou_gem_get >= 8:
            gem_get_sprites.empty()
            cou_gem_get = 1
            gem_get_is = False
        if attack_is_1:
            if cou_attack_1 <= 8:
                if cou_attack_1 == 1:
                    # приводим класс в действие
                    attack = AnimatedAttack1(load_image("anim.png", 'white'), 4, 2, 50, 50, player.look)
                attack1_sprites.update()  # запускаем анимацию
                attack1_sprites.draw(screen)
                cou_attack_1 += 1
            if cou_attack_1 > 8:
                attack1_sprites.empty()
                cou_attack_1 = 1
                attack_is_1 = False
                if player.look == 'left':
                    player = Player(save_coord[0], save_coord[1])
                    player.change_look('left')
                else:
                    player = Player(save_coord[0], save_coord[1])
        if attack_is_2:
            if cou_attack_2 <= 8:
                if cou_attack_2 == 1:
                    # приводим класс в действие
                    attack = AnimatedAttack2(load_image("anim2.png", 'white'), 4, 2, 50, 50, player.look)
                attack2_sprites.update()  # запускаем анимацию
                attack2_sprites.draw(screen)
                cou_attack_2 += 1
            if cou_attack_2 > 8:
                attack2_sprites.empty()
                cou_attack_2 = 1
                attack_is_2 = False
                if player.look == 'left':
                    player = Player(save_coord[0], save_coord[1])
                    player.change_look('left')
                else:
                    player = Player(save_coord[0], save_coord[1])
        if attack_is_3:
            if cou_attack_3 <= 8:
                if cou_attack_3 == 1:
                    # приводим класс в действие
                    attack = AnimatedAttack3(load_image("anim3.png", 'white'), 4, 2, 50, 50)
                attack3_sprites.update()  # запускаем анимацию
                attack3_sprites.draw(screen)
                cou_attack_3 += 1
            if cou_attack_3 > 8:
                attack3_sprites.empty()
                cou_attack_3 = 1
                attack_is_3 = False
        up_level(all_points)
        remote_out(all_points)
        remote_load(level_player)
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()
