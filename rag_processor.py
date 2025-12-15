# rag_processor.py
import re
from datetime import datetime


class RAGProcessor:
    def __init__(self, storage):
        """
        Инициализация RAG процессора
        :param storage: экземпляр JSONStorage
        """
        self.storage = storage

    def simple_search(self, query, messages, top_k=5):
        """Простой поиск по ключевым словам"""
        query_words = set(re.findall(r'\w+', query.lower()))

        scored_messages = []
        for msg in messages:
            text = msg['text'].lower()
            text_words = set(re.findall(r'\w+', text))

            # Простой скоринг: количество совпадающих слов
            score = len(query_words.intersection(text_words))
            if score > 0:
                scored_messages.append((score, msg))

        # Сортируем по релевантности
        scored_messages.sort(key=lambda x: x[0], reverse=True)

        return [msg for _, msg in scored_messages[:top_k]]

    def get_channel_context(self, channel, query, message_limit=100):
        """Получение контекста по каналу и запросу"""
        # Получаем сообщения из хранилища
        messages = self.storage.get_recent_messages(channel, message_limit)

        # Ищем релевантные
        relevant = self.simple_search(query, messages)

        # Форматируем контекст
        context_parts = []
        for i, msg in enumerate(relevant, 1):
            context_parts.append(f"{i}. {msg['text'][:200]}...")

        return "\n".join(context_parts) if context_parts else "Нет релевантных сообщений"

    def build_rag_prompt(self, channel, query, context, analysis_type="qa"):
        """Построение промпта для RAG"""

        templates = {
            "qa": f"""
            На основе сообщений из канала {channel} ответь на вопрос.

            Релевантные сообщения:
            {context}

            Вопрос: {query}

            Ответь максимально информативно, цитируй конкретные сообщения если нужно.
            """,

            "analysis": f"""
            Проанализируй тему на основе сообщений из канала {channel}.

            Релевантные сообщения по теме "{query}":
            {context}

            Сделай анализ: тренды, мнения, важные факты.
            """,

            "summary": f"""
            Суммаризируй информацию по теме из канала {channel}.

            Сообщения по теме:
            {context}

            Сделай краткую выжимку основных точек зрения и фактов.
            """
        }

        return templates.get(analysis_type, templates["qa"])

    def process_query(self, channel, query, analysis_type="qa", ai_caller=None):
        """
        Основной метод обработки запроса
        :param ai_caller: функция для вызова AI (из основного класса)
        """
        # Получаем контекст
        context = self.get_channel_context(channel, query)

        # Строим промпт
        prompt = self.build_rag_prompt(channel, query, context, analysis_type)

        # Вызываем AI (через переданную функцию)
        if ai_caller:
            return ai_caller(prompt)
        else:
            return prompt  # Возвращаем промпт если нет AI