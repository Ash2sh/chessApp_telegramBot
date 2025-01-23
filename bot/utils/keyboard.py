from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup

class InlineKeyboard:
    def __init__(self, buttons: list[dict]) -> None:
        self.builder = InlineKeyboardBuilder()
        for button in buttons:
            self.builder.button(**button)

    def markup(self) -> InlineKeyboardMarkup:
        return self.builder.as_markup()
