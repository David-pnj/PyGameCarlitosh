import sys, pygame as pg

pg.init()

class SnakePart():
    def __init__(self,rect):
        self.rect=rect
    def move_part(self,screen,position):
        self.rect=pg.Rect(position[0],position[1],30,30)
        pg.draw.rect(screen,(255,0,0),self.rect)
        

    
screen = pg.display.set_mode((720,720))
position = [200,50]
amount = 6
movementDict = {"w" : (0,-5),"a" : (-5,0),"s" : (0,5),"d" : (5,0)}
run = True

head= SnakePart(pg.Rect(position[0],position[1],30,30)) 
body= SnakePart(pg.Rect(position[0]-30,position[1],30,30))
body1= SnakePart(pg.Rect(position[0]-60,position[1],30,30))
body2= SnakePart(pg.Rect(position[0]-90,position[1],30,30))
tail= SnakePart(pg.Rect(position[0]-120,position[1],30,30))

prevPositions=[]

snake=[head,body,body1,body2,tail]
while run:
    
    for event in pg.event.get():
        if event.type == pg.QUIT: sys - exit()
        """Obtener Input"""
        if event.type == pg.KEYDOWN:
            try:
                key = chr(event.key)             
                if key in movementDict.keys():
                    position[0] += movementDict[key][0] * amount
                    position[1] += movementDict[key][1] * amount
                    prevPositions.clear();
                    prevPositions.append(position)
                    snakeAux=snake[:len(snake)] #todos los elementos menos el último
                    for part in snakeAux:
                        prevPositions.append([part.rect.left,part.rect.top])
            except ValueError:
                print('input no valido') #por ahora esto se queda como try catch para no dar error. hay que incluir soporte para las flechas, que no tienen chr
    """prevPositions es una lista que guarda la NUEVA posición a la que deberán moverse todas las partes, la cual es la que ocupaba la anterior antes excepto head, que tomará
    de nueva posición el input. Importante separar el obtener las posiciones del renderizado."""

    """Renderizado"""
    screen.fill((0,0,0))
    count = 0
    
    if len(prevPositions) > 0:
        for part in snake:
            part.move_part(screen,prevPositions[count])
            count+=1      
    else:
        for part in snake:
            pg.draw.rect(screen,(255,0,0),part.rect)

        
    pg.display.flip()