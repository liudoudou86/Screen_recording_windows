#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:lz


import os
import time
import tkinter

import cv2
import numpy as np
import PySimpleGUI as sg
from PIL import ImageGrab
from pynput import keyboard
import threading


class mouse_screen:

    isExists=os.path.exists('D:\@@@')
    if not isExists:
        os.mkdir('D:\@@@')
    else:
        pass

    def __init__(self):
        self.start_x, self.start_y = 0, 0
        self.scale = 1

        self.win = tkinter.Tk()
        self.win.attributes("-alpha", 0.2)  # 设置窗口半透明
        self.win.attributes("-fullscreen", True)  # 设置全屏
        self.win.attributes("-topmost", True)  # 设置窗口在最上层

        self.width, self.height = self.win.winfo_screenwidth(), self.win.winfo_screenheight()

        # 创建画布
        self.canvas = tkinter.Canvas(self.win, width=self.width, height=self.height, bg="black")

        self.win.bind('<Button-1>', self.Fun1)  # 绑定鼠标左键点击事件
        self.win.bind('<ButtonRelease-1>', self.Fun1)  # 绑定鼠标左键点击释放事件
        self.win.bind('<B1-Motion>', self.Fun2)  # 绑定鼠标左键点击移动事件
        self.win.bind('<Escape>', lambda e: self.win.destroy())  # 绑定Esc按键退出事件

    def Fun1(self, event):
        # print(f"鼠标左键点击了一次坐标是:x={g_scale * event.x}, y={g_scale * event.y}")
        if event.state == 8:  # 鼠标左键按下
            self.start_x, self.start_y = event.x, event.y
        elif event.state == 264:  # 鼠标左键释放
            if event.x == self.start_x or event.y == self.start_y:
                return
            img = ImageGrab.grab((self.scale * self.start_x, self.scale * self.start_y, self.scale * event.x, self.scale * event.y))
            time_tup=time.localtime(time.time()) # 获取当前时间
            format_time="%Y-%m-%d_%H-%M-%S"
            cur_time=time.strftime(format_time,time_tup)
            img.save('D:\@@@\Screenshots_{}.png'.format(cur_time)) # 保存文件的名字

            self.win.update()
            time.sleep(0.5)
            self.win.destroy()

    def Fun2(self, event):
        # print(f"鼠标左键点击了一次坐标是:x={self.__scale * event.x}, y={self.__scale * event.y}")
        if event.x == self.start_x or event.y == self.start_y:
            return
        self.canvas.delete()
        self.canvas.create_rectangle(self.start_x, self.start_y, event.x, event.y, fill='white', outline='red')
        # 包装画布
        self.canvas.pack()

def get_desktop():

    isExists=os.path.exists('D:\@@@')
    if not isExists:
        os.mkdir('D:\@@@')
    else:
        pass
    time_tup=time.localtime(time.time()) # 获取当前时间
    format_time="%Y-%m-%d_%H-%M-%S"
    cur_time=time.strftime(format_time,time_tup)
    img = ImageGrab.grab() # 获取当前屏幕内容
    img.save('D:\@@@\Screenshots_{}.png'.format(cur_time)) # 保存文件的名字
    # img.show()


flag=False  #停止标志位

def get_recode():

    isExists=os.path.exists('D:\@@@')
    if not isExists:
        os.mkdir('D:\@@@')
    else:
        pass
    vie = ImageGrab.grab() #获得当前屏幕
    width = vie.size[0]
    height = vie.size[1]
    time_tup = time.localtime(time.time())
    format_time="%Y-%m-%d_%H-%M-%S"
    cur_time=time.strftime(format_time,time_tup)
    fourcc = cv2.VideoWriter_fourcc(*'XVID') # 规定编码器编码视频格式
    video = cv2.VideoWriter('D:\@@@\Record_{}.avi'.format(cur_time), fourcc, 60, (width,height)) # 输出文件命名,帧率为30
    while True:
        im = ImageGrab.grab()
        imm = cv2.cvtColor(np.array(im), cv2.COLOR_RGB2BGR) # 转为opencv的BGR格式
        video.write(imm)
        if flag:
            break
    video.release()


def on_press(key):

    global flag
    if key == keyboard.Key.esc:
        flag=True
        return False  #返回False，键盘监听结束！


layout = [
    [sg.Button('区域截图', key = '_MOUSE_', font='微软雅黑', size=(8, 3)), sg.Button('全屏截图', key = '_PHOTO_', font='微软雅黑', size=(8, 3)), sg.Button('录屏', key = '_VIDEO_', font='微软雅黑', size=(8, 3)), sg.Button('打开', key='_FOLDER_', size=(8, 3)), sg.Exit('退出', key = '_EXIT_', font='微软雅黑', size=(8, 3))]
]
# 定义窗口，窗口名称
window = sg.Window('截图录屏工具',layout,font='微软雅黑')
# 自定义窗口进行数值回显
while True:
    event,values = window.read()
    if event == '_MOUSE_':
        mouse_screen()
    elif event == '_PHOTO_':
        window.disappear() # 隐藏窗口
        get_desktop()
        window.reappear() # 显示窗口
    elif event == '_VIDEO_':
        th=threading.Thread(target=get_recode)
        th.start()
        with keyboard.Listener(on_press=on_press) as listener:
            listener.join()
    elif event == '_FOLDER_':
        os.startfile(r"D:\@@@")
    elif event in ['_EXIT_',None]:
        break
    else:
        pass
