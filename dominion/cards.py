from random import shuffle
from itertools import chain


class BaseCard(object):
    is_attack = False
    is_action = False
    is_treasure = False
    is_victory = False
    extra_actions = 0
    extra_buys = 0
    extra_cards = 0
    extra_money = 0
    victory_points = 0

    def __unicode__(self):
        return self.__class__.__name__

    def get_victory_points(self, deck):
        return self.victory_points

    def get_treasure_value(self):
        return self.extra_money


class Treasure(BaseCard):
    is_treasure = True


class Copper(Treasure):
    cost = 0
    extra_money = 1


class Silver(Treasure):
    cost = 3
    extra_money = 2


class Gold(Treasure):
    cost = 6
    extra_money = 3


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
