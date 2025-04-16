import json
from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Optional

from aiohttp import ClientSession

from bot.config import logger, timezone, username


@dataclass
class TournamentParams:
    name: str
    clockTime: int  # минуты на партию
    clockIncrement: int  # добавка за ход
    minutes: int  # длительность турнира
    startDate: Optional[int] = None  # timestamp в миллисекундах
    waitMinutes: Optional[int] = None  # сколько минут подождать до старта
    variant: str = "standard"  # "standard" "chess960" "crazyhouse" "antichess" etc.
    rated: bool = True  # рейтинг или нет
    berserkable: bool = True  # можно ли использовать берсерк
    streakable: bool = True # After 2 wins, consecutive wins grant 4 points instead of 2.
    description: Optional[str] = None  # описание турнира
    password: Optional[str] = None  # пароль для входа
    conditions_team: Optional[str] = None  # ID команды, если турнир только для команды
    conditions_minRating: Optional[int] = None  # минимальный рейтинг
    conditions_maxRating: Optional[int] = None  # максимальный рейтинг
    conditions_nbRatedGame: Optional[int] = None  # минимальное число сыгранных партий

    def to_dict(self) -> dict:
        return {k: v for k, v in asdict(self).items() if v is not None}


class Tournament:
    def __init__(
        self, session: ClientSession, headers: str, params: TournamentParams | None = None
    ) -> None:
        self.session = session
        self.params = params
        self.headers = headers
        self.data: dict | None = None

    def when(self) -> datetime:
        return datetime.strptime(self.data["startsAt"][:-4], "%Y-%m-%dT%H:%M:%S.%f")

    def get_id(self) -> str:
        return self.data["id"]

    @classmethod
    async def create(cls, api: str, params: TournamentParams) -> "Tournament":
        session = ClientSession()
        headers = {"Authorization": f"Bearer {api}"}
        instance = cls(session, params, headers)
        await instance._create()
        return instance

    async def _create(self) -> None:
        async with self.session.post(
            "https://lichess.org/api/tournament",
            json=self.params.to_dict(),
            headers=self.headers,
        ) as response:
            if response.ok:
                self.data = await response.json()
                logger.info(f"Турнир успешно создан! id турнира: {self.get_id()}")
            else:
                error_data = await response.text()
                logger.error(
                    f"Ошибка при создании турнира: {response.status}, {error_data}"
                )

    async def terminate(self) -> bool:
        if not self.data:
            logger.error("Турнир еще не создан")
            return False

        async with self.session.post(
            f"https://lichess.org/api/tournament/{self.get_id()}/terminate",
            headers=self.headers,
        ) as response:
            if response.ok:
                logger.info(f"Турнир завершен! id: {self.get_id()}")
                return True
            else:
                error_data = await response.text()
                logger.error(f"Ошибка при завершении: {response.status}, {error_data}")
                return False

    def message(self) -> str:
        if not self.data:
            return "Ошибка при создании турнира, попробуйте позже"

        tournament_url = f"https://lichess.org/tournament/{self.get_id()}"
        current_date = datetime.now(timezone).strftime("%d %B")
        return (
            '<b>Ежедневный онлайн турнир по блицу для всех желающих "Kyrgyzstan Arena"</b>\n\n'
            "- <b>Время начала:</b> 21:30\n"
            f"- <b>Формат:</b> {self.params.variant}\n"
            f"- <b>Контроль времени:</b> {self.params.clockTime}+{self.params.clockIncrement}\n"
            f"- <b>Длительность:</b> {self.params.minutes} минут\n\n"
            "<b>Ссылка на вступление в клуб:</b>\n"
            "https://lichess.org/team/kyrgyz-republic\n\n"
            "<b>Ссылки на турниры:</b>\n\n"
            f"- {current_date}:\n{tournament_url}"
        )


class TournamentFactory:
    def __init__(self, api: str) -> None:
        self.session = ClientSession()
        self.headers = {"Authorization": f"Bearer {api}"}
        self._tourList: list[Tournament] = []

    async def create(self, params: TournamentParams) -> Tournament:
        tour = Tournament(self.session, params, self.headers)
        await tour._create()

        self._tourList.append(tour)
        return tour

    async def terminate(self, id: str) -> bool:
        for tour in self._tourList:
            if tour.get_id() == id:
                return await tour.terminate()
        logger.warning("Такого id нет")
        return False

    async def get_tours(self) -> list[Tournament]:
        if not self._tourList:
            async with self.session.get(f"https://lichess.org/api/user/{username}/tournament/created", headers=self.headers) as response:
                async for i in response.content:
                    data = json.loads(i.decode("utf-8"))
                    tour = Tournament(self.session, self.headers)
                    tour.data = data
                    self._tourList.append(tour)
        return self._tourList
