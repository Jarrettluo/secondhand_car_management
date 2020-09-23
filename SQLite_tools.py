#!/usr/bin/env python
# _*_coding:utf-8 _*_
"""
@Time    :   9:53
@Auther  : Jarrett
@FileName: SQLite_tools
@Software: PyCharm
"""

"""https://blog.csdn.net/weixin_42686768/article/details/87992476"""
from PyQt5 import QtSql
from PyQt5.QtSql import QSqlQuery

import sqlite3

# # 必须先创建一个应用程序对象，否则sqlite3数据库不支持PyQt5的类和方法对其进行操作
# a = QtWidgets.QApplication(sys.argv)


# coding:utf-8

import os
from PyQt5.QtSql import QSqlDatabase, QSqlQuery


class SQLiteTools():
    def __init__(self):
        pass

    # region 创建数据库连接和数据表

    def createConnection(self, DB_name):
        '''
        创建数据库连接
        :param DB_name: 数据库名称
        :return: null
        '''
        #选择数据库类型，这里为sqlite3数据库
        db=QSqlDatabase.addDatabase("QSQLITE")
        #创建数据库test0.db,如果存在则打开，否则创建该数据库
        db.setDatabaseName(DB_name)
        #打开数据库
        db.open()
        #此语句必须放在打开数据库之后
        self.que = QSqlQuery()

    def selectTableExist(self, tbname):
        '''
        判断指定数据表是否存在
        :param tbname: 表格名称
        :return: 在返回True,否则返回False
        '''
        sql = u"select * from sqlite_master where type='table' and name = '" + tbname + u"';"
        self.que.exec_(sql)
        return self.que.next()

    def createSQLtable(self, tbname):
        '''
        创建通用数据表，默认第一列为主键，名称:ID，类型:INTEGER, 自增
        :param tbname: 数据表名称
        :return:  null
        '''
        # CREATE TABLE if not exists 表名 (ID INTEGER PRIMARY KEY AUTOINCREMENT);
        sql = u"CREATE TABLE if not exists " + tbname + u" (ID INTEGER PRIMARY KEY AUTOINCREMENT);"
        self.que.exec_(sql)

    # endregion


    # region 添加表格数据

    def addSQLtableColumn(self, tbname, columnName, genre):
        '''
        指定数据表添加列
        :param tbname: 表名
        :param columnName: 列名
        :param genre: 添加列类型
        :return: null
        '''
        # ALTER TABLE 表名 ADD 列名 列类型;
        sql = u"ALTER TABLE " + tbname + u" ADD " + columnName + " " + genre +";"
        self.que.exec_(sql)

    def addSQLtableRow(self, tbname, rowNum):
        '''
        指定数据表添加指定行
        :param tbname: 表格名称
        :param rowNum: 行数
        :return: null
        '''
        # INSERT INTO 表名 (ID) VALUES (行);
        for row in range(rowNum):
            sql = "INSERT INTO " + tbname + " (ID) VALUES (" + str(row) + ");"
            b = self.que.exec_(sql)

    def setSQLtableValue(self, tbname, column, row, value):
        '''
        更新数据表指定位置的值
        :param tbname: 数据表名称
        :param column: 行数
        :param row: 列数
        :param value: 值
        :return: null
        '''
        # UPDATE 表名 SET 列名=值 WHERE ID=行;
        sql = u"UPDATE " + tbname + u" SET " +column+ "='" +value+ "' WHERE ID=" +str(row)+ ";"
        a = self.que.exec_(sql)


    # endregion


    # region 获取表格数据
    def getSQLtableRowNum(self, tbname):
        '''
        获取指定表格总行数
        :param tbname: 表格名称
        :return: 行数
        '''
        result = 0
        sql = "SELECT COUNT(*) FROM " + tbname + ";"
        self.que.exec_(sql)
        if self.que.next():
            result = self.que.value(0)
        return result

    def getSQLtableColumnName(self, tbname):
        '''
        获取指定表所有字段名称
        :param taname:  表格名称
        :return:  列名称列表
        '''
        sql = "PRAGMA table_info([" +tbname+ "])"
        self.que.exec_(sql)
        NameList = []
        while self.que.next():
            result = self.que.value(1)
            if result and result != "ID":
                NameList.append(result)
        return NameList

    def getSQLtableValue(self, tbname, column, row):
        '''
        读取指定数据表的指定数据
        :param tbname: 数据表名称
        :param row: 数据表行
        :param column: 数据表列
        :return: 值
        '''
        #SELECT 列名 FROM 表名 WHERE ID = 行号;
        value = 0
        sql = "SELECT " +column+ " FROM " +tbname+ " WHERE ID=" +str(row)+ ";"
        self.que.exec_(sql)
        if self.que.next():
            value = self.que.value(0)
        return value

    def getSQLtableValue_by_column_value(self, tbname, column, column_value):
        '''
        读取指定数据表的指定数据
        :param tbname: 数据表名称
        :param column: 数据表列名称
        :param column_value: 查询列的值
        :return: 值,列表形式
        '''
        #SELECT 列名 FROM 表名 WHERE car_code = 行号;
        sql = "SELECT * FROM " +tbname+ " WHERE " + column + " = '" +str(column_value)+ "';"
        a = self.que.exec_(sql)
        id = []
        while self.que.next():
            id.append(self.que.value('id'))
        return id

    def getSQLtableColumn(self, tbname, column):
        '''
        读取数据表指定列的所有数据
        :param tbname: 数据表名称
        :param column: 列名称
        :return: 值列表
        '''
        #SELECT 列名 FROM 表名;
        sql = "SELECT " +column+ " FROM " +tbname+ ";"
        value_list = []
        if self.que.exec_(sql):
            column_index = self.que.record().indexOf(column) #获取列索引值
            while self.que.next():
                value = self.que.value(column_index)
                value_list.append(value)
        return value_list

    def getSQLtableRow(self, tbname, row):
        '''
        获取指定表格指定行数据
        :param tbname: 表格名称
        :param row: 行数
        :return: 值列表
        '''
        # SELECT * FROM 表名 WHERE ID=行数;
        columnNum = len(self.getSQLtableColumnName(tbname))
        sql = "SELECT * FROM " + tbname + " WHERE ID="+ str(row) +";"
        self.que.exec_(sql)
        valueList = []
        while self.que.next():
            for i in range(1, columnNum+1):
                result = self.que.value(i)
                valueList.append(result)
        return valueList

    # endregion


    # region 操作数据表

    def delSQLtableColumn(self, tbname, columnName):
        '''
        指定数据表删除指定列
        SQLite不支持删除列操作，采用复制新表的方式。
        :param tbname: 表名
        :param columnName: 列名
        :return: null
        '''
        # ALTER TABLE 表名 drop 列名;   #SQLite不支持
        tbName = "tbName0"
        CloumnNameList = self.getSQLtableColumnName(tbname)
        if columnName in CloumnNameList:
            CloumnNameList.remove(columnName)
        CloumnNameList.insert(0, "ID")
        strName = ','.join(CloumnNameList)
        # create table 零时表名 as select 所有列名称 from 表名 where 1 = 1;
        sql = u"create table "+tbName+" as select "+strName+" from "+tbname+" where 1 = 1"
        self.que.exec_(sql)
        self.delSQLtable(tbname)
        self.removeSQLtableName(tbName, tbname)

    def delSQLtableRow(self, tbname, startRow, rowNum=1):
        '''
        指定数据表删除指定行数
        :param tbname: 表格名称
        :param startRow: 开始行数
        :param rowNum: 要删除总行数
        :return: null
        '''
        # DELETE FROM 表名 WHERE ID = 行;
        for row in range(startRow, startRow + rowNum):
            sql = "DELETE FROM " + tbname + " WHERE ID = " + str(row) + ";"
            self.que.exec_(sql)

    def removeSQLtableName(self, tbname, newTbname):
        '''
        重命名表格
        :param tbname:  旧表格名称
        :param newTbname:  新表格名称
        :return:  null
        '''
        # alter table 旧表格名称 rename to 新表格名称;
        sql = u"alter table "+tbname+" rename to "+newTbname+";"
        self.que.exec_(sql)

    def ClearSQLtableRowValue(self, tbname):
        '''
        清空指定数据表
        :param tbname: 表名
        :return:  null
        '''
        # DELETE FROM table_name WHERE[condition];
        sql = "DELETE FROM " +tbname+ ";"
        self.que.exec_(sql)

    def delSQLtable(self, tbname):
        '''
        删除指定表
        :param tbname:
        :return: null
        '''
        # drop table record;
        sql = u"drop table "+tbname+";"
        self.que.exec_(sql)

    # endregion
    def getSQLAtableRow(self, table_name, param):
        pass


if __name__ == '__main__':
    print("PyQt5 SQLite实例")
    class sqliteTest():
        def __init__(self):
            self.PathFile = "./sqlite.db"
            self.tableName = "sqlite"

            # 如果存在mysql.ini先删除，方便下列代码的测试
            if os.path.exists(self.PathFile):
                os.remove(self.PathFile)

            self.sqlite = SQLiteTools()
            self.sqlite.createConnection(self.PathFile)

        #创建表
        def createTable(self):
            if not self.sqlite.selectTableExist(self.tableName):
                self.sqlite.createSQLtable(self.tableName)

        # 添加数据
        def addData(self):
            self.sqlite.addSQLtableColumn(self.tableName, "month1", "text")
            self.sqlite.addSQLtableColumn(self.tableName, "month2", "text")
            self.sqlite.addSQLtableColumn(self.tableName, "month3", "text")
            self.sqlite.addSQLtableColumn(self.tableName, "month4", "text")

            self.sqlite.addSQLtableRow(self.tableName, 30)

            self.sqlite.setSQLtableValue(self.tableName, "month1", 0, "1-0")
            self.sqlite.setSQLtableValue(self.tableName, "month1", 1, "1-1")
            self.sqlite.setSQLtableValue(self.tableName, "month2", 2, "2-2")
            self.sqlite.setSQLtableValue(self.tableName, "month2", 3, "2-3")

        # 获取数据
        def getData(self):
            value = self.sqlite.getSQLtableRowNum(self.tableName)
            print("数据表总行数：", value)

            value = self.sqlite.getSQLtableColumnName(self.tableName)
            print("所有列的名称(不包括ID列)：", value)

            value = self.sqlite.getSQLtableValue(self.tableName, "month1", 0)
            print("month1列，第一行的值：", value)

            value  = self.sqlite.getSQLtableColumn(self.tableName, "month2")
            print("month2列的所有值：", value)

            value = self.sqlite.getSQLtableRow(self.tableName, 2)
            print("第三行的所有值(不包括ID)： ", value)

        # 删除数据
        def delData(self):
            value = self.sqlite.getSQLtableRowNum(self.tableName)
            print("删除前数据表总行数：", value)
            self.sqlite.delSQLtableRow(self.tableName, 10, 5)
            value = self.sqlite.getSQLtableRowNum(self.tableName)
            print("删除后数据表总行数：", value)

            value = self.sqlite.getSQLtableColumnName(self.tableName)
            print("删除前所有列名(不包括ID)：", value)
            self.sqlite.delSQLtableColumn(self.tableName, "month3")
            value = self.sqlite.getSQLtableColumnName(self.tableName)
            print("删除后所有列名(不包括ID)", value)
            self.sqlite.ClearSQLtableRowValue(self.tableName)
            self.sqlite.delSQLtable(self.tableName)

    win = sqliteTest()
    win.createTable()
    win.addData()
    win.getData()
    win.delData()






class SQLiteTools_2():
    def __init__(self):
        pass

    # region 创建数据库连接和数据表

    def createConnection(self, DB_name):
        ''' 创建数据库连接 '''
        #创建数据库,如果存在则打开，否则创建该数据库
        self.con = sqlite3.connect(DB_name)
        #创建一个游标对象
        self.cur = self.con.cursor()

    def selectTableExist(self, tbname):
        '''
        判断指定数据表是否存在
        :param tbname: 数据表名称
        :return: 存在范围True,否则返回False
        '''
        sql = "select * from sqlite_master where type='table' and name = '" + tbname + "';"
        self.cur.execute(sql)
        cursor = self.cur.fetchall()
        if cursor:
            return True
        else:
            return False

    def createSQLtable(self, tbname):
        '''
        创建通用数据表，默认第一列为主键，名称:ID，类型:INTEGER, 自增
        :param tbname: 数据表名称
        '''
        # CREATE TABLE if not exists 表名 (ID INTEGER PRIMARY KEY AUTOINCREMENT);
        sql = u"CREATE TABLE if not exists " + tbname + u" (ID INTEGER PRIMARY KEY AUTOINCREMENT);"
        self.cur.execute(sql)
        self.con.commit()  # 提交更新至数据库文件

    # endregion



def create_SQL(sqlname):
    '''
    创建数据库
    :param sqlname: 数据库目录名称
    '''
    database = QtSql.QSqlDatabase.addDatabase('QSQLITE')
    database.setDatabaseName(sqlname)
    database.open()

def create_SQLtable(tbname):
    '''
    创建通用数据表，默认第一列为主键，名称:ID，类型:INTEGER, 自增
    :param tbname: 数据表名称
    '''
    # CREATE TABLE if not exists 表名 (ID INTEGER PRIMARY KEY AUTOINCREMENT);
    q = QSqlQuery()
    command = u"CREATE TABLE if not exists {} (ID INTEGER PRIMARY KEY AUTOINCREMENT);".format(tbname)
    q.exec_(command)

def add_SQLtable_cloumn(tbname, column_name, genre):
    '''
    指定数据表添加列
    :param tbname: 表名
    :param column_name: 列名
    :param genre: 添加列类型
    '''
    # ALTER TABLE 表名 ADD 列名 列类型;
    q = QSqlQuery()
    command = u"ALTER TABLE {} ADD {} {};".format(tbname, column_name, genre)
    q.exec_(command)

def add_SQLtable_row(tbname, row_num):
    '''
    指定数据表添加行
    :param tbname: 表格名称
    :param row_num: 行数
    '''
    # INSERT INTO 表名 (ID) VALUES (行);
    q = QSqlQuery()
    for row in range(1, row_num + 1):
        command = "INSERT INTO {} (ID) VALUES ({});".format(tbname, str(row))
        q.exec_(command)

def set_SQLtable_value(tbname, column, row, value):
    '''
    更新数据表指定位置的值
    :param tbname: 数据表名称
    :param row: 行数
    :param column: 列数
    :param value: 值
    '''
    # UPDATE 表名 SET 列名=值 WHERE ID=行;
    q = QSqlQuery()
    command = u"UPDATE {} SET {}='{}' WHERE ID={};".format(tbname, column, value, str(row))
    q.exec_(command)

def get_SQLtable_value(tbname, column, row):
    '''
    读取指定数据表的指定列行数据
    :param tbname: 数据表名称
    :param row: 数据表行
    :param column: 数据表列
    :return 返回查询到的值
    '''
    # SELECT 列名 FROM 表名 WHERE ID = 行号;
    q = QSqlQuery()
    command = "SELECT {} FROM {} WHERE ID={};".format(column, tbname, str(row))
    q.exec_(command)
    if q.next():
        result = q.value(0)
        return result

def get_SQLtable_column(tbname, column):
    '''
    读取数据表指定列的所有数据
    :param tbname: 数据表名称
    :param column: 列名称
    :return 返回查询到的值列表
    '''
    # SELECT 列名 FROM 表名;
    q = QSqlQuery()
    command = "SELECT {} FROM {};".format(column, tbname)
    value_list = []
    if q.exec_(command):
        column_index = q.record().indexOf(column)  # 获取列索引值
        while q.next():
            value = q.value(column_index)
            value_list.append(value)
    return value_list

def get_SQLtable_column_name(tbname):
    '''
    获取数据表字段名字
    :param tbname: 数据表名称
    :return: 返回字段(列)名称列表
    '''
    q = QSqlQuery()
    command = "pragma table_info({})".format(tbname)
    name_list = []
    if q.exec_(command):
        while q.next():
            column_name = q.value(1)
            name_list.append(column_name)
    return name_list

def get_SQLtable_row(tbname, row):
    '''
    读取数据表指定行的所有数据
    :param tbname: 数据表名称
    :param column: 行名称
    :return 返回查询到的值列表
    '''
    # SELECT * FROM 表名 WHERE ID = 行号;
    name_list = get_SQLtable_column_name(tbname)
    num = len(name_list) - 1
    q = QSqlQuery()
    command = "SELECT * FROM {} WHERE ID={};".format(tbname, str(row))
    value_list = []
    if q.exec_(command):
        while q.next():
            for i in range(1, num):
                value = q.value(i)
                value_list.append(value)
    return value_list

def delete_SQLtable_value(tbname):
    '''
    清空指定数据表
    :param tbname: 表名
    '''
    # DELETE FROM table_name WHERE[condition];
    q = QSqlQuery()
    command = "DELETE FROM " + tbname + ";"
    q.exec_(command)

