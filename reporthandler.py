import json
from pathlib import Path
from model import Lottery


def print_readable_report(lottery: Lottery):
    print('Template: {}'.format(lottery.name))
    print('Winners:')
    for winner, prize in lottery.winners:
        print('{} {}, {}'.format(winner.first_name, winner.last_name,
                                 prize.name))


def write_json_report(lottery, output):
    winner_list = [{'participant': winner, 'prize': prize}
                   for (winner, prize) in lottery.winners]
    report = {'template_name': lottery.name,
              'winners': winner_list}
    with Path(output).open('w') as f:
        json.dump(report, f)
