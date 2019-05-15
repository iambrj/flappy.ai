import pygame
import time
from random import randint, randrange


# Colors
black = (0, 0, 0)
textcolor1 = (255, 32, 23)
textcolor2 = (235, 32, 55)
textcolorBlock = (0, 0, 235)
sunset = (255, 0, 0)
green = (100, 255, 100)
darkgreen = (6, 127, 2)
brightblue = (47, 228, 253)
orange = (255, 113, 0)
yellow = (255, 236, 0)
purple = (252, 67, 255)


pygame.init ()


# Global variables
surfaceWidth = 800
surfaceHeight = 500
surface = pygame.display.set_mode ((surfaceWidth, surfaceHeight))
pygame.display.set_caption ("flappy.ai")
clock = pygame.time.Clock ()
BIRD_COUNT = 10


# Use a image with transparent background
background = pygame.image.load("../assets/background1.jpg")


class Bird:
    """
    x, y represent bird's position relative to top-left corner and y_move represents amount by which the bird should move
    """
    # TODO: add member variable AST
    # TODO: add random AST generator for member variable
    # TODO: add AST evaluator
    def __init__(self, xval, yval, y_moveval, scoreval, no):
        self.y_move = y_moveval
        self.x = xval
        self.y = yval
        self.number = no
        self.current_score = scoreval
        self.img = pygame.image.load ("../assets/bird.png")
        self.imageWidth = self.img.get_width ()
        self.imageHeight = self.img.get_height ()


# Restart/quit the game
def replay_or_quit():
    for event in pygame.event.get ([pygame.KEYDOWN, pygame.KEYUP, pygame.QUIT]):
        if event.type == pygame.QUIT:
            pygame.quit ()
            quit ()

        elif event.type == pygame.KEYDOWN:
            continue

        return event.key

    return None


# Display stats
def score(count, number):

    smallText = pygame.font.Font ("freesansbold.ttf", 20)

    score = "Score: " + str(count) + " Bird: " + str(number)
    titleTextSurface, titleTextRectangle = makeTextObjs (score, smallText, sunset)
    titleTextRectangle.center = surfaceWidth / 2, 20
    # Put text on screen
    surface.blit (titleTextSurface, titleTextRectangle)


# Drawing obstacles(blocks)
def blocks(x_block, y_block, blockWidth, blockHeight, gap,color):

    # Pipe body
    pygame.draw.rect (surface, color, [x_block, y_block, blockWidth, blockHeight])
    pygame.draw.rect (surface, color,[x_block, y_block + blockHeight + gap, blockWidth, surfaceHeight - gap - blockHeight])
    # Pipe ends
    pygame.draw.rect (surface, darkgreen, [x_block - 5, blockHeight - 10, blockWidth + 10, 30])
    pygame.draw.rect (surface, darkgreen, [x_block - 5, y_block + blockHeight + gap, blockWidth + 10, 30])


# Small function to render text
def makeTextObjs(text, font, color):
    textSurface = font.render (text, True, color)
    return textSurface, textSurface.get_rect ()


# This function is used to display messages on screen
def msgsurface(text):
    smallText = pygame.font.Font ("freesansbold.ttf", 20)
    largeText = pygame.font.Font ("freesansbold.ttf", 50)

    titleTextSurface, titleTextRectangle = makeTextObjs (text, largeText, textcolor1)
    titleTextRectangle.center = surfaceWidth / 2, surfaceHeight / 2
    surface.blit (titleTextSurface, titleTextRectangle)

    smallTextSurface, smallTextRectangle = makeTextObjs ("Press any key to continue", smallText, textcolor2)
    # Adjust height for small text
    smallTextRectangle.center = surfaceWidth / 2, ((surfaceHeight / 2) + 100)

    surface.blit (smallTextSurface, smallTextRectangle)

    # updating the screen to make text appear
    pygame.display.update ()
    time.sleep (1)

    while replay_or_quit () == None:
        clock.tick ()
    main ()


# Gameover function
def gameOver(finalscore):
    # TODO: show stats 
    msgsurface("Game Over")


# Initial screen
def gameStart():
    # This function displays the message on the screen
    msgsurface ("Hold up arrow to move upwards")


# x and y are co-ordinates measured from top left
def image(x, y, img):
    surface.blit (img, (x, y))


def main():
    # x_block and y_block determine the positions of block
    x_block = surfaceWidth
    y_block = 0
    blockWidth = 80

    # Block  height is randomed between 100 and  around half of surface height
    blockHeight1 = randint (100, int (surfaceHeight / 1.5) - 100)

    # Initialize array of Bird objects
    birds = []
    for i in range(1, BIRD_COUNT + 1):
        birds.append(Bird(200, 150, 0, 0, i))

    # Gap is the distance between blocks
    gap = int(birds[0].imageHeight * 4)

    # Movement speed of block
    block_move = 4

    game_over = False

    while True:
        for b in birds:
            game_over = False
            scoreVal = 0
            while not game_over:
                # Responding to events such as key up and quit button
                for event in pygame.event.get ():
                    if event.type == pygame.QUIT:
                        game_over = True

                    # TODO: Implemet genetic programming here
                    # Setting key controls
                    # if up key is pressed move up 4 positions vertically
                    if event.type == pygame.KEYDOWN:
                         if event.key == pygame.K_UP:
                             b.y_move = -4
                    # if up key is released move down 4 positions vertically
                    if event.type == pygame.KEYUP:
                         if event.key == pygame.K_UP:
                             b.y_move = 4
                # Update position accordingly
                b.y += b.y_move

                image(0,0,background)
                image(b.x, b.y,b.img)
                blocks(x_block, y_block, blockWidth, blockHeight1, gap,green)

                # Move block towards bird
                x_block -= block_move

                # Display score
                score(scoreVal, b.number)

                # Check whether bird is in frame
                if b.y > surfaceHeight - b.imageHeight:
                    game_over = True

                # Draw new block as current block exits frame
                if x_block < (-1 * blockWidth):
                    x_block = surfaceWidth
                    blockHeight1 = randint (0, int (surfaceHeight / 1.5))

                # Check for collision with upper block
                if b.x + b.imageWidth > x_block:
                    # bird is within the block
                    if b.x < x_block + blockWidth:
                        if b.y < blockHeight1 + 15:
                            if b.x - b.imageWidth < blockWidth + x_block:
                                game_over = True

                # Check for collision with lower block
                if b.x + b.imageWidth > x_block:
                    if b.y + b.imageHeight > blockHeight1 + gap:
                        if b.x < x_block + blockWidth:
                            game_over = True
                
                # Update score
                if b.x < x_block + 40 and b.x > x_block - block_move + i * 20:
                    scoreVal += 1

                pygame.display.update ()
                clock.tick (60)


if __name__ == '__main__':
    gameStart()
    main ()
    pygame.quit ()
    quit ()
