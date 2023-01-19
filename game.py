import pygame
import os
import sys

pygame.init()
sector = 1
size = width, height = 1500, 800
screen = pygame.display.set_mode(size)
cou = 0


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
    'wall': load_image('wall.png'),
    'empty': load_image('floor.png'),
    'door_next': load_image('door_next.png', 'white'),
    'door_prev': load_image('door_prev.png', 'white'),
    'gem': load_image('gem.png', 'white'),
    'spike': load_image('spike.png', 'white'),
    'checkpoint': load_image('checkpoint.png', 'white'),
    'enemy1': load_image('enemy1.png', 'white')
}
player_image = load_image('knight.png', 'white')
tile_width = tile_height = 50
# основной персонаж
player = None

# группы спрайтов
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()


def save_level():
    filename = "data/" + f'sector{sector}.txt'
    # читаем уровень, убирая символы перевода строки
    map_of_level[12][28] = '@'
    with open(filename, 'w') as mapFile:
        for y in map_of_level:
            mapFile.writelines(''.join(y) + '\n')


def load_level(filename):
    filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: list(x.ljust(max_width, '.')), level_map))


def terminate():
    pygame.quit()
    sys.exit()


def start_screen(wid, heig):
    intro_text = ["Master of dungeon", "",
                  "Правила игры",
                  "Если в правилах несколько строк,",
                  "приходится выводить их построчно"]

    fon = pygame.transform.scale(load_image('fon.jpg'), (wid, heig))
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
    intro_text = ["YOU DIED", "",
                  " ",
                  " ",
                  " "]

    fon = pygame.transform.scale(load_image('fon.jpg'), (wid, heig))
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
                return

        pygame.display.flip()
        '''clock.tick(FPS)'''


def delete_thing(x, y):
    Tile('empty', x, y)
    map_of_level[y][x] = '.'


def generate_level(level):
    new_player, x, y = None, None, None
    global cou
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@' and cou == 0:
                cou += 1
                Tile('empty', x, y)
                new_player = Player(x, y)
                level[y][x] = '.'
                print(level)
            elif level[y][x] == '@' and cou != 0:
                cou += 1
                Tile('empty', x, y)
                level[y][x] = '.'
                print(level)
            elif level[y][x] == '*':
                Tile('empty', x, y)
                Tile('gem', x, y)
            elif level[y][x] == '?':
                Tile('empty', x, y)
                Tile('door_next', x, y)
            elif level[y][x] == '!':
                Tile('empty', x, y)
                Tile('door_prev', x, y)
            elif level[y][x] == '^':
                Tile('empty', x, y)
                Tile('spike', x, y)
            elif level[y][x] == '&':
                Tile('empty', x, y)
                Tile('checkpoint', x, y)
            elif level[y][x] == '1':
                Tile('empty', x, y)

    # вернем игрока, а также размер поля в клетках
    return new_player, x, y


def restart(how):
    if how == 'normal':
        player.move_player(9, 5)
    if how == 'total':
        pass


def movement(charec, direction):
    x, y = charec.positions
    global sector
    global map_of_level
    if direction == 'down':
        if map_of_level[y + 1][x] == '&' and y < border_y - 1:
            save_level()
        if map_of_level[y + 1][x] == '*' and y < border_y - 1:
            Tile('empty', x, y + 1)
            map_of_level[y + 1][x] = '.'
        if map_of_level[y + 1][x] == '^' and y < border_y - 1:
            death_screen(width, height)
            restart('normal')
        if map_of_level[y + 1][x] == '?' and y < border_y - 1:
            sector += 1
            map_of_level = load_level(f'sector{sector}.txt')
            generate_level(map_of_level)
            player.move_player(3, 5)
            save_level()
        if map_of_level[y + 1][x] == '!' and y < border_y - 1:
            sector -= 1
            map_of_level = load_level(f'sector{sector}.txt')
            generate_level(map_of_level)
            player.move_player(3, 5)
            save_level()
        if y < border_y - 1 and map_of_level[y + 1][x] == '.' or map_of_level[y + 1][x] == '*' or map_of_level[y + 1][
            x] == '&':
            charec.move_player(x, y + 1)
    if direction == 'up':
        if map_of_level[y - 1][x] == '&' and y > 0:
            save_level()
        if map_of_level[y - 1][x] == '*' and y > 0:
            Tile('empty', x, y - 1)
            map_of_level[y - 1][x] = '.'
        if map_of_level[y - 1][x] == '^' and y > 0:
            death_screen(width, height)
            restart('normal')
        if map_of_level[y - 1][x] == '?' and y > 0:
            sector += 1
            map_of_level = load_level(f'sector{sector}.txt')
            generate_level(map_of_level)
            player.move_player(3, 5)
            save_level()
        if map_of_level[y - 1][x] == '!' and y > 0:
            sector -= 1
            map_of_level = load_level(f'sector{sector}.txt')
            generate_level(map_of_level)
            player.move_player(3, 5)
            save_level()
        if y > 0 and map_of_level[y - 1][x] == '.' or map_of_level[y - 1][x] == '*' or map_of_level[y - 1][x] == '&':
            charec.move_player(x, y - 1)
    if direction == 'right':
        if map_of_level[y][x + 1] == '&' and x < border_x - 1:
            save_level()
        if map_of_level[y][x + 1] == '*' and x < border_x - 1:
            Tile('empty', x + 1, y)
            map_of_level[y][x + 1] = '.'
        if map_of_level[y][x + 1] == '^' and x < border_x - 1:
            death_screen(width, height)
            restart('normal')
        if map_of_level[y][x + 1] == '?' and x < border_x - 1:
            sector += 1
            map_of_level = load_level(f'sector{sector}.txt')
            generate_level(map_of_level)
            player.move_player(3, 5)
            save_level()
        if map_of_level[y][x + 1] == '!' and x < border_x - 1:
            sector -= 1
            map_of_level = load_level(f'sector{sector}.txt')
            generate_level(map_of_level)
            player.move_player(3, 5)
            save_level()
        if x < border_x - 1 and map_of_level[y][x + 1] == '.' or map_of_level[y][x + 1] == '*' or map_of_level[y][
            x + 1] == '&':
            charec.move_player(x + 1, y)
            charec.change_look('right')
    if direction == 'left':
        if map_of_level[y][x - 1] == '&' and x > 0:
            save_level()
        if map_of_level[y][x - 1] == '*' and x > 0:
            Tile('empty', x - 1, y)
            map_of_level[y][x - 1] = '.'
        if map_of_level[y][x - 1] == '^' and x > 0:
            death_screen(width, height)
            restart('normal')
        if map_of_level[y][x - 1] == '?' and x > 0:
            sector += 1
            map_of_level = load_level(f'sector{sector}.txt')
            generate_level(map_of_level)
            player.move_player(3, 5)
            save_level()
        if map_of_level[y][x - 1] == '!' and x > 0:
            sector -= 1
            map_of_level = load_level(f'sector{sector}.txt')
            generate_level(map_of_level)
            player.move_player(3, 5)
            save_level()
        if x > 0 and map_of_level[y][x - 1] == '.' or map_of_level[y][x - 1] == '*' or map_of_level[y][x - 1] == '&':
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
    running = True

    map_of_level = load_level(f'sector{sector}.txt')
    player, border_x, border_y = generate_level(map_of_level)
    start_screen(width, height)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
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
        screen.fill((0, 0, 0))
        tiles_group.draw(screen)
        player_group.draw(screen)
        tiles_group.update()
        player_group.update()
        pygame.display.flip()
        '''clock.tick(FPS)'''
    pygame.quit()
