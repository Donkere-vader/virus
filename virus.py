import arcade
import random
import math
import threading
import json

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
SCREEN_TITLE = "Virus"

HOUSES = 300
HOUSE_WIDTH = 20
PERSON_RADIUS = 5
PERSON_SPEED = 3
TRAVELING_SPEED = 10
SCREEN_PART_WIDTH = 50

DEFAULT_VISITING_CHANCE = 0.2 # out of 100 
VISITING_CHANCE = DEFAULT_VISITING_CHANCE


def check_in_area(pos: tuple, area: tuple):  # area has to be a rectangle
    if pos[0] > area[0][0] and pos[0] < area[1][0]:
        if pos[1] > area[0][1] and pos[1] < area[1][1]:
            return True
    return False


def calculate_distance(pos1: tuple, pos2: tuple):
    delta_x = abs(pos1[0] - pos2[0])
    delta_y = abs(pos1[1] - pos2[1])
    return math.sqrt(delta_x**2 + delta_y**2)


class Person(arcade.Sprite):
    def __init__(self, house, center_x: float, center_y: float, game):
        super().__init__(
            "person.png",
            scale=0.5,
            image_height=PERSON_RADIUS * 4,
            image_width=PERSON_RADIUS * 4,
            center_x=center_x,
            center_y=center_y
        )
        self.center_x = center_x
        self.center_y = center_y
        self.infected = False
        self.infected_ticks = 0
        self.visiting = False
        self.visiting_ticks = 0
        self.visiting_time = 0
        self.parent_house = house
        self.parent_game = game
        self.area = self.parent_house.area
        self.change_x = 0
        self.change_y = 0
        self.traveling = False
        self.recovered = False

        self.screen_part = [int(self.center_x // SCREEN_PART_WIDTH), int(self.center_y // SCREEN_PART_WIDTH)]
        self.parent_game.screen_parts[self.screen_part[0]][self.screen_part[1]].append(self)
        
        self.close_persons = []

        self.speed = PERSON_SPEED

    def on_update(self):
        _screen_part = [int(self.center_x // SCREEN_PART_WIDTH), int(self.center_y // SCREEN_PART_WIDTH)]
        if self.screen_part != _screen_part:
            self.parent_game.screen_parts[self.screen_part[0]][self.screen_part[1]].remove(self)
            self.screen_part = _screen_part
            self.parent_game.screen_parts[self.screen_part[0]][self.screen_part[1]].append(self)

        # if infected bigger chance to die
        if self.infected:
            self.infected_ticks += 1

            if random.randint(100, 50000) < self.infected_ticks:
                if random.randint(0, 100) <= 2:
                    self.die()
                    return
                else:
                    self.recover()

        elif not self.traveling and not self.recovered:
            # does someone infect me?
            for person in self.parent_game.screen_parts[self.screen_part[0]][self.screen_part[1]]:
                if person.infected and not person.traveling:
                    distance = calculate_distance((self.center_x, self.center_y), (person.center_x, person.center_y))
                    if distance < PERSON_RADIUS * 2:
                        self.infect()
                        break
        
        elif self.recovered: # Am i not recovered anymore??
            if random.uniform(0, 100) < 0.005:
                self.infectable() 


        # am i gonna visit?
        if random.uniform(0, 100) < VISITING_CHANCE:
            self.visiting = True
            self.visiting_time = random.randint(100, 1000)
            random_house = random.choice(self.parent_game.houses)
            while random_house.persons == 0:
                random_house = random.choice(self.parent_game.houses)
            self.area = random_house.area

        if random.uniform(0, 10000) < 1:
            self.visiting = True
            self.visiting_time = random.randint(10, 20)
            self.area = self.parent_game.houses[-1].area

        # am i in the right spot? if not where do i go?
        if check_in_area((self.center_x, self.center_y), self.area):  # in the correct area
            self.traveling = False
            if self.visiting:
                self.visiting_ticks += 1
                if self.visiting_ticks > self.visiting_time:
                    self.area = self.parent_house.area
                    self.visiting = False
                    self.visiting_ticks = 0
                    self.visiting_time = 0

            self.speed = PERSON_SPEED
            self.random_change()

        else:
            self.traveling = True
            self.speed = TRAVELING_SPEED
            self.go_to(self.area)

        # move it baby!
        if not self.center_x + self.change_x > 0 or not self.center_x + self.change_x < SCREEN_WIDTH:
            self.change_x = self.change_x * -1
        self.center_x += self.change_x
        if not self.center_y + self.change_y > 0 or not self.center_y + self.change_y < SCREEN_WIDTH:
            self.change_y = self.change_y * -1
        self.center_y += self.change_y

    def go_to(self, area: tuple):
        area_center = ((area[0][0] + area[1][0]) / 2, (area[0][1] + area[1][1]) / 2)

        delta_x = area_center[0] - self.center_x
        delta_y = area_center[1] - self.center_y

        mul = self.speed / calculate_distance((self.center_x, self.center_y), area_center)

        self.change_x = delta_x * mul
        self.change_y = delta_y * mul

    def random_change(self):
        self.change_x = random.randint(0, PERSON_SPEED) * random.choice([1, -1])
        self.change_y = math.sqrt(PERSON_SPEED ** 2 - self.change_x ** 2) * random.choice([1, -1])

    def infect(self):
        self.infected = True
        self.parent_game.infected_persons.append(self)
        self._set_color((255, 0, 0))
        self.parent_game.infected += 1

    def die(self):
        self.parent_game.living -= 1
        self.parent_game.infected -= 1
        self.parent_game.dead += 1
        self.parent_house.persons.remove(self)
        self.parent_game.infected_persons.remove(self)
        self.parent_game.sprites.remove(self)

    def recover(self):
        self.infected = False
        self.recovered = True
        self.parent_game.infected -= 1
        self.parent_game.recovered += 1
        self.parent_game.infected_persons.remove(self)
        self._set_color((0, 0, 255))

    def infectable(self):
        if self.recovered:
            self.recovered = False
            self.parent_game.recovered -= 1
        if self.infected:
            self.infected = False
            self.parent_game.infected -= 1
        
        self._set_color((255, 255, 255))


class House(arcade.Sprite):
    def __init__(self, width, center_x, center_y):
        super().__init__(
                    "house.png",
                    scale= 0.5,
                    image_width=100,
                    image_height=100,
                    center_x=center_x,
                    center_y=center_y
                )
        self.center_x = center_x
        self.center_y = center_y
        self.persons = []
        self.width = HOUSE_WIDTH
        self.height = HOUSE_WIDTH
        self.area = ((self.center_x-self.width/2, self.center_y-self.width/2), (self.center_x+self.width/2, self.center_y+self.width/2))


class Game(arcade.Window):
    def __init__(self):
        super().__init__(width=SCREEN_WIDTH, height=SCREEN_HEIGHT, title=SCREEN_TITLE)
        self.living = 0
        self.infected = 0
        self.dead = 0
        self.recovered = 0
        self.recovered_time_line = []
        self.infected_persons = []
        self.untouched_time_line = []
        self.houses = []
        self.infected_time_line = []
        self.dead_time_line = []
        self.tick = 0

        self.screen_parts = [[[] for i in range(SCREEN_HEIGHT // SCREEN_PART_WIDTH)] for i in range(SCREEN_WIDTH // SCREEN_PART_WIDTH)]

        self.sprites = arcade.sprite_list.SpriteList()

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
                self.sprites.append(self.houses[-1])

        for house in self.houses:
            if house == self.houses[-1]:
                break

            for i in range(random.randint(1, 6)):
                i += 1  # to get rid of the warning
                self.living += 1
                center_x = house.center_x + (random.randint(0, (HOUSE_WIDTH - PERSON_RADIUS) // 2) * random.choice([1, -1]))
                center_y = house.center_y + (random.randint(0, (HOUSE_WIDTH - PERSON_RADIUS) // 2) * random.choice([1, -1]))
                house.persons.append(
                    Person(
                        house,
                        center_x,
                        center_y,
                        self
                    )
                )
                self.sprites.append(house.persons[-1])

    def update_partialy(self, a, length):
        for house in self.houses[int(a):][:int(length)]:
            for person in house.persons:
                person.on_update()
    
    def on_update(self, delta_time):
        self.tick += 1
        self.infected_time_line.append(self.infected)
        self.dead_time_line.append(self.dead)
        self.recovered_time_line.append(self.recovered)
        self.untouched_time_line.append(self.living - self.recovered - self.infected)

        divide_num = 10
        if HOUSES < divide_num:
            divide_num = HOUSES

        batch_amount = HOUSES / divide_num

        for i in range(divide_num):
            #thread = threading.Thread(target=self.update_partialy, args=(i * batch_amount, batch_amount), daemon=True)
            #thread.start()

            self.update_partialy(i*batch_amount, batch_amount)

    def on_draw(self):
        arcade.start_render()

        self.sprites.draw()


    def on_key_press(self, key, mod):
        if key == arcade.key.I:
            # make someone infected
            while True:
                try:
                    person = self.houses[random.randint(0, len(self.houses)-1)].persons[0]
                    break
                except IndexError:
                    pass
            person.infect()
        
        if key == arcade.key.E:
            self.export()

        if key == arcade.key.Q:
            global VISITING_CHANCE
            if not VISITING_CHANCE:
                VISITING_CHANCE = DEFAULT_VISITING_CHANCE
            else:
                VISITING_CHANCE = 0

                for h in self.houses:
                    for p in h.persons:
                        p.visiting_time = 0
    
    def export(self):
        import sys
        try:
            json.dump(
                    {"infected": self.infected_time_line, "dead": self.dead_time_line, "recovered": self.recovered_time_line, "untouched": self.untouched_time_line},
                    open("export.json", 'w')
                )
        except:
            print(sys.exc_info())

def main():
    game = Game()
    arcade.run()


if __name__ == "__main__":
    main()
