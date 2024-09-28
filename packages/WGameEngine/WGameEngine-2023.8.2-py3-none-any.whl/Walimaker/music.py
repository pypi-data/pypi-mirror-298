from .config import *


def bgmusic(bgm, loops=-1, start=0.0):
    pygame.mixer.music.load(bgm)
    pygame.mixer.music.play(loops=loops, start=start)


def set_volume(vol):
    pygame.mixer.music.set_volume(vol)

def music_load(bgm):
    pygame.mixer.music.load(bgm)

def music_play(loops=-1 ,start=0.0):
    pygame.mixer.music.play(loops=loops, start=start)  # 开始播放音乐流


def music_rewind():
    pygame.mixer.music.rewind()  # 重新开始播放音乐


def music_stop():
    pygame.mixer.music.stop()  # 结束音乐播放


def music_pause():
    pygame.mixer.music.pause()  # 暂停音乐播放


def music_unpause():
    pygame.mixer.music.unpause()  # 恢复音乐播放


def music_fadeout():
    pygame.mixer.music.fadeout()  # 淡出的效果结束音乐播放


def music_set_volume(vol):
    pygame.mixer.music.set_volume(vol)  # 设置音量


def music_get_volume():
    return pygame.mixer.music.get_volume()  # 获取音量


def music_get_busy():
    return pygame.mixer.music.get_busy()  # 检查是否正在播放音乐


def music_set_pos(pos):
    pygame.mixer.music.pause()  # 暂停音乐播放
    pygame.mixer.music.set_pos(pos)  # 设置播放的位置
    pygame.mixer.music.unpause()  # 恢复音乐播放


def music_get_pos():
    return pygame.mixer.music.get_pos()  # 获取播放的位置


def music_queue():
    pygame.mixer.music.queue()  # 将一个音乐文件放入队列中，并排在当前播放的音乐之后


def music_set_endevent():
    return pygame.mixer.music.set_endevent()  # 当播放结束时发出一个事件


def music_get_endevent():
    return pygame.mixer.music.get_endevent()  # 获取播放结束时发送的事件
