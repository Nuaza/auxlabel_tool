#!/usr/bin/env python3.8
# @Time:2023/2/27
# @Author:CarryLee
# @File:batch_rename.py
# @Info:批量改名脚本
import os


def rename(pre_name=''):
    filelist = os.listdir('../dataset/images/')
    number = 0
    for item in filelist:
        if item.endswith('.jpg'):
            src = os.path.join(os.path.abspath('../dataset/images/'), item)
            dst = os.path.join(os.path.abspath('../dataset/images/'), str(pre_name) + str(number) + '.jpg')
            try:
                os.rename(src, dst)
                number += 1
            except:
                continue


if __name__ == "__main__":
    rename(input('Input the pre name:'))
