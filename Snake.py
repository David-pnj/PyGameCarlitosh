import sys,random, pygame as pg

pg.init()

"""TO DO: Consumable que aumenta la puntuación de los azules, tener varios azules (opcional) y sonidos para la serpiente y consumables"""

class Entity():
    def __init__(self,rect) -> None:
        self.rect=rect
    def move_entity(self,screen,position,color):
        self.rect=pg.Rect(position[0],position[1],25,25)
        pg.draw.rect(screen,color,self.rect)

class Consumable(Entity):
    def __init__(self,rect,points):
        self.rect=rect
        self.points=points
    

class SnakePart(Entity):
    def __init__(self,rect):
        super().__init__(rect)

class Wall(Entity):
    def __init__(self,rect):
        super().__init__(rect)

RED = (255, 0, 0)
GREY = (128, 128, 128)
BLUE = (0, 0, 255)
screen = pg.display.set_mode((720,720))
position = [200,50]
amount = 5
movementDict = {"w" : (0,-5),"a" : (-5,0),"s" : (0,5),"d" : (5,0)}
run = True

head= SnakePart(pg.Rect(position[0],position[1],25,25)) 
body= SnakePart(pg.Rect(position[0]-25,position[1],25,25))
body1= SnakePart(pg.Rect(position[0]-50,position[1],25,25))
body2= SnakePart(pg.Rect(position[0]-75,position[1],25,25))
tail= SnakePart(pg.Rect(position[0]-100,position[1],25,25))

consum1Position=[225,100]
consum1=Consumable(pg.Rect(consum1Position[0],consum1Position[1],25,25),1)
"""Añadir un consumable verde que suba el valor del consumable azul por 2"""

wall1=Wall(pg.Rect(0,0,25,25))

prevPositions=[]

snake=[head,body,body1,body2,tail]
canMove=False
def calculate_pos_consum():
    x=random.randint(-15,15)*25
    y=random.randint(-15,15)*25
    """se sale algunas veces y por consecuencia aparece demasiado en el borde. Probar las tecnicas de try catch que vienen en las diapos de clase a ver si es mejor."""
    if x < 0:
        x= 0
    if x > 720: 
        x= 720
    if y < 0:
        y = 0
    if y > 720:
        y = 720
    return [x,y]
while run:
    for event in pg.event.get():
        if event.type == pg.QUIT: sys - exit()
        """Obtener Input"""
        if event.type == pg.KEYDOWN:
            try:
                key = chr(event.key)                            
                if key in movementDict.keys():
                    position[0] = head.rect.left + movementDict[key][0] * amount
                    position[1] = head.rect.top + movementDict[key][1] * amount                    
                    canMove=True
                    prevPositions.clear()            
                    prevPositions.append(position)
                    testRect=pg.Rect(position[0],position[1],25,25)
                    """Si toca un consumable, añade 1 pieza a la serpiente. Cambiarlo para que la cantidad de piezas añadidas dependa del atributo points de la clase Consumable"""
                    if testRect.colliderect(consum1.rect):                      
                        newPart= SnakePart(pg.Rect(body.rect.left,body.rect.top,25,25))
                        snake.append(newPart)
                        consum1Position=calculate_pos_consum()
                        print(consum1Position)
                        
                            
                    snakeAux=snake[:len(snake)] #todos los elementos menos el último
                    for part in snakeAux:
                        """Malo de narices pero no he encontrado forma de chequear si puede hacer un solo heck de 'si hay un objeto x en esta posicion', tengo que hacerlo en un for
                        y ya que está este aquí obligatorio, al menos aprovecho este en vez de crear otro."""
                        if testRect.colliderect(part.rect): 
                            canMove=False     
                            break
                        prevPositions.append([part.rect.left,part.rect.top])
                    
            except ValueError:
                print('input no valido') #por ahora esto se queda como try catch para no dar error. hay que incluir soporte para las flechas, que no tienen chr
    """prevPositions es una lista que guarda la NUEVA posición a la que deberán moverse todas las partes, la cual es la que ocupaba la anterior antes excepto head, que tomará
    de nueva posición el input. Importante separar el obtener las posiciones del renderizado."""

    """Renderizado"""
    screen.fill((0,0,0))
    count = 0
    consum1.move_entity(screen,consum1Position,BLUE)
    if canMove:        
        for part in snake:
            part.move_entity(screen,prevPositions[count],RED)
            count+=1                   
    else:
        for part in snake:
            pg.draw.rect(screen, RED ,part.rect)
        
    pg.draw.rect(screen,GREY,wall1.rect)
    pg.display.flip()
