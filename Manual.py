import pygame
import sys

def run_manual(screen, first_time=False):
    sw, sh = screen.get_size()
    clock = pygame.time.Clock()
    
    manual_soundtrack = pygame.mixer.Sound('soundtracks/SA2 - Advertise.mp3')
    manual_soundtrack.play(-1)
    
    try:
        title_font = pygame.font.SysFont('Arial', 64, bold=True)
        text_font = pygame.font.SysFont('Arial', 36)
        hint_font = pygame.font.SysFont('Arial', 24)
    except:
        title_font = pygame.font.Font(None, 64)
        text_font = pygame.font.Font(None, 36)
        hint_font = pygame.font.Font(None, 24)
    
    try:
        background = pygame.transform.scale(pygame.image.load('images/images Pixel/1Background.png'), (sw, sh))
    except:
        background = pygame.Surface((sw, sh))
        background.fill((30, 30, 50))
    
    ESC_img = pygame.transform.scale(pygame.image.load('images/ESC.png'), (50, 50))
    ESC_rect = ESC_img.get_rect(topleft=(sw - 70, 20))
    
    text_lines = [
        "ЧистоМэн",
        "",
        "Привет! Я супергерой ЧистоМэн из Челябинска!",
        "",
        "Моя главная задача — оберегать этот мир",
        "от загрязнения природы.",
        "",
        "Я каждый субботник прихожу убирать мусор,",
        "но и постоянно это делаю.",
        "",
        "Меня позвали убрать мусор в лесу,",
        "но здесь больше мусора, чем в Челябинске...",
        "",
        "Значит, за это берётся ЧистоМэн!",
        "",
        "Ещё слышал, что произошёл разлив нефти в Анапе.",
        "Я этого так не оставлю!",
        "",
        "Вы думаете, зачем мне всё это делать?",
        "",
        "А вот ответ: если бы меня не было,",
        "то земля была бы загрязнена гораздо сильнее,",
        "чем сейчас.",
        "",
        "Поэтому я здесь. ЧистоМэн всегда на страже!",
    ]
    
    rendered_lines = []
    for line in text_lines:
        if line == "":
            rendered_lines.append(None)
        else:
            if line == "ЧистоМэн":
                surf = title_font.render(line, True, (255, 215, 0))
            else:
                surf = text_font.render(line, True, (255, 255, 255))
            rendered_lines.append(surf)
    
    total_height = 0
    for surf in rendered_lines:
        if surf is not None:
            total_height += surf.get_height() + 10
        else:
            total_height += 30
    
    running = True
    text_start_y = sh
    scroll_speed = 1.5
    scroll_active = True
    skip_requested = False
    animation_complete = False
    
    fade_surface = pygame.Surface((sw, sh))
    fade_surface.fill((0, 0, 0))
    fade_alpha = 0
    fading_out = False
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                manual_soundtrack.stop()
                return "QUIT"
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if ESC_rect.collidepoint(event.pos):
                    manual_soundtrack.stop()
                    return "MENU"
                
                if not fading_out:
                    if scroll_active:
                        skip_requested = True
                    else:
                        fading_out = True
        
        screen.blit(background, (0, 0))
        screen.blit(ESC_img, ESC_rect)
        
        if scroll_active and not skip_requested:
            y = text_start_y
            for surf in rendered_lines:
                if surf is not None:
                    screen.blit(surf, (sw//2 - surf.get_width()//2, y))
                    y += surf.get_height() + 10
                else:
                    y += 30
            
            text_start_y -= scroll_speed
            
            if text_start_y + total_height < 0:
                scroll_active = False
                animation_complete = True
            
            hint_text = hint_font.render("Кликните мышкой, чтобы пропустить", True, (200, 200, 200))
            screen.blit(hint_text, (sw//2 - hint_text.get_width()//2, sh - 50))
        
        elif skip_requested and scroll_active:
            text_start_y = -total_height + sh
            scroll_active = False
            animation_complete = True
            
            y = text_start_y
            for surf in rendered_lines:
                if surf is not None:
                    screen.blit(surf, (sw//2 - surf.get_width()//2, y))
                    y += surf.get_height() + 10
                else:
                    y += 30
            
            hint_text = hint_font.render("Кликните мышкой, чтобы выйти", True, (200, 200, 200))
            screen.blit(hint_text, (sw//2 - hint_text.get_width()//2, sh - 50))
        
        elif not scroll_active and not fading_out:
            y = text_start_y if text_start_y + total_height > 0 else -total_height + sh
            for surf in rendered_lines:
                if surf is not None:
                    screen.blit(surf, (sw//2 - surf.get_width()//2, y))
                    y += surf.get_height() + 10
                else:
                    y += 30
            
            if animation_complete:
                hint_text = hint_font.render("Кликните мышкой, чтобы выйти", True, (200, 200, 200))
                screen.blit(hint_text, (sw//2 - hint_text.get_width()//2, sh - 50))
        
        if fading_out:
            fade_alpha += 15
            if fade_alpha >= 255:
                fade_alpha = 255
                manual_soundtrack.stop()
                if first_time:
                    return "MANUAL_SEEN"
                else:
                    return "MENU"
            fade_surface.set_alpha(fade_alpha)
            screen.blit(fade_surface, (0, 0))
        
        if not scroll_active and animation_complete and not fading_out and first_time:
            fading_out = True
        
        pygame.display.flip()
        clock.tick(60)
    
    manual_soundtrack.stop()
    return "MENU"