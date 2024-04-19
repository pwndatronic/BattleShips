import random


class WrongShipOption(Exception):
    pass


class WrongBoardCoord(Exception):
    pass


class WrongShotFormat(Exception):
    pass


class WrongShotDot(Exception):
    pass


class WrongShotInDamagedShip(Exception):
    pass


class WrongShotInDeadShip(Exception):
    pass


class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def generate_surrounding_dots(self):
        surrounding_dots = []
        for x in range(self.x - 1, self.x + 2):
            for y in range(self.y - 1, self.y + 2):
                if all([x == self.x,
                        y == self.y]):
                    continue
                if any([x not in range(1, 7),
                        y not in range(1, 7)]):
                    continue
                else:
                    surrounding_dots.append(Dot(x, y))
        return surrounding_dots

    def generate_crest_dots(self):
        crest_dots = []
        for x in range(self.x - 1, self.x + 2):
            for y in range(self.y - 1, self.y + 2):
                if all([x == self.x,
                        y == self.y]):
                    continue
                if any([x not in range(1, 7),
                        y not in range(1, 7)]):
                    continue
                if any([x == self.x,
                        y == self.y]):
                    crest_dots.append(Dot(x, y))
        return crest_dots


class Ship:
    def __init__(self, size, starting_dot: Dot, direction):
        self.ship_size = size
        self.health = size
        self.starting_dot = starting_dot
        self.direction = direction
        self.direct_ship(size, starting_dot, direction)

    def direct_ship(self, size, starting_dot: Dot, direction):
        self.ship_size = size
        self.direction = direction
        self.starting_dot_x = starting_dot.x
        self.starting_dot_y = starting_dot.y
        self.all_dots = []

        if direction == 0:
            for j in range(self.ship_size):
                self.all_dots.append(Dot(starting_dot.x - j, starting_dot.y))
        elif direction == 1:
            for j in range(self.ship_size):
                self.all_dots.append(Dot(starting_dot.x, starting_dot.y + j))
        elif direction == 2:
            for j in range(self.ship_size):
                self.all_dots.append(Dot(starting_dot.x + j, starting_dot.y))
        elif direction == 3:
            for j in range(self.ship_size):
                self.all_dots.append(Dot(starting_dot.x, starting_dot.y - j))

    def get_all_dots(self):
        return self.all_dots

    def got_shot(self):
        self.health = self.health - 1

    def get_ship_health(self):
        return self.health


class Board:
    def __init__(self, hide=False):
        self.board = [['O' for _ in range(6)] for _ in range(6)]
        self.board_dots = {'ships': [],  # ['■'],
                           'dead_ship': [],  # ['X'],
                           'contour': [],  # ['O'],
                           'miss': [],  # ['T'],
                           'damaged_ship': [],  # ['□'],
                           'dots_out_of_play': [],  # ['~']
                           'free_dots': [Dot(x, y) for x in range(1, 7) for y in range(1, 7)]}
        self.hide = hide
        self.ships_on_board = []

    def get_ship_count(self):
        return len(self.ships_on_board)

    def draw_board(self):
        for x in range(len(self.board) + 1):
            for y in range(len(self.board) + 1):
                if Dot(x, y) in self.board_dots['free_dots']:
                    self.board[x - 1][y - 1] = 'O'
                elif Dot(x, y) in self.board_dots['miss']:
                    self.board[x - 1][y - 1] = 'T'
                elif Dot(x, y) in self.board_dots['dead_ship']:
                    self.board[x - 1][y - 1] = 'X'
                elif Dot(x, y) in self.board_dots['damaged_ship']:
                    self.board[x - 1][y - 1] = '□'
                elif Dot(x, y) in self.board_dots['dots_out_of_play']:
                    self.board[x - 1][y - 1] = '~'

                elif Dot(x, y) in self.board_dots['ships']:
                    self.board[x - 1][y - 1] = '■'

        print('\n')
        print(' ' * 9 + 'Ваша доска:\n')
        print(' ' * 4 + '| ' + ' | '.join(map(str, range(1, 7))) + ' |')
        for x in range(len(self.board)):
            print(f'| {x + 1} | ' + " | ".join(map(str, self.board[x])) + " |")

    def add_ship(self, ship):
        for dot in range(len(ship.get_all_dots())):
            self.board_dots['free_dots'].remove(ship.get_all_dots()[dot])
            self.board_dots['ships'].append(ship.get_all_dots()[dot])

        self.ships_on_board.append(ship)
        self.mark_contour(ship)

    def mark_contour(self, ship):
        for ship_dot in ship.get_all_dots():
            contour_for_dot = ship_dot.generate_surrounding_dots()

            if ship.get_ship_health() != 0:
                for dot in contour_for_dot:
                    if any([dot in self.board_dots['contour'],
                            dot in self.board_dots['ships']]):
                        continue
                    self.board_dots['free_dots'].remove(dot)
                    self.board_dots['contour'].append(dot)

            if ship.get_ship_health() == 0:
                for dot in contour_for_dot:
                    if any([dot in self.board_dots['dead_ship'],
                            dot in self.board_dots['dots_out_of_play']]):
                        continue
                    self.board_dots['dots_out_of_play'].append(dot)
                    for key, value in self.board_dots.items():
                        if all([dot in value,
                                key != 'dots_out_of_play']):
                            self.board_dots[key].remove(dot)

    def get_damaged_dots(self):
        result = []
        for key, value in self.board_dots.items():
            if key == 'damaged_ship':
                for dot in value:
                    result.append(dot)
        return result

    def get_dead_ship_dots(self):
        result = []
        for key, value in self.board_dots.items():
            if key == 'dead_ship':
                for dot in value:
                    result.append(dot)
        return result

    def get_dots_out_of_play(self):
        result = []
        for key, value in self.board_dots.items():
            if key == 'dots_out_of_play':
                for dot in value:
                    result.append(dot)
        return result

    def get_free_dots(self):
        result = []
        for key, value in self.board_dots.items():
            if key == 'free_dots':
                for dot in value:
                    result.append(dot)
        return result

    def get_miss_dots(self):
        result = []
        for key, value in self.board_dots.items():
            if key == 'miss':
                for dot in value:
                    result.append(dot)
        return result

    def get_dots_for_ai(self):
        result = []
        for key, value in self.board_dots.items():
            if key == 'ships':
                for dot in value:
                    result.append(dot)
            if key == 'contour':
                for dot in value:
                    result.append(dot)
            if key == 'free_dots':
                for dot in value:
                    result.append(dot)
        return result

    def check_ship_fits(self, ship):
        for dot in ship.get_all_dots():
            if dot not in self.board_dots['free_dots']:
                return False
        else:
            return True

    def set_default_board(self):
        self.ships_on_board.clear()
        self.board_dots = {'ships': [],  # ['■'],
                           'dead_ship': [],  # ['X'],
                           'contour': [],  # ['O'],
                           'miss': [],  # ['T'],
                           'damaged_ship': [],  # ['□'],
                           'dots_out_of_play': [],  # ['~']
                           'free_dots': [Dot(x, y) for x in range(1, 7) for y in range(1, 7)]}

    def generate_board(self):
        while self.get_ship_count() != 7:

            while self.get_ship_count() == 0:
                ship_3_deck = Ship(3, random.choice(self.get_free_dots()), random.randrange(0, 4))
                if self.check_ship_fits(ship_3_deck):
                    self.add_ship(ship_3_deck)
                else:
                    continue

            while self.get_ship_count() in range(1, 3):
                ship_2_deck = Ship(2, random.choice(self.get_free_dots()), random.randrange(0, 4))
                if self.check_ship_fits(ship_2_deck):
                    self.add_ship(ship_2_deck)
                else:
                    continue

            while self.get_ship_count() in range(3, 7):
                if len(self.get_free_dots()) == 0:
                    self.set_default_board()
                    break
                else:
                    ship_1_deck = Ship(1, random.choice(self.get_free_dots()), random.randrange(0, 4))
                    if self.check_ship_fits(ship_1_deck):
                        self.add_ship(ship_1_deck)
                    else:
                        continue

    @staticmethod
    def dot_out_of_play(dot):
        return dot not in [Dot(x, y) for x in range(1, 7) for y in range(1, 7)]

    def get_shot(self, dot):
        if dot in self.board_dots['dead_ship']:
            return 'Retry.'
        if dot in self.board_dots['miss']:
            return 'Retry.'
        if dot in self.board_dots['damaged_ship']:
            return 'Retry.'
        if dot in self.board_dots['dots_out_of_play']:
            return 'Retry.'

        if dot in self.board_dots['contour']:
            self.board_dots['contour'].remove(dot)
            self.board_dots['miss'].append(dot)
            return 'Miss.'
        if dot in self.board_dots['free_dots']:
            self.board_dots['free_dots'].remove(dot)
            self.board_dots['miss'].append(dot)
            return 'Miss'

        if dot in self.board_dots['ships']:
            for ship in self.ships_on_board:
                if dot in ship.get_all_dots():
                    ship.got_shot()
                    if ship.get_ship_health() != 0:
                        self.board_dots['ships'].remove(dot)
                        self.board_dots['damaged_ship'].append(dot)
                        return 'Retry.'
                    if ship.get_ship_health() == 0:
                        for ship_dot in ship.get_all_dots():
                            self.board_dots['dead_ship'].append(ship_dot)
                            for key, value in self.board_dots.items():
                                if all([ship_dot in value,
                                        key != 'dead_ship']):
                                    self.board_dots[key].remove(ship_dot)
                        self.mark_contour(ship)
                        self.ships_on_board.remove(ship)
                        return 'Retry.'


class Board_AI(Board):
    def __init__(self):
        super().__init__(hide=True)

    def switch_Visibility(self):
        if self.hide is False:
            self.hide = True
        else:
            self.hide = False

    def draw_board(self):
        for x in range(len(self.board) + 1):
            for y in range(len(self.board) + 1):
                if Dot(x, y) in self.board_dots['free_dots']:
                    self.board[x - 1][y - 1] = 'O'
                elif Dot(x, y) in self.board_dots['miss']:
                    self.board[x - 1][y - 1] = 'T'
                elif Dot(x, y) in self.board_dots['dead_ship']:
                    self.board[x - 1][y - 1] = 'X'
                elif Dot(x, y) in self.board_dots['damaged_ship']:
                    self.board[x - 1][y - 1] = '□'
                elif Dot(x, y) in self.board_dots['dots_out_of_play']:
                    self.board[x - 1][y - 1] = '~'

                elif Dot(x, y) in self.board_dots['ships']:
                    if self.hide is False:
                        self.board[x - 1][y - 1] = '■'
                    else:
                        self.board[x - 1][y - 1] = 'O'

        print('\n')
        print(' ' * 6 + 'Доска противника:\n')
        print(' ' * 4 + '| ' + ' | '.join(map(str, range(1, 7))) + ' |')
        for x in range(len(self.board)):
            print(f'| {x + 1} | ' + " | ".join(map(str, self.board[x])) + " |")


class Player:
    def __init__(self):
        self.board = Board(hide=False)

    def ask_for_shot(self, enemy):
        pass

    def turn(self, enemy):
        dot = self.ask_for_shot(enemy)
        shot_status = enemy.board.get_shot(dot)

        if shot_status != 'Miss.':
            return True
        else:
            return False


class User(Player):
    def __init__(self):
        super().__init__()
        self.name = 'User'

    def ask_for_shot(self, enemy):
        while True:
            try:
                player_input = input('\nКуда стреляем, капитан? ')
                if any([not player_input.isdigit(),
                        not len(player_input) == 2]):
                    raise WrongShotFormat
                if enemy.board.dot_out_of_play(Dot(int(player_input) // 10, int(player_input) % 10)):
                    raise WrongBoardCoord
                if any([Dot(int(player_input) // 10, int(player_input) % 10) in enemy.board.get_miss_dots(),
                        Dot(int(player_input) // 10, int(player_input) % 10) in enemy.board.get_dots_out_of_play()]):
                    raise WrongShotDot
                if Dot(int(player_input) // 10, int(player_input) % 10) in enemy.board.get_damaged_dots():
                    raise WrongShotInDamagedShip
                if Dot(int(player_input) // 10, int(player_input) % 10) in enemy.board.get_dead_ship_dots():
                    raise WrongShotInDeadShip
            except WrongBoardCoord:
                print('Вы промахнулись по доске. Повторите выстрел.')
                continue
            except WrongShotFormat:
                print('Неверный формат ввода. Повторите выстрел.')
                continue
            except WrongShotDot:
                print('Здесь уж точно не может быть корабля. Повторите выстрел.')
                continue
            except WrongShotInDamagedShip:
                print('Эта точка уже является частью раненого корабля. Повторите выстрел.')
                continue
            except WrongShotInDeadShip:
                print('Этот корабль уже уничтожен. Повторите выстрел.')
                continue
            else:
                player_input = int(player_input)
                x = player_input // 10
                y = player_input % 10
                return Dot(x, y)


class AI(Player):
    def __init__(self):
        super().__init__()
        self.board = Board_AI()
        self.name = 'AI'

    def ask_for_shot(self, enemy):
        if len(enemy.board.get_damaged_dots()) == 1:
            shot_variants = enemy.board.get_damaged_dots()[0].generate_crest_dots()
            for dot in shot_variants:
                if dot in enemy.board.get_miss_dots():
                    shot_variants.remove(dot)
            dot = random.choice(shot_variants)
            return dot
        elif len(enemy.board.get_damaged_dots()) == 2:
            shot_variants = []
            damaged_ship = enemy.board.get_damaged_dots()

            if damaged_ship[0].get_x() == damaged_ship[1].get_x():
                shot_variants_for_y = sorted(damaged_ship, key=lambda x: x.get_y())
                if shot_variants_for_y[0].get_y() - 1 in range(1, 7):
                    shot_variants.append(Dot(shot_variants_for_y[0].get_x(), shot_variants_for_y[0].get_y() - 1))
                if shot_variants_for_y[1].get_y() + 1 in range(1, 7):
                    shot_variants.append(Dot(shot_variants_for_y[1].get_x(), shot_variants_for_y[1].get_y() + 1))

            if damaged_ship[0].get_y() == damaged_ship[1].get_y():
                shot_variants_for_x = sorted(damaged_ship, key=lambda x: x.get_x())
                if shot_variants_for_x[0].get_x() - 1 in range(1, 7):
                    shot_variants.append(Dot(shot_variants_for_x[0].get_x() - 1, shot_variants_for_x[0].get_y()))
                if shot_variants_for_x[1].get_x() + 1 in range(1, 7):
                    shot_variants.append(Dot(shot_variants_for_x[1].get_x() + 1, shot_variants_for_x[1].get_y()))
            dot = random.choice(shot_variants)
            return dot
        else:
            dot = random.choice(enemy.board.get_dots_for_ai())
            return dot


class Game:
    def __init__(self):
        self.user_player = User()
        self.user_board = self.user_player.board
        self.ai_player = AI()
        self.ai_board = self.ai_player.board
        self.players = []

    def greet(self):
        text_greet = ("\nCыграем в Морской бой."
                      "\n\nВ данной вариации размер поля будет 6 на 6 клеток."
                      "\nОбщее количество кораблей для каждого игрока 7, а именно:"
                      "\n\n3ёх палубный корабль - 1шт;"
                      "\n2ух палубный корабль - 2шт;"
                      "\n1но палубный корабль - 4шт."
                      "\n\nВы будете играть с искусственным интеллектом, \nа доски будут сгенерированны автоматически."
                      "\n\nДля того, чтоб ваш ход учелся, дайте ответ в виде числа,"
                      "\nгде перва цифра отображает номер ряда, а вторая - столбика.\n"
                      "\n\nЛегенда: \n"
                      "\n'■' - целый корабль;"
                      "\n'X' - полность уничтоженный корабль;"
                      "\n'O' - свободные для хода клетки;"
                      "\n'T' - промах;"
                      "\n'□' - раненый корабль;"
                      "\n'~' - контур унитоженного корабля.")

        print(text_greet)

    def switch_players(self):
        self.players.append(self.players.pop(0))

    def draw_players_boards(self):
        self.user_board.draw_board()
        self.ai_board.draw_board()

    def check_end_of_game(self):
        if any([self.user_board.get_ship_count() == 0,
                self.ai_board.get_ship_count() == 0]):
            return True
        else:
            return False

    def loop(self):
        self.players = [self.user_player, self.ai_player]
        self.user_board.generate_board()
        self.ai_board.generate_board()
        self.draw_players_boards()

        while True:
            if not self.check_end_of_game():
                print(f'\nХод {self.players[0].name}.')
                result = self.players[0].turn(self.players[1])

                if result:
                    self.draw_players_boards()
                    print('\nПопадание. Продолжайте.')
                    continue
                else:
                    self.switch_players()
                    self.draw_players_boards()
                    print('\nПромах. Передаем ход.')
                    continue
            else:
                break

        if self.check_end_of_game():
            if self.user_board.get_ship_count() == 0:
                self.ai_board.switch_Visibility()
                print(f'\nПобеда {self.ai_player.name}.')
                self.draw_players_boards()
            elif self.ai_board.get_ship_count() == 0:
                self.ai_board.switch_Visibility()
                print(f'\nПобеда {self.user_player.name}.')
                self.draw_players_boards()

    def start_game(self):
        self.greet()
        self.loop()


game = Game()
game.start_game()
