import argparse
import sys
import traceback
from config import Config
from core.coordinator import AICoordinator

def main():
    parser = argparse.ArgumentParser(description='Telegram AI Analyzer')
    parser.add_argument('--channel', default='spydell_finance', help='Telegram channel')
    parser.add_argument('--analyzer', choices=['simple', 'historical', 'rag'],
                        default='rag', help='Analyzer type')
    parser.add_argument('--user-profile', type=str, help='Путь к файлу с профилем пользователя (текст)')
    parser.add_argument('--profile-text', type=str, help='Текст профиля пользователя напрямую')

    args = parser.parse_args()

    try:
        if args.user_profile:
            with open(args.user_profile, 'r', encoding='utf-8') as f:
                user_context = f.read().strip()
        elif args.profile_text is not None:
            user_context = args.profile_text.strip()
        else:
            user_context = ("Гражданин РФ, живу в Сыктывкаре, 33 года. Есть накопления 800 тысяч на вкладе, 6000$."
                            " Моя цель - сохранить капитал, в условиях России где нет доступа к мировым рынкам финансов.")

        if not user_context:
            print('⚠️ Профиль пользователя пуст. Использую профиль по умолчанию.')
            user_context = ("Гражданин РФ, живу в Сыктывкаре, 33 года. Есть накопления 800 тысяч на вкладе, 6000$."
                            " Моя цель - сохранить капитал, в условиях России где нет доступа к мировым рынкам финансов.")

        print(f"🚀 Telegram AI Platform запущен")
        print(f"📊 Канал: {args.channel}")
        print(f"🤖 Анализатор: {args.analyzer}")

        config = Config()
        coordinator = AICoordinator(config)

        success, result = coordinator.run_analysis(args.channel, args.analyzer, user_context)

        if success:
            print("✅ Анализ успешно завершен")
            if result is not None:
                print(result)
            sys.exit(0)
        else:
            print(f"❌ Ошибка: {result}")
            sys.exit(1)

    except KeyboardInterrupt:
        print("\n⛔ Операция прервана пользователем")
        sys.exit(130)
    except Exception:
        print("💥 Критическая ошибка:")
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()