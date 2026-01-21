from pygame import *
from random import *
from time import time as tm
mixer.init() #пробуждаем возможности модуля миксер (работа со звуком)
mixer.music.load('space.ogg') #подключаем музыку
mixer.music.play() #проигрываем его
mixer.music.set_volume(0.5) #меняем громкость музыки

sound_fire = mixer.Sound('fire.ogg') #звуковые эффекты

font.init()
font1 = font.SysFont('Areal', 70)
win = font1.render('Победа!', True, (255, 215, 0))
lose = font1.render('Поражение!', True, (255, 0, 0))

font2 = font.SysFont('Areal', 25)


propusheni = 0
ubiti = 0



window = display.set_mode((700, 500)) #создал экран 700х500
display.set_caption('Шутер') #заголовок игры
background = transform.scale(image.load('ghetto.jpg'), (700, 500)) #загружаю картунку и скейлю ее под нужные размеры

clock = time.Clock() #создали игровой таймер
FPS = 60


class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, w, h):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (w, h))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    
    def reset(self): #отрисовать 
        window.blit(self.image, (self.rect.x, self.rect.y))



class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_d] and self.rect.x < 620:
            self.rect.x += self.speed

        if keys_pressed[K_a] and self.rect.x > 0:
            self.rect.x -= self.speed
    
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, -15, 20, 15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        global propusheni
        self.rect.y += self.speed
        if self.rect.y >= 500:
            self.rect.y = -50
            self.rect.x = randint(0, 600)
            propusheni += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y <= 0:
            self.kill()

class Dog(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y >= 500:
            self.rect.y = -50
            self.rect.x = randint(0, 600)
 

player = Player('michael.png', 330, 375, 6, 80, 130)
dogs = sprite.Group()
for i in range(3):
    dog = Dog('doberman.png', randint(0, 600), -50, randint(1, 3), 80, 90)
    dogs.add(dog)

#создали группу
bullets = sprite.Group()
bandits = sprite.Group()
for i in range(5): #создаем 5 экземпляров
    bandit = Enemy('bandit.png', randint(0, 600), -50, randint(1, 3), 100, 110)
    bandits.add(bandit) #добавляем их в группу

num_fire = 0
rel_time = False


finish = False
game = True

while game:
    for e in event.get(): #для каждого события совершаемого пользователем в списке всех событий
        if e.type == QUIT: #если тип -  события нажатый крестик
            game = False #переменная-флаг = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                if rel_time == False and num_fire <= 5:
                    player.fire()
                    sound_fire.play()
                    num_fire += 1
                if num_fire > 5 and rel_time == False:
                    rel_time = True
                    start_time = tm()
    if finish != True:
        
        window.blit(background, (0, 0)) #отрисовывает на экране фоновую картинку в координатах 0, 0
        player.update()
        player.reset()

        bandits.update()
        bandits.draw(window)

        bullets.update()
        bullets.draw(window)

        dogs.update()
        dogs.draw(window)

        kills = font2.render('Убиты:' + str(ubiti), True, (255, 255, 0))
        losts = font2.render('Пропущены: ' + str(propusheni), True, (255, 255, 0))
    
        window.blit(losts, (0, 5)) #отрисовываем надпись "пропущены" на экране
        window.blit(kills, (0, 25))

        if rel_time == True:
            new_time = tm( )
            if new_time - start_time < 3:
                reloading = font2.render('Перезарядка....', True, (255, 255, 0))
                window.blit(reloading, (275, 350))
            else:
                num_fire = 0
                rel_time = False
        
        sprites_list = sprite.groupcollide(bandits, bullets, True, True)
        for i in sprites_list:
            ubiti += 1
            bandit = Enemy('bandit.png', randint(0, 600), -50, randint(1, 3), 100, 110)
            bandits.add(bandit) #добавляем их в группу

        if ubiti > 10:
            window.blit(win, (200, 200))
            finish = True
            mixer.music.stop()

        if propusheni >= 3 or sprite.spritecollide(player, bandits, False) or sprite.spritecollide(player, dogs, False):
            window.blit(lose, (200, 200)) #значения в фиолетовых скобка это координаты надписи
            finish = True
            mixer.music.stop()


     
     
    
    clock.tick(FPS) #фпс
    display.update() #на каждом шаге цикла while все отрисовывает заново