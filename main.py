from pygame import*
from pyengine import*
from random import*

create_window(800, 600)
from pyengine import win_w, win_h, center_x, center_y
world_x = center_x
world_generated = []
scene_car = []
ground = []

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
while run_game(run):
    fill_window(black)
    for i in scene_car.copy():
        i.reset()
        if i.x <= -64:
            scene_car.remove(i)

    car.update()
    car.reset()

    if ground[-1].x <= world_x + win_w/2:
        x = ground[-1].x
        for y in range(win_h//64+1):
            scene_car.append(SimpleSprite('images/mapTile_022.png', x+64, y*64))
            ground.append(scene_car[-1])
    

    fps = SimpleText(str(int(clock.get_fps())), 24, 0, 0, background=white)
    fps.reset()
    display.update()
    clock.tick(60)