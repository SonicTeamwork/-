import pygame

def run_level(screen):
    running = True
    clock = pygame.time.Clock()
    
    # 1. Загрузка ресурсов под размер 1900x1000
    background = pygame.image.load('images/Background.png')
    resized_background = pygame.transform.scale(background, (1920, 1080))

    trash_img = pygame.image.load('images/oil.png')
    trash_res = pygame.transform.scale(trash_img, (80, 100)) # Увеличил, т.к. экран большой
    
    # СТАВИМ В ПРЕДЕЛАХ 1900x1000
    # Мусор справа
    trash_rect = trash_res.get_rect(center=(1800, 150))
    
    # Корзина слева (сделал побольше, чтобы легче попасть)
    bin_rect = pygame.Rect(1720, 480, 200, 600)
    
    trash_exist = True
    dragging = False 

    while running:
        mouse_pos = pygame.mouse.get_pos() 

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "QUIT"
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if trash_exist and trash_rect.collidepoint(event.pos):
                    dragging = True

            if event.type == pygame.MOUSEBUTTONUP:
                if dragging:
                    dragging = False
                    if trash_rect.colliderect(bin_rect):
                        trash_exist = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        if dragging:
            trash_rect.center = mouse_pos 

        # Отрисовка
        screen.blit(resized_background, (0, 0))
        
        # Рисуем корзину (белая рамка)
        pygame.draw.rect(screen, (255, 255, 255), bin_rect, 3) 
        
        if trash_exist:
            screen.blit(trash_res, trash_rect)
            if dragging:
                pygame.draw.rect(screen, (255, 255, 0), trash_rect, 2)

        pygame.display.flip()
        clock.tick(60)

    return "MENU"
