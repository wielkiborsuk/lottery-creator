import json
import random


def load_json_file(name):
    with open(name, 'r') as f:
        participants = json.load(f)
        return participants


def main():
    input_file = ''
    # file_format = ''
    winner_count = 1

    participants = load_json_file(input_file)
    weights = [float(p.get('weight', '1')) for p in participants]
    winners = random.choices(participants, weights=weights, k=winner_count)
    print(winners)


if __name__ == "__main__":
    main()
