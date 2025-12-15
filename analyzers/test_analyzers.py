# test_analyzers.py
from analyzers import SimpleAnalyzer, HistoricalAnalyzer
from json_storage import JSONStorage

# Тест
api_key = "sk-3de96d9f4f88438aa5584831f6b9b0d2"
storage = JSONStorage()

simple = SimpleAnalyzer(api_key)
historical = HistoricalAnalyzer(api_key)

# Тестовые сообщения
test_messages = [
    {'text': 'Биткоин вырос на 10% за сутки'},
    {'text': 'Акции Tesla обновляют максимумы'},
    {'text': 'ФРС оставила ставки без изменений'}
]

# Тестируем
print("Testing SimpleAnalyzer...")
result1 = simple.analyze(test_messages, "test_channel")
print(result1[:200], "...")

print("\nTesting HistoricalAnalyzer...")
result2 = historical.analyze(test_messages, "test_channel", storage)
print(result2[:200], "...")