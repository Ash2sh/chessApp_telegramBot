from aiogram.utils.keyboard import (
    InlineKeyboardBuilder,
    InlineKeyboardMarkup,
    ReplyKeyboardBuilder,
    ReplyKeyboardMarkup,
)


class InlineKeyboard:
    def __init__(self, buttons: list[dict], btnRows: list[int] = [3]) -> None:
        self.btnRows = btnRows

        self.builder = InlineKeyboardBuilder()
        [self.builder.button(**button) for button in buttons]
        self.builder.adjust(*self.btnRows, repeat=True)

    def markup(self) -> InlineKeyboardMarkup:
        return self.builder.as_markup()


class ReplyKeyboard:
    def __init__(self, buttons: list[dict], btnRows: list[int] = [3]) -> None:
        self.btnRows = btnRows

        self.builder = ReplyKeyboardBuilder()
        [self.builder.button(**button) for button in buttons]
        self.builder.adjust(*self.btnRows, repeat=True)

    def markup(self) -> ReplyKeyboardMarkup:
        return self.builder.as_markup()
