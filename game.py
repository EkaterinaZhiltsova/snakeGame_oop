import pygame
import random

from accessify import protected

import os

try:
    os.environ["DISPLAY"]
except:
    os.environ["SDL_VIDEODRIVER"] = "dummy"

# Импорт модуля отрисовки
import drawing

pygame.init()

DIS_WIDTH = 600
DIS_HEIGHT = 400

SNAKE_BLOCK = 10
SNAKE_SPEED = 5

dis = pygame.display.set_mode((DIS_WIDTH, DIS_HEIGHT + 50))
pygame.display.set_caption('Snake Game')

clock = pygame.time.Clock()


# Класс: змейка
class Snake(object):
    def __init__(self, segments):
        self.segments = segments
        self.length = len(self)     # или 1
        self.x_change = 0
        self.y_change = 0
        # self.head = self.segments[-1]
        self.x = (self.segments[-1])[0]
        self.y = (self.segments[-1])[1]

    def __len__(self):
        return len(self.segments)

    # Проверка столкновения (проигрышной ситуации) змейки с самой собой или с другой змейкой
    def collision_check_with(self, another_snake_list):
        for coord in self.segments[:-1]:
            if coord == self.segments[-1]:
                return True
        if self.segments[-1] in another_snake_list:
            return True
        return False

    # Проверка окончания игры (проигрышной ситуации врезания в границы поля)
    def losing_situation(self):
        if self.x >= DIS_WIDTH or self.x < 0 or self.y >= DIS_HEIGHT or self.y < 0:
            return True
        else:
            return False

    # Перемещение змеи на шаг (всех блоков тела) в координатах и увеличение длины, если змея заработала очко
    def move_snake_blocks(self):
        self.segments.append([self.x, self.y])
        if len(self) > self.length:
            del self.segments[0]

    # Проверка нахождения змейкой еды (увеличение счета)
    def find_food(self, food_x, food_y):
        if self.x == food_x and self.y == food_y:
            self.length += 1
            return True
        return False

    # Проверка, может ли змейка сделать шаг в новые координаты без проигрыша
    # _protected метод
    @protected
    def _can_take_a_step(self, x, y, another_snake_list):
        possible_snake = Snake([[x, y]])
        if ((not possible_snake.losing_situation())
                and ([x, y] not in self.segments)
                and ([x, y] not in another_snake_list)):
            return True
        return False


# Класс: самостоятельная (игровая) змейка-соперник (наследуется от класса змейка)
class CompetitorSnake(Snake):
    # У класса CompetitorSnake нет своего конструктора, поэтому он наследует его от родителя Snake

    # Расчет следующего шага змеи-соперника
    def independent_snake_movement(self, food_x, food_y, controlled_snake_list):
        # Рассчет расстояния до еды в разных направлениях
        right = food_x - self.x
        left = -right
        bottom = food_y - self.y
        top = -bottom

        points = [right, left, bottom, top]
        points.sort(reverse=True)  # выбор кратчайшего расстояния

        flag = 0
        for current_point in points:
            if current_point == right:
                if self._can_take_a_step(self.x + SNAKE_BLOCK, self.y, controlled_snake_list):
                    self.x_change = SNAKE_BLOCK
                    self.y_change = 0
                    flag = -1
                    break
            elif current_point == left:
                if self._can_take_a_step(self.x - SNAKE_BLOCK, self.y, controlled_snake_list):
                    self.x_change = -SNAKE_BLOCK
                    self.y_change = 0
                    flag = -1
                    break
            elif current_point == bottom:
                if self._can_take_a_step(self.x, self.y + SNAKE_BLOCK, controlled_snake_list):
                    self.y_change = SNAKE_BLOCK
                    self.x_change = 0
                    flag = -1
                    break
            elif current_point == top:
                if self._can_take_a_step(self.x, self.y - SNAKE_BLOCK, controlled_snake_list):
                    self.y_change = -SNAKE_BLOCK
                    self.x_change = 0
                    flag = -1
                    break

        if flag == 0:
            print("No possible moves")
            if self._can_take_a_step(self.x + SNAKE_BLOCK, self.y, controlled_snake_list):
                self.x_change = SNAKE_BLOCK
                self.y_change = 0
            elif self._can_take_a_step(self.x - SNAKE_BLOCK, self.y, controlled_snake_list):
                self.x_change = -SNAKE_BLOCK
                self.y_change = 0
            elif self._can_take_a_step(self.x, self.y + SNAKE_BLOCK, controlled_snake_list):
                self.y_change = SNAKE_BLOCK
                self.x_change = 0
            elif self._can_take_a_step(self.x, self.y - SNAKE_BLOCK, controlled_snake_list):
                self.y_change = -SNAKE_BLOCK
                self.x_change = 0
            else:
                print("No possible moves")
                
    # @staticmethod
    # def static_check_can_move(competitor_list, x, y, controlled_list):
        # comp_snake = CompetitorSnake(competitor_list)
        # return comp_snake._can_take_a_step(x, y, controlled_list)

    def check_can_move(self, x, y, controlled_list):
        return self._can_take_a_step(x, y, controlled_list)


# Класс: еда (яблоко)
class Food(object):
    # Вычисление новых случайных координат для яблока на поле
    # def random_food
    def __init__(self, controlled_snake_list, competitor_snake_list, width, height):
        self.x = round(random.randrange(0, width - SNAKE_BLOCK) / 10.0) * 10.0
        self.y = round(random.randrange(0, height - SNAKE_BLOCK) / 10.0) * 10.0
        while ([self.x, self.y] in controlled_snake_list) or ([self.x, self.y] in competitor_snake_list):
            self.x = round(random.randrange(0, width - SNAKE_BLOCK) / 10.0) * 10.0
            self.y = round(random.randrange(0, height - SNAKE_BLOCK) / 10.0) * 10.0


# Основной цикл игры
def game_loop(game_over=False):
    game_close = False

    # controlled - управляемая змейка  (№1)
    controlled_snake = Snake([[DIS_WIDTH / 3 * 2, DIS_HEIGHT / 2]])

    # competitor - самостоятельная (игровая) змейка-соперник (№2)
    competitor_snake = CompetitorSnake([[DIS_WIDTH / 3, DIS_HEIGHT / 2]])

    food = Food(controlled_snake.segments, competitor_snake.segments, DIS_WIDTH, DIS_HEIGHT)

    display = drawing.Display(dis, DIS_WIDTH, DIS_HEIGHT)

    while not game_over:

        while game_close:
            display.draw_background()   # отрисовка фона

            display.message("Game over!", DIS_WIDTH / 8, 100)   # отрисовка сообщения об окончании игры

            finish_message = ""
            if (controlled_snake.length - 1) > (competitor_snake.length - 1):
                finish_message = "You win!"
            elif (controlled_snake.length - 1) < (competitor_snake.length - 1):
                finish_message = "You lost!"
            else:
                finish_message = "Same score!"

            display.message(finish_message, DIS_WIDTH / 8, 140)  # отрисовка сообщения
            display.message("Press C to play again or Q to quit", DIS_WIDTH / 8, 220)  # отрисовка сообщения

            # Отрисовка счета
            display.show_scores(controlled_snake.length - 1, competitor_snake.length - 1)
            pygame.display.update()

            # Отслеживание реакции на действия пользователя
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                    game_close = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        game_loop()

        if game_over:
            continue

        # Рассчет следующего шага змеи-соперника
        competitor_snake.independent_snake_movement(food.x, food.y, controlled_snake.segments)

        # Отслеживание реакции на действия пользователя
        for event in pygame.event.get():
            # Для закрытия приложения
            if event.type == pygame.QUIT:
                game_over = True
                game_close = False
            # Реакция на нажатие стрелок
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    controlled_snake.x_change = -SNAKE_BLOCK
                    controlled_snake.y_change = 0
                elif event.key == pygame.K_RIGHT:
                    controlled_snake.x_change = SNAKE_BLOCK
                    controlled_snake.y_change = 0
                elif event.key == pygame.K_UP:
                    controlled_snake.y_change = -SNAKE_BLOCK
                    controlled_snake.x_change = 0
                elif event.key == pygame.K_DOWN:
                    controlled_snake.y_change = SNAKE_BLOCK
                    controlled_snake.x_change = 0

        # Изменение координат управляемой змейки
        controlled_snake.x += controlled_snake.x_change
        controlled_snake.y += controlled_snake.y_change

        # Изменение координат самостоятельной (игровой) змейки-соперника
        competitor_snake.x += competitor_snake.x_change
        competitor_snake.y += competitor_snake.y_change

        # Перемещение змеи на шаг (всех блоков тела) в координатах и увеличение длины, если змея заработала очко
        controlled_snake.move_snake_blocks()
        competitor_snake.move_snake_blocks()

        # Проверка окончания игры (если game_close == True, игра заканчивается)
        game_close = controlled_snake.losing_situation() or competitor_snake.losing_situation()

        # Проверка столкновения управляемой змейки с собой и со змейкой-соперником
        # и столкновения змейки-соперника с собой и с управляемой змейкой
        game_close = (game_close or controlled_snake.collision_check_with(competitor_snake.segments)
                      or competitor_snake.collision_check_with(controlled_snake.segments))
        # теперь надо 2 проверки collision_check: для каждой змейки при столкновении с другой

        if game_close:
            continue

        # Отрисовка основных объектов на поле игры
        display.draw_field(food.x, food.y, SNAKE_BLOCK)

        # Отрисовка змей на экране игры
        display.draw_snakes(SNAKE_BLOCK, controlled_snake.segments, competitor_snake.segments)

        # Отрисовка счета (для обеих змеек) на экране игры
        display.show_scores(controlled_snake.length - 1, competitor_snake.length - 1)

        pygame.display.update()

        # Проверка нахождения змейкой еды (увеличение счета)
        flag_find = controlled_snake.find_food(food.x, food.y) or competitor_snake.find_food(food.x, food.y)
        # теперь надо 2 проверки find_food: для каждой змейки

        # Если нашла еду, надо сгенерировать новое положение еды на поле (новый экземпляр класса Food)
        if flag_find:
            food = Food(controlled_snake.segments, competitor_snake.segments, DIS_WIDTH, DIS_HEIGHT)

        clock.tick(SNAKE_SPEED)

    pygame.quit()
    quit()


if __name__ == '__main__':
    game_loop()
