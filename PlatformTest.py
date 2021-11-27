import sys, pygame as pg
pg.init()

size = width, height = 1680, 1050
speed = [1, 1]

bgColor = 0, 40, 0
screen = pg.display.set_mode(size)
ball = pg.image.load("Intro_ball.gif")
ground = pg.image.load("ground.png")
ballrect = ball.get_rect()
groundrect= ground.get_rect()
groundPos= pg.Rect(500,850,871,191)
gravity=1



def checkLimits(ball,spd,grav):
    if ball.left < 0 or ball.right > width:
        spd[0] =  -spd[0]
    if ball.top < 0 or ball.bottom > height:
        spd[1] =  -spd[1]
        grav=grav*-1

while 1:
    for event in pg.event.get():
        if event.type == pg.QUIT: sys-exit()
    ballrect = ballrect.move(speed)
    
    checkLimits(ballrect,speed,gravity)
    if ballrect.colliderect(groundPos):
        speed[1] =  -speed[1]
        gravity=gravity*-1
    speed[1]+=0.2*gravity
    screen.fill(bgColor)
    screen.blit(ground,groundPos)
    screen.blit(ball,ballrect)

    pg.display.flip()