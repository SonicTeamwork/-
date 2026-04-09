import pygame

def run_level(screen):
    running = True
    FPS = pygame.time.Clock()
    font = pygame.font.SysFont('Arial', 40)
    ESC = pygame.image.load('images/ESC.png')
    ESC_res = pygame.transform.scale(ESC, (50, 50))
    ESC_rect = ESC_res.get_rect(topleft=(1750, 100))
    
    while running:
        # ВСЕ события должны быть внутри этого цикла
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "QUIT"
            
            # Проверка клика МЫШКОЙ (внутри for event!)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if ESC_rect.collidepoint(event.pos):
                    return "MENU"
            
            # Проверка КЛАВИАТУРЫ (внутри for event!)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "MENU"

        screen.fill((30, 30, 100))
        text = font.render("это уровень 3 НЕЗАВЕРШЁННЫЙ ЗДЕСЬ НЕЧЕГО СМОТРЕТЬ", True, (255, 255, 255))
        screen.blit(text, (250, 200))
        screen.blit(ESC_res, ESC_rect)
            
        pygame.display.flip()
        FPS.tick(60)
