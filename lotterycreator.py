import json
import csv
import random


def load_csv_file(name):
    with open(name, 'r') as f:
        lines = list(csv.reader(f))
        keys = lines[0]
        return [{keys[i]: line[i] for i in range(len(line))}
                for line in lines[1:]]


def load_json_file(name):
    with open(name, 'r') as f:
        participants = json.load(f)
        return participants


def load_participants_info(format, name):
    if format == 'csv':
        return load_csv_file(name)
    elif format == 'json':
        return load_json_file(name)
    else:
        return []


def draw(participants, winner_count):
    winners = []
    for i in range(winner_count):
        weights = [float(p.get('weight', '1')) for p in participants]
        (winner, ) = random.choices(participants, weights=weights)
        winners.append(winner)
        participants.remove(winner)
    return winners


def main():
    input_file = '../data/participants2.json'
    file_format = 'json'
    winner_count = 3

    participants = load_participants_info(file_format, input_file)
    winners = draw(participants, winner_count)
    for winner in winners:
        print('{} {}'.format(winner['first_name'], winner['last_name']))


if __name__ == "__main__":
    main()
