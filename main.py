"""
Random Quote Generator - Генератор случайных цитат
Автор: Суфияров Роман Алексеевич
Версия: 1.0
"""

import tkinter as tk
from gui import QuoteGeneratorGUI

def main():
    """Запуск приложения"""
    try:
        root = tk.Tk()
        app = QuoteGeneratorGUI(root)
        root.mainloop()
    except Exception as e:
        print(f"Ошибка при запуске приложения: {e}")

if __name__ == "__main__":
    main()