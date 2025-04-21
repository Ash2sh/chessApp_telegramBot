from aiogram import Bot, F, Router
from aiogram.filters import BaseFilter, Command
from aiogram.types import CallbackQuery, Message, FSInputFile

from bot.config import logger, dataPath
from bot.middlewares.broadcaster import Notify
from bot.utils.keyboard import InlineKeyboard
from bot.utils.tournament import Tournament, TournamentFactory, TournamentParams


TOURNAMENT_PARAMS = TournamentParams(
    name="Kyrgyzstan Arena",
    clockTime=3,
    clockIncrement=0,
    minutes=70,
    waitMinutes=5,
    variant="standard",
    rated=True,
    berserkable=True,
    streakable=True,
    description="Ежедневный онлайн турнир по блицу для всех желающих",
)


class IsAdmin(BaseFilter):
    async def __call__(self, message: Message, bot: Bot) -> bool:
        # Для личных сообщений всегда разрешаем
        if message.chat.type == "private":
            return True

        # Для групп/супергрупп проверяем админство
        member = await bot.get_chat_member(message.chat.id, message.from_user.id)
        return member.status in ("administrator", "creator")


async def get_apps_handler(message: Message) -> None:
    file = FSInputFile(f"{dataPath}/users.xlsx")
    print(file)
    await message.answer_document(file)


async def top_players_handler(message: Message) -> None:
    logger.info(f"Вызван хендлер /top_players от пользователя {message.from_user.id}")
    try:
        message_text = "Выберите топ:\n"
        categories = [
            (
                "ТОП 20 по стандарту среди мужчин",
                "https://ratings.fide.com/rankings.phtml?country=KGZ&gender=M",
            ),
            (
                "ТОП 20 по рапиду среди мужчин",
                "https://ratings.fide.com/rankings.phtml?continent=0&country=KGZ&rating=rapid&gender=M&age1=0&age2=0",
            ),
            (
                "ТОП 20 по блицу среди мужчин",
                "https://ratings.fide.com/rankings.phtml?continent=0&country=KGZ&rating=blitz&gender=M&age1=0&age2=0",
            ),
            (
                "ТОП 20 по стандарту среди женщин",
                "https://ratings.fide.com/rankings.phtml?country=KGZ&gender=F",
            ),
            (
                "ТОП 20 по рапиду среди женщин",
                "https://ratings.fide.com/rankings.phtml?continent=0&country=KGZ&rating=rapid&gender=F&age1=0&age2=0",
            ),
            (
                "ТОП 20 по блицу среди женщин",
                "https://ratings.fide.com/rankings.phtml?continent=0&country=KGZ&rating=blitz&gender=F&age1=0&age2=0",
            ),
            (
                "ТОП 20 по стандарту среди юниоров до 20 лет",
                "https://ratings.fide.com/rankings.phtml?continent=0&country=KGZ&rating=standard&gender=M&age1=0&age2=20",
            ),
        ]
        for category, url in categories:
            message_text += f"[{category}]({url})\n"
        await message.answer(message_text, parse_mode="Markdown")
        logger.info("Список топов успешно отправлен")
    except Exception as e:
        logger.exception(f"Ошибка в top_players_handler: {e}")


async def create_tournament_handler(
    message: Message, notify: Notify, tour: TournamentFactory
) -> None:
    logger.info(f"Вызван /create_tournament от пользователя {message.from_user.id}")
    try:
        tournament: Tournament = await tour.create(TOURNAMENT_PARAMS)
        result: str = tournament.message()
        await message.answer(result, parse_mode="HTML")
        await notify.tournament(tournament)
        logger.info(f"Турнир создан и сообщение отправлено: ID {tournament.get_id()}")
    except Exception as e:
        logger.exception(f"Ошибка в create_tournament_handler: {e}")
        await message.answer("Произошла ошибка при создании турнира.")


async def stop_tournament_handler(message: Message, tour: TournamentFactory) -> None:
    logger.info(f"Вызван запрос на остановку турнира от {message.from_user.id}")
    try:
        tours = []
        for i in await tour.get_tours():
            name = i.data["fullName"]
            tourId = i.get_id()
            callData = f"tourId_{tourId}"
            tours.append({"text": f"{tourId} | {name}", "callback_data": callData})
        if tours:
            buttons = InlineKeyboard(tours)
            await message.answer(
                "Выберите турнир, который нужно завершить:", reply_markup=buttons.markup()
            )
            logger.info("Пользователю отправлен список турниров на завершение")
        else:
            await message.answer("Нет активных турниров")
    except Exception as e:
        logger.exception(f"Ошибка в stop_tournament_handler: {e}")
        await message.answer("Произошла ошибка при получении турниров.")


async def tournament_id_received_handler(
    call: CallbackQuery, tour: TournamentFactory
) -> None:
    logger.info(f"Пользователь {call.from_user.id} выбрал турнир: {call.data}")
    try:
        tourId = call.data.split("_")[1]
        result = await tour.terminate(tourId)
        if result:
            await call.message.answer(f"Турнир завершен! id: {tourId}")
            logger.info(f"Турнир {tourId} успешно завершён")
        else:
            await call.message.answer(f"Не удалось завершить турнир {tourId}")
            logger.warning(f"Не удалось завершить турнир {tourId}")
        await call.answer()
    except Exception as e:
        logger.exception(f"Ошибка в tournament_id_received_handler: {e}")
        await call.message.answer("Произошла ошибка при завершении турнира.")


def reg_handler(router: Router) -> None:
    router.message.register(get_apps_handler, Command(commands=["get_apps"]), IsAdmin())
    router.message.register(
        top_players_handler, Command(commands=["top_players"]), IsAdmin()
    )
    router.message.register(
        create_tournament_handler, Command(commands=["create_tournament"]), IsAdmin()
    )
    router.callback_query.register(
        tournament_id_received_handler, F.data.startswith("tourId")
    )
    router.message.register(
        stop_tournament_handler, Command(commands=["stop_tournament"]), IsAdmin()
    )
