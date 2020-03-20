from inputhandlers import DataInputHandler, MalformedInputFileError
from mock import patch
from pytest import fixture, raises, mark


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
        with raises(MalformedInputFileError):
            input_handler.load_participants_info(
                'json', '5_participants_weighted.csv')

    def test_load_wrong_format_csv(self, input_handler):
        with raises(MalformedInputFileError):
            input_handler.load_participants_info(
                'csv', '3_participants.json')

    @patch('pathlib.Path.iterdir')
    @mark.parametrize("files", [["abc_template.json", "bcd_template.json"]])
    def test_load_lottery_template_default(self, input_handler, files):
        # TODO - work in progress
        input_handler.load_lottery_template('')
