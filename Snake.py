import pygame
import random
import sys
from time import sleep

WIDTH = 720
HEIGHT = 720
gameTitle = 'Snake - By MeZN'
fileName = 'map'

class Game():
    def __init__(self, screen, level, apple, snake):
        self.running = True
        self.clock = pygame.time.Clock()
        self.FPS = 20
        self.BG = (0, 0, 0)
        self.run(screen, level, apple, snake)

    def updateScreen(self, screen, level, apple, snake):
        screen.fill(self.BG)
        level.draw()
        apple.draw()
        snake.draw()
        pygame.display.flip()

    def checkForKeyPress(self, snake):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    snake.setUp()
                elif event.key == pygame.K_RIGHT:
                    snake.setRight()
                elif event.key == pygame.K_DOWN:
                    snake.setDown()
                elif event.key == pygame.K_LEFT:
                    snake.setLeft()

                break

    def run(self, screen, level, apple, snake):
        while self.running:
            self.clock.tick(self.FPS)
            self.checkForKeyPress(snake)
            snake.move()
            self.updateScreen(screen, level, apple, snake)

    def quit(self):
        pygame.quit()
        sys.exit()
        self.running = False      
        

class Snake():
    def __init__(self, screen, mapFile, apple):
        self.screen = screen
        self.xBlockSize, self.yBlockSize = mapFile.getBlockSize()
        self.xBlocks, self.yBlocks = mapFile.getNoOfBlocks()
        self.apple = apple
        self.wallCoordinates = mapFile.getWallCoordinates()

        self.appleCoordinate = self.apple.getCoordinate()
        self.snakeCoordinates = mapFile.getFirstSnakeCoordinates()
        self.SNAKE_COLOUR = (0, 255, 0)
        self.start = False

        self.setMovementAsFalse()

        if(self.snakeCoordinates == [()]):
            freeCoordinates = list( set(mapFile.getAllCoordinates()) - set(self.appleCoordinate) - set(self.wallCoordinates) )
            self.snakeCoordinates[0] = ( random.choice( tuple(freeCoordinates) ) )

    def draw(self):
        for snakePiece in self.snakeCoordinates:
            x, y = snakePiece
            xSnakeCoordinate = x * self.xBlockSize
            ySnakeCoordinate = y * self.yBlockSize
            pygame.draw.rect(self.screen, self.SNAKE_COLOUR, (xSnakeCoordinate, ySnakeCoordinate, self.xBlockSize, self.yBlockSize) )

    def setMovementAsFalse(self):
        self.up = self.right = self.down = self.left = False

    def setUp(self):
        if not self.down:
            self.setMovementAsFalse()
            self.up = True
            self.start = True

    def setRight(self):
        if not self.left:
            self.setMovementAsFalse()
            self.right = True
            self.start = True

    def setDown(self):
        if not self.up:
            self.setMovementAsFalse()
            self.down = True
            self.start = True

    def setLeft(self):
        if not self.right:
            self.setMovementAsFalse()
            self.left = True
            self.start = True

    def move(self):
        x, y = self.snakeCoordinates[0]

        if self.up:
            newCoordinates = (x, y-1)
            self.snakeCoordinates.insert( 0, self.checkIfOnWindowsEdge(newCoordinates) )
        elif self.right:
            newCoordinates = (x+1, y)
            self.snakeCoordinates.insert( 0, self.checkIfOnWindowsEdge(newCoordinates)  )
        elif self.down:
            newCoordinates = (x, y+1)
            self.snakeCoordinates.insert( 0, self.checkIfOnWindowsEdge(newCoordinates) )
        elif self.left:
            newCoordinates = (x-1, y)
            self.snakeCoordinates.insert( 0, self.checkIfOnWindowsEdge(newCoordinates) )

        if(self.start):
            self.checkForSelfCollision()
            self.checkForWallCollision()
            self.checkIfEaten()

    def checkIfOnWindowsEdge(self, coordinates):
        x, y = coordinates

        if x > (self.xBlocks-1):
            x = 0
        elif x < 0:
            x = self.xBlocks-1

        if y > (self.yBlocks-1):
            y = 0
        elif y < 0:
            y = self.yBlocks-1

        return (x, y)

    def checkForSelfCollision(self):
        for i in range(1, len(self.snakeCoordinates)):
            if self.snakeCoordinates[0] == self.snakeCoordinates[i]:
                self.quit()

    def checkForWallCollision(self):
        if self.snakeCoordinates[0] in self.wallCoordinates:
            self.quit()

    def checkIfEaten(self):
        self.appleCoordinate = self.apple.getCoordinate()

        if self.snakeCoordinates[0] == self.appleCoordinate:
            self.apple.eaten(self.snakeCoordinates, self.wallCoordinates)
        else:
            self.snakeCoordinates.pop()

    def quit(self):
        pygame.quit()
        sys.exit()
            
        

class Apple():
    def __init__(self, screen, mapFile):
        self.screen = screen
        self.xBlockSize, self.yBlockSize = mapFile.getBlockSize()
        self.allCoordinates = mapFile.getAllCoordinates()
        self.appleCoordinate = mapFile.getFirstAppleCoordinate()
        self.APPLE_COLOUR = (255, 0, 0)

        if(self.appleCoordinate == ()):
            self.eaten(mapFile.getFirstSnakeCoordinates(), mapFile.getWallCoordinates())
        else:
            self.draw()

    def eaten(self, snakeCoordinates, wallCoordinates):
        freeCoordinates = list( set(self.allCoordinates) - set(snakeCoordinates) - set(wallCoordinates) )
        self.appleCoordinate = random.choice( tuple(freeCoordinates) )
        self.draw()

    def draw(self):
        x, y = self.appleCoordinate
        xAppleCoordinate = x * self.xBlockSize
        yAppleCoordinate = y * self.yBlockSize
        pygame.draw.rect(self.screen, self.APPLE_COLOUR, (xAppleCoordinate, yAppleCoordinate, self.xBlockSize, self.yBlockSize) )

    def getCoordinate(self):
        return self.appleCoordinate     
        

class Level():
    def __init__(self, screen, mapFile):
        self.screen = screen
        self.xBlockSize, self.yBlockSize = mapFile.getBlockSize()
        self.wallCoordinates = mapFile.getWallCoordinates()
        self.WALL_COLOUR = (100, 100, 100)

    def draw(self):
        for wall in self.wallCoordinates:
            x, y = wall
            xWallCoordinate = x * self.xBlockSize
            yWallCoordinate = y * self.yBlockSize
            pygame.draw.rect(self.screen, self.WALL_COLOUR, (xWallCoordinate, yWallCoordinate, self.xBlockSize, self.yBlockSize) )


class ReadFile():
    def __init__(self, pathToMapFile):
        self.levelFile = open(pathToMapFile, 'r')
        self.fileLines = self.levelFile.readlines()
        self.levelFile.close()

        self.calcsForLevel()

    def calcsForLevel(self):
        self.xBlocks = 0
        self.yBlocks = len(self.fileLines)

        noOfLines = self.yBlocks
        for i in range(0, self.yBlocks):
            noOfCharacters = len(self.fileLines[i]) - 1         # 1 is subtracted as each line ends with an extra character( \n or EOF )
            if(noOfCharacters > self.xBlocks ):
                self.xBlocks = noOfCharacters

        global WIDTH
        global HEIGHT
        self.xBlockSize = WIDTH // self.xBlocks
        self.yBlockSize = HEIGHT // self.yBlocks

    def getNoOfBlocks(self):
        return (self.xBlocks, self.yBlocks)

    def getBlockSize(self):
        return (self.xBlockSize, self.yBlockSize)

    def getWallCoordinates(self):
        wallCoordinates = []

        for x in range(0, self.xBlocks):
            for y in range(0, self.yBlocks):
                try:
                    if(self.fileLines[y][x] == '#'):
                        wallCoordinates.append((x, y))
                except:
                    continue

        return wallCoordinates

    def getFirstSnakeCoordinates(self):
        snakeCoordinates = ()

        for x in range(0, self.xBlocks):
            for y in range(0, self.yBlocks):
                try:
                    if(self.fileLines[y][x] == 's'):
                        snakeCoordinates = (x, y)
                except:
                    continue

        try:
            return [snakeCoordinates]
        except:
            return []

    def getFirstAppleCoordinate(self):
        appleCoordinate = ()

        for x in range(0, self.xBlocks):
            for y in range(0, self.yBlocks):
                try:
                    if(self.fileLines[y][x] == 'a'):
                        appleCoordinate = (x, y)
                except:
                    continue

        return appleCoordinate

    def getAllCoordinates(self):
        allCoordinates = []
        for x in range(self.xBlocks):
            for y in range(self.yBlocks):
                allCoordinates.append((x, y))

        return allCoordinates


pygame.init()
screen = pygame.display.set_mode( (WIDTH, HEIGHT) )
pygame.display.set_caption(gameTitle)

mapFile = ReadFile(fileName)
level = Level(screen, mapFile)
apple = Apple(screen, mapFile)
snake = Snake(screen, mapFile, apple)

game = Game(screen, level, apple, snake)
