import numpy as np
from scipy.io import wavfile
import os

# 确保sounds目录存在
if not os.path.exists('sounds'):
    os.makedirs('sounds')

# 生成正弦波音效
def generate_tone(frequency=440, duration=0.5, volume=0.5, sample_rate=44100):
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    tone = np.sin(2 * np.pi * frequency * t) * volume * 32767
    return tone.astype(np.int16)

# 1. 生成吃食物音效 (短促的高频音)
eat_tone = np.concatenate([
    generate_tone(1000, 0.1, 0.3),
    generate_tone(1200, 0.05, 0.3)
])
wavfile.write('sounds/eat.wav', 44100, eat_tone)

# 2. 生成游戏结束音效 (低频下降音)
game_over_tone = np.array([], dtype=np.int16)
for freq in range(800, 300, -50):
    game_over_tone = np.concatenate([
        game_over_tone,
        generate_tone(freq, 0.05, 0.4)
    ])
wavfile.write('sounds/game_over.wav', 44100, game_over_tone)

# 3. 生成菜单选择音效 (中频双音)
menu_tone = np.concatenate([
    generate_tone(800, 0.1, 0.3),
    np.zeros(2205, dtype=np.int16),  # 50ms静音
    generate_tone(1000, 0.1, 0.3)
])
wavfile.write('sounds/menu_select.wav', 44100, menu_tone)

print("已生成3个音效文件到sounds目录")