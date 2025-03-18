import pygame, sys, time, random
from button import Button
from main import main  # Import the main function from main.py
from checkers.constants import get_font, SCREEN, fanfare_sound, sad_trombone, BLUE
from music import stop_music
from stats import Database_for_stats

pygame.init()

pygame.display.set_caption("Main Menu")

BG1 = pygame.image.load("assets/background_new.png") #background for the start screen- pink with flowers
BG2 = pygame.image.load("assets/rules.png") #background for the rules screen
BG3 = pygame.image.load("assets/baby.png") #baby image for the loser screen
settings_background = pygame.image.load("assets/settings_background.png") #background for the settings screen

celebration1 = pygame.image.load("assets/celebration1.png") #for winner
celebration2 = pygame.image.load("assets/celebration2.png")

tear = pygame.image.load("assets/tear.png")
tear_img = pygame.transform.scale(tear, (30, 45)) #resizes the tear to match size of baby

confetti = pygame.image.load("assets/confetti.png")
confetti_img = pygame.transform.scale(confetti, (200, 300))

LEFT_EYE_X, LEFT_EYE_Y = 330, 455 #coordinates for the left eye of baby
RIGHT_EYE_X, RIGHT_EYE_Y = 450, 455 #coordinates for the right eye

class Tear: #draws tears onto baby's face for loser
    def __init__(self, x, y):
        self.x = x + random.randint(-3, 3)  #adds some slight variation for where the tears appear, so individual tears are visible when they fall
        self.y = y
        self.speed = random.uniform(2, 5)  #random speed to create a natural effect

    def update(self):
        self.y += self.speed  #moves the tear down the screen
        if self.y > 800:  #reset when it reaches bottom of the screen
            self.y = random.randint(LEFT_EYE_Y, LEFT_EYE_Y + 20)

    def draw(self, screen):
        screen.blit(tear_img, (self.x, self.y))

class Confetti: #draws falling confetti onto screen for winner
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = random.uniform(2, 5)

    def update(self):
        self.y += self.speed
        if self.y > 800:
            self.y = random.randint(0, 800)

    def draw(self, screen):
        screen.blit(confetti_img, (self.x, self.y))

#creates multiple tears from both eyes
tears = [Tear(LEFT_EYE_X, LEFT_EYE_Y) for _ in range(5)] + [Tear(RIGHT_EYE_X, RIGHT_EYE_Y) for _ in range(5)]
confettis = [Confetti(random.randint(0, 800), random.randint(0, 200)) for _ in range(10)]

def loser(): #for when the player loses
    pygame.display.set_caption("Loser")
    stop_music()

    start_time = time.time() #necessary to ensure that the tears fall for 6 seconds before the screen clears
    clock = pygame.time.Clock()

    #creates the text message for the screen
    LOSER_TEXT = get_font(70).render("YOU LOSE!", True, "White")
    LOSER_RECT = LOSER_TEXT.get_rect(center=(400, 100))

    #tracks how long the tears have been falling
    tears_start_time = time.time()

    while True:
        sad_trombone.play(-1) #plays the sad trombone sound on loop whilsy the screen is displayed

        #quits background with baby image
        SCREEN.blit(BG3, (0, 0)) 

        SCREEN.blit(LOSER_TEXT, LOSER_RECT)

        if time.time() - tears_start_time < 6:
            for tear in tears:
                tear.update()
                tear.draw(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q): #so that the player can quit the game more quickly, than going through the start menu
                pygame.quit() 
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_b:
                sad_trombone.stop()
                main_menu()
                return

        pygame.display.update()
        clock.tick(30)  #smooth 30 FPS animation

        #after 6 seconds of tears, the screen will clear and return to the main menu
        if time.time() - tears_start_time >= 6:
            SCREEN.fill("black")
            time.sleep(0.3)
            sad_trombone.stop()
            main_menu()
            return

def winner(): #for when the player wins
    pygame.display.set_caption("Winner")
    stop_music()

    SCREEN.blit(celebration1, (0, 0)) #background for the winner screen. the initial background is this one and it should alternate with the other background
    
    confetti_start_time = time.time()

    #defines the  colors for the text
    colors = [(255, 0, 0), (255, 165, 0), (255, 255, 0), (51, 255, 51), (0, 191, 0), (57, 229, 225), (51, 51, 255), (168, 37, 255), (238, 130, 238)] #colours for the words to flash between

    start_time = time.time()
    last_background_switch = time.time()  #tracks last background switch time
    background_switch_interval = 0.2  #so that the background switches every 0.2 seconds

    j = 0  #for alternating the background
    clock = pygame.time.Clock()  #controls frame rate

    while True:
        fanfare_sound.play(-1) #plats on loop

        elapsed_time = time.time() - start_time  #updates elapsed time

        if elapsed_time >= 6:  #stops after 6 seconds
            break

        if time.time() - confetti_start_time < 6:
            for confetti in confettis:
                confetti.update()
                confetti.draw(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q): #keyboard inputs are also accepted
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_b:
                fanfare_sound.stop()
                main_menu() #back to main menu
                return

        #in order to switch the background every 0.2 seconds
        if time.time() - last_background_switch >= background_switch_interval:
            if j % 2 == 0: #modulus used to switch the background
                SCREEN.blit(celebration1, (0, 0))  #celebration1
            else:
                SCREEN.blit(celebration2, (0, 0))  #celebration2
            last_background_switch = time.time()  # update the last background switch time
            j += 1  #increment j to alternate between backgrounds

        #cycle through colors for the text every 0.2 seconds
        color_change_time = time.time() - start_time  #track time for color changes
        color_index = int(color_change_time / 0.2) % len(colors)  #determines the color based on time
        current_color = colors[color_index]

        #draw text with the current color
        WINNER_TEXT = get_font(70).render("YOU WIN!", True, current_color)
        WINNER_RECT = WINNER_TEXT.get_rect(center=(400, 100))
        SCREEN.blit(WINNER_TEXT, WINNER_RECT)  #draw text with changing colors
        pygame.display.update()

        clock.tick(30)  #limit the frame rate to 30 FPS for smooth animation
    fanfare_sound.stop()
    main_menu()  #switches to main_menu after 6 seconds automatically
    
def options():
    pygame.display.set_caption("Rules")

    while True:
        SCREEN.blit(BG2, (0, 0))

        OPTIONS_MOUSE_POS = pygame.mouse.get_pos() #so that the mouse can be used to select options since its position on the window is known

        OPTIONS_BACK = Button(image=None, pos=(600, 690),  
                            text_input="BACK", font=get_font(40), base_color="#455946", hovering_color="#5c0603ff") #back button

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
                pygame.quit()
                sys.exit()
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_b):
                    main_menu()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()

        pygame.display.update() #updates the screen

def settings(): #settings screen
    global difficulty
    pygame.display.set_caption("Settings")
    while True:
            board_background = pygame.image.load("assets/board_background.png") #so that the background is the one that I want - transparent
            SCREEN.blit(board_background, (0, 0))
           
            settings_rect = settings_background.get_rect(center=(400, 400))
            SCREEN.blit(settings_background, settings_rect.topleft)

            SETTINGS_MOUSE_POS = pygame.mouse.get_pos()
           
            SETTINGS_TEXT = get_font(70).render("SETTINGS", True, "White") #the title
            SETTINGS_RECT = SETTINGS_TEXT.get_rect(center=(400, 110))

            #the different buttons for the levels to choose from
            LV1_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(400, 250),
                                text_input="EASY", font=get_font(75), base_color="#D8FCFF", hovering_color="White")
            LV2_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(400, 400),
                                text_input="MEDIUM", font=get_font(68), base_color="#D8FCFF", hovering_color="White")
            LV3_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(400, 550),
                                text_input="HARD", font=get_font(75), base_color="#D8FCFF", hovering_color="White")
           
            settings_BACK = Button(image=None, pos=(655, 710),
                            text_input="BACK", font=get_font(40), base_color="White", hovering_color="#D8FCFF")
           
            settings_BACK.changeColor(SETTINGS_MOUSE_POS)
            settings_BACK.update(SCREEN)

            SCREEN.blit(SETTINGS_TEXT, SETTINGS_RECT)

            for button in [LV1_BUTTON, LV2_BUTTON, LV3_BUTTON]: #so that the buttons are displayed on the screen and vary with cover if the mouse hovers over them
                button.changeColor(SETTINGS_MOUSE_POS)
                button.update(SCREEN)
           
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
                    pygame.quit()
                    sys.exit()
                if (event.type == pygame.KEYDOWN and event.key == pygame.K_b):
                    main_menu()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if LV1_BUTTON.checkForInput(SETTINGS_MOUSE_POS):
                        difficulty = "easy"
                        return difficulty #so that the dissiculty given the the player matches up with the level they chose
                    if LV2_BUTTON.checkForInput(SETTINGS_MOUSE_POS): 
                        difficulty = "medium"
                        return difficulty
                    if LV3_BUTTON.checkForInput(SETTINGS_MOUSE_POS):
                        difficulty = "hard"
                        return difficulty
                    if settings_BACK.checkForInput(SETTINGS_MOUSE_POS):
                        main_menu()
    
            pygame.display.update()

def stats(): #stats screen 
    pygame.display.set_caption("⭐Stats⭐") #title for the stats screen
    db_instance = Database_for_stats()
    #upack the four stat rows (id 1, 2, 3, and 4)
    (wins1, losses1, quits1), (wins2, losses2, quits2), (wins3, losses3, quits3), (wins4, losses4, quits4) = db_instance.get_stats()

    # Helper function to calculate win rate
    def calc_win_rate(wins, losses):
        return (wins / (wins + losses) * 100) if (wins + losses) != 0 else 0

    #win rate calculated for each row.
    win_rate1 = calc_win_rate(wins1, losses1) 
    win_rate2 = calc_win_rate(wins2, losses2)
    win_rate3 = calc_win_rate(wins3, losses3)
    win_rate4 = calc_win_rate(wins4, losses4)

    # Define x-positions for each column (for Easy, Medium, Hard columns)
    col_positions = [150, 400, 650]
    # y-position where these columns begin (below the overall row)
    top_y = 350

    while True:
        GREY = (98, 120, 156)
        SCREEN.fill(GREY) #background colour is this
        YELLOW = (242, 210, 29)
        STATS_MOUSE_POS = pygame.mouse.get_pos()

        # Render and display the title
        title_text = get_font(70).render("STATS", True, YELLOW)
        title_rect = title_text.get_rect(center=(400, 80))
        SCREEN.blit(title_text, title_rect)

        overall_TEXT = get_font(20).render("Overall Stats", True, YELLOW) #greater size and yellow colour ensures that the title stands out well.
        overall_RECT = overall_TEXT.get_rect(center=(400, 200))
        SCREEN.blit(overall_TEXT, overall_RECT)

        overall_y = 250  # y-position just under the title
        overall_texts = [
            get_font(20).render(f"Wins: {wins4}", True, "White"),
            get_font(20).render(f"Losses: {losses4}", True, "White"),
            get_font(20).render(f"Quits: {quits4}", True, "White"),
            get_font(20).render(f"Win: {win_rate4:.2f}%", True, "White")
        ]
        # Hardcode x-positions for each overall stat (adjust as needed)
        overall_x_positions = [80, 280, 480, 680]
        for text_surface, x in zip(overall_texts, overall_x_positions):
            text_rect = text_surface.get_rect(center=(x, overall_y))
            SCREEN.blit(text_surface, text_rect)

        # Create lists of text surfaces for each column (Easy, Medium, Hard). This is what is displayed
        texts1 = [
            get_font(20).render("Easy", True, YELLOW),
            get_font(20).render(f"Wins: {wins1}", True, "White"),
            get_font(20).render(f"Losses: {losses1}", True, "White"),
            get_font(20).render(f"Quits: {quits1}", True, "White"),
            get_font(20).render(f"Win: {win_rate1:.2f}%", True, "White")
        ]
        texts2 = [
            get_font(20).render("Medium", True, YELLOW),
            get_font(20).render(f"Wins: {wins2}", True, "White"),
            get_font(20).render(f"Losses: {losses2}", True, "White"),
            get_font(20).render(f"Quits: {quits2}", True, "White"),
            get_font(20).render(f"Win: {win_rate2:.2f}%", True, "White")
        ]
        texts3 = [
            get_font(20).render("Hard", True, YELLOW),
            get_font(20).render(f"Wins: {wins3}", True, "White"),
            get_font(20).render(f"Losses: {losses3}", True, "White"),
            get_font(20).render(f"Quits: {quits3}", True, "White"),
            get_font(20).render(f"Win: {win_rate3:.2f}%", True, "White")
        ]

        # Helper function to blit a column of text surfaces vertically
        def blit_column(text_surfaces, x, start_y, line_height=40):
            for i, text_surface in enumerate(text_surfaces):
                text_rect = text_surface.get_rect(center=(x, start_y + i * line_height))
                SCREEN.blit(text_surface, text_rect)

        # Blit each column at its designated x-position
        blit_column(texts1, col_positions[0], top_y)
        blit_column(texts2, col_positions[1], top_y)
        blit_column(texts3, col_positions[2], top_y)

        # Create and display the BACK and RESET buttons.
        stats_BACK = Button(image=None, pos=(655, 710),
                            text_input="BACK", font=get_font(40), base_color="White", hovering_color=YELLOW)
        stats_BACK.changeColor(STATS_MOUSE_POS)
        stats_BACK.update(SCREEN)

        stats_RESET = Button(image=None, pos=(145, 710),
                             text_input="RESET", font=get_font(40), base_color="White", hovering_color=YELLOW)
        stats_RESET.changeColor(STATS_MOUSE_POS)
        stats_RESET.update(SCREEN)

        # Event handling for quitting, navigating, and resetting stats.
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_b:
                main_menu()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if stats_BACK.checkForInput(STATS_MOUSE_POS):
                    main_menu()
                if stats_RESET.checkForInput(STATS_MOUSE_POS):
                    db_instance = Database_for_stats()  # Create instance
                    db_instance.reset_stats()  # Reset stats
                    stats() 

        pygame.display.update()

def play(): #takes player to the main game loop to actually play draughts
    main()

def main_menu(): #start menu
    pygame.display.set_caption("Main Menu")
    while True:
        SCREEN.blit(BG1, (0, 0))
        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(70).render("START MENU", True, "#ff0000")
        MENU_RECT = MENU_TEXT.get_rect(center=(400, 100))

        #the difffernt buttons for the player to choose from
        PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(400, 250), 
                            text_input="PLAY", font=get_font(75), base_color="#D8FCFF", hovering_color="White")
        OPTIONS_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(400, 400), 
                            text_input="RULES", font=get_font(75), base_color="#D8FCFF", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(400, 700), 
                            text_input="QUIT", font=get_font(75), base_color="#D8FCFF", hovering_color="White")
        STATS_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(400, 550), 
                            text_input="STATS", font=get_font(75), base_color="#D8FCFF", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON, STATS_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                    break
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()
                if STATS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    stats()

        pygame.display.update()

main_menu() #this is the first function called since it is the main menu and the game starts from here. 




