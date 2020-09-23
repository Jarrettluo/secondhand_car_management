#!/usr/bin/env python
# _*_coding:utf-8 _*_
"""
@Time    :   22:56
@Auther  : Jarrett
@FileName: panel_1
@Software: PyCharm
"""

import fix_qt_import_error  # 来自于https://www.cnblogs.com/hester/p/11460121.html 解决bug

# https://www.codercto.com/a/19041.html 教程，如何添加数据库
import sys

from PyQt5.QtCore import QDate, QThread, pyqtSignal, Qt
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QApplication
from SQLite_tools import *
from PyQt5.Qt import QIntValidator


class Panel1(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        loadUi("ui_source/panel1.ui", self)

        self.db_name = './database.db'
        self.table_name = 'all_car'
        self.panel1_sqlite = SQLiteTools()
        self.connect_db()

        value = self.panel1_sqlite.getSQLtableColumn(self.table_name, "car_code")

        self.init_car_code(value)  # 初始化车辆编码
        self.init_all_inputs()  # 初始化输入框
        self.panel1_date1.setCalendarPopup(True)  # 设置日历弹出
        self.panel1_date2.setCalendarPopup(True)  # 设置日历弹出
        self.panel1_submit.clicked.connect(self.add_car_info)  # 提交按钮用于提交到数据库
        self.panel1_cancle.clicked.connect(self.init_all_inputs)  # 取消按钮用于刷新重置页面
        self.statusBar().hide()  # 关闭状态栏

        # spin_icon = qtawesome.icon('fa5.edit', color='#ac395d')  # #d4f1ef        # 车辆整备
        # self.panel1_title.setPixmap(QPixmap(spin_icon))  # 设置图标
        # self.panel1_title.setIconSize(QSize(25, 25))
        self.panel1_title.setAlignment(Qt.AlignLeft)
        self.panel1_title.setText('入库登记')

    def panel1_callback(self, value):
        """
        多线程回调函数
        :return:
        """
        # print('回调函数，写入完毕')
        self.panel1_submit.setEnabled(True)
        self.init_all_inputs()
        self.init_car_code(value)
        self.panel1_show_msg()  # 写入
        pass

    def connect_db(self):
        self.panel1_sqlite.createConnection(self.db_name)

    def init_car_code(self, value):
        # 读取车辆编码信息
        if len(value)==0:
            self.car_code = 'car-1'
            self.panel1_label1.setText(self.car_code)
        else:
            last_car_code = value[-1].split('-')
            self.car_code = last_car_code[0] + '-' + str(int(last_car_code[1]) + 1)
            self.panel1_label1.setText(self.car_code)

    def init_all_inputs(self):
        """
        初始化输入框
        :return:
        """
        self.panel1_line_edit1.setPlaceholderText('示例：川A123456')  # 车牌
        self.panel1_line_edit2.setPlaceholderText('示例：宝马325Li')  # 品牌型号
        self.panel1_date1.setDate(QDate.fromString('2019-01-01', 1))  # 注册时间
        self.panel1_date2.setDate(QDate.currentDate())  # 购买时间
        self.panel1_line_edit3.setPlaceholderText('示例：蓝色')  # 颜色
        self.panel1_line_edit4.setPlaceholderText('示例：88888元')  # 购买总价
        self.panel1_line_edit5.setPlaceholderText('示例：88888元')  # 自筹资金
        self.panel1_line_edit6.setPlaceholderText('示例：王总')  # 合作伙伴1
        self.panel1_line_edit7.setPlaceholderText('示例：88888元')  # 合作金额1
        self.panel1_text_edit1.setPlaceholderText('示例：本车品质较好！')
        self.panel1_line_edit1.setText('')  # 车牌
        self.panel1_line_edit2.setText('')  # 品牌型号
        self.panel1_line_edit3.setText('')
        self.panel1_line_edit4.setText('')
        self.panel1_line_edit5.setText('')
        self.panel1_line_edit6.setText('')
        self.panel1_line_edit7.setText('')
        self.panel1_line_edit8.setText('')
        self.panel1_line_edit9.setText('')
        self.panel1_line_edit10.setText('')
        self.panel1_line_edit11.setText('')
        self.panel1_line_edit12.setText('')
        self.panel1_line_edit13.setText('')
        self.panel1_text_edit1.setPlainText('')
        self.panel1_line_edit4.setValidator(QIntValidator())
        self.panel1_line_edit5.setValidator(QIntValidator())
        self.panel1_line_edit7.setValidator(QIntValidator())
        self.panel1_line_edit9.setValidator(QIntValidator())
        self.panel1_line_edit11.setValidator(QIntValidator())
        self.panel1_line_edit13.setValidator(QIntValidator())

    def add_car_info(self):
        # region 车辆基本信息
        license_plate = self.panel1_line_edit1.text()  # 车牌号
        car_brand = self.panel1_line_edit2.text()  # 车品牌型号
        register_time = self.panel1_date1.text()  # 车注册时间
        car_color = self.panel1_line_edit3.text()  # 车颜色
        # endregion

        # region 车辆购买信息
        buy_car_time = self.panel1_date2.text()  # 车购买时间
        buy_car_price = self.panel1_line_edit4.text()  # 车购买价格
        # endregion

        # region 车辆成本信息
        self_fund = self.panel1_line_edit5.text()  # 自出资金
        # endregion

        # region 合作伙伴信息
        cor1 = self.panel1_line_edit6.text()  # 合作伙伴1
        cor2 = self.panel1_line_edit8.text()  # 合作伙伴1
        cor3 = self.panel1_line_edit10.text()  # 合作伙伴1
        cor4 = self.panel1_line_edit12.text()  # 合作伙伴1
        fund1 = self.panel1_line_edit7.text()  # 合作伙伴1
        fund2 = self.panel1_line_edit9.text()  # 合作伙伴1
        fund3 = self.panel1_line_edit11.text()  # 合作伙伴1
        fund4 = self.panel1_line_edit13.text()  # 合作伙伴1
        # endregion

        # region 车辆成本信息
        note_msg = self.panel1_text_edit1.toPlainText()  # 自出资金
        # endregion

        if license_plate and car_brand and register_time and car_color and buy_car_time and buy_car_price and self_fund:
            # 必须输入基本信息才能写入数据库
            a, b, c, d, e, f = int(buy_car_price if buy_car_price else 0), int(self_fund if self_fund else 0),\
                               int(fund1 if fund1 else 0), int(fund2 if fund2 else 0), \
                               int(fund3 if fund3 else 0), int(fund4 if fund4 else 0)
            # 必须要合作伙伴的金额等于总金额才能往下写
            if a == b+c+d+e+f:
                args_list = [self.car_code, license_plate, car_brand, register_time, car_color, buy_car_time,
                             buy_car_price, self_fund, cor1, cor2, cor3, cor4, fund1, fund2, fund3, fund4, note_msg]
                self.panel1_submit.setEnabled(False)
                self.panel1_thread = panel1_Example(args_list)
                self.panel1_thread.signal.connect(self.panel1_callback)
                self.panel1_thread.start()  # 启动线程
            else:
                self.panel1_show_warning()

    def panel1_show_msg(self):
        QMessageBox.about(self, '提示信息', self.car_code + '保存成功！')

    def panel1_show_warning(self):
        QMessageBox.warning(self, '警告', '总金额不相等，请检查', QMessageBox.Yes)

class panel1_Example(QThread):
    signal = pyqtSignal(list)  # 括号里填写信号传递的参数

    def __init__(self, args_list):
        super().__init__()
        self.args_data = args_list

    def __del__(self):
        self.wait()

    def run(self):
        # 进行任务操作
        try:
            # print(self.args_data)   # 在这里
            value = write_to_database(self.args_data)
            self.signal.emit(value)  # 发射信号
        except Exception as e:
            print(e)




def write_to_database(args_data):
    db_name = './database.db'
    table_name = 'all_car'
    sql = SQLiteTools()
    sql.createConnection(db_name)
    value = sql.getSQLtableRowNum(table_name)
    sql.addSQLtableRow(table_name, (value + 1))
    car_info = args_data
    sql.setSQLtableValue(table_name, "car_code", value, car_info[0])
    sql.setSQLtableValue(table_name, "license_plate", value, car_info[1])
    sql.setSQLtableValue(table_name, "car_brand", value, car_info[2])
    sql.setSQLtableValue(table_name, 'register_time', value, car_info[3])
    sql.setSQLtableValue(table_name, 'car_color', value, car_info[4])
    sql.setSQLtableValue(table_name, 'buy_car_time', value, car_info[5])
    sql.setSQLtableValue(table_name, 'buy_car_price', value, car_info[6])
    sql.setSQLtableValue(table_name, 'self_fund', value, car_info[7])
    sql.setSQLtableValue(table_name, 'cor1', value, car_info[8])
    sql.setSQLtableValue(table_name, 'cor2', value, car_info[9])
    sql.setSQLtableValue(table_name, 'cor3', value, car_info[10])
    sql.setSQLtableValue(table_name, 'cor4', value, car_info[11])
    sql.setSQLtableValue(table_name, 'fund1', value, car_info[12])
    sql.setSQLtableValue(table_name, 'fund2', value, car_info[13])
    sql.setSQLtableValue(table_name, 'fund3', value, car_info[14])
    sql.setSQLtableValue(table_name, 'fund4', value, car_info[15])
    sql.setSQLtableValue(table_name, 'note_msg', value, car_info[16])
    value = sql.getSQLtableColumn(table_name, "car_code")
    return value

if __name__ == '__main__':
    if hasattr(sys, 'frozen'):
        os.environ['PATH'] = sys._MEIPASS + ";" + os.environ['PATH']

    app = QApplication(sys.argv)
    window = Panel1()
    window.show()
    sys.exit(app.exec_())
    # value = write_to_database(['car-5', '1', '2', '2019/1/1', '3', '2020/8/10', '4', '5', '6', '', '', '', '7', '', '', '', ''])
    # print(value)
