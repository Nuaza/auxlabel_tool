#!/usr/bin/env python3.8
# @Time:2023/2/27
# @Author:CarryLee
# @File:video_capture.py
# @Info:视频自动抓帧脚本，设置好视频路径和抓帧频率即可
# pip3 install opencv-python
import cv2
import os


def video_to_frame(video_path, frame_frequency=60):
    times = 0
    camera = cv2.VideoCapture(video_path)
    while True:
        times += 1
        res, image = camera.read()
        if not res:
            break
        if times % frame_frequency == 0:  # Save frame according the frequency.
            cv2.imwrite('./Pictures/' + video_path + '_' + str(times) + '.jpg', image)
    camera.release()
    return


if __name__ == "__main__":
    while True:
        path = input('Input the path of video:')
        try:
            frame_frequency = int(input('Input the frequency of the capture actions:'))
        except:
            print('Not a valid number! Use the default 60')
            frame_frequency = 60
        print('Wait a moment...')
        video_to_frame(path, frame_frequency)
        if input('Done!Press any key to continue.Press q to quit:') == 'q':
            break
