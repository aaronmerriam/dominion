from random import shuffle
from functools import partial
from itertools import chain


class BaseCard(object):
    is_attack = False
    is_action = False
    is_reaction = False
    is_treasure = False
    is_victory = False
    treasure_value = 0
    victory_points = 0
    events = []

    def __hash__(self):
        return hash(self.short_name)

    def __cmp__(self, other):
        if self.__class__ == other.__class__:
            return 0
        else:
            return 1

    def __unicode__(self):
        return self.__class__.__name__

    def __repr__(self):
        return unicode(self)

    def total_victory_point_value(self, deck):
        return self.victory_points

    def execute_events(self, **kwargs):
        for event in self.events:
            if isinstance(event, basestring):
                getattr(self, event)(**kwargs)
            else:
                event(**kwargs)


class Action(BaseCard):
    is_action = True


class Attack(BaseCard):
    is_action = True


class Reaction(BaseCard):
    is_reaction = True


class Treasure(BaseCard):
    is_treasure = True


class Victory(BaseCard):
    is_victory = True


class CardCollection(object):
    def __init__(self, cards=[]):
        self.cards = list(cards)
        self.validate_cards(*self.cards)

    def __nonzero__(self):
        return bool(self.cards)

    def __contains__(self, card):
        if isinstance(card, BaseCard):
            return card in self.cards
        elif issubclass(card, BaseCard):
            return any(isinstance(c, card) for c in self.cards)
        else:
            raise TypeError('Unkown object passed in as card')

    def __iter__(self):
        return iter(self.cards)

    def __len__(self):
        return len(self.cards)

    def __add__(self, other):
        return CardCollection(chain(self.cards, other.cards))

    def __getitem__(self, index):
        return self.cards[index]

    def total_treasure_value(self):
        return sum(card.treasure_value for card in self)

    def index_of_card(self, card):
        if isinstance(card, BaseCard):
            return self.cards.indexof(card)
        elif issubclass(card, BaseCard):
            for i in xrange(len(self)):
                if isinstance(self[i], card):
                    return i
            raise IndexError
        else:
            raise TypeError('Unknown object passed in as card')

    def pop_card(self, index):
        return self.cards.pop(index)

    def draw_card(self):
        try:
            return self.cards.pop()
        except IndexError:
            raise IndexError('Cannot deal from an empty deck')

    def validate_cards(self, *cards):
        assert all(isinstance(card, BaseCard) for card in cards), 'Attempt to add a non card instance to collection'

    def add_cards(self, *cards):
        self.validate_cards(*cards)
        self.cards.extend(cards)

    def shuffle(self):
        shuffle(self.cards)


def pop_matching_cards(key, cards):
    treasures = CardCollection()
    to_pop = None
    while True:
        for i in xrange(len(cards)):
            if key(cards[i]):
                to_pop = i
                break
        if to_pop is not None:
            treasures.add_cards(cards.pop_card(to_pop))
            to_pop = None
            continue
        break
    return treasures

pop_treasures = partial(pop_matching_cards, lambda c: c.is_treasure)
pop_actions = partial(pop_matching_cards, lambda c: c.is_action)
pop_points = partial(pop_matching_cards, lambda c: c.is_victory)
