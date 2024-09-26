#!/usr/bin/python
# -*- coding: utf-8 -*-
import tkinter
from pynput_recorder.actionlistener import ActionListener
from pynput_recorder.actionrunner import ActionRunner
from pynput_recorder.comm import root

class MyButton(tkinter.Button):
    def __init__(self, master, normal_label, disable_label, listener_cls):
        '''
        :param master 父组件
        :param normal_label 正常时显示label
        :param disable_label 禁用时显示label
        :param listener_cls ActionListener 或 ActionRunner
        '''
        def start():
            self['text'] = disable_label
            self['state'] = 'disable'
            listener.start() # 启动监听器或执行器
        def on_stop():
            self['text'] = normal_label
            self['state'] = 'normal'
        listener = listener_cls(on_stop=on_stop)
        super().__init__(master, text=normal_label, command=start)

def run_recorder():
    root.title('PynputRecorder-shigebeyond')
    root.geometry('260x260+400+100')

    startListenerBtn = MyButton(root, "start record", "recording...[esc] to stop", ActionListener)
    startListenerBtn.place(x=30, y=45, width=200, height=30)

    startRunnerBtn = MyButton(root, "start replay", "replaying...close window to stop", ActionRunner)
    startRunnerBtn.place(x=30, y=145, width=200, height=30)
    root.mainloop()

if __name__ == '__main__':
    run_recorder()