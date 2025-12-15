# analyzers/simple_analyzer.py
from .base_analyzer import BaseAnalyzer


class SimpleAnalyzer(BaseAnalyzer):
    def analyze(self, messages, channel, storage=None):
        """Простой анализ без истории"""

        formatted_messages = self._format_messages(messages, limit=10, max_length=200)

        prompt = f"""
Проанализируй эти сообщения из финансового Telegram-канала {channel} и составь краткий аналитический отчет:

{formatted_messages}

Выдели:
• 3-4 основные темы обсуждения
• Ключевые тренды или тенденции  
• Важные события или новости
• Общую тональность обсуждений

Будь конкретен и используй примеры из сообщений.
Длина текста не более 4000 символов.
"""

        print(f"🔍 SimpleAnalyzer: анализируем {len(messages)} сообщений из {channel}")

        result = self._call_ai(prompt)

        # Очищаем Markdown
        clean_result = self._clean_markdown(result)

        return clean_result