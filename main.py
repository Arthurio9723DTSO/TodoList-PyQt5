import json
import os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QListWidget
from PyQt5.QtGui import QIcon

SAVE_FILE = "tasks.json"

class TodoApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("To-Do List")
        self.setWindowIcon(QIcon("icon.ico"))

        layout = QVBoxLayout()

        # Поле ввода
        self.input = QLineEdit()
        self.input.setPlaceholderText("Enter a task...")
        layout.addWidget(self.input)

        # Кнопка добавления
        add_btn = QPushButton("Add Task")
        add_btn.clicked.connect(self.add_task)
        layout.addWidget(add_btn)

        # Кнопка удаления
        delete_btn = QPushButton("Delete Task")
        delete_btn.clicked.connect(self.delete_task)
        layout.addWidget(delete_btn)

        # Кнопка очистки
        clear_btn = QPushButton("Clear All")
        clear_btn.clicked.connect(self.clear_all)
        layout.addWidget(clear_btn)

        # Список
        self.list = QListWidget()
        layout.addWidget(self.list)

        self.setLayout(layout)

        # Загружаем задачи из файла
        self.load_tasks()

    # --- ЛОГИКА ---

    def add_task(self):
        task = self.input.text()
        if task:
            self.list.addItem(task)
            self.input.clear()
            self.save_tasks()

    def delete_task(self):
        selected = self.list.currentRow()
        if selected >= 0:
            self.list.takeItem(selected)
            self.save_tasks()

    def clear_all(self):
        self.list.clear()
        self.save_tasks()

    # --- СОХРАНЕНИЕ ---

    def save_tasks(self):
        tasks = []
        for i in range(self.list.count()):
            tasks.append(self.list.item(i).text())

        with open(SAVE_FILE, "w", encoding="utf-8") as f:
            json.dump(tasks, f, ensure_ascii=False, indent=4)

    def load_tasks(self):
        if not os.path.exists(SAVE_FILE):
            return

        try:
            with open(SAVE_FILE, "r", encoding="utf-8") as f:
                tasks = json.load(f)
                for t in tasks:
                    self.list.addItem(t)
        except:
            pass


app = QApplication([])
window = TodoApp()
window.show()
app.exec()
