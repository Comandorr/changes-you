from pygame import*
from pyengine import*
from random import*

create_window(800, 600)
from pyengine import win_w, win_h, center_x, center_y
world_x = center_x
world_generated = []
scene_car = []
ground = []

wind = []
WIND = False
wind_rapid = 5 # number from 1 to 100
wind_speed = 10

rain = []
RAIN = False
rain_rapid = 5
rain_speed = 7


class WindDust(SimpleSprite):
    def __init__(self, x, y, size = (8, 4)):
        img = 'images/wind_sand.png'
        super().__init__(img, x, y, size)
        wind.append(self)

    def update(self):
        self.x -= wind_speed
        if self.x <= 0:
            scene_car.remove(self)
            wind.remove(self)


class RainDrop(SimpleSprite):
    def __init__(self, x, y, size = (4, 8)):
        img = 'images/raindrop.png'
        super().__init__(img, x, y, size)
        self.destination = randint(int(win_h/2), win_h)
        rain.append(self)

    def update(self):
        self.y += rain_speed
        if WIND:
            self.x -= wind_speed
        if self.y >= self.destination:
            scene_car.remove(self)
            rain.remove(self)



class Car(SimpleSprite):
    def __init__(self, img, x, y, speed = 1, size = None):
        super().__init__(img, x, y, size)
        self.speed = speed

    def up(self):
        self.y -= self.speed

    def down(self):
        self.y += self.speed

    def left(self):
        global world_x
        for i in scene_car:
            i.x += self.speed
        world_x -= self.speed

    def right(self):
        global world_x
        for i in scene_car:
            i.x -= self.speed
        world_x += self.speed

    def update(self):
        keyboard_control(self)


car = Car('images/rounded_red.png', center_x/2, center_y, size=(62, 24), speed = 3)
for x in range(win_w//64+1):
    world_generated.append(x*64)
    for y in range(win_h//64+1):
        scene_car.append(SimpleSprite('images/mapTile_022.png', x*64, y*64))
        ground.append(scene_car[-1])



run = True
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        if e.type == KEYDOWN:
            if e.key == K_1:
                WIND = not WIND
            if e.key == K_2:
                RAIN = not RAIN

    fill_window(black)
    for i in ground.copy():
        i.reset()
        if i.x <= -64:
            scene_car.remove(i)
            ground.remove(i)

    if WIND:
        for y in range(0, win_h):
            if chance(wind_rapid, max = 1001):
                scene_car.append(WindDust(x = win_w, y = y))

    if RAIN:
        for x in range(0, win_w*2):
            if chance(rain_rapid, max = 1001):
                scene_car.append(RainDrop(x, y = 0))

    if ground[-1].x <= world_x + win_w/2:
        x = ground[-1].x
        for y in range(win_h//64+1):
            scene_car.append(SimpleSprite('images/mapTile_022.png', x+64, y*64))
            ground.append(scene_car[-1])
    
    car.update()
    car.reset()
    for particle in wind+rain:
        particle.update()
        particle.reset()
        

    fps = SimpleText(str(int(clock.get_fps())), 24, 0, 0, background=white)
    fps.reset()
    display.update()
    clock.tick(60)