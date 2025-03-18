import pygame

pygame.init()  

WIDTH, HEIGHT = 800, 800 #game window 
ROWS, COLS = 8, 8
SQUARE_SIZE = 87 

SCREEN = pygame.display.set_mode((800, 800))

# rgb
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (55, 140, 171)
GREY = (128,128,128)
RED = (127, 9, 9,)

CROWN = pygame.transform.scale(pygame.image.load('assets/crown.png'), (44, 25)) #to indetify king pieces

font = pygame.font.Font(None, 32) #font to be used for titles and on buttons

#sounds
piece_sound = pygame.mixer.Sound("assets/piece_sound.wav")
fanfare_sound = pygame.mixer.Sound("assets/fanfare.wav")
celebration_sound = pygame.mixer.Sound("assets/celebration.wav")
sad_trombone = pygame.mixer.Sound("assets/sad_trombone.wav")

def get_font(size): 
    return pygame.font.Font("assets/font.ttf", size)
