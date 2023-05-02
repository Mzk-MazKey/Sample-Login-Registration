import sqlite3
import subprocess
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QDialog, QFormLayout, QLineEdit, QPushButton, QVBoxLayout, QLabel)

class LoginWindow(QDialog):
    def __init__(self):
        super().__init__()

        # Создание интерфейса окна входа
        self.setWindowTitle('Login')
        self.setWindowIcon(QIcon('icon.png'))
        self.setStyleSheet('font-size: 18px;')

        label = QLabel('Login', self)
        label.setFont(QFont('Arial', 24))
        label.setAlignment(Qt.AlignCenter)

        self.username_edit = QLineEdit(self)
        self.username_edit.setPlaceholderText('Enter username')

        self.password_edit = QLineEdit(self)
        self.password_edit.setPlaceholderText('Enter password')
        self.password_edit.setEchoMode(QLineEdit.Password)

        self.login_button = QPushButton('Login', self)
        self.login_button.setStyleSheet('background-color: #4CAF50; color: white; border-radius: 10px; padding: 10px; font-size: 18px;')

        self.register_button = QPushButton('Register', self)
        self.register_button.setStyleSheet('background-color: #008CBA; color: white; border-radius: 10px; padding: 10px; font-size: 18px;')

        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(self.username_edit)
        layout.addWidget(self.password_edit)
        layout.addWidget(self.login_button)
        layout.addWidget(self.register_button)
        layout.setAlignment(Qt.AlignCenter)

        self.setLayout(layout)

        # Подключение базы данных SQLite
        self.connection = sqlite3.connect('database.db')
        self.cursor = self.connection.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS users
                             (id INTEGER PRIMARY KEY AUTOINCREMENT,
                              username TEXT NOT NULL,
                              password TEXT NOT NULL)''')
        self.connection.commit()

        # Связывание кнопок входа и регистрации с функциями обработки событий
        self.login_button.clicked.connect(self.login)
        self.register_button.clicked.connect(self.register)

    def login(self):
        # Извлечение имени пользователя и пароля из текстовых полей
        username = self.username_edit.text()
        password = self.password_edit.text()

        # Поиск пользователя в базе данных
        self.cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
        user = self.cursor.fetchone()

        if user is not None:
            # Открытие окна с базой данных
            self.accept()
        else:
            # Вывод сообщения об ошибке, если пользователь не найден
            label = QLabel('Invalid username or password', self)
            label.setFont(QFont('Arial', 18))
            label.setStyleSheet('color: red;')
            label.setAlignment(Qt.AlignCenter)

            layout = QVBoxLayout()
            layout.addWidget(label)
            layout.setAlignment(Qt.AlignCenter)

            self.setLayout(layout)

    def register(self):
        # Открытие окна регистрации
        registration_window = RegistrationWindow()
        registration_window.exec_()

class RegistrationWindow(QDialog):
    def __init__(self):
        super().__init__()

        # Создание интерфейса окна регистрации
        self.setWindowTitle('Registration')
        self.setWindowIcon(QIcon('icon.png'))
        self.setStyleSheet('font-size: 18px;')

        label = QLabel('Registration', self)
        label.setFont(QFont('Arial', 24))
        label.setAlignment(Qt.AlignCenter)
        self.username_edit = QLineEdit(self)
        self.username_edit.setPlaceholderText('Enter username')

        self.password_edit = QLineEdit(self)
        self.password_edit.setPlaceholderText('Enter password')
        self.password_edit.setEchoMode(QLineEdit.Password)

        self.confirm_password_edit = QLineEdit(self)
        self.confirm_password_edit.setPlaceholderText('Confirm password')
        self.confirm_password_edit.setEchoMode(QLineEdit.Password)

        self.register_button = QPushButton('Register', self)
        self.register_button.setStyleSheet('background-color: #008CBA; color: white; border-radius: 10px; padding: 10px; font-size: 18px;')

        layout = QFormLayout()
        layout.addRow(label)
        layout.addRow('Username:', self.username_edit)
        layout.addRow('Password:', self.password_edit)
        layout.addRow('Confirm password:', self.confirm_password_edit)
        layout.addRow(self.register_button)
        layout.setAlignment(Qt.AlignCenter)

        self.setLayout(layout)

        # Подключение базы данных SQLite
        self.connection = sqlite3.connect('database.db')
        self.cursor = self.connection.cursor()

        # Связывание кнопки регистрации с функцией обработки событий
        self.register_button.clicked.connect(self.register)

    def register(self):
        # Извлечение имени пользователя и пароля из текстовых полей
        username = self.username_edit.text()
        password = self.password_edit.text()
        confirm_password = self.confirm_password_edit.text()

        # Проверка, что пароль и подтверждение пароля совпадают
        if password != confirm_password:
            # Вывод сообщения об ошибке, если пароли не совпадают
            label = QLabel('Passwords do not match', self)
            label.setFont(QFont('Arial', 18))
            label.setStyleSheet('color: red;')
            label.setAlignment(Qt.AlignCenter)

            layout = QVBoxLayout()
            layout.addWidget(label)
            layout.setAlignment(Qt.AlignCenter)

            self.setLayout(layout)
        else:
            # Добавление нового пользователя в базу данных
            self.cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
            self.connection.commit()

            # Вывод сообщения об успешной регистрации
            label = QLabel('Registration successful', self)
            label.setFont(QFont('Arial', 18))
            label.setStyleSheet('color: green;')
            label.setAlignment(Qt.AlignCenter)

            layout = QVBoxLayout()
            layout.addWidget(label)
            layout.setAlignment(Qt.AlignCenter)

            self.setLayout(layout)  
            self.username_edit.clear()
            self.password_edit.clear()
            self.confirm_password_edit.clear()   
        
    def handle_login(self):
        # Проверка учетных данных
        if self.username == 'admin' and self.password == 'admin':
            self.accept()  # Вход выполнен успешно, закрываем окно
            # Запуск другого файла
            subprocess.run(['python', 'steam.py'])
        else:
            QMessageBox.warning(self, 'Error', 'Invalid username or password')
            # Очищаем поля для ввода
            self.username_input.setText('')
            self.password_input.setText('')

if __name__ == '__main__':
    app = QApplication([])
    login_window = LoginWindow()
    if login_window.exec_() == QDialog.Accepted:
        print('Login successful')
        # Открытие окна с базой данных
    else:
        print('Login canceled')
    app.quit()
