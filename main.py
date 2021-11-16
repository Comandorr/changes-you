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
world_generated = []
scene_car = []
ground = []
crates = []
tires = []

wind = []
WIND = False
wind_rapid = 4 # number from 1 to 100
wind_speed = 15

rain = []
RAIN = False
rain_rapid = 5
rain_speed = 7

ENGINE = True

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
        scene_car.append(SimpleSprite('images/black_square_50.png', self.x, self.y+14))
        tires.append(scene_car[-1])
        scene_car.append(SimpleSprite('images/black_square_50.png', self.x, self.y+20))
        tires.append(scene_car[-1])

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
    world_generated.append(x*64)
    for y in range(win_h//64+1):
        scene_car.append(SimpleSprite('images/mapTile_017.png', x*64, y*64))
        ground.append(scene_car[-1])



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
            scene_car.remove(i)
            ground.remove(i)

    if ground[-1].x <= world_x + win_w/2:
        x = ground[-1].x
        for y in range(win_h//64+1):
            scene_car.append(SimpleSprite('images/mapTile_017.png', x+64, y*64))
            ground.append(scene_car[-1])  

    fill_window(black)
    for g in ground + tires:
        g.reset()
    car.animate()
    shadow.replace(car.x-3, car.y+10)
    shadow.reset()
    car.reset()
    if WIND:
        for y in range(0, win_h):
            if chance(wind_rapid, max = 1001):
                scene_car.append(WindDust(x = win_w, y = y))
    for w in wind:
        w.update()
        w.reset()
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
            scene_car.append(SimpleSprite('images/black_square_50.png', car.x, car.y+14))
            tires.append(scene_car[-1])
            scene_car.append(SimpleSprite('images/black_square_50.png', car.x, car.y+20))
            tires.append(scene_car[-1])
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
            if e.key == K_d:
                ENGINE = not ENGINE
                if ENGINE:
                    engine_start.play()

    fill_window(black)
    for i in ground.copy():
        i.reset()
        if i.x <= -64:
            scene_car.remove(i)
            ground.remove(i)
    for i in crates.copy():
        i.reset()
        if i.x <= -64:
            scene_car.remove(i)
            crates.remove(i)

    for i in tires.copy():
        i.reset()
        if i.x <= -64:
            scene_car.remove(i)
            tires.remove(i)

    if WIND:
        for y in range(0, win_h):
            if chance(wind_rapid, max = 1001):
                scene_car.append(WindDust(x = win_w, y = y))

    if RAIN:
        for x in range(0, int(win_w/2)):
            if chance(rain_rapid, max = 1001):
                scene_car.append(RainDrop(x*4, y = 0))

    if ground[-1].x <= win_w:
        x = ground[-1].x
        for y in range(win_h//64+1):
            scene_car.append(SimpleSprite('images/mapTile_017.png', x+64, y*64))
            ground.append(scene_car[-1])
            if chance(2):
                img = choice(['barrel_red_down.png', 'tanks_barrelGreen.png', 'tanks_barrelGrey.png', 'tanks_tankDesert_body1.png', 'tanks_tankDesert_body3.png'])
                scene_car.append(SimpleSprite('images/garbage/'+img, x+64, y*64))
                crates.append(scene_car[-1])
            if chance(2):
                img = choice(['01', '02', '03', '04', '05', '16', '18', '31', '32', '33'])
                scene_car.append(SimpleSprite('images/tiles/mapTile_0'+img+'.png', x+64, y*64))
                crates.append(scene_car[-1])
    
    car.update()
    shadow.replace(car.x-3, car.y+10)
    shadow.reset()
    car.reset()
    for c in crates:
        c.reset()
    for particle in wind+rain:
        particle.update()
        particle.reset()
        

    fps = SimpleText(str(int(clock.get_fps())), 24, 0, 0, background=white)
    fps.reset()
    display.update()
    clock.tick(60)