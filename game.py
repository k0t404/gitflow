import pygame
import os
import sys


pygame.init()
size = width, height = 950, 550
screen = pygame.display.set_mode(size)


def load_image(name, colorkey=None):
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
    return image


tile_images = {
    'wall': load_image('box.png'),
    'empty': load_image('grass.png')
}
player_image = load_image('mario.png')

tile_width = tile_height = 50
# основной персонаж
player = None

# группы спрайтов
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()


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
        clock.tick(FPS)


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
                level[y][x] = '.'
                print(level)
    # вернем игрока, а также размер поля в клетках
    return new_player, x, y


def movement(charec, direction):
    x, y = charec.positions
    if direction == 'down':
        if map_of_level[y + 1][x] == '.' and y < border_y - 1:
            charec.move_player(x, y + 1)
    if direction == 'up':
        if map_of_level[y - 1][x] == '.' and y > 0:
            charec.move_player(x, y - 1)
    if direction == 'right':
        if map_of_level[y][x + 1] == '.' and x < border_x - 1:
            charec.move_player(x + 1, y)
    if direction == 'left':
        if map_of_level[y][x - 1] == '.' and x > 0:
            charec.move_player(x - 1, y)


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group)
        self.image = player_image
        self.rect = self.image.get_rect().move(tile_width * pos_x + 15, tile_height * pos_y + 5)
        self.positions = (pos_x, pos_y)

    def move_player(self, x, y):
        self.positions = (x, y)
        self.rect = self.image.get_rect().move(tile_width * self.positions[0] + 15, tile_height * self.positions[1] + 5)


class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self):
        self.dx = 10
        self.dy = 10

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    # позиционировать камеру на объекте target
    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - width // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - height // 2)


if __name__ == '__main__':
    FPS = 50

    all_sprites = pygame.sprite.Group()
    clock = pygame.time.Clock()
    running = True

    map_of_level = load_level('map.txt')
    move_by = 50
    player, border_x, border_y = generate_level(map_of_level)
    start_screen(width, height)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONUP:
                yes = 1
            key = pygame.key.get_pressed()
            if key[pygame.K_DOWN]:
                movement(player, 'down')
            elif key[pygame.K_UP]:
                movement(player, 'up')
            if key[pygame.K_LEFT]:
                movement(player, 'left')
            elif key[pygame.K_RIGHT]:
                movement(player, 'right')
        screen.fill((0, 0, 0))
        tiles_group.draw(screen)
        player_group.draw(screen)
        tiles_group.update()
        player_group.update()
        pygame.display.flip()
        clock.tick(FPS)

        camera = Camera()
        # изменяем ракурс камеры
        camera.update(player)
        # обновляем положение всех спрайтов
        for sprite in all_sprites:
            camera.apply(sprite)
    pygame.quit()
