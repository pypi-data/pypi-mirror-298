#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import time
from pynput import keyboard, mouse
from pyutilb.keycode import *
from pynput_recorder.comm import root

# 键盘/鼠标动作监听
class ActionListener(object):

    def __init__(self, file_name='action.yml', on_stop=None):
        '''
        :param file_name
        :param on_stop 停止时回调
        '''
        self.file_name = file_name
        self.on_stop = on_stop
        self.file = None
        self.last_time = None # 上一个动作的时间
        # 键盘监听器
        self.keyboardListener = None
        # 鼠标监听器
        self.mouseListener = None

    def append_action(self, action, params):
        '''
        记录动作
        '''
        # 计算跟上一次动作的耗时
        now = time.time()
        if self.last_time is not None:
            span = now - self.last_time
            if span > 0.2:
                self.file.write(f"- sleep: {span}\n")
        self.last_time = now
        # 记录动作
        if isinstance(params, (list, tuple, dict)):
            params = json.dumps(params)
        self.file.write(f"- {action}: {params}\n")
        self.file.flush()

    def start(self):
        self.file = open(self.file_name, 'w', encoding='utf-8')
        # 键盘监听器
        self.keyboardListener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
        self.keyboardListener.start()
        # 鼠标监听器
        self.mouseListener = mouse.Listener(on_move=self.on_move, on_click=self.on_click, on_scroll=self.on_scroll)
        self.mouseListener.start()
        # 记录当时屏幕大小，以便后续重放时按实际屏幕大小调整坐标，针对动作move/scroll
        self.append_action('screen_size', [root.winfo_screenwidth(), root.winfo_screenheight()])

    def stop(self):
        # 停止监听
        self.keyboardListener.stop()
        self.mouseListener.stop()
        self.file.close()
        self.file = None
        if self.on_stop:
            self.on_stop()
        return False

    # ------------------ 键盘监听处理 ----------------
    # 键盘按下监听
    def on_press(self, key):
        self.append_action('press_key', self.get_key_code(key))

    # 键盘抬起监听
    def on_release(self, key):
        if key == keyboard.Key.esc:
            return self.stop()
        self.append_action('release_key', self.get_key_code(key))

    def get_key_code(self, key):
        try:
            ret = key.vk
        except AttributeError:
            ret = key.value.vk
        # 如果是特殊字符码，则转字符，以便增加录制脚本的可读性
        if ret in keycode2char:
            # return keycode2char[ret] + '=' + str(ret) # 调试
            return keycode2char[ret]
        return ret

    # ------------------ 鼠标监听处理 ----------------
    # 鼠标移动事件
    def on_move(self, x, y):
        self.append_action('move', [x, y])

    # 鼠标点击事件
    def on_click(self, x, y, button, pressed):
        if pressed:
            self.append_action('press', button.name)
        else:
            self.append_action('release', button.name)

    # 鼠标滚动事件
    def on_scroll(self, x, y, x_axis, y_axis):
        self.append_action('scroll', [x_axis, y_axis])
