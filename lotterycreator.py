import json
import csv
from random import choices
from pathlib import Path
import click


def load_csv_file(name):
    with open(name, 'r') as f:
        return list(csv.DictReader(f))


def load_json_file(name):
    with open(name, 'r') as f:
        participants = json.load(f)
        return participants


def load_participants_info(format, name):
    file_path = Path('../data').joinpath(name)

    if format == 'csv':
        return load_csv_file(file_path)
    elif format == 'json':
        return load_json_file(file_path)
    else:
        return []


def load_lottery_template(name):
    base_path = Path('../data/lottery_templates')

    if name:
        file_path = base_path.joinpath(name)
    else:
        file_path = sorted(base_path.iterdir())[0]

    with open(file_path, 'r') as f:
        return json.load(f)


def prepare_prizes(lottery_template):
    flat_prize_list = []
    for p in lottery_template['prizes']:
        for i in range(p.get('amount', 1)):
            flat_prize_list.append(p)

    return flat_prize_list


def draw(participants, lottery_template):
    participants = participants[:]
    flat_prize_list = prepare_prizes(lottery_template)
    winners = []
    while participants and flat_prize_list:
        weights = [float(p.get('weight', '1')) for p in participants]
        winner = choices(participants, weights=weights)[0]
        winners.append((winner, flat_prize_list.pop(0)))
        participants.remove(winner)
    return winners


def write_json_report(winners, lottery_template, output):
    winner_list = [{'participant': winner, 'prize': prize}
                   for (winner, prize) in winners]
    report = {'template_name': lottery_template['name'],
              'winners': winner_list}
    with Path(output).open('w') as f:
        json.dump(report, f)


def write_output(winners, lottery_template, output):
    print('Template: {}'.format(lottery_template['name']))
    print('Winners:')
    for winner, prize in winners:
        print('{} {}, {}'.format(winner['first_name'], winner['last_name'],
                                 prize['name']))

    if output:
        write_json_report(winners, lottery_template,  output)


@click.command(name='lotterycreator')
@click.argument('participants_file', required=True)
@click.option('--format', type=click.Choice(['json', 'csv']), default='json',
              help='Format of participants file')
@click.option('--template',
              help='Lottery template file (in lottery_templates directory)')
@click.option('--output', help='Output file for lottery report')
def main(participants_file, format, template, output):

    participants = load_participants_info(format, participants_file)
    lottery_template = load_lottery_template(template)
    winners = draw(participants, lottery_template)

    write_output(winners, lottery_template, output)


if __name__ == "__main__":
    main()
