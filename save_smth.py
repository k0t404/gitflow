def save_level_player(level_pl):  # сохранение уровня игрока(ярик)
    point = open('data/level_player.txt', 'w')
    point.write(str(level_pl))
    point.close()


def save_points(all_point):  # сохранение очков(ярик)
    point = open('data/points.txt', 'w')
    point.write(str(all_point))
    point.close()