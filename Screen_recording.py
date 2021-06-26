#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:lz


import os
import time

import cv2
import numpy as np
import PySimpleGUI as sg
from PIL import ImageGrab


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
    [sg.Button('截图', key = '_PHOTO_', font='微软雅黑', size=(8, 3)), sg.Button('录屏', key = '_VIDEO_', font='微软雅黑', size=(8, 3)), sg.Button('打开', key='_FOLDER_', size=(8, 3)), sg.Exit('退出', key = '_EXIT_', font='微软雅黑', size=(8, 3))]
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
        # sg.popup_ok('已下载至当前目录',title='成功',font='微软雅黑')
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
