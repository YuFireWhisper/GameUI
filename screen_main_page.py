import pygame
import sys

pygame.init()

class setupScreen:
    def __init__(self, screenInfo):
        # 主畫面
        self.screen_width = screenInfo.current_w
        self.screen_height = screenInfo.current_h
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

        self.background_image = pygame.image.load("public\\background.png").convert()
        self.background_image = pygame.transform.scale(self.background_image, (self.screen_width, self.screen_height))
        
        self.fps = 60
        self.fpsClock = pygame.time.Clock()

        # 開始按鈕
        self.start_button = pygame.image.load("public\\start_button.png").convert_alpha()
        self.start_button = pygame.transform.scale(self.start_button, (self.start_button.get_width() // 2, self.start_button.get_height() // 2))
        self.start_button_rect = self.start_button.get_rect()
        self.start_button_rect.topleft = (self.screen_width // 2 - self.start_button.get_width() // 2, self.screen_height // 2 - self.start_button.get_height() // 2 + 200)
        
        # 設定頁面
        self.setting_icon = pygame.image.load("public\\cogs.png").convert_alpha()
        self.setting_icon = pygame.transform.scale(self.setting_icon, (200, 200))
        self.setting_icon_rect = self.setting_icon.get_rect()
        self.setting_icon_rect.topleft = (self.screen_width - 200, 10)

    def quit(self):
        pygame.quit()
        sys.exit()