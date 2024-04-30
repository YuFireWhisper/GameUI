import pygame
import sys
from screen_main_page import setupScreen
from screen_setting_page import SettingScreenPage
from screen_start_page import StartPage

pygame.init()

screen = setupScreen(pygame.display.Info())
setting_screen = SettingScreenPage(pygame.display.Info())
start_screen = StartPage(pygame.display.Info())

current_screen = "main"

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if current_screen == "main" and screen.setting_icon_rect.collidepoint(event.pos):
                current_screen = "setting"

            elif current_screen == "setting":
                setting_screen.handle_event(event)

            elif current_screen == "main" and screen.start_button_rect.collidepoint(event.pos):
                current_screen = "start"
            
            elif current_screen == "start":
                start_screen.handle_events(event)

    if current_screen == "main":
        # 繪製物件
        screen.screen.blit(screen.background_image, (0, 0))
        screen.screen.blit(screen.setting_icon, screen.setting_icon_rect)
        screen.screen.blit(screen.start_button, screen.start_button_rect)

    elif current_screen == "setting":
        setting_screen.draw()

    elif current_screen == "start":
        start_screen.draw()

    # main code here


    pygame.display.flip()
    screen.fpsClock.tick(screen.fps)