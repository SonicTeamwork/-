import pygame 
import sys

pygame.init()
FPS = pygame.time.Clock()

screen = pygame.display.set_mode((987, 494))
background = pygame.image.load('images/Background.png')

t1_x, t1_y = 940, 330
trash1 = pygame.image.load('images/oil.png')
resized_trash1 = pygame.transform.scale(trash1, (35, 45))
trash1_rect = resized_trash1.get_rect(topleft=(t1_x, t1_y))

t2_x, t2_y = 150, 330
trash2 = pygame.image.load('images/core bottle.png')
resized_trash2 = pygame.transform.scale(trash2, (35, 35))
trash2_rect = resized_trash2.get_rect(topleft=(t2_x, t2_y))

bush1 = pygame.image.load('images/Bush.png')
resized_bush = pygame.transform.scale(bush1, (95, 65))
bush_rect = resized_bush.get_rect(topleft=(t2_x - 5, t2_y))

trash1_exists = True
trash2_exists = True

bg_x = 0
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Проверяем клик по первому мусору
            if trash1_exists and trash1_rect.collidepoint(event.pos):
                trash1_exists = False

            elif trash2_exists and trash2_rect.collidepoint(event.pos):
                trash2_exists = False
    
    # Отрисовка фона
    screen.blit(background, (bg_x, 0))
    screen.blit(background, (bg_x + 987, 0))
    
    # Отрисовка куста
    screen.blit(resized_bush, bush_rect)
    
    # Отрисовка мусора (только если существует)
    if trash1_exists:
        screen.blit(resized_trash1, trash1_rect)
    if trash2_exists:
        screen.blit(resized_trash2, trash2_rect)
    
    pygame.display.update()
    FPS.tick(30)

pygame.quit()