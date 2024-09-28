# WGameEngine

#### 介绍
**这是一个对pygame的游戏引擎封装**
    仅用于个人研究

# 更新说明
2020.2.29 修正了碰撞检测的mask存在左右颠倒的问题
2020.3.2 修正了播放动画时的set_start_func功能，增加了stop_anim()方法，将key_released()修改为key_just_released()

2023.7.26
更新了.bat文件中pip升级的方式

TextBox支持\n换行

say支持自定义对话框和字体，通过修改Character的DialogBox_font和DialogBox_img（图片大小最好是650x524）

.say支持更换颜色a.say("hello",(0,255,0))

2023.7.27

修正了透明度低于128无法交互的问题，现在下限是1，为0时无法交互

SET_IME_SHOW()开启输入法UI界面，必须写在setup之前

key_input()可以返回候选词

角色.get_mouse_just_clicked()和角色.get_mouse_clicked()和get_mouse_just_clicked()和get_mouse_clicked()添加了一个形式参数b，
角色.get_mouse_just_clicked(b=1)表示角色只有被左键点击才有效，b=1表示左键，b=2表示中键，b=3表示右键

添加了一个根据角度设置运动方向函数，a.set_angle(90)，上0下180左-90右90

添加了一个获取运动方向角度a.get_angle，上0下180左-90右90

2023.7.28

更新了一系列音乐组件
music_load(bgm)# 加载音乐
music_play(loops=-1, start=0.0)# 开始播放音乐流
music_rewind() # 重新开始播放音乐
music_stop() # 结束音乐播放
music_pause() # 暂停音乐播放
music_unpause() # 恢复音乐播放
music_fadeout() # 淡出的效果结束音乐播放
music_set_volume() # 设置音量
music_get_volume() # 获取音量
music_get_busy()  # 检查是否正在播放音乐
music_set_pos(pos) # 设置播放的位置
music_get_pos() # 获取播放的位置
music_queue() # 将一个音乐文件放入队列中，并排在当前播放的音乐之后
music_set_endevent() # 当播放结束时发出一个事件
music_get_endevent() # 获取播放结束时发送的事件
2023.7.29

修改了文本框出现的位置，文本框会根据角色处于不同的象限出现在不同的位置
2023.8.2
b=TextBox(size, font = 新字体,bgfill=文本背景颜色,font_color=字体颜色)


