import sys, pygame as pg
import random
import time

from pygame.constants import K_LEFT, K_RIGHT, K_SPACE
pg.init()
pg.font.init()

size = width, height = 480, 720
vec = pg.math.Vector2 #vec nos permite crear variables de dos dimensiones para más tarde. Util para cosas como velocidad que tiene 2 valores. Posee x e y
bgColor = 0, 0, 0
screen = pg.display.set_mode(size)
ACC=0.75 #aceleración
FRIC=-0.12 #fricción para que el personaje tenga ímpetu
JUMPDIST = 15 #longitud de salto
FPS = 60
MAXPLATFORMS= 6
FramePerSec = pg.time.Clock()



displaysurface = pg.display.set_mode((width, height))
class Player(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf=pg.image.load("Intro_ball.gif")
        self.surf = pg.transform.scale(self.surf,(64,64)) #cambiar el tamaño
        self.rect = self.surf.get_rect() 
        self.flipImage=False
        self.pos=vec((100,360))
        self.vel=vec(0,0)
        self.acc=vec(0,0)
        self.jumping = False
        self.score = 0
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
        if hits and not self.jumping: # si estoy en una plataforma y NO estoy saltando
            self.jumping= True
            self.vel.y = -17
    
    def cancel_jump(self): #debido a que en PyGame podemos detectar cuando se suelta una tecla, podemos hacer un salto controlado donde "perdemos" momento
        if self.jumping:
            if self.vel.y < -3:
                self.vel.y = -3
 
    def update(self):
        hits = pg.sprite.spritecollide(self ,platforms, False) #devuelve el objeto con el que se ha colisionado. None en caso de no haber colisionado
        if self.vel.y > 0:        
            if hits:
                if self.pos.y < hits[0].rect.bottom: #este if se asegura de que solo se detenga en la plataforma cuando se "posa" sobre ella. sin el, una vez la bola toque la plataforma por abajo se teleporta
                    self.pos.y = hits[0].rect.top +1
                    self.vel.y = 0
                    self.jumping = False
                    self.pos.x+=hits[0].speed #hace que la bola se mueva junto a la plataforma cuando esté quieta
                    if hits[0].point == True:
                        hits[0].point = False
                        self.score +=1
            

class Platform(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf= pg.image.load("ground.png")
        self.surf = pg.transform.scale(self.surf,(180,32))
        self.rect = self.surf.get_rect(center = (random.randint(0,width-10),random.randint(0, height-30))) #crear plataforma en pos random, entre 0 (el top) y el máximo (con un margen)
        self.moving = True
        self.speed= random.randint(-1,1) #puede moverse a la izquierda, a la derecha o no moverse (el 0)
        self.point =  True #para asegurarse de que no se pueden "duplicar" puntos
    def move(self):
        if self.moving:
            self.rect.move_ip(self.speed,0)
            if self.speed > 0: #si toca un borde, que se transporte al otro lado
                if self.rect.left > width:
                    self.rect.right=0
                if self.rect.right < 0:
                    self.rect.left=width
                

player = Player()
ground = Platform()

ground.surf=pg.transform.scale(ground.surf,(360,64))
ground.rect = ground.surf.get_rect(center = (width/2,height-50))
ground.point= False

all_sprites= pg.sprite.Group()
all_sprites.add(player)
all_sprites.add(ground)

platforms= pg.sprite.Group()
platforms.add(ground)

#fuentes
goFont = pg.font.SysFont('Comic Sans MS', 30)
pointsFont = pg.font.SysFont('Verdana',20)
gameOverTextSurface = goFont.render("Game Over!",False,(255,255,255))


def check_plat_collision(platform,group):
    if pg.sprite.spritecollideany(platform,group): #función que nos permite ver si x sprite colisiona con alguno de los del grupo
        return True
    else:
        #return False valdría, pero sigue existiendo el problema de que quedan demasiado juntas. Para ello haremos:
        for pl in group:
            if pl ==  platform:
                continue
            if (abs(platform.rect.top - pl.rect.bottom) < 50) and (abs(platform.rect.bottom - pl.rect.top) < 50): #si se coloca en una distancia menor a 50, se cuenta como "mala" y retorna true
                return True
        C = False

def platform_generation():
    while len(platforms) < MAXPLATFORMS:
        pl = Platform()
        C = True
        while C: #solo sale del while si la plataforma no choca con alguna de las existentes
            pl= Platform()
            pl.rect.center = (random.randrange(0,width-10),random.randrange(0,50))
            C = check_plat_collision(pl,platforms)

        platforms.add(pl)
        all_sprites.add(pl)

count = random.randint(MAXPLATFORMS-2,MAXPLATFORMS-1)

while count > 0:
    C = True
    pl = Platform()
    while C:
        pl = Platform()
        C = check_plat_collision(pl,platforms)
    platforms.add(pl)
    all_sprites.add(pl)
    count-=1

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT: 
            pg.quit()
            sys-exit()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                player.jump()
        if event.type == pg.KEYUP:    
            if event.key == pg.K_SPACE:
                player.cancel_jump() 

    #check de si el jugador se ha caido de todo, game over.
    if player.rect.top > height:
        for spr in all_sprites:
            spr.kill()
            time.sleep(1)
            screen.fill((255,0,0))
            screen.blit(gameOverTextSurface,(width/2.5,height/2.5))
            pg.display.update()
            time.sleep(2)
            pg.quit()
            sys-exit()

    # esta parte permite el scroll vertical. Cada vez que lleguemos a un punto determinado, 
    if player.rect.top <= height / 3: # si pasa del pto determinado
        player.pos.y += abs(player.vel.y) #actualiza la pos del jugador
        for pl in platforms: #actualiza la pos de las plataformas (se quedan abajo ya que no se mueven, a diferencia del jugador)
            pl.rect.y += abs(player.vel.y)
            if pl.rect.top >= height:
                pl.kill() #quita las plataformas que desaparecen de la pantalla por abajo.

    player.update() #ejecuta la función UPDATE del jugador. ahora mismo solo gestiona las colisiones con plataformas.

    screen.fill(bgColor)

    platform_generation()

    screen.blit(pg.transform.flip(player.surf,player.flipImage,False),player.rect)
    
    for entity in all_sprites: #renderiza las entidades y muevelas
        screen.blit(entity.surf,entity.rect)
        entity.move()

    pointsText= pointsFont.render(str(player.score),True,(0,255,255)) #el render debe estar aqui pues va a cambiar constantemente no como el otro texto
    screen.blit(pointsText,(width/2,10))
    pg.display.flip()
    FramePerSec.tick(FPS)