from pyengine import*
from random import*
mixer.init()
music = mixer.Channel(1)
paint_it_black = mixer.Sound('sounds/paint.mp3')
black_boot = mixer.Sound('sounds/black_boot.mp3')
broke_down = mixer.Sound('sounds/broke_down.mp3')

create_window(1920, 1080)
#create_window(800, 600)
from pyengine import win_w, win_h, center_x, center_y, window
mouse.set_visible(False)
world_x = center_x
scene_car = Group()
ground = Group()
crates = Group()
tires = Group()
walls = Group()
water = Group()
walls_chance = 3
gears = 0
desert = ['images/tiles/sand.png']
swamp = ['images/tiles/swamp1.png', 'images/tiles/swamp2.png', 'images/tiles/swamp2.png']
border = ['images/tiles/brick.png']
winter = ['images/tiles/snow1.png', 'images/tiles/snow2.png']
locations = [desert, swamp, winter]
#shuffle(locations)
scene = locations[0]
n = 0

desert_upgrade = False
swamp_upgrade = False
winter_upgrade = False


gears = 0
lives = 3
fuel = 100

wind = Group()
WIND = False
wind_rapid = 2 # number from 1 to 100
wind_speed = 15

rain = Group()
RAIN = False
rain_rapid = 2
rain_speed = 7

ENGINE = True

if scene == swamp:
    RAIN = True
elif scene == winter or scene == desert:
    WIND = True


class SmokeParticle(SimpleSprite):
    def __init__(self, x, y, img = 'images/tile_0008.png'):
        super().__init__(img, x, y, size=(16, 16))
        self.add(wind, scene_car)

    def update(self):
        if self.image.get_alpha() > 0:
            self.image.set_alpha(self.image.get_alpha()-3)
            self.y -= 2
            self.x += 2
            self.image = transform.scale(self.image, (self.rect.width + 2, self.rect.height + 2))
            self.rect.width += 2
            self.rect.height += 2
            
            
class WindDust(SimpleSprite):
    def __init__(self, x, y, size = (8, 4)):
        if scene == winter:
            img = 'images/snowdrop.png'
        else:
            img = 'images/wind_sand.png'
        super().__init__(img, x, y, size)
        self.add(wind, scene_car)

    def update(self):
        self.x -= wind_speed
        if self.x <= 0:
            scene_car.remove(self)
            wind.remove(self)


class RainDrop(SimpleSprite):
    def __init__(self, x, y, size = (8, 16)):
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
        self.orig_speed = speed
        self.original = image.load(img).convert_alpha()
        self.frame = 0
        self.fps = 0
        self.aniframe = 10
        self.hitbox = Rect(self.rect.x, self.rect.y, self.rect.width, self.rect.height/2)
        self.kilometers = 0
        self.original_height = self.rect.height

    def animate(self):
        self.fps += 1
        if self.frame == 0 and self.fps >= self.aniframe:
            self.frame = 1
            self.image = transform.scale(self.original, (self.rect.width, self.original_height))
            self.y -= 1
            self.fps = 0
        elif self.frame == 1 and self.fps >= self.aniframe:
            self.frame = 0
            self.image = transform.scale(self.original, (self.rect.width, self.original_height - 1))
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
        self.kilometers += self.speed
        if chance(10):
            SmokeParticle(self.x - 16, self.rect.bottom - 16)
        

    def update(self):
        self.hitbox.x = self.rect.x
        self.hitbox.y = self.rect.y + self.rect.height/2
        self.aniframe = 10
        if ENGINE:
            keys = key.get_pressed()
            if keys[K_w]:
                self.up()
            if keys[K_s]:
                self.down()    
            self.right()
        self.animate()
        

def upgrade():
    if desert_upgrade and winter_upgrade and swamp_upgrade:
        car.image = image.load('images/car/ultimate.png').convert_alpha()
    elif desert_upgrade and swamp_upgrade:
        car.image = image.load('images/car/desert-swamp.png').convert_alpha()
    elif desert_upgrade and winter_upgrade:
        car.image = image.load('images/car/desert-winter.png').convert_alpha()
    elif winter_upgrade and swamp_upgrade:
        car.image = image.load('images/car/swamp-winter.png').convert_alpha()
    elif desert_upgrade:
        car.image = image.load('images/car/desert.png').convert_alpha()
    elif swamp_upgrade:
        car.image = image.load('images/car/swamp.png').convert_alpha()
    elif winter_upgrade:
        car.image = image.load('images/car/winter.png').convert_alpha()
    car.original = car.image
    

car = Car('images/car/car.png', center_x/2, center_y, size=(72, 24), speed = 7)
shadow = SimpleSprite('images/shadow.png', car.x, car.y, size = (72, 24))
for x in range(win_w//64+1):
    for y in range(win_h//64+1):
        SimpleSprite(choice(scene), x*64, y*64).add(scene_car, ground)

cutscene = True
run = True
car.x = -84
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
music.play(paint_it_black)                                     # включение музыки
music.queue(black_boot)
music.queue(broke_down)
start_time = time.get_ticks()
while cutscene:
    time_passed = time.get_ticks() - start_time
    for e in event.get():
        if e.type == QUIT:
            cutscene = False
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
            SimpleSprite(choice(scene), x+64, y*64).add(scene_car, ground)
            

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
    if RAIN:
        for x in range(0, int(win_w/4)):
            if chance(rain_rapid, max = 1001):
                RainDrop(x*8, y = 0).add(scene_car)

    wind.update()
    wind.reset()
    rain.update()
    rain.reset()
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


button_restart = SimpleText(' продолжить ', 48, center_x, center_y, color=white, background=black)
button_restart.position[0] = center_x - button_restart.rect.width/2
button_restart.position[1] = center_y - button_restart.rect.height/2
kilometers_text = SimpleText('км', 24, win_w-100, 0, background=gray)
location_text = SimpleText('Пустыня', 24, win_w-150, kilometers_text.rect.height, background=gray)
fuel_icon = SimpleSprite('images/fuel.png', win_w/3.2, win_h - 75)
fuel_bar = SimpleSprite('images/black_square.png', win_w/3, win_h - 50, size = (win_w/2, 20))
fuel_bar_shadow = SimpleSprite('images/black_square_50.png', win_w/3, win_h - 55, size = (win_w/3+5, 30))

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
                if button_restart.rect.collidepoint(mouse.get_pos()):
                    if lives > 0 and fuel > 1:
                        sprite.spritecollide(car, walls, True)
                        car.replace(center_x/2, center_y)
                        ENGINE = True
                        mouse.set_visible(False)
                    else:
                        run = False

    fill_window(black)
    for i in ground.sprites() + crates.sprites() + tires.sprites() + walls.sprites() + water.sprites():
        if i.x <= -64:
            i.kill()

    if WIND:                                            # ветер и снег
        for y in range(0, win_h):
            if chance(wind_rapid, max = 1001):
                WindDust(x = win_w, y = y).add(scene_car)
    if RAIN:                                            # дождь
        for x in range(0, int(win_w/4)):
            if chance(rain_rapid, max = 1001):
                RainDrop(x*8, y = 0).add(scene_car)

    if ground.sprites()[-1].x <= win_w:                 # спавн новых тайлов
        x = ground.sprites()[-1].x+64
        for y in range(win_h//64+1):
            SimpleSprite(choice(scene), x, y*64).add(scene_car, ground)
            if chance(1) and scene != border:
                SimpleSprite('images/crate_24.png', x, y*64).add(scene_car, crates)
            elif chance(walls_chance) and scene == desert:
                SimpleSprite('images/block_02.png', x, y*64).add(scene_car, walls)
            elif chance(20) and scene == swamp:
                SimpleSprite('images/tiles/water.png', x, y*64).add(scene_car, water)
            elif chance(5) and scene == winter:
                SimpleSprite('images/stone.png', x, y*64).add(scene_car, walls)
    
    for c in crates.sprites():                          # столкновение с ящиками
        if c.rect.colliderect(car.hitbox) and ENGINE:
            c.image = image.load('images/crate_32.png').convert_alpha()
            c.rect.width = 0
            c.rect.height = 0
            gears += 1
            fuel = fuel + 10
            if fuel > 100:
                fuel = 100
            if gears == 10:
                if scene == desert:
                    desert_upgrade = True
                elif scene == swamp:
                    swamp_upgrade = True
                elif scene == winter:
                    winter_upgrade = True
                upgrade()
                gears = 0
            
    for w in walls.sprites():                           # столкновение со стенами
        if w.rect.colliderect(car.hitbox) and ENGINE:
            if winter_upgrade and scene == winter:
                w.image = image.load('images/stone_dead.png').convert_alpha()
                w.rect.width = 0
                w.rect.height = 0
            else:    
                ENGINE = False
                time_dead = time.get_ticks()
                lives -= 1

    for w in water.sprites():                           # торможение об воду в болоте
        if w.rect.colliderect(car.hitbox) and ENGINE:
            if swamp_upgrade:
                car.speed *= 1.25
            else:
                car.speed *= 0.5

    if scene == desert and desert_upgrade:              # ускорение в пустыне
        car.speed *= 1.25

    if scene == winter and winter_upgrade:
        car.speed *= 0.75

    ground.reset()                                      # отрисовка графики
    crates.reset()
    crates.reset()
    tires.reset()
    
    shadow.replace(car.x-3, car.y+10)
    walls.reset()
    shadow.reset()
    water.reset()
    car.update()
    car.reset()
     
    wind.update()
    wind.reset()
    rain.update()
    rain.reset()
    
    car.speed = car.orig_speed

    if not ENGINE:                                      # кнопка рестарт
        if (time.get_ticks() - time_dead) > 1000:
            mouse.set_visible(True)
            if lives == 0 or fuel <= 1:
                button_restart.setText(' игра окончена ')
                button_restart.position[0] = center_x - button_restart.rect.width/2
            button_restart.reset()

    kilometers_text.setText(str(int(car.kilometers//10)) + ' м')
    kilometers_text.position[0] = win_w - kilometers_text.rect.width
    kilometers_text.reset()
    if scene == winter:
        location_text.setText('Тундра')
    elif scene == desert:
        location_text.setText('Пустыня')
    elif scene == swamp:
        location_text.setText('Болота')
    else:
        location_text.setText('')
    location_text.position[0] = win_w - location_text.rect.width
    location_text.reset()
    walls_chance = 3 + car.kilometers//10//1000
    
    fuel_icon.reset()                                       # работа с топливом
    fuel_bar.image = transform.scale(fuel_bar.image, (win_w/3 * fuel/100, 20))
    fuel_bar_shadow.reset()
    fuel_bar.reset()
    if ENGINE:
        fuel -= 0.1
        #pass
    if fuel <= 1 and ENGINE:
        ENGINE = False
        time_dead = time.get_ticks()

    for x in range(10):                                     # интерфейс
        SimpleSprite('images/gear_blank.png', center_x + win_w/6 + 50*x, 0).reset()
    for x in range(gears):
        SimpleSprite('images/gear.png', center_x + win_w/6 + 50*x, 0).reset()

    for x in range(3):
        SimpleSprite('images/heart_blank.png', center_x - 75 + 50*x, 0, size = (50, 50)).reset()
    for x in range(lives):
        SimpleSprite('images/heart.png', center_x -75 + 50*x, 0, size = (50, 50)).reset()
        

    


    display.update()
    clock.tick(60)