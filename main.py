import tkinter as tk
from tkinter import ttk, messagebox
import random
import string
import json
import os
import pyperclip

class PasswordGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Password Generator")
        self.root.geometry("600x500")

        # Переменные
        self.password_length = tk.IntVar(value=12)
        self.use_digits = tk.BooleanVar(value=True)
        self.use_letters = tk.BooleanVar(value=True)
        self.use_special = tk.BooleanVar(value=False)
        self.generated_passwords = []

        self.setup_ui()
        self.load_history()

    def setup_ui(self):
        # Ползунок длины пароля
        ttk.Label(self.root, text="Длина пароля:").pack(pady=5)
        length_scale = ttk.Scale(self.root, from_=4, to=64,
                                   variable=self.password_length, orient=tk.HORIZONTAL)
        length_scale.pack(pady=5, fill=tk.X, padx=20)

        length_label = ttk.Label(self.root,
                              textvariable=self.password_length)
        length_label.pack()

        # Чекбоксы для выбора символов
        ttk.Checkbutton(self.root, text="Цифры (0-9)",
                        variable=self.use_digits).pack(anchor=tk.W, padx=20)
        ttk.Checkbutton(self.root, text="Буквы (a-z, A-Z)",
                        variable=self.use_letters).pack(anchor=tk.W, padx=20)
        ttk.Checkbutton(self.root, text="Спецсимволы (!@#$%)",
                        variable=self.use_special).pack(anchor=tk.W, padx=20)

        # Кнопка генерации
        generate_btn = ttk.Button(self.root, text="Сгенерировать пароль",
                                 command=self.generate_password)
        generate_btn.pack(pady=10)

        # Поле для отображения пароля
        self.password_entry = ttk.Entry(self.root, font=("Courier", 12),
                                   justify=tk.CENTER)
        self.password_entry.pack(fill=tk.X, padx=20, pady=5)

        # Кнопка копирования в буфер обмена
        copy_btn = ttk.Button(self.root, text="Копировать в буфер обмена",
                             command=self.copy_to_clipboard)
        copy_btn.pack(pady=5)

        # Таблица истории
        ttk.Label(self.root, text="История паролей:").pack(pady=(20, 5))

        columns = ("ID", "Пароль", "Длина", "Символы")
        self.history_tree = ttk.Treeview(self.root, columns=columns, show="headings")

        for col in columns:
            self.history_tree.heading(col, text=col)
            self.history_tree.column(col, width=100)

        self.history_tree.pack(fill=tk.BOTH, expand=True, padx=20, pady=5)

    def generate_password(self):
        # Проверка корректности ввода
        if not (self.use_digits.get() or self.use_letters.get()
                or self.use_special.get()):
            messagebox.showerror("Ошибка", "Выберите хотя бы один тип символов!")
            return

        if self.password_length.get() < 4:
            messagebox.showerror("Ошибка", "Минимальная длина пароля — 4 символа!")
            return
        elif self.password_length.get() > 64:
            messagebox.showerror("Ошибка", "Максимальная длина пароля — 64 символа!")
            return

        # Формирование набора символов
        characters = ""
        if self.use_digits.get():
            characters += string.digits
        if self.use_letters.get():
            characters += string.ascii_letters
        if self.use_special.get():
            characters += "!@#$%^&*()_+-=[]{}|;:,.<>?"

        # Генерация пароля
        password = ''.join(random.choice(characters)
                           for _ in range(self.password_length.get()))

        # Отображение пароля
        self.password_entry.delete(0, tk.END)
        self.password_entry.insert(0, password)

        # Добавление в историю
        self.add_to_history(password)

    def add_to_history(self, password):
        char_types = []
        if self.use_digits.get(): char_types.append("Цифры")
        if self.use_letters.get(): char_types.append("Буквы")
        if self.use_special.get(): char_types.append("Спецсимволы")

        entry = {
            "id": len(self.generated_passwords) + 1,
            "password": password,
            "length": self.password_length.get(),
            "characters": ", ".join(char_types)
        }

        self.generated_passwords.append(entry)
        self.update_history_table()
        self.save_history()

    def update_history_table(self):
        # Очистка таблицы
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)

        # Заполнение таблицы
        for entry in self.generated_passwords:
            self.history_tree.insert("", tk.END, values=(
                entry["id"], entry["password"],
                entry["length"], entry["characters"]
            ))

    def copy_to_clipboard(self):
        password = self.password_entry.get()
        if password:
            pyperclip.copy(password)
            messagebox.showinfo("Успех", "Пароль скопирован в буфер обмена!")

    def save_history(self):
        with open("password_history.json", "w", encoding="utf-8") as f:
            json.dump(self.generated_passwords, f, indent=2, ensure_ascii=False)

    def load_history(self):
        if os.path.exists("password_history.json"):
            try:
                with open("password_history.json", "r", encoding="utf-8") as f:
                    self.generated_passwords = json.load(f)
                self.update_history_table()
            except json.JSONDecodeError:
                self.generated_passwords = []

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGeneratorApp(root)
    root.mainloop()
