import json
import csv
import os
from pathlib import Path
from model import Participant, Prize, Lottery


class DataInputHandler:
    data_dir = os.environ.get('LOTTERY_DATA', '../data')

    @classmethod
    def _load_csv_file(cls, name):
        with open(name, 'r') as f:
            participants = list(csv.DictReader(f))
            # CSV format doesn't allow strict validation, we can attempt this
            if not cls._participants_data_valid(participants):
                raise MalformedInputFileError
            return participants

    @staticmethod
    def _participants_data_valid(participants):
        keys = ('id', 'first_name', 'last_name')
        return participants and all(key in participants[0] for key in keys)

    @staticmethod
    def _load_json_file(name):
        try:
            with open(name, 'r') as f:
                participants = json.load(f)
                return participants
        except json.decoder.JSONDecodeError as e:
            raise MalformedInputFileError from e

    def load_participants_info(self, format, name):
        file_path = Path(self.data_dir).joinpath(name)

        participants_data = []
        if format == 'csv':
            participants_data = self._load_csv_file(file_path)
        elif format == 'json':
            participants_data = self._load_json_file(file_path)

        return [Participant(p['id'], p['first_name'],
                            p['last_name'], float(p.get('weight', 1)))
                for p in participants_data]

    def load_lottery_template(self, name):
        base_path = Path(self.data_dir).joinpath('lottery_templates')

        if name:
            file_path = base_path.joinpath(name)
        else:
            file_path = sorted(base_path.iterdir())[0]

        with open(file_path, 'r') as f:
            template = json.load(f)
            prizes = [Prize(p['id'], p['name'], p['amount'])
                      for p in template['prizes']]

            return Lottery(template['name'], prizes)


class MalformedInputFileError(ValueError):
    pass
