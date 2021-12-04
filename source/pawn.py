import source.field


class Pawn:

    def __init__(self, currentField: "source.field.Field" = None) -> None:
        self._currentField = currentField

    def current_field(self):
        return self._currentField

    def set_current_field(self, field: "source.field.Field"):
        self._currentField = field
