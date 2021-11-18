import sys, pygame as pg
pg.init()

size = width, height = 1680, 1050
speed = [1, 1]
speed2=list(map(lambda x: x*2,speed))
bgColor = 0, 40, 0
screen = pg.display.set_mode(size)
ball = pg.image.load("Intro_ball.gif")
ball2 = pg.image.load("Intro_ball.gif")
ballrect = ball.get_rect()
ball2rect = ball2.get_rect()

def checkLimits(ball,spd):
    if ball.left < 0 or ball.right > width:
        spd[0] =  -spd[0]
    if ball.top < 0 or ball.bottom > height:
        spd[1] =  -spd[1]

while 1:
    for event in pg.event.get():
        if event.type == pg.QUIT: sys-exit()
    ballrect = ballrect.move(speed)
    ball2rect = ball2rect.move(speed2)
    checkLimits(ballrect,speed)
    checkLimits(ball2rect,speed2)
    screen.fill(bgColor)
    screen.blit(ball,ballrect)
    screen.blit(ball2,ball2rect)
    pg.display.flip()



