#!/usr/bin/env python
# _*_coding:utf-8 _*_
"""
@Time    :   22:56
@Auther  : Jarrett
@FileName: panel_1
@Software: PyCharm
"""

import sys

from PyQt5.QtGui import QIntValidator
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QMainWindow, QApplication
from SQLite_tools import SQLiteTools
from PyQt5.QtCore import QDate, QThread, pyqtSignal, Qt


class panel2_Example(QThread):
    signal = pyqtSignal(list)  # 括号里填写信号传递的参数

    def __init__(self, args):
        super().__init__()
        self.arg = args

    def __del__(self):
        self.wait()

    def run(self):
        # 进行任务操作
        # print(self.arg)
        panel1 = Panel2()
        panel1.current_car_chepai = panel1.panel2_sqlite.getSQLtableValue_by_column_value(panel1.table_name, 'car_code', self.arg)
        pasassafs = panel1.panel2_sqlite.getSQLtableRow(panel1.table_name, str(panel1.current_car_chepai[0]))
        # print(pasassafs)
        panel1.panel2_line_edit2.setText('')
        self.signal.emit(pasassafs)  # 发射信号

class panel2_Example2(QThread):
    signal = pyqtSignal(list)  # 括号里填写信号传递的参数

    def __init__(self, args):
        super().__init__()
        self.arg = args

    def __del__(self):
        self.wait()

    def run(self):
        # 进行任务操作
        panel2 = Panel2()
        panel2.current_car_chepai = panel2.panel2_sqlite.getSQLtableValue_by_column_value(panel2.table_name, 'license_plate', self.arg)
        if len(panel2.current_car_chepai) > 0:
            pasassafs = panel2.panel2_sqlite.getSQLtableRow(panel2.table_name, str(panel2.current_car_chepai[0]))
        else:
            pasassafs = [1]
        self.signal.emit(pasassafs)  # 发射信号


class panel2_Example3(QThread):
    signal = pyqtSignal()  # 括号里填写信号传递的参数

    def __init__(self, args):
        super().__init__()
        self.arg = args

    def __del__(self):
        self.wait()

    def run(self):
        # 进行任务操作
        panel2 = Panel2()
        value = panel2.panel2_sqlite.getSQLtableRowNum(panel2.spend_table_name)  # 获取所有/行
        # panel2.write_to_database(self.arg)
        value = panel2.panel2_sqlite.getSQLtableRowNum(panel2.spend_table_name)  # 获取所有/行
        # print('这里是写入到数据库的value', value)
        args_list = self.arg
        panel2.panel2_sqlite.addSQLtableRow(panel2.spend_table_name, (value + 1))
        panel2.panel2_sqlite.setSQLtableValue(panel2.spend_table_name, "item", value, args_list[0])
        panel2.panel2_sqlite.setSQLtableValue(panel2.spend_table_name, "money", value, args_list[1])
        panel2.panel2_sqlite.setSQLtableValue(panel2.spend_table_name, "car_host", value, args_list[4])
        panel2.panel2_sqlite.setSQLtableValue(panel2.spend_table_name, 'person', value, args_list[2])
        panel2.panel2_sqlite.setSQLtableValue(panel2.spend_table_name, 'time', value, args_list[3])
        self.signal.emit()  # 发射信号

class panel2_Example4(QThread):
    signal = pyqtSignal(list)  # 括号里填写信号传递的参数

    def __init__(self, args):
        super().__init__()
        self.arg = args

    def __del__(self):
        self.wait()

    def run(self):
        # 进行任务操作
        panel2 = Panel2()

        # all_cars = panel2.panel2_sqlite.getSQLtableColumn(panel2.table_name, "car_code")
        # all_cars.reverse()  # 列表反转
        # panel2.all_car = all_cars
        # panel2.panel2_combo_box1.addItems(all_cars)

        panel2.search_result = panel2.panel2_sqlite.getSQLtableValue_by_column_value(panel2.spend_table_name, 'car_host', self.arg)
        result_list = []    # 用于返回查询到的结果
        if len(panel2.search_result) > 0:
            for car_index in panel2.search_result:
                info = panel2.panel2_sqlite.getSQLtableRow(panel2.spend_table_name, str(car_index))
                result_list.append(list(info))
            result_list.append([None])
        else:
            result_list = [None]
        self.signal.emit(result_list)  # 发射信号

class panel2_Example5(QThread):
    signal = pyqtSignal(list)  # 括号里填写信号传递的参数

    def __init__(self):
        super().__init__()

    def __del__(self):
        self.wait()

    def run(self):
        # print('这里进入线程中操作了')
        # 进行任务操作
        panel2 = Panel2()
        all_car = panel2.panel2_sqlite.getSQLtableColumn(panel2.table_name, "car_code")
        all_car.reverse()  # 列表反转
        self.signal.emit(all_car)  # 发射信号

class Panel2(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        loadUi("ui_source/panel2.ui", self)

        self.db_name = './database.db'
        self.table_name = 'all_car'
        self.spend_table_name = 'spend'
        self.panel2_sqlite = SQLiteTools()
        self.connect_db()

        self.panel2_combo_box1.setMaxVisibleItems(10)   # 设置最大下拉数量
        self.panel2_combo_box1.activated.connect(self.change_index)

        self.change_car_code()
        self.panel2_line_edit1.editingFinished.connect(self.search_edit1)
        self.panel2_line_edit2.editingFinished.connect(self.search_edit2)
        self.panel2_button1.clicked.connect(self.click_search)  # 点击搜索按钮
        self.current_car = self.panel2_combo_box1.currentText()

        self.start_record()  # 开始记录，这里主要用于将提交按钮进行同步
        self.init_panel_input() # 初始化输入框

        self.statusBar().hide()

        # spin_icon = qtawesome.icon('fa5.handshake', color='#166f6b')  # #d4f1ef        #  销售
        # self.panel2_title.setIcon(spin_icon)  # 设置图标
        # self.panel2_title.setIconSize(QSize(25, 25))
        self.panel2_title.setAlignment(Qt.AlignLeft)
        self.panel2_title.setText('车辆整备')


    def init_all_car(self):
        self.panel2_thread6 = panel2_Example5()
        self.panel2_thread6.signal.connect(self.panel2_call_back_6)
        self.panel2_thread6.start()  # 启动线程

    def panel2_call_back_6(self, all_car):
        self.panel2_combo_box1.clear()
        self.all_car = all_car
        self.panel2_combo_box1.addItems(self.all_car)
        # print(self.all_car)


    # 搜索输入初始化部分
    def change_index(self):
        self.current_car = self.panel2_combo_box1.currentText()
        self.panel2_thread = panel2_Example(self.current_car)
        self.panel2_thread.signal.connect(self.panel2_call_back)
        self.panel2_thread.start()  # 启动线程
        self.panel2_line_edit1.setStyleSheet("border:1px solid black;")

    def panel2_call_back(self, xxx):
        # self.current_car = self.panel2_combo_box1.currentText()
        self.panel2_line_edit1.setText(self.current_car)
        self.panel2_line_edit2.setText(xxx[1])
        self.reset_input_close() # 重置input, 关闭按钮

    def change_car_code(self):
        self.current_car = self.panel2_combo_box1.currentText()
        self.panel2_line_edit1.setText(self.current_car)

    def search_edit1(self):
        edit1_car_code = self.panel2_line_edit1.text()
        if edit1_car_code in self.all_car:
            code_index = self.all_car.index(edit1_car_code)
            self.panel2_combo_box1.setCurrentIndex(code_index)
            self.panel2_line_edit1.setStyleSheet("border:1px solid black;")
        else:
            self.panel2_line_edit1.setText('')
            self.panel2_line_edit1.setStyleSheet("border:1px solid red;")

    def search_edit2(self):
        che_pai = self.panel2_line_edit2.text() # 获取收入的车牌
        if che_pai:
            self.panel2_thread2 = panel2_Example2(che_pai)
            self.panel2_thread2.signal.connect(self.panel2_call_back2)
            self.panel2_thread2.start()  # 启动线程
        else:
            pass

    def panel2_call_back2(self, args):
        car_code = args[0]
        if car_code in self.all_car:
            xx = self.all_car.index(car_code)
            self.panel2_combo_box1.setCurrentIndex(xx)
            self.panel2_line_edit2.setStyleSheet("border:1px solid black;")
        else:
            self.panel2_line_edit2.setStyleSheet("border:1px solid red;")

    # 搜索输入初始化部分

    def click_search(self):
        """
        点击搜索按钮的函数
        :return:
        """
        self.panel2_thread4 = panel2_Example4(self.current_car)
        self.panel2_thread4.signal.connect(self.panel2_call_back_4)
        self.panel2_thread4.start()  # 启动线程

    def panel2_call_back_4(self, spend_list):
        self.open_button()  # 打开按钮
        # 点击搜索以后的回调函数

        # self.change_index() # 返回车牌结果
        self.current_car = self.panel2_combo_box1.currentText()
        self.panel2_thread5 = panel2_Example(self.current_car)
        self.panel2_thread5.signal.connect(self.panel2_call_back_5)
        self.panel2_thread5.start()  # 启动线程

        if spend_list[0]:
            # 查询结果去设置每一项
            self.set_item_value(spend_list)
        else:
            # 如果没有查询到，那么就清空输入框，重置
            self.reset_input_open()

    def panel2_call_back_5(self, args):
        """
        用于重置车牌
        :param args:
        :return:
        """
        self.panel2_line_edit2.setText(args[1])
        self.panel2_line_edit2.setStyleSheet("border:1px solid black;")

    def reset_input_open(self):
        item_list = ['item1', 'item2', 'item3', 'item4', 'item5', 'item6', 'item7', 'item8', 'item9',
                     'item10', 'item11', 'item12', 'item13']
        price_lice = ['price1', 'price2', 'price3', 'price4', 'price5', 'price6', 'price7', 'price8',
                      'price9', 'price10', 'price11', 'price12', 'price13']
        person_list = ['comboBox',  'comboBox_2', 'comboBox_3', 'comboBox_4', 'comboBox_5',
                       'comboBox_6', 'comboBox_7', 'comboBox_8', 'comboBox_9', 'comboBox_10',
                       'comboBox_11', 'comboBox_12', 'comboBox_13']
        dated_list = ['dateEdit', 'dateEdit_2','dateEdit_3', 'dateEdit_4', 'dateEdit_5', 'dateEdit_6',
                      'dateEdit_7','dateEdit_8', 'dateEdit_9', 'dateEdit_10', 'dateEdit_11',
                      'dateEdit_12', 'dateEdit_13']
        button_list = ['prepare_1', 'prepare_2', 'prepare_3', 'prepare_4', 'prepare_5', 'prepare_6', 'prepare_7',
                       'prepare_8', 'prepare_9', 'prepare_10', 'prepare_11', 'prepare_12', 'prepare_13']
        for i in range(len(item_list)):
            eval('self.' + item_list[i]).setText('')
            eval('self.' + price_lice[i]).setText('')
            eval('self.' + person_list[i]).setCurrentIndex(0)
            eval('self.' + dated_list[i]).setDate(QDate.currentDate())
            eval('self.' + button_list[i]).setEnabled(True)

    def reset_input_close(self):
        item_list = ['item1', 'item2', 'item3', 'item4', 'item5', 'item6', 'item7', 'item8', 'item9',
                     'item10', 'item11', 'item12', 'item13']
        price_lice = ['price1', 'price2', 'price3', 'price4', 'price5', 'price6', 'price7', 'price8',
                      'price9', 'price10', 'price11', 'price12', 'price13']
        person_list = ['comboBox',  'comboBox_2', 'comboBox_3', 'comboBox_4', 'comboBox_5',
                       'comboBox_6', 'comboBox_7', 'comboBox_8', 'comboBox_9', 'comboBox_10',
                       'comboBox_11', 'comboBox_12', 'comboBox_13']
        dated_list = ['dateEdit', 'dateEdit_2','dateEdit_3', 'dateEdit_4', 'dateEdit_5', 'dateEdit_6',
                      'dateEdit_7','dateEdit_8', 'dateEdit_9', 'dateEdit_10', 'dateEdit_11',
                      'dateEdit_12', 'dateEdit_13']
        button_list = ['prepare_1', 'prepare_2', 'prepare_3', 'prepare_4', 'prepare_5', 'prepare_6', 'prepare_7',
                       'prepare_8', 'prepare_9', 'prepare_10', 'prepare_11', 'prepare_12', 'prepare_13']
        for i in range(len(item_list)):
            eval('self.' + item_list[i]).setText('')
            eval('self.' + price_lice[i]).setText('')
            eval('self.' + person_list[i]).setCurrentIndex(0)
            eval('self.' + dated_list[i]).setDate(QDate.currentDate())
            eval('self.' + button_list[i]).setEnabled(False)

    def open_button(self):
        button_list = ['prepare_1', 'prepare_2', 'prepare_3', 'prepare_4', 'prepare_5', 'prepare_6', 'prepare_7',
                       'prepare_8', 'prepare_9', 'prepare_10', 'prepare_11', 'prepare_12', 'prepare_13']
        for i in range(len(button_list)):
            eval('self.' + button_list[i]).setEnabled(True)

    def set_item_value(self, spend_list):
        item_list = ['item1', 'item2', 'item3', 'item4', 'item5', 'item6', 'item7', 'item8', 'item9',
                     'item10', 'item11', 'item12', 'item13']
        price_lice = ['price1', 'price2', 'price3', 'price4', 'price5', 'price6', 'price7', 'price8',
                      'price9', 'price10', 'price11', 'price12', 'price13']
        person_list = ['comboBox',  'comboBox_2', 'comboBox_3', 'comboBox_4', 'comboBox_5',
                       'comboBox_6', 'comboBox_7', 'comboBox_8', 'comboBox_9', 'comboBox_10',
                       'comboBox_11', 'comboBox_12', 'comboBox_13']
        dated_list = ['dateEdit', 'dateEdit_2','dateEdit_3', 'dateEdit_4', 'dateEdit_5', 'dateEdit_6',
                      'dateEdit_7','dateEdit_8', 'dateEdit_9', 'dateEdit_10', 'dateEdit_11',
                      'dateEdit_12', 'dateEdit_13']
        button_list = ['prepare_1', 'prepare_2', 'prepare_3', 'prepare_4', 'prepare_5', 'prepare_6', 'prepare_7',
                       'prepare_8', 'prepare_9', 'prepare_10', 'prepare_11', 'prepare_12', 'prepare_13']

        spend_list = spend_list[0:-1]
        spend_list = [[row[i] for row in spend_list] for i in range(len(spend_list[0]))]

        for i in range(len(spend_list[0])): # 项目输入框
            eval('self.' + item_list[i]).setText(spend_list[0][i])

        for j in range(len(spend_list[1])): # 项目价格
            eval('self.' + price_lice[j]).setText(str(spend_list[1][j]))
            # print(j)

        for k in range(len(spend_list[3])): # 付款人
            # eval('self.' + person_list[k]).addItem(spend_list[3][k])
            person = spend_list[3][k]
            if person == '自筹':
                i = 0
            elif person == '他人':
                i = 1
            else:
                i = 2
            eval('self.' + person_list[k]).setCurrentIndex(i)

        for m in range(len(spend_list[4])): # 谁谁
            time_str = spend_list[4][m]
            time_list = time_str.split('/')
            eval('self.' + dated_list[m]).setDate(QDate(int(time_list[0]), int(time_list[1]), int(time_list[2])))
            eval('self.' + button_list[m]).setEnabled(False)


    def init_panel_input(self):
        item_list = ['item1', 'item2', 'item3', 'item4', 'item5', 'item6', 'item7', 'item8', 'item9',
                     'item10', 'item11', 'item12', 'item13']
        price_lice = ['price1', 'price2', 'price3', 'price4', 'price5', 'price6', 'price7', 'price8',
                      'price9', 'price10', 'price11', 'price12', 'price13']
        person_list = ['comboBox',  'comboBox_2', 'comboBox_3', 'comboBox_4', 'comboBox_5',
                       'comboBox_6', 'comboBox_7', 'comboBox_8', 'comboBox_9', 'comboBox_10',
                       'comboBox_11', 'comboBox_12', 'comboBox_13']
        dated_list = ['dateEdit', 'dateEdit_2','dateEdit_3', 'dateEdit_4', 'dateEdit_5', 'dateEdit_6',
                      'dateEdit_7','dateEdit_8', 'dateEdit_9', 'dateEdit_10', 'dateEdit_11',
                      'dateEdit_12', 'dateEdit_13']
        button_list = ['prepare_1', 'prepare_2', 'prepare_3', 'prepare_4', 'prepare_5', 'prepare_6', 'prepare_7',
                       'prepare_8', 'prepare_9', 'prepare_10', 'prepare_11', 'prepare_12', 'prepare_13']

        for i in range(len(price_lice)):
            eval('self.' + item_list[i]).setPlaceholderText('输入整备项目，如：洗车')
            eval('self.' + price_lice[i]).setValidator(QIntValidator())
            eval('self.' + person_list[i]).setCurrentIndex(0)
            eval('self.' + dated_list[i]).setDate(QDate.currentDate())
            eval('self.' + dated_list[i]).setCalendarPopup(True)  # 设置日历弹出
            eval('self.' + button_list[i]).setEnabled(False)



    def start_record(self):
        """
        初始化用于链接函数
        :return:
        """
        self.prepare_1.clicked.connect(self.prepare1)
        self.prepare_2.clicked.connect(self.prepare2)
        self.prepare_3.clicked.connect(self.prepare3)
        self.prepare_4.clicked.connect(self.prepare4)
        self.prepare_5.clicked.connect(self.prepare5)
        self.prepare_6.clicked.connect(self.prepare6)
        self.prepare_7.clicked.connect(self.prepare7)
        self.prepare_8.clicked.connect(self.prepare8)
        self.prepare_9.clicked.connect(self.prepare9)
        self.prepare_10.clicked.connect(self.prepare10)
        self.prepare_11.clicked.connect(self.prepare11)
        self.prepare_12.clicked.connect(self.prepare12)
        self.prepare_13.clicked.connect(self.prepare13)


    def connect_db(self):
        self.panel2_sqlite.createConnection(self.db_name)


    def prepare1(self):
        item = self.item1.text()
        price = self.price1.text()
        if item and price:
            person = self.comboBox.currentText()
            date_str = self.dateEdit.text()
            self.panel2_thread3 = panel2_Example3([item, price, person, date_str, self.current_car])
            self.panel2_thread3.signal.connect(self.panel2_call_back_3)
            self.panel2_thread3.start()  # 启动线程
            self.prepare_1.setEnabled(False)
        pass

    def panel2_call_back_3(self):
        pass

    def prepare2(self):
        item = self.item2.text()
        price = self.price2.text()
        if item and price:
            person = self.comboBox_2.currentText()
            date_str = self.dateEdit_2.text()
            self.panel2_thread7 = panel2_Example3([item, price, person, date_str, self.current_car])
            self.panel2_thread7.signal.connect(self.panel2_call_back_3)
            self.panel2_thread7.start()  # 启动线程
            self.prepare_2.setEnabled(False)
        pass

    def prepare3(self):
        item = self.item3.text()
        price = self.price3.text()
        if item and price:
            person = self.comboBox_3.currentText()
            date_str = self.dateEdit_3.text()
            self.panel2_thread8 = panel2_Example3([item, price, person, date_str, self.current_car])
            self.panel2_thread8.signal.connect(self.panel2_call_back_3)
            self.panel2_thread8.start()  # 启动线程
            self.prepare_3.setEnabled(False)
        pass

    def prepare4(self):
        item = self.item4.text()
        price = self.price4.text()
        if item and price:
            person = self.comboBox_4.currentText()
            date_str = self.dateEdit_4.text()
            self.panel2_thread9 = panel2_Example3([item, price, person, date_str, self.current_car])
            self.panel2_thread9.signal.connect(self.panel2_call_back_3)
            self.panel2_thread9.start()  # 启动线程
            self.prepare_4.setEnabled(False)
        pass

    def prepare5(self):
        item = self.item5.text()
        price = self.price5.text()
        if item and price:
            person = self.comboBox_5.currentText()
            date_str = self.dateEdit_5.text()
            self.panel2_thread10 = panel2_Example3([item, price, person, date_str, self.current_car])
            self.panel2_thread10.signal.connect(self.panel2_call_back_3)
            self.panel2_thread10.start()  # 启动线程
            self.prepare_5.setEnabled(False)
        pass

    def prepare6(self):
        item = self.item6.text()
        price = self.price6.text()
        if item and price:
            person = self.comboBox_6.currentText()
            date_str = self.dateEdit_6.text()
            self.panel2_thread11 = panel2_Example3([item, price, person, date_str, self.current_car])
            self.panel2_thread11.signal.connect(self.panel2_call_back_3)
            self.panel2_thread11.start()  # 启动线程
            self.prepare_6.setEnabled(False)
        pass

    def prepare7(self):
        item = self.item7.text()
        price = self.price7.text()
        if item and price:
            person = self.comboBox_7.currentText()
            date_str = self.dateEdit_7.text()
            self.panel2_thread12 = panel2_Example3([item, price, person, date_str, self.current_car])
            self.panel2_thread12.signal.connect(self.panel2_call_back_3)
            self.panel2_thread12.start()  # 启动线程
            self.prepare_7.setEnabled(False)
        pass

    def prepare8(self):
        item = self.item8.text()
        price = self.price8.text()
        if item and price:
            person = self.comboBox_8.currentText()
            date_str = self.dateEdit_8.text()
            self.panel2_thread13 = panel2_Example3([item, price, person, date_str, self.current_car])
            self.panel2_thread13.signal.connect(self.panel2_call_back_3)
            self.panel2_thread13.start()  # 启动线程
            self.prepare_8.setEnabled(False)
        pass

    def prepare9(self):
        item = self.item9.text()
        price = self.price9.text()
        if item and price:
            person = self.comboBox_9.currentText()
            date_str = self.dateEdit_9.text()
            self.panel2_thread14 = panel2_Example3([item, price, person, date_str, self.current_car])
            self.panel2_thread14.signal.connect(self.panel2_call_back_3)
            self.panel2_thread14.start()  # 启动线程
            self.prepare_9.setEnabled(False)
        pass

    def prepare10(self):
        item = self.item10.text()
        price = self.price10.text()
        if item and price:
            person = self.comboBox_10.currentText()
            date_str = self.dateEdit_10.text()
            self.panel2_thread15 = panel2_Example3([item, price, person, date_str, self.current_car])
            self.panel2_thread15.signal.connect(self.panel2_call_back_3)
            self.panel2_thread15.start()  # 启动线程
            self.prepare_10.setEnabled(False)
        pass

    def prepare11(self):
        item = self.item11.text()
        price = self.price11.text()
        if item and price:
            person = self.comboBox_11.currentText()
            date_str = self.dateEdit_11.text()
            self.panel2_thread16 = panel2_Example3([item, price, person, date_str, self.current_car])
            self.panel2_thread16.signal.connect(self.panel2_call_back_3)
            self.panel2_thread16.start()  # 启动线程
            self.prepare_11.setEnabled(False)
        pass

    def prepare12(self):
        item = self.item12.text()
        price = self.price12.text()
        if item and price:
            person = self.comboBox_12.currentText()
            date_str = self.dateEdit_12.text()
            self.panel2_thread17 = panel2_Example3([item, price, person, date_str, self.current_car])
            self.panel2_thread17.signal.connect(self.panel2_call_back_3)
            self.panel2_thread17.start()  # 启动线程
            self.prepare_12.setEnabled(False)
        pass

    def prepare13(self):
        item = self.item13.text()
        price = self.price13.text()
        if item and price:
            person = self.comboBox_13.currentText()
            date_str = self.dateEdit_13.text()
            self.panel2_thread18 = panel2_Example3([item, price, person, date_str, self.current_car])
            self.panel2_thread18.signal.connect(self.panel2_call_back_3)
            self.panel2_thread18.start()  # 启动线程
            self.prepare_13.setEnabled(False)
        pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Panel2()
    window.show()
    sys.exit(app.exec_())