import arcade
import random
import math

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 900
SCREEN_TITLE = "Virus"

HOUSES = 20
HOUSE_WIDTH = 50
PERSON_RADIUS = 5

class Person:
    def __init__(self, center_x, center_y):
        self.center_x = center_x
        self.center_y = center_y
        self.infected = False
        self.infected_ticks = 0
        self.radius = PERSON_RADIUS

    def on_update(self, delta_time):
        if self.infected:
            self.infected_ticks += 1

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

        for person in self.persons:
            person.on_draw()

class Game(arcade.Window):
    def __init__(self):
        super().__init__(width=SCREEN_WIDTH, height=SCREEN_HEIGHT, title=SCREEN_TITLE)

        self.houses = []

        grid = [0, 0]
        grid[0] = int(math.sqrt(HOUSES))
        grid[1] = HOUSES // grid[0]
    
        for y in range(grid[1]):
            for x in range(grid[0]):
                center_x = x * ( SCREEN_WIDTH / grid[0] ) + (0.5 * ( SCREEN_WIDTH / grid[0] ))
                center_y = y * ( SCREEN_HEIGHT / grid[1] ) + (0.5 * ( SCREEN_HEIGHT / grid[1] ) )
                self.houses.append(
                    House(
                        HOUSE_WIDTH,
                        HOUSE_WIDTH,
                        center_x,
                        center_y
                    )
                )
        
        for house in self.houses:
            for i in range(random.randint(1, 5)):
                house.persons.append(
                    Person(
                        house.center_x + (random.randint(0, (HOUSE_WIDTH - PERSON_RADIUS) // 2) * random.choice([1, -1])),
                        house.center_y + (random.randint(0, (HOUSE_WIDTH - PERSON_RADIUS) // 2) * random.choice([1, -1])),
                    )
                )

        
    def on_update(self, delta_time):
        for house in self.houses:
            for person in house.persons:
                person.on_update(delta_time)

    def on_draw(self):
        arcade.start_render()
        
        for house in self.houses:
            house.on_draw()


def main():
    game = Game()
    arcade.run()


if __name__ == "__main__":
    main()