import json
import tkinter as tk
from tkinter import filedialog
import pygame
import sys
import os

# Global font variable
font = None

# Game base class
class GamePage:
    def __init__(self, game_name):
        self.game_name = game_name
        self.back_icon = pygame.image.load("public\\setting_back.png").convert_alpha()
        self.back_icon = pygame.transform.scale(self.back_icon, (self.back_icon.get_width() // 2, self.back_icon.get_height() // 2))
        self.score = 0

    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_pos = event.pos
                back_icon_rect = self.back_icon.get_rect(topleft=(10, 10))
                if back_icon_rect.collidepoint(mouse_pos):
                    self.save_score()
                    return "main"
        return None

    def save_score(self):
        try:
            with open("game_info.json", "r") as f:
                game_info = json.load(f)
        except FileNotFoundError:
            game_info = {}

        if self.game_name in game_info:
            game_data = game_info[self.game_name]
            if "high_score" not in game_data:
                game_data["high_score"] = self.score
            else:
                game_data["high_score"] = max(game_data["high_score"], self.score)
        else:
            game_info[self.game_name] = {"high_score": self.score}

        with open("game_info.json", "w") as f:
            json.dump(game_info, f)

    def draw(self, screen):
        screen.blit(self.back_icon, (10, 10))

# Main page setup
class SetupScreen:
    def __init__(self, screenInfo):
        global font
        font = pygame.font.SysFont(None, 36)
        
        self.screen_width = screenInfo.current_w
        self.screen_height = screenInfo.current_h
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

        self.background_image = pygame.image.load("public\\background.png").convert()
        self.background_image = pygame.transform.scale(self.background_image, (self.screen_width, self.screen_height))
        
        self.fps = 60
        self.fpsClock = pygame.time.Clock()

        # Start button
        self.start_button = pygame.image.load("public\\start_button.png").convert_alpha()
        self.start_button = pygame.transform.scale(self.start_button, (self.start_button.get_width() // 2, self.start_button.get_height() // 2))
        self.start_button_rect = self.start_button.get_rect()
        self.start_button_rect.topleft = (self.screen_width // 2 - self.start_button.get_width() // 2, self.screen_height - self.screen_height // 4)
        
        # Setting page
        self.setting_icon = pygame.image.load("public\\cogs.png").convert_alpha()
        self.setting_icon = pygame.transform.scale(self.setting_icon, (200, 200))
        self.setting_icon_rect = self.setting_icon.get_rect()
        self.setting_icon_rect.topleft = (self.screen_width - 200, 10)

    def draw(self):
        self.screen.blit(self.background_image, (0, 0))
        self.screen.blit(self.start_button, self.start_button_rect.topleft)
        self.screen.blit(self.setting_icon, self.setting_icon_rect.topleft)

    def quit(self):
        pygame.quit()
        sys.exit()

    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_pos = event.pos
                if self.start_button_rect.collidepoint(mouse_pos):  # 這裡修改
                    return "start"
                elif self.setting_icon_rect.collidepoint(mouse_pos):
                    return "setting"
        return None


class SettingScreenPage:
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)

    def __init__(self, screenInfo):
        self.screen_width = screenInfo.current_w
        self.screen_height = screenInfo.current_h
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.screen.fill(SettingScreenPage.WHITE)
        self.fpsClock = pygame.time.Clock()  # Add this line for fpsClock
        
        # Import icon
        self.import_icon = pygame.image.load("public\\setting_import.png").convert_alpha()
        self.import_icon = pygame.transform.scale(self.import_icon, (self.import_icon.get_width() // 2, self.import_icon.get_height() // 2))

        # Back icon
        self.back_icon = pygame.image.load("public\\setting_back.png").convert_alpha()
        self.back_icon = pygame.transform.scale(self.back_icon, (self.back_icon.get_width() // 2, self.back_icon.get_height() // 2))

        # Exit icon
        self.exit_icon = pygame.image.load("public\\setting_exit.png").convert_alpha()
        self.exit_icon = pygame.transform.scale(self.exit_icon, (self.exit_icon.get_width() // 2, self.exit_icon.get_height() // 2))
    
    def draw(self):
        self.screen.fill(SettingScreenPage.WHITE)

        self.x = self.screen_width // 2 - 100

        # Import icon
        self.screen.blit(self.import_icon, (self.x, 180))

        # Back icon
        self.screen.blit(self.back_icon, (self.x, 300))

        # Exit icon
        self.screen.blit(self.exit_icon, (self.x, 420))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  
                mouse_pos = event.pos
                import_icon_rect = self.import_icon.get_rect()
                back_icon_rect = self.back_icon.get_rect()
                exit_icon_rect = self.exit_icon.get_rect()

                import_icon_rect.topleft = (self.x, 180)
                if import_icon_rect.collidepoint(mouse_pos):
                    print("import")
                    global current_screen
                    current_screen = "import"
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
            self.fpsClock.tick(self.fps)

# Start page
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
        self.go_button_rect.topleft = (self.screen_width // 2 - self.go_button.get_width() // 2, self.screen_height - self.screen_height // 4)
        self.current_game = next(iter(gameInfo)) if gameInfo else ""

        self.game_info = load_game_info()

    def draw(self, game_info):
        self.screen.fill((255, 255, 255))

        # Check if current_game is empty
        if self.current_game:
            game_name_font = pygame.font.Font("font\\mexcellent.otf", 36)
            game_name_text = game_name_font.render(gameInfo[self.current_game]["game_name"], True, (0, 0, 0))
            self.screen.blit(game_name_text, (50, 50))

            # Display game name
            game_name_font = pygame.font.Font("font\\mexcellent.otf", 36)
            game_name_text = game_name_font.render(gameInfo[self.current_game]["game_name"], True, (0, 0, 0))
            self.screen.blit(game_name_text, (self.screen_width // 2 - game_name_text.get_width() // 2, 50))

            # Display high score
            high_score = game_info.get(gameInfo[self.current_game]["game_name"], {}).get("high_score", 0)
            score_text = font.render(f"最高分數: {high_score}", True, (0, 0, 0))
            self.screen.blit(score_text, (self.screen_width - 200, 50))

            # Display game picture
            game_picture = pygame.image.load("public\\" + gameInfo[self.current_game]["game_image"])
            game_picture = pygame.transform.scale(game_picture, (game_picture.get_width() // 2, game_picture.get_height() // 2))
            self.screen.blit(game_picture, (self.screen_width // 2 - game_picture.get_width() // 2, 300))
            
            # Display go_button
            self.screen.blit(self.go_button, self.go_button_rect.topleft)

        else:
            # Display a message indicating no game selected
            no_game_selected_text = font.render("No game selected", True, (0, 0, 0))
            text_rect = no_game_selected_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2))
            self.screen.blit(no_game_selected_text, text_rect)

    def draw_not_game_prompt(self):
        self.screen.fill((255, 255, 255))  # 清空屏幕
        prompt_font = pygame.font.SysFont(None, 48)  # 设置字体
        prompt_text = prompt_font.render("Not Game", True, (255, 0, 0))  # 渲染文本
        text_rect = prompt_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2))  # 获取文本矩形
        self.screen.blit(prompt_text, text_rect)  # 绘制文本

    def handle_events(self, event, game_info):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.go_button_rect.collidepoint(event.pos):
                if len(gameInfo) > 0:  # 检查游戏信息是否为空
                    os.system("python " + gameInfo[self.current_game]["game_path"])
                else:
                    self.draw_not_game_prompt()  # 调用提示框方法
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                self.current_game = (self.current_game + 1) % num_games
            elif event.key == pygame.K_LEFT:
                self.current_game = (self.current_game - 1) % num_games

class ImportScreen:
    def __init__(self, screenInfo):
        global font, num_games
        font = pygame.font.Font("font\\清松手寫體.ttf", 36)
        num_games = len(gameInfo)

        self.screen_width = screenInfo.current_w
        self.screen_height = screenInfo.current_h
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.screen.fill((255, 255, 255))

        self.game_name_label = font.render('遊戲名稱: ', True, (0, 0, 0))
        self.game_name_label_rect = self.game_name_label.get_rect(center=(self.screen_width // 2 - 100, self.screen_height // 3))

        self.game_name_field = ""

        self.submit_button = font.render("提交", True, (0, 0, 0))
        self.submit_button_rect = self.submit_button.get_rect(center=(self.screen_width // 2, self.screen_height // 3 * 2))

        self.game_file_path = ""
        self.game_picture_path = ""

        self.is_pinyin_input = True

        self.font = pygame.font.Font(None, 24)
        self.error_message = ""

        # Back icon
        self.back_icon = pygame.image.load("public\\setting_back.png").convert_alpha()
        self.back_icon = pygame.transform.scale(self.back_icon, (self.back_icon.get_width() // 2, self.back_icon.get_height() // 2))
        self.back_icon_rect = self.back_icon.get_rect(topleft=(10, 10))

        # 選擇遊戲檔案按鈕
        self.select_file_button = font.render("選擇檔案", True, (0, 0, 0))
        self.select_file_button_rect = self.select_file_button.get_rect(center=(self.screen_width // 2, self.screen_height // 3 * 2 + 100))

        # 選擇遊戲圖片按鈕
        self.select_image_button = font.render("選擇圖片", True, (0, 0, 0))
        self.select_image_button_rect = self.select_image_button.get_rect(center=(self.screen_width // 2, self.screen_height // 3 * 2 + 150))

    def render_error_message(self):
        error_text = self.font.render(self.error_message, True, (255, 0, 0))
        error_text_rect = error_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2))
        self.screen.blit(error_text, error_text_rect)

    def draw(self):
        self.screen.fill((255, 255, 255))

        self.screen.blit(self.back_icon, self.back_icon_rect.topleft)

        self.screen.blit(self.game_name_label, self.game_name_label_rect)
        pygame.draw.rect(self.screen, (0, 0, 0), (self.screen_width // 2 - 100, self.screen_height // 3 + 20, 200, 50), 2)

        game_name_text = font.render(self.game_name_field, True, (0, 0, 0))
        game_name_text_rect = game_name_text.get_rect(center=(self.screen_width // 2 + 100, self.screen_height // 3 + 45))
        self.screen.blit(game_name_text, game_name_text_rect)

        self.screen.blit(self.submit_button, self.submit_button_rect)

        self.render_error_message()

        self.screen.blit(self.select_file_button, self.select_file_button_rect.topleft)
        self.screen.blit(self.select_image_button, self.select_image_button_rect.topleft)


    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_pos = event.pos
                if self.submit_button_rect.collidepoint(mouse_pos):
                    return self.submit_game()  # 返回提交游戏的结果
                elif self.back_icon_rect.collidepoint(mouse_pos):
                    return "main"  # 返回主界面
                elif self.select_file_button_rect.collidepoint(mouse_pos):
                    self.select_game_file()
                elif self.select_image_button_rect.collidepoint(mouse_pos):
                    self.select_game_picture()
        elif event.type == pygame.KEYDOWN:
            self.handle_keyboard_input(event)

    def select_game_file(self):
        root = tk.Tk()
        root.withdraw()
        self.game_file_path = filedialog.askopenfilename()

    def select_game_picture(self):
        root = tk.Tk()
        root.withdraw()
        self.game_picture_path = filedialog.askopenfilename()

    def handle_keyboard_input(self, event):
        if event.key == pygame.K_BACKSPACE:
            self.game_name_field = self.game_name_field[:-1]
        elif event.key == pygame.K_RETURN:
            self.submit_game()
        elif event.unicode.isalnum() or event.key == pygame.K_SPACE:
            self.game_name_field += event.unicode

    def submit_game(self):
        if not self.game_name_field:
            self.error_message = "請輸入遊戲名稱"
            return

        if not self.game_file_path:
            self.error_message = "請選擇遊戲文件"
            return

        if not self.game_picture_path:
            self.error_message = "請選擇遊戲圖片"
            return

        try:
            with open("game_info.json", "r") as f:
                game_info = json.load(f)
        except FileNotFoundError:
            game_info = {}

        game_info[self.game_name_field] = {"game_name": self.game_name_field, "game_path": self.game_file_path, "picture_path": self.game_picture_path}

        with open("game_info.json", "w") as f:
            json.dump(game_info, f)

        return "main"

# Load game info
def load_game_info():
    try:
        with open("game_info.json", "r") as f:
            game_info = json.load(f)
    except FileNotFoundError:
        game_info = {}
    return game_info

# Main loop
if __name__ == "__main__":
    pygame.init()

    gameInfo = load_game_info()

    screenInfo = pygame.display.Info()
    current_screen = "main"

    setupScreen = SetupScreen(screenInfo)
    settingScreen = SettingScreenPage(screenInfo)
    importScreen = ImportScreen(screenInfo)
    startPage = StartPage(screenInfo)

    while True:
        if current_screen == "main":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mouse_pos = event.pos
                        if setupScreen.setting_icon_rect.collidepoint(mouse_pos):
                            current_screen = "setting"
                        elif setupScreen.start_button_rect.collidepoint(mouse_pos):
                            current_screen = "start"
                            startPage.current_game = next(iter(gameInfo)) if gameInfo else ""
                            startPage.game_info = load_game_info()

            setupScreen.screen.blit(setupScreen.background_image, (0, 0))
            setupScreen.screen.blit(setupScreen.setting_icon, setupScreen.setting_icon_rect.topleft)
            setupScreen.screen.blit(setupScreen.start_button, setupScreen.start_button_rect.topleft)
            pygame.display.flip()
            setupScreen.fpsClock.tick(setupScreen.fps)
        elif current_screen == "setting":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        return_value = settingScreen.handle_event(event)
                        if return_value == "import":
                            current_screen = "import"
                        elif return_value == "back":
                            current_screen = "main"

            settingScreen.draw()
            pygame.display.flip()
            settingScreen.fpsClock.tick(settingScreen.fps)
        elif current_screen == "import":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        return_value = importScreen.handle_events(event)
                        if return_value == "main":
                            current_screen = "main"

            importScreen.draw()
            pygame.display.flip()
            importScreen.fpsClock.tick(importScreen.fps)
        elif current_screen == "start":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    else:
                        startPage.handle_events(event, startPage.game_info)

            startPage.screen.blit(startPage.go_button, startPage.go_button_rect.topleft)
            startPage.draw(startPage.game_info)
            pygame.display.flip()
            startPage.fpsClock.tick(startPage.fps)
