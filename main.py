from functools import partial
from PyQt5 import QtCore, QtWidgets
from dialog_table import Ui_Dialog
from client_record import Ui_Dialog_client_rec


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(934, 699)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(30, 50, 161, 371))
        self.pushButton.setStyleSheet("QPushButton {\n" "    font-size: 14pt;\n" "}")
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(210, 50, 161, 371))
        self.pushButton_2.setStyleSheet("QPushButton {\n" "    font-size: 14pt;\n" "}")
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(390, 50, 161, 371))
        self.pushButton_3.setStyleSheet("QPushButton {\n" "    font-size: 14pt;\n" "}")
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(570, 50, 161, 371))
        self.pushButton_4.setStyleSheet("QPushButton {\n" "    font-size: 14pt;\n" "}")
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_5 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_5.setGeometry(QtCore.QRect(20, 470, 891, 151))
        self.pushButton_5.setStyleSheet(
            "QPushButton {\n" "    font-size: 20pt;\n" "}\n" ""
        )
        self.pushButton_5.setIconSize(QtCore.QSize(20, 20))
        self.pushButton_5.setAutoRepeatDelay(300)
        self.pushButton_5.setAutoDefault(False)
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton_6 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_6.setGeometry(QtCore.QRect(750, 50, 161, 371))
        self.pushButton_6.setStyleSheet("QPushButton {\n" "    font-size: 14pt;\n" "}")
        self.pushButton_6.setObjectName("pushButton_6")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 934, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.pushButton.clicked.connect(partial(self.table_dialog, 'services'))
        self.pushButton_2.clicked.connect(partial(self.table_dialog, 'clients'))
        self.pushButton_3.clicked.connect(partial(self.table_dialog, 'employees'))
        self.pushButton_4.clicked.connect(partial(self.table_dialog, 'positions'))
        self.pushButton_6.clicked.connect(partial(self.table_dialog, 'rendered_services'))
        self.pushButton_5.clicked.connect(self.client_record)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "УСЛУГИ"))
        self.pushButton_2.setText(_translate("MainWindow", "КЛИЕНТЫ"))
        self.pushButton_3.setText(_translate("MainWindow", "СОТРУДНИКИ"))
        self.pushButton_4.setText(_translate("MainWindow", "ДОЛЖНОСТИ"))
        self.pushButton_5.setText(_translate("MainWindow", "ЗАПИСАТЬ КЛИЕНТА"))
        self.pushButton_6.setText(_translate("MainWindow", "ОКАЗАННЫЕ\n" "УСЛУГИ"))

    def table_dialog(self, table_name):
        Dialog = QtWidgets.QDialog()
        ui_table = Ui_Dialog()
        ui_table.table_name = table_name
        ui_table.setupUi(Dialog)
        Dialog.show()
        Dialog.exec_()

    def client_record(self):
        Dialog = QtWidgets.QDialog()
        ui_table = Ui_Dialog_client_rec()
        ui_table.setupUi(Dialog)
        Dialog.show()
        Dialog.exec_()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
