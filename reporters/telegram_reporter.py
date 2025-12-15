# reporters/telegram_reporter.py
import requests
from datetime import datetime


class TelegramReporter:
    def __init__(self, token, chat_id):
        self.token = token
        self.chat_id = chat_id

    def send(self, text, max_length=4096):
        """Отправка сообщения в Telegram"""
        if len(text) > max_length:
            text = text[:max_length - 6] + "..."

        url = f"https://api.telegram.org/bot{self.token}/sendMessage"
        data = {
            "chat_id": self.chat_id,
            "text": text,
        }

        print(f"📤 Отправляем в Telegram ({len(text)} символов)")

        try:
            response = requests.post(url, json=data, timeout=10)
            result = response.json()

            if result.get('ok'):
                print(f"✅ Сообщение отправлено (id: {result['result']['message_id']})")
            else:
                print(f"❌ Ошибка Telegram API: {result.get('description')}")

            return result

        except Exception as e:
            print(f"❌ Ошибка отправки: {e}")
            return {"ok": False, "error": str(e)}

    def send_report(self, channel, analysis, analyzer_type):
        """Форматирование и отправка отчета"""
        analyzer_names = {
            'simple': 'Базовый',
            'historical': 'Исторический',
            'rag': 'RAG с контекстом'
        }

        report = f"""
📊 {analyzer_names.get(analyzer_type, 'AI')} анализ канала: {channel}

{analysis}

────────────────
🤖 Анализатор: {analyzer_names.get(analyzer_type, analyzer_type)}
📅 Дата: {datetime.now().strftime('%d.%m.%Y %H:%M')}
"""

        return self.send(report)