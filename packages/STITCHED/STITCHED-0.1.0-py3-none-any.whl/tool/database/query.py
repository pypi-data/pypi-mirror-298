import argparse
from queryInterface import QueryInterface
import sqlite3

def display_query_results(column_names, result):
    print(column_names)
    for row in result:
        print(row)

def setup_get_dataset_text_labels_parser(subparsers):
    parser_get_dataset_text_labels = subparsers.add_parser('get_dataset_text_labels', help='Query the database')
    parser_get_dataset_text_labels.add_argument('--metadata', help='Whether the label definition, text source and language are needed', action='store_true')
    parser_get_dataset_text_labels.add_argument('--show-lines', type=int, default=10, help='Number of lines to show')
    parser_get_dataset_text_labels.add_argument('--save-to', type=str, help='Path to save the results')
def setup_query_sql_from_file_parser(subparsers):
    parser_query_sql_from_file = subparsers.add_parser('query_sql_from_file', help='Query the database using a SQL statement')
    parser_query_sql_from_file.add_argument('--read', type=str, help='Path to read the SQL command from')
    parser_query_sql_from_file.add_argument('--show-lines', type=int, default=10, help='Number of lines to show')
    parser_query_sql_from_file.add_argument('--save-to', type=str, help='Path to save the results')

if __name__ == '__main__':
    '''
    CommandLine:
    python query.py
    python query.py get_dataset_text_labels
    python query.py get_dataset_text_labels --metadata --show-lines 1 --save-to trial.csv
    
    python query.py query_sql_from_file --show-lines 1 --read sql_command.sql --save-to trial_sql.csv
    '''
    # connect to database
    path = '.\\hate_speech_data.db'
    conn = sqlite3.connect(path)
    queryInterface = QueryInterface(conn)
    # create parser
    parser = argparse.ArgumentParser(description="Command line interface for querying the database.")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    # set subparsers
    setup_get_dataset_text_labels_parser(subparsers)
    setup_query_sql_from_file_parser(subparsers)
    # parse arguments
    args = parser.parse_args()
    # process commands
    if args.command == 'get_dataset_text_labels':
        column_names, result = queryInterface.get_dataset_text_labels(metadata=args.metadata, show_lines=args.show_lines, file_path=args.save_to)
        display_query_results(column_names, result)
    if args.command == 'query_sql_from_file':
        if args.read is None:
            parser.error("The --read argument is required. Please provide a valid file path!")
        column_names, result = queryInterface.query_sql_from_file(sql_file=args.read, show_lines=args.show_lines, file_path=args.save_to)
        display_query_results(column_names, result)