import csv
import os
class QueryInterface:
    def __init__(self, conn):
        self.conn = conn
        self.cur = conn.cursor()
    def __fetchall(self, query, params=()):
        self.cur.execute(query, params)
        result = self.cur.fetchall()
        column_names = [description[0] for description in self.cur.description]
        return column_names, result
    def __save_to_csv(self, column_names, result, file_path):
        with open(file_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(column_names)
            for row in result:
                # deal with None value
                row = [str(item) if item is not None else '' for item in row]
                writer.writerow(row)
    def __save_to_tsv(self, column_names, result, file_path):
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write('\t'.join(column_names) + '\n')
            for row in result:
                # deal with None value
                row = [str(item) if item is not None else '' for item in row]
                f.write('\t'.join(row) + '\n')
    def __save_query_result(self, column_names, result, file_path):
        _, file_extension = os.path.splitext(file_path)
        if file_extension == '.csv':
            self.__save_to_csv(column_names, result, file_path)
        elif file_extension.lower() == '.tsv':
            self.__save_to_tsv(column_names, result, file_path)
        else:
            raise ValueError("Unsupported file extension. Please use .csv or .tsv")
    def get_dataset_text_labels(self, show_lines, metadata = False, file_path=None):
        query = '''
        SELECT dataset.dataset_name, text.text, label.label_name, label.label_value
        FROM text
        JOIN dataset ON text.dataset_id = dataset.dataset_id
        JOIN label ON label.dataset_id = dataset.dataset_id AND label.text_id = text.text_id;
        '''
        if metadata:
            query = '''
            SELECT dataset.dataset_name, text.text, label.label_name, label.label_value, label.label_definition, text_source.source, language.language
            FROM text
            JOIN dataset ON text.dataset_id = dataset.dataset_id
            JOIN label ON label.dataset_id = dataset.dataset_id AND label.text_id = text.text_id
            JOIN text_source ON text_source.source_id = text.source_id
            JOIN language ON language.language_id = text.language_id
            '''
        column_names, result = self.__fetchall(query)
        if file_path is not None:
            self.__save_query_result(column_names, result, file_path)
        return column_names, result[:show_lines]



    # assuming that only for queries
    # currently only for one query
    def query_sql_from_file(self, sql_file, show_lines, file_path=None):
        try:
            with open(sql_file, 'r', encoding='utf-8') as file:
                sql_commands = file.read().split(';')
                sql_commands = [cmd.strip() for cmd in sql_commands if cmd.strip()]
                # Assert there's exactly one SQL command
                assert len(sql_commands) == 1, "Invalid file format. Expected exactly one SQL command."
                sql_command = sql_commands[0]
                column_names, result = self.__fetchall(sql_command)
                if file_path is not None:
                    self.__save_query_result(column_names, result, file_path)
                return column_names, result[:show_lines]
        except Exception as e:
            print("An error occurred while executing the SQL query:", str(e))
    def close(self):
        self.conn.close()