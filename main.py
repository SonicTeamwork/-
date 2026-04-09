import pygame 
import sys
import saves
import L1, L2, L3, L4, L5

pygame.init()
FPS = pygame.time.Clock()
screen = pygame.display.set_mode((1920, 1080))
pygame.display.set_caption("ЧистоМэн")

GRAY = (50, 50, 50)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

background = pygame.Surface((1920, 1080))
background.fill(GRAY)

OFFSET_X = 80
OFFSET_Y = -10

done_raw = pygame.image.load('images/Здесь прибрался чисто мэн.png')
done_scaled = pygame.transform.smoothscale(done_raw, (100, 150)) 

level_positions = {
    1: (300, 400),
    2: (600, 400),
    3: (900, 400),
    4: (1200, 400),
    5: (1500, 400)
}

level_images = {}
for i in range(1, 6):
    level_images[i] = pygame.image.load(f'images/level{i}.png')
    level_images[i] = pygame.transform.scale(level_images[i], (150, 150))

ESC_img = pygame.image.load('images/ESC.png')
ESC_resized = pygame.transform.scale(ESC_img, (60, 60))
ESC_rect = ESC_resized.get_rect(topleft=(1750, 60))

font = pygame.font.SysFont('Arial', 36)
text_NewGame = font.render("Новая игра", True, BLACK)
NewGame = pygame.image.load('images/NewGame.png')
NewGame_res = pygame.transform.scale(NewGame, (150, 60))
NewGame_rect = NewGame_res.get_rect(topleft=(1700, 500))

text_are_you_SURE = font.render("Ты уверен?", True, WHITE)

button_YES = pygame.transform.scale(NewGame, (100, 60))
text_YES = font.render("ДА", True, BLACK)
text_YES_rect = button_YES.get_rect(topleft=(1000, 600))

button_NO = pygame.transform.scale(NewGame, (100, 60))
text_NO = font.render("НЕТ", True, BLACK)
text_NO_rect = button_NO.get_rect(topleft=(820, 600))

def reset_game():
    saves.reset_progress()

def load_and_display_data():
    data = saves.load_data()
    return data.get("completed_levels", [])

running = True
showing_confirmation = False
completed_levels = load_and_display_data()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if ESC_rect.collidepoint(event.pos):
                running = False

            if showing_confirmation:
                if text_YES_rect.collidepoint(event.pos):
                    reset_game()
                    showing_confirmation = False
                    completed_levels = load_and_display_data()
                elif text_NO_rect.collidepoint(event.pos):
                    showing_confirmation = False
            else:
                if NewGame_rect.collidepoint(event.pos):
                    showing_confirmation = True

                for level_num in range(1, 6):
                    if level_num in level_positions:
                        img_rect = level_images[level_num].get_rect(center=level_positions[level_num])
                        if img_rect.collidepoint(event.pos):
                            if saves.is_level_unlocked(level_num):
                                if level_num == 1:
                                    result = L1.run_level(screen)
                                elif level_num == 2:
                                    result = L2.run_level(screen)
                                elif level_num == 3:
                                    result = L3.run_level(screen)
                                elif level_num == 4:
                                    result = L4.run_level(screen)
                                elif level_num == 5:
                                    result = L5.run_level(screen)
                                
                                if result == "QUIT":
                                    running = False
                                elif result == "COMPLETED":
                                    saves.complete_level(level_num)
                                    completed_levels = load_and_display_data()

    screen.blit(background, (0, 0))
    
    for level_num in range(1, 6):
        if level_num in level_positions:
            pos = level_positions[level_num]
            level_img = level_images[level_num]
            level_rect = level_img.get_rect(center=pos)
            
            screen.blit(level_img, level_rect)

            if level_num in completed_levels:
                done_rect = done_scaled.get_rect(center=(pos[0] + OFFSET_X, pos[1] + OFFSET_Y))
                screen.blit(done_scaled, done_rect)

    screen.blit(NewGame_res, NewGame_rect)
    screen.blit(text_NewGame, (1705, 505))
    screen.blit(ESC_resized, ESC_rect)
    
    if showing_confirmation:
        overlay = pygame.Surface((1920, 1080))
        overlay.set_alpha(180)
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))
        
        screen.blit(text_are_you_SURE, (960 - text_are_you_SURE.get_width() // 2, 540))
        screen.blit(button_YES, text_YES_rect)
        screen.blit(text_YES, (text_YES_rect.x + 35, text_YES_rect.y + 15))
        screen.blit(button_NO, text_NO_rect)
        screen.blit(text_NO, (text_NO_rect.x + 30, text_NO_rect.y + 15))
    
    pygame.display.update()
    FPS.tick(60)

pygame.quit()
sys.exit()
