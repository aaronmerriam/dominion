from random import shuffle
from itertools import chain
from functools import partial

from .actions import bonus_cards, bonus_treasure, bonus_buys, bonus_actions


class BaseCard(object):
    is_attack = False
    is_action = False
    is_treasure = False
    is_victory = False
    bonus_actions = 0
    bonus_buys = 0
    bonus_cards = 0
    bonus_treasure = 0
    treasure_value = 0
    victory_points = 0
    events = None

    def __init__(self):
        if self.events is None:
            events = []
            events.append(self.bonus_actions and partial(bonus_actions, self.bonus_actions))
            events.append(self.bonus_buys and partial(bonus_buys, self.bonus_buys))
            events.append(self.bonus_cards and partial(bonus_cards, self.bonus_cards))
            events.append(self.bonus_treasure and partial(bonus_treasure, self.bonus_treasure))
            events = filter(bool, events)
            self.events = events

    def __unicode__(self):
        return self.__class__.__name__

    def get_victory_points(self, deck):
        return self.victory_points

    def get_treasure_value(self):
        return self.treasure_value

    def get_events(self):
        return self.events


class Action(BaseCard):
    is_action = True


class Market(Action):
    cost = 5
    treasure_value = 1
    bonus_cards = 1
    bonus_actions = 1
    bonus_buys = 1


class Treasure(BaseCard):
    is_treasure = True


class Copper(Treasure):
    cost = 0
    treasure_value = 1


class Silver(Treasure):
    cost = 3
    treasure_value = 2


class Gold(Treasure):
    cost = 6
    treasure_value = 3


class Victory(BaseCard):
    is_victory = True


class Estate(Victory):
    cost = 2
    victory_points = 1


class Duchy(Victory):
    cost = 5
    victory_points = 2


class Province(Victory):
    cost = 8
    victory_points = 3


class CardCollection(object):
    def __init__(self, *cards):
        self.cards = list(cards)

    def __nonzero__(self):
        return bool(self.cards)

    def __contains__(self, card):
        return card in self.cards

    def __iter__(self):
        return iter(self.cards)

    def __len__(self):
        return len(self.cards)

    def __add__(self, other):
        return CardCollection(*chain(self.cards, other.cards))

    def __getitem__(self, index):
        return self.cards[0]

    def get_treasure_value(self):
        return sum(card.get_treasure_value() for card in self)

    def draw_card(self):
        try:
            return self.cards.pop()
        except IndexError:
            raise IndexError('Cannot deal from an empty deck')

    def add_cards(self, *cards):
        self.cards.extend(cards)

    def shuffle(self):
        shuffle(self.cards)
