class WinCondition(Exception):
    pass


class ProvincesDepleted(WinCondition):
    pass


class ActionsDepleted(WinCondition):
    pass


class EmptyDeck(Exception):
    pass
