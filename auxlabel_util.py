"""
!/usr/bin python3
Created on 2023/3/2
@author: CarryLee
@site: https://github.com/Nuaza
@file: auxlabel_util.py
@info: 快速配置以及一键运行的脚本
#################################
    Dataset Structure
- dataset/
    - images/
        - img_0.jpg
        - img_1.jpg
        ...
    - labels/
        - classes.txt
        - img_0.txt
        - img_1.txt
        ...
    - test/ (Optional)
        - test1.jpg
        ...
    - dataset.yaml
    - train.txt
    - val.txt
#################################
"""
import os
import sys
import yaml
import shutil
import random
import configparser


def get_classes(classes_path):
    """
    通过读取labelimg在打标签的文件夹下存储的classes.txt而获得数据集的所有类\n
    :param classes_path: classes.txt的路径
    :return: 带有所有class的字符串的一个列表
    """
    return list(i.strip('\n') for i in open(classes_path, 'r').readlines())


def get_cfg(section, option, value_type='path', file='setup.ini'):
    """
    获取ini参数文件\n
    :param section: 参数文件的section
    :param option: 参数文件section下对应的option
    :param value_type: 取得的参数的类型，默认为path，可设置为str和float
    :param file: 读取哪个参数文件，默认为当前目录下的setup.ini
    :return: 根据value_type返回str类型的文件路径或者float、int类型的数值型参数
    """
    cfp = configparser.ConfigParser()
    cfp.read(file, encoding='utf-8')
    value = cfp.get(section, option)
    if value_type == 'path':
        return os.path.abspath(value)
    elif value_type == 'float':
        return float(value)
    elif value_type == 'int':
        return int(value)
    else:
        return value


def set_cfg(section, option, value, file='setup.ini'):
    cfp = configparser.ConfigParser()
    cfp.read(file, encoding='utf-8')
    cfp.set(section, option, value.replace('\\', '/'))
    cfp.write(open(file, 'w'))


def shuffle_dataset(image_path, label_path, dataset_path, train_percent=0.8, picture_format='.jpg'):
    """
    按照设定的比例随机分配训练集和验证集，并生成其对应的text文件\n
    :param image_path: 存放数据集图片的路径
    :param label_path: 存放数据集标签的路径
    :param dataset_path: 数据集的根路径
    :param train_percent: 设置训练集的比例，默认为0.8
    :type train_percent: float
    :param picture_format: 图片的后缀名，默认为.jpg
    :type picture_format: str
    """
    image_list = list(i.split('.')[0] for i in os.listdir(image_path))
    label_list = list(j.split('.')[0] for j in os.listdir(label_path))
    labeled_list = list(set(image_list).intersection(label_list))
    train_list = random.sample(labeled_list, int(len(labeled_list) * train_percent))
    val_list = list(set(labeled_list) ^ set(train_list))
    train_file, val_file = open(dataset_path + '/train.txt', 'w'), open(dataset_path + '/val.txt', 'w')
    for i in train_list:
        train_file.write(os.path.abspath(image_path + '/' + i + picture_format).replace('\\', '/') + '\n')
    for j in val_list:
        val_file.write(os.path.abspath(image_path + '/' + j + picture_format).replace('\\', '/') + '\n')
    print('数据集划分成功!有效样本数为' + str(len(labeled_list)) + '个。根据设定随机划分了' + str(
        len(train_list)) + '个训练集样本以及' + str(len(val_list)) + '个验证集样本')
    train_file.close()
    val_file.close()


def generate_yaml(label_path, dataset_path, yaml_name='dataset.yaml'):
    """
    生成数据集的配置文件\n
    :param label_path: 存放数据集标签的路径
    :param dataset_path: 数据集的根路径
    :param yaml_name: 数据集配置文件的名称，默认dataset.yaml
    """
    try:
        classes = get_classes(label_path + '/classes.txt')
    except:
        print('生成失败!未能在标签文件夹下找到有效的classes.txt文件!')
    yaml_file = open(dataset_path + '/' + yaml_name, 'w')
    yaml_data = {'path': os.path.abspath(dataset_path).replace('\\', '/'),
                 'train': os.path.abspath(dataset_path + '/train.txt').replace('\\', '/'),
                 'val': os.path.abspath(dataset_path + '/val.txt').replace('\\', '/'), 'nc': len(classes),
                 'names': dict(zip(list(i for i in range(len(classes))), classes))}
    yaml.dump(yaml_data, yaml_file)
    print('成功生成 ' + dataset_path + '\\' + yaml_name + ' 配置文件!')
    yaml_file.close()


def copy_labels(source_labels, target_labels):
    """
    将标签文件从检测任务的输出文件夹复制到数据集文件夹下\n
    :param source_labels: 检测任务的输出文件夹路径
    :param target_labels: 数据集文件夹路径
    """
    number = 1
    if not os.path.exists(source_labels):
        print('source labels dir not exist!')
        exit(0)
    if not os.path.exists(target_labels):
        print('target labels dir not exist!')
        exit(0)
    for label_file in os.listdir(source_labels):
        source_path = os.path.abspath(source_labels).replace('\\', '/') + '/' + label_file
        target_path = os.path.abspath(target_labels).replace('\\', '/') + '/' + label_file
        shutil.copyfile(source_path, target_path)
        print('label copy ' + str(number) + '/' + str(len(os.listdir(source_labels))) + ': FROM ' + source_path
              + ' TO ' + target_path)
        number += 1
    print(str(number) + ' label(s) successfully copied!')
    # time.sleep(2)


def launch_train(train_weight, dataset_cfg, train_epochs, train_batch, train_device):
    from ultralytics import YOLO
    model = YOLO(train_weight)
    model.train(data=dataset_cfg, epochs=train_epochs, batch=train_batch, device=train_device)
    return


def launch_predict(predict_weight, image_source):
    from ultralytics import YOLO
    model = YOLO(predict_weight)
    model(image_source, save=True)
    return
