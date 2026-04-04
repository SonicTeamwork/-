import pygame 
import sys
import json
import os
import L1
import L2
import L3
import L4
import L5



SAVE_FILE = "savegame.json"

def save_data(data):
    with open(SAVE_FILE, "w") as f:
        json.dump(data, f)

def load_data():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r") as f:
            return json.load(f)
    # Если файла нет, возвращаем значения по умолчанию
    return {"level": 1, "score": 0} 


pygame.init()
FPS = pygame.time.Clock()

# Теперь это сработает!
progress = load_data()
current_level = progress["level"]

screen = pygame.display.set_mode((1920, 1080))

try:
    font = pygame.font.Font('Arial', 36)
except:
    font = pygame.font.SysFont('Arial', 36)

text_surface = font.render('Уровень 1: Опушка леса', False, (255, 255, 255)) 
# Твои картинки
background = pygame.Surface((1900, 1080)) 
background.fill((50, 50, 50)) 

Level1 = pygame.image.load('images/Level1.png')
Level1_rect = Level1.get_rect(center=(950, 500))

ESC = pygame.image.load('images/ESC.png')
ESC_resized = pygame.transform.scale(ESC, (50, 50))
ESC_rect = ESC_resized.get_rect(center=(1750, 100))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            if ESC_rect.collidepoint(event.pos):
                running = False

            if Level1_rect.collidepoint(event.pos):
                result = L1.run_level(screen)
                
                # АВТОСОХРАНЕНИЕ: если вернулись из уровня, сохраняем прогресс
                # Например, пометим, что уровень 1 пройден
                save_data({"level": 2, "score": 100})
                
                if result == "QUIT":
                    running = False

    screen.blit(background, (0, 0))
    screen.blit(Level1, Level1_rect)
    screen.blit(ESC_resized, ESC_rect)
    screen.blit(text_surface, (820, 600))

    pygame.display.update()
    FPS.tick(60)

pygame.quit()
sys.exit()
