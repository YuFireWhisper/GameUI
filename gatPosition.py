import pygame
import sys

# 初始化Pygame
pygame.init()

# 設置視窗大小
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Mouse Position")

# 定義顏色
WHITE = (255, 255, 255)

# 主迴圈
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 獲取滑鼠位置
    mouse_pos = pygame.mouse.get_pos()
    mouse_x, mouse_y = mouse_pos

    # 清除畫面
    screen.fill(WHITE)

    # 在視窗中顯示滑鼠位置
    font = pygame.font.Font(None, 36)
    text = font.render(f"Mouse Position: ({mouse_x}, {mouse_y})", True, (0, 0, 0))
    screen.blit(text, (10, 10))

    # 更新畫面
    pygame.display.flip()

# 退出Pygame
pygame.quit()
sys.exit()
