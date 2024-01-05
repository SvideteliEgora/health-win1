from PyQt5 import QtCore, QtGui, QtWidgets
import re
from datetime import datetime
from db_handler import db_connection, foreign_key_manager


class ValidateData:
    foreign_key_manager = foreign_key_manager

    def validate_str_tel(self, tel: str):
        tel_pattern = re.compile(r'^\+375\d{9}$')

        if tel_pattern.match(tel):
            return tel
        else:
            raise ValueError("Ошибка: Некорректный формат телефонного номера. Введите в формате +375XXXXXXXXX.")


    def validate_date(self, date: str):
        date_pattern = re.compile(r'^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])$')
        if date_pattern.match(date):
            return date
        else:
            raise ValueError("Ошибка: Некорректный формат даты. Введите в формате YYYY-MM-DD.")

    def validate_timestamp(self, time: str):
        try:
            datetime.strptime(time, '%Y-%m-%d %H:%M')
            return time
        except ValueError:
            raise ValueError("Ошибка: Некорректный формат даты и времени. Введите в формате YYYY-MM-DD HH:MM.")

    def validate_integer(self, number: str):
        try:
            return int(number)
        except ValueError:
            raise ValueError("Ошибка: Некорректный формат данных. Ожидалось целое число (INTEGER)")

    def validate_real(self, salary: str):
        try:
            salary = float(salary)
            return salary
        except ValueError:
            raise ValueError("Ошибка: Некорректный формат данных. Ожидалось вещественное число (REAL)")

    def validate_text(self, text: str):
        if isinstance(text, str):
            return text
        else:
            raise ValueError("Ошибка: Некорректный формат данных. Ожидалась строка (TEXT).")

    def __validate_id(self, value: str, id_getter, name_getter):
        pattern = re.compile(r'^\d+ - [\w\s]+$')

        try:
            if value.isdigit():
                ident = int(value)
                data = id_getter(ident)
                if data[1] != 'NULL':
                    return " - ".join(map(str, data))
                else:
                    raise ValueError(
                        f"Ошибка: Запись с идентификатором '{value}' не найдена. Пожалуйста, убедитесь, что введенное значение существует в указанной таблице.")

            elif pattern.match(value):
                ident = int(value.split(" - ")[0])
                data = id_getter(ident)
                data_str = " - ".join(map(str, data))
                if data_str == value:
                    return value
                else:
                    raise ValueError(
                        f"Ошибка: Неверное имя или идентификатор. Пожалуйста, проверьте введенное значение.")
            else:
                data = name_getter(value)
                if data[0] != 'NULL':
                    return " - ".join(map(str, data))
                else:
                    raise ValueError(
                        f"Ошибка: Запись с именем '{value}' не найдена. Пожалуйста, убедитесь, что введенное значение существует в указанной таблице.")
        except ValueError as e:
            print(f"Ошибка валидации: {e}")
            raise

    def validate_position_id(self, value: str):
        return self.__validate_id(value, self.foreign_key_manager.get_position_by_id, self.foreign_key_manager.get_position_by_name)

    def validate_client_id(self, value: str):
        return self.__validate_id(value, self.foreign_key_manager.get_client_by_id, self.foreign_key_manager.get_client_by_fio)

    def validate_employee_id(self, value: str):
        return self.__validate_id(value, self.foreign_key_manager.get_employee_by_id, self.foreign_key_manager.get_employee_by_fio)

    def validate_service_id(self, value: str):
        return self.__validate_id(value, self.foreign_key_manager.get_service_by_id, self.foreign_key_manager.get_service_by_name)


class Ui_Dialog(object):
    table_name = ''

    def __init__(self):
        self.table_data = []
        self.initial_table_data = []
        self.new_identifiers = []
        self.db_connection = db_connection
        self.db_connection.connect()
        self.foreign_key_manager = foreign_key_manager
        self.validate_data = ValidateData()
        self.table_info = {}
        self.errors = {}
        self.new_row = None
        self.flag_on_item_changed = True    # update on self.tableWidget.blockSignals(False)

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(934, 699)
        self.tableWidget = QtWidgets.QTableWidget(Dialog)
        self.tableWidget.setGeometry(QtCore.QRect(40, 120, 851, 431))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.plainTextEdit = QtWidgets.QPlainTextEdit(Dialog)
        self.plainTextEdit.setGeometry(QtCore.QRect(40, 560, 491, 131))
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.horizontalLayoutWidget = QtWidgets.QWidget(Dialog)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(550, 590, 341, 81))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton_2 = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout.addWidget(self.pushButton_2)
        self.pushButton = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(Dialog)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(540, 30, 351, 71))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.pushButton_3 = QtWidgets.QPushButton(self.horizontalLayoutWidget_2)
        self.pushButton_3.setObjectName("pushButton_3")
        self.horizontalLayout_2.addWidget(self.pushButton_3)
        self.pushButton_4 = QtWidgets.QPushButton(self.horizontalLayoutWidget_2)
        self.pushButton_4.setObjectName("pushButton_4")
        self.horizontalLayout_2.addWidget(self.pushButton_4)
        self.load_table_structure_from_db()
        self.pushButton_3.clicked.connect(self.add_row)
        self.pushButton_4.clicked.connect(self.delete_filed)
        self.tableWidget.itemChanged.connect(self.on_item_changed)
        self.tableWidget.itemChanged.connect(self.check_row_completion)
        self.pushButton_2.clicked.connect(self.save_all)
        self.pushButton.clicked.connect(self.cancel_all)
        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.pushButton_2.setText(_translate("Dialog", "Сохранить"))
        self.pushButton.setText(_translate("Dialog", "Отменить"))
        self.pushButton_3.setText(_translate("Dialog", "Добавить"))
        self.pushButton_4.setText(_translate("Dialog", "Удалить"))

    def update_table_widget_data(self, table_data):
        select_all = self.db_connection.get_data_from_db("SELECT * FROM {};".format(self.table_name)).fetchall()
        column_count = len(self.table_info)

        column_titles = tuple(self.table_info.keys())

        for row in select_all:
            table_data.append(tuple(str(item) for item in row))

        row_count = len(select_all)
        self.tableWidget.setRowCount(row_count)
        for row in range(row_count):
            for col in range(column_count):
                if column_titles[col] == 'position_id':
                    data = self.foreign_key_manager.get_position_by_id(table_data[row][col+1])
                    data = " - ".join(data)
                    item = QtWidgets.QTableWidgetItem(data)

                elif column_titles[col] == 'client_id':
                    data = self.foreign_key_manager.get_client_by_id(table_data[row][col+1])
                    data = " - ".join(data)
                    item = QtWidgets.QTableWidgetItem(data)

                elif column_titles[col] == 'employee_id':
                    data = self.foreign_key_manager.get_employee_by_id(table_data[row][col+1])
                    data = " - ".join(data)
                    item = QtWidgets.QTableWidgetItem(data)

                elif column_titles[col] == 'service_id':
                    data = self.foreign_key_manager.get_service_by_id(table_data[row][col+1])
                    data = " - ".join(data)
                    item = QtWidgets.QTableWidgetItem(data)

                else:
                    item = QtWidgets.QTableWidgetItem(table_data[row][col+1])

                self.tableWidget.setItem(row, col, item)
                if col:
                    self.tableWidget.setColumnWidth(col, 200)
                else:
                    self.tableWidget.setColumnWidth(col, 300)

    def load_table_structure_from_db(self):
        columns_info = self.db_connection.get_data_from_db("PRAGMA table_info({})".format(self.table_name)).fetchall()[1:]
        for item in columns_info:
            field = item[1]
            field_type = item[2]
            if field_type == 'TEXT' and field == 'tel':
                self.table_info[field] = self.validate_data.validate_str_tel
            elif field_type == 'INTEGER' and field == 'position_id':
                self.table_info[field] = self.validate_data.validate_position_id
            elif field_type == 'INTEGER' and field == 'client_id':
                self.table_info[field] = self.validate_data.validate_client_id
            elif field_type == 'INTEGER' and field == 'employee_id':
                self.table_info[field] = self.validate_data.validate_employee_id
            elif field_type == 'INTEGER' and field == 'service_id':
                self.table_info[field] = self.validate_data.validate_service_id
            elif field_type == 'INTEGER':
                self.table_info[field] = self.validate_data.validate_integer
            elif field_type == 'DATE':
                self.table_info[field] = self.validate_data.validate_date
            elif field_type == 'TIMESTAMP':
                self.table_info[field] = self.validate_data.validate_timestamp
            elif field_type == 'REAL':
                self.table_info[field] = self.validate_data.validate_real
            else:
                self.table_info[field] = self.validate_data.validate_text

        self.tableWidget.clear()

        column_count = len(columns_info)
        self.tableWidget.setColumnCount(column_count)
        column_headers = [column[1] for column in columns_info]
        self.tableWidget.setHorizontalHeaderLabels(column_headers)
        self.update_table_widget_data(self.initial_table_data)
        self.table_data = self.initial_table_data.copy()

    def on_item_changed(self, item):
        if self.plainTextEdit.toPlainText() == 'Данные сохранены!':
            self.plainTextEdit.clear()
        if self.flag_on_item_changed:
            row = item.row()
            column_number = item.column()
            data = item.text()
            column_title = self.tableWidget.horizontalHeaderItem(column_number).text()
            column_validate_func = self.table_info.get(column_title)

            try:
                identifier = int(self.table_data[row][0])
            except Exception as e:
                identifier = None
                print(str(e))
            # expression = column_info[1].format('data')
            try:
                # dt = eval(expression)
                dt = column_validate_func(data)

                print(dt)

                if self.errors.get(str((row, column_number))):
                    del self.errors[str((row, column_number))]

                if identifier is not None and row != self.new_row:
                    if column_title in ['position_id', 'employee_id', 'service_id', 'client_id']:
                        value = int(dt.split(" - ")[0])
                    else:
                        value = dt
                    self.db_connection.add_query("UPDATE '{}' SET {} = '{}' WHERE id = {};".format(self.table_name, column_title, value, identifier))

                if column_title in ['position_id', 'employee_id', 'service_id', 'client_id']:
                    item = QtWidgets.QTableWidgetItem(dt)
                    self.tableWidget.blockSignals(True)
                    self.tableWidget.setItem(row, column_number, item)
                    self.tableWidget.blockSignals(False)

            except Exception as e:
                self.errors[str((row, column_number))] = str(e)
            finally:
                text = ''
                if self.errors:
                    print(self.errors)
                for row_col, error_text in self.errors.items():
                    text += f'{row_col}: {error_text}\n'
                self.plainTextEdit.setPlainText(text)

    def check_row_completion(self, item):
        current_row = item.row()
        if self.new_row == current_row:
            is_row_complete = all(
                self.tableWidget.item(current_row, col) is not None
                and self.tableWidget.item(current_row, col).text() != ''
                and not self.plainTextEdit.toPlainText()
                for col in range(self.tableWidget.columnCount())
            )
            if is_row_complete:
                print(f"Ряд {current_row + 1} был полностью заполнен.")

                items = []
                for col in range(self.tableWidget.columnCount()):
                    items.append(self.tableWidget.item(current_row, col).text())

                columns = str(tuple([i for i in self.table_info.keys()])).replace("'", "")
                items = str(tuple(items))

                self.db_connection.connect()
                query = "INSERT INTO {} {} VALUES {};".format(self.table_name, columns, items)
                self.db_connection.execute_one(query)
                last_record = self.db_connection.get_data_from_db("SELECT * FROM {} ORDER BY id DESC LIMIT 1".format(self.table_name)).fetchone()
                self.table_data.append(last_record[1:])
                self.new_identifiers.append(last_record[0])
                self.new_row = None
                self.db_connection.disconnect()

    def add_row(self):
        if self.plainTextEdit.toPlainText() == 'Данные сохранены!':
            self.plainTextEdit.clear()
        last_row = self.tableWidget.rowCount() - 1
        if last_row == -1:
            self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
        flag = True
        column_count = self.tableWidget.columnCount()
        self.new_row = self.tableWidget.rowCount() - 1
        for col in range(column_count):
            item = self.tableWidget.item(last_row, col)
            if not item or self.plainTextEdit.toPlainText():
                print(f'Error (row {last_row}; col {col}): empty field')
                flag = False
        if flag:
            self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
            self.new_row = self.tableWidget.rowCount() - 1

    def delete_filed(self):
        if self.plainTextEdit.toPlainText() == 'Данные сохранены!':
            self.plainTextEdit.clear()
        selected_items = self.tableWidget.selectedItems()
        selected_ranges = self.tableWidget.selectedRanges()

        rows_to_del = []
        for ran in selected_ranges:
            top_row = ran.topRow()
            bottom_row = ran.bottomRow()
            left_column = ran.leftColumn()
            right_column = ran.rightColumn()

            if top_row == bottom_row and left_column == 0 and right_column == self.tableWidget.columnCount() - 1:
                rows_to_del.append(top_row)

        if rows_to_del:
            for row in rows_to_del:
                try:
                    identifier = int(self.table_data[row][0])
                    self.db_connection.add_query("DELETE FROM '{}' WHERE id = {};".format(self.table_name, identifier))
                except Exception as e:
                    print(str(e))

        for item in selected_items:
            row = item.row()
            column = item.column()
            try:
                if row not in rows_to_del:
                    field = self.tableWidget.horizontalHeaderItem(column).text()
                    identifier = int(self.table_data[row][0])
                    self.db_connection.add_query("UPDATE '{}' SET {} = NULL WHERE id = {};".format(self.table_name, field, identifier))
                self.tableWidget.takeItem(row, column)
            except Exception as e:
                print(str(e))

    def save_all(self):
        if not self.plainTextEdit.toPlainText() and not self.new_row:
            self.db_connection.execute_all()
            self.db_connection.clear_queries()
            self.flag_on_item_changed = False
            self.table_data.clear()
            self.initial_table_data.clear()
            self.update_table_widget_data(self.table_data)
            self.initial_table_data = self.table_data.copy()
            self.new_identifiers.clear()
            self.flag_on_item_changed = True
            self.plainTextEdit.setPlainText('Данные сохранены!')

    def cancel_all(self):
        self.errors.clear()
        self.new_row = None
        self.plainTextEdit.clear()
        self.flag_on_item_changed = False
        self.db_connection.clear_queries()
        if self.new_identifiers:
            print(self.new_identifiers)
            for identifier in self.new_identifiers:
                self.db_connection.execute_one("DELETE FROM {} WHERE id = {}".format(self.table_name, identifier))
            self.new_identifiers.clear()
        self.update_table_widget_data(self.initial_table_data)
        self.initial_table_data = self.table_data
        self.flag_on_item_changed = True

    def __del__(self):
        self.db_connection.disconnect()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())



