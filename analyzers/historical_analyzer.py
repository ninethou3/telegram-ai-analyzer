# analyzers/historical_analyzer.py
from .base_analyzer import BaseAnalyzer


class HistoricalAnalyzer(BaseAnalyzer):
    def analyze(self, messages, channel, storage):
        """Анализ с историческим контекстом"""

        if storage is None:
            return "❌ Для исторического анализа требуется storage"

        # Получаем исторические сообщения
        historical_messages = storage.get_recent_messages(channel, 20)

        # Форматируем
        current_texts = self._format_messages(messages, limit=5, max_length=200)
        historical_texts = self._format_messages(historical_messages, limit=5, max_length=150)

        prompt = f"""
Анализ канала: {channel}

Последние сообщения ({len(messages)}):
{current_texts}

Исторический контекст ({len(historical_messages)} сообщений):
{historical_texts}

Ответь на вопросы:
1. Что нового по сравнению с историей?
2. Какие темы повторяются?
3. Изменилась ли тональность?
"""

        print(f"📚 HistoricalAnalyzer: анализируем с историей из {channel}")
        result = self._call_ai(prompt)

        # Очищаем Markdown
        clean_result = self._clean_markdown(result)

        return clean_result