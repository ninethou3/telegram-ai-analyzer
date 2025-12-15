# json_storage.py
import json
import os
from datetime import datetime
import hashlib

class JSONStorage:
    def __init__(self, filename="telegram_data.json"):
        self.filename = filename
        self.data = self._load_data()

    def _load_data(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, Exception):
                # Если файл поврежден, создаем заново
                return {
                    "messages": [],
                    "analysis_history": []
                }
        else:
            return {
                "messages": [],
                "analysis_history": []
            }

    def _save_data(self):
        # Сохраняем аккуратно с обработкой ошибок
        try:
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Ошибка сохранения в {self.filename}: {e}")

    def save_message(self, channel, text, original_date=None):
        message_hash = hashlib.md5(f"{channel}:{text}".encode()).hexdigest()

        existing = [msg for msg in self.data["messages"]
                    if msg.get("hash") == message_hash]

        if not existing:
            self.data["messages"].append({
                "channel": channel,
                "text": text,
                "hash": message_hash,
                "original_date": original_date or datetime.now().isoformat(),
                "saved_at": datetime.now().isoformat()
            })
            self._save_data()

    def save_analysis(self, channel, analysis_text, message_count):
        self.data["analysis_history"].append({
            "channel": channel,
            "analysis": analysis_text,
            "message_count": message_count,
            "created_at": datetime.now().isoformat()
        })
        self._save_data()

    def get_recent_messages(self, channel, limit=10):
        channel_messages = [
            msg for msg in self.data["messages"]
            if msg["channel"] == channel
        ]
        channel_messages.sort(key=lambda x: x["saved_at"], reverse=True)
        return channel_messages[:limit]

    def get_analysis_history(self, channel, limit=5):
        channel_analysis = [
            analysis for analysis in self.data["analysis_history"]
            if analysis["channel"] == channel
        ]
        channel_analysis.sort(key=lambda x: x["created_at"], reverse=True)
        return channel_analysis[:limit]