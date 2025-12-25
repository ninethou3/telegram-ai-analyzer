# analyzers/rag_analyzer.py
import traceback

from .base_analyzer import BaseAnalyzer


class RagAnalyzer(BaseAnalyzer):
    def __init__(self, api_key, base_url, rag_processor, model="deepseek-chat"):
        super().__init__(api_key, base_url, model)
        self.rag_processor = rag_processor

    def analyze(self, messages, channel, user_context="", storage=None):
        """Анализ с автоматическим RAG"""
        print(
            f"📌 RagAnalyzer.analyze вызван с user_context: {user_context[:30]}..." if user_context else "user_context пустой")

        try:
            # 1. Выявляем ключевые темы
            topics_prompt = f"""
Выдели 3-5 ключевых тем из этих сообщений:

{" ".join([m['text'][:150] for m in messages[:5]])}

Верни только темы через запятую.
"""

            topics_text = self._call_ai(topics_prompt)
            topics = [t.strip() for t in topics_text.split(',')[:3]]

            print(f"📌 RagAnalyzer: выявлены темы: {', '.join(topics)}")

            # 2. Для каждой темы ищем исторический контекст
            all_contexts = []
            for topic in topics:
                context = self.rag_processor.get_channel_context(channel, topic, 20)
                if context and "Нет релевантных" not in context:
                    all_contexts.append(f"Тема: {topic}\n{context}")

            # 3. Собираем финальный промпт
            historical_summary = "\n\n".join(all_contexts) if all_contexts else "Нет исторического контекста"

            user_section = f"""
                            ИНФОРМАЦИЯ О ПОЛЬЗОВАТЕЛЕ (адаптируй ответ под него):
                            {user_context}
                            """ if user_context else ""

            final_prompt = f"""
                ТЫ — ПРОФЕССИОНАЛЬНЫЙ ФИНАНСОВЫЙ АНАЛИТИК. Твоя задача — проанализировать данные из канала {channel}.
                Используй ТОЛЬКО предоставленную ниже информацию.

                {user_section}

                КЛЮЧЕВЫЕ ТЕМЫ СЕГОДНЯ:
                {', '.join(topics)}

                ИСТОРИЧЕСКИЙ КОНТЕКТ (для сравнения):
                {historical_summary}

                НОВЫЕ СООБЩЕНИЯ (текущая ситуация):
                {" ".join([m['text'] for m in messages[:3]])}

                ЗАДАНИЕ:
                1. Проведи сравнительный анализ: что изменилось в темах по сравнению с историей?
                2. Если есть ПРОФИЛЬ ПОЛЬЗОВАТЕЛЯ, дай конкретные рекомендации.
                3. Пиши кратко, по делу, без общих фраз.

                ОТВЕТ НА РУССКОМ ЯЗЫКЕ:
                """

            result = self._call_ai(final_prompt)

            # Очищаем Markdown
            clean_result = self._clean_markdown(result)

            return clean_result

        except Exception as e:
            print(f"❌ Ошибка в RagAnalyzer.analyze: {e}")
            print(f"❌ Traceback: {traceback.format_exc()}")  # ← ДОБАВЬ ИМПОРТ traceback
            return f"❌ Ошибка RAG анализа: {str(e)}"