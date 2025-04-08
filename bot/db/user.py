from .base import ExcelDB

class User(ExcelDB):
    def __init__(
        self,
        path: str
    ) -> None:
        sheet_name = "users"
        id_column = "id"
        headers = [
                "firstSurName",
                "birthYear",
                "gender",
                "ageCategory",
                "ratingFIDE",
                "classRank",
                "innPin",
                "criteria",
                "status",
            ]
        super().__init__(path, sheet_name, id_column, headers)