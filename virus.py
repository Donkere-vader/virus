import arcade
import random
import math

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 900
SCREEN_TITLE = "Virus"

HOUSES = 20
HOUSE_WIDTH = 50
PERSON_RADIUS = 5
PERSON_SPEED = 2

VISITING_CHANCE = 1 # out of 100


def check_in_area(pos: tuple, area: tuple):  # area has to be a rectangle
    if pos[0] > area[0][0] and pos[0] < area[1][0]:
        if pos[1] > area[0][1] and pos[1] < area[1][1]:
            return True
    return False


def calculate_distance(pos1: tuple, pos2: tuple):
    delta_x = abs(pos1[0] - pos2[0])
    delta_y = abs(pos1[1] - pos2[1])
    return math.sqrt(delta_x**2 + delta_y**2)


class Person:
    def __init__(self, house, center_x, center_y):
        self.center_x = center_x
        self.center_y = center_y
        self.infected = False
        self.infected_ticks = 0
        self.visiting = False
        self.visiting_ticks = 0
        self.visiting_time = 0
        self.radius = PERSON_RADIUS
        self.parent_house = house
        self.area = self.parent_house.area
        self.change_x = 0
        self.change_y = 0

    def on_update(self, delta_time):
        if self.infected:
            self.infected_ticks += 1

            if random.randint(0, 50000) < self.infected_ticks:
                game.living -= 1
                game.dead += 1
                self.parent_house.persons.remove(self)
                return

        if random.randint(0, 100) < VISITING_CHANCE:
            self.visiting = True
            self.visiting_time = random.randint(20, 100)
            self.area = random.choice(game.houses).area

        if check_in_area((self.center_x, self.center_y), self.area): # in the correct area
            if self.visiting:
                self.visiting_ticks += 1
                if self.visiting_ticks > self.visiting_time:
                    self.area = self.parent_house.area
                    self.visiting = False
                    self.visiting_ticks = 0 
                    self.visiting_time = 0

            self.go_to(self.area)
        else:
            self.random_change()

        self.center_x += self.change_x
        self.center_y += self.change_y
    
    def go_to(self, area: tuple):
        area_center = ((area[0][0] + area[1][0]) / 2, (area[0][1] + area[1][1] / 2))
        
        delta_x = area_center[0] - self.center_x
        delta_y = area_center[1] - self.center_y

        mul = PERSON_SPEED / calculate_distance((self.center_x, self.center_y), area_center)

        self.change_x = delta_x * mul
        self.change_y = delta_y * mul

    def random_change(self):
        self.change_x = random.randint(0, PERSON_SPEED) * random.choice([1, -1])
        self.change_y = math.sqrt(PERSON_SPEED ** 2 - self.change_x ** 2) * random.choice([1, -1])

    def on_draw(self):
        arcade.draw_circle_filled(self.center_x, self.center_y, self.radius, color=(255, 255, 255) if not self.infected else (255, 0, 0))

class House:
    def __init__(self, width, center_x, center_y):
        self.center_x = center_x
        self.center_y = center_y
        self.width = width
        self.persons = []
        self.area = ((self.center_x-self.width/2, self.center_y-self.width/2), (self.center_x+self.width/2, self.center_y+self.width/2))

    def on_draw(self):
        arcade.draw_rectangle_outline(center_x=self.center_x, center_y=self.center_y, width=self.width, height=self.width, border_width=1, color=(255, 255, 255))

        for person in self.persons:
            person.on_draw()


class Game(arcade.Window):
    def __init__(self):
        super().__init__(width=SCREEN_WIDTH, height=SCREEN_HEIGHT, title=SCREEN_TITLE)
        self.living = 0
        self.dead = 0

        self.houses = []

        grid = [0, 0]
        grid[0] = int(math.sqrt(HOUSES))
        grid[1] = HOUSES // grid[0]

        for y in range(grid[1]):
            for x in range(grid[0]):
                center_x = x * (SCREEN_WIDTH / grid[0]) + (0.5 * (SCREEN_WIDTH / grid[0]))
                center_y = y * (SCREEN_HEIGHT / grid[1]) + (0.5 * (SCREEN_HEIGHT / grid[1]))
                self.houses.append(
                    House(
                        HOUSE_WIDTH,
                        center_x,
                        center_y
                    )
                )

        for house in self.houses:
            for i in range(random.randint(1, 5)):
                i += 1  # to get rid of the warning
                self.living += 1
                house.persons.append(
                    Person(
                        house,
                        house.center_x + (random.randint(0, (HOUSE_WIDTH - PERSON_RADIUS) // 2) * random.choice([1, -1])),
                        house.center_y + (random.randint(0, (HOUSE_WIDTH - PERSON_RADIUS) // 2) * random.choice([1, -1])),
                    )
                )

        # make someone infected
        self.houses[random.randint(0, len(self.houses)-1)].persons[0].infected = True

    def on_update(self, delta_time):
        for house in self.houses:
            for person in house.persons:
                person.on_update(delta_time)

    def on_draw(self):
        arcade.start_render()

        for house in self.houses:
            house.on_draw()


def main():
    global game
    game = Game()
    arcade.run()


if __name__ == "__main__":
    main()
