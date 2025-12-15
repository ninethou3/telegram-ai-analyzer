from collectors.telegram_collector import TelegramCollector
from reporters.telegram_reporter import TelegramReporter
from analyzers import SimpleAnalyzer, HistoricalAnalyzer, RagAnalyzer


class AICoordinator:
    def __init__(self, config):
        self.config = config
        self.storage = config.storage
        self.rag = config.rag

        # Инициализация компонентов
        self.collector = TelegramCollector(self.storage)
        self.reporter = TelegramReporter(config.token, config.chat_id)
        self.analyzers = self._init_analyzers()

    def _init_analyzers(self):
        """Инициализация анализаторов"""
        return {
            'simple': SimpleAnalyzer(
                api_key=self.config.deepseek_api_key,
                base_url=self.config.deepseek_base_url
            ),
            'historical': HistoricalAnalyzer(
                api_key=self.config.deepseek_api_key,
                base_url=self.config.deepseek_base_url
            ),
            'rag': RagAnalyzer(
                api_key=self.config.deepseek_api_key,
                base_url=self.config.deepseek_base_url,
                rag_processor=self.rag
            )
        }

    def run_analysis(self, channel, analyzer_type='rag', user_context=""):
        """Основной пайплайн анализа"""
        print(f"🚀 Запускаем {analyzer_type} анализ канала {channel}")

        # 1. Сбор
        messages = self.collector.collect(channel)
        if not messages:
            return False, "❌ Не удалось собрать сообщения"

        # 2. Анализ
        analyzer = self.analyzers.get(analyzer_type)
        if not analyzer:
            return False, f"❌ Анализатор '{analyzer_type}' не найден"

        print(f"🤖 Используем {analyzer_type} анализатор")

        try:
            if analyzer_type == 'historical':
                analysis = analyzer.analyze(messages, channel, self.storage)
            elif analyzer_type == 'rag':
                print(f"Передаем user_context в RAG анализатор")
                # Только для RAG передаем user_context
                analysis = analyzer.analyze(messages, channel, user_context)
            else:
                # Для simple и других
                analysis = analyzer.analyze(messages, channel)
        except Exception as e:
            return False, f"❌ Ошибка анализа: {e}"

        # 3. Сохранение
        self.storage.save_analysis(channel, analysis, len(messages))

        # 4. Отправка
        result = self.reporter.send_report(channel, analysis, analyzer_type)

        return result.get('ok', False), analysis