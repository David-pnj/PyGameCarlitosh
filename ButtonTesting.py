import sys, pygame as pg
pg.init()

size = width, height = 1680, 1050

BLACK=(0,0,0)
WHITE = (255,255,255)
bgColor = 0, 40, 0
screen = pg.display.set_mode(size)

myFont= pg.font.SysFont('Arial',35)
text1= myFont.render('Quit',False,WHITE)
rect1= pg.Rect(300,300,205,80)

text2= myFont.render('Start',False,WHITE)
rect2= pg.Rect(600,300,205,80)

def func1():
    sys.exit()
def func2():
    print('Start')

buttons=[[text1,rect1,BLACK,func1],[text2,rect2,BLACK,func2]] #funciona y todo muy guay, pero esto debe transformarse en unas clases. Buscar como implementar una clase button en pygame
run = True
while run:
    mousePos=pg.mouse.get_pos()
    for event in pg.event.get():
        if event.type == pg.QUIT: sys-exit()
        if event.type == pg.MOUSEBUTTONDOWN:
            for button in buttons:
                if button[1].collidepoint(mousePos):
                    button[3]()
            
    
    screen.fill(bgColor)
    for text,rect,color,fun in buttons:
        pg.draw.rect(screen,color,rect)
        screen.blit(text,rect.center)
    
    pg.display.flip()


