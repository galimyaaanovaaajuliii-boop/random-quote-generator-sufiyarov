"""
Модуль для управления цитатами
Содержит логику работы с цитатами, историей и JSON
Автор: Суфияров Роман Алексеевич
"""

import json
import os
import random
from typing import List, Dict, Tuple
from datetime import datetime

class Quote:
    """Класс для представления цитаты"""
    
    def __init__(self, text: str, author: str, topic: str):
        self.text = text.strip()
        self.author = author.strip()
        self.topic = topic.strip()
    
    def to_dict(self) -> Dict:
        """Преобразует цитату в словарь для JSON"""
        return {
            'text': self.text,
            'author': self.author,
            'topic': self.topic
        }
    
    @classmethod
    def from_dict(cls, data: Dict):
        """Создаёт цитату из словаря"""
        return cls(data['text'], data['author'], data['topic'])
    
    def __str__(self):
        return f'"{self.text}" — {self.author}'

class HistoryEntry:
    """Класс для записи истории генерации"""
    
    def __init__(self, quote: Quote, generated_at: str = None):
        self.quote = quote
        self.generated_at = generated_at or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def to_dict(self) -> Dict:
        return {
            'quote': self.quote.to_dict(),
            'generated_at': self.generated_at
        }
    
    @classmethod
    def from_dict(cls, data: Dict):
        quote = Quote.from_dict(data['quote'])
        return cls(quote, data.get('generated_at', datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

class QuoteManager:
    """Класс для управления цитатами"""
    
    def __init__(self, quotes_file: str = "quotes.json", history_file: str = "history.json"):
        self.quotes_file = quotes_file
        self.history_file = history_file
        self.quotes: List[Quote] = []
        self.history: List[HistoryEntry] = []
        self.load_quotes()
        self.load_history()
    
    def load_quotes(self):
        """Загружает цитаты из JSON файла"""
        if not os.path.exists(self.quotes_file):
            self.add_default_quotes()
            return
        
        try:
            with open(self.quotes_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            self.quotes = [Quote.from_dict(item) for item in data]
        except Exception as e:
            print(f"Ошибка при загрузке цитат: {e}")
            self.add_default_quotes()
    
    def add_default_quotes(self):
        """Добавляет предопределённые цитаты"""
        default_quotes = [
            ("Будь тем изменением, которое хочешь видеть в мире.", "Махатма Ганди", "Мотивация"),
            ("Жизнь — это то, что с тобой происходит, пока ты строишь планы.", "Джон Леннон", "Жизнь"),
            ("Успех — это способность идти от неудачи к неудаче, не теряя энтузиазма.", "Уинстон Черчилль", "Успех"),
            ("Самое трудное — это начать действовать, остальное зависит только от упорства.", "Амелия Эрхарт", "Мотивация"),
            ("Знание — сила.", "Фрэнсис Бэкон", "Знание"),
            ("Я мыслю, следовательно, существую.", "Рене Декарт", "Философия"),
            ("Не бойтесь совершенства, вам его не достичь.", "Сальвадор Дали", "Юмор"),
            ("Единственный способ сделать великую работу — любить то, что ты делаешь.", "Стив Джобс", "Успех"),
            ("Вдохновение приходит только во время работы.", "Габриэль Гарсиа Маркес", "Творчество"),
            ("Оптимист видит возможность в каждой опасности, пессимист видит опасность в каждой возможности.", "Уинстон Черчилль", "Мотивация"),
            ("Сложнее всего начать действовать, проще продолжать.", "Рэй Брэдбери", "Творчество"),
            ("Лучший способ предсказать будущее — изобрести его.", "Алан Кей", "Инновации"),
        ]
        for text, author, topic in default_quotes:
            self.quotes.append(Quote(text, author, topic))
        self.save_quotes()
    
    def save_quotes(self) -> bool:
        """Сохраняет цитаты в JSON файл"""
        try:
            data = [quote.to_dict() for quote in self.quotes]
            with open(self.quotes_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"Ошибка при сохранении цитат: {e}")
            return False
    
    def load_history(self):
        """Загружает историю из JSON файла"""
        if not os.path.exists(self.history_file):
            self.history = []
            return
        
        try:
            with open(self.history_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            self.history = [HistoryEntry.from_dict(item) for item in data]
        except Exception as e:
            print(f"Ошибка при загрузке истории: {e}")
            self.history = []
    
    def save_history(self) -> bool:
        """Сохраняет историю в JSON файл"""
        try:
            data = [entry.to_dict() for entry in self.history]
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"Ошибка при сохранении истории: {e}")
            return False
    
    def add_quote(self, text: str, author: str, topic: str) -> Tuple[bool, str]:
        """
        Добавляет новую цитату с валидацией
        
        Returns:
            Tuple[bool, str]: (успех, сообщение)
        """
        # Валидация
        if not text or not text.strip():
            return False, "Текст цитаты не может быть пустым!"
        
        if not author or not author.strip():
            return False, "Автор не может быть пустым!"
        
        if not topic or not topic.strip():
            return False, "Тема не может быть пустой!"
        
        # Проверка на дубликат
        for quote in self.quotes:
            if quote.text.lower() == text.lower() and quote.author.lower() == author.lower():
                return False, "Такая цитата уже существует!"
        
        quote = Quote(text, author, topic)
        self.quotes.append(quote)
        self.save_quotes()
        return True, "Цитата успешно добавлена!"
    
    def remove_quote(self, index: int) -> Tuple[bool, str]:
        """Удаляет цитату по индексу"""
        if 0 <= index < len(self.quotes):
            deleted_text = self.quotes[index].text
            del self.quotes[index]
            self.save_quotes()
            return True, f"Цитата удалена!"
        return False, "Цитата не найдена!"
    
    def get_random_quote(self) -> Quote:
        """Возвращает случайную цитату"""
        if not self.quotes:
            return Quote("Нет доступных цитат", "Система", "Инфо")
        return random.choice(self.quotes)
    
    def add_to_history(self, quote: Quote):
        """Добавляет цитату в историю"""
        entry = HistoryEntry(quote)
        self.history.insert(0, entry)  # Новые сверху
        # Ограничим историю 100 записями
        if len(self.history) > 100:
            self.history = self.history[:100]
        self.save_history()
    
    def get_history(self) -> List[HistoryEntry]:
        """Возвращает историю генераций"""
        return self.history.copy()
    
    def clear_history(self) -> Tuple[bool, str]:
        """Очищает историю"""
        self.history = []
        self.save_history()
        return True, "История очищена!"
    
    def filter_by_author(self, author: str) -> List[Quote]:
        """Фильтрует цитаты по автору"""
        if not author or author == "Все авторы":
            return self.quotes
        return [quote for quote in self.quotes if quote.author.lower() == author.lower()]
    
    def filter_by_topic(self, topic: str) -> List[Quote]:
        """Фильтрует цитаты по теме"""
        if not topic or topic == "Все темы":
            return self.quotes
        return [quote for quote in self.quotes if quote.topic.lower() == topic.lower()]
    
    def get_unique_authors(self) -> List[str]:
        """Возвращает список уникальных авторов"""
        authors = sorted(set(quote.author for quote in self.quotes))
        return authors
    
    def get_unique_topics(self) -> List[str]:
        """Возвращает список уникальных тем"""
        topics = sorted(set(quote.topic for quote in self.quotes))
        return topics
    
    def get_quotes_count(self) -> int:
        """Возвращает количество цитат"""
        return len(self.quotes)
    
    def get_history_count(self) -> int:
        """Возвращает количество записей в истории"""
        return len(self.history)