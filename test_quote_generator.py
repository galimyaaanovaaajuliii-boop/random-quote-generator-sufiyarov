"""
Модульные тесты для Random Quote Generator
Автор: Суфияров Роман Алексеевич
"""

import unittest
import os
import tempfile
from quote_manager import Quote, QuoteManager

class TestQuote(unittest.TestCase):
    """Тесты для класса Quote"""
    
    def test_quote_creation(self):
        """Тест создания цитаты"""
        quote = Quote("Тестовая цитата", "Тестовый автор", "Тест")
        self.assertEqual(quote.text, "Тестовая цитата")
        self.assertEqual(quote.author, "Тестовый автор")
        self.assertEqual(quote.topic, "Тест")
    
    def test_quote_to_dict(self):
        """Тест преобразования в словарь"""
        quote = Quote("Тест", "Автор", "Тема")
        data = quote.to_dict()
        self.assertEqual(data['text'], "Тест")
        self.assertEqual(data['author'], "Автор")
    
    def test_quote_from_dict(self):
        """Тест создания из словаря"""
        data = {'text': 'Тест', 'author': 'Автор', 'topic': 'Тема'}
        quote = Quote.from_dict(data)
        self.assertEqual(quote.text, "Тест")


class TestQuoteManager(unittest.TestCase):
    """Тесты для класса QuoteManager"""
    
    def setUp(self):
        self.temp_quotes = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
        self.temp_history = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
        self.temp_quotes.close()
        self.temp_history.close()
        self.manager = QuoteManager(self.temp_quotes.name, self.temp_history.name)
    
    def tearDown(self):
        if os.path.exists(self.temp_quotes.name):
            os.unlink(self.temp_quotes.name)
        if os.path.exists(self.temp_history.name):
            os.unlink(self.temp_history.name)
    
    def test_add_quote_positive(self):
        """Тест успешного добавления цитаты"""
        success, message = self.manager.add_quote("Новая цитата", "Новый автор", "Новая тема")
        self.assertTrue(success)
        self.assertEqual(self.manager.get_quotes_count(), 13)  # 12 дефолтных + 1
    
    def test_add_quote_empty_text(self):
        """Тест добавления с пустым текстом"""
        success, message = self.manager.add_quote("", "Автор", "Тема")
        self.assertFalse(success)
        self.assertIn("пустым", message)
    
    def test_add_quote_empty_author(self):
        """Тест добавления с пустым автором"""
        success, message = self.manager.add_quote("Цитата", "", "Тема")
        self.assertFalse(success)
    
    def test_add_quote_empty_topic(self):
        """Тест добавления с пустой темой"""
        success, message = self.manager.add_quote("Цитата", "Автор", "")
        self.assertFalse(success)
    
    def test_add_quote_duplicate(self):
        """Тест добавления дубликата"""
        self.manager.add_quote("Дубликат", "Автор", "Тема")
        success, message = self.manager.add_quote("Дубликат", "Автор", "Тема")
        self.assertFalse(success)
        self.assertIn("существует", message)
    
    def test_get_random_quote(self):
        """Тест получения случайной цитаты"""
        quote = self.manager.get_random_quote()
        self.assertIsNotNone(quote.text)
    
    def test_filter_by_author(self):
        """Тест фильтрации по автору"""
        filtered = self.manager.filter_by_author("Махатма Ганди")
        self.assertTrue(all(q.author == "Махатма Ганди" for q in filtered))
    
    def test_filter_by_topic(self):
        """Тест фильтрации по теме"""
        filtered = self.manager.filter_by_topic("Мотивация")
        self.assertTrue(all(q.topic == "Мотивация" for q in filtered))
    
    def test_get_unique_authors(self):
        """Тест получения уникальных авторов"""
        authors = self.manager.get_unique_authors()
        self.assertGreater(len(authors), 0)
        self.assertIn("Махатма Ганди", authors)
    
    def test_get_unique_topics(self):
        """Тест получения уникальных тем"""
        topics = self.manager.get_unique_topics()
        self.assertGreater(len(topics), 0)
        self.assertIn("Мотивация", topics)
    
    def test_add_to_history(self):
        """Тест добавления в историю"""
        quote = Quote("Тест", "Автор", "Тема")
        self.manager.add_to_history(quote)
        self.assertEqual(self.manager.get_history_count(), 1)
    
    def test_clear_history(self):
        """Тест очистки истории"""
        quote = Quote("Тест", "Автор", "Тема")
        self.manager.add_to_history(quote)
        success, _ = self.manager.clear_history()
        self.assertTrue(success)
        self.assertEqual(self.manager.get_history_count(), 0)
    
    def test_remove_quote(self):
        """Тест удаления цитаты"""
        before = self.manager.get_quotes_count()
        self.manager.remove_quote(0)
        after = self.manager.get_quotes_count()
        self.assertEqual(after, before - 1)
    
    def test_save_and_load(self):
        """Тест сохранения и загрузки"""
        self.manager.add_quote("Тест сохранения", "Тест", "Тест")
        
        new_manager = QuoteManager(self.temp_quotes.name, self.temp_history.name)
        self.assertGreaterEqual(new_manager.get_quotes_count(), 1)


def run_tests():
    """Запуск всех тестов"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    suite.addTests(loader.loadTestsFromTestCase(TestQuote))
    suite.addTests(loader.loadTestsFromTestCase(TestQuoteManager))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print("\n" + "="*60)
    print(f"📊 РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ:")
    print(f"✅ Запущено тестов: {result.testsRun}")
    print(f"✅ Успешно: {result.testsRun - len(result.failures) - len(result.errors)}")
    print("="*60)
    
    return result.wasSuccessful()

if __name__ == "__main__":
    run_tests()