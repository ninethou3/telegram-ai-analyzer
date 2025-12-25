# analyzers/base_analyzer.py
from abc import ABC, abstractmethod
from openai import OpenAI


class BaseAnalyzer(ABC):
    def __init__(self, api_key, base_url="https://api.deepseek.com/v1", model="deepseek-chat"):
        self.client = OpenAI(api_key=api_key, base_url=base_url)
        self.model = model
        self.max_tokens = 2000

    @abstractmethod
    def analyze(self, messages, channel, storage=None):
        """Основной метод анализа"""
        pass

    def _call_ai(self, prompt):
        """Общий метод для вызова AI"""
        try:
            print(f"📡 [AI Call] Модель: {self.model}, URL: {self.client.base_url}")
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=self.max_tokens,
                temperature = 0.7  # Добавим немного креативности
            )
            content = response.choices[0].message.content
            if not content:
                print("⚠️ [AI Call] Модель вернула пустой ответ!")
                return "Модель не смогла сформулировать ответ."

            print(f"📩 [AI Call] Получен ответ ({len(content)} симв.)")
            return content
        except Exception as e:
            print(f"❌ [AI Call] Ошибка при вызове: {e}")
            return f"Ошибка AI: {str(e)}"

    def _format_messages(self, messages, limit=10, max_length=200):
        """Форматирование сообщений для промпта"""
        formatted = []
        for i, msg in enumerate(messages[:limit], 1):
            text = msg['text'][:max_length] + "..." if len(msg['text']) > max_length else msg['text']
            formatted.append(f"{i}. {text}")
        return "\n".join(formatted)

    def _clean_markdown(self, text):
        """Очищает Markdown разметку для plain text"""
        import re

        # Удаляем Markdown заголовки (###, ##, #)
        text = re.sub(r'^#+\s*', '', text, flags=re.MULTILINE)

        # Удаляем жирный текст (**текст** или __текст__)
        text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
        text = re.sub(r'__(.*?)__', r'\1', text)

        # Удаляем курсив (*текст* или _текст_)
        text = re.sub(r'\*(.*?)\*', r'\1', text)
        text = re.sub(r'_(.*?)_', r'\1', text)

        # Удаляем списки с маркерами
        text = re.sub(r'^[\*\-]\s*', '', text, flags=re.MULTILINE)
        text = re.sub(r'^\d+\.\s*', '', text, flags=re.MULTILINE)

        # Удаляем лишние пустые строки
        text = re.sub(r'\n{3,}', '\n\n', text)

        return text.strip()