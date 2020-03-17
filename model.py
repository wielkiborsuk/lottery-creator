from collections import namedtuple
from random import choices


Participant = namedtuple('Participant',
                         ['id', 'first_name', 'last_name', 'weight'])
Participant.__new__.__defaults__ = (None, None, None, 1)

Prize = namedtuple('Prize', ['id', 'name', 'amount'])


class Lottery(object):
    def __init__(self, name, prizes):
        self.name = name
        self.prizes = prizes

    def draw(self, participants):
        participants = participants[:]
        flat_prize_list = self.__prepare_prizes()
        self.winners = []
        while participants and flat_prize_list:
            weights = [float(p.weight) for p in participants]
            winner = choices(participants, weights=weights)[0]
            self.winners.append((winner, flat_prize_list.pop(0)))
            participants.remove(winner)

    def __prepare_prizes(self):
        flat_prize_list = []
        for p in self.prizes:
            for i in range(p.amount):
                flat_prize_list.append(p._replace(amount=1))
        return flat_prize_list
