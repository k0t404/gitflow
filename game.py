import pygame
import os
import sys


pygame.init()
sector = 0
size = width, height = 1500, 800
screen = pygame.display.set_mode(size)
cou = 0
cou2 = 0


def load_image(name, colorkey=None):
    change_name = ['wall.png', 'floor.png', 'knight.png', 'gem.png', 'door.png']
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    if name in change_name:
        return pygame.transform.scale(image, (50, 50))
    return image


tile_images = {
    'grass': load_image('grass.png'),
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
    'enemy3': load_image('enemy3.png', 'white')
}
player_image = load_image('knight.png', 'white')
tile_width = tile_height = 50
# основной персонаж
player = None

# группы спрайтов
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()


def save_level(kind, x, y):
    filename = "data/" + f'sector{sector}.txt'
    # читаем уровень, убирая символы перевода строки
    if kind == 'normal':
        map_of_level[7][12] = '@'
    elif kind == 'quit':
        map_of_level[y][x] = '@'
    with open(filename, 'w') as mapFile:
        for y in map_of_level:
            mapFile.writelines(''.join(y) + '\n')


def save_points(all_point):
    point = open('data/points.txt', 'w')
    point.write(str(all_point))
    point.close()


def load_points():
    with open('data/points.txt', 'r') as points:
        point = points.read()
    return point


def load_level(filename):
    filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: list(x.ljust(max_width, '.')), level_map))


def write_save():
    original_maps = [load_level('sector0.txt'), load_level('sector1.txt'), load_level('sector2.txt')]
    with open('data/save.txt', 'w') as save:
        for map_level in original_maps:
            for line in map_level:
                save.writelines(''.join(line) + '\n')
            save.writelines('|')


def remote(all_point):
    font = pygame.font.Font(None, 30)
    text = font.render(f"Points: {all_point}", True, (250, 42, 42))
    screen.blit(text, (10, 770))


def terminate():
    pygame.quit()
    sys.exit()


def start_screen(wid, heig):
    intro_text = ["Master of dungeon", "",
                  "Правила игры",
                  "Если в правилах несколько строк,",
                  "приходится выводить их построчно"]

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
        '''clock.tick(FPS)'''


def death_screen(wid, heig):
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
        '''clock.tick(FPS)'''


def generate_level(level):
    new_player, x, y = None, None, None
    global cou
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '%':
                Tile('grass', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            if sector != 0:
                if level[y][x] == '@' and cou == 0:
                    cou += 1
                    Tile('empty', x, y)
                    new_player = Player(x, y)
                    level[y][x] = '%'
                elif level[y][x] == '@' and cou != 0:
                    cou += 1
                    Tile('empty', x, y)
                    level[y][x] = '%'
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
                    level[y][x] = '.'
                elif level[y][x] == '@' and cou != 0:
                    cou += 1
                    Tile('grass', x, y)
                    level[y][x] = '.'
                elif level[y][x] == '*':
                    Tile('grass', x, y)
                    Tile('gem', x, y)
                elif level[y][x] == '?':
                    Tile('grass', x, y)
                    Tile('door_next', x, y)
                elif level[y][x] == '!':
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

    # вернем игрока, а также размер поля в клетках
    return new_player, x, y


def restart(how):
    global sector
    global cou
    cou1 = 0
    if how == 'normal':
        player.move_player(9, 5)
    if how == 'total':
        save_points(0)
        save = open('data/save.txt', 'r')
        maps = (''.join(save.readlines())).split('|')
        save.close()
        maps.pop(-1)
        maps_orig = []
        for part in maps:
            maps_orig.append(part.split('\n'))
        for map_level in maps_orig:
            print(map_level)
            print(map_of_level)
            with open(f'data/sector{cou1}', 'w') as map_save:
                for line in map_level:
                    print(line)
                    map_save.write(line + '\n')
            with open(f'data/sector{cou1}', 'r') as map_save:
                map_save.readlines()
            cou1 += 1
        sector = 0
        cou = 0


def movement(charec, direction):
    x, y = charec.positions
    global sector
    global map_of_level
    global all_points
    global cou2
    if direction == 'down':
        if map_of_level[y + 1][x] == '&' and y < border_y - 1:
            save_level('normal', x, y)
        if sector != 0:
            if map_of_level[y + 1][x] == '*' and y < border_y - 1:
                all_points += 1
                Tile('empty', x, y + 1)
                map_of_level[y + 1][x] = '.'
                save_level('normal', x, y)
        if sector == 0:
            if map_of_level[y + 1][x] == '*' and y < border_y - 1:
                all_points += 1
                Tile('grass', x, y + 1)
                map_of_level[y + 1][x] = '.'
        if map_of_level[y + 1][x] == '0':
            if all_points >= 1 and y < border_y - 1:
                all_points += 1
                Tile('empty', x, y + 1)
                map_of_level[y + 1][x] = '.'
                player.move_player(x, y + 1)
            else:
                death_screen(width, height)
                restart('normal')
        if map_of_level[y + 1][x] == '1':
            if all_points >= 10 and y < border_y - 1:
                all_points += 2
                Tile('empty', x, y + 1)
                map_of_level[y + 1][x] = '.'
                player.move_player(x, y + 1)
            else:
                death_screen(width, height)
                restart('normal')
        if map_of_level[y + 1][x] == '2':
            if all_points >= 15 and y < border_y - 1:
                all_points += 3
                Tile('empty', x, y + 1)
                map_of_level[y + 1][x] = '.'
                player.move_player(x, y + 1)
            else:
                death_screen(width, height)
                restart('normal')
        if map_of_level[y + 1][x] == '3':
            if all_points >= 25 and y < border_y - 1:
                all_points += 4
                Tile('empty', x, y + 1)
                map_of_level[y + 1][x] = '.'
                player.move_player(x, y + 1)
            else:
                death_screen(width, height)
                restart('normal')
        if map_of_level[y + 1][x] == '^' and y < border_y - 1:
            death_screen(width, height)
            restart('normal')
        if map_of_level[y + 1][x] == '?' and y < border_y - 1:
            sector += 1
            map_of_level = load_level(f'sector{sector}.txt')
            generate_level(map_of_level)
            player.move_player(9, 6)
            save_level('normal', x, y)
        if map_of_level[y + 1][x] == '!' and y < border_y - 1:
            sector -= 1
            map_of_level = load_level(f'sector{sector}.txt')
            generate_level(map_of_level)
            player.move_player(4, 4)
            save_level('normal', x, y)
        if y < border_y - 1 and map_of_level[y + 1][x] == '.' or map_of_level[y + 1][x] == '*' or \
                map_of_level[y + 1][x] == '&' or map_of_level[y + 1][x] == '@' or map_of_level[y + 1][x] == '%':
            charec.move_player(x, y + 1)
    if direction == 'up':
        if map_of_level[y - 1][x] == '&' and y > 0:
            save_level('normal', x, y)
        if sector != 0:
            if map_of_level[y - 1][x] == '*' and y > 0:
                all_points += 1
                Tile('empty', x, y - 1)
                map_of_level[y - 1][x] = '.'
        if sector == 0:
            if map_of_level[y - 1][x] == '*' and y > 0:
                all_points += 1
                Tile('grass', x, y - 1)
                map_of_level[y - 1][x] = '.'
        if map_of_level[y - 1][x] == '0':
            if all_points >= 1 and y > 0:
                all_points += 1
                Tile('empty', x, y - 1)
                map_of_level[y - 1][x] = '.'
                player.move_player(x, y - 1)
            else:
                death_screen(width, height)
                restart('normal')
        if map_of_level[y - 1][x] == '1':
            if all_points >= 10 and y > 0:
                all_points += 2
                Tile('empty', x, y - 1)
                map_of_level[y - 1][x] = '.'
                player.move_player(x, y - 1)
            else:
                death_screen(width, height)
                restart('normal')
        if map_of_level[y - 1][x] == '2':
            if all_points >= 15 and y > 0:
                all_points += 3
                Tile('empty', x, y - 1)
                map_of_level[y - 1][x] = '.'
                player.move_player(x, y - 1)
            else:
                death_screen(width, height)
                restart('normal')
        if map_of_level[y - 1][x] == '3':
            if all_points >= 25 and y > 0:
                all_points += 4
                Tile('empty', x, y - 1)
                map_of_level[y - 1][x] = '.'
                player.move_player(x, y - 1)
            else:
                death_screen(width, height)
                restart('normal')
        if map_of_level[y - 1][x] == '^' and y > 0:
            death_screen(width, height)
            restart('normal')
        if map_of_level[y - 1][x] == '?' and y > 0:
            sector += 1
            map_of_level = load_level(f'sector{sector}.txt')
            generate_level(map_of_level)
            player.move_player(9, 6)
            save_level('normal', x, y)
        if map_of_level[y - 1][x] == '!' and y > 0:
            sector -= 1
            map_of_level = load_level(f'sector{sector}.txt')
            generate_level(map_of_level)
            player.move_player(4, 4)
            save_level('normal', x, y)
        if y > 0 and map_of_level[y - 1][x] == '.' or map_of_level[y - 1][x] == '*' or \
                map_of_level[y - 1][x] == '&' or map_of_level[y - 1][x] == '@' or map_of_level[y + 1][x] == '%':
            charec.move_player(x, y - 1)
    if direction == 'right':
        if map_of_level[y][x + 1] == '&' and x < border_x - 1:
            save_level('normal', x, y)
        if sector != 0:
            if map_of_level[y][x + 1] == '*' and x < border_x - 1:
                all_points += 1
                Tile('empty', x + 1, y)
                map_of_level[y][x + 1] = '.'
        if sector == 0:
            if map_of_level[y][x + 1] == '*' and x < border_x - 1:
                all_points += 1
                Tile('grass', x + 1, y)
                map_of_level[y][x + 1] = '.'
        if map_of_level[y][x + 1] == '0':
            if all_points >= 1 and x < border_x - 1:
                all_points += 1
                Tile('empty', x + 1, y)
                map_of_level[y][x + 1] = '.'
                player.move_player(x + 1, y)
            else:
                death_screen(width, height)
                restart('normal')
        if map_of_level[y][x + 1] == '1':
            if all_points >= 10 and x < border_x - 1:
                all_points += 2
                Tile('empty', x + 1, y)
                map_of_level[y][x + 1] = '.'
                player.move_player(x + 1, y)
            else:
                death_screen(width, height)
                restart('normal')
        if map_of_level[y][x + 1] == '2':
            if all_points >= 15 and x < border_x - 1:
                all_points += 3
                Tile('empty', x + 1, y)
                map_of_level[y][x + 1] = '.'
                player.move_player(x + 1, y)
            else:
                death_screen(width, height)
                restart('normal')
        if map_of_level[y][x + 1] == '3':
            if all_points >= 25 and x < border_x - 1:
                all_points += 4
                Tile('empty', x + 1, y)
                map_of_level[y][x + 1] = '.'
                player.move_player(x + 1, y)
            else:
                death_screen(width, height)
                restart('normal')
        if map_of_level[y][x + 1] == '^' and x < border_x - 1:
            death_screen(width, height)
            restart('normal')
        if map_of_level[y][x + 1] == '?' and x < border_x - 1:
            sector += 1
            map_of_level = load_level(f'sector{sector}.txt')
            generate_level(map_of_level)
            player.move_player(9, 6)
            save_level('normal', x, y)
        if map_of_level[y][x + 1] == '!' and x < border_x - 1:
            sector -= 1
            map_of_level = load_level(f'sector{sector}.txt')
            generate_level(map_of_level)
            player.move_player(4, 4)
            save_level('normal', x, y)
        if x < border_x - 1 and map_of_level[y][x + 1] == '.' or map_of_level[y][x + 1] == '*' or \
                map_of_level[y][x + 1] == '&' or map_of_level[y][x + 1] == '@' or map_of_level[y + 1][x] == '%':
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
        if sector == 0:
            if map_of_level[y][x - 1] == '*' and x > 0:
                all_points += 1
                Tile('grass', x - 1, y)
                map_of_level[y][x - 1] = '.'
        if map_of_level[y][x - 1] == '0':
            if all_points >= 1 and x > 0:
                all_points += 1
                Tile('empty', x - 1, y)
                map_of_level[y][x - 1] = '.'
                player.move_player(x - 1, y)
            else:
                death_screen(width, height)
                restart('normal')
        if map_of_level[y][x - 1] == '1':
            if all_points >= 10 and x > 0:
                all_points += 2
                Tile('empty', x - 1, y)
                map_of_level[y][x - 1] = '.'
                player.move_player(x - 1, y)
            else:
                death_screen(width, height)
                restart('normal')
        if map_of_level[y][x - 1] == '2':
            if all_points >= 15 and x > 0:
                all_points += 3
                Tile('empty', x - 1, y)
                map_of_level[y][x - 1] = '.'
                player.move_player(x - 1, y)
            else:
                death_screen(width, height)
                restart('normal')
        if map_of_level[y][x - 1] == '3':
            if all_points >= 25 and x > 0:
                all_points += 4
                Tile('empty', x - 1, y)
                map_of_level[y][x - 1] = '.'
                player.move_player(x - 1, y)
            else:
                death_screen(width, height)
                restart('normal')
        if map_of_level[y][x - 1] == '^' and x > 0:
            death_screen(width, height)
            restart('normal')
        if map_of_level[y][x - 1] == '?' and x > 0:
            sector += 1
            map_of_level = load_level(f'sector{sector}.txt')
            generate_level(map_of_level)
            player.move_player(9, 6)
            save_level('normal', x, y)
        if map_of_level[y][x - 1] == '!' and x > 0:
            sector -= 1
            map_of_level = load_level(f'sector{sector}.txt')
            generate_level(map_of_level)
            player.move_player(4, 4)
            save_level('normal', x, y)
        if x > 0 and map_of_level[y][x - 1] == '.' or map_of_level[y][x - 1] == '*' or \
                map_of_level[y][x - 1] == '&' or map_of_level[y][x - 1] == '@' or map_of_level[y + 1][x] == '%':
            charec.move_player(x - 1, y)
            charec.change_look('left')


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
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


if __name__ == '__main__':
    all_points = int(load_points())
    pygame.mixer.music.load('data/game_music.mp3')
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.2)
    running = True

    map_of_level = load_level(f'sector{sector}.txt')
    player, border_x, border_y = generate_level(map_of_level)
    start_screen(width, height)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_points(all_points)
                save_level('quit', player.positions[0], player.positions[1])
                running = False
            if event.type == pygame.MOUSEBUTTONUP:
                yes = 1
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
        screen.fill((0, 0, 0))
        tiles_group.draw(screen)
        player_group.draw(screen)
        tiles_group.update()
        player_group.update()
        remote(all_points)
        pygame.display.flip()
        '''clock.tick(FPS)'''
    pygame.quit()
