import pygame
import sys

def run_title_screen(screen):
    FPS = pygame.time.Clock()
    sw, sh = screen.get_size()
    ESC = pygame.image.load('images/ESC.png')
    ESC_resized = pygame.transform.scale(ESC, (60, 60))
    ESC_rect = ESC_resized.get_rect(topleft=(1860, 60))
    
    GRAY = (50, 50, 50)
    BLACK = (0, 0, 0)
    
    background = pygame.Surface((sw, sh))
    background.fill(GRAY)
    
    start_img = pygame.image.load('images/Start.png')
    start_img = pygame.transform.scale(start_img, (300, 100))
    start_rect = start_img.get_rect(center=(sw // 2, sh // 2))
    
    font = pygame.font.SysFont('Arial', 72)
    title_text = font.render('ЧистоМэн', True, (255, 255, 255))
    title_rect = title_text.get_rect(center=(sw // 2, 200))
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "QUIT"
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if ESC_rect.collidepoint(event.pos):
                    return "QUIT"
                
                if start_rect.collidepoint(event.pos):
                    return "START"
                elif ESC_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
        
        screen.blit(background, (0, 0))
        screen.blit(title_text, title_rect)
        screen.blit(start_img, start_rect)
        screen.blit(ESC_resized, ESC_rect)
        
        pygame.display.update()
        FPS.tick(60)
    
    return "QUIT"