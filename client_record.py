from functools import partial
from PyQt5 import QtCore, QtGui, QtWidgets
from dialog_table import Ui_Dialog
from db_handler import db_connection, foreign_key_manager


class Ui_Dialog_client_rec(object):
    def __init__(self):
        self.db_connection = db_connection
        self.foreign_key_manager = foreign_key_manager

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(934, 699)
        self.comboBox = QtWidgets.QComboBox(Dialog)
        self.comboBox.setGeometry(QtCore.QRect(30, 110, 200, 31))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("ФИО КЛИЕНТА", userData=None)
        self.comboBox_2 = QtWidgets.QComboBox(Dialog)
        self.comboBox_2.setGeometry(QtCore.QRect(350, 110, 200, 31))
        self.comboBox_2.setObjectName("comboBox_2")
        self.comboBox_2.addItem("ФИО ВРАЧА", userData=None)
        self.comboBox_3 = QtWidgets.QComboBox(Dialog)
        self.comboBox_3.setGeometry(QtCore.QRect(660, 110, 200, 31))
        self.comboBox_3.setObjectName("comboBox_3")
        self.comboBox_3.addItem("НАЗВАНИЕ ПРОЦЕДУРЫ", userData=None)
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(660, 630, 241, 31))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(Dialog)
        self.pushButton_2.setGeometry(QtCore.QRect(240, 110, 31, 31))
        self.pushButton_2.setObjectName("pushButton_2")
        self.dateTimeEdit = QtWidgets.QDateTimeEdit(Dialog)
        self.dateTimeEdit.setGeometry(QtCore.QRect(350, 250, 241, 31))
        self.dateTimeEdit.setAccelerated(False)
        self.dateTimeEdit.setProperty("showGroupSeparator", False)
        self.dateTimeEdit.setDateTime(QtCore.QDateTime(QtCore.QDate(2024, 1, 1), QtCore.QTime(0, 0, 0)))
        self.dateTimeEdit.setCalendarPopup(True)
        self.dateTimeEdit.setObjectName("dateTimeEdit")
        self.pushButton_3 = QtWidgets.QPushButton(Dialog)
        self.pushButton_3.setGeometry(QtCore.QRect(560, 110, 31, 31))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_4 = QtWidgets.QPushButton(Dialog)
        self.pushButton_4.setGeometry(QtCore.QRect(870, 110, 31, 31))
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_5 = QtWidgets.QPushButton(Dialog)
        self.pushButton_5.setGeometry(QtCore.QRect(350, 400, 241, 31))
        self.pushButton_5.setObjectName("pushButton_5")
        self.plainTextEdit = QtWidgets.QPlainTextEdit(Dialog)
        self.plainTextEdit.setGeometry(QtCore.QRect(30, 550, 441, 111))
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.load_data_to_combo_boxes()
        self.pushButton.clicked.connect(self.table_show)
        self.pushButton_2.clicked.connect(partial(self.table_dialog, 'clients'))
        self.pushButton_3.clicked.connect(partial(self.table_dialog, 'employees'))
        self.pushButton_4.clicked.connect(partial(self.table_dialog, 'services'))
        self.pushButton_5.clicked.connect(self.add_record)
        self.pushButton.clicked.connect(lambda: self.plainTextEdit.clear())
        self.pushButton_2.clicked.connect(lambda: self.plainTextEdit.clear())
        self.pushButton_3.clicked.connect(lambda: self.plainTextEdit.clear())
        self.pushButton_4.clicked.connect(lambda: self.plainTextEdit.clear())
        self.comboBox.activated.connect(lambda: self.plainTextEdit.clear())
        self.comboBox_2.activated.connect(lambda: self.plainTextEdit.clear())
        self.comboBox_3.activated.connect(lambda: self.plainTextEdit.clear())
        self.dateTimeEdit.dateTimeChanged.connect(lambda: self.plainTextEdit.clear())

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.pushButton.setText(_translate("Dialog", "ОТОБРАЗИТЬ ТАБЛИЦУ"))
        self.pushButton_2.setText(_translate("Dialog", "+"))
        self.pushButton_3.setText(_translate("Dialog", "+"))
        self.pushButton_4.setText(_translate("Dialog", "+"))
        self.pushButton_5.setText(_translate("Dialog", "ДОБАВИТЬ ЗАПИСЬ"))

    def load_data_to_combo_boxes(self):
        self.db_connection.connect()

        # get selecting from db for comboBoxes
        self.clients_data = self.db_connection.get_data_from_db("SELECT id, fio FROM clients;").fetchall()
        self.employees_data = self.db_connection.get_data_from_db("SELECT id, fio FROM employees;").fetchall()
        self.services_data = self.db_connection.get_data_from_db("SELECT id, name FROM services;").fetchall()

        # loading data to comboBox
        for dt in self.clients_data:
            self.comboBox.addItem(dt[1], userData=dt[0])

        for dt in self.employees_data:
            self.comboBox_2.addItem(dt[1], userData=dt[0])

        for dt in self.services_data:
            self.comboBox_3.addItem(dt[1], userData=dt[0])

        self.db_connection.disconnect()

    def table_dialog(self, table_name):
        Dialog = QtWidgets.QDialog()
        ui_table = Ui_Dialog()
        ui_table.table_name = table_name
        ui_table.setupUi(Dialog)
        Dialog.show()
        Dialog.exec_()

        self.clients_data.clear()
        self.employees_data.clear()
        self.services_data.clear()

        self.load_data_to_combo_boxes()

    def add_record(self):
        self.db_connection.connect()

        # gets id from comboBox (userData) for writing rendered_services table
        client_id = self.comboBox.currentData()
        employee_id = self.comboBox_2.currentData()
        service_id = self.comboBox_3.currentData()
        time = self.dateTimeEdit.dateTime().toString("yyyy-MM-dd HH:mm")

        if client_id and employee_id and service_id and time:
            sql_query = "INSERT INTO rendered_services (time , client_id, employee_id, service_id) VALUES (?, ?, ?, ?)"
            self.db_connection.execute_one(sql_query, (time, client_id, employee_id, service_id))
            self.db_connection.disconnect()
            self.plainTextEdit.setPlainText("Новая запись успешно добавлена!")
        else:
            self.plainTextEdit.setPlainText("Ошибка: Не все обязательные значения выбраны. Пожалуйста, убедитесь, что вы сделали выбор в каждом выпадающем списке перед продолжением.")

        self.db_connection.disconnect()

    def table_show(self):
        Dialog = QtWidgets.QDialog()
        ui_table = Ui_Dialog()
        ui_table.table_name = 'rendered_services'
        ui_table.setupUi(Dialog)
        Dialog.show()
        Dialog.exec_()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog_client_rec()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
