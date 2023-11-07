"""
!/usr/bin python3
Created on 2023/3/16
@author: CarryLee
@site: https://github.com/Nuaza
@file: auxLabel_GUI.py
@info:
!pip install windows-filedialogs
"""
import sys
import os.path

import win32ui
import subprocess
import filedialogs
import auxlabel_util as autil
from PyQt5.QtWidgets import QWidget, QGridLayout
from labelImg.labelImg import MainWindow as labelimgWindow

try:
    from PyQt5.QtGui import *
    from PyQt5.QtCore import *
    from PyQt5.QtWidgets import *
except ImportError:
    from PySide2.QtGui import *
    from PySide2.QtCore import *
    from PySide2.QtWidgets import *


def selectPath(object):
    object.setText(filedialogs.open_folder_dialog('选择文件夹路径', 'gbk'))


def selectWeight(object):
    dlg = win32ui.CreateFileDialog(True, "pt", None, 0x04 | 0x02, "PyTorch权重文件 (*.pt)|*.pt|")
    dlg.DoModal()
    object.setText(dlg.GetPathName())


def selectYaml(object):
    dlg = win32ui.CreateFileDialog(True, "yaml", None, 0x04 | 0x02, "数据集YAML配置文件 (*.yaml)|*.yaml|")
    dlg.DoModal()
    object.setText(dlg.GetPathName())


def selectTxt(object):
    dlg = win32ui.CreateFileDialog(True, "txt", None, 0x04 | 0x02, "纯文本格式文件 (*.txt)|*.txt|")
    dlg.DoModal()
    object.setText(dlg.GetPathName())


def openDefaultYAML():
    subprocess.run(["notepad", os.path.abspath("./ultralytics/yolo/cfg/default.yaml")])


class UI_SubWindow(QWidget):

    def __init__(self, stackedObject=None):
        super().__init__()
        self.setWindowTitle("开始")
        self.setMinimumSize(QSize(300, 60))
        self.btn_forward = QPushButton('下一步')
        self.btn_forward.clicked.connect(lambda: self.page_forward(stackedObject))
        self.btn_backward = QPushButton('上一步')
        self.btn_backward.setEnabled(False)
        self.btn_backward.clicked.connect(lambda: self.page_backward(stackedObject))
        self.hbox = QHBoxLayout()
        self.hbox.addWidget(self.btn_backward)
        self.hbox.addWidget(self.btn_forward)
        self.vbox = QVBoxLayout()
        self.vbox.addLayout(self.hbox)
        self.setLayout(self.vbox)

    def page_forward(self, stackedObject):
        self.btn_backward.setEnabled(True)
        if stackedObject.currentIndex() == 4:
            print("数据集处理界面")
        if stackedObject.currentIndex() == 1:
            print("训练界面")
        if stackedObject.currentIndex() == 2:
            print("检测界面")
        if stackedObject.currentIndex() == 3:
            if QMessageBox.question(self, "开始", "再进行一轮？", QMessageBox.Yes, QMessageBox.No) == QMessageBox.Yes:
                # TODO: 检测完成后，标签文件会被存放在runs/exp文件夹下，考虑迁移标签文件到labelimg设定的保存目录下
                stackedObject.setCurrentIndex(4)
                self.btn_backward.setEnabled(False)
                print("回到了labelimg界面")
                return
            else:
                print("您可以在左侧菜单栏自行选择欲进行的操作")
                self.close()
                return
        stackedObject.setCurrentIndex((stackedObject.currentIndex() + 1) % 4)

    def page_backward(self, stackedObject):
        print("那么，返回到上一步")
        if stackedObject.currentIndex() == 1:
            stackedObject.setCurrentIndex(4)
            self.btn_backward.setEnabled(False)
            return
        stackedObject.setCurrentIndex((stackedObject.currentIndex() - 1) % 4)


class UI_MainWindow(QMainWindow):
    # parameters for window references
    WINDOW_WIDTH = autil.get_cfg('window_cfg', 'WINDOW_WIDTH', value_type='int')
    WINDOW_HEIGHT = autil.get_cfg('window_cfg', 'WINDOW_HEIGHT', value_type='int')
    MAXIUM_CONSOLE_LINE = autil.get_cfg('window_cfg', 'MAXIUM_CONSOLE_LINE', value_type='int')

    # parameters for coping label files
    copy_from = autil.get_cfg('Copy_cfg', 'copy_from', value_type='path')
    copy_to = autil.get_cfg('Copy_cfg', 'copy_to', value_type='path')

    # definitions for size policies
    sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.MinimumExpanding)
    sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
    sizePolicy2 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

    def closeEvent(self, event):
        reply = QMessageBox.question(self, "退出", "确认要退出吗？", QMessageBox.Yes, QMessageBox.No)
        if reply == QMessageBox.Yes:
            # 直接退出会报错“Error in atexit._run_exitfuncs:”
            # event.accept()
            sys.exit(app.exec_())
        else:
            event.ignore()

    def setup_console(self):
        self.ConsoleOutput = QTextBrowser(self.centralWidget)
        self.ConsoleOutput.setObjectName("ConsoleOutput")
        self.ConsoleOutput.document().setMaximumBlockCount(self.MAXIUM_CONSOLE_LINE)

        self.sizePolicy1.setHeightForWidth(self.ConsoleOutput.sizePolicy().hasHeightForWidth())
        self.ConsoleOutput.setSizePolicy(self.sizePolicy1)

    def setup_startupPage(self):
        self.startupPage = QWidget()
        self.startupPage.setObjectName("startupPage")
        self.startupLayout = QGridLayout(self.startupPage)
        self.startupLayout.setObjectName("startupLayout")
        self.startup_label = QLabel(self.startupPage)
        self.startup_label.setPixmap(QPixmap("resources/procedure.png"))
        # self.startup_label.setPixmap(QPixmap("resources/procedure_zh.png"))
        self.startup_label.setScaledContents(True)
        self.startup_label.setObjectName("startup_label")
        self.startupLayout.addWidget(self.startup_label)

    def setup_datasetPage(self):
        self.datasetPage = QWidget()
        self.datasetPage.setObjectName("datasetPage")
        self.datasetPage.setEnabled(True)
        self.datasetLayout = QGridLayout(self.datasetPage)
        self.datasetLayout.setObjectName("datasetLayout")

        self.dataset_path_label = QLabel("数据集路径", self.datasetPage)
        self.dataset_path_label.setObjectName("dataset_path_label")
        self.datasetLayout.addWidget(self.dataset_path_label, 0, 0, 1, 1)

        self.dataset_path = QLineEdit(autil.get_cfg('DataSet_cfg', 'dataset', value_type='path'), self.datasetPage)
        self.dataset_path.setObjectName("dataset_path")
        self.datasetLayout.addWidget(self.dataset_path, 0, 2, 1, 1)

        self.select_dataset = QPushButton("...", self.datasetPage)
        self.select_dataset.setObjectName("select_dataset")
        self.select_dataset.clicked.connect(lambda: selectPath(self.dataset_path))
        self.datasetLayout.addWidget(self.select_dataset, 0, 3, 1, 1)

        self.image_path_label = QLabel("图片文件夹", self.datasetPage)
        self.image_path_label.setObjectName("image_path_label")
        self.datasetLayout.addWidget(self.image_path_label, 1, 0, 1, 1)

        self.image_path = QLineEdit(autil.get_cfg('DataSet_cfg', 'image', value_type='path'), self.datasetPage)
        self.image_path.setObjectName("image_path")
        self.datasetLayout.addWidget(self.image_path, 1, 2, 1, 1)

        self.select_image = QPushButton("...", self.datasetPage)
        self.select_image.setObjectName("select_image")
        self.select_image.clicked.connect(lambda: selectPath(self.image_path))
        self.datasetLayout.addWidget(self.select_image, 1, 3, 1, 1)

        self.label_path_label = QLabel("标签文件夹", self.datasetPage)
        self.label_path_label.setObjectName("label_path_label")
        self.datasetLayout.addWidget(self.label_path_label, 2, 0, 1, 1)

        self.label_path = QLineEdit(autil.get_cfg('DataSet_cfg', 'label', value_type='path'), self.datasetPage)
        self.label_path.setObjectName("label_path")
        self.datasetLayout.addWidget(self.label_path, 2, 2, 1, 1)

        self.select_label = QPushButton("...", self.datasetPage)
        self.select_label.setObjectName("select_label")
        self.select_label.clicked.connect(lambda: selectPath(self.label_path))
        self.datasetLayout.addWidget(self.select_label, 2, 3, 1, 1)

        self.train_percent_label = QLabel("训练集比例", self.datasetPage)
        self.train_percent_label.setObjectName("train_percent_label")
        self.datasetLayout.addWidget(self.train_percent_label, 3, 0, 1, 1)

        self.train_percent = QSlider(self.datasetPage)
        self.train_percent.setObjectName("train_percent")
        self.train_percent.setMinimum(1)
        self.train_percent.setMaximum(100)
        self.train_percent.setSingleStep(1)
        self.train_percent.setValue(int(autil.get_cfg('DataSet_cfg', 'train_percent', value_type='float') * 100))
        self.train_percent.setOrientation(Qt.Horizontal)
        self.train_percent.valueChanged.connect(lambda: self.changePercentResult())
        self.datasetLayout.addWidget(self.train_percent, 3, 2, 1, 1)

        self.train_percent_result = QLabel(str(self.train_percent.value() / 100), self.datasetPage)
        self.train_percent_result.setObjectName("train_percent_result")
        self.train_percent_result.setAlignment(Qt.AlignCenter)
        self.datasetLayout.addWidget(self.train_percent_result, 3, 3, 1, 1)

        self.save_dataset_btn = QPushButton("保存设置", self.datasetPage)
        self.save_dataset_btn.setObjectName("save_dataset_btn")
        self.save_dataset_btn.clicked.connect(lambda: self.save_dataset_config())
        self.datasetLayout.addWidget(self.save_dataset_btn, 5, 3, 1, 1)

        self.shuffle_dataset = QPushButton("划分数据集", self.datasetPage)
        self.shuffle_dataset.setObjectName("shuffle_dataset")
        self.shuffle_dataset.clicked.connect(
            lambda: autil.shuffle_dataset(autil.get_cfg('DataSet_cfg', 'image', value_type='path'),
                                          autil.get_cfg('DataSet_cfg', 'label', value_type='path'),
                                          autil.get_cfg('DataSet_cfg', 'dataset', value_type='path'),
                                          autil.get_cfg('DataSet_cfg', 'train_percent', value_type='float')))
        self.datasetLayout.addWidget(self.shuffle_dataset, 5, 0, 1, 1)

        self.generate_yaml = QPushButton("生成配置文件", self.datasetPage)
        self.generate_yaml.setObjectName("generate_yaml")
        self.generate_yaml.clicked.connect(
            lambda: autil.generate_yaml(autil.get_cfg('DataSet_cfg', 'label', value_type='path'),
                                        autil.get_cfg('DataSet_cfg', 'dataset', value_type='path')))
        self.datasetLayout.addWidget(self.generate_yaml, 6, 0, 1, 1)

    def setup_trainPage(self):
        self.trainPage = QWidget()
        self.trainPage.setObjectName("trainPage")
        self.trainLayout = QGridLayout(self.trainPage)
        self.trainLayout.setObjectName("trainLayout")

        self.train_weight_label = QLabel("训练权重文件", self.trainPage)
        self.train_weight_label.setObjectName("train_weight_label")
        self.trainLayout.addWidget(self.train_weight_label, 0, 1, 1, 1)

        self.train_weight_path = QLineEdit(autil.get_cfg('Train_cfg', 'train_weight', value_type='path'),
                                           self.trainPage)
        self.train_weight_path.setObjectName("train_weight_path")
        self.trainLayout.addWidget(self.train_weight_path, 0, 3, 1, 5)

        self.select_train_weight = QPushButton("...", self.trainPage)
        self.select_train_weight.setObjectName("select_train_weight")
        self.select_train_weight.clicked.connect(lambda: selectWeight(self.train_weight_path))
        self.sizePolicy2.setHeightForWidth(self.select_train_weight.sizePolicy().hasHeightForWidth())
        self.select_train_weight.setSizePolicy(self.sizePolicy2)
        self.trainLayout.addWidget(self.select_train_weight, 0, 8, 1, 1)

        self.dataset_cfg_label = QLabel("数据集配置文件", self.trainPage)
        self.dataset_cfg_label.setObjectName("dataset_cfg_label")
        self.trainLayout.addWidget(self.dataset_cfg_label, 1, 1, 1, 1)

        self.dataset_cfg_path = QLineEdit(autil.get_cfg('Train_cfg', 'dataset_cfg', value_type='path'), self.trainPage)
        self.dataset_cfg_path.setObjectName("dataset_cfg_path")
        self.trainLayout.addWidget(self.dataset_cfg_path, 1, 3, 1, 5)

        self.select_dataset_cfg = QPushButton("...", self.trainPage)
        self.select_dataset_cfg.setObjectName("select_dataset_cfg")
        self.select_dataset_cfg.clicked.connect(lambda: selectYaml(self.dataset_cfg_path))
        self.sizePolicy2.setHeightForWidth(self.select_dataset_cfg.sizePolicy().hasHeightForWidth())
        self.select_dataset_cfg.setSizePolicy(self.sizePolicy2)
        self.trainLayout.addWidget(self.select_dataset_cfg, 1, 8, 1, 1)

        self.epoch_label = QLabel("训练轮数", self.trainPage)
        self.epoch_label.setObjectName("epoch_label")
        self.trainLayout.addWidget(self.epoch_label, 3, 1, 1, 1)

        self.epoch_val = QLineEdit(autil.get_cfg('Train_cfg', 'train_epochs', value_type='str'), self.trainPage)
        self.epoch_val.setObjectName("epoch_val")
        self.sizePolicy2.setHeightForWidth(self.epoch_val.sizePolicy().hasHeightForWidth())
        self.epoch_val.setSizePolicy(self.sizePolicy2)
        self.epoch_val.setMaximumSize(QSize(100, 100))
        self.trainLayout.addWidget(self.epoch_val, 3, 3, 1, 1)

        self.epoch_info = QLabel("若未设置则默认为300轮", self.trainPage)
        self.epoch_info.setObjectName("epoch_info")
        self.trainLayout.addWidget(self.epoch_info, 3, 4, 1, 2)

        self.default_yaml_info = QLabel("欲进行更详细的设置，请修改", self.trainPage)
        self.default_yaml_info.setObjectName("default_yaml_info")
        self.trainLayout.addWidget(self.default_yaml_info, 3, 7, 1, 1)

        self.default_yaml = QPushButton("default.yaml", self.trainPage)
        self.default_yaml.setObjectName("default_yaml")
        self.default_yaml.clicked.connect(lambda: openDefaultYAML())
        self.trainLayout.addWidget(self.default_yaml, 3, 8, 1, 1)

        self.batch_label = QLabel("Batch Size", self.trainPage)
        self.batch_label.setObjectName("batch_label")
        self.trainLayout.addWidget(self.batch_label, 4, 1, 1, 1)

        self.batch_val = QLineEdit(autil.get_cfg('Train_cfg', 'train_batch', value_type='str'), self.trainPage)
        self.batch_val.setObjectName("batch_val")
        self.sizePolicy2.setHeightForWidth(self.batch_val.sizePolicy().hasHeightForWidth())
        self.batch_val.setSizePolicy(self.sizePolicy2)
        self.batch_val.setMaximumSize(QSize(100, 100))
        self.trainLayout.addWidget(self.batch_val, 4, 3, 1, 1)

        self.batch_info = QLabel("设置为-1可自动识别，若未设置则默认为24", self.trainPage)
        self.batch_info.setObjectName("batch_info")
        self.trainLayout.addWidget(self.batch_info, 4, 4, 1, 3)

        self.save_train = QPushButton("保存设置", self.trainPage)
        self.save_train.setObjectName("save_train")
        self.save_train.clicked.connect(lambda: self.save_train_config())
        self.trainLayout.addWidget(self.save_train, 4, 8, 1, 1)

        self.device_label = QLabel("训练设备", self.trainPage)
        self.device_label.setObjectName("device_label")
        self.trainLayout.addWidget(self.device_label, 6, 1, 1, 1)

        self.device_val = QLineEdit(autil.get_cfg('Train_cfg', 'train_device', value_type='str'), self.trainPage)
        self.device_val.setObjectName("device_val")
        self.sizePolicy2.setHeightForWidth(self.device_val.sizePolicy().hasHeightForWidth())
        self.device_val.setSizePolicy(self.sizePolicy2)
        self.device_val.setMaximumSize(QSize(100, 100))
        self.trainLayout.addWidget(self.device_val, 6, 3, 1, 1)

        self.device_info = QLabel("设置训练所用设备，例如 0 或者 0,1,2,3 或者 cpu", self.trainPage)
        self.device_info.setObjectName("device_info")
        self.trainLayout.addWidget(self.device_info, 6, 4, 1, 4)

        self.start_train = QPushButton("开始训练", self.trainPage)
        self.start_train.setObjectName("start_train")
        self.start_train.setEnabled(False)
        self.start_train.clicked.connect(lambda: self.launch_train())
        self.trainLayout.addWidget(self.start_train, 6, 8, 1, 1)

    def setup_predictPage(self):
        self.predictPage = QWidget()
        self.predictPage.setObjectName("predictPage")
        self.predictLayout = QGridLayout(self.predictPage)
        self.predictLayout.setObjectName("predictLayout")

        self.predict_weight_label = QLabel("检测权重文件", self.predictPage)
        self.predict_weight_label.setObjectName("predict_weight_label")
        self.sizePolicy2.setHeightForWidth(self.predict_weight_label.sizePolicy().hasHeightForWidth())
        self.predict_weight_label.setSizePolicy(self.sizePolicy2)
        self.predictLayout.addWidget(self.predict_weight_label, 0, 1, 1, 1)

        self.predict_weight_path = QLineEdit(autil.get_cfg('Predict_cfg', 'predict_weight', value_type='path'),
                                             self.predictPage)
        self.predict_weight_path.setObjectName("predict_weight_path")
        self.predictLayout.addWidget(self.predict_weight_path, 0, 2, 1, 4)

        self.select_predict_weight = QPushButton("...", self.predictPage)
        self.select_predict_weight.setObjectName("select_predict_weight")
        self.select_predict_weight.clicked.connect(lambda: selectWeight(self.predict_weight_path))
        self.sizePolicy2.setHeightForWidth(self.select_predict_weight.sizePolicy().hasHeightForWidth())
        self.select_predict_weight.setSizePolicy(self.sizePolicy2)
        self.predictLayout.addWidget(self.select_predict_weight, 0, 6, 1, 1)

        self.source_cfg_label = QLabel("源文件存放路径", self.predictPage)
        self.source_cfg_label.setObjectName("source_cfg_label")
        self.sizePolicy2.setHeightForWidth(self.source_cfg_label.sizePolicy().hasHeightForWidth())
        self.source_cfg_label.setSizePolicy(self.sizePolicy2)
        self.predictLayout.addWidget(self.source_cfg_label, 1, 1, 1, 1)

        self.source_cfg_path = QLineEdit(autil.get_cfg('Predict_cfg', 'image_source', value_type='path'),
                                         self.predictPage)
        self.source_cfg_path.setObjectName("source_cfg_path")
        self.predictLayout.addWidget(self.source_cfg_path, 1, 2, 1, 4)

        self.select_source_cfg = QPushButton("...", self.predictPage)
        self.select_source_cfg.setObjectName("select_source_cfg")
        self.select_source_cfg.clicked.connect(lambda: selectPath(self.source_cfg_path))
        self.sizePolicy2.setHeightForWidth(self.select_source_cfg.sizePolicy().hasHeightForWidth())
        self.select_source_cfg.setSizePolicy(self.sizePolicy2)
        self.predictLayout.addWidget(self.select_source_cfg, 1, 6, 1, 1)

        self.default_yaml_info = QLabel("欲进行更详细的设置，请修改", self.predictPage)
        self.default_yaml_info.setObjectName("default_yaml_info")
        self.predictLayout.addWidget(self.default_yaml_info, 3, 5, 1, 1)

        self.default_yaml = QPushButton("default.yaml", self.predictPage)
        self.default_yaml.setObjectName("default_yaml")
        self.default_yaml.clicked.connect(lambda: openDefaultYAML())
        self.predictLayout.addWidget(self.default_yaml, 3, 6, 1, 1)

        self.save_predict = QPushButton("保存设置", self.predictPage)
        self.save_predict.setObjectName("save_predict")
        self.save_predict.clicked.connect(lambda: self.save_predict_config())
        self.predictLayout.addWidget(self.save_predict, 4, 6, 1, 1)

        self.start_predict = QPushButton("开始检测", self.predictPage)
        self.start_predict.setObjectName("start_predict")
        self.start_predict.setEnabled(False)
        self.start_predict.clicked.connect(lambda: self.launch_predict())
        self.predictLayout.addWidget(self.start_predict, 6, 6, 1, 1)

    def setup_labelimgPage(self):
        self.labelimgPage = QWidget()
        self.labelimgPage.setObjectName("labelimgPage")
        self.labelimgLayout = QGridLayout(self.labelimgPage)
        self.labelimgLayout.setObjectName("labelimgLayout")

        self.input_image_label = QLabel("图片路径", self.labelimgPage)
        self.input_image_label.setObjectName("input_image_label")
        self.sizePolicy2.setHeightForWidth(self.input_image_label.sizePolicy().hasHeightForWidth())
        self.input_image_label.setSizePolicy(self.sizePolicy2)
        self.labelimgLayout.addWidget(self.input_image_label, 0, 1, 1, 1)

        self.input_image_path = QLineEdit(autil.get_cfg("labelImg_cfg", "image_dir", value_type="path"),
                                          self.labelimgPage)
        self.input_image_path.setObjectName("input_image_path")
        self.labelimgLayout.addWidget(self.input_image_path, 0, 2, 1, 4)

        self.select_input_image = QPushButton("...", self.labelimgPage)
        self.select_input_image.setObjectName("select_input_image")
        self.select_input_image.clicked.connect(lambda: selectPath(self.input_image_path))
        self.sizePolicy2.setHeightForWidth(self.select_input_image.sizePolicy().hasHeightForWidth())
        self.select_input_image.setSizePolicy(self.sizePolicy2)
        self.labelimgLayout.addWidget(self.select_input_image, 0, 6, 1, 1)

        self.input_class_label = QLabel("类别文件", self.labelimgPage)
        self.input_class_label.setObjectName("input_class_label")
        self.sizePolicy2.setHeightForWidth(self.input_class_label.sizePolicy().hasHeightForWidth())
        self.input_class_label.setSizePolicy(self.sizePolicy2)
        self.labelimgLayout.addWidget(self.input_class_label, 1, 1, 1, 1)

        self.input_class_path = QLineEdit(autil.get_cfg("labelImg_cfg", "class_file", value_type="path"),
                                          self.labelimgPage)
        self.input_class_path.setObjectName("input_class_path")
        self.labelimgLayout.addWidget(self.input_class_path, 1, 2, 1, 4)

        self.select_input_class = QPushButton("...", self.labelimgPage)
        self.select_input_class.setObjectName("select_input_class")
        self.select_input_class.clicked.connect(lambda: selectTxt(self.input_class_path))
        self.sizePolicy2.setHeightForWidth(self.select_input_class.sizePolicy().hasHeightForWidth())
        self.select_input_class.setSizePolicy(self.sizePolicy2)
        self.labelimgLayout.addWidget(self.select_input_class, 1, 6, 1, 1)

        self.input_save_label = QLabel("保存路径", self.labelimgPage)
        self.input_save_label.setObjectName("input_save_label")
        self.sizePolicy2.setHeightForWidth(self.input_save_label.sizePolicy().hasHeightForWidth())
        self.input_save_label.setSizePolicy(self.sizePolicy2)
        self.labelimgLayout.addWidget(self.input_save_label, 3, 1, 1, 1)

        self.input_save_path = QLineEdit(autil.get_cfg("labelImg_cfg", "save_dir", value_type="path"),
                                         self.labelimgPage)
        self.input_save_path.setObjectName("input_save_path")
        self.labelimgLayout.addWidget(self.input_save_path, 3, 2, 1, 4)

        self.select_input_save = QPushButton("...", self.labelimgPage)
        self.select_input_save.setObjectName("select_input_save")
        self.select_input_save.clicked.connect(lambda: selectPath(self.input_save_path))
        self.sizePolicy2.setHeightForWidth(self.select_input_save.sizePolicy().hasHeightForWidth())
        self.select_input_save.setSizePolicy(self.sizePolicy2)
        self.labelimgLayout.addWidget(self.select_input_save, 3, 6, 1, 1)

        self.save_labelimg = QPushButton("保存设置", self.labelimgPage)
        self.save_labelimg.setObjectName("save_labelimg")
        self.save_labelimg.clicked.connect(lambda: self.save_labelimg_config())
        self.labelimgLayout.addWidget(self.save_labelimg, 4, 6, 1, 1)

        self.start_labelimg = QPushButton("开始标注", self.labelimgPage)
        self.start_labelimg.setObjectName("start_labelimg")
        self.start_labelimg.clicked.connect(lambda: self.launch_labelimg())
        self.labelimgLayout.addWidget(self.start_labelimg, 6, 6, 1, 1)

    def setup_settingPage(self):
        self.settingPage = QWidget()
        self.settingPage.setObjectName("settingPage")
        self.settingLayout = QGridLayout(self.settingPage)
        self.settingLayout.setObjectName("settingLayout")
        self.setting_label = QLabel("设置界面", self.settingPage)
        self.setting_label.setObjectName("setting_label")
        self.settingLayout.addWidget(self.setting_label)

    def setup_pageLayout(self):
        self.pageLayout = QGridLayout()
        self.pageLayout.setSpacing(0)
        self.pageLayout.setObjectName("pageLayout")
        self.pageLayout.setContentsMargins(0, 0, 0, 0)
        # setup MainWindow->centralWidget->RightLayout->pageLayout->stackedWidget
        self.stackedWidget = QStackedWidget(self.centralWidget)
        # setup MainWindow->centralWidget->RightLayout->pageLayout->stackedWidget->startupPage
        self.setup_startupPage()
        self.stackedWidget.addWidget(self.startupPage)
        # setup MainWindow->centralWidget->RightLayout->pageLayout->stackedWidget->datasetPage
        self.setup_datasetPage()
        self.stackedWidget.addWidget(self.datasetPage)
        # setup MainWindow->centralWidget->RightLayout->pageLayout->stackedWidget->trainPage
        self.setup_trainPage()
        self.stackedWidget.addWidget(self.trainPage)
        # setup MainWindow->centralWidget->RightLayout->pageLayout->stackedWidget->predictPage
        self.setup_predictPage()
        self.stackedWidget.addWidget(self.predictPage)
        # setup MainWindow->centralWidget->RightLayout->pageLayout->stackedWidget->labelimgPage
        self.setup_labelimgPage()
        self.stackedWidget.addWidget(self.labelimgPage)
        # setup MainWindow->centralWidget->RightLayout->pageLayout->stackedWidget->settingPage
        self.setup_settingPage()
        self.stackedWidget.addWidget(self.settingPage)

        self.pageLayout.addWidget(self.stackedWidget, 0, 0, 1, 1)
        self.RightLayout.addLayout(self.pageLayout)
        self.RightLayout.addWidget(self.ConsoleOutput)
        self.gridLayout.addLayout(self.RightLayout, 0, 2, 1, 1)

    def setup_buttons(self):
        self.ButtonWidget = QWidget(self.centralWidget)
        self.ButtonWidget.setObjectName("ButtonWidget")
        self.sizePolicy.setHeightForWidth(self.ButtonWidget.sizePolicy().hasHeightForWidth())
        self.ButtonWidget.setSizePolicy(self.sizePolicy)
        self.verticalLayout = QVBoxLayout(self.ButtonWidget)
        self.verticalLayout.setObjectName("verticalLayout")
        # setup MainWindow->centralWidget->ButtonWidget->startButton
        self.startupButton = QPushButton("开始", self.ButtonWidget)
        self.startupButton.setObjectName("startupButton")
        self.startupButton.clicked.connect(lambda: self.startup())
        self.verticalLayout.addWidget(self.startupButton)
        # setup MainWindow->centralWidget->ButtonWidget->datasetButton
        self.datasetButton = QPushButton("数据集处理", self.ButtonWidget)
        self.datasetButton.setObjectName("datasetButton")
        self.datasetButton.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))
        self.verticalLayout.addWidget(self.datasetButton)
        # setup MainWindow->centralWidget->ButtonWidget->trainButton
        self.trainButton = QPushButton("训练任务", self.ButtonWidget)
        self.trainButton.setObjectName("trainButton")
        self.trainButton.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(2))
        self.verticalLayout.addWidget(self.trainButton)
        # setup MainWindow->centralWidget->ButtonWidget->predictButton
        self.predictButton = QPushButton("检测任务", self.ButtonWidget)
        self.predictButton.setObjectName("predictButton")
        self.predictButton.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(3))
        self.verticalLayout.addWidget(self.predictButton)
        # setup MainWindow->centralWidget->ButtonWidget->labelimgButton
        self.labelimgButton = QPushButton("labelImg", self.ButtonWidget)
        self.labelimgButton.setObjectName("labelimgButton")
        self.labelimgButton.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(4))
        self.verticalLayout.addWidget(self.labelimgButton)
        # setup MainWindow->centralWidget->ButtonWidget->settingButton
        # TODO: 设置页面还没做...
        self.settingButton = QPushButton("设置", self.ButtonWidget)
        self.settingButton.setObjectName("settingButton")
        self.settingButton.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(5))
        self.verticalLayout.addWidget(self.settingButton)
        self.gridLayout.addWidget(self.ButtonWidget, 0, 0, 1, 1)

    def setup_divideLine(self):
        self.divideLine = QFrame(self.centralWidget)
        self.divideLine.setObjectName("divideLine")
        self.divideLine.setFrameShape(QFrame.VLine)
        self.divideLine.setFrameShadow(QFrame.Sunken)
        self.gridLayout.addWidget(self.divideLine, 0, 1, 1, 1)

    def setup_menuBar(self):
        menuBar = self.menuBar()
        aboutMenu = menuBar.addAction("关于")
        aboutMenu.triggered.connect(lambda: self.aboutWindow())

    def setupUI(self, MainWindow):
        # setup MainWindow
        if not MainWindow.objectName():
            MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowTitle("Auxiliary Tool for Labeling & Training & Predicting")
        MainWindow.resize(self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
        MainWindow.setMinimumSize(QSize(1024, 768))
        MainWindow.statusBar().showMessage("准备就绪")
        # setup MainWindow->centralWidget
        self.centralWidget = QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.gridLayout = QGridLayout(self.centralWidget)
        self.gridLayout.setObjectName("gridLayout")
        # setup MainWindow->centralWidget->RightLayout
        self.RightLayout = QVBoxLayout()
        self.RightLayout.setSpacing(9)
        self.RightLayout.setObjectName("RightLayout")
        self.RightLayout.setContentsMargins(-1, -1, -1, 0)
        # setup MainWindow->centralWidget->RightLayout->ConsoleOutput
        self.setup_console()
        # setup MainWindow->centralWidget->RightLayout->pageLayout
        self.setup_pageLayout()
        # setup MainWindow->centralWidget->ButtonWidget
        self.setup_buttons()
        # setup a line which divides RightLayout and ButtonWidget
        self.setup_divideLine()
        MainWindow.setCentralWidget(self.centralWidget)
        # setup a menubar
        self.setup_menuBar()


class EmittingStream(QObject):
    textWritten = pyqtSignal(str)

    def write(self, text):
        self.textWritten.emit(str(text))


class ControlBoard(UI_MainWindow):
    def __init__(self):
        super(ControlBoard, self).__init__()
        self.setupUI(self)
        sys.stdout = EmittingStream(textWritten=self.outputWritten)
        sys.stderr = EmittingStream(textWritten=self.outputWritten)
        self.train_thread = TrainThread()
        self.predict_thread = PredictThread()

    def startup(self):
        self.stackedWidget.setCurrentIndex(0)
        if QMessageBox.question(self, "开始", "开始运行？", QMessageBox.Yes, QMessageBox.No) == QMessageBox.Yes:
            print("开始运行")
            print("首先进行图片的标注，请在当前页面点击‘开始标注’以运行labelimg软件进行图片标注工作")
            print("您也可以在当前页面设置好图片文件夹的路径、classes.txt类别文件（如果有的话）的路径以及标签文件的保存路径")
            print("设置完成后请点击‘保存设置’，然后再点击‘开始标注’即可直接开始图片的标注工作")
            print("(以上设置并非强制性要求，您也可以进入labelimg软件后再打开图片文件夹以及设置保存目录)")
            print("在标注完成后，请点击‘下一步’以进行数据集的处理工作")
            self.sub_window = UI_SubWindow(stackedObject=self.stackedWidget)
            self.sub_window.show()
            self.stackedWidget.setCurrentIndex(4)
        return

    def showTipOnStatusBar(self, text):
        self.statusBar().showMessage(text)

    def outputWritten(self, text):
        cursor = self.ConsoleOutput.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.insertText(text)
        self.ConsoleOutput.setTextCursor(cursor)
        self.ConsoleOutput.ensureCursorVisible()

    def changePercentResult(self):
        self.train_percent_result.setText(str(self.train_percent.value() / 100))

    def save_dataset_config(self):
        if not os.path.exists(self.dataset_path.text()):
            print("ERROR: 数据集文件夹不存在！请检查数据集路径")
            return
        if not os.path.exists(self.image_path.text()):
            print("ERROR: 图片文件夹不存在！请检查图片文件夹路径")
            return
        if not os.path.exists(self.label_path.text()):
            print("ERROR: 标签文件夹不存在！请检查标签文件夹路径")
            return
        autil.set_cfg("DataSet_cfg", "dataset", self.dataset_path.text())
        autil.set_cfg("DataSet_cfg", "image", self.image_path.text())
        autil.set_cfg("DataSet_cfg", "label", self.label_path.text())
        autil.set_cfg("DataSet_cfg", "train_percent", self.train_percent_result.text())
        print("成功将数据集设置保存到 " + os.path.abspath("./setup.ini"))

    def save_train_config(self):
        if not os.path.exists(self.train_weight_path.text()):
            print("ERROR: 权重文件不存在！请检查权重文件路径")
            return
        if not os.path.exists(self.dataset_cfg_path.text()):
            print("ERROR: 数据集配置文件不存在！请检查数据集配置文件路径")
            return
        autil.set_cfg("Train_cfg", "train_weight", self.train_weight_path.text())
        autil.set_cfg("Train_cfg", "dataset_cfg", self.dataset_cfg_path.text())
        autil.set_cfg("Train_cfg", "train_epochs", self.epoch_val.text())
        autil.set_cfg("Train_cfg", "train_batch", self.batch_val.text())
        autil.set_cfg("Train_cfg", "train_device", self.device_val.text())
        print("成功将训练设置保存到 " + os.path.abspath("./setup.ini"))
        self.start_train.setEnabled(True)

    def launch_train(self):
        self.train_thread.start()
        if self.train_thread.isFinished():
            del self.train_thread
        return

    def save_predict_config(self):
        if not os.path.exists(self.predict_weight_path.text()):
            print("ERROR: 权重文件不存在！请检查权重文件路径")
            return
        if not os.path.exists(self.source_cfg_path.text()):
            print("ERROR: 检测源文件不存在！请检查源文件")
            return
        autil.set_cfg("Predict_cfg", "predict_weight", self.predict_weight_path.text())
        autil.set_cfg("Predict_cfg", "image_source", self.source_cfg_path.text())
        print("成功将检测设置保存到 " + os.path.abspath("./setup.ini"))
        self.start_predict.setEnabled(True)

    def launch_predict(self):
        self.predict_thread.start()
        if self.predict_thread.isFinished():
            print("检测结束")
        return

    def save_labelimg_config(self):
        if not os.path.exists(self.input_image_path.text()):
            print("WARNING: 图片文件夹路径不存在！labelimg可能会以默认配置启动")
        if not os.path.exists(self.input_class_path.text()):
            print("WARNING: 类别文件不存在！labelimg可能会以默认配置启动")
        if not os.path.exists(self.input_save_path.text()):
            print("WARNING: 保存路径不存在！labelimg可能会以默认配置启动")
        autil.set_cfg("labelImg_cfg", "image_dir", self.input_image_path.text())
        autil.set_cfg("labelImg_cfg", "class_file", self.input_class_path.text())
        autil.set_cfg("labelImg_cfg", "save_dir", self.input_save_path.text())
        print("成功将labelimg设置保存到 " + os.path.abspath("./setup.ini"))

    def launch_labelimg(self):
        print("正在运行labelimg")
        labelwin = labelimgWindow(default_filename=autil.get_cfg('labelImg_cfg', 'image_dir', value_type='path'),
                                  default_prefdef_class_file=autil.get_cfg('labelImg_cfg', 'class_file',
                                                                           value_type='path'),
                                  default_save_dir=autil.get_cfg('labelImg_cfg', 'save_dir', value_type='path'))
        labelwin.show()
        return

    def aboutWindow(self):
        QMessageBox.about(self, "关于", "Auxiliary Tool for Labeling & Training & Predicting v0.55\n\n"
                                        "Training & Predicting based on ultralytics/YOLOv8\n"
                                        "repository site: https://github.com/ultralytics/ultralytics\n\n"
                                        "Labeling based on HumanSignal/labelImg\n"
                                        "repository site: https://github.com/HumanSignal/labelImg\n\n")


class TrainThread(QThread):
    def __init__(self):
        super(TrainThread, self).__init__()

    def run(self):
        print("正在准备开始训练任务...（初次运行耗时较长，请稍候）")
        autil.launch_train(autil.get_cfg('Train_cfg', 'train_weight', value_type='path'),
                           autil.get_cfg('Train_cfg', 'dataset_cfg', value_type='path'),
                           autil.get_cfg('Train_cfg', 'train_epochs', value_type='str'),
                           autil.get_cfg('Train_cfg', 'train_batch', value_type='str'),
                           autil.get_cfg('Train_cfg', 'train_device', value_type='str'))
        return


class PredictThread(QThread):
    def __init__(self):
        super(PredictThread, self).__init__()

    def run(self):
        print("正在准备开始检测任务...（初次运行耗时较长，请稍候）")
        autil.launch_predict(autil.get_cfg('Predict_cfg', 'predict_weight', value_type='path'),
                             autil.get_cfg('Predict_cfg', 'image_source', value_type='path'))

        return


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = ControlBoard()
    win.show()
    sys.exit(app.exec_())
