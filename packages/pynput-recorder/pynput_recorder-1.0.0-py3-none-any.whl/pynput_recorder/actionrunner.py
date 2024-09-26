#!/usr/bin/python
# -*- coding: utf-8 -*-
import threading
import time
from pynput.keyboard import Controller as KeyBoardController, KeyCode
from pynput.mouse import Button, Controller as MouseController
from pyutilb.file import read_yaml
from pyutilb.keycode import *
from pyutilb.util import replace_var, get_vars, set_vars
from pynput_recorder.comm import root

# 键盘/鼠标动作执行者，用于重放
class ActionRunner(object):

    def __init__(self, file_name='action.yml', on_stop=None):
        '''
        :param file_name
        :param on_stop 停止时回调
        '''
        self.file_name = file_name

        self.on_stop = on_stop
        self.original_screen_size = None # 录制时的原始屏幕大小
        self.screen_size = [root.winfo_screenwidth(), root.winfo_screenheight()]  # 运行时的屏幕大小，实例化时就要获得，否则报错 RuntimeError: main thread is not in main loop
        self.screen_scale_ratio = None  # 屏幕缩放比例

    def fix_position_by_screen_size(self, params):
        '''
        根据屏幕大小变化，来调整坐标，针对动作move/scroll
        '''
        if self.screen_scale_ratio is None:
            return params
        # 两值 x,y
        if isinstance(params, (list,tuple)):
            return [params[0]*self.screen_scale_ratio[0], params[1]*self.screen_scale_ratio[1]]
        # 单值 x
        return params*self.screen_scale_ratio

    def start(self):
        # 异步执行，不然会阻塞窗口渲染
        t = threading.Thread(target=self._start, args=(get_vars(),)) # 要传递threadlocal变量
        t.start()

    def _start(self, vars):
        set_vars(vars) # 应用threadlocal变量
        start_time = time.time()
        # 键盘执行器
        keyboard_runner = KeyBoardController()
        # 鼠标执行器
        mouse_runner = MouseController()
        # 读动作
        steps = read_yaml(self.file_name)
        for step in steps:
            for action, params in step.items():
                params = replace_var(params)
                print(f"{action}: {params}")
                if action == 'screen_size':
                    self.original_screen_size = params
                    wr = self.screen_size[0] / self.original_screen_size[0]
                    hr = self.original_screen_size[1]
                    if wr != 1 and hr != 1:
                        self.screen_scale_ratio = [wr, self.screen_size[1] / hr] # 屏幕缩放比例
                        print(f"屏幕缩放比例: {self.screen_scale_ratio}")
                elif action == 'press_key':
                    keyboard_runner.press(self.from_key_vk(params))
                elif action == 'release_key':
                    keyboard_runner.release(self.from_key_vk(params))
                elif action == 'move':
                    mouse_runner.position = self.fix_position_by_screen_size(params)
                if action == 'press':
                    btn = self.get_mouse_button(params)
                    mouse_runner.press(btn)
                elif action == 'release':
                    btn = self.get_mouse_button(params)
                    mouse_runner.release(btn)
                elif action == 'scroll':
                    mouse_runner.scroll(*self.fix_position_by_screen_size(params))
                elif action == 'sleep':
                    time.sleep(float(params))
                elif action == 'exit':
                    exit()
                elif action == 'input':
                    keyboard_runner.type(params)


        if self.on_stop:
            self.on_stop()
        print("time cost: ", time.time() - start_time, "s")

    def from_key_vk(self, vk):
        '''
        vk转key code
        :param vk int或char
        '''
        # char先转为字符码
        if isinstance(vk, str):
            if vk in char2keycode:
                vk = char2keycode[vk]
        return KeyCode.from_vk(vk)

    def get_mouse_button(self, type):
        if type == 'left':
            return Button.left
        return Button.right