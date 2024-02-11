import csv
import datetime as dt

from prettytable import PrettyTable

from constants import BASE_DIR, DirConstants, LiteralConstants


def default_output(results, *args):
    for result in results:
        print(*result)


def file_output(results: list, cli_args, encoding='utf-8'):
    results_dir = BASE_DIR / DirConstants.RESULTS_DIR
    results_dir.mkdir(exist_ok=True)
    parser_mode = cli_args.mode
    current_time = dt.datetime.now().strftime(
        LiteralConstants.FILE_DATETIME_FORMAT
    )
    filename = f'{parser_mode}_{current_time}.csv'
    filepath = results_dir / filename
    with open(filepath, 'w', encoding=encoding) as file:
        csv.writer(file, dialect=csv.excel).writerows(results)


def pretty_output(results, *args):
    table = PrettyTable()
    table.field_names = results[0]
    table.align = 'l'
    table.add_rows(results[1:])
    print(table)


OUTPUT_MODES = {
    LiteralConstants.PRETTY_OUTPUT_MODE: pretty_output,
    LiteralConstants.FILE_OUTPUT_MODE: file_output,
    None: default_output
}


def control_output(results, cli_args):
    OUTPUT_MODES.get(cli_args.output)(results, cli_args)
