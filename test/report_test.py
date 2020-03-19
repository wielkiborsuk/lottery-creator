from reporthandler import write_json_report, print_readable_report
from model import Prize, Participant, Lottery
from pytest import fixture
import json


@fixture
def test_lottery():
    participants = [
        Participant(i, f'first{i}', f'last{i}', i)
        for i in range(10)
    ]
    prizes = [
        Prize(i, f'prize{i}', 2)
        for i in range(3)
    ]

    lottery = Lottery('test_lottery', prizes)
    lottery.draw(participants)
    return lottery


class TestRepotHandler:
    def test_json_report(self, tmp_path, test_lottery):
        output = tmp_path / 'output.json'
        write_json_report(test_lottery, output)

        with output.open('r') as f:
            report = json.load(f)

            assert report['template_name'] == 'test_lottery'
            assert len(report['winners']) == 6

            assert report['winners'][0]['prize'][0] == 0
            assert report['winners'][0]['prize'][1] == 'prize0'
            assert report['winners'][0]['prize'][2] == 1

            assert report['winners'][5]['prize'][0] == 2
            assert report['winners'][5]['prize'][1] == 'prize2'
            assert report['winners'][5]['prize'][2] == 1

    def test_readable_report_output(self, capsys, test_lottery):
        print_readable_report(test_lottery)
        captured = capsys.readouterr()
        assert 'Template: test_lottery' in captured.out
        assert 'Winners:' in captured.out
        assert 'prize0' in captured.out
        assert 'prize1' in captured.out
        assert 'prize2' in captured.out
