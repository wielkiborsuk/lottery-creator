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

    def test_prize_amounts_assign_multiple_prizes(self):
        prizes = self._generate_prizes(3, lambda x: 2*x+1)
        participants = self._generate_participants(10)

        lottery = Lottery(self.name, prizes)
        lottery.draw(participants)

        winners = [winner for (winner, prize) in lottery.winners]
        assert len(winners) == 9

        assert not all([participant in winners
                        for participant in participants])

        drawn_prizes = [prize for (winner, prize) in lottery.winners]
        assert prizes[0] in drawn_prizes

        for prize in prizes:
            matching_prizes = filter(lambda p: p.id == prize.id, drawn_prizes)
            assert prize.amount == len(list(matching_prizes))

    def test_too_many_prizes(self):
        prizes = self._generate_prizes(13)
        participants = self._generate_participants(4)

        lottery = Lottery(self.name, prizes)
        lottery.draw(participants)

        winners = [winner for (winner, prize) in lottery.winners]
        assert len(winners) == 4

        assert all([participant in winners
                    for participant in participants])

        drawn_prizes = [prize for (winner, prize) in lottery.winners]
        assert prizes[:4] == drawn_prizes

    def _generate_prizes(self, count, amount_lambda=lambda x: 1):
        return [Prize(c+1, f'prize{c+1}', amount_lambda(c))
                for c in range(count)]

    def _generate_participants(self, count, weight_lambda=lambda x: 1):
        return [Participant(c+1, f'name{c+1}', f'surname{c+1}',
                            weight_lambda(c))
                for c in range(count)]
