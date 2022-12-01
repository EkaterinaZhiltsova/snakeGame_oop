import pygame

light_green_color = (144, 238, 144)
green_color = (0, 128, 0)
dark_green_color = (0, 100, 0)
black_color = (0, 0, 0)
violet_color = (75, 0, 130)
red_color = (213, 50, 80)
brown_color = (139, 69, 19)
dark_red_color = (139, 0, 0)


# Класс: дисплей (поле отрисовки)
class Display(object):
    def __init__(self, display, dis_width, dis_height):
        self.dis = display
        self.width = dis_width
        self.height = dis_height

    # Отрисовка счета (для обеих змеек) на экране игры
    def show_scores(self, score1, score2):
        score_font = pygame.font.SysFont("verdana", 36)
        pygame.draw.rect(self.dis, green_color, [0, self.height, self.width, 50])  # фон для счета
        # управляемая змейка
        self._show_score(score1, violet_color, "Your score: ", 350, score_font)
        # змейка-соперник
        self._show_score(score2, black_color, "Score: ", 10, score_font)

    # Отрисовка счета (для одной змейки) на экране игры
    def _show_score(self, score, color, text, x_coord, score_font):
        value = score_font.render(text + str(score), True, color)  # счёт
        self.dis.blit(value, [x_coord, 402])

    # Вывод сообщения на экран игры
    def message(self, msg, x_coord, y_coord):
        font_style = pygame.font.SysFont("verdana", 22)
        mesg = font_style.render(msg, True, dark_red_color)
        self.dis.blit(mesg, [x_coord, y_coord])

    # Отрисовка змей на экране игры
    def draw_snakes(self, snake_block, controlled_snake_list, competitor_snake_list):
        # управляемая змейка
        self._draw_snake(snake_block, controlled_snake_list, violet_color)
        # змейка-соперник
        self._draw_snake(snake_block, competitor_snake_list, black_color)

    # Отрисовка змеи (каждого блока) на экране игры
    def _draw_snake(self, snake_block, snake_list, color):
        for block in snake_list:
            pygame.draw.rect(self.dis, color, [block[0], block[1], snake_block, snake_block])    # змея

    # Отрисовка фона
    def draw_background(self):
        self.dis.fill(light_green_color)  # зелёный фон

    # Отрисовка основных объектов
    def draw_field(self, foodx, foody, snake_block):
        self.draw_background()    # отрисовка фона
        pygame.draw.rect(self.dis, red_color, [foodx, foody, snake_block, snake_block])  # красное яблоко
        pygame.draw.rect(self.dis, brown_color, [foodx + 4, foody - 3, 2, 5])  # веточка
        pygame.draw.ellipse(self.dis, dark_green_color, (foodx + 4, foody - 4.5, 6, 3))  # листик
