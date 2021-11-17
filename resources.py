from pyengine import*

desert = [Image('images/tiles/sand.png')]
swamp = [Image('images/tiles/swamp1.png'), Image('images/tiles/swamp2.png'), Image('images/tiles/swamp2.png')]
border = [Image('images/tiles/brick.png')]
winter = [Image('images/tiles/snow1.png'), Image('images/tiles/snow2.png')]

crate_img = Image('images/crate_24.png')
wall_img = Image('images/block_02.png')
water_img = Image('images/tiles/water.png')
stone_img = Image('images/stone.png')
broken_crate_img = Image('images/crate_32.png')
broken_stone_img = Image('images/stone_dead.png')

gear_img = Image('images/gear.png')
gear_blank_img = Image('images/gear_blank.png')
heart_img = Image('images/heart.png', size = (50, 50))
heart_blank_img = Image('images/heart_blank.png', size = (50, 50))

black_square = Image('images/black_square.png')
black_square_50 = Image('images/black_square.png')
black_square_50.set_alpha(50)
raindrop_img = Image('images/raindrop.png', size = (8, 16))
snowdrop_img = Image('images/snowdrop.png', size = (8, 4))
wind_sand_img = Image('images/wind_sand.png', size = (8, 4))
smoke_img = Image('images/tile_0008.png', size=(16, 16))

car_desert_img = Image('images/car/desert.png')
car_winter_img = Image('images/car/winter.png')
car_swamp_img = Image('images/car/swamp.png')
car_desert_winter_img = Image('images/car/desert-winter.png')
car_desert_swamp_img = Image('images/car/desert-swamp.png')
car_swamp_winter_img = Image('images/car/swamp-winter.png')
car_ultimate_img = Image('images/car/ultimate.png')

music = mixer.Channel(1)
paint_it_black = mixer.Sound('sounds/paint.mp3')
black_boot = mixer.Sound('sounds/black_boot.mp3')
broke_down = mixer.Sound('sounds/broke_down.mp3')

scene_car = Group()
ground = Group()
crates = Group()
tires = Group()
walls = Group()
water = Group()

wind = Group()
rain = Group()

