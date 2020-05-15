import os, sys, pygame, time, random
from pynput import keyboard
from pygame.locals import *

class Game:

    def __init__(self):
        self.field_width = 1200
        self.field_height = 600

        self.border_size = 30
        self.snake_element_size = 20

        self.grid_width = int( (self.field_width - 2*self.border_size ) / self.snake_element_size)
        self.grid_height = int( (self.field_height - 2*self.border_size ) / self.snake_element_size)

        self.snake = Snake(int(self.grid_width / 2), int(self.grid_height / 2))

        self.randomFruit()

        self.score = 0

        self.isGameOver = False

        self.pyGameStart()

        self.loadResourses()
        
        self.flagDirectionChange = False
        self.startListner()
        

    def pyGameStart(self):
        pygame.init()

        self.screen = pygame.display.set_mode((1200, 600))
        pygame.display.set_caption( "SNAKE" )
        
    def loadResourses(self):
        self.background_image = pygame.image.load( 'background.png' ).convert()
        self.snake_image = pygame.image.load( 'simplesnake.png' ).convert()
        self.fruit_image = pygame.image.load( 'simplefruit1.png' ).convert()
        self.tail_image = pygame.image.load ( 'simplefruit.png' ).convert()

    def onPress(self, key):
        try:
            k=key.char
        except:
            k=key.name
        if k in ['w', 'a', 's', 'd']:
            if k == 'w' and self.snake.direction != 'DOWN' and not self.flagDirectionChange:
                self.snake.direction = 'UP'
                self.flagDirectionChange = True
            if k == 'a' and self.snake.direction != 'RIGHT' and not self.flagDirectionChange:
                self.snake.direction = 'LEFT'
                self.flagDirectionChange = True
            if k == 's' and self.snake.direction != 'UP' and not self.flagDirectionChange:
                self.snake.direction = 'DOWN'
                self.flagDirectionChange = True
            if k == 'd' and self.snake.direction != 'LEFT' and not self.flagDirectionChange:
                self.snake.direction = 'RIGHT'
                self.flagDirectionChange = True

    def startListner(self):
        self.listener = keyboard.Listener(self.onPress)
        self.listener.start() 
    
    def clearScreen(self):
        #os.system("clear")  
        self.screen.blit ( self.background_image , ( 0, 0 ) )  

    def drawField(self):
        self.clearScreen()
        for grid_y in range(0, self.grid_height ):
            for grid_x in range(0, self.grid_width ):
                if grid_y == self.snake.getHeadPos()[1] and grid_x == self.snake.getHeadPos()[0]:
                    self.screen.blit( self.snake_image, (30 + 20*grid_x, 30 + 20*grid_y))
                elif self.snake.isPartOfTail(grid_x, grid_y):
                    self.screen.blit( self.tail_image, (30 + 20*grid_x, 30 + 20*grid_y))
                elif grid_y == self.fruit_y and grid_x == self.fruit_x:
                    self.screen.blit( self.fruit_image, (30 + 20*grid_x, 30 + 20*grid_y))
        self.screen.blit(self.generateTextSurface( 'SCORE: ' + str(self.score) , 30 ) ,(30,5))
        pygame.display.update()


    def randomFruit(self):
        self.fruit_x = random.randint(0, self.grid_width - 1)
        self.fruit_y = random.randint(0, self.grid_height - 1)     
    
    def isFruitOnHead(self):
        return self.fruit_x == self.snake.getHeadPos()[0] and self.fruit_y == self.snake.getHeadPos()[1]

    def isHeadInWall(self):
        return  self.snake.getHeadPos()[0] == -1 or self.snake.getHeadPos()[0]  == self.grid_width or self.snake.getHeadPos()[1] == -1 or self.snake.getHeadPos()[1] == self.grid_height

    def isHeadOnTail(self):
        return self.snake.isPartOfTail( self.snake.getHeadPos()[0], self.snake.getHeadPos()[1])

    def generateTextSurface(self, text, size):
        myfont = pygame.font.SysFont('Comic Sans MS', size)
        return myfont.render(text, False, (255, 255, 255))
    
    def update(self):
        self.snake.move()

        if self.isFruitOnHead():
            self.snake.addTail()
            self.score += 10
            self.randomFruit()
        
        if self.isHeadInWall() or self.isHeadOnTail(): 
            self.isGameOver = True

        self.flagDirectionChange = False

    def playGame(self):
        while not self.isGameOver:
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit()
            self.drawField()
            time.sleep(0.1)
            self.update()
        if self.isHeadOnTail():
            self.drawField()

        game_over_surface = self.generateTextSurface( 'GAME OVER' , 60 ) 
        score_surface = self.generateTextSurface( 'SCORE: ' + str(self.score) , 60 )
        game_over_position = ((self.field_width - game_over_surface.get_width() ) / 2, (self.field_height - 2*game_over_surface.get_height() ) / 2 )
        score_position = ((self.field_width - score_surface.get_width() ) / 2, self.field_height / 2 )

        self.screen.blit(game_over_surface , game_over_position )
        self.screen.blit(score_surface, score_position )
        pygame.display.update()

        while(True):
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit()


class SnakeElement:
    def __init__(self, element_x, element_y, isHead, number):
        self.element_x = element_x
        self.element_y = element_y

        self.isHead = isHead

        self.number = number
    
class Snake:
    def __init__(self, startx, starty):
        self.direction = 'NONE'

        self.snake_elements_list = []
        self.snake_elements_list.append(SnakeElement(startx, starty, True, 1))


    def getHeadPos(self):
        for snake_element in self.snake_elements_list:
            if snake_element.isHead:
                return [snake_element.element_x, snake_element.element_y]

    def move(self):
        if len( self.snake_elements_list ) == 1: # THIS IS HOW TO MOVE IF ONLY HEAD 
            if self.direction == 'UP':
                self.snake_elements_list[0].element_y -= 1
            if self.direction == 'DOWN':
                self.snake_elements_list[0].element_y += 1
            if self.direction == 'LEFT':
                self.snake_elements_list[0].element_x -= 1
            if self.direction == 'RIGHT':
                self.snake_elements_list[0].element_x += 1
        else:
            previous_head_index = -1
            for i in range(0, len(self.snake_elements_list)):
                if self.snake_elements_list[i].isHead == True:
                    previous_head_index = i

            for snake_element in self.snake_elements_list:
                if snake_element.number == len(self.snake_elements_list):
                    self.previous_tail_end = [ snake_element.element_x, snake_element.element_y ] 

            for snake_element in self.snake_elements_list:
                if snake_element.number == len(self.snake_elements_list):
                    if self.direction == 'UP':
                        snake_element.element_x = self.getHeadPos()[0]
                        snake_element.element_y = self.getHeadPos()[1] - 1
                    if self.direction == 'DOWN':
                        snake_element.element_x = self.getHeadPos()[0]
                        snake_element.element_y = self.getHeadPos()[1] + 1
                    if self.direction == 'LEFT':
                        snake_element.element_x = self.getHeadPos()[0] - 1
                        snake_element.element_y = self.getHeadPos()[1]
                    if self.direction == 'RIGHT':
                        snake_element.element_x = self.getHeadPos()[0] + 1
                        snake_element.element_y = self.getHeadPos()[1] 
                    snake_element.isHead = True
                    self.snake_elements_list[previous_head_index].isHead = False
                    
            for element in self.snake_elements_list:
                if element.isHead :
                    element.number = 1
                else:
                    element.number += 1


    def addTail(self):
        if len( self.snake_elements_list ) == 1: # THIS IS HOW TO ADD TAIL IF ONLY HEAD 
            if self.direction == 'UP':
                self.snake_elements_list.append(SnakeElement(self.snake_elements_list[0].element_x, self.snake_elements_list[0].element_y + 1, False, 2))
            if self.direction == 'DOWN':
                self.snake_elements_list.append(SnakeElement(self.snake_elements_list[0].element_x, self.snake_elements_list[0].element_y - 1, False, 2))
            if self.direction == 'LEFT':
                self.snake_elements_list.append(SnakeElement(self.snake_elements_list[0].element_x + 1, self.snake_elements_list[0].element_y, False, 2))
            if self.direction == 'RIGHT':
                self.snake_elements_list.append(SnakeElement(self.snake_elements_list[0].element_x - 1, self.snake_elements_list[0].element_y, False, 2))
        else:
            self.snake_elements_list.append( SnakeElement( self.previous_tail_end[0], self.previous_tail_end[1], False, len(self.snake_elements_list)+1))

    def isPartOfTail(self, x, y):
        for snake_element in self.snake_elements_list:
            if snake_element.element_x == x and snake_element.element_y == y and snake_element.isHead == False:
                return True
        return False


def main():
    game = Game()
    game.playGame()

if __name__ == "__main__":
    main()
