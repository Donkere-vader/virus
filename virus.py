import arcade
import random

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 900
SCREEN_TITLE = "Virus"

HOUSES = 20
HOUSE_WIDTH = 30

class Person:
    def __init__(self, center_x, center_y):
        self.center_x = center_x
        self.center_y = center_y
        self.infected = False
        self.radius = 5

    def on_update(self):
        pass

    def on_draw(self):
        arcade.draw_circle_filled(self.center_x, self.center_y, self.radius, color= (255, 255, 255) if not self.infected else (255, 0, 0))

class House:
    def __init__(self, height, width, center_x, center_y):
        self.center_x = center_x
        self.center_y = center_y
        self.height = height
        self.width = width
        self.persons = []

    def on_draw(self):
        arcade.draw_rectangle_outline(center_x=self.center_x, center_y=self.center_y, width=self.width, height=self.height, border_width=1,color=(255, 255, 255))

class Game(arcade.Window):
    def __init__(self):
        super().__init__(width=SCREEN_WIDTH, height=SCREEN_HEIGHT, title=SCREEN_TITLE)

        self.houses = []
    
        for i in range(0, HOUSES):
            self.houses.append(
                House(
                    HOUSE_WIDTH, HOUSE_WIDTH, 20, 20
                )
            )

    def on_update(self, delta_time):
        pass

    def on_draw(self):
        arcade.start_render()
        
        for house in self.houses:
            house.on_draw()


def main():
    game = Game()
    arcade.run()


if __name__ == "__main__":
    main()