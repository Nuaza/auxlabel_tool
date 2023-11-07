# Nuaza's AuxLabel Tool

[English](./README.md) | [简体中文](./README_CN.md)

这个项目基于YOLOv8，用于一键式**处理数据集**

也可以进行训练任务和检测任务

![image1](./resources/1.png)

# 💻Requirements

+ Microsoft Windows 7 / 8 / 8.1 / 10 / 11 (MacOS和带图形界面的Linux系统应该也能用吧，俺没测试过)
+ 一块(或者多块)能够支撑你运行YOLOv8的英伟达图形处理卡(或者如果你不介意用CPU运行的话，那就忽略这项)
+ Python 3.8及以上版本，以及这些[python第三方包](./requirements.txt)

# 😫咋装啊这玩意儿?

1. 用`git clone https://github.com/Nuaza/auxlabel_tool.git` 来把这个项目克隆到你的本机上 (或者点右上角那个绿色儿的Code按钮，然后点Download ZIP把这个项目压缩包手动下载到本机上也行嗷。这步有可能会报错或者卡在下载那儿，这是网络的问题)
2. 用`cd auxlabel_tool` 来进入到项目文件夹里面
3. 用`pip install -r requirements.txt` 来安装所有你所需要的第三方包 (如果你搁这儿报错了，检查下你的Python安装好了没)
4. 用`python auxLabel_GUI.py` 运行图形化界面

# 🤨咋运行啊这玩意儿?



# 😮这玩意儿能干啥?

用来快速创建你的YOLO自定义数据集，帮你一键划分好训练集和测试集，帮你自动生成yaml配置文件，帮你一键式跑训练和检测任务

这玩意儿最开始设想的理想的使用方法是：假设你有一个包含114514张图片的没有标签文件的数据集，你只需要在labelImg上手动标注其中的50张或者100张，然后用这些数据帮你训练好一个模型，并用这个模型把所有的图片都给检测一次。然后你从这里面再选一些标签再改改，再拿去训练...最后成功训练出一个完美的模型

额，如果你觉得这步骤太麻烦了，它也能作为一个帮你快速处理YOLO数据集的工具来用，还挺好使的捏

# 😉TODO

| Status | Things      |
| ------ |-------------|
| ❌      | 把整个项目翻译成英文  |
| ❌      | 适配其它的YOLO版本 |

*懒狗一条了嗷*

# 参考

[ultralytics/YOLOv8](https://github.com/ultralytics/ultralytics)

[HumanSignal/labelImg](https://github.com/HumanSignal/labelImg)
