"""
Простий лаунчер ігор для навчання
"""
import tkinter as tk
from tkinter import filedialog, messagebox
import json
import os
import subprocess


class SimpleLauncher:
    def __init__(self):
        # Створюємо головне вікно
        self.window = tk.Tk()
        self.window.title("Лаунчер Ігор")
        self.window.geometry("600x400")
        
        # Файл для збереження ігор
        self.games_file = "games_simple.json"
        self.games = []
        
        # Завантажуємо ігри
        self.load_games()
        
        # Створюємо інтерфейс
        self.create_ui()
        
    def create_ui(self):
        """Створення інтерфейсу"""
        # Заголовок
        title = tk.Label(
            self.window,
            text="МОЇ ІГРИ",
            font=("Arial", 20, "bold")
        )
        title.pack(pady=10)
        
        # Кнопка додавання
        add_btn = tk.Button(
            self.window,
            text="➕ Додати гру",
            command=self.add_game,
            font=("Arial", 12),
            bg="#4CAF50",
            fg="white",
            width=15
        )
        add_btn.pack(pady=10)
        
        # Список ігор
        frame = tk.Frame(self.window)
        frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Скролбар
        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side="right", fill="y")
        
        # Listbox для ігор
        self.listbox = tk.Listbox(
            frame,
            font=("Arial", 12),
            yscrollcommand=scrollbar.set,
            height=10
        )
        self.listbox.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.listbox.yview)
        
        # Кнопки управління
        buttons_frame = tk.Frame(self.window)
        buttons_frame.pack(pady=10)
        
        play_btn = tk.Button(
            buttons_frame,
            text="▶ Грати",
            command=self.play_game,
            font=("Arial", 12),
            bg="#2196F3",
            fg="white",
            width=10
        )
        play_btn.pack(side="left", padx=5)
        
        delete_btn = tk.Button(
            buttons_frame,
            text="🗑 Видалити",
            command=self.delete_game,
            font=("Arial", 12),
            bg="#f44336",
            fg="white",
            width=10
        )
        delete_btn.pack(side="left", padx=5)
        
        # Оновлюємо список
        self.update_list()
        
    def update_list(self):
        """Оновлення списку ігор"""
        self.listbox.delete(0, tk.END)
        for game in self.games:
            self.listbox.insert(tk.END, game['name'])
            
    def add_game(self):
        """Додавання нової гри"""
        # Вибір файлу
        file_path = filedialog.askopenfilename(
            title="Виберіть гру",
            filetypes=[("Програми", "*.exe"), ("Всі файли", "*.*")]
        )
        
        if file_path:
            # Отримуємо назву
            name = os.path.basename(file_path)
            
            # Додаємо в список
            new_game = {
                'name': name,
                'path': file_path
            }
            self.games.append(new_game)
            
            # Зберігаємо та оновлюємо
            self.save_games()
            self.update_list()
            
            messagebox.showinfo("Успіх", f"Додано: {name}")
            
    def play_game(self):
        """Запуск гри"""
        # Отримуємо вибрану гру
        selection = self.listbox.curselection()
        
        if not selection:
            messagebox.showwarning("Увага", "Виберіть гру!")
            return
            
        # Запускаємо
        index = selection[0]
        game = self.games[index]
        
        try:
            subprocess.Popen([game['path']])
            messagebox.showinfo("Запуск", f"Запущено: {game['name']}")
        except Exception as e:
            messagebox.showerror("Помилка", f"Не вдалося запустити:\n{e}")
            
    def delete_game(self):
        """Видалення гри"""
        selection = self.listbox.curselection()
        
        if not selection:
            messagebox.showwarning("Увага", "Виберіть гру!")
            return
            
        index = selection[0]
        game = self.games[index]
        
        # Підтвердження
        if messagebox.askyesno("Видалення", f"Видалити {game['name']}?"):
            self.games.pop(index)
            self.save_games()
            self.update_list()
            
    def save_games(self):
        """Збереження в JSON"""
        with open(self.games_file, 'w', encoding='utf-8') as f:
            json.dump(self.games, f, ensure_ascii=False, indent=4)
            
    def load_games(self):
        """Завантаження з JSON"""
        if os.path.exists(self.games_file):
            with open(self.games_file, 'r', encoding='utf-8') as f:
                self.games = json.load(f)
        else:
            self.games = []
            
    def run(self):
        """Запуск програми"""
        self.window.mainloop()


# Запуск програми
if __name__ == "__main__":
    app = SimpleLauncher()
    app.run()
