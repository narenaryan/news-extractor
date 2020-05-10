import enum

class Topics(enum.Enum):
    top = enum.auto()
    business = enum.auto()
    health = enum.auto()
    entertainment = enum.auto()

class Countries(enum.Enum):
    AU = "australia"
    CA = "canada"
    NZ = "newzealand"
    GB = "uk"
    US = "usa"
