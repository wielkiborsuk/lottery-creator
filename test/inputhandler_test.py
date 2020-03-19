from json.decoder import JSONDecodeError
from inputhandlers import DataInputHandler
from pytest import fixture, raises


@fixture
def input_handler():
    handler = DataInputHandler()
    handler.data_dir = 'test/test_data'
    return handler


class TestInputHandler:
    def test_load_proper_json_file(self, input_handler):
        participants = input_handler.load_participants_info(
            'json', '3_participants.json')
        assert len(participants) == 3
        last_participant = participants[-1]
        assert last_participant.id == '3'
        assert last_participant.first_name == 'Sigmund'
        assert last_participant.last_name == 'Saw'
        assert last_participant.weight == 1.0

    def test_load_proper_csv_file_with_weights(self, input_handler):
        participants = input_handler.load_participants_info(
            'csv', '5_participants_weighted.csv')
        assert len(participants) == 5
        last_participant = participants[-1]
        assert last_participant.id == '5'
        assert last_participant.first_name == 'Carilyn'
        assert last_participant.last_name == 'Semper'
        assert last_participant.weight == 5.0

    def test_load_wrong_format_json(self, input_handler):
        with raises(JSONDecodeError):
            input_handler.load_participants_info(
                'json', '5_participants_weighted.csv')
