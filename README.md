# 贪吃蛇游戏

这是一个使用 Python 和 Pygame 开发的贪吃蛇游戏，包含主菜单、设置界面以及游戏主体功能。

## 安装依赖

在运行游戏之前，请确保已安装所需的依赖库。可以通过以下命令安装：

```bash
pip install -r requirements.txt
```
      
## 运行游戏

运行以下命令启动游戏：

```bash
python main.py
```
     
## 操作说明

### 主菜单
- 使用方向键上下选择菜单选项。
- 按回车键确认选择。
- 菜单选项包括：
  - **开始游戏**：进入游戏主体。
  - **设置**：调整游戏难度和音效。
  - **退出游戏**：退出程序。

### 游戏中
- 使用方向键控制蛇的移动方向。
- 按空格键暂停游戏。
- 按 ESC 键返回主菜单。

### 设置界面
- 使用方向键上下选择设置选项。
- 使用左右方向键调整设置：
  - **难度**：简单、中等、困难。
  - **音效**：开或关。
- 按回车键或 ESC 键返回主菜单。

## 功能

### 主菜单
- 动态标题动画。
- 显示最高分记录。
- 菜单选项带有悬停效果。

### 游戏设置
- 可调整游戏难度（简单、中等、困难）。
- 可开启或关闭音效。

### 游戏主体
- 贪吃蛇的基本玩法：
  - 蛇会随着移动逐渐增长。
  - 吃到食物得分，食物位置随机生成。
  - 撞到自身时游戏结束。
- 支持暂停功能，暂停时显示半透明覆盖层。
- 游戏结束后显示最终得分和最高记录。

### 音效
- 游戏包含以下音效（可选）：
  - 吃到食物时的音效。
  - 游戏结束时的音效。
  - 菜单选择时的音效。
- 如果音效文件加载失败，音效功能会自动关闭。

### 动画效果
- 主菜单标题带有浮动动画。
- 菜单选项带有动态悬停效果。

### 高分记录
- 游戏会自动保存最高分记录到 `highscore.txt` 文件中。

## 文件结构

- `main.py`：游戏的主程序。
- `requirements.txt`：依赖库列表。
- `highscore.txt`：保存最高分记录。
- `sounds/`：存放游戏音效文件（如 `eat.wav`, `game_over.wav`, `menu_select.wav`）。

## 注意事项

1. 确保系统中安装了 Pygame 库。
2. 如果使用 Windows 系统，请确保路径 `C:/Windows/Fonts/simhei.ttf` 存在黑体字体文件，否则会使用默认字体。
3. 如果音效文件缺失，游戏会自动禁用音效功能。

## 未来计划

- 增加更多游戏模式。
- 提供更丰富的设置选项。
- 优化游戏性能和界面设计。