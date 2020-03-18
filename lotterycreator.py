import click
from iohandlers import DataInputHandler, ReportHandler


@click.command(name='lotterycreator')
@click.argument('participants_file', required=True)
@click.option('--format', type=click.Choice(['json', 'csv']), default='json',
              help='Format of participants file')
@click.option('--template',
              help='Lottery template file (in lottery_templates directory)')
@click.option('--output', help='Output file for lottery report')
def main(participants_file, format, template, output):
    participants = DataInputHandler.load_participants_info(
        format, participants_file)
    lottery = DataInputHandler.load_lottery_template(template)
    lottery.draw(participants)

    ReportHandler.print_readable_report(lottery)
    if output:
        ReportHandler.write_json_report(lottery, output)


if __name__ == "__main__":
    main()
