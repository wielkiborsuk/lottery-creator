import json
import csv
import os
from pathlib import Path
from model import Participant, Prize, Lottery


class DataInputHandler(object):
    data_dir = os.environ.get('LOTTERY_DATA', '../data')

    @classmethod
    def __load_csv_file(cls, name):
        with open(name, 'r') as f:
            return list(csv.DictReader(f))

    @classmethod
    def __load_json_file(cls, name):
        with open(name, 'r') as f:
            participants = json.load(f)
            return participants

    @classmethod
    def load_participants_info(cls, format, name):
        file_path = Path(cls.data_dir).joinpath(name)

        participants_data = []
        if format == 'csv':
            participants_data = cls.__load_csv_file(file_path)
        elif format == 'json':
            participants_data = cls.__load_json_file(file_path)

        return [Participant(**p) for p in participants_data]

    @classmethod
    def load_lottery_template(cls, name):
        base_path = Path(cls.data_dir).joinpath('lottery_templates')

        if name:
            file_path = base_path.joinpath(name)
        else:
            file_path = sorted(base_path.iterdir())[0]

        with open(file_path, 'r') as f:
            template = json.load(f)
            prizes = [Prize(**p) for p in template['prizes']]

            return Lottery(template['name'], prizes)


class ReportHandler(object):
    @staticmethod
    def print_readable_report(lottery: Lottery):
        print('Template: {}'.format(lottery.name))
        print('Winners:')
        for winner, prize in lottery.winners:
            print('{} {}, {}'.format(winner.first_name, winner.last_name,
                                     prize.name))

    @staticmethod
    def write_json_report(lottery, output):
        winner_list = [{'participant': winner, 'prize': prize}
                       for (winner, prize) in lottery.winners]
        report = {'template_name': lottery.name,
                  'winners': winner_list}
        with Path(output).open('w') as f:
            json.dump(report, f)
