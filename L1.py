import pygame
import saves

def run_level(screen):
    pygame.event.clear()
    running = True
    clock = pygame.time.Clock()
    sw, sh = screen.get_size()
    
    ESC_res = pygame.transform.scale(pygame.image.load('images/ESC.png'), (50, 50))
    ESC_rect = ESC_res.get_rect(topleft=(1750, 100))

    try:
        font = pygame.font.SysFont('Arial', 40)
        btn_font = pygame.font.SysFont('Arial', 30)
    except:
        font = pygame.font.Font(None, 40)
        btn_font = pygame.font.Font(None, 30)
    
    text_surface = font.render('Уровень пройден!', True, (255, 255, 255))
    
    next_btn_text = btn_font.render('Следующий уровень', True, (255, 255, 255))
    menu_btn_text = btn_font.render('В меню', True, (255, 255, 255))
    next_btn_rect = next_btn_text.get_rect(center=(sw // 2, sh // 2 + 50))
    menu_btn_rect = menu_btn_text.get_rect(center=(sw // 2, sh // 2 + 120))

    background = pygame.transform.scale(pygame.image.load('images/Background.png'), (sw, sh))
    bin_res = pygame.transform.scale(pygame.image.load('images/Урна.png'), (185, 250))
    bin_rect = bin_res.get_rect(bottomright=(sw - 100, sh - 50))

    bush_res = pygame.transform.scale(pygame.image.load('images/Bush.png'), (250, 160))
    bush_rect = bush_res.get_rect(topleft=(100, 700))
    
    bush2_res = pygame.transform.scale(pygame.image.load('images/Bush.png'), (250, 160))
    bush2_rect = bush2_res.get_rect(topleft=(1000, 700))
    
    lupa_res = pygame.transform.scale(pygame.image.load('images/Lupa.png'), (40, 40))

    trash2_res = pygame.transform.scale(pygame.image.load('images/core bottle.png'), (80, 70))
    trash3_res = pygame.transform.scale(pygame.image.load('images/Balloon.png'), (80, 30))
    
    all_trash = []

    positions = [(1050, 900), (780, 910), (1080, 900), (500, 860), (1700, 810), (450, 830)]
    for pos in positions:
        all_trash.append({'rect': trash2_res.get_rect(center=pos), 'img': trash2_res, 'visible': True})
    
    # Мусор за первым кустом
    hidden_rect1 = trash3_res.get_rect(center=bush_rect.center)
    all_trash.append({'rect': hidden_rect1, 'img': trash3_res, 'visible': False, 'bush': bush_rect})
    
    # Мусор за вторым кустом
    hidden_rect2 = trash3_res.get_rect(center=bush2_rect.center)
    all_trash.append({'rect': hidden_rect2, 'img': trash3_res, 'visible': False, 'bush': bush2_rect})
    
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
                
                # Проверка клика по кустам для обнаружения мусора
                if bush_rect.collidepoint(event.pos):
                    for item in all_trash:
                        if not item['visible'] and 'bush' in item and item['bush'] == bush_rect:
                            item['visible'] = True
                
                if bush2_rect.collidepoint(event.pos):
                    for item in all_trash:
                        if not item['visible'] and 'bush' in item and item['bush'] == bush2_rect:
                            item['visible'] = True
                
                # Захват мусора
                for i in range(len(all_trash) - 1, -1, -1):
                    if all_trash[i]['visible'] and all_trash[i]['rect'].collidepoint(event.pos):
                        dragging = True
                        active_idx = i
                        break

            if event.type == pygame.MOUSEBUTTONUP:
                if dragging and active_idx is not None:
                    if active_idx < len(all_trash) and all_trash[active_idx]['rect'].colliderect(bin_rect):
                        all_trash.pop(active_idx)
                    dragging = False
                    active_idx = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "MENU"

        if dragging and active_idx is not None and active_idx < len(all_trash):
            all_trash[active_idx]['rect'].center = mouse_pos 

        # Отрисовка
        screen.blit(background, (0, 0))
        screen.blit(bin_res, bin_rect)
        screen.blit(bush_res, bush_rect)
        screen.blit(bush2_res, bush2_rect)
        screen.blit(ESC_res, ESC_rect)

        # Лупа при наведении на кусты
        if bush_rect.collidepoint(mouse_pos) or bush2_rect.collidepoint(mouse_pos):
            screen.blit(lupa_res, (mouse_pos[0] - 20, mouse_pos[1] - 20))

        # Отрисовка видимого мусора
        for item in all_trash:
            if item['visible']:
                screen.blit(item['img'], item['rect'])

        # Счетчик мусора
        visible_trash = sum(1 for item in all_trash if item['visible'])
        count_text = font.render(f"Осталось мусора: {visible_trash}", True, (255, 255, 255))
        screen.blit(count_text, (150, 50))

        # Проверка завершения уровня
        if visible_trash == 0:
            # Сохраняем прогресс - отмечаем уровень 1 как пройденный и разблокируем уровень 2
            saves.complete_level(1)
            
            choosing = True
            while choosing:
                screen.blit(text_surface, (sw // 2 - text_surface.get_width() // 2, sh // 2 - 80))
                
                # Кнопка "Следующий уровень"
                pygame.draw.rect(screen, (0, 150, 0), next_btn_rect.inflate(20, 10))
                pygame.draw.rect(screen, (100, 100, 100), next_btn_rect.inflate(20, 10), 2)
                screen.blit(next_btn_text, next_btn_rect)
                
                # Кнопка "В меню"
                pygame.draw.rect(screen, (150, 0, 0), menu_btn_rect.inflate(20, 10))
                pygame.draw.rect(screen, (100, 100, 100), menu_btn_rect.inflate(20, 10), 2)
                screen.blit(menu_btn_text, menu_btn_rect)
                
                pygame.display.flip()
                
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return "QUIT"
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if next_btn_rect.collidepoint(event.pos):
                            # Проверяем, разблокирован ли уровень 2
                            if saves.is_level_unlocked(2):
                                import L2
                                result = L2.run_level(screen)
                                return result
                            else:
                                print("Ошибка: уровень 2 не разблокирован!")
                                return "MENU"
                        if menu_btn_rect.collidepoint(event.pos):
                            return "MENU"

        pygame.display.flip()
        clock.tick(60)
    
    return "MENU"
