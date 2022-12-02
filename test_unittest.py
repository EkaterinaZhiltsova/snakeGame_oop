import unittest
from mock import patch
import mock

import game


class TestGame(unittest.TestCase):
    # Блочные тесты на метод losing_situation
    # Позитивный тест
    def test_not_losing_situation_positive(self):
        snake = game.Snake([[200, 300]])
        self.assertFalse(snake.losing_situation())  # False - ситуация не проигрышная

    # Позитивный тест
    def test_not_losing_situation_positive_2(self):
        snake = game.Snake([[590, 390]])
        self.assertFalse(snake.losing_situation())  # False - ситуация не проигрышная (краевой случай)

    # Негативный тест
    def test_losing_situation_negative(self):
        snake = game.Snake([[600, 400]])
        self.assertTrue(snake.losing_situation())  # True - ситуация проигрышная (краевой случай)

    # Негативный тест
    def test_losing_situation_negative_2(self):
        snake = game.Snake([[-10, -10]])
        self.assertTrue(snake.losing_situation())  # True - ситуация проигрышная (краевой случай)

    # Блочные тесты на метод collision_check_with
    # Позитивный тест (ситуация не проигрышная)
    # Змейки не врезаются
    def test_not_collision_check_with_positive(self):
        snake = game.Snake([[230.0, 350.0]])
        self.assertFalse(snake.collision_check_with([[290.0, 370.0], [290.0, 380.0]]))  # False - ситуация не проигрышная

    # Негативный тест (ситуация проигрышная)
    # Змейка врезалась в другую
    def test_collision_check_with_negative_1(self):
        snake = game.Snake([[280.0, 350.0]])
        self.assertTrue(snake.collision_check_with([[280.0, 360.0], [280.0, 350.0], [280.0, 340.0]]))    # True - ситуация проигрышная

    # Негативный тест (ситуация проигрышная)
    # Змейка врезалась в себя
    def test_collision_check_with_negative_2(self):
        snake = game.Snake([[150.0, 200.0], [150.0, 210.0], [150.0, 220.0], [160.0, 220.0], [160.0, 210.0], [150.0, 210.0]])
        self.assertTrue(snake.collision_check_with([[210.0, 170.0], [220.0, 170.0], [220.0, 160.0], [230.0, 160.0], [240.0, 160.0], [250.0, 160.0], [260.0, 160.0], [270.0, 160.0], [280.0, 160.0], [290.0, 160.0]]))

    # Блочные тесты на метод find_food
    # Позитивный тест (змейка нашла еду)
    def test_find_food_positive(self):
        snake = game.Snake([[400.0, 160.0]])
        self.assertTrue(snake.find_food(400.0, 160.0))

    # Негативный тест (змейка не нашла еду)
    def test_find_food_negative(self):
        snake = game.Snake([[580.0, 200.0]])
        self.assertFalse(snake.find_food(150.0, 210.0))

    # Блочные тесты на метод move_snake_blocks
    # Позитивный тест (с увеличением длины при добавлением очка)
    def test_move_snake_blocks_positive(self):
        snake = game.Snake([[120.0, 90.0], [120.0, 80.0]])
        snake.x = 130.0
        snake.y = 80.0
        snake.length += 1
        snake.move_snake_blocks()
        self.assertEqual(snake.segments, [[120.0, 90.0], [120.0, 80.0], [130.0, 80.0]])

    # Позитивный тест (без увеличения длины без добавления очка)
    def test_move_snake_blocks_positive_2(self):
        snake = game.Snake([[100.0, 140.0], [100.0, 130.0]])
        snake.x = 100.0
        snake.y = 120.0
        snake.move_snake_blocks()
        self.assertEqual(snake.segments, [[100.0, 130.0], [100.0, 120.0]])

    # Негативный тест (выход за пределы поля без добавления очка)
    def test_move_snake_blocks_negative(self):
        snake = game.Snake([[580.0, 110.0], [590.0, 110.0]])
        snake.x = 600.0
        snake.y = 110.0
        snake.move_snake_blocks()
        self.assertEqual(snake.segments, [[590.0, 110.0], [600.0, 110.0]])

    # Негативный тест (змейка заполняет всё поле и выходит за него)
    def test_move_snake_blocks_negative_2(self):
        full_screen_snake_list = []
        full_screen_snake_list_new = []
        for i in range(0, 400, 10):
            for j in range(0, 600, 10):
                y = j
                if i % 20 != 0:
                    y = 590 - j
                full_screen_snake_list.append([float(i), float(y)])
                full_screen_snake_list_new.append([float(i), float(y)])

        snake = game.Snake(full_screen_snake_list)
        full_screen_snake_list_new.append([400.0, 0.0])
        snake.x = 400.0
        snake.y = 0.0
        snake.length += 1
        snake.move_snake_blocks()
        self.assertEqual(snake.segments, full_screen_snake_list_new)

    # Блочные тесты на метод Food.__init__
    # Позитивный тест
    def test_random_food_position_when_init_positive(self):
        food = game.Food([[720.0, 250.0], [730.0, 250.0]],
                         [[560.0, 160.0], [560.0, 150.0], [570.0, 150.0], [570.0, 140.0]], 600, 400)
        # True - функция выдает подходящие случайные значения для размещения еды внутри игрового поля
        self.assertTrue(0 <= food.x < 600 and 0 <= food.y < 400)

    # Негативный тест
    def test_random_food_position_when_init_negative(self):
        width = 1000
        height = 300
        food = game.Food([[720.0, 250.0], [730.0, 250.0]],
                         [[560.0, 160.0], [560.0, 150.0], [570.0, 150.0], [570.0, 140.0]], width, height)
        # True - функция выдает подходящие случайные значения для размещения еды внутри игрового поля
        # c заявленными width и height (неправильными размерами поля)
        self.assertTrue(0 <= food.x < width and 0 <= food.y < height)

    # Блочные тесты на метод CompetitorSnake.independent_snake_movement
    # С mock-объектом на вызываемый метод losing_situation
    # Позитивный тест
    def test_unit_independent_snake_movement_positive(self):
        with patch('game.Snake.losing_situation') as losing_situation_mock:
            losing_situation_mock.return_value = False
            # при True -> No possible moves (0, 0)
            competitor_snake = game.CompetitorSnake([[150.0, 270.0], [150.0, 280.0]])
            competitor_snake.independent_snake_movement(180.0, 310.0, [[600.0, 200.0]])
            self.assertEqual(
                (competitor_snake.x_change, competitor_snake.y_change),
                (10, 0))

    # Негативный тест (нет возможных перемещений)
    def test_unit_independent_snake_movement_negative(self):
        with patch('game.Snake.losing_situation') as losing_situation_mock:
            losing_situation_mock.return_value = False
            competitor_snake = game.CompetitorSnake([[430.0, 220.0], [440.0, 220.0], [440.0, 230.0], [450.0, 230.0], [450.0, 240.0], [460.0, 240.0], [460.0, 250.0], [470.0, 250.0], [470.0, 260.0], [480.0, 260.0], [480.0, 270.0], [490.0, 270.0], [490.0, 280.0], [500.0, 280.0], [500.0, 290.0], [490.0, 290.0], [480.0, 290.0], [470.0, 290.0], [460.0, 290.0], [450.0, 290.0], [440.0, 290.0], [430.0, 290.0], [420.0, 290.0], [410.0, 290.0], [400.0, 290.0], [390.0, 290.0], [390.0, 280.0], [390.0, 270.0], [390.0, 260.0], [390.0, 250.0], [400.0, 250.0], [400.0, 240.0], [410.0, 240.0], [410.0, 230.0], [420.0, 230.0], [420.0, 240.0], [420.0, 250.0], [410.0, 250.0], [410.0, 260.0], [400.0, 260.0], [400.0, 270.0], [400.0, 280.0], [410.0, 280.0], [410.0, 270.0], [420.0, 270.0], [420.0, 260.0], [430.0, 260.0], [430.0, 250.0], [430.0, 240.0], [430.0, 230.0], [430.0, 230.0]])
            competitor_snake.independent_snake_movement(20.0, 90.0, [[400.0, 200.0]])
            self.assertEqual(
                (competitor_snake.x_change, competitor_snake.y_change),
                (0, 0))
     
    # Блочные тесты на protected метод Snake._can_take_a_step через метод check_can_move
    # Позитивный тест
    def test_can_take_a_step_positive(self):
        competitor_snake = game.CompetitorSnake([[250.0, 200.0], [260.0, 200.0]])
        # self.assertTrue(competitor_snake._can_take_a_step(270.0, 200.0, [[400.0, 200.0]]))

        # self.assertTrue(game.CompetitorSnake.static_check_can_move([[250.0, 200.0], [260.0, 200.0]],
                                                                   # 270.0, 200.0, [[400.0, 200.0]]))
        self.assertTrue(competitor_snake.check_can_move(270.0, 200.0, [[400.0, 200.0]]))

    # Негативный тест
    def test_can_take_a_step_negative(self):
        competitor_snake = game.CompetitorSnake([[250.0, 200.0], [260.0, 200.0]])
        # self.assertFalse(game.CompetitorSnake.static_check_can_move([[250.0, 200.0], [260.0, 200.0]],
                                                                    # 270.0, 200.0, [[270.0, 200.0]]))
        self.assertFalse(competitor_snake.check_can_move(270.0, 200.0, [[270.0, 200.0]]))

    # Интеграционные тесты на метод independent_snake_movement -> вызываемый метод losing_situation
    # Позитивный тест
    def test_integration_independent_snake_movement_positive(self):
        competitor_snake = game.CompetitorSnake([[260.0, 90.0], [260.0, 80.0], [250.0, 80.0]])
        competitor_snake.independent_snake_movement(230.0, 50.0, [[400.0, 200.0]])
        self.assertEqual(
            (competitor_snake.x_change, competitor_snake.y_change),
            (0, -10))

    # Негативный тест (нет возможных перемещений)
    def test_integration_independent_snake_movement_negative(self):
        competitor_snake = game.CompetitorSnake([[430.0, 80.0], [440.0, 80.0], [440.0, 70.0], [430.0, 70.0], [420.0, 70.0], [420.0, 80.0], [410.0, 80.0], [410.0, 90.0], [400.0, 90.0], [400.0, 100.0], [390.0, 100.0], [380.0, 100.0], [370.0, 100.0], [360.0, 100.0], [350.0, 100.0], [340.0, 100.0], [330.0, 100.0], [320.0, 100.0], [310.0, 100.0], [310.0, 90.0], [320.0, 90.0], [330.0, 90.0], [340.0, 90.0], [350.0, 90.0], [360.0, 90.0], [370.0, 90.0], [380.0, 90.0], [390.0, 90.0], [390.0, 80.0], [380.0, 80.0], [370.0, 80.0], [360.0, 80.0], [350.0, 80.0], [340.0, 80.0], [330.0, 80.0], [320.0, 80.0], [310.0, 80.0], [310.0, 70.0], [320.0, 70.0], [330.0, 70.0], [340.0, 70.0], [350.0, 70.0], [360.0, 70.0], [370.0, 70.0], [380.0, 70.0], [390.0, 70.0], [400.0, 70.0], [400.0, 80.0], [400.0, 80.0]])
        competitor_snake.independent_snake_movement(310.0, 230.0, [[400.0, 200.0]])
        self.assertEqual(
            (competitor_snake.x_change, competitor_snake.y_change),
            (0, 0))


if __name__ == '__main__':
    unittest.main()
