import pygame
import saves

def run_level(screen):
    pygame.event.clear()
    running = True
    clock = pygame.time.Clock()
    sw, sh = screen.get_size()
    
    # Загрузка ресурсов
    ESC_res = pygame.transform.scale(pygame.image.load('images/ESC.png'), (50, 50))
    ESC_rect = ESC_res.get_rect(topleft=(1750, 100))
    
    try:
        font = pygame.font.SysFont('Arial', 40)
        btn_font = pygame.font.SysFont('Arial', 30)
    except:
        font = pygame.font.Font(None, 40)
        btn_font = pygame.font.Font(None, 30)
    
    text_surface = font.render('Уровень 2 пройден!', True, (255, 255, 255))
    
    next_btn_text = btn_font.render('Следующий уровень', True, (255, 255, 255))
    menu_btn_text = btn_font.render('В меню', True, (255, 255, 255))
    next_btn_rect = next_btn_text.get_rect(center=(sw // 2, sh // 2 + 50))
    menu_btn_rect = menu_btn_text.get_rect(center=(sw // 2, sh // 2 + 120))

    background = pygame.transform.scale(pygame.image.load('images/Background.png'), (sw, sh))
    bin_res = pygame.transform.scale(pygame.image.load('images/Урна.png'), (185, 250))
    bin_rect = bin_res.get_rect(bottomright=(sw - 100, sh - 50))

    # Создаем мусор для уровня 2
    trash_items = []
    trash_img = pygame.transform.scale(pygame.image.load('images/oil.png'), (80, 100))
    
    # Позиции мусора для уровня 2
    positions = [(500, 800), (800, 850), (1200, 800), (1500, 850), (300, 900)]
    for pos in positions:
        trash_items.append({'rect': trash_img.get_rect(center=pos), 'img': trash_img, 'visible': True})
    
    active_idx = None
    dragging = False

    while running:
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "QUIT"
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if ESC_rect.collidepoint(event.pos):
                    return "MENU"
                
                # Захват мусора
                for i in range(len(trash_items) - 1, -1, -1):
                    if trash_items[i]['visible'] and trash_items[i]['rect'].collidepoint(event.pos):
                        dragging = True
                        active_idx = i
                        break
            
            if event.type == pygame.MOUSEBUTTONUP:
                if dragging and active_idx is not None:
                    if trash_items[active_idx]['rect'].colliderect(bin_rect):
                        trash_items.pop(active_idx)
                    dragging = False
                    active_idx = None
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "MENU"
        
        if dragging and active_idx is not None and active_idx < len(trash_items):
            trash_items[active_idx]['rect'].center = mouse_pos
        
        # Отрисовка
        screen.blit(background, (0, 0))
        screen.blit(bin_res, bin_rect)
        screen.blit(ESC_res, ESC_rect)
        
        # Отрисовка мусора
        for item in trash_items:
            if item['visible']:
                screen.blit(item['img'], item['rect'])
        
        # Счетчик
        visible_trash = sum(1 for item in trash_items if item['visible'])
        count_text = font.render(f"Осталось мусора: {visible_trash}", True, (255, 255, 255))
        screen.blit(count_text, (150, 50))
        
        # Проверка завершения
        if visible_trash == 0:
            # Сохраняем прогресс
            saves.save_data({"level_2_completed": True, "level": 3, "score": 200})
            
            choosing = True
            while choosing:
                screen.blit(text_surface, (sw // 2 - text_surface.get_width() // 2, sh // 2 - 80))
                
                # Кнопки
                pygame.draw.rect(screen, (0, 150, 0), next_btn_rect.inflate(20, 10))
                pygame.draw.rect(screen, (100, 100, 100), next_btn_rect.inflate(20, 10), 2)
                screen.blit(next_btn_text, next_btn_rect)
                
                pygame.draw.rect(screen, (150, 0, 0), menu_btn_rect.inflate(20, 10))
                pygame.draw.rect(screen, (100, 100, 100), menu_btn_rect.inflate(20, 10), 2)
                screen.blit(menu_btn_text, menu_btn_rect)
                
                pygame.display.flip()
                
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return "QUIT"
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if next_btn_rect.collidepoint(event.pos):
                            import L3
                            return L3.run_level(screen)
                        if menu_btn_rect.collidepoint(event.pos):
                            return "MENU"
        
        pygame.display.flip()
        clock.tick(60)
    
    return "MENU"
