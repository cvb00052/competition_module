# -*- coding: utf-8 -*-
"""
Created on Tue Jul 25 12:55:01 2017

@author: RXYH

get_picture

"""

import re
import os
import numpy as np
from PIL import Image

def get_num(path):
    #"计算共有多少张图片"
    dirs = os.listdir(path)
    i = 0
    for jpg in dirs:
        i += 1
    return i-1

#"图片和图片对应的类别的是按顺序的，相互对应"
#"例如第三张图片res_name[3]的类别在res_class[3]中"
def get_label(path):
    #"获取label文本"
    f = open(path)
    st = f.read()
    #"确定图片名字的格式，数字加逗号加数字"
    rule_name = r'\b(\d*,+\d+)\s'
    compile_name = re.compile(rule_name, re.M)
    #"在文本中找到所有图片名字"
    res_name = compile_name.findall(st)
    #"确定图片名字对应的类别的格式，空格加数字加空格"
    rule_class = r'\s(\d+)\s'
    compile_class = re.compile(rule_class, re.M)
    #"在文本中找到所有图片对应的类别名字"
    res_class = compile_class.findall(st)
    return res_name, res_class
 
def load_data_pic_test(path, count):
    #"创建data空数组和label空数组"
    data = np.empty((count, 70, 70, 3), dtype = float)
    imgs = os.listdir(path)
    for i in range(count):
        #打开对应图片
        newpath = path + '/' + imgs[i]
        #异常文件，自动跳过
        if newpath == path + '/Thumbs.db':
            continue
        #打开图片，初始化图片为70*70规格
        img = Image.open(newpath, mode = "r")
        img = img.resize(size = (70, 70))
        arr = np.asarray(img, dtype = float)
        #记录图片数据
        data[i,: ,: ,:] = arr
        if i % 1000 == 0:
            print(i, 'pictures loaded')
    return data


def load_data_pic(path, count, listname, listclass):
    #"创建data空数组和label空数组"
    data = np.empty((count, 70, 70, 3), dtype = float)
    label = np.empty((count, ), dtype = int)
    #"确定图片名字格式，与上一个函数一样"
    rule_picname = r'\b(\d*,+\d*).'
    compile_pic = re.compile(rule_picname);
    #"打开文件路径"
    imgs = os.listdir(path)
    for i in range(count):
        #打开对应图片
        newpath = path + '/' + imgs[i]
        #异常文件，自动跳过
        if newpath == path + '/Thumbs.db':
            continue
        #找到对应图片名字
        strname = compile_pic.findall(imgs[i])
        data_name = strname[0]
        #在上一个函数得到的list中
        #寻找对应的名字，返回这个名字在list中的位置
        try:
            pos = listname.index(data_name)
        except:
        #删除没有标签的图片
            os.remove(newpath)
            continue
        #记录标签
        label[i] = listclass[pos]
        #print(data_name, label[i])
        #打开图片，初始化图片为70*70规格
        img = Image.open(newpath, mode = "r")
        img = img.resize(size = (70, 70))
        arr = np.asarray(img, dtype = float)
        #记录图片数据
        data[i,: ,: ,:] = arr
        if i % 1000 == 0:
            print(i, 'pictures loaded')
    return data, label

def load_data(label_path, pic_path):
    count = get_num(pic_path)
    listname, listclass = get_label(label_path)
    data, label = load_data_pic(pic_path, count, listname, listclass)
    return data, label

def load_data_test(pic_path):
    count = get_num(pic_path)
    data = load_data_pic_test(pic_path, count)
    return data


