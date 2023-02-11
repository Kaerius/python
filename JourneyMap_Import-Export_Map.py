# -*- coding: utf-8 -*-
"""
Created on Sat Feb 11 13:25:22 2023

JourneyMap Import-Export Map

@author: Kaerius
"""

import PySimpleGUI as sg
import os
from PIL import Image
import shutil
from pathlib import Path

progress_bar_counter = 0

# Рисуем кнопки и окна
layout = [
    [sg.Text('Папка экспорта'), sg.InputText('Папка от куда брать карту'), sg.FolderBrowse(),
     ],
    [sg.Text('Папка импорта '), sg.InputText('Папка куда нужно дополнить'), sg.FolderBrowse(),
     ],
    [sg.ProgressBar(max_value=265, orientation='h', size=(44, 20), key='progressbar')],
    [sg.Output(size=(67, 15))],
    [sg.Submit('Применить'), sg.Cancel('Выход')]
]
window = sg.Window('Import-Export JourneyMap', layout)
progress_bar = window['progressbar']

# Обидиненить или скопировать файл
def merging_images(img_path1,img_path2):
    if os.path.exists(img_path2):
        print('Дополнен:',img_path2,'->',img_path1)
        img1 = Image.open(img_path1)
        img2 = Image.open(img_path2)
        img1.paste(img2, (0,0), img2)
        img1.save(img_path2)
        img1.close()
        img2.close()
        window.Refresh()
    else:
        print('Скопирован:',img_path1,'->',img_path2)
        shutil.copyfile(img_path1, img_path2)
        window.Refresh()

# Рекурсивный перебор папки
def folder_crawl(path,path2):
    global progress_bar_counter
    for i in os.listdir(path):
        if not os.path.isdir(path2):
            os.mkdir(path2)
        if os.path.isdir(path+'\\'+i):
            folder_crawl(path+'\\'+i,path2+'\\'+i)
            if not os.path.isdir(path2+'\\'+i):
                os.mkdir(path2+'\\'+i)
        else:
            if i.endswith('.png'):
                merging_images(path+'\\'+i,path2+'\\'+i)
                progress_bar_counter = progress_bar_counter + 1
                progress_bar.UpdateBar(progress_bar_counter, progress_bar_max)

# Основной цикл программы
while True: 
    event, values = window.read()
    if event in (None, 'Exit', 'Cancel', 'Выход'):
        break
    if event in ('Применить', 'Submit'):
        if os.path.isdir(values[0]) and os.path.isdir(values[1]):
            print('Из ',values[0])
            print('В ',values[1])
            progress_bar_max=len(list(Path(values[0]).rglob("*.png")))
            folder_crawl(values[1],values[0])
            print('Завершено!')
        else:
            print('Выбраны не папки.')
window.close()
