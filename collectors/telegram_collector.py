import requests
import re
from datetime import datetime


class TelegramCollector:
    def __init__(self, storage, max_messages=10, min_length=20):
        self.storage = storage
        self.max_messages = max_messages
        self.min_length = min_length

    def collect(self, channel_username):
        """Сбор сообщений из канала"""
        url = f"https://t.me/s/{channel_username}"

        try:
            response = requests.get(url)
            if response.status_code == 200:
                messages = re.findall(r'tgme_widget_message_text.*?>(.*?)</div>', response.text)

                clean_messages = []
                for msg in messages[:self.max_messages]:
                    clean_msg = re.sub('<[^<]+?>', '', msg).strip()
                    if clean_msg and len(clean_msg) > self.min_length:
                        # Сохраняем в хранилище
                        self.storage.save_message(channel_username, clean_msg)
                        clean_messages.append({
                            'date': datetime.now().isoformat(),
                            'text': clean_msg
                        })

                print(f"📥 Собрано {len(clean_messages)} сообщений из {channel_username}")
                return clean_messages

        except Exception as e:
            print(f"❌ Ошибка сбора: {e}")

        return []