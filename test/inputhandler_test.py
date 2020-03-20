from inputhandlers import DataInputHandler, MalformedInputFileError
from mock import patch
from pytest import fixture, raises, mark
import pathlib


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

    @mark.parametrize('files, default', [
        (['bcd_template.json', 'abc_template.json'], 'abc_template'),
        (['def_template.json', 'power_template.json'], 'def_template'),
        (['def_template.json', 'abc_template.json'], 'abc_template'),
        (['power_template.json', 'def_template.json'], 'def_template'),
    ])
    @patch('pathlib.Path.iterdir')
    def test_load_lottery_template_default(self, mock_iterdir, input_handler,
                                           files, default):
        template_path = pathlib.Path(input_handler.data_dir).joinpath(
            'lottery_templates')
        pathlib.Path.iterdir.return_value = [
            template_path.joinpath(f)
            for f in files]

        template = input_handler.load_lottery_template(None)
        assert template.name == default

    @mark.parametrize('template_file',
                      ['abc_template.json', 'def_template.json'])
    def test_load_lottery_template(self, input_handler, template_file):
        template = input_handler.load_lottery_template(template_file)
        assert template_file.startswith(template.name)
