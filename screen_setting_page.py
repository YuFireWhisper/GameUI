import pygame
import sys

from screen_main_page import setupScreen as screen

pygame.init()

screen = screen(pygame.display.Info())

class SettingScreenPage:

    WHITE = (255, 255, 255)
    RED = (255, 0, 0)

    def __init__(self, screenInfo):
        self.screen_width = screenInfo.current_w
        self.screen_height = screenInfo.current_h
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.screen.fill(SettingScreenPage.WHITE)

        # 聲音圖示
        self.sound_icon = pygame.image.load("public\\setting_sound.png").convert_alpha()
        self.sound_icon = pygame.transform.scale(self.sound_icon, (self.sound_icon.get_width() // 2, self.sound_icon.get_height() // 2))

        # 返回圖示
        self.back_icon = pygame.image.load("public\\setting_back.png").convert_alpha()
        self.back_icon = pygame.transform.scale(self.back_icon, (self.back_icon.get_width() // 2, self.back_icon.get_height() // 2))

        # 離開圖示
        self.exit_icon = pygame.image.load("public\\setting_exit.png").convert_alpha()
        self.exit_icon = pygame.transform.scale(self.exit_icon, (self.exit_icon.get_width() // 2, self.exit_icon.get_height() // 2))
    
    def draw(self):
        self.screen.fill(SettingScreenPage.WHITE)

        self.x = self.screen_width // 2 - 100

        # sound icon
        self.screen.blit(self.sound_icon, (self.x, 180))

        # back icon
        self.screen.blit(self.back_icon, (self.x, 300))

        # exit icon
        self.screen.blit(self.exit_icon, (self.x, 420))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  
                mouse_pos = event.pos
                sound_icon_rect = self.sound_icon.get_rect()
                back_icon_rect = self.back_icon.get_rect()
                exit_icon_rect = self.exit_icon.get_rect()

                sound_icon_rect.topleft = (self.x, 180)
                if sound_icon_rect.collidepoint(mouse_pos):
                    print("sound")
                    return
                
                back_icon_rect.topleft = (self.x, 300)
                if back_icon_rect.collidepoint(mouse_pos):
                    print("back")
                    return
                
                exit_icon_rect.topleft = (self.x, 420)
                if exit_icon_rect.collidepoint(mouse_pos):
                    print("exit")
                    pygame.quit()
                    sys.exit()

            pygame.display.flip()
            screen.fpsClock.tick(screen.fps)