# -*- coding: utf-8 -*-
import pygame
import sys
import os
import sys
import math
import random
import time
import os

# 初始化Pygame
pygame.init()
pygame.mixer.init()  # 初始化音频系统

# 设置窗口
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("贪吃蛇")

# 颜色定义
BACKGROUND_COLOR = (0, 0, 51)  # 深蓝色
WHITE = (255, 255, 255)  # 白色
YELLOW = (255, 255, 0)  # 黄色
GRAY = (128, 128, 128)  # 灰色
GREEN = (0, 255, 0)  # 绿色

# 状态常量
MAIN_MENU = 0
SETTINGS = 1
GAME = 2
GAME_OVER = 3
GAME_PAUSED = 4
current_state = MAIN_MENU  # 初始状态为主菜单

# 游戏设置
difficulty = 2    # 默认难度（1-3）
sound_enabled = True  # 音效开关
music_enabled = True  # 背景音乐开关
music_enabled = True  # 背景音乐开关

# 高分记录
def load_highscore():
    try:
        with open('highscore.txt', 'r') as f:
            return int(f.read().strip())
    except:
        return 0

def save_highscore(score):
    with open('highscore.txt', 'w') as f:
        f.write(str(score))

highscore = load_highscore()  # 加载最高分

def resource_path(relative_path):
    """获取打包后资源的绝对路径"""
    try:
        # PyInstaller创建的临时文件夹
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# 加载音效
sounds = {
    'eat': None,
    'game_over': None,
    'menu_select': None,
    'background_music': None
}

try:
    # 尝试加载音效文件
    sounds['eat'] = pygame.mixer.Sound(resource_path('sounds/eat.wav'))
    sounds['game_over'] = pygame.mixer.Sound(resource_path('sounds/game_over.wav'))
    sounds['menu_select'] = pygame.mixer.Sound(resource_path('sounds/menu_select.wav'))
    sounds['background_music'] = pygame.mixer.Sound(resource_path('sounds/background_music.wav'))
except Exception as e:
    print(f"无法加载音效文件: {e}")
    sound_enabled = False  # 如果加载失败，关闭音效
    music_enabled = False  # 如果加载失败，关闭背景音乐

# 背景音乐控制函数
def play_background_music():
    if music_enabled and sounds['background_music']:
        sounds['background_music'].stop()  # 先停止，防止重叠播放
        sounds['background_music'].play(-1)  # -1表示循环播放

def stop_background_music():
    if sounds['background_music']:
        sounds['background_music'].stop()

# 字体设置
try:
    # 尝试加载中文字体
    FONT_PATH = "C:/Windows/Fonts/simhei.ttf"  # Windows 系统自带黑体
    title_font = pygame.font.Font(FONT_PATH, 74)
    menu_font = pygame.font.Font(FONT_PATH, 50)
    settings_font = pygame.font.Font(FONT_PATH, 40)
except:
    # 如果加载失败，使用默认字体
    title_font = pygame.font.Font(None, 74)
    menu_font = pygame.font.Font(None, 50)
    settings_font = pygame.font.Font(None, 40)

# 菜单选项
main_menu_items = ["开始游戏", "设置", "退出游戏"]
settings_menu_items = ["难度: 简单", "音效: 开", "背景音乐: 开", "返回"]
selected_main_item = 0
selected_settings_item = 0

# 动画变量
animation_time = 0

# 游戏常量
GRID_SIZE = 20
GRID_WIDTH = WINDOW_WIDTH // GRID_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // GRID_SIZE
game_speed = [10, 15, 20]  # 不同难度对应的速度

# 蛇类
class Snake:
    def __init__(self):
        self.reset()
        
    def reset(self):
        self.length = 3
        self.positions = [(GRID_WIDTH//2, GRID_HEIGHT//2)]
        self.direction = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])
        self.score = 0
        
    def get_head_position(self):
        return self.positions[0]
    
    def move(self):
        head = self.get_head_position()
        x, y = self.direction
        new_head = ((head[0] + x) % GRID_WIDTH, (head[1] + y) % GRID_HEIGHT)
        
        if new_head in self.positions[1:]:
            return False  # 游戏结束
            
        self.positions.insert(0, new_head)
        if len(self.positions) > self.length:
            self.positions.pop()
        return True
    
    def grow(self):
        self.length += 1
        self.score += 1
        
    def draw(self, surface):
        for i, p in enumerate(self.positions):
            color = GREEN if i == 0 else WHITE  # 头部绿色，身体白色
            rect = pygame.Rect((p[0] * GRID_SIZE, p[1] * GRID_SIZE), (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, color, rect)
            pygame.draw.rect(surface, BACKGROUND_COLOR, rect, 1)

# 食物类
class Food:
    def __init__(self):
        self.position = (0, 0)
        self.randomize_position()
        
    def randomize_position(self):
        self.position = (random.randint(0, GRID_WIDTH-1), random.randint(0, GRID_HEIGHT-1))
        
    def draw(self, surface):
        rect = pygame.Rect((self.position[0] * GRID_SIZE, self.position[1] * GRID_SIZE), (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, YELLOW, rect)
        pygame.draw.rect(surface, BACKGROUND_COLOR, rect, 1)

# 绘制函数
def draw_main_menu():
    global animation_time
    screen.fill(BACKGROUND_COLOR)
    
    # 更新动画时间
    animation_time += 0.005  # 减小增量值，动画变慢
    
    # 绘制标题（带有浮动动画）
    title_y = 100 + math.sin(animation_time) * 8  # 可同时调整振幅（8像素）
    title_text = title_font.render("贪吃蛇", True, WHITE)
    title_rect = title_text.get_rect(center=(WINDOW_WIDTH/2, title_y))
    screen.blit(title_text, title_rect)
    
    # 绘制最高分
    highscore_text = settings_font.render(f"最高记录: {highscore}", True, YELLOW)
    highscore_rect = highscore_text.get_rect(center=(WINDOW_WIDTH/2, 180))
    screen.blit(highscore_text, highscore_rect)
    
    # 绘制菜单选项（带有悬停效果）
    for i, item in enumerate(main_menu_items):
        if i == selected_main_item:
            # 选中项：黄色文字，带背景框
            color = YELLOW
            bg_rect = pygame.Rect(0, 0, 300, 60)
            bg_rect.center = (WINDOW_WIDTH/2, 250 + i * 70)
            pygame.draw.rect(screen, (50, 50, 100), bg_rect, border_radius=10)
            pygame.draw.rect(screen, GREEN, bg_rect, 2, border_radius=10)
        else:
            color = GRAY
            
        text = menu_font.render(item, True, color)
        rect = text.get_rect(center=(WINDOW_WIDTH/2, 250 + i * 70))
        screen.blit(text, rect)
    
    # 绘制操作提示
    hint_text = settings_font.render("使用方向键选择，回车键确认", True, WHITE)
    hint_rect = hint_text.get_rect(center=(WINDOW_WIDTH/2, 500))
    screen.blit(hint_text, hint_rect)
    
    pygame.display.flip()

def draw_settings_menu():
    screen.fill(BACKGROUND_COLOR)
    
    # 绘制标题
    title_text = title_font.render("设置", True, WHITE)
    title_rect = title_text.get_rect(center=(WINDOW_WIDTH/2, 100))
    screen.blit(title_text, title_rect)
    
    # 更新设置选项文本
    difficulty_text = ""
    if difficulty == 1:
        difficulty_text = "难度: 简单"
    elif difficulty == 2:
        difficulty_text = "难度: 中等"
    else:
        difficulty_text = "难度: 困难"
    
    sound_text = "音效: 开" if sound_enabled else "音效: 关"
    music_text = "背景音乐: 开" if music_enabled else "背景音乐: 关"
    
    settings_menu_items[0] = difficulty_text
    settings_menu_items[1] = sound_text
    settings_menu_items[2] = music_text
    
    # 绘制设置选项
    for i, item in enumerate(settings_menu_items):
        color = YELLOW if i == selected_settings_item else GRAY
        text = settings_font.render(item, True, color)
        rect = text.get_rect(center=(WINDOW_WIDTH/2, 250 + i * 70))
        screen.blit(text, rect)
    
    # 绘制操作提示
    hint_text = settings_font.render("使用左右键修改设置，上下键选择选项", True, WHITE)
    hint_rect = hint_text.get_rect(center=(WINDOW_WIDTH/2, 500))
    screen.blit(hint_text, hint_rect)
    
    pygame.display.flip()

def draw_game(snake, food):
    screen.fill(BACKGROUND_COLOR)
    
    # 绘制网格线
    for x in range(0, WINDOW_WIDTH, GRID_SIZE):
        pygame.draw.line(screen, (30, 30, 80), (x, 0), (x, WINDOW_HEIGHT))
    for y in range(0, WINDOW_HEIGHT, GRID_SIZE):
        pygame.draw.line(screen, (30, 30, 80), (0, y), (WINDOW_WIDTH, y))
    
    # 绘制蛇和食物
    snake.draw(screen)
    food.draw(screen)
    
    # 绘制分数
    score_text = settings_font.render(f"分数: {snake.score}", True, WHITE)
    screen.blit(score_text, (10, 10))
    
    pygame.display.flip()

def draw_pause_menu(snake, food):
    # 创建静态暂停画面（只在进入暂停时调用一次）
    pause_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
    
    # 1. 绘制游戏画面
    draw_game(snake, food)
    
    # 2. 添加半透明覆盖层 (50%透明度)
    overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 128))
    pause_surface.blit(overlay, (0, 0))
    
    # 3. 绘制暂停菜单文字
    pause_text = title_font.render("游戏暂停", True, WHITE)
    pause_rect = pause_text.get_rect(center=(WINDOW_WIDTH/2, 200))
    pause_surface.blit(pause_text, pause_rect)
    
    hint_text = menu_font.render("按空格键继续游戏", True, YELLOW)
    hint_rect = hint_text.get_rect(center=(WINDOW_WIDTH/2, 300))
    pause_surface.blit(hint_text, hint_rect)
    
    hint_text2 = menu_font.render("按 ESC 返回主菜单", True, WHITE)
    hint_rect2 = hint_text2.get_rect(center=(WINDOW_WIDTH/2, 350))
    pause_surface.blit(hint_text2, hint_rect2)
    
    return pause_surface
def draw_pause_menu(snake, food):
    # 先绘制当前游戏画面作为背景
    draw_game(snake, food)
    
    # 创建半透明覆盖层
    overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 100))  # 更透明的遮罩
    screen.blit(overlay, (0, 0))
    
    # 绘制暂停菜单文字
    pause_text = title_font.render("游戏暂停", True, WHITE)
    pause_rect = pause_text.get_rect(center=(WINDOW_WIDTH/2, 200))
    screen.blit(pause_text, pause_rect)
    
    hint_text = menu_font.render("按 P 继续游戏", True, YELLOW)
    hint_rect = hint_text.get_rect(center=(WINDOW_WIDTH/2, 300))
    screen.blit(hint_text, hint_rect)
    
    hint_text2 = menu_font.render("按 ESC 返回主菜单", True, WHITE)
    hint_rect2 = hint_text2.get_rect(center=(WINDOW_WIDTH/2, 350))
    screen.blit(hint_text2, hint_rect2)
    
    pygame.display.flip()

def draw_game_over(snake):
    global highscore
    screen.fill(BACKGROUND_COLOR)
    
    # 检查是否创造新的最高分
    if snake.score > highscore:
        highscore = snake.score
        save_highscore(highscore)
        # 显示新纪录提示
        new_record_text = title_font.render("新纪录！", True, (255, 215, 0))  # 金色
        new_record_rect = new_record_text.get_rect(center=(WINDOW_WIDTH/2, 100))
        screen.blit(new_record_text, new_record_rect)
    
    # 绘制游戏结束标题
    title_text = title_font.render("游戏结束", True, (255, 0, 0))  # 红色
    title_rect = title_text.get_rect(center=(WINDOW_WIDTH/2, 150))
    screen.blit(title_text, title_rect)
    
    # 绘制最终得分
    score_text = menu_font.render(f"最终得分: {snake.score}", True, WHITE)
    score_rect = score_text.get_rect(center=(WINDOW_WIDTH/2, 220))
    screen.blit(score_text, score_rect)
    
    # 绘制最高分
    highscore_text = menu_font.render(f"最高记录: {highscore}", True, YELLOW)
    highscore_rect = highscore_text.get_rect(center=(WINDOW_WIDTH/2, 270))
    screen.blit(highscore_text, highscore_rect)
    
    # 绘制选项
    options = ["重新开始", "返回主菜单"]
    for i, option in enumerate(options):
        color = YELLOW if i == selected_main_item else GRAY
        text = menu_font.render(option, True, color)
        rect = text.get_rect(center=(WINDOW_WIDTH/2, 350 + i * 70))
        screen.blit(text, rect)
    
    # 绘制操作提示
    hint_text = settings_font.render("使用方向键选择，回车键确认", True, WHITE)
    hint_rect = hint_text.get_rect(center=(WINDOW_WIDTH/2, 500))
    screen.blit(hint_text, hint_rect)
    
    pygame.display.flip()

# 游戏主函数
def start_game():
    global current_state, selected_main_item
    current_state = GAME
    selected_main_item = 0  # 重置选择
    
    # 播放背景音乐
    play_background_music()
    
    snake = Snake()
    food = Food()
    clock = pygame.time.Clock()
    pause_surface = None  # 初始化暂停画面
    
    running = True
    while running:
        # 处理输入
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                current_state = MAIN_MENU
                return
                
            if event.type == pygame.KEYDOWN:
                if current_state == GAME:
                    if event.key == pygame.K_UP and snake.direction != (0, 1):
                        snake.direction = (0, -1)
                    elif event.key == pygame.K_DOWN and snake.direction != (0, -1):
                        snake.direction = (0, 1)
                    elif event.key == pygame.K_LEFT and snake.direction != (1, 0):
                        snake.direction = (-1, 0)
                    elif event.key == pygame.K_RIGHT and snake.direction != (-1, 0):
                        snake.direction = (1, 0)
                    elif event.key == pygame.K_SPACE:  # 空格键暂停游戏
                        current_state = GAME_PAUSED
                        pause_surface = draw_pause_menu(snake, food)  # 创建静态暂停画面
                    elif event.key == pygame.K_ESCAPE:
                        current_state = MAIN_MENU
                        stop_background_music()  # 停止背景音乐
                        return
                        
                elif current_state == GAME_PAUSED:
                    if event.key == pygame.K_SPACE:  # 空格键继续游戏
                        current_state = GAME
                    elif event.key == pygame.K_ESCAPE:
                        current_state = MAIN_MENU
                        return
                        
                elif current_state == GAME_OVER:
                    if event.key == pygame.K_UP:
                        selected_main_item = (selected_main_item - 1) % 2
                    elif event.key == pygame.K_DOWN:
                        selected_main_item = (selected_main_item + 1) % 2
                    elif event.key == pygame.K_RETURN:
                        if selected_main_item == 0:  # 重新开始
                            current_state = GAME
                            snake = Snake()
                            food = Food()
                        else:  # 返回主菜单
                            current_state = MAIN_MENU
                            stop_background_music()  # 停止背景音乐
                            return
                    elif event.key == pygame.K_ESCAPE:
                        current_state = MAIN_MENU
                        stop_background_music()  # 停止背景音乐
                        return
        
        # 游戏逻辑
        if current_state == GAME:
            # 移动蛇
            if not snake.move():
                current_state = GAME_OVER  # 切换到游戏结束状态
                stop_background_music()  # 停止背景音乐
                if sound_enabled and sounds['game_over']:
                    sounds['game_over'].play()
                
            # 检查是否吃到食物
            if snake.get_head_position() == food.position:
                snake.grow()
                if sound_enabled and sounds['eat']:
                    sounds['eat'].play()
                food.randomize_position()
                while food.position in snake.positions:  # 确保食物不会出现在蛇身上
                    food.randomize_position()
            
            # 绘制游戏画面
            draw_game(snake, food)
        
        elif current_state == GAME_PAUSED:
            if pause_surface:
                screen.blit(pause_surface, (0, 0))
                pygame.display.flip()
            
        elif current_state == GAME_OVER:
            draw_game_over(snake)
        
        # 控制游戏速度
        if current_state == GAME:
            clock.tick(game_speed[difficulty-1])  # 根据难度设置速度
        else:
            clock.tick(30)  # 菜单界面使用较低帧率

# 主游戏循环
def main():
    global current_state, selected_main_item, selected_settings_item, sound_enabled, difficulty
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            if event.type == pygame.KEYDOWN:
                if current_state == MAIN_MENU:
                    if event.key == pygame.K_UP:
                        selected_main_item = (selected_main_item - 1) % len(main_menu_items)
                    elif event.key == pygame.K_DOWN:
                        selected_main_item = (selected_main_item + 1) % len(main_menu_items)
                    elif event.key == pygame.K_RETURN:
                        if sound_enabled and sounds['menu_select']:
                            sounds['menu_select'].play()
                        if selected_main_item == 0:  # 开始游戏
                            start_game()
                        elif selected_main_item == 1:  # 设置
                            current_state = SETTINGS
                        elif selected_main_item == 2:  # 退出
                            running = False
                
                elif current_state == SETTINGS:
                    if event.key == pygame.K_UP:
                        selected_settings_item = (selected_settings_item - 1) % len(settings_menu_items)
                    elif event.key == pygame.K_DOWN:
                        selected_settings_item = (selected_settings_item + 1) % len(settings_menu_items)
                    elif event.key == pygame.K_LEFT:
                        if sound_enabled and sounds['menu_select']:
                            sounds['menu_select'].play()
                        if selected_settings_item == 0:  # 难度
                            difficulty = max(1, difficulty - 1)
                        elif selected_settings_item == 1:  # 音效
                            sound_enabled = not sound_enabled
                        elif selected_settings_item == 2:  # 背景音乐
                            global music_enabled
                            music_enabled = not music_enabled
                            if music_enabled:
                                play_background_music()
                            else:
                                stop_background_music()
                    elif event.key == pygame.K_RIGHT:
                        if sound_enabled and sounds['menu_select']:
                            sounds['menu_select'].play()
                        if selected_settings_item == 0:  # 难度
                            difficulty = min(3, difficulty + 1)
                        elif selected_settings_item == 1:  # 音效
                            sound_enabled = not sound_enabled
                        elif selected_settings_item == 2:  # 背景音乐
                            music_enabled = not music_enabled
                            if music_enabled:
                                play_background_music()
                            else:
                                stop_background_music()
                    elif event.key == pygame.K_RETURN or event.key == pygame.K_ESCAPE:
                        if selected_settings_item == 2 or event.key == pygame.K_ESCAPE:  # 返回
                            current_state = MAIN_MENU
        
        # 根据当前状态绘制界面
        if current_state == MAIN_MENU:
            draw_main_menu()
        elif current_state == SETTINGS:
            draw_settings_menu()
        
        # 控制菜单帧率
        pygame.time.Clock().tick(30)

# 启动游戏
if __name__ == "__main__":
    main()
    pygame.quit()
    sys.exit()