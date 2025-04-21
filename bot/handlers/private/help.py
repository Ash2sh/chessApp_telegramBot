from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from bot.config import logger

async def help(message: Message) -> None:
    help_text = (
        "\U0001F44B <b>Привет!</b> Этот бот создан, чтобы <b>автоматически организовывать турниры</b>! \U0001F3C6\U0001F389\n\n"
        "\U0001F538 <b>Вот список команд, которые могут тебе пригодиться:</b>\n\n"

        "\U0001F4CD <b>Основные команды:</b>\n"
        "\u2699 /help – Показать справку по боту\n"
        "\U0001F3C5 /top_players – Показать топ игроков\n"

        "\U0001F4CE <b>Управление турнирами:</b>\n"
        "\U0001F3AE /create_tournament – Создать новый турнир вручную\n"
        "\u26D4 /stop_tournament – Завершить турнир немедленно\n\n"

        "\U0001F3C1 <b>Технические команды:</b>\n"
        "\U0001F4BB /get_apps – получить все заявки(для админов)\n\n"

        "\U0001F680 <i>Удачи в турнирах! Пусть победит сильнейший!</i> \U0001F947"
    )
    await message.answer(help_text, parse_mode='HTML')

def reg_handler(router: Router) -> None:
    router.message.register(help, Command(commands=["help"]))

    logger.debug("help handler registered")