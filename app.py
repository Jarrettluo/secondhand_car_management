#!/usr/bin/env python
# _*_coding:utf-8 _*_
"""
@Time    :   22:10
@Auther  : Jarrett
@FileName: app
@Software: PyCharm
"""

import os
import sys

"""
以下引用是由于使用PyInstaller进行软件打包时出现bug。
参考链接：https://bbs.csdn.net/topics/392428917
"""
if hasattr(sys, 'frozen'):
    os.environ['PATH'] = sys._MEIPASS + ";" + os.environ['PATH']
    import fix_qt_import_error

import qtawesome
from PyQt5.QtGui import QCursor
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox
from PyQt5.Qt import QPixmap
from PyQt5.QtCore import Qt, pyqtSlot, QSize

from panel1 import Panel1
from panel2 import Panel2
from panel3 import Panel3
from panel4 import Panel4


# from test2 import LeftTabWidget


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        loadUi("ui_source/main.ui", self)

        self.title.setText("二手车管理软件 樱桃智库开发")
        # self.setStyleSheet("#MainWindow{background-color:#feffff}")

        pixMap = QPixmap("style/图片1.png").scaled(self.label.width(), self.label.height())
        self.label.setPixmap(pixMap)

        # 设置窗口透明度，取值0-1
        # self.setWindowOpacity(0.5)

        a = Panel1()
        self.b = Panel2()
        self.c = Panel3()
        self.d = Panel4()
        # d = c

        self.stackedWidget.addWidget(a)
        self.stackedWidget.addWidget(self.b)
        self.stackedWidget.addWidget(self.c)
        self.stackedWidget.addWidget(self.d)

        self.stackedWidget.setCurrentIndex(2)

        self.pushButton.clicked.connect(self.panel_1)
        self.pushButton_2.clicked.connect(self.panel_2)
        self.pushButton_3.clicked.connect(self.panel_3)
        self.pushButton_4.clicked.connect(self.panel_4)

        self.statusBar().hide()
        self.resize(1200, 920)
        self.setFixedSize(1200, 920)

        self.setWindowFlags(Qt.FramelessWindowHint)

        spin_icon = qtawesome.icon('mdi.minus', color='#1e704d')
        self.xxx.setIcon(spin_icon)  # 设置图标
        self.xxx.setIconSize(QSize(18, 18))
        self.xxx.setText('')
        self.xxx.setGeometry(920, 0, 30, 30)
        self.xxx.setToolTip('最小化')

        styling_icon = qtawesome.icon('mdi.close', color='#1e704d')
        self.yyy.setIcon(styling_icon)  # 设置图标
        self.yyy.setIconSize(QSize(18, 18))
        self.yyy.setText('')
        self.yyy.setGeometry(952, 0, 30, 30)
        self.yyy.setToolTip('关闭窗口')

        spin_icon = qtawesome.icon('fa5.plus-square', color='#687681')  # #d4f1ef        # 入库登记
        self.pushButton.setIcon(spin_icon)  # 设置图标
        self.pushButton.setIconSize(QSize(25, 25))

        spin_icon = qtawesome.icon('fa5.edit', color='#ac395d')  # #d4f1ef        # 车辆整备
        self.pushButton_2.setIcon(spin_icon)  # 设置图标
        self.pushButton_2.setIconSize(QSize(25, 25))

        spin_icon = qtawesome.icon('fa5.handshake', color='#166f6b')  # #d4f1ef        #  销售
        self.pushButton_3.setIcon(spin_icon)  # 设置图标
        self.pushButton_3.setIconSize(QSize(25, 25))

        spin_icon = qtawesome.icon('fa5.calendar-check', color='#1e704d')  # #d4f1ef
        self.pushButton_4.setIcon(spin_icon)  # 设置图标
        self.pushButton_4.setIconSize(QSize(25, 25))

        spin_icon = qtawesome.icon('ei.home-alt', color='#6074c3')  # #d4f1ef
        self.main_copyright.setIcon(spin_icon)  # 设置图标
        self.main_copyright.setIconSize(QSize(25, 25))

    def panel_1(self):
        self.stackedWidget.setCurrentIndex(2)
        self.pushButton.setEnabled(False)
        self.pushButton_2.setEnabled(True)
        self.pushButton_3.setEnabled(True)
        self.pushButton_4.setEnabled(True)

    def panel_2(self):
        self.stackedWidget.setCurrentIndex(3)
        self.b.init_all_car()
        self.pushButton.setEnabled(True)
        self.pushButton_2.setEnabled(False)
        self.pushButton_3.setEnabled(True)
        self.pushButton_4.setEnabled(True)

    def panel_3(self):
        self.stackedWidget.setCurrentIndex(4)
        self.c.init_all_car()
        self.pushButton.setEnabled(True)
        self.pushButton_2.setEnabled(True)
        self.pushButton_3.setEnabled(False)
        self.pushButton_4.setEnabled(True)

    def panel_4(self):
        self.stackedWidget.setCurrentIndex(5)
        self.d.all_car_selled()
        self.pushButton.setEnabled(True)
        self.pushButton_2.setEnabled(True)
        self.pushButton_3.setEnabled(True)
        self.pushButton_4.setEnabled(False)

    #
    #
    # def show_panel(self):  # 按钮信号
    #     dic = {
    #         "pushButton": 0,
    #         "pushButton_2": 1,
    #         "pushButton_3": 2,
    #     }
    #     print("hahahah")
    #     # 三个按钮信号都绑定一个槽函数 show_panel
    #     index = dic[self.sender().objectName()]
    #     print(index)
    #     print(self.sender().objectName())
    #     # 获取当前点击按钮的名称，结合字典获取索引，通过索引设置堆叠布局展示的页面。
    #     self.stackedWidget.setCurrentIndex(index)
    #
    # def buttonClicked(self):
    #     sender = self.sender()
    #     self.statusbar.showMessage(sender.text() + ' ' + sender.objectName() + '被点击了')

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.m_flag = True
            self.m_Position = event.globalPos() - self.pos()
            event.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))

    def mouseMoveEvent(self, QMouseEvent):
        if Qt.LeftButton and self.m_flag:
            self.move(QMouseEvent.globalPos() - self.m_Position)
            QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        self.m_flag = False
        self.setCursor(QCursor(Qt.ArrowCursor))

    @pyqtSlot()
    def on_yyy_clicked(self):
        """
        关闭窗口
        """
        self.close()

    @pyqtSlot()
    def on_xxx_clicked(self):
        """
        最小化窗口
        """
        self.showMinimized()

    @pyqtSlot()
    def on_main_copyright_clicked(self):
        QMessageBox.about(self, '版权信息', '该软件由樱桃智库开发，联系电话+8615008201329。')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    with open('./style_source/app_style.qss', encoding='utf-8') as f:
        qss_style = f.read()
    window.setStyleSheet(qss_style)
    window.show()
    sys.exit(app.exec_())
