import sys, pygame as pg

from pygame.constants import K_LEFT, K_RIGHT, K_SPACE
pg.init()

size = width, height = 720, 720
vec = pg.math.Vector2 #vec nos permite crear variables de dos dimensiones para más tarde. Util para cosas como velocidad que tiene 2 valores. Posee x e y
bgColor = 0, 0, 0
screen = pg.display.set_mode(size)
ACC=0.75 #aceleración
FRIC=-0.12 #fricción para que el personaje tenga ímpetu
JUMPDIST = 15 #longitud de salto
FPS = 60
FramePerSec = pg.time.Clock()

displaysurface = pg.display.set_mode((width, height))
class Player(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf=pg.image.load("Intro_ball.gif")
        self.rect = self.surf.get_rect() 
        self.flipImage=False
        self.pos=vec((100,360))
        self.vel=vec(0,0)
        self.acc=vec(0,0)

    def move(self):
        self.acc=vec(0,0.5) #el 0.5 añade gravedad constante
        keys=pg.key.get_pressed() #teclas pulsadas. Contiene todas las teclas de PyGame y por cada una un valor booleano. True si se ha pulsado, False si no

        #obtener aceleración y/o saltar
        if keys[K_LEFT]:
            self.acc.x= -ACC
            self.flipImage=False
        if keys[K_RIGHT]:
            self.acc.x = ACC
            self.flipImage=True
       
        #moverse
        self.acc.x += self.vel.x * FRIC #esto es lo que permite que el personaje vaya perdiendo movimiento con el tiempo si no se pulsa
        self.vel += self.acc #añadir aceleramiento a la vel
        self.pos += self.vel + 0.5 * self.acc #ecuación de aceleración. 

        if self.pos.x > width:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = width

        #update
        self.rect.midbottom=self.pos
    
    def jump(self):
        hits = pg.sprite.spritecollide(self, platforms, False)
        if hits:
           self.vel.y = -15
 
 
    def update(self):
        hits = pg.sprite.spritecollide(player ,platforms, False)
        if player.vel.y > 0:        
            if hits:
                self.vel.y = 0
                self.pos.y = hits[0].rect.top + 1
            

class Platform(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf= pg.image.load("ground.png")
        self.rect = self.surf.get_rect(center = (width/2, height - 10))
        

player = Player()
ground = Platform()

all_sprites= pg.sprite.Group()
all_sprites.add(player)
all_sprites.add(ground)

platforms= pg.sprite.Group()
platforms.add(ground)

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT: 
            pg.quit()
            sys-exit()

        if event.type == pg.KEYDOWN:    
            if event.key == pg.K_SPACE:
                player.jump()

    player.update() #ejecuta la función UPDATE del jugador. ahora mismo solo gestiona las colisiones con plataformas.

    screen.fill(bgColor)

    player.move()
    screen.blit(pg.transform.flip(player.surf,player.flipImage,False),player.rect)
    for spr in platforms:
        screen.blit(spr.surf,spr.rect)

    pg.display.flip()
    FramePerSec.tick(FPS)