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

# 生成和弦
def generate_chord(frequencies, duration=0.5, volume=0.5, sample_rate=44100):
    chord = np.zeros(int(sample_rate * duration), dtype=np.int16)
    for freq in frequencies:
        chord += generate_tone(freq, duration, volume / len(frequencies), sample_rate)
    return chord

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

# 4. 生成背景音乐 (简单的循环旋律)
# 使用简单的音阶和和弦创建一个循环的背景音乐
background_music = np.array([], dtype=np.int16)

# 定义一些简单的音符频率 (C大调音阶)
C4 = 261.63
D4 = 293.66
E4 = 329.63
F4 = 349.23
G4 = 392.00
A4 = 440.00
B4 = 493.88
C5 = 523.25

# 创建一个简单的旋律
melody = [
    # 第一小节
    (C4, 0.25, 0.2), (E4, 0.25, 0.2), (G4, 0.25, 0.2), (C5, 0.25, 0.2),
    # 第二小节
    (G4, 0.25, 0.2), (E4, 0.25, 0.2), (C4, 0.5, 0.2),
    # 第三小节
    (D4, 0.25, 0.2), (F4, 0.25, 0.2), (A4, 0.25, 0.2), (D4, 0.25, 0.2),
    # 第四小节
    (G4, 0.5, 0.2), (B4, 0.5, 0.2),
]

# 生成旋律
for freq, duration, volume in melody:
    note = generate_tone(freq, duration, volume)
    background_music = np.concatenate([background_music, note])

# 添加一些简单的和弦作为伴奏
chords = [
    # C和弦
    ([C4/2, E4/2, G4/2], 1.0, 0.15),
    # F和弦
    ([F4/2, A4/2, C4], 1.0, 0.15),
    # G和弦
    ([G4/2, B4/2, D4], 1.0, 0.15),
    # C和弦
    ([C4/2, E4/2, G4/2], 1.0, 0.15),
]

accompaniment = np.array([], dtype=np.int16)
for freqs, duration, volume in chords:
    chord = generate_chord(freqs, duration, volume)
    accompaniment = np.concatenate([accompaniment, chord])

# 确保伴奏和旋律长度相同
min_length = min(len(background_music), len(accompaniment))
background_music = background_music[:min_length]
accompaniment = accompaniment[:min_length]

# 混合旋律和伴奏
background_music = background_music + accompaniment

# 重复几次以获得更长的背景音乐
background_music = np.tile(background_music, 4)

# 保存背景音乐
wavfile.write('sounds/background_music.wav', 44100, background_music)

print("已生成4个音效文件到sounds目录，包括背景音乐")