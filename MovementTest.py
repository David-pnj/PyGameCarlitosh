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
        if event.type == pg.KEYDOWN:
            try:
                key = chr(event.key)             
                if key in movementDict.keys():
                    position[0] += movementDict[key][0] * amount
                    position[1] += movementDict[key][1] * amount
                    prevPositions.clear();
                    for part in snake:
                        prevPositions.append([part.rect.left,part.rect.top])
            except ValueError:
                print('input no valido') #por ahora esto se queda como try catch para no dar error. hay que incluir soporte para las flechas, que no tienen chr

    screen.fill((0,0,0))
    """Creo que el problema radica en que estoy intentando actualizar las posiciones y sprites al mismo tiempo, cuando realmente deberían estar separados.
    Posibilidad: dejar este for para actualizar SOLO los sprites y antes de eso, en el TRY, hacer una función que actualice todas las posiciones. El comentario verde ahí
    dentro muestra como tomar la posición anterior"""
    count = 0
    if len(prevPositions) > 0:
        for part in snake:
            if head==part:
                part.move_part(screen,position)
            else:                               
                part.move_part(screen,prevPositions[count])
                count+=1      
    else:
        for part in snake:
            pg.draw.rect(screen,(255,0,0),part.rect)

        
    pg.display.flip()