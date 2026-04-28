"""
Графический интерфейс для Random Quote Generator
Автор: Суфияров Роман Алексеевич
"""

import tkinter as tk
from tkinter import ttk, messagebox
from quote_manager import QuoteManager

class QuoteGeneratorGUI:
    """Основной класс GUI приложения"""
    
    def __init__(self, root):
        self.root = root
        self.quote_manager = QuoteManager()
        
        # Настройка главного окна
        self.root.title("Random Quote Generator - Генератор случайных цитат")
        self.root.geometry("950x750")
        self.root.configure(bg='#2c3e50')
        
        # Стили
        self.setup_styles()
        
        # Создание интерфейса
        self.create_widgets()
        
        # Обновление фильтров
        self.update_filters()
        
        # Первая случайная цитата
        self.generate_quote()
    
    def setup_styles(self):
        """Настройка стилей"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Цветовая схема
        self.bg_color = '#2c3e50'
        self.fg_color = '#ecf0f1'
        self.accent_color = '#3498db'
        self.success_color = '#27ae60'
        self.danger_color = '#e74c3c'
    
    def create_widgets(self):
        """Создание всех виджетов интерфейса"""
        
        # Основной контейнер
        main_frame = tk.Frame(self.root, bg=self.bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Заголовок
        title_label = tk.Label(main_frame, text="✨ Генератор случайных цитат ✨", 
                               font=('Arial', 20, 'bold'), bg=self.bg_color, fg=self.fg_color)
        title_label.pack(pady=10)
        
        # === Панель генерации ===
        self.create_generation_panel(main_frame)
        
        # === Панель добавления цитаты ===
        self.create_add_quote_panel(main_frame)
        
        # === Панель фильтрации ===
        self.create_filter_panel(main_frame)
        
        # === Таблица с цитатами ===
        self.create_quotes_table(main_frame)
        
        # === История генераций ===
        self.create_history_panel(main_frame)
        
        # === Статус бар ===
        self.status_var = tk.StringVar()
        self.status_var.set("✅ Готов к работе")
        status_bar = tk.Label(main_frame, textvariable=self.status_var, 
                              relief=tk.SUNKEN, anchor=tk.W, bg='#34495e', fg=self.fg_color)
        status_bar.pack(fill=tk.X, pady=(10, 0))
    
    def create_generation_panel(self, parent):
        """Создание панели для генерации цитаты"""
        gen_frame = tk.Frame(parent, bg=self.bg_color)
        gen_frame.pack(fill=tk.X, pady=10)
        
        # Рамка для цитаты
        quote_frame = tk.Frame(gen_frame, bg=self.accent_color, relief=tk.RIDGE, bd=2)
        quote_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.quote_text_var = tk.StringVar()
        self.quote_text_var.set("Нажмите кнопку, чтобы получить цитату")
        
        quote_label = tk.Label(quote_frame, textvariable=self.quote_text_var, 
                               font=('Georgia', 14, 'italic'), bg=self.accent_color, 
                               fg='white', wraplength=800, justify=tk.CENTER)
        quote_label.pack(padx=20, pady=15)
        
        self.author_var = tk.StringVar()
        self.author_var.set("")
        
        author_label = tk.Label(quote_frame, textvariable=self.author_var, 
                                font=('Arial', 11), bg=self.accent_color, 
                                fg='#ecf0f1', wraplength=800)
        author_label.pack(pady=(0, 10))
        
        # Кнопка генерации
        generate_btn = tk.Button(gen_frame, text="🎲 Сгенерировать случайную цитату", 
                                 command=self.generate_quote, bg=self.success_color, fg='white',
                                 font=('Arial', 12, 'bold'), padx=20, pady=10)
        generate_btn.pack(pady=10)
    
    def create_add_quote_panel(self, parent):
        """Создание панели добавления новой цитаты"""
        add_frame = tk.LabelFrame(parent, text="➕ Добавить новую цитату", 
                                   font=('Arial', 10, 'bold'), bg=self.bg_color, 
                                   fg=self.fg_color, bd=2, relief=tk.GROOVE)
        add_frame.pack(fill=tk.X, pady=10)
        
        inner_frame = tk.Frame(add_frame, bg=self.bg_color)
        inner_frame.pack(padx=10, pady=10)
        
        # Текст цитаты
        tk.Label(inner_frame, text="Цитата:", bg=self.bg_color, fg=self.fg_color).grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.quote_entry = tk.Text(inner_frame, width=60, height=3)
        self.quote_entry.grid(row=0, column=1, columnspan=3, padx=5, pady=5)
        
        # Автор
        tk.Label(inner_frame, text="Автор:", bg=self.bg_color, fg=self.fg_color).grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.author_entry = tk.Entry(inner_frame, width=30)
        self.author_entry.grid(row=1, column=1, padx=5, pady=5)
        
        # Тема
        tk.Label(inner_frame, text="Тема:", bg=self.bg_color, fg=self.fg_color).grid(row=1, column=2, sticky=tk.W, padx=5, pady=5)
        self.topic_entry = tk.Entry(inner_frame, width=20)
        self.topic_entry.grid(row=1, column=3, padx=5, pady=5)
        
        # Кнопка добавления
        add_btn = tk.Button(inner_frame, text="➕ Добавить цитату", 
                           command=self.add_quote, bg=self.accent_color, fg='white',
                           font=('Arial', 10, 'bold'), padx=10)
        add_btn.grid(row=2, column=0, columnspan=4, pady=10)
    
    def create_filter_panel(self, parent):
        """Создание панели фильтрации"""
        filter_frame = tk.LabelFrame(parent, text="🔍 Фильтрация цитат", 
                                      font=('Arial', 10, 'bold'), bg=self.bg_color, 
                                      fg=self.fg_color, bd=2, relief=tk.GROOVE)
        filter_frame.pack(fill=tk.X, pady=10)
        
        inner_frame = tk.Frame(filter_frame, bg=self.bg_color)
        inner_frame.pack(padx=10, pady=10)
        
        # Фильтр по автору
        tk.Label(inner_frame, text="Автор:", bg=self.bg_color, fg=self.fg_color).grid(row=0, column=0, padx=5)
        self.author_filter_var = tk.StringVar(value="Все авторы")
        self.author_filter_combo = ttk.Combobox(inner_frame, textvariable=self.author_filter_var, 
                                                 width=20, state='readonly')
        self.author_filter_combo.grid(row=0, column=1, padx=5)
        self.author_filter_combo.bind('<<ComboboxSelected>>', lambda e: self.refresh_quotes_table())
        
        # Фильтр по теме
        tk.Label(inner_frame, text="Тема:", bg=self.bg_color, fg=self.fg_color).grid(row=0, column=2, padx=5)
        self.topic_filter_var = tk.StringVar(value="Все темы")
        self.topic_filter_combo = ttk.Combobox(inner_frame, textvariable=self.topic_filter_var, 
                                                width=20, state='readonly')
        self.topic_filter_combo.grid(row=0, column=3, padx=5)
        self.topic_filter_combo.bind('<<ComboboxSelected>>', lambda e: self.refresh_quotes_table())
        
        # Кнопки
        btn_frame = tk.Frame(inner_frame, bg=self.bg_color)
        btn_frame.grid(row=1, column=0, columnspan=4, pady=10)
        
        apply_btn = tk.Button(btn_frame, text="🔍 Применить фильтры", 
                             command=self.refresh_quotes_table, bg=self.accent_color, fg='white')
        apply_btn.pack(side=tk.LEFT, padx=5)
        
        reset_btn = tk.Button(btn_frame, text="🔄 Сбросить фильтры", 
                             command=self.reset_filters, bg='#e67e22', fg='white')
        reset_btn.pack(side=tk.LEFT, padx=5)
        
        # Информация о количестве
        self.quotes_count_var = tk.StringVar(value="Всего цитат: 0")
        count_label = tk.Label(inner_frame, textvariable=self.quotes_count_var, 
                               bg=self.bg_color, fg=self.fg_color, font=('Arial', 9, 'italic'))
        count_label.grid(row=2, column=0, columnspan=4, pady=5)
    
    def create_quotes_table(self, parent):
        """Создание таблицы со всеми цитатами"""
        table_frame = tk.LabelFrame(parent, text="📚 Библиотека цитат", 
                                     font=('Arial', 10, 'bold'), bg=self.bg_color, 
                                     fg=self.fg_color, bd=2, relief=tk.GROOVE)
        table_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Контейнер с прокруткой
        container = tk.Frame(table_frame, bg=self.bg_color)
        container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Создание Treeview
        columns = ('text', 'author', 'topic')
        self.tree = ttk.Treeview(container, columns=columns, show='headings', height=6)
        
        self.tree.heading('text', text='Цитата')
        self.tree.heading('author', text='Автор')
        self.tree.heading('topic', text='Тема')
        
        self.tree.column('text', width=500)
        self.tree.column('author', width=150)
        self.tree.column('topic', width=120)
        
        # Скроллбар
        scrollbar = ttk.Scrollbar(container, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Кнопка удаления
        delete_btn = tk.Button(table_frame, text="🗑️ Удалить выбранную цитату", 
                               command=self.delete_quote, bg=self.danger_color, fg='white',
                               font=('Arial', 9), padx=10)
        delete_btn.pack(pady=5)
    
    def create_history_panel(self, parent):
        """Создание панели истории"""
        history_frame = tk.LabelFrame(parent, text="📜 История генераций", 
                                       font=('Arial', 10, 'bold'), bg=self.bg_color, 
                                       fg=self.fg_color, bd=2, relief=tk.GROOVE)
        history_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Контейнер
        container = tk.Frame(history_frame, bg=self.bg_color)
        container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Списбокс для истории
        scrollbar = tk.Scrollbar(container)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.history_listbox = tk.Listbox(container, yscrollcommand=scrollbar.set,
                                           font=('Arial', 10), bg='#34495e', fg=self.fg_color,
                                           selectmode=tk.SINGLE, height=5)
        self.history_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.history_listbox.yview)
        
        # Кнопки управления историей
        btn_frame = tk.Frame(history_frame, bg=self.bg_color)
        btn_frame.pack(pady=5)
        
        clear_history_btn = tk.Button(btn_frame, text="🗑️ Очистить историю", 
                                      command=self.clear_history, bg=self.danger_color, fg='white')
        clear_history_btn.pack(side=tk.LEFT, padx=5)
        
        refresh_history_btn = tk.Button(btn_frame, text="🔄 Обновить историю", 
                                        command=self.refresh_history, bg=self.accent_color, fg='white')
        refresh_history_btn.pack(side=tk.LEFT, padx=5)
    
    def generate_quote(self):
        """Генерирует случайную цитату"""
        quote = self.quote_manager.get_random_quote()
        
        self.quote_text_var.set(f'"{quote.text}"')
        self.author_var.set(f"— {quote.author} | 📚 {quote.topic}")
        
        # Добавляем в историю
        self.quote_manager.add_to_history(quote)
        self.refresh_history()
        
        self.status_var.set(f"✨ Сгенерирована цитата: {quote.author}")
    
    def add_quote(self):
        """Добавляет новую цитату"""
        text = self.quote_entry.get("1.0", tk.END).strip()
        author = self.author_entry.get().strip()
        topic = self.topic_entry.get().strip()
        
        success, message = self.quote_manager.add_quote(text, author, topic)
        
        if success:
            messagebox.showinfo("Успех", message)
            self.clear_add_quote_fields()
            self.refresh_quotes_table()
            self.update_filters()
            self.status_var.set(f"✅ Добавлена цитата: {author}")
        else:
            messagebox.showerror("Ошибка", message)
    
    def clear_add_quote_fields(self):
        """Очищает поля добавления цитаты"""
        self.quote_entry.delete("1.0", tk.END)
        self.author_entry.delete(0, tk.END)
        self.topic_entry.delete(0, tk.END)
    
    def delete_quote(self):
        """Удаляет выбранную цитату"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите цитату для удаления!")
            return
        
        # Получаем текст цитаты
        item = self.tree.item(selected[0])
        quote_text = item['values'][0]
        quote_author = item['values'][1]
        
        if messagebox.askyesno("Подтверждение", f'Удалить цитату "{quote_text[:50]}..."?'):
            # Находим индекс
            for i, quote in enumerate(self.quote_manager.quotes):
                if quote.text == quote_text and quote.author == quote_author:
                    self.quote_manager.remove_quote(i)
                    break
            
            self.refresh_quotes_table()
            self.update_filters()
            self.status_var.set(f"🗑️ Удалена цитата: {quote_author}")
    
    def refresh_quotes_table(self):
        """Обновляет таблицу цитат с учётом фильтров"""
        # Очищаем таблицу
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Получаем цитаты
        quotes = self.quote_manager.quotes
        
        # Применяем фильтры
        selected_author = self.author_filter_var.get()
        if selected_author != "Все авторы":
            quotes = self.quote_manager.filter_by_author(selected_author)
        
        selected_topic = self.topic_filter_var.get()
        if selected_topic != "Все темы":
            quotes = self.quote_manager.filter_by_topic(selected_topic)
        
        # Отображаем
        for quote in quotes:
            self.tree.insert('', tk.END, values=(quote.text, quote.author, quote.topic))
        
        count = len(quotes)
        total = self.quote_manager.get_quotes_count()
        self.quotes_count_var.set(f"Показано: {count} из {total} цитат")
        self.status_var.set(f"📚 Найдено цитат: {count}")
    
    def refresh_history(self):
        """Обновляет список истории"""
        self.history_listbox.delete(0, tk.END)
        
        history = self.quote_manager.get_history()
        for entry in history:
            display_text = f'[{entry.generated_at}] "{entry.quote.text[:50]}..." — {entry.quote.author}'
            self.history_listbox.insert(tk.END, display_text)
        
        if not history:
            self.history_listbox.insert(tk.END, "История пуста. Сгенерируйте первую цитату!")
        
        count = len(history)
        self.status_var.set(f"📜 В истории {count} записей")
    
    def clear_history(self):
        """Очищает историю"""
        if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите очистить всю историю?"):
            success, message = self.quote_manager.clear_history()
            self.refresh_history()
            self.status_var.set(message)
    
    def update_filters(self):
        """Обновляет выпадающие списки фильтров"""
        authors = self.quote_manager.get_unique_authors()
        authors.insert(0, "Все авторы")
        self.author_filter_combo['values'] = authors
        
        topics = self.quote_manager.get_unique_topics()
        topics.insert(0, "Все темы")
        self.topic_filter_combo['values'] = topics
    
    def reset_filters(self):
        """Сбрасывает фильтры"""
        self.author_filter_var.set("Все авторы")
        self.topic_filter_var.set("Все темы")
        self.refresh_quotes_table()
        self.status_var.set("🔄 Фильтры сброшены")