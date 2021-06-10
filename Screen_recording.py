#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:lz


import time

import cv2
import numpy as np
import PySimpleGUI as sg
from PIL import ImageGrab


def get_desktop():

    img = ImageGrab.grab()

    # 设置保存的文件名
    time_tup=time.localtime(time.time())
    format_time="%Y%m%d%H%M%S"
    cur_time=time.strftime(format_time,time_tup)
    img.save('桌面截图_{}.jpg'.format(cur_time))
    # img.show()

def get_recode():
    p = ImageGrab.grab()#获得当前屏幕
    k=np.zeros((9,9),np.uint8)
    a,b=p.size#获得当前屏幕的大小
    fourcc = cv2.VideoWriter_fourcc(*'XVID')#编码格式
    time_tup=time.localtime(time.time())
    format_time="%Y%m%d%H%M%S"
    cur_time=time.strftime(format_time,time_tup)
    video = cv2.VideoWriter('屏幕录制_{}.mp4'.format(cur_time), fourcc, 16, (a, b))#输出文件命名为test.mp4,帧率为16，可以自己设置
    while True:
        im = ImageGrab.grab()
        imm=cv2.cvtColor(np.array(im), cv2.COLOR_RGB2BGR)#转为opencv的BGR格式
        video.write(imm)
        cv2.imshow('recoding', k)
        if cv2.waitKey(1) & 0xFF == ord('q'):
          break
    video.release()
    cv2.destroyAllWindows()


layout = [
    [sg.Button('录屏开始',key = '_VIDEOSTART_',font='微软雅黑', size=(9, 1)), sg.Button('录屏结束',key = '_VIDEOSTOP_',font='微软雅黑', size=(9, 1))],
    [sg.Button('抓图',key = '_PHOTO_',font='微软雅黑', size=(9, 1)), sg.Exit('退出',key = '_EXIT_',font='微软雅黑', size=(9, 1))]
]
# 定义窗口，窗口名称
window = sg.Window('抓图录屏工具',layout,font='微软雅黑')
# 自定义窗口进行数值回显
while True:
    event,values = window.read()
    if event == '_PHOTO_':
        get_desktop = get_desktop()
        # sg.popup_ok('已下载至当前目录',title='成功',font='微软雅黑')
    elif event == '_VIDEOSTART_':
        get_recode = get_recode()
    elif event in ['_EXIT_',None]:
        break
    else:
        pass
