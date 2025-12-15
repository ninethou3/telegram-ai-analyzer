import argparse
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
    if args.user_profile:
        with open(args.user_profile, 'r', encoding='utf-8') as f:
            user_context = f.read()
    elif args.profile_text:
        user_context = args.profile_text
    else:
        user_context = "Гражданин РФ, живу в Сыктывкаре, 33 года"

    print(f"🚀 Telegram AI Platform запущен")
    print(f"📊 Канал: {args.channel}")
    print(f"🤖 Анализатор: {args.analyzer}")

    try:
        config = Config()
        coordinator = AICoordinator(config)

        success, result = coordinator.run_analysis(args.channel, args.analyzer, user_context)

        if success:
            print("✅ Анализ успешно завершен")
        else:
            print(f"❌ Ошибка: {result}")

    except Exception as e:
        print(f"💥 Критическая ошибка: {e}")


if __name__ == "__main__":
    main()