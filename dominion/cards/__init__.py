from .base import (  # NOQA
    CardCollection, BaseCard, Action, Treasure, Victory,
    pop_treasures, pop_matching_cards, pop_actions
)

from .core import (  # NOQA
    Copper, Silver, Gold, Estate, Duchy, Province,
    Market, Militia, Village, Envoy, Moat, Woodcutter, Workshop,
    Bureaucrat, Gardens, Smithy, Festival, Laboratory,
)


TREASURE_CARDS = (Copper, Silver, Gold)
VICTORY_CARDS = (Estate, Duchy, Province)
BASE_SUPPLY_CARDS = dict(
    zip(TREASURE_CARDS, (60, 40, 25)) + zip(VICTORY_CARDS, (30, 18, 12))
)
CORE_ACTION_CARDS = (
    Market, Village, Militia, Envoy, Moat, Woodcutter, Workshop,
    Bureaucrat, Gardens, Smithy, Festival, Laboratory,
)
