import click
from inputhandlers import DataInputHandler
from reporthandler import print_readable_report, write_json_report


@click.command(name='lotterycreator')
@click.argument('participants_file', required=True)
@click.option('--format_', '--format', type=click.Choice(['json', 'csv']),
              default='json', help='Format of participants file')
@click.option('--template',
              help='Lottery template file (in lottery_templates directory)')
@click.option('--output', help='Output file for lottery report')
def main(participants_file, format_, template, output):
    input_handler = DataInputHandler()
    participants = input_handler.load_participants_info(
        format_, participants_file)
    lottery = input_handler.load_lottery_template(template)
    lottery.draw(participants)

    print_readable_report(lottery)
    if output:
        write_json_report(lottery, output)


if __name__ == "__main__":
    main()
