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
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem, QHeaderView, QAbstractItemView, \
    QMessageBox
from SQLite_tools import SQLiteTools
from PyQt5.QtCore import QDate, QThread, pyqtSignal, Qt
import pandas as pd


class panel3_Example(QThread):
    signal = pyqtSignal(list)  # 括号里填写信号传递的参数

    def __init__(self, args):
        super().__init__()
        self.arg = args

    def __del__(self):
        self.wait()

    def run(self):
        # 进行任务操作
        print(self.arg)
        panel3 = Panel3()
        panel3.current_car_chepai = panel3.panel3_sqlite.getSQLtableValue_by_column_value(panel3.table_name, 'car_code', self.arg)
        pasassafs = panel3.panel3_sqlite.getSQLtableRow(panel3.table_name, str(panel3.current_car_chepai[0]))
        # panel3.panel2_line_edit2.setText('')
        self.signal.emit(pasassafs)  # 发射信号

class panel3_Example2(QThread):
    signal = pyqtSignal(list)  # 括号里填写信号传递的参数

    def __init__(self, args):
        super().__init__()
        self.arg = args

    def __del__(self):
        self.wait()

    def run(self):
        # 进行任务操作
        panel3 = Panel3()
        panel3.current_car_chepai = panel3.panel3_sqlite.getSQLtableValue_by_column_value(panel3.table_name, 'license_plate', self.arg)
        if len(panel3.current_car_chepai) > 0:
            pasassafs = panel3.panel3_sqlite.getSQLtableRow(panel3.table_name, str(panel3.current_car_chepai[0]))
        else:
            pasassafs = [1]
        self.signal.emit(pasassafs)  # 发射信号

class panel3_Example3(QThread):
    signal = pyqtSignal(list)  # 括号里填写信号传递的参数

    def __init__(self):
        super().__init__()

    def __del__(self):
        self.wait()

    def run(self):
        # 进行任务操作
        panel3 = Panel3()
        all_car = panel3.panel3_sqlite.getSQLtableColumn(panel3.table_name, "car_code")
        all_car.reverse()  # 列表反转
        self.signal.emit(all_car)  # 发射信号


class panel3_Example4(QThread):
    signal = pyqtSignal(list)  # 括号里填写信号传递的参数

    def __init__(self, args):
        super().__init__()
        self.arg = args

    def __del__(self):
        self.wait()

    def run(self):
        # 进行任务操作
        panel3 = Panel3()
        panel3.search_result = panel3.panel3_sqlite.getSQLtableValue_by_column_value(panel3.spend_table_name, 'car_host', self.arg)
        result_list = []    # 用于返回查询到的结果
        if len(panel3.search_result) > 0:
            for car_index in panel3.search_result:
                info = panel3.panel3_sqlite.getSQLtableRow(panel3.spend_table_name, str(car_index))
                result_list.append(list(info))
            result_list.append([None])
        else:
            result_list = [None]
        self.signal.emit(result_list)  # 发射信号


class panel3_Example5(QThread):
    signal = pyqtSignal(list)  # 括号里填写信号传递的参数

    def __init__(self, args):
        super().__init__()
        self.args = args

    def __del__(self):
        self.wait()

    def run(self):
        # 进行任务操作
        panel3 = Panel3()
        value = panel3.panel3_sqlite.getSQLtableRowNum(panel3.sell_table_name)  # 获取所有/行
        panel3.panel3_sqlite.addSQLtableRow(panel3.sell_table_name, (value + 1))
        panel3.panel3_sqlite.setSQLtableValue(panel3.sell_table_name, "car_code", value, self.args[0])
        panel3.panel3_sqlite.setSQLtableValue(panel3.sell_table_name, "car_plate", value, str(self.args[1]))
        panel3.panel3_sqlite.setSQLtableValue(panel3.sell_table_name, "car_brand", value, str(self.args[2]))
        panel3.panel3_sqlite.setSQLtableValue(panel3.sell_table_name, "car_license", value, str(self.args[3]))
        panel3.panel3_sqlite.setSQLtableValue(panel3.sell_table_name, "car_color", value, str(self.args[4]))
        panel3.panel3_sqlite.setSQLtableValue(panel3.sell_table_name, "car_price_sum", value, str(self.args[5]))
        panel3.panel3_sqlite.setSQLtableValue(panel3.sell_table_name, "sell_time", value, str(self.args[6]))
        panel3.panel3_sqlite.setSQLtableValue(panel3.sell_table_name, "sell_price", value, str(self.args[7]))
        panel3.panel3_sqlite.setSQLtableValue(panel3.sell_table_name, "percentage", value, str(self.args[8]))
        panel3.panel3_sqlite.setSQLtableValue(panel3.sell_table_name, "profit", value, str(self.args[9]))
        panel3.panel3_sqlite.setSQLtableValue(panel3.sell_table_name, "self_profit", value, str(self.args[10]))
        panel3.panel3_sqlite.setSQLtableValue(panel3.sell_table_name, "person1", value, str(self.args[11]))
        panel3.panel3_sqlite.setSQLtableValue(panel3.sell_table_name, "person1_profit", value, str(self.args[12]))
        panel3.panel3_sqlite.setSQLtableValue(panel3.sell_table_name, "person2", value, str(self.args[13]))
        panel3.panel3_sqlite.setSQLtableValue(panel3.sell_table_name, "person2_profit", value, str(self.args[14]))
        panel3.panel3_sqlite.setSQLtableValue(panel3.sell_table_name, "person3", value, str(self.args[15]))
        panel3.panel3_sqlite.setSQLtableValue(panel3.sell_table_name, "person3_profit", value, str(self.args[16]))
        panel3.panel3_sqlite.setSQLtableValue(panel3.sell_table_name, "person4", value, str(self.args[17]))
        panel3.panel3_sqlite.setSQLtableValue(panel3.sell_table_name, "person4_profit", value, str(self.args[18]))
        # value = panel3.panel3_sqlite.getSQLtableColumn(panel3.sell_table_name, "car_code")
        value = ['这个是用于测试写入数据库的']
        self.signal.emit(value)  # 发射信号

# 用于查找该车辆的售卖情况
class panel3_Example6(QThread):
    signal = pyqtSignal(list)  # 括号里填写信号传递的参数

    def __init__(self, args):
        super().__init__()
        self.arg = args

    def __del__(self):
        self.wait()

    def run(self):
        # 进行任务操作
        print(self.arg)
        panel3 = Panel3()
        value = panel3.panel3_sqlite.getSQLtableValue_by_column_value(panel3.sell_table_name, 'car_code', self.arg)
        # pasassafs = panel3.panel3_sqlite.getSQLtableRow(panel3.table_name, str(panel3.current_car_chepai[0]))
        # panel3.panel2_line_edit2.setText('')
        self.signal.emit(value)  # 发射信号

class Panel3(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        loadUi("ui_source/panel3.ui", self)

        self.db_name = './database.db'
        self.table_name = 'all_car'
        self.spend_table_name = 'spend'
        self.sell_table_name = 'sell'
        self.panel3_sqlite = SQLiteTools()
        self.connect_db()

        # self.all_car = self.panel3_sqlite.getSQLtableColumn(self.table_name, "car_code")
        # self.all_car.reverse()  # 列表反转
        # self.panel3_combo_box1.addItems(self.all_car)

        # self.init_all_car()

        self.panel3_combo_box1.setMaxVisibleItems(10)   # 设置最大下拉数量
        self.panel3_combo_box1.activated.connect(self.change_index)
        # self.panel3_combo_box1.currentIndexChanged.connect(self.change_index)
        self.change_car_code()

        self.panel3_line_edit1.editingFinished.connect(self.search_edit1)
        self.panel3_line_edit2.editingFinished.connect(self.search_edit2)

        # self.init_panel()
        # self.pushButton.clicked.connect(self.search_car)

        self.panel3_pushbutton_1.clicked.connect(self.click_search)  # 点击搜索按钮

        self.init_cal()
        self.panel3_pushbutton_2.clicked.connect(self.click_cal)    # 点击计算按钮

        self.statusBar().hide()

        # spin_icon = qtawesome.icon('fa5.calendar-check', color='#1e704d')    # #d4f1ef
        # self.panel3_title.setIcon(spin_icon)  # 设置图标
        # self.panel3_title.setIconSize(QSize(25, 25))
        self.panel3_title.setText('车辆销售')
        self.panel3_title.setAlignment(Qt.AlignLeft)

        self.panel3_table1.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)     # 表格占满整个空间
        self.panel3_table2.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.panel3_table3.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.panel3_table1.setEditTriggers(QAbstractItemView.NoEditTriggers)       # 不能编辑
        self.panel3_table2.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.panel3_table3.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.panel3_table1.setSelectionBehavior(QAbstractItemView.SelectRows)   # 选中整行
        self.panel3_table2.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.panel3_table3.setSelectionBehavior(QAbstractItemView.SelectRows)


    def init_all_car(self):
        print('这里是panel3的多线程')
        self.panel3_thread6 = panel3_Example3()
        self.panel3_thread6.signal.connect(self.panel3_call_back3)
        self.panel3_thread6.start()  # 启动线程

    def panel3_call_back3(self, all_car):
        print('这里是panel3', all_car)
        self.panel3_combo_box1.clear()
        self.all_car = all_car
        self.panel3_combo_box1.addItems(self.all_car)

    def connect_db(self):
        self.panel3_sqlite.createConnection(self.db_name)

    # 搜索输入初始化部分
    def change_index(self):
        self.current_car = self.panel3_combo_box1.currentText()
        self.panel3_thread1 = panel3_Example(self.current_car)
        self.panel3_thread1.signal.connect(self.panel3_call_back)
        self.panel3_thread1.start()  # 启动线程
        self.panel3_line_edit1.setStyleSheet("border:1px solid black;")

    def panel3_call_back(self, xxx):
        print('这里是改变了combox的索引', xxx)

        self.panel3_line_edit1.setText(self.current_car)
        self.panel3_line_edit2.setText(xxx[1])
        # self.reset_input_close() # 重置input, 关闭按钮

    def change_car_code(self):
        self.current_car = self.panel3_combo_box1.currentText()
        self.panel3_line_edit1.setText(self.current_car)

    def search_edit1(self):
        print('zhelidiaoyong ')
        edit1_car_code = self.panel3_line_edit1.text()
        print(edit1_car_code)
        if edit1_car_code in self.all_car:
            code_index = self.all_car.index(edit1_car_code)
            self.panel3_combo_box1.setCurrentIndex(code_index)
            self.panel3_line_edit1.setStyleSheet("border:1px solid black;")
        else:
            self.panel3_line_edit1.setText('')
            self.panel3_line_edit1.setStyleSheet("border:1px solid red;")

    def search_edit2(self):
        che_pai = self.panel3_line_edit2.text() # 获取收入的车牌
        if che_pai:
            self.panel3_thread2 = panel3_Example2(che_pai)
            self.panel3_thread2.signal.connect(self.panel3_call_back2)
            self.panel3_thread2.start()  # 启动线程
        else:
            pass

    def panel3_call_back2(self, args):
        car_code = args[0]
        if car_code in self.all_car:
            xx = self.all_car.index(car_code)
            self.panel3_combo_box1.setCurrentIndex(xx)
            self.panel3_line_edit2.setStyleSheet("border:1px solid black;")
        else:
            self.panel3_line_edit2.setStyleSheet("border:1px solid red;")

    ## 以上是搜索的初始化


    def click_search(self):
        """
        点击搜索按钮的函数
        :return:
        """
        edit2_car_code = self.panel3_line_edit1.text()
        if edit2_car_code in self.all_car:  # 如果车在列表中才会进行搜索的操作
            code_index = self.all_car.index(edit2_car_code)
            self.panel3_combo_box1.setCurrentIndex(code_index)
            self.panel3_line_edit1.setStyleSheet("border:1px solid black;")

            self.panel3_thread3 = panel3_Example(self.current_car)
            self.panel3_thread3.signal.connect(self.panel3_call_back_4)
            self.panel3_thread3.start()  # 启动线程
        else:
            self.panel3_line_edit1.setText('')
            self.panel3_line_edit1.setStyleSheet("border:1px solid red;")
        pass

    def panel3_call_back_4(self, args):
        """
        搜索函数的回调函数，用于对结果的展示
        :param args:
        :return:
        """
        self.current_car_plate = args[1] # 车牌信息
        self.current_car_type = args[2] # 车辆型号 颜色信息
        self.current_car_license = args[3]   # 车辆上户信息
        self.current_car_color = args[4] # 车辆购买时间
        self.current_car_cost = args[5]  # 车辆购买总价
        self.panel3_line_edit2.setText(self.current_car_plate)  # 填充车牌信息

        self.car_buy_price = args[6]
        self.panel3_label5.setText(str(args[6])+'  元')    # 修改车本购买价格,将其放入本车的购买价格中

        self.partner = [['自筹', str(args[7])],
                        [str(args[8]), str(args[9])],
                        [str(args[10]), str(args[11])],
                        [str(args[12]), str(args[13])],
                        [str(args[14]), str(args[15])]]

        self.partner_df = pd.DataFrame(self.partner, columns=['person', 'money'])
        self.partner_df.dropna(inplace=True)
        self.partner_df['money'] = pd.to_numeric(self.partner_df['money'])
        self.partner_df.dropna(inplace=True)
        self.partner_df['ratio'] = self.partner_df['money'] / int(self.car_buy_price)   # 计算每个人的占比

        self.panel3_table1.setRowCount(self.partner_df.shape[1])
        self.panel3_table1.setColumnCount(3)
        for i, item in self.partner_df.iterrows():
            newItem = QTableWidgetItem(item['person'])
            newItem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.panel3_table1.setItem(i, 0, newItem)

            newItem = QTableWidgetItem(str(item['money']))
            newItem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.panel3_table1.setItem(i, 1, newItem)

            newItem = QTableWidgetItem(str(item['ratio']))
            newItem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.panel3_table1.setItem(i, 2, newItem)


        # 开始查找该车辆的整备情况
        self.panel3_thread4 = panel3_Example4(self.current_car)
        self.panel3_thread4.signal.connect(self.panel3_call_back_5)
        self.panel3_thread4.start()  # 启动线程


    def panel3_call_back_5(self, spend_list):
        if spend_list[0]:
            self.panel3_table2.setRowCount(len(spend_list)-1)
            self.panel3_table2.setColumnCount(3)
            columns_list = ['item', 'price', 'car_id', 'person', 'time', 'reserved']
            df = pd.DataFrame(spend_list, columns=columns_list)
            df = df[['item', 'price', 'person']]
            df.dropna(inplace=True)
            self.car_price_sum = sum(df['price'])
            print('这里是计算价格总数', self.car_price_sum)
            for index, row in df.iterrows():
                newItem = QTableWidgetItem(str(row['item']))
                newItem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.panel3_table2.setItem(index, 0, newItem)
                newItem = QTableWidgetItem(str(row['price']))
                newItem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.panel3_table2.setItem(index, 1, newItem)
                newItem = QTableWidgetItem(str(row['person']))
                newItem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.panel3_table2.setItem(index, 2, newItem)
        else:
            self.panel3_table2.setRowCount(1)
            self.panel3_table2.setColumnCount(3)
            newItem = QTableWidgetItem('无')
            self.panel3_table2.setItem(0, 0, newItem)
            newItem = QTableWidgetItem('0')
            self.panel3_table2.setItem(0, 1, newItem)
            newItem = QTableWidgetItem('-')
            self.panel3_table2.setItem(0, 2, newItem)
            self.car_price_sum = 0


        # 开始查找该车辆的售出情况
        self.panel3_thread7 = panel3_Example6(self.current_car)
        self.panel3_thread7.signal.connect(self.panel3_call_back_7)
        self.panel3_thread7.start()  # 启动线程

        # 获得本车的总支出
        # 获得本车的整备费用
        self.panel3_label7.setText(str(self.car_price_sum)+'  元')       # 放入车辆的总整备费用
        print('888888888888888888888888888888888888')
        print(self.car_price_sum)
        self.car_all_cost = self.car_price_sum + self.car_buy_price   # 获得总成本，包括购车价和整备费用
        self.panel3_label9.setText(str(self.car_all_cost)+'  元')    # 计算总支出成本


    def panel3_call_back_7(self, args):
        if len(args):
            self.panel3_show_warning()  # 本车已经被售卖，请注意
            self.init_cal() # 初始化计算部分的按钮
        else:
            # 到这里搜索结束啦，可以进行计算啦，计算的时候将输入框打开！
            self.open_calculator()  # 打开计算的框
            # print('本车没有售卖')


    def open_calculator(self):
        # 这里用来打开计算的按钮
        # self.init_cal() # 重置计算部分
        # print('打开计算的按钮了')
        self.panel3_pushbutton_2.setEnabled(True)
        self.panel3_line_edit3.setEnabled(True)
        self.panel3_line_edit4.setEnabled(True) # 可以调整
        self.panel3_doubleSpinBox.setEnabled(True)  # 可以调整提成比例


    # 点击计算按钮
    def click_cal(self):
        print('这里是计算部分')

        self.sell_time = self.panel3_dateEdit.text()    # 获取本车的销售时间
        self.percentage = self.panel3_line_edit4.text() # 获取本车的提成金额
        print(int(self.partner[0][1]))
        print(self.percentage)
        print(type(self.percentage))
        print(float(self.percentage))
        print(int(self.car_price_sum))
        if self.sell_price and self.percentage:
            print('#####################################')
            self.partner[0][1] = str(int(self.partner[0][1]) + float(self.percentage) + int(self.car_price_sum)) # 自己部分
            # 的支出应该加上提成费用，以及整备的费用
            self.car_all_cost = int(self.car_all_cost) + int(self.percentage)   # 所有的支出费用
            self.car_all_profit = int(self.car_buy_price) - int(self.car_all_cost)
            self.panel3_label9.setText(str(self.car_all_cost) + '  元')  # 计算总支出成本
            # self.panel3_label9.setText('hhafhfahfdsafds')  # 计算总支出成本
            # 车辆编码， 车辆号牌， 车辆型号，
            # 车辆上户时间， 车辆颜色，车辆整备费用，
            # 车辆销售时间，车辆销售价格，销售提成，
            # 车辆总利润，自筹，
            # 合作伙伴1，利润1，
            # 合作伙伴2， 利润2，
            # 合作伙伴3，利润3，
            # 合作伙伴4， 利润4
            varies = [self.current_car, self.current_car_plate, self.current_car_type,
                      self.current_car_license, self.current_car_color,  self.car_price_sum,
                      self.sell_time, self.sell_price, self.percentage,
                      self.car_all_profit, self.partner[0][1],
                      self.partner[1][0], self.partner[1][1],
                      self.partner[2][0], self.partner[2][1],
                      self.partner[3][0], self.partner[3][1],
                      self.partner[4][0], self.partner[4][1]
                      ]
            print(varies)
            self.panel3_thread5 = panel3_Example5(varies)
            self.panel3_thread5.signal.connect(self.panel3_call_back_6)
            self.panel3_thread5.start()  # 启动线程

    def panel3_call_back_6(self, args):
        # print(args)

        # 点击搜索按钮以后获得的出资人
        partner_df = pd.DataFrame(self.partner, columns=['person', 'money'])
        partner_df['money'] = partner_df['money'].apply(pd.to_numeric, errors='ignore')
        partner_df.dropna(inplace=True)

        self.car_all_profit_2 = int(self.sell_price) - float(self.car_all_cost)
        self.panel3_label14.setText(str(self.car_all_profit_2)) # 将车辆的最终总利润显示出来

        partner_df['ratio'] = self.partner_df['ratio'] #round(partner_df['money']*100/int(self.sell_price), 2)    # 计算占比
        partner_df['profit'] = round(partner_df['ratio']*float(self.car_all_profit_2), 2)   #TODO 这里用来计算利润率
        self.panel3_table3.setRowCount(int(partner_df.shape[1]))
        self.panel3_table1.setColumnCount(3)
        for index, row in partner_df.iterrows():
            newItem = QTableWidgetItem(str(row['person']))
            newItem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.panel3_table3.setItem(index, 0, newItem)
            newItem = QTableWidgetItem(str(row['profit']))
            newItem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.panel3_table3.setItem(index, 1, newItem)
            newItem = QTableWidgetItem(str(row['ratio']))
            newItem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.panel3_table3.setItem(index, 2, newItem)

        self.panel3_pushbutton_2.setEnabled(False)  # 点击计算完毕以后，计算的按钮将关闭，不能被点击
        self.panel3_show_msg()  # 用于展示已经售卖的消息
        self.init_cal()  # 初始化计算部分的按钮





    def init_cal(self):
        """
        这里用来初始化计算部分的输入框
        :return:
        """
        self.panel3_dateEdit.setDate(QDate.currentDate())
        self.panel3_dateEdit.setCalendarPopup(True)  # 设置日历弹出
        self.panel3_doubleSpinBox.setRange(0, 10)
        self.panel3_doubleSpinBox.setSingleStep(0.5)
        self.panel3_doubleSpinBox.setValue(6)
        self.panel3_doubleSpinBox.setSuffix(" %")
        self.panel3_doubleSpinBox.setWrapping(True)
        self.panel3_line_edit4.setText('-')

        self.panel3_line_edit3.setValidator(QIntValidator())
        self.panel3_line_edit4.setValidator(QIntValidator())
        self.panel3_pushbutton_2.setEnabled(False)

        self.panel3_line_edit3.editingFinished.connect(self.calculate_ticheng)  # 一旦改变就计算提成

        self.panel3_line_edit3.setEnabled(False)    # 不能输入出售的时间
        self.panel3_doubleSpinBox.setEnabled(False)  # 不能调整提成比例
        self.panel3_line_edit4.setEnabled(False)    # 不能输入出售的时间



    def calculate_ticheng(self):
        print('连接到这里了')
        self.sell_price = self.panel3_line_edit3.text()
        jia_li_run = int(self.sell_price) - int(self.car_all_cost)
        self.ratio = self.panel3_doubleSpinBox.value()
        ti_cheng = jia_li_run*float(self.ratio)*0.01
        if ti_cheng > 0:
            self.panel3_line_edit4.setText(str(int(ti_cheng)))
        else:
            self.panel3_line_edit4.setText('0') # 如果计算出来的提成是负值那么就把提成给置0

    def panel3_show_msg(self):
        QMessageBox.about(self, '提示信息', self.current_car + '保存成功！')

    def panel3_show_warning(self):
        QMessageBox.warning(self, '警告', '本车已经被售卖！', QMessageBox.Yes)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Panel3()
    window.show()
    sys.exit(app.exec_())