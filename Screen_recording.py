#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:lz


import os
import threading
import time

import cv2
import numpy as np
import PySimpleGUI as sg
from PIL import ImageGrab
from pynput import keyboard


def system_time():

    time_tup=time.localtime(time.time()) # 获取当前时间
    format_time="%Y-%m-%d_%H-%M-%S"
    cur_time=time.strftime(format_time,time_tup)
    return cur_time

def folder_path():
    
    isExists=os.path.exists('D:\@@@')
    if not isExists:
        os.mkdir('D:\@@@')
    else:
        pass

def get_desktop():

    folder_path()
    img = ImageGrab.grab() # 获取当前屏幕内容
    img.save('D:\@@@\Picture_{}.png'.format(system_time())) # 保存文件的名字
    # img.show()

def get_recode():

    folder_path()
    vie = ImageGrab.grab() #获得当前屏幕
    width = vie.size[0]
    height = vie.size[1]
    fourcc = cv2.VideoWriter_fourcc(*'XVID') # 规定编码器编码视频格式
    video = cv2.VideoWriter('D:\@@@\Video_{}.avi'.format(system_time()), fourcc, 10, (width,height), True) # 输出文件命名,帧率为30
    while True:
        im = ImageGrab.grab()
        imm = cv2.cvtColor(np.array(im), cv2.COLOR_RGB2BGR) # 转为opencv的BGR格式
        video.write(imm)
        if flag:
            break
    video.release()

flag=False  #停止标志位

def on_press(key):

    global flag
    if key == keyboard.Key.esc:
        flag = True
        return False  #返回False，键盘监听结束！

layout = [
    [sg.Button('截图', key = '_PHOTO_', font='微软雅黑', size=(10, 2)), sg.Button('录屏', key = '_VIDEO_', font='微软雅黑', size=(10, 2)), sg.Button('打开文件夹', key='_FOLDER_', size=(10, 2)), sg.Exit('退出', key = '_EXIT_', font='微软雅黑', size=(10, 2))],
    [sg.Text('请输入间隔时间(分)',font='微软雅黑',size=(15, 1)),sg.Input(key='_TIME_', size=(17, 1)),sg.Button('定时截图', key = '_TIMER_', font='微软雅黑', size=(10, 1))]
]
# 定义窗口，窗口名称
window = sg.Window('截图录屏工具',layout,font='微软雅黑')
# 自定义窗口进行数值回显
while True:
    event,values = window.read()
    if event == '_PHOTO_':
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
    elif event == '_TIMER_':
        timing = int(values['_TIME_'])
        while True:
            window.disappear()
            get_desktop()
            window.reappear()
            time.sleep(timing*60)
    elif event in ['_EXIT_',None]:
        break
    else:
        pass
window.close()

