from pygame import*
from pyengine import*
from random import*
mixer.init()
music = mixer.Channel(1)
paint_it_black = mixer.Sound('sounds/paint.mp3')
engine_start = mixer.Sound('sounds/engine_start.mp3')

create_window(1920, 1080)
from pyengine import win_w, win_h, center_x, center_y
mouse.set_visible(False)
world_x = center_x
scene_car = Group()
ground = Group()
crates = Group()
tires = Group()
walls = Group()

wind = Group()
WIND = False
wind_rapid = 4 # number from 1 to 100
wind_speed = 15

rain = Group()
RAIN = False
rain_rapid = 5
rain_speed = 7

ENGINE = True

class WindDust(SimpleSprite):
    def __init__(self, x, y, size = (8, 4)):
        img = 'images/wind_sand.png'
        super().__init__(img, x, y, size)
        self.add(wind, scene_car)

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
        self.add(rain, scene_car)

    def update(self):
        self.y += rain_speed
        if WIND:
            self.x -= wind_speed
        if self.y >= self.destination:
            self.kill()



class Car(SimpleSprite):
    def __init__(self, img, x, y, speed = 1, size = None):
        super().__init__(img, x, y, size)
        self.speed = speed
        self.original = image.load(img).convert_alpha()
        self.frame = 0
        self.fps = 0
        self.aniframe = 10

    def animate(self):
        self.fps += 1
        if self.frame == 0 and self.fps >= self.aniframe:
            self.frame = 1
            self.image = transform.scale(self.original, (62, 24))
            self.y -= 1
            self.fps = 0
        elif self.frame == 1 and self.fps >= self.aniframe:
            self.frame = 0
            self.image = transform.scale(self.original, (62, 23))
            self.y += 1
            self.fps = 0

    def up(self):
        self.y -= self.speed/2
        self.aniframe = 5

    def down(self):
        self.y += self.speed/2
        self.aniframe = 5

    def right(self):
        global world_x
        for i in scene_car:
            i.x -= self.speed
        world_x += self.speed
        self.aniframe = 5
        SimpleSprite('images/black_square_50.png', self.x, self.y+14).add(scene_car, tires)
        SimpleSprite('images/black_square_50.png', self.x, self.y+20).add(scene_car, tires)
        

    def update(self):
        self.aniframe = 10
        if ENGINE:
            keys = key.get_pressed()
            if keys[K_w]:
                self.up()
            if keys[K_s]:
                self.down()    
            self.right()
        self.animate()
        


car = Car('images/rounded_red.png', center_x/2, center_y, size=(62, 24), speed = 5)
shadow = SimpleSprite('images/shadow.png', car.x, car.y, size = (62, 24))
for x in range(win_w//64+1):
    for y in range(win_h//64+1):
        SimpleSprite('images/mapTile_017.png', x*64, y*64).add(scene_car, ground)


cutscene = True
WIND = True
car.x = -64
R0 = SimpleSprite('images/black_square.png', 0, 0, (win_w, win_h))
R1 = SimpleSprite('images/black_square.png', 0, 0, (win_w, win_h/5))
R2 = SimpleSprite('images/black_square.png', 0, win_h*0.8, (win_w, win_h/5))
text_up = SimpleText('год 2052', 64, win_w/2, win_h*0.1, color = white)
text_up.position[0] = win_w/2 - text_up.rect.width/2
text_down = SimpleText('ты последний выживший', 64, win_w/2, win_h*0.9, color = white)
text_down.position[0] = win_w/2 - text_down.rect.width/2
text_center = SimpleText('CHANGES', 100, win_w/2, win_h/2)
text_center.position[0] = win_w/2 - text_down.rect.width/1.7
text_center.position[1] = win_h/2 - text_down.rect.height/2
music.play(paint_it_black)
start_time = time.get_ticks()
while cutscene:
    time_passed = time.get_ticks() - start_time
    for e in event.get():
        if e.type == QUIT:
            run = False
        if e.type == KEYDOWN:
            if e.key == K_ESCAPE or e.key == K_SPACE:
                cutscene = False
                car.replace(center_x/2, center_y)

    for i in ground.copy():
        i.reset()
        if i.x <= -64:
            i.kill()
            
    if ground.sprites()[-1].x <= world_x + win_w/2:
        x = ground.sprites()[-1].x
        for y in range(win_h//64+1):
            SimpleSprite('images/mapTile_017.png', x+64, y*64).add(scene_car, ground)
            

    fill_window(black)
    ground.reset()
    tires.reset()
    car.animate()
    shadow.replace(car.x-3, car.y+10)
    shadow.reset()
    car.reset()
    if WIND:
        for y in range(0, win_h):
            if chance(wind_rapid, max = 1001):
                WindDust(x = win_w, y = y).add(scene_car)
    wind.update()
    wind.reset()
    R0.reset()
    if R0.image.get_alpha() > 0:
        R0.image.set_alpha(R0.image.get_alpha()-1)
    R1.reset()
    R2.reset()
    if time_passed > 3500:
        text_up.reset()
    if time_passed > 5400:
        text_down.reset()
    if time_passed > 7500:
        text_up.position[1] -= 3
        text_down.position[1] += 3
    if time_passed > 11550:
        text_center.reset()
    if time_passed > 8500:
        if car.x < center_x/4:
            car.x += 5
            SimpleSprite('images/black_square_50.png', car.x, car.y+14).add(scene_car, tires)
            SimpleSprite('images/black_square_50.png', car.x, car.y+20).add(scene_car, tires)
        else:
            car.right()
    if time_passed > 12500:
        if R1.y > -win_h/4:
            R1.y -= 2
            R2.y += 2
        if text_center.image.get_alpha() > 0:
            text_center.image.set_alpha(text_center.image.get_alpha()-3)
        else:
            if car.x < center_x/2:
                car.x += 5
            else:
                car.right()
    if time_passed > 18000:
        cutscene = False
    display.update()
    clock.tick(60)


button_restart = SimpleText(' начать заново ', 48, center_x, center_y, color=white, background=black)
button_restart.position[0] = center_x - button_restart.rect.width/2
button_restart.position[1] = center_y - button_restart.rect.height/2
car.speed = 7
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
        if e.type == MOUSEBUTTONDOWN:
            if not ENGINE:
                print(mouse.get_pos())
                if button_restart.rect.collidepoint(mouse.get_pos()):
                    sprite.spritecollide(car, walls, True)
                    car.replace(center_x/2, center_y)
                    ENGINE = True
                    mouse.set_visible(False)


    fill_window(black)
    for i in ground.sprites() + crates.sprites() + tires.sprites():
        if i.x <= -64:
            i.kill()

    if WIND:
        for y in range(0, win_h):
            if chance(wind_rapid, max = 1001):
                WindDust(x = win_w, y = y).add(scene_car)

    if RAIN:
        for x in range(0, int(win_w/2)):
            if chance(rain_rapid, max = 1001):
                RainDrop(x*4, y = 0).add(scene_car)

    if ground.sprites()[-1].x <= win_w:
        x = ground.sprites()[-1].x+64
        for y in range(win_h//64+1):
            SimpleSprite('images/mapTile_017.png', x, y*64).add(scene_car, ground)
            if chance(1):
                SimpleSprite('images/crate_22.png', x, y*64).add(scene_car, crates)
            if chance(3):
                SimpleSprite('images/block_02.png', x, y*64).add(scene_car, walls)
    
    ground.reset()
    crates.reset()
    tires.reset()
    crates.reset()
    walls.reset()

    car.reset()
    car.update()
    shadow.replace(car.x-3, car.y+10)
    shadow.reset()

    wind.update()
    wind.reset()
    rain.update()
    rain.reset()

    for c in sprite.spritecollide(car, crates, False):
        c.image = image.load('images/crate_32.png')
        
    if sprite.spritecollide(car, walls, False) and ENGINE:
        ENGINE = False
        time_dead = time.get_ticks()

    if not ENGINE:
        if (time.get_ticks() - time_dead) > 1000:
            mouse.set_visible(True)
            button_restart.reset()

    fps = SimpleText(str(int(clock.get_fps())), 24, 0, 0, background=white)
    fps.reset()
    display.update()
    clock.tick(60)