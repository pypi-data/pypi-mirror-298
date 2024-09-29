import unittest
import sqlite3
from tool.database.setup import setupSchema
from tool.loader.loader import DataLoader
from STITCHED.tool.loader.validator import Validator, ConfigValidator
import pandas as pd

class LoaderTestCase(unittest.TestCase):
    def test_dataset_storage_correctness(self):
        path = './hate_speech_data.db'
        conn = sqlite3.connect(path)

        setupSchema(conn)

        self.config_path = "config_generatorTest.csv"
        config = pd.read_csv(self.config_path)
        self.data_folder = "../data"

        self.validator = ConfigValidator(config_file=self.config_path, data_folder=self.data_folder)
        self.loader = DataLoader(conn=conn, validator=self.validator)

        self.assertIsInstance(self.loader, DataLoader)
        self.assertEqual(self.queryDB(conn, 'dataset'), 0)
        self.loader.storage_datasets()
        self.assertEqual(self.queryDB(conn, 'dataset'), len(config))

        text_label_count = self.count_text_label_per_dataset()
        self.assertEqual(self.queryDB(conn, 'text'),sum(sublist[0] for sublist in text_label_count))
        self.assertEqual(self.queryDB(conn,'label'),sum(sublist[0] * sublist[1] for sublist in text_label_count))

    def count_text_label_per_dataset(self):
        df_config = self.validator.read_and_prepare_config(self.config_path)
        res = []
        for idx, row in df_config.iterrows():
            filepath = self.data_folder + '/' + str(row['dataset_file_name'])
            df = self.validator.read_dataframe(filepath)
            res.append([len(df), len(row['label_name_definition'])])
        return res

    def queryDB(self,conn, table_name):
        cur = conn.cursor()
        cur.execute(f"SELECT COUNT(*) FROM {table_name}")
        return cur.fetchone()[0]


if __name__ == '__main__':
    unittest.main()
