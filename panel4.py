#!/usr/bin/env python
# _*_coding:utf-8 _*_
"""
@Time    :   22:56
@Auther  : Jarrett
@FileName: panel_1
@Software: PyCharm
"""
import datetime
import os
import sys

from PyQt5.QtCore import QThread, pyqtSignal, QDate, Qt
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QTableWidgetItem
import pandas as pd
import xlwt

from SQLite_tools import SQLiteTools


class Panel4(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        loadUi("ui_source/panel4.ui", self)
        self.cwd = os.getcwd()  # 获取当前程序文件位置

        self.db_name = './database.db'
        self.table_name = 'all_car'
        self.spend_table_name = 'spend'
        self.sell_table_name = 'sell'
        self.panel4_sqlite = SQLiteTools()
        self.connect_db()

        self.init_input()  # 初始化输入框

        # self.all_car_selled()

        self.panel4_pushButton_3.clicked.connect(self.init_filter)  # 重新筛选
        self.panel4_pushButton_2.clicked.connect(self.write2csv)

        self.panel4_pushButton_4.clicked.connect(self.filter)  # 筛选显示

        self.statusBar().hide()

        self.panel4_title.setAlignment(Qt.AlignLeft)
        self.panel4_title.setText('统计报表')

        self.panel4_table1.horizontalHeader().resizeSection(0, 50)
        self.panel4_table1.horizontalHeader().resizeSection(1, 70)
        self.panel4_table1.horizontalHeader().resizeSection(2, 70)
        self.panel4_table1.horizontalHeader().resizeSection(3, 100)
        self.panel4_table1.horizontalHeader().resizeSection(4, 50)
        self.panel4_table1.horizontalHeader().resizeSection(5, 70)
        self.panel4_table1.horizontalHeader().resizeSection(6, 100)
        self.panel4_table1.horizontalHeader().resizeSection(7, 70)
        self.panel4_table1.horizontalHeader().resizeSection(8, 70)
        self.panel4_table1.horizontalHeader().resizeSection(9, 70)
        self.panel4_table1.horizontalHeader().resizeSection(10, 70)
        self.panel4_table1.horizontalHeader().resizeSection(11, 70)
        self.panel4_table1.horizontalHeader().resizeSection(12, 70)

    def connect_db(self):
        self.panel4_sqlite.createConnection(self.db_name)

    def init_filter(self):  # 重置过滤器
        print('到这里了，你看看')
        self.panel4_thread1 = panel4_Example1()
        self.panel4_thread1.signal.connect(self.panel4_call_back_1)
        self.panel4_thread1.start()  # 启动线程

        self.init_input()

    def init_input(self):
        self.panel4_lineEdit1.setText('')
        self.panel4_lineEdit2.setText('')
        self.panel4_dateEdit_1.setDate(QDate.fromString('2009-01-01', 1))  # 注册时间
        self.panel4_dateEdit_2.setDate(QDate.currentDate())
        self.panel4_dateEdit_3.setDate(QDate.fromString('2009-01-01', 1))  # 注册时间
        self.panel4_dateEdit_4.setDate(QDate.currentDate())
        self.panel4_dateEdit_1.setCalendarPopup(True)  # 设置日历弹出
        self.panel4_dateEdit_2.setCalendarPopup(True)  # 设置日历弹出
        self.panel4_dateEdit_3.setCalendarPopup(True)  # 设置日历弹出
        self.panel4_dateEdit_4.setCalendarPopup(True)  # 设置日历弹出

    def all_car_selled(self):
        """
        这里是默认初始化
        :return:
        """
        self.panel4_thread2 = panel4_Example1()
        self.panel4_thread2.signal.connect(self.panel4_call_back_1)
        self.panel4_thread2.start()  # 启动线程

    def panel4_call_back_1(self, all_sell_car):
        """
        默认获得的所有销售车辆信息
        :param all_sell_car:
        :return:
        """
        self.all_selled_df = all_sell_car[0]
        self.palyed_selled_df = self.all_selled_df.copy(deep=True)

        print(self.all_selled_df)

        if not self.palyed_selled_df.empty:
            self.play_it()  # 查询到的结果显示出来

            self.panel4_thread3 = panel4_Example2(self.palyed_selled_df)
            self.panel4_thread3.signal.connect(self.panel4_call_back_2)
            self.panel4_thread3.start()  # 启动线程
        else:
            pass

    def play_it(self):
        row_length = self.palyed_selled_df.shape[0]
        columns_length = self.palyed_selled_df.shape[1]
        self.panel4_table1.setRowCount(row_length)
        self.panel4_table1.setColumnCount(columns_length)
        # 以下代码为显示df到表格中
        self.palyed_selled_df['car_license'] = self.palyed_selled_df['car_license'].map(
            lambda x: x.strftime('%Y-%m-%d'))
        self.palyed_selled_df['sell_time'] = self.palyed_selled_df['sell_time'].map(lambda x: x.strftime('%Y-%m-%d'))
        for index, row in self.palyed_selled_df.T.iteritems():
            row = row.tolist()
            for i, item in enumerate(row):
                newItem = QTableWidgetItem(str(item))
                newItem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.panel4_table1.setItem(index, i, newItem)

    def panel4_call_back_2(self, result):
        # result -> list
        self.panel4_lineEdit_3.setText(str(result[0]))
        self.panel4_lineEdit_4.setText(str(result[1]))
        self.panel4_lineEdit_5.setText(str(result[2]))
        self.panel4_lineEdit_6.setText(str(result[3]))

    def filter(self):
        search_car_code = self.panel4_lineEdit1.text()
        search_car_plate = self.panel4_lineEdit2.text()
        search_s_date_1 = self.panel4_dateEdit_1.text()
        search_e_date_1 = self.panel4_dateEdit_2.text()
        search_s_date_2 = self.panel4_dateEdit_3.text()
        search_e_date_2 = self.panel4_dateEdit_4.text()

        filter_varies = [search_car_code, search_car_plate, search_s_date_1, search_e_date_1,
                         search_s_date_2, search_e_date_2]
        if not self.all_selled_df.empty:
            # 如果当前不为空，再进行筛选
            self.panel4_thread4 = panel4_Example3(self.all_selled_df, filter_varies)
            self.panel4_thread4.signal.connect(self.panel4_call_back_3)
            self.panel4_thread4.start()  # 启动线程
        else:
            pass

    def panel4_call_back_3(self, result):
        if not result[0].empty:
            self.palyed_selled_df = pd.DataFrame(result[0])
            self.panel4_label1.setText('筛选成功')
            self.play_it()

        else:
            self.panel4_label1.setText('筛选失败')
            self.init_input()  # 重置过滤器

    def write2csv(self):
        today = datetime.date.today()
        self.cwd = self.cwd + '/二手车销售报表_' + str(today)
        filename = QFileDialog.getSaveFileName(self, '保存报表', self.cwd, "Excel Files (*.xls)")

        if filename[0] and not self.palyed_selled_df.empty:
            self.panel4_thread5 = panel4_Example(self.palyed_selled_df, filename[0])
            self.panel4_thread5.signal.connect(self.panel4_call_back)
            self.panel4_thread5.start()  # 启动线程
        else:
            pass

    def panel4_call_back(self):
        print('保存成功')
        self.panel4_label1.setText('报表保存成功')
        pass


class panel4_Example(QThread):
    signal = pyqtSignal()  # 括号里填写信号传递的参数

    def __init__(self, filename, file_path):
        super().__init__()
        self.filename = filename
        self.file_path = file_path

    def __del__(self):
        self.wait()

    def run(self):
        self.filename.columns = ['车辆编码', '车牌号', '车型号', '上户时间', '颜色',
                                 '购买价', '销售时间', '销售价', '提成费', '总利润',
                                 '自家利润', '合作伙伴1', '伙伴1利润', '合作伙伴2', '伙伴2利润',
                                 '合作伙伴3', '伙伴3利润', '合作伙伴4', '伙伴4利润',
                                 '备注']
        self.filename = self.filename.T
        self.filename.to_excel(self.file_path)
        self.signal.emit()  # 发射信号


class panel4_Example1(QThread):
    signal = pyqtSignal(list)  # 括号里填写信号传递的参数

    def __init__(self):
        super().__init__()

    def __del__(self):
        self.wait()

    def run(self):
        panel4 = Panel4()
        record_num = panel4.panel4_sqlite.getSQLtableRowNum(panel4.sell_table_name)  # 获取销售订单的总数
        result = []
        for i in range(record_num):
            search_result = panel4.panel4_sqlite.getSQLtableRow(panel4.sell_table_name, i)  # 逐个查询销售订单
            result.append(search_result)  # 返回销售数据的结果

        print(result)

        columns_list = ['car_code', 'car_plate', 'car_brand', 'car_license', 'car_color',
                        'car_price_sum', 'sell_time', 'sell_price', 'percentage', 'profit',
                        'self_profit', 'person1', 'person1_profit', 'person2', 'person2_profit',
                        'person3', 'person3_profit', 'person4', 'person4_profit', 'reserved']
        all_selled_df = pd.DataFrame(result, columns=columns_list)
        print(all_selled_df)
        all_selled_df['car_license'] = all_selled_df['car_license'].map(
            lambda x: datetime.datetime.strptime(x, '%Y/%m/%d'))
        all_selled_df['sell_time'] = all_selled_df['sell_time'].map(
            lambda x: datetime.datetime.strptime(x, '%Y/%m/%d'))
        print(all_selled_df)
        self.signal.emit([all_selled_df])  # 发射信号


class panel4_Example2(QThread):
    signal = pyqtSignal(list)  # 括号里填写信号传递的参数

    def __init__(self, df):
        super().__init__()
        self.df = df

    def __del__(self):
        self.wait()

    def run(self):
        print(self.df)
        self.df['car_price_sum'] = pd.to_numeric(self.df['car_price_sum'], errors='ignore')
        self.df['sell_price'] = pd.to_numeric(self.df['sell_price'], errors='ignore')
        self.df['profit'] = pd.to_numeric(self.df['profit'], errors='ignore')
        self.df['self_profit'] = pd.to_numeric(self.df['self_profit'], errors='ignore')
        a = sum(self.df['car_price_sum'])
        b = sum(self.df['sell_price'])
        c = sum(self.df['profit'].apply(int))
        d = sum(self.df['self_profit'].apply(int))
        result = [a, b, c, d]
        self.signal.emit(result)  # 发射信号


class panel4_Example3(QThread):
    signal = pyqtSignal(list)  # 括号里填写信号传递的参数

    def __init__(self, df, fiter_varies):
        super().__init__()
        self.df = df
        self.rules = fiter_varies

    def __del__(self):
        self.wait()

    def run(self):
        s_date = datetime.datetime.strptime(self.rules[2], '%Y/%m/%d')
        e_date = datetime.datetime.strptime(self.rules[3], '%Y/%m/%d')
        filtered_df = self.df[(self.df['car_license'] >= s_date) &
                              (self.df['car_license'] <= e_date)]
        if not filtered_df.empty:
            s_date = datetime.datetime.strptime(self.rules[4], '%Y/%m/%d')
            e_date = datetime.datetime.strptime(self.rules[5], '%Y/%m/%d')
            filtered_df = filtered_df[(filtered_df['sell_time'] >= s_date) &
                                      (filtered_df['sell_time'] <= e_date)]
        if not filtered_df.empty and self.rules[0]:
            filtered_df = filtered_df[filtered_df['car_code'] == self.rules[0]]
        if not filtered_df.empty and self.rules[1]:
            filtered_df = filtered_df[filtered_df['car_plate'] == self.rules[1]]

        result = [filtered_df]

        self.signal.emit(result)  # 发射信号


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Panel4()
    window.show()
    sys.exit(app.exec_())
