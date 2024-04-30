import pygame
import sys
import os

from collections import OrderedDict

WHITE = (255, 255, 255)

gameInfo = OrderedDict()

gameInfo[0] = {
    "game_name": "AirWar",
    "game_path": r"E:\Program\Dev\Private_code\AirWar\main.py",
    "game_image" : "public\\Game_Picture\\Game_0.png",
    "game_description" : "public\\Game_description\\Game_description_0.png"
}

num_games = len(gameInfo)

class StartPage:
    def __init__(self, screenInfo):
        self.screen_width = screenInfo.current_w
        self.screen_height = screenInfo.current_h
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.FULLSCREEN)
        self.fps = 60
        self.fpsClock = pygame.time.Clock()

        self.go_button = pygame.image.load("public\\go_button.png")
        self.go_button = pygame.transform.scale(self.go_button, (self.go_button.get_width() // 2, self.go_button.get_height() // 2))
        self.go_button_rect = self.go_button.get_rect()

        self.current_game = 0

    def draw(self):
        self.screen.fill(WHITE)

        game_image = pygame.image.load(gameInfo[self.current_game]["game_image"])
        self.screen.blit(game_image, (self.screen_width // 2 - game_image.get_width() // 2, self.screen_height // 2 - game_image.get_height() // 2 - self.screen_height // 10.8))

        self.go_button_rect.topleft = (self.screen_width // 2 - self.go_button.get_width() // 2, self.screen_height // 2 - self.go_button.get_height() // 2 + self.screen_height // 3.6)
        self.screen.blit(self.go_button, self.go_button_rect.topleft)

        game_description = pygame.image.load(gameInfo[self.current_game]["game_description"])
        game_description = pygame.transform.scale(game_description, (game_description.get_width() // 2, game_description.get_height() // 2))
        self.screen.blit(game_description, (self.screen_width // 2 - game_description.get_width() // 2, self.screen_height // 2 - game_description.get_height() // 2 - self.screen_height // 2.5))
        
    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.go_button_rect.collidepoint(event.pos):
                os.system("python " + gameInfo[self.current_game]["game_path"])