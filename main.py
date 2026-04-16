import pygame 
import sys
import saves
import L1, L2, L3, L4, L5
import Title
import Bonus_level_TRASH_E
import Manual

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
    5: (1500, 400),
    6: (300, 600)
}

level_images = {}
for i in range(1, 6):
    level_images[i] = pygame.image.load(f'images/level{i}.png')
    level_images[i] = pygame.transform.scale(level_images[i], (150, 150))

bonus_img = pygame.image.load('images/Bonus Levels.png')
bonus_img = pygame.transform.scale(bonus_img, (150, 150))
level_images[6] = bonus_img

font_bonus = pygame.font.SysFont('Arial', 40)
bonus_text = font_bonus.render("TRASH E", True, BLACK)

ESC_img = pygame.image.load('images/ESC.png')
ESC_resized = pygame.transform.scale(ESC_img, (60, 60))
ESC_rect = ESC_resized.get_rect(topleft=(1750, 60))

font = pygame.font.SysFont('Arial', 36)
text_NewGame = font.render("Новая игра", True, BLACK)
NewGame = pygame.image.load('images/NewGame.png')
NewGame_res = pygame.transform.scale(NewGame, (150, 60))
NewGame_rect = NewGame_res.get_rect(topleft=(1300, 800))

text_are_you_SURE = font.render("Ты уверен?", True, WHITE)

button_YES = pygame.transform.scale(NewGame, (100, 60))
text_YES = font.render("ДА", True, BLACK)
text_YES_rect = button_YES.get_rect(topleft=(1000, 600))

button_NO = pygame.transform.scale(NewGame, (100, 60))
text_NO = font.render("НЕТ", True, BLACK)
text_NO_rect = button_NO.get_rect(topleft=(820, 600))

manual_button = pygame.image.load('images/scenes_block.png')
manual_res = pygame.transform.scale(manual_button, (150, 150))
manual_rect = manual_res.get_rect(topleft=(150, 830))

Title_music = pygame.mixer.Sound('soundtracks/Sonic the Hedgehog(spinball) - Toxic caves.mp3')
MENU_music = pygame.mixer.Sound('soundtracks/Sonic 3 Music Team Various - Data Select.mp3')

def reset_game():
    saves.reset_progress()
    # Также сбрасываем флаг просмотра мануала
    data = saves.load_data()
    data["manual_seen"] = False
    saves.save_data(data)

def load_and_display_data():
    data = saves.load_data()
    return data.get("completed_levels", [])

def is_bonus_unlocked():
    """Бонусный уровень открывается после прохождения всех 5 уровней"""
    completed = load_and_display_data()
    return all(level in completed for level in [1, 2, 3, 4, 5])

def has_seen_manual():
    """Проверяет, видел ли игрок мануал"""
    data = saves.load_data()
    return data.get("manual_seen", False)

def set_manual_seen():
    """Отмечает, что игрок видел мануал"""
    data = saves.load_data()
    data["manual_seen"] = True
    saves.save_data(data)

def has_any_save():
    """Проверяет, есть ли какие-либо сохранения"""
    data = saves.load_data()
    completed = data.get("completed_levels", [])
    return len(completed) > 0

current_screen = "TITLE"
showing_confirmation = False
completed_levels = load_and_display_data()
music_playing = False

while True:
    if current_screen == "TITLE":
        if not music_playing:
            Title_music.play(-1)
            music_playing = True
        result = Title.run_title_screen(screen)
        if result == "QUIT":
            Title_music.stop()
            break
        elif result == "START":
            Title_music.stop()
            music_playing = False
            
            # Проверяем: если нет сохранений И мануал не был показан
            if not has_any_save() and not has_seen_manual():
                # Показываем мануал только если нет сохранений и мануал не был показан
                manual_result = Manual.run_manual(screen, first_time=True)
                if manual_result == "QUIT":
                    pygame.quit()
                    sys.exit()
                elif manual_result == "MANUAL_SEEN":
                    set_manual_seen()
            
            MENU_music.play(-1)
            music_playing = True
            current_screen = "LEVELS"
            completed_levels = load_and_display_data()
    
    elif current_screen == "LEVELS":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if ESC_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

                if showing_confirmation:
                    if text_YES_rect.collidepoint(event.pos):
                        # Сбрасываем прогресс
                        saves.reset_progress()
                        reset_game()
                        showing_confirmation = False
                        completed_levels = load_and_display_data()
                        # Возвращаемся в титульный экран
                        MENU_music.stop()
                        music_playing = False
                        current_screen = "TITLE"
                    elif text_NO_rect.collidepoint(event.pos):
                        showing_confirmation = False
                else:
                    if NewGame_rect.collidepoint(event.pos):
                        showing_confirmation = True
                        continue

                    # Проверка клика по мануалу
                    if manual_rect.collidepoint(event.pos):
                        MENU_music.stop()
                        music_playing = False
                        result = Manual.run_manual(screen, first_time=False)
                        if result == "QUIT":
                            pygame.quit()
                            sys.exit()
                        elif result == "MENU":
                            current_screen = "TITLE"
                        # Возобновляем музыку меню только если мы всё ещё на экране LEVELS
                        if current_screen == "LEVELS" and not music_playing:
                            MENU_music.play(-1)
                            music_playing = True
                        continue

                    # Проверка клика по бонусному уровню (6)
                    bonus_rect = level_images[6].get_rect(center=level_positions[6])
                    if bonus_rect.collidepoint(event.pos):
                        if is_bonus_unlocked():
                            MENU_music.stop()
                            music_playing = False
                            result = Bonus_level_TRASH_E.run_level(screen)
                            
                            print(f"Результат бонусного уровня: {result}")
                            
                            if result == "QUIT":
                                pygame.quit()
                                sys.exit()
                            elif result == "MENU":
                                current_screen = "TITLE"
                            else:
                                saves.complete_level('bonus')
                                completed_levels = load_and_display_data()
                            
                            if current_screen == "LEVELS" and not music_playing:
                                MENU_music.play(-1)
                                music_playing = True
                        continue

                    # Обычные уровни 1-5
                    for level_num in range(1, 6):
                        if level_num in level_positions:
                            img_rect = level_images[level_num].get_rect(center=level_positions[level_num])
                            if img_rect.collidepoint(event.pos):
                                if saves.is_level_unlocked(level_num):
                                    MENU_music.stop()
                                    music_playing = False
                                    
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
                                    
                                    print(f"Результат уровня {level_num}: {result}")
                                    
                                    if result == "QUIT":
                                        pygame.quit()
                                        sys.exit()
                                    elif result == "MENU":
                                        current_screen = "TITLE"
                                    elif result == "GAME_COMPLETE":
                                        print("Поздравляем! Игра полностью пройдена!")
                                        saves.complete_level(5)
                                        completed_levels = load_and_display_data()
                                        current_screen = "TITLE"
                                    else:
                                        saves.complete_level(level_num)
                                        completed_levels = load_and_display_data()
                                        print(f"Уровень {level_num} отмечен как пройденный! Пройдено: {completed_levels}")
                                    
                                    if current_screen == "LEVELS" and not music_playing:
                                        MENU_music.play(-1)
                                        music_playing = True
                                break

        screen.blit(background, (0, 0))
        
        # Отрисовка уровней 1-5
        for level_num in range(1, 6):
            if level_num in level_positions:
                pos = level_positions[level_num]
                level_img = level_images[level_num]
                level_rect = level_img.get_rect(center=pos)
                
                screen.blit(level_img, level_rect)

                if level_num in completed_levels:
                    done_rect = done_scaled.get_rect(center=(pos[0] + OFFSET_X, pos[1] + OFFSET_Y))
                    screen.blit(done_scaled, done_rect)

        # Отрисовка бонусного уровня
        bonus_pos = level_positions[6]
        bonus_rect = level_images[6].get_rect(center=bonus_pos)
        screen.blit(level_images[6], bonus_rect)
        
        # Если бонус не открыт - затемнение
        if not is_bonus_unlocked():
            overlay = pygame.Surface((150, 150))
            overlay.set_alpha(180)
            overlay.fill(BLACK)
            screen.blit(overlay, bonus_rect)
            
            # Рисуем замок
            try:
                lock_img = pygame.transform.scale(pygame.image.load('images/lock.png'), (50, 50))
                screen.blit(lock_img, (bonus_pos[0] - 25, bonus_pos[1] - 25))
            except:
                lock_text = font.render("?", True, WHITE)
                screen.blit(lock_text, (bonus_pos[0] - 10, bonus_pos[1] - 10))
        
        # Если бонус пройден - галочка
        elif 'bonus' in completed_levels:
            done_rect = done_scaled.get_rect(center=(bonus_pos[0] + OFFSET_X, bonus_pos[1] + OFFSET_Y))
            screen.blit(done_scaled, done_rect)

        screen.blit(NewGame_res, NewGame_rect)
        screen.blit(text_NewGame, (1300, 805))
        screen.blit(ESC_resized, ESC_rect)
        screen.blit(bonus_text, (230, 580))
        screen.blit(manual_res, manual_rect)
        
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
