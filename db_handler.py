import sqlite3


DB_NAME = "data_base.db"


class DB_connection:
    __obj = None

    def __new__(cls, *args, **kwargs):
        if cls.__obj is None:
            cls.__obj = super().__new__(cls)
        return cls.__obj

    def __init__(self, db_name):
        self.connection = None
        self.cursor = None
        self.db_name = db_name
        self.db_queries = []

    def connect(self):
        try:
            self.connection = sqlite3.connect(self.db_name)
            self.cursor = self.connection.cursor()
            print(f"Connected to {self.db_name}")
        except Exception as e:
            print(f"Error connecting to the database: {e}")

    def add_query(self, query):
        self.db_queries.append(query)

    def execute_all(self):
        try:
            for query in self.db_queries:
                self.cursor.execute(query)
            self.connection.commit()
        except Exception as e:
            print(f"Error executing query: {e}")

    def get_data_from_db(self, query):
        return self.cursor.execute(query)

    def execute_one(self, query, params=None):
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            self.connection.commit()
        except Exception as e:
            print(f"Error executing query: {e}")

    def get_queries(self):
        return self.db_queries

    def clear_queries(self):
        self.db_queries.clear()

    def disconnect(self):
        if self.connection:
            self.connection.close()
            print("Disconnected from the database")

    def __del__(self):
        DB_connection.__obj = None


class ForeignKeyManager:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def __get_data_by_id(self, table, data_id, field="name"):
        try:
            query = f"SELECT id, {field} FROM {table} WHERE id = {data_id}"
            data = list(self.db_connection.get_data_from_db(query).fetchone())
            data = list(map(str, data))
            return tuple(data)
        except Exception as e:
            print(f"Error in get_data_by_id: {e}")
            return (str(data_id), 'NULL')

    def __get_data_by_name(self, table, name, field="name"):
        try:
            query = f"SELECT id, {field} FROM {table} WHERE {field} LIKE '%{name}%'"
            data = list(self.db_connection.get_data_from_db(query).fetchone())
            data = list(map(str, data))
            return tuple(data)
        except Exception as e:
            print(f"Error in get_data_by_name: {e}")
            return ('NULL', str(name))

    def get_client_by_id(self, client_id):
        print(f"Вызван get_client_by_id с id={client_id}")
        return self.__get_data_by_id("clients", client_id, "fio")

    def get_client_by_fio(self, fio):
        print(f"Вызван get_client_by_fio с id={fio}")
        return self.__get_data_by_name("clients", fio, "fio")

    def get_employee_by_id(self, employee_id):
        print(f"Вызван get_employee_by_id с id={employee_id}")
        return self.__get_data_by_id("employees", employee_id, "fio")

    def get_employee_by_fio(self, fio):
        print(f"Вызван get_employee_by_fio с id={fio}")
        return self.__get_data_by_name("employees", fio, "fio")

    def get_service_by_id(self, service_id):
        print(f"Вызван get_service_by_id с id={service_id}")
        return self.__get_data_by_id("services", service_id)

    def get_service_by_name(self, name):
        print(f"Вызван get_service_by_name с id={name}")
        return self.__get_data_by_name("services", name)

    def get_position_by_id(self, position_id):
        print(f"Вызван get_position_by_id с id={position_id}")
        return self.__get_data_by_id("positions", position_id)

    def get_position_by_name(self, name):
        print(f"Вызван get_position_by_name с id={name}")
        return self.__get_data_by_name("positions", name)


db_connection = DB_connection(DB_NAME)
foreign_key_manager = ForeignKeyManager(db_connection)


if __name__ == '__main__':
    db_connection = DB_connection(DB_NAME)

    db_connection.add_query('''
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            salary REAL,
            cab TEXT
        )
    ''')

    db_connection.add_query('''
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fio TEXT,
            tel TEXT,
            date_of_birth DATE,
            comment TEXT
        )
    ''')

    db_connection.add_query('''
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fio TEXT,
            date_of_birth DATE,
            tel TEXT,  -- Запятая была пропущена здесь
            position_id INTEGER,
            FOREIGN KEY (position_id) REFERENCES positions(id)
        )
    ''')

    db_connection.add_query('''
        CREATE TABLE IF NOT EXISTS services (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            price REAL,
            time_sec INTEGER,
            position_id INTEGER,
            FOREIGN KEY (position_id) REFERENCES positions(id)
        )
    ''')

    db_connection.add_query('''
        CREATE TABLE IF NOT EXISTS rendered_services (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            client_id INTEGER,
            employee_id INTEGER,
            service_id INTEGER,
            FOREIGN KEY (client_id) REFERENCES clients(id) ON DELETE CASCADE,
            FOREIGN KEY (employee_id) REFERENCES employees(id) ON DELETE CASCADE,
            FOREIGN KEY (service_id) REFERENCES services(id) ON DELETE CASCADE
        )
    ''')

    db_connection.connect()
    db_connection.execute_all()
    db_connection.disconnect()
    db_connection.clear_queries()