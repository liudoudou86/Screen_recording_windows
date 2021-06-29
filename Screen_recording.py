#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:lz


import ctypes
import os
import time
import tkinter

import cv2
import numpy as np
import PySimpleGUI as sg
from PIL import ImageGrab


class mouse_screen:

    isExists=os.path.exists('D:\@@@')
    if not isExists:
        os.mkdir('D:\@@@')
    else:
        pass

    def __init__(self):
        self.__start_x, self.__start_y = 0, 0
        self.__scale = 1

        self.__win = tkinter.Tk()
        self.__win.attributes("-alpha", 0.1)  # 设置窗口半透明
        self.__win.attributes("-fullscreen", True)  # 设置全屏
        self.__win.attributes("-topmost", True)  # 设置窗口在最上层

        self.__width, self.__height = self.__win.winfo_screenwidth(), self.__win.winfo_screenheight()

        # 创建画布
        self.__canvas = tkinter.Canvas(self.__win, width=self.__width, height=self.__height, bg="gray")

        self.__win.bind('<Button-1>', self.xFunc1)  # 绑定鼠标左键点击事件
        self.__win.bind('<ButtonRelease-1>', self.xFunc1)  # 绑定鼠标左键点击释放事件
        self.__win.bind('<B1-Motion>', self.xFunc2)  # 绑定鼠标左键点击移动事件
        self.__win.bind('<Escape>', lambda e: self.__win.destroy())  # 绑定Esc按键退出事件
        '''
        user32 = ctypes.windll.user32
        gdi32 = ctypes.windll.gdi32
        dc = user32.GetDC(None)
        widthScale = gdi32.GetDeviceCaps(dc, 8)  # 分辨率缩放后的宽度
        heightScale = gdi32.GetDeviceCaps(dc, 10)  # 分辨率缩放后的高度
        width = gdi32.GetDeviceCaps(dc, 118)  # 原始分辨率的宽度
        height = gdi32.GetDeviceCaps(dc, 117)  # 原始分辨率的高度
        self.__scale = width / widthScale
        # print(self.__width, self.__height, widthScale, heightScale, width, height, self.__scale)
        # self.__win.mainloop()  # 窗口持久化
        '''
    def xFunc1(self, event):
        # print(f"鼠标左键点击了一次坐标是:x={g_scale * event.x}, y={g_scale * event.y}")
        if event.state == 8:  # 鼠标左键按下
            self.__start_x, self.__start_y = event.x, event.y
        elif event.state == 264:  # 鼠标左键释放
            if event.x == self.__start_x or event.y == self.__start_y:
                return
            img = ImageGrab.grab((self.__scale * self.__start_x, self.__scale * self.__start_y, self.__scale * event.x, self.__scale * event.y))
            time_tup=time.localtime(time.time()) # 获取当前时间
            format_time="%Y-%m-%d_%H-%M-%S"
            cur_time=time.strftime(format_time,time_tup)
            img.save('D:\@@@\Screen_{}.png'.format(cur_time)) # 保存文件的名字

            self.__win.update()
            time.sleep(0.5)
            self.__win.destroy()

    def xFunc2(self, event):
        # print(f"鼠标左键点击了一次坐标是:x={self.__scale * event.x}, y={self.__scale * event.y}")
        if event.x == self.__start_x or event.y == self.__start_y:
            return
        self.__canvas.delete("prscrn")
        self.__canvas.create_rectangle(self.__start_x, self.__start_y, event.x, event.y,
                                       fill='white', outline='red', tag="prscrn")
        # 包装画布
        self.__canvas.pack()

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
    img.save('D:\@@@\Screen_{}.png'.format(cur_time)) # 保存文件的名字
    # img.show()


def get_recode():

    isExists=os.path.exists('D:\@@@')
    if not isExists:
        os.mkdir('D:\@@@')
    else:
        pass
    vie = ImageGrab.grab() #获得当前屏幕
    width = vie.size[0]
    height = vie.size[1]
    k=np.zeros((1,1),np.uint8)
    time_tup = time.localtime(time.time())
    format_time="%Y-%m-%d_%H-%M-%S"
    cur_time=time.strftime(format_time,time_tup)
    fourcc = cv2.VideoWriter_fourcc(*'X264') # 规定编码器编码视频格式
    video = cv2.VideoWriter('D:\@@@\Record_{}.mp4'.format(cur_time), fourcc, 60, (width,height)) # 输出文件命名,帧率为30
    while True:
        im = ImageGrab.grab()
        imm = cv2.cvtColor(np.array(im), cv2.COLOR_RGB2BGR) # 转为opencv的BGR格式
        video.write(imm)
        cv2.imshow('imm', k)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print(ord('q'))
            break
    video.release()
    cv2.destroyAllWindows()


layout = [
    [sg.Button('区域截图', key = '_MOUSE_', font='微软雅黑', size=(8, 3)), sg.Button('全屏截图', key = '_PHOTO_', font='微软雅黑', size=(8, 3)), sg.Button('录屏', key = '_VIDEO_', font='微软雅黑', size=(8, 3)), sg.Button('打开', key='_FOLDER_', size=(8, 3)), sg.Exit('退出', key = '_EXIT_', font='微软雅黑', size=(8, 3))]
]
# 定义窗口，窗口名称
window = sg.Window('截图录屏工具',layout,font='微软雅黑')
# 自定义窗口进行数值回显
while True:
    event,values = window.read()
    if event == '_MOUSE_':
        window.disappear() # 隐藏窗口
        mouse_screen()
        window.reappear() # 显示窗口
    elif event == '_PHOTO_':
        window.disappear() # 隐藏窗口
        get_desktop()
        window.reappear() # 显示窗口
    elif event == '_VIDEO_':
        window.disappear() # 隐藏窗口
        get_recode()
        window.reappear() # 显示窗口
    elif event == '_FOLDER_':
        os.startfile(r"D:\@@@")
    elif event in ['_EXIT_',None]:
        break
    else:
        pass
