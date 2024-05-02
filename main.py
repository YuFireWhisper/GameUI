import json
import os
import sys
import tkinter as tk
from tkinter import filedialog
import pygame

class GamePage:
    def __init__(self, game_name, game_info):
        self.game_name = game_name
        self.back_icon = self.load_icon("back.png", size=(100, 100))
        self.score = 0
        self.game_info = game_info

    def load_icon(self, filename, size=None):
        icon = pygame.image.load(os.path.join("public", filename)).convert_alpha()
        if size:
            icon = pygame.transform.scale(icon, size)
        return icon

    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_pos = event.pos
                back_icon_rect = self.back_icon.get_rect(topleft=(10, 10))
                if back_icon_rect.collidepoint(mouse_pos):
                    self.save_score()
                    return "start"
        return None

    def save_score(self):
        game_data = self.game_info.get(self.game_name, {})
        game_data["high_score"] = max(game_data.get("high_score", 0), self.score)
        self.game_info[self.game_name] = game_data
        with open("game_info.json", "w") as f:
            json.dump(self.game_info, f)

    def draw(self, screen):
        screen.fill((255, 255, 255))
        screen.blit(self.back_icon, (10, 10))

class SetupScreen:
    def __init__(self, screen_info):
        self.font = pygame.font.SysFont(None, 36)
        self.screen_width = screen_info.current_w
        self.screen_height = screen_info.current_h
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.FULLSCREEN)
        self.load_assets()
        self.define_positions()

    def load_assets(self):
        self.background_image = self.load_image("background.png", (self.screen_width, self.screen_height))
        self.start_button = self.load_icon("start_button.png", size=(300, 300))
        self.setting_icon = self.load_icon("cogs.png", size=(200, 200))
        self.back_icon = self.load_icon("back.png", size=(50, 50))

    def load_image(self, filename, size=None):
        image = pygame.image.load(os.path.join("public", filename)).convert()
        if size:
            image = pygame.transform.scale(image, size)
        return image

    def load_icon(self, filename, size=None):
        icon = pygame.image.load(os.path.join("public", filename)).convert_alpha()
        if size:
            icon = pygame.transform.scale(icon, size)
        return icon

    def define_positions(self):
        self.setting_icon_rect = self.setting_icon.get_rect(topleft=(self.screen_width - 200, 10))
        self.start_button_rect = self.start_button.get_rect(
            topleft=(self.screen_width // 2 - self.start_button.get_width() // 2,
                     self.screen_height - self.screen_height // 4)
        )
        self.back_icon_rect = self.back_icon.get_rect(topleft=(10, 10))

    def draw(self):
        self.screen.fill((255, 255, 255))
        self.screen.blit(self.background_image, (0, 0))
        self.screen.blit(self.start_button, self.start_button_rect.topleft)
        self.screen.blit(self.setting_icon, self.setting_icon_rect.topleft)
        self.screen.blit(self.back_icon, self.back_icon_rect.topleft)

    def handle_events(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_pos = event.pos
                if self.start_button_rect.collidepoint(mouse_pos):
                    print("Start button clicked")
                    return "start"
                elif self.setting_icon_rect.collidepoint(mouse_pos):
                    return "setting"
                elif self.back_icon_rect.collidepoint(mouse_pos):
                    return "back"
        return None

class SettingScreenPage:
    def __init__(self, screen_info):
        self.screen_width = screen_info.current_w
        self.screen_height = screen_info.current_h
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.FULLSCREEN)
        self.load_assets()

    def load_assets(self):
        self.import_icon = self.load_icon("setting_import.png", size=(100, 100))
        self.back_icon = self.load_icon("back.png", size=(50, 50))
        self.exit_icon = self.load_icon("setting_exit.png", size=(100, 100))

    def load_icon(self, filename, size=None):
        icon = pygame.image.load(os.path.join("public", filename)).convert_alpha()
        if size:
            icon = pygame.transform.scale(icon, size)
        return icon

    def draw(self):
        self.screen.fill((255, 255, 255))
        x = self.screen_width // 2 - 100
        self.screen.blit(self.import_icon, (x, 180))
        self.screen.blit(self.back_icon, (50, 50))
        self.screen.blit(self.exit_icon, (x, 420))

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_pos = event.pos
                x = self.screen_width // 2 - 100
                import_icon_rect = self.import_icon.get_rect(topleft=(x, 180))
                back_icon_rect = self.back_icon.get_rect(topleft=(50, 50))
                exit_icon_rect = self.exit_icon.get_rect(topleft=(x, 420))

                if import_icon_rect.collidepoint(mouse_pos):
                    return "import"
                
                if back_icon_rect.collidepoint(mouse_pos):
                    return "back"
                
                if exit_icon_rect.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()
        pygame.display.update()
        return None

class ImportScreen:
    def __init__(self, screen_info):
        self.font = pygame.font.Font(os.path.join("font", "清松手寫體.ttf"), 36)
        self.screen_width = screen_info.current_w
        self.screen_height = screen_info.current_h
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.FULLSCREEN)
        self.load_assets()
        self.define_positions()

    def load_assets(self):
        self.game_name_label = self.font.render('遊戲名稱: ', True, (0, 0, 0))
        self.game_name_field = ""
        self.submit_button = self.font.render("提交", True, (0, 0, 0))
        self.game_file_path = ""
        self.game_picture_path = ""
        self.is_pinyin_input = True
        self.error_message = ""
        self.back_icon = self.load_icon("back.png", size=(50, 50))
        self.select_file_button = self.font.render("選擇檔案", True, (0, 0, 0))
        self.select_image_button = self.font.render("選擇圖片", True, (0, 0, 0))

    def load_icon(self, filename, size=None):
        icon = pygame.image.load(os.path.join("public", filename)).convert_alpha()
        if size:
            icon = pygame.transform.scale(icon, size)
        return icon

    def define_positions(self):
        self.submit_button_rect = self.submit_button.get_rect(topleft=(self.screen_width // 2, self.screen_height // 3 * 2))
        self.back_icon_rect = self.back_icon.get_rect(topleft=(10, 10))
        self.select_file_button_rect = self.select_file_button.get_rect(topleft=(self.screen_width // 2, self.screen_height // 3 * 2 + 100))
        self.select_image_button_rect = self.select_image_button.get_rect(topleft=(self.screen_width // 2, self.screen_height // 3 * 2 + 150))

    def draw(self):
        self.screen.fill((255, 255, 255))
        self.screen.blit(self.game_name_label, (self.screen_width // 2 - 100, self.screen_height // 3))
        pygame.draw.rect(self.screen, (0, 0, 0), pygame.Rect(self.screen_width // 2 - 20, self.screen_height // 3, 300, 50), 2)
        game_name_text_surface = self.font.render(self.game_name_field, True, (0, 0, 0))
        self.screen.blit(game_name_text_surface, (self.screen_width // 2, self.screen_height // 3 + 10))
        self.screen.blit(self.submit_button, self.submit_button_rect.topleft)
        self.screen.blit(self.back_icon, self.back_icon_rect.topleft)
        self.screen.blit(self.select_file_button, self.select_file_button_rect.topleft)
        self.screen.blit(self.select_image_button, self.select_image_button_rect.topleft)
        if self.error_message:
            error_text_surface = self.font.render(self.error_message, True, (255, 0, 0))
            self.screen.blit(error_text_surface, (self.screen_width // 2 - error_text_surface.get_width() // 2, 550))

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_pos = event.pos
                if self.submit_button_rect.collidepoint(mouse_pos):
                    if self.game_name_field and self.game_file_path and self.game_picture_path:
                        self.save_game_info()
                        return "submit"
                    else:
                        self.error_message = "請填寫完整資訊"
                elif self.back_icon_rect.collidepoint(mouse_pos):
                    return "back"
                elif self.select_file_button_rect.collidepoint(mouse_pos):
                    self.select_file()
                elif self.select_image_button_rect.collidepoint(mouse_pos):
                    self.select_image()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.game_name_field = self.game_name_field[:-1]
            elif event.key == pygame.K_RETURN:
                pass
            elif event.unicode.isalpha():
                self.game_name_field += event.unicode
        return None

    def save_game_info(self):
        try:
            with open("game_info.json", "r") as f:
                game_info = json.load(f)
        except FileNotFoundError:
            game_info = {}

        game_info[self.game_name_field] = {
            "game_name": self.game_name_field,
            "game_path": self.game_file_path,
            "game_image": self.game_picture_path
        }

        os.makedirs("public", exist_ok=True)  # 確保 public 目錄存在

        with open("game_info.json", "w") as f:
            json.dump(game_info, f)

    def select_file(self):
        file_path = filedialog.askopenfilename(title="選擇遊戲文件", filetypes=[("Python files", "*.py")])
        if file_path:
            self.game_file_path = file_path

    def select_image(self):
        file_path = filedialog.askopenfilename(title="選擇遊戲圖片", filetypes=[("Image files", "*.png *.jpg *.jpeg")])
        if file_path:
            self.game_picture_path = file_path
    
def main():
    pygame.init()
    screen_info = pygame.display.Info()

    try:
        with open("game_info.json", "r") as f:
            game_info = json.load(f)
    except FileNotFoundError:
        game_info = {}

    current_screen = "start"

    running = True
    setup_screen = SetupScreen(screen_info)
    setting_screen = SettingScreenPage(screen_info)
    import_screen = ImportScreen(screen_info)
    game_page = None
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

            if current_screen == "start":
                action = setup_screen.handle_events(event) 
                if action == "start":
                    current_screen = "start_page"
                    game_page = GamePage(list(game_info.keys())[0], game_info)
                elif action == "setting":
                    current_screen = "setting_screen"
            elif current_screen == "setting_screen":
                action = setting_screen.handle_event(event)  
                if action == "import":
                    current_screen = "import_screen"
                elif action == "back":
                    current_screen = "start"
            elif current_screen == "start_page":
                action = game_page.handle_events(event)
                if action:
                    current_screen = action
            elif current_screen == "import_screen":
                action = import_screen.handle_event(event)
                if action == "submit":
                    current_screen = "start"

        if running:
            if current_screen == "start":
                setup_screen.draw()
            elif current_screen == "setting_screen":
                setting_screen.draw()
            elif current_screen == "start_page":
                game_page.draw(setup_screen.screen)
            elif current_screen == "import_screen":
                import_screen.draw()

            pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
