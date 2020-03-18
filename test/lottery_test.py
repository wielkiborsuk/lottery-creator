from model import Prize, Participant, Lottery


class TestLottery:
    name = 'test_lottery'

    def test_draw_all_prizes(self):
        prizes = self._generate_prizes(3)
        participants = self._generate_participants(5)

        lottery = Lottery(self.name, prizes)
        lottery.draw(participants)

        drawn_prizes = [prize for (winner, prize) in lottery.winners]
        for prize in prizes:
            assert prize in drawn_prizes

    def test_draw_all_participants(self):
        # with enough prizes every participant will get drawn
        prizes = self._generate_prizes(10)
        participants = self._generate_participants(10)

        lottery = Lottery(self.name, prizes)
        lottery.draw(participants)

        winners = [winner for (winner, prize) in lottery.winners]
        assert all([participant in winners
                    for participant in participants])

    def _generate_prizes(self, count):
        return [Prize(c+1, f'prize{c+1}', 1)
                for c in range(count)]

    def _generate_participants(self, count):
        return [Participant(c+1, f'name{c+1}', f'surname{c+1}', 1)
                for c in range(count)]
